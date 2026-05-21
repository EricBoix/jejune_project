# Common utilities for graph extraction scripts
import os
import sys
import networkx as nx

from langchain_neo4j import Neo4jGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_ollama import ChatOllama
from neo4j import GraphDatabase
from dotenv import load_dotenv

DEBUG_PROMPT = "   "


def initialize_llm():
    load_dotenv()
    MODEL = os.environ["MODEL"]
    MODEL_URL = os.environ["MODEL_URL"]
    headers = {"Authorization": f'Bearer {os.environ["API_KEY"]}'}

    llm = ChatOllama(
        # Note: the following base_url will be auto-magically extended with
        # a trailing "/api/chat"
        base_url=MODEL_URL,
        model=MODEL,
        # How to pass authentication to OpenWebUI, refer to
        # - https://github.com/langchain-ai/langchain/issues/25055
        # - https://medium.com/learnwithrahul/running-ollama-remotely-in-a-secure-way-d14ba13c8d77
        # - https://docs.openwebui.com/getting-started/api-endpoints/
        client_kwargs={"headers": headers},
        temperature=0,
        format="json",
    )

    # Handshake test
    print(DEBUG_PROMPT + "Testing LLM connection...", end="", flush=True)
    try:
        response = llm.invoke('Reply with exactly: {"status": "ok"}')
        print(DEBUG_PROMPT + f" {response.content}")
    except Exception as e:
        print(f"\nFailed to connect to LLM at {MODEL_URL}.")
        print(f"Error: {e}")
        sys.exit(1)

    return llm


def extract_graph(llm, documents):
    llm_transformer = LLMGraphTransformer(llm=llm)
    print(DEBUG_PROMPT + "Graph extracting: starting...", flush=True)
    graph_documents = llm_transformer.convert_to_graph_documents(documents)
    print(DEBUG_PROMPT + "\nGraph extraction: done.")
    return graph_documents


def create_neo4j_database(graph_documents):
    graph = Neo4jGraph(
        username=os.environ["NEO4J_USERNAME"], password=os.environ["NEO4J_PASSWORD"]
    )

    print(DEBUG_PROMPT + "Resulting graph: ", graph_documents[0])
    graph.add_graph_documents(
        graph_documents, baseEntityLabel=True, include_source=True
    )

    driver = GraphDatabase.driver(
        uri=os.environ["NEO4J_URI"],
        auth=(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"]),
    )

    def create_fulltext_index(tx):
        # Note : "IF NOT EXISTS" is appended to the query in order to prevents
        # an exception to be thrown should a full-text index on the same schema
        # already exist (probably because of a previous run of this script).
        query = """
        CREATE FULLTEXT INDEX `fulltext_entity_id` IF NOT EXISTS
        FOR (n:__Entity__)
        ON EACH [n.id];
        """
        tx.run(query)

    try:
        with driver.session() as session:
            session.execute_write(create_fulltext_index)
            print(DEBUG_PROMPT + "Neo4j database fulltext index successfully created.")
    except Exception as e:
        print(DEBUG_PROMPT + "Neo4j database fulltext index creation failed.")
        print(DEBUG_PROMPT + "Exception: ", repr(e))
        pass

    driver.close()
