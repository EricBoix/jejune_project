# This code is derived from
#   https://github.com/Coding-Crashkurse/GraphRAG-with-Llama-3.1.git
import os
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_neo4j import Neo4jGraph
from langchain_community.vectorstores import Neo4jVector
from langchain_ollama import OllamaEmbeddings, ChatOllama
from extract_from_knowledge_graph import extract_entities_from_question, graph_retriever
from dotenv import load_dotenv

if __name__ == "__main__":
    DEBUG_PROMPT = ""

    ############################# Retrieve script context and parameters
    load_dotenv()

    graph = Neo4jGraph(
        username=os.environ["NEO4J_USERNAME"], password=os.environ["NEO4J_PASSWORD"]
    )
    MODEL = os.environ["MODEL"]
    MODEL_URL = os.environ["MODEL_URL"]
    HEADERS = {"Authorization": f'Bearer {os.environ["API_KEY"]}'}

    ############################# Then, consider a user given main question,
    # given in Natural Language, and
    # 1. make an graph/embedding-space hybrid search to collect elements of
    #    answer with the help of both structures
    # 2. synthesize those elements of answer with some llm
    # 3. provide the resulting Natural Language response
    main_question = (
        "Who is Nonna Lucia? Did she teach anyone about restaurants or cooking?"
    )

    ############################ Build the various required software components

    ##### First, build a vector retriever that will search the embedding space
    # for vectors that are close enough to the question
    embeddings = OllamaEmbeddings(
        base_url=MODEL_URL,
        model="mxbai-embed-large:latest",
        client_kwargs={"headers": HEADERS},
    )
    vector_index = Neo4jVector.from_existing_graph(
        embedding=embeddings,
        search_type="hybrid",
        node_label="Document",
        text_node_properties=["text"],
        embedding_node_property="embedding",
    )
    vector_retriever = vector_index.as_retriever()

    ##### Provide a function does an graph/embedding hybrid search, that is
    # 1. searches the graph structure: the function retrieves, within the graph,
    #    the neighbors of the entities encountered in the argument question
    # 2. searches the embedding (vector) space for (text) vectors that are
    #    "close" to the argument question (usual RAG approach, which breaks
    #    text into chunks, vectorizes them, and stores them in a vector store,
    #    and then compares the similarity by vectorizing the user’s query)
    # 3. blends both results (GraphRAG) within a text (as a shallowly structured
    #    sentence) to be provided as context for the llm.
    # Note: many global scope variables (e.g. MODEL or graph) are implicitly
    # passed/imported/transmitted to full_retriever which is not a
    # recommendable practice.
    def full_retriever(question: str):
        concerned_entities = extract_entities_from_question(
            MODEL, MODEL_URL, HEADERS, question
        )
        graph_data = graph_retriever(graph, concerned_entities)
        vector_data = [el.page_content for el in vector_retriever.invoke(question)]
        final_data = f"""Graph data:
    {graph_data}
    vector data:
    {"#Document ". join(vector_data)}
        """
        return final_data

    ##### Define the prompt for the (langchain based) prompt
    template = """Answer the question based only on the following context:
    {context}

    Question: {question}
    Use natural language and be concise.
    Answer:"""

    prompt = ChatPromptTemplate.from_template(template)

    ##### Eventually build an LLM to be used to synthesize the elements of
    # answer that will be collected both within embedding space and within
    # graph neighborhood
    llm = ChatOllama(
        # Note: the following base_url will be auto-magically extended with
        # a trailing "/api/chat"
        base_url=MODEL_URL,
        model=MODEL,
        # How to pass authentication to OpenWebUI, refer to
        # - https://github.com/langchain-ai/langchain/issues/25055
        # - https://medium.com/learnwithrahul/running-ollama-remotely-in-a-secure-way-d14ba13c8d77
        # - https://docs.openwebui.com/getting-started/api-endpoints/
        client_kwargs={"headers": HEADERS},
        temperature=0,
        format="json",
    )

    ################################## Define the chain of treatment and run it
    chain = (
        {
            "context": full_retriever,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    answer = chain.invoke(input=main_question)
    print(DEBUG_PROMPT, answer)
