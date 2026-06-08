# Neo4j to RDF file exportation utility

## Purpose

The purpose of this directory is to implement a Neo4j database exportation code that

- logs into a neo4j database (using the authentication info provided in a `.env`file)
- collects all the nodes and edges
- exports this content to a newly created RDF file (using the Turtle format)
- can be easily customized (node/edge filtering) and thus written in Python

## Setup

```bash
# Prepare the virtual environment
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

or equivalently run `make setup` and `source venv/bin/activate`

```bash
cp .env.example .env
```

and edit the resulting `.env` file to set your Neo4j credentials e.g.

```bash
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
```

## Usage

Launch a live instance of Neo4j database server: refer e.g. to [https://github.com/EricBoix/jj_neo4j_docker](https://github.com/EricBoix/jj_neo4j_docker).

Then use

```bash
python neo4j_to_rdf.py              # Default output written to `output.ttl`
python neo4j_to_rdf.py graph.ttl    # Custom filename given as output path
```

## RDF Mapping

- **Namespaces**: `ex:` = `http://example.org/graph/`,
  `neo:` = `http://example.org/neo4j/`
- **Nodes**: `ex:node_{id}` with `rdf:type neo:Label` and property literals
- **Relationships without properties**: direct triple
  `ex:node_src neo:REL_TYPE ex:node_tgt`
- **Relationships with properties**: direct triple plus reification
  via `rdf:Statement` blank node carrying the property literals

## Devel debug notes

```bash

```