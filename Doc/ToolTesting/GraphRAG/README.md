# Hands on lowbrow exploration of GraphRAG in Python

## Introduction

This directory explores, with a direct hands-on approach, a process of graph extraction (and exploitation) that is described in the ["Local GraphRAG with LLaMa 3.1 - LangChain, Ollama & Neo4j" youtube tutorial](https://www.youtube.com/watch?v=nkbyD4joa0A).
The original associated code, from which this work is partly derived, is available through [this Coding Crash Courses git repository](https://github.com/Coding-Crashkurse/GraphRAG-with-Llama-3.1.git).

## Running things

1. Launch a Neo4j database (to collect the extracted graph)

    ```bash
    # Prepare the virtual environment
    python3.10 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    # Launch the Neo4j database
    docker compose up --detach
    ```

1. Transmit to the extracting python code the required configuration elements (neo4j database and llm server accesses) by
   - copying the [`env-reference` file](./env-reference) to a `.env` file
   - customize the resulting  `.env` file by configuring (at least) the entries mentioning the `CHANGE_ME` string.

1. Realize the graph extraction

    ```bash
    # Extract the graph and store it in database
    python extracting_graph.py
    ```

    (or `python extracting_graph.py > extract.log &` when the extracting is too lengthy or running on a remote server).

    Note: when ran on `2017_-_Culadasa_John_Yates-Matthew_Immergut-Jeremy_Graves_-_The_Mind_Illuminated_-_llamaparse_raw_conversion.md` this script will trigger ~5800 llm calls.

### Visually explore the resulting knowledge graph (with neo4j web UI)

Interactively explore the extracted graph through neo4j web UI

```bash
# For exact hostname/port refer to the NEO4J_URI entry of your `/.env` # configuration file):
open http://localhost:7474/
```

Run [`cypher (queries)`](https://neo4j.com/docs/cypher-manual/current/introduction/) like

```bash
$:server connect   # Assert the UI is connected to the proper db server
                    # (has to match what was configured in you .env file)
:use neo4j         # Make sure you are connect to the right database
                    # (has to match what was configured in you .env file)
neo4j$ MATCH (n) RETURN n  # Displays the full extracted graph 
```

### Use the knowledge graph programmatically

For example search the graph database with a Natural Language query by running the provided python script

```bash
python extract_from_knowledge_graph.py
```

Or search both the knowledge graph and the embedding space structures with

```bash
python vector_and_graph_hybrid_search.py
```

### Dump the database content for later usage

The following is a direct application of the [dump and load neo4j examples](https://neo4j.com/docs/operations-manual/current/docker/dump-load/)

```bash
docker compose down     # Database dump requires being "offline"
docker run --interactive --tty --rm  \
           --volume=`pwd`/data:/data \       # Has to match docker-compose.yaml
           --volume=`pwd`/backups:/backups \ # Sub-directory where dumps end up
           neo4j/neo4j-admin neo4j-admin database dump neo4j --to-path=/backups
```

and check the `backup/` sub-directory for the new existence of `neo4j.dump` file.

```bash
rm -fr data     # WARNING: this deletes all your databases !
docker run --interactive --tty --rm \
    --volume=`pwd`/data:/data \
    --volume=`pwd`/backups:/backups \
    neo4j/neo4j-admin neo4j-admin database load neo4j --from-path=/backups
docker compose up --detach
```

Some (neo4j's Cypher) queries

- `neo4j$ MATCH (n) RETURN n` to display all the nodes (caveat emptor: within the UI settings the "Initial node display" integer parameter controls the number of nodes displayed which, by default, is set to 300)
- `MATCH (n) WHERE n:Person RETURN n` to display the nodes with the "Person" label
- `MATCH (n) WHERE NOT n:Person RETURN n` to display the nodes not having the "Person" label
- `MATCH (n) WHERE NOT(SIZE(LABELS(n)) = 1 AND n:Document) RETURN n` to display the nodes not having "Document" as single label
- `MATCH (n) WHERE NOT(SIZE(LABELS(n)) = 1 AND n:Document) and NOT n:Person RETURN n` ...

## References

- [GraphRAG: The Marriage of Knowledge Graphs and RAG: Emil Eifrem](https://www.youtube.com/watch?v=knDDGYHnnSI)
- [Introduction to Neo4j](https://www.youtube.com/watch?v=YDWkPFijKQ4cdt)
- [Build a RAG agent with LangChain](https://docs.langchain.com/oss/python/langchain/rag#ollama)
- Calling [LLM through OpenwebUI examples](https://github.com/UDL-LIRIS/python-openwebui-bootstraping-examples)

## Next steps

### Improve observability

For the time being, tracing LLM calls (which is the minimum required for observability) is done by patching
`venv/lib/python3.10/site-packages/langchain_ollama/chat_models.py` and adding the following line at line 947

```python
print(" (chat client call) ", end='', flush=True)  # EBO was here: added
```

Instead, (and because [LangSmith (IBM docs)](https://www.ibm.com/think/topics/langsmith) is [expensive](https://www.metacto.com/blogs/the-true-cost-of-langsmith-a-comprehensive-pricing-integration-guide)), a cleaner way consists in

- using [OpenLLMetry](https://github.com/traceloop/openllmetry)
- deploying a [docker based OpenTelemetry backend](https://opentelemetry.io/docs/demo/docker-deployment/)

### Improve the (graph) extraction process

[Read this and improve the script](https://neo4j.com/blog/developer/knowledge-graph-extraction-challenges/)

### Ingesting a Markdown file

- Use [LangChain's `UnstructuredMarkdownLoader`](https://docs.langchain.com/oss/python/integrations/document_loaders/unstructured_markdown)
