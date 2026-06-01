# Hands on lowbrow exploration of GraphRAG in Python<!-- omit in toc -->

- [Introduction](#introduction)
- [Running things: the simple extraction use case](#running-things-the-simple-extraction-use-case)
  - [Notes](#notes)
- [Further advanced document "chunkings"](#further-advanced-document-chunkings)
- [Visually explore the resulting knowledge graph (with neo4j web UI)](#visually-explore-the-resulting-knowledge-graph-with-neo4j-web-ui)
- [Use the knowledge graph programmatically](#use-the-knowledge-graph-programmatically)
  - [Displaying knowledge graph main characteristics](#displaying-knowledge-graph-main-characteristics)
  - [Searching the database](#searching-the-database)
- [Dump/Restore the database content for later usage](#dumprestore-the-database-content-for-later-usage)
- [Scripting things](#scripting-things)
  - [Collecting Gold Dust](#collecting-gold-dust)
- [References](#references)
- [Next steps](#next-steps)
  - [Improve observability](#improve-observability)
  - [Improve the (graph) extraction process](#improve-the-graph-extraction-process)
  - [Ingesting a Markdown file](#ingesting-a-markdown-file)

## Introduction

This directory explores, with a direct hands-on approach, a process of graph extraction (and exploitation) that is described in the ["Local GraphRAG with LLaMa 3.1 - LangChain, Ollama & Neo4j" youtube tutorial](https://www.youtube.com/watch?v=nkbyD4joa0A).
The original associated code, from which this work is partly derived, is available through [this Coding Crash Courses git repository](https://github.com/Coding-Crashkurse/GraphRAG-with-Llama-3.1.git).

## Running things: the simple extraction use case

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
    python extracting_graph.py \
    --input_directory ../../../Data/ISBN_978-1-5011-5698-4_-_The_Mind_Illuminated/result_data/ \
    --load_markdown_document 2017_-_Culadasa_John_Yates-Matthew_Immergut-Jeremy_Graves_-_The_Mind_Illuminated_-_llamaparse_manually_fixed.md
    ```

### Notes

- when the extraction is too lengthy (or running on a remote ssh server) consider using

    ```bash
    python extracting_graph.py [...] > extract.log &
    tail -f extract.log
    ```

- when a pre-existing neo4j database content exists (look a the content of the `./data` directory), and depending on your filesystem rights setup) you might get an error message on

    ```bash
    docker run --interactive --tty --rm --volume=`pwd`/data:/data neo4j /usr/bin/rm -fr /data/*
    rmdir ./data
    ```

- when ran on `2017_-_Culadasa_John_Yates-Matthew_Immergut-Jeremy_Graves_-_The_Mind_Illuminated_-_llamaparse_raw_conversion.md` this script will trigger **~5800 llm calls**.

## Further advanced document "chunkings"

If you wish to break down the original document in chunks that follow the sentence structure (as opposed to evenly sized chunks with some overlap) use the following script (that depends on the output of [Collecting Gold Dust conversion](https://github.com/EricBoix/jj_doc_Collecting_Gold_Dust/blob/main/Readme.md)) :

```bash
python extracting_graph_semantic_chuncker.py \
--input_directory ../../../Data/ISBN_978-0-9835844-5-2_-_Collecting_Gold_Dust/ \
--load_markdown_document result_data/2019_-_Sayadaw-U-Tejaniya-Collecting-Gold-Dust-Web-Book-1_-_local_converter.md \
--load_json_document result_data/2019_-_Sayadaw-U-Tejaniya-Collecting-Gold-Dust-Web-Book-1_-_Sentences_as_LangChain_Document.json
```

## Visually explore the resulting knowledge graph (with neo4j web UI)

Interactively explore the extracted graph through neo4j web UI

```bash
# For exact hostname/port refer to the NEO4J_URI entry of your `/.env` # configuration file):
open http://localhost:7474/
```

Run [`cypher (queries)`](https://neo4j.com/docs/cypher-manual/current/introduction/) like

```bash
# Assert the UI is connected to the proper db server (has to match what was 
# configured in you .env file)
$:server connect   
# Make sure you are connect to the right database (again this has to match 
# with what was configured in you .env file)
$:use neo4j
# Displays the full extracted graph with all its nodes. Caveat emptor: 
# within the UI settings, the "Initial node display" integer parameter 
# controls the number of nodes displayed which defaults to 300
neo4j$ MATCH (n) RETURN n
# Display the nodes with the "Person" label
neo4j$ MATCH (n) WHERE n:Person RETURN n
# Display the nodes NOT having the "Person" label
neo4j$ MATCH (n) WHERE NOT n:Person RETURN n
# Display the nodes not having "Document" as single label
neo4j$ MATCH (n) WHERE NOT(SIZE(LABELS(n)) = 1 AND n:Document) RETURN n
# A composition of the above
neo4j$ MATCH (n) WHERE NOT(SIZE(LABELS(n)) = 1 AND n:Document) and NOT n:Person RETURN n
# Nodes that are not documents together with their relations
neo4j$ MATCH (n) WHERE NOT n:Document OPTIONAL MATCH (n)-[r]-(c) WHERE NOT c:Document RETURN n,r,c
...
```

## Use the knowledge graph programmatically

### Displaying knowledge graph main characteristics

```bash
python display_neo4jdb_graph_characteristics.py
```

### Searching the database

For example search the graph database with a Natural Language query by running the provided python script

```bash
python extract_from_knowledge_graph.py
```

Or search both the knowledge graph and the embedding space structures with

```bash
python vector_and_graph_hybrid_search.py
```

## Dump/Restore the database content for later usage

The following is a direct application of the [dump and load neo4j examples](https://neo4j.com/docs/operations-manual/current/docker/dump-load/)

```bash
docker compose down     # Database dump requires being "offline"
docker run --interactive --tty --rm  \
           --volume=`pwd`/data:/data \       # Has to match docker-compose.yaml
           --volume=`pwd`/backups:/backups \ # Sub-directory where dumps end up
           neo4j/neo4j-admin neo4j-admin database dump neo4j --to-path=/backups
```

and check the `backups/` sub-directory for the new existence of `neo4j.dump` file.

Restoring a previously dumped database is done with the following command

```bash
rm -fr data     # WARNING: this deletes all your databases !
docker run --interactive --tty --rm \
    --volume=`pwd`/data:/data \
    --volume=`pwd`/backups:/backups \
    neo4j/neo4j-admin neo4j-admin database load neo4j --from-path=/backups
docker compose up --detach
```

## Scripting things

In order to reproduce resulting data production (cut and paste based)

### Collecting Gold Dust

```bash
source ven/bin/activate
docker compose up --detach
python extracting_graph_semantic_chuncker.py --input_directory ../../../Data/ISBN_978-0-9835844-5-2_-_Collecting_Gold_Dust/ --load_markdown_document result_data/2019_-_Sayadaw-U-Tejaniya-Collecting-Gold-Dust-Web-Book-1_-_local_converter.md --load_json_document Convert/SelfMadePython/Sentences_as_LangChain_Document.json > extract.log 2>&1 &
tail -f extract.log
...
docker compose down
docker run --interactive --tty --rm  --volume=`pwd`/data:/data --volume=`pwd`/backups:/backups neo4j/neo4j-admin neo4j-admin database dump neo4j --to-path=/backups
mv backups/neo4j.dump backups/neo4j.CollectingGoldDust.MarkdownTextSplitterAndSentences.dump
```

## References

- [GraphRAG: The Marriage of Knowledge Graphs and RAG: Emil Eifrem](https://www.youtube.com/watch?v=knDDGYHnnSI)
- [Introduction to Neo4j](https://www.youtube.com/watch?v=YDWkPFijKQ4cdt)
- [Build a RAG agent with LangChain](https://docs.langchain.com/oss/python/langchain/rag#ollama)
- Calling [LLM through OpenwebUI examples](https://github.com/UDL-LIRIS/python-openwebui-bootstraping-examples)

## Next steps

### Improve observability

For the time being, tracing LLM calls (which is the minimum required for observability) is done by patching
`venv/lib/python3.10/site-packages/langchain_ollama/chat_models.py` and adding the following line as first line of the _create_chat_stream member function:

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
