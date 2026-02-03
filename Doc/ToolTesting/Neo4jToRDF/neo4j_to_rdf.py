"""Export a Neo4j database to an RDF file in Turtle format."""

import os
import re
import sys

from dotenv import load_dotenv
from neo4j import GraphDatabase
from rdflib import BNode, Graph, Literal, Namespace, RDF, URIRef, XSD


EX = Namespace("http://example.org/graph/")
NEO = Namespace("http://example.org/neo4j/")

_SANITIZE_RE = re.compile(r"[^A-Za-z0-9_]")


def _sanitize(element_id: str) -> str:
    """Turn an element ID into a safe URI local name."""
    return _SANITIZE_RE.sub("_", element_id)


def _node_uri(element_id: str) -> URIRef:
    return EX[f"node_{_sanitize(element_id)}"]


def _predicate(name: str) -> URIRef:
    return NEO[_SANITIZE_RE.sub("_", name)]


def _to_literal(value):
    """Convert a Python value to an rdflib Literal with an XSD type."""
    if isinstance(value, bool):
        return Literal(value, datatype=XSD.boolean)
    if isinstance(value, int):
        return Literal(value, datatype=XSD.integer)
    if isinstance(value, float):
        return Literal(value, datatype=XSD.double)
    return Literal(str(value), datatype=XSD.string)


def _add_properties(g: Graph, subject, props: dict):
    """Add property triples for a subject, expanding lists."""
    for key, value in props.items():
        if value is None:
            continue
        pred = _predicate(key)
        if isinstance(value, list):
            for item in value:
                if item is not None:
                    g.add((subject, pred, _to_literal(item)))
        else:
            g.add((subject, pred, _to_literal(value)))


def build_graph(driver) -> tuple[Graph, dict]:
    """Query Neo4j and return an rdflib Graph plus summary counts."""
    g = Graph()
    g.bind("ex", EX)
    g.bind("neo", NEO)

    node_count = 0
    rel_count = 0

    with driver.session() as session:
        # --- Nodes ---
        result = session.run(
            "MATCH (n) RETURN elementId(n) AS eid, labels(n) AS labels, properties(n) AS props"
        )
        for record in result:
            node_count += 1
            # The embedding property of a node is a lengthy vector that we
            # can later retrieve in the Neo4j DB
            if "embedding" in record["props"].keys():
                del record["props"]["embedding"]
            uri = _node_uri(record["eid"])
            for label in record["labels"]:
                g.add((uri, RDF.type, NEO[_SANITIZE_RE.sub("_", label)]))
            _add_properties(g, uri, record["props"])

        # --- Relationships ---
        result = session.run(
            "MATCH (a)-[r]->(b) "
            "RETURN elementId(a) AS src, elementId(b) AS tgt, "
            "type(r) AS rtype, properties(r) AS props"
        )
        for record in result:
            rel_count += 1
            src = _node_uri(record["src"])
            tgt = _node_uri(record["tgt"])
            pred = _predicate(record["rtype"])
            props = record["props"]

            # Always emit the direct triple
            g.add((src, pred, tgt))

            # Reify when the relationship carries properties
            if props:
                stmt = BNode()
                g.add((stmt, RDF.type, RDF.Statement))
                g.add((stmt, RDF.subject, src))
                g.add((stmt, RDF.predicate, pred))
                g.add((stmt, RDF.object, tgt))
                _add_properties(g, stmt, props)

    return g, {"nodes": node_count, "relationships": rel_count, "triples": len(g)}


def main():
    load_dotenv()

    uri = os.environ.get("NEO4J_URI")
    username = os.environ.get("NEO4J_USERNAME")
    password = os.environ.get("NEO4J_PASSWORD")

    missing = [
        v
        for v, val in [
            ("NEO4J_URI", uri),
            ("NEO4J_USERNAME", username),
            ("NEO4J_PASSWORD", password),
        ]
        if not val
    ]
    if missing:
        sys.exit(f"Missing environment variables: {', '.join(missing)}")

    output_path = sys.argv[1] if len(sys.argv) > 1 else "output.ttl"

    driver = GraphDatabase.driver(uri, auth=(username, password))
    try:
        driver.verify_connectivity()
        print(f"Connected to {uri}")

        g, summary = build_graph(driver)
        g.serialize(destination=output_path, format="turtle")

        print(
            f"Exported {summary['nodes']} nodes, "
            f"{summary['relationships']} relationships "
            f"({summary['triples']} triples) to {output_path}"
        )
    finally:
        driver.close()


if __name__ == "__main__":
    main()
