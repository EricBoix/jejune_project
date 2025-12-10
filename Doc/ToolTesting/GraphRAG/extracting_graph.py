# This code is derived from
#   https://github.com/Coding-Crashkurse/GraphRAG-with-Llama-3.1.git
import os
from langchain_neo4j import Neo4jGraph
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.graph_transformers import LLMGraphTransformer
from neo4j import GraphDatabase
from langchain_community.vectorstores import Neo4jVector
from langchain_community.document_loaders import TextLoader
from langchain_ollama import OllamaEmbeddings, ChatOllama
from dotenv import load_dotenv

DEBUG_PROMPT = "   "

# Retrieve script context and parameters
load_dotenv()

graph = Neo4jGraph(
    username=os.environ["NEO4J_USERNAME"], password=os.environ["NEO4J_PASSWORD"]
)
MODEL = os.environ["MODEL"]
MODEL_URL = os.environ["MODEL_URL"]
headers = {"Authorization": f'Bearer {os.environ["API_KEY"]}'}

# Load the original text an start graph extraction
loader = TextLoader(file_path="dummytext.txt")
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=24)
documents = text_splitter.split_documents(documents=docs)

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

llm_transformer = LLMGraphTransformer(llm=llm)

print(DEBUG_PROMPT + "Extracting graph :", end="", flush=True)
graph_documents = llm_transformer.convert_to_graph_documents(documents)
print(DEBUG_PROMPT + "\nGraph extracted.")
print(DEBUG_PROMPT + "Resulting graph: ", graph_documents[0])
graph.add_graph_documents(graph_documents, baseEntityLabel=True, include_source=True)

embeddings = OllamaEmbeddings(
    base_url=MODEL_URL,
    model="mxbai-embed-large:latest",
    client_kwargs={"headers": headers},
)

vector_index = Neo4jVector.from_existing_graph(
    embedding=embeddings,
    search_type="hybrid",
    node_label="Document",
    text_node_properties=["text"],
    embedding_node_property="embedding",
)
vector_retriever = vector_index.as_retriever()

### Proceed with database creation
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


# Index creation
try:
    with driver.session() as session:
        session.execute_write(create_fulltext_index)
        print(DEBUG_PROMPT + "Neo4j database fulltext index created successfully.")
except Exception as e:
    print(DEBUG_PROMPT + "Neo4j database fulltext index creation failed.")
    print(DEBUG_PROMPT + "Exception: ", repr(e))
    # print(DEBUG_PROMPT + "Exiting.")
    # sys.exit(1)
    pass

# Close the driver connection (writing the database)
driver.close()
