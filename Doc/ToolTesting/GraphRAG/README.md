# Hands on lowbrow exploration of GraphRAG in Python

## Introduction

This directory explores, with a direct hands-on approach, a process of graph extraction (and
exploitation) that is described in the ["Local GraphRAG with LLaMa 3.1 - LangChain, Ollama & Neo4j" youtube tutorial](https://www.youtube.com/watch?v=nkbyD4joa0A).
The original associated code, from which this work is partly derived, is available through [this Coding Crash Courses git repository](https://github.com/Coding-Crashkurse/GraphRAG-with-Llama-3.1.git).

## Running things

```bash
# Prepare the virtual environment
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Launch the Neo4j database
docker compose up --detach
```

Copy the [`env-reference` file](./env-reference) to a `.env` file and customize (at least) the entries mentioning the `CHANGE_ME` string.

```bash
# Extract the graph and store it in database
python extracting_graph.py
# Explore the extracted graph with Neo4j web UI (for exact hostname refer to 
# the NEO4J_URI entry of the `/.env` configuration file):
open http://localhost:7474/
```

```bash
# Search the graph database with a Natural Language query
python extract_from_knowledge_graph.py
```

```bash
# Search both graph and embedding space structures to with a Natural 
# Language query
python vector_and_graph_hybrid_search.py
```

## References

- [GraphRAG: The Marriage of Knowledge Graphs and RAG: Emil Eifrem](https://www.youtube.com/watch?v=knDDGYHnnSI)
- [Introduction to Neo4j](https://www.youtube.com/watch?v=YDWkPFijKQ4cdt)
- [Build a RAG agent with LangChain](https://docs.langchain.com/oss/python/langchain/rag#ollama)
- Calling [LLM through OpenwebUI examples](https://github.com/UDL-LIRIS/python-openwebui-bootstraping-examples)

## Next steps

### Improve the (graph) extraction process

[Read this and improve the script](https://neo4j.com/blog/developer/knowledge-graph-extraction-challenges/)

### Ingesting a Markdown file

- Use [LangChain's `UnstructuredMarkdownLoader`](https://docs.langchain.com/oss/python/integrations/document_loaders/unstructured_markdown)

### Using LangSmith for model traces

- [What is LangSmith (IBM docs)](https://www.ibm.com/think/topics/langsmith)
- [Running LangSmith on Kubernetes](https://langchain-5e9cc07a.mintlify.app/langsmith/kubernetes) (works on MiniKube)
- [Langsmith is expensive](https://www.metacto.com/blogs/the-true-cost-of-langsmith-a-comprehensive-pricing-integration-guide)
