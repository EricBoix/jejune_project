# Progress

## Done

- Created `requirements.txt` (neo4j, rdflib, python-dotenv)
- Created `.env.example` with credential template
- Created `.gitignore` (.env, \_\_pycache\_\_, output.ttl)
- Created `neo4j_to_rdf.py` implementing full export pipeline:
  - Loads credentials from `.env`, fails fast on missing vars
  - Connects to Neo4j, verifies connectivity
  - Queries all nodes (labels + properties) and relationships
  - Maps to RDF triples using `ex:` and `neo:` namespaces
  - Reifies relationships that carry properties
  - Serializes to Turtle format
  - CLI arg for output path (default `output.ttl`)

## Next

- Test against a live Neo4j instance
