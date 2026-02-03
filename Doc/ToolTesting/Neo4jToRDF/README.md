# Neo4j to RDF file exportation utility

## Purpose

The purpose of this directory is to implement a Neo4j database exportation code  that 

- is written in Python
- logs into a neo4j database (using the authentication info provided in a `.env`file)
- collects all the nodes and edges
- exports this content to a newly created RDF file (using the Turtle format)

## Setup

```bash
# Prepare the virtual environment
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with your Neo4j credentials e.g.

```bash
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
```

## Usage

Launch a live instance of Neo4j database server. For example simply trigger the `docker compose` demo located in [`Neo4jVisjsDocker/FromBackup`](../Neo4jVisjsDocker/FromBackup/README.md) located in this git repository.
Then use

```bash
python neo4j_to_rdf.py              # writes output.ttl
python neo4j_to_rdf.py graph.ttl    # custom output path
```

## RDF Mapping

- **Namespaces**: `ex:` = `http://example.org/graph/`,
  `neo:` = `http://example.org/neo4j/`
- **Nodes**: `ex:node_{id}` with `rdf:type neo:Label` and property literals
- **Relationships without properties**: direct triple
  `ex:node_src neo:REL_TYPE ex:node_tgt`
- **Relationships with properties**: direct triple plus reification
  via `rdf:Statement` blank node carrying the property literals
