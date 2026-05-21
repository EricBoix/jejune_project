import os
import sys
from dotenv import load_dotenv

import neo4j
import networkx as nx

DEBUG_PROMPT = "  "


def graph_from_cypher(neo4j_graph):
    # Source - https://stackoverflow.com/a/63658690
    # a.k.a. https://stackoverflow.com/questions/59289134/constructing-networkx-graph-from-neo4j-query-result
    # Posted by F.Z
    # Retrieved 2026-05-21, License - CC BY-SA 4.0
    """
    Constructs a networkx graph from the results of a neo4j cypher query.
    """

    G = nx.MultiDiGraph()
    nodes = list(neo4j_graph._nodes.values())
    for node in nodes:
        G.add_node(node.element_id, labels=node._labels, properties=node._properties)

    relations = list(neo4j_graph._relationships.values())
    for rel in relations:
        G.add_edge(
            rel.start_node.element_id,
            rel.end_node.element_id,
            key=rel.element_id,
            type=rel.type,
            properties=rel._properties,
        )
    return G


def display_graph_main_characteristics(nx_graph):
    # Source: https://medium.com/thedeephub/cleaning-llm-generated-knowledge-graphs-to-improve-data-quality-2b5caa1ae4dc
    if not isinstance(nx_graph, nx.MultiDiGraph):
        print(DEBUG_PROMPT + "Expected a NetworkX MultiDiGraph. Exiting.")
        sys.exit()

    num_nodes = nx.number_of_nodes(nx_graph)
    print(DEBUG_PROMPT + "Number of nodes: " + str(num_nodes))
    print(
        DEBUG_PROMPT + "Number of relationships: " + str(nx.number_of_edges(nx_graph))
    )

    centrality = {}
    for node in nx_graph.nodes():
        degree = nx_graph.degree(node)
        centrality[node] = degree / (num_nodes - 1)
    sorted_centrality = sorted(centrality.items(), key=lambda item: item[1])

    # Print ten most central nodes (together with their centrality):
    labels = nx.get_node_attributes(nx_graph, "labels")
    properties = nx.get_node_attributes(nx_graph, "properties")

    for node, cent in sorted_centrality[-50:]:
        print(
            DEBUG_PROMPT
            + f"Node centrality = {cent:.4f}, name: {properties[node]['id']}, labels: {labels[node]}"
        )


if __name__ == "__main__":
    load_dotenv()

    print(DEBUG_PROMPT + "Using neo4j DB: " + os.environ["NEO4J_URI"])
    driver = neo4j.GraphDatabase.driver(
        uri=os.environ["NEO4J_URI"],
        auth=(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"]),
    )

    query = """
    MATCH (n) OPTIONAL MATCH (n)-[r]-(c) RETURN n,r,c
    """

    with driver.session() as session:
        result = session.run(query)
        G = graph_from_cypher(result.graph())
        display_graph_main_characteristics(G)
