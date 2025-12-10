# This code is derived from
#   https://github.com/Coding-Crashkurse/GraphRAG-with-Llama-3.1.git
import os
from pydantic import BaseModel, Field
from langchain_neo4j import Neo4jGraph
from langchain_ollama import ChatOllama
from dotenv import load_dotenv


def extract_entities_from_question(model, model_url, headers, question):
    """Build an llm (with the model, model_url and headers argument) and use
    that llm to extract the list of entities encountered in the question"""

    class Entities(BaseModel):
        """Identifying information about entities."""

        names: list[str] = Field(
            ...,
            description="All the person, organization, or business entities that "
            "appear in the text",
        )

    llm = ChatOllama(
        # Note: the following base_url will be auto-magically extended with
        # a trailing "/api/chat"
        base_url=model_url,
        model=model,
        # How to pass authentication to OpenWebUI, refer to
        # - https://github.com/langchain-ai/langchain/issues/25055
        # - https://medium.com/learnwithrahul/running-ollama-remotely-in-a-secure-way-d14ba13c8d77
        # - https://docs.openwebui.com/getting-started/api-endpoints/
        client_kwargs={"headers": headers},
        temperature=0,
        format="json",
    )
    entity_chain = llm.with_structured_output(Entities)
    answer = entity_chain.invoke(question)
    return answer.names


def graph_retriever(graph, entities: str) -> str:
    """
    Collects the graph neighborhood of entities that were given as argument
    """
    result = ""
    for entity in entities:
        response = graph.query(
            """CALL db.index.fulltext.queryNodes('fulltext_entity_id', $query, {limit:2})
            YIELD node,score
            CALL {
              WITH node
              MATCH (node)-[r:!MENTIONS]->(neighbor)
              RETURN node.id + ' - ' + type(r) + ' -> ' + neighbor.id AS output
              UNION ALL
              WITH node
              MATCH (node)<-[r:!MENTIONS]-(neighbor)
              RETURN neighbor.id + ' - ' + type(r) + ' -> ' +  node.id AS output
            }
            RETURN output LIMIT 50
            """,
            {"query": entity},
        )
        result += "\n".join([el["output"] for el in response])
    return result


if __name__ == "__main__":
    DEBUG_PROMPT = ""

    ############################# Retrieve script context, tools and parameters
    load_dotenv()

    graph = Neo4jGraph(
        username=os.environ["NEO4J_USERNAME"], password=os.environ["NEO4J_PASSWORD"]
    )
    MODEL = os.environ["MODEL"]
    MODEL_URL = os.environ["MODEL_URL"]
    HEADERS = {"Authorization": f'Bearer {os.environ["API_KEY"]}'}

    ######################### Then, consider a user given question given in
    # Natural Language and extract (by using NLP with the considered llm) from
    # that question the entities/names that the question is concerned with.
    # For the question considered bellow the list of concerned entities is
    # reduced to [ "Nonna Lucia" ].
    question = "Who is Nonna Lucia?"
    concerned_entities = extract_entities_from_question(
        MODEL, MODEL_URL, HEADERS, question
    )
    print(
        DEBUG_PROMPT + " Look within the graph for info concerning : ",
        concerned_entities,
    )

    #### Then use the graph structure to retrieve information about the
    # concerned entities
    answer = graph_retriever(graph, concerned_entities)
    print(DEBUG_PROMPT + " Graph response: ", answer)
