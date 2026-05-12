# It focuses on providing a (hopefully) more refined breakdown of the
# original document than the one offered by langchain's
# RecursiveCharacterTextSplitter algorithm.
# Note: this code is derived from
#   https://github.com/Coding-Crashkurse/GraphRAG-with-Llama-3.1.git
import argparse
import json
import os
import sys

from langchain_neo4j import Neo4jGraph
from langchain_text_splitters import MarkdownTextSplitter
from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer
from neo4j import GraphDatabase
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

DEBUG_PROMPT = "   "


def load_documents_from_json(json_path):
    def as_document(dct):
        if "__document__" in dct:
            return Document(metadata=dct["metadata"], page_content=dct["page_content"])
        return dct

    with open(json_path, "r") as in_file:
        try:
            documents = json.load(fp=in_file, object_hook=as_document)
        except ValueError as e:
            print(DEBUG_PROMPT, "Invalid json: %s" % e)
            sys.exit()
    return documents


def load_documents_from_markdown(file_path):
    loader = UnstructuredMarkdownLoader(file_path=file_path)
    docs = loader.load()
    text_splitter = MarkdownTextSplitter()
    documents = text_splitter.split_documents(documents=docs)
    return documents


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Extract graph from documents using LLM and store in Neo4j."
    )
    parser.add_argument(
        "--input_directory",
        type=str,
        metavar="DIR",
        help="Directory to prefix to all loaded file paths.",
    )
    parser.add_argument(
        "--load_json_document",
        type=str,
        metavar="JSON_FILE",
        help="Load documents from a JSON file instead of parsing markdown.",
    )
    parser.add_argument(
        "--load_markdown_document",
        type=str,
        metavar="MARKDOWN_FILE",
        help="Load documents from a markdown file.",
    )
    args = parser.parse_args()

    if args.load_json_document:
        if args.input_directory:
            args.json_file_path = os.path.join(
                args.input_directory, args.load_json_document
            )
        else:
            args.json_file_path = args.load_json_document

    if args.load_markdown_document:
        if args.input_directory:
            args.markdown_file_path = os.path.join(
                args.input_directory, args.load_markdown_document
            )
        else:
            args.markdown_file_path = args.load_markdown_document

    return args


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
            print(DEBUG_PROMPT + "Neo4j database fulltext index created successfully.")
    except Exception as e:
        print(DEBUG_PROMPT + "Neo4j database fulltext index creation failed.")
        print(DEBUG_PROMPT + "Exception: ", repr(e))
        pass

    driver.close()


def main():
    args = parse_arguments()

    documents = []  # The breakdown elements for LLMGraphTransformer algorithm
    if hasattr(args, "json_file_path"):
        documents.extend(load_documents_from_json(args.json_file_path))
    if hasattr(args, "markdown_file_path"):
        documents.extend(load_documents_from_markdown(args.markdown_file_path))
    if not documents:
        print(DEBUG_PROMPT + "No documents loaded. Exiting.")
        sys.exit()
    else:
        print(
            DEBUG_PROMPT + "Number of documents for LLMGraphTransformer to deal with: ",
            len(documents),
        )

    # Proceed with graph extraction per se
    llm = initialize_llm()
    llm_transformer = LLMGraphTransformer(llm=llm)
    print(DEBUG_PROMPT + "Extracting graph :", end="", flush=True)
    graph_documents = llm_transformer.convert_to_graph_documents(documents)
    print(DEBUG_PROMPT + "\nGraph extracted.")

    create_neo4j_database(graph_documents)


if __name__ == "__main__":
    main()
