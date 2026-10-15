# Database related needs and rationale for choice<!-- omit from toc --> 

## Table of contents<!-- omit from toc -->

- [The context](#the-context)
- [Why RDF ?](#why-rdf-)
- [Concrete needs](#concrete-needs)
- [Existing and recommendable triple-stores](#existing-and-recommendable-triple-stores)
  - [Oxigraph](#oxigraph)
  - [GraphDB Free](#graphdb-free)
  - [Apache Jena](#apache-jena)
- [Python wrappers](#python-wrappers)
- [Conclusion](#conclusion)
  - [Prototype](#prototype)
  - [Production](#production)
- [References](#references)

## The context

Knowledge Graph extraction (refer to [jejune_extract_knowledge_graph](https://github.com/EricBoix/jejune_extract_knowledge_graph)) uses the `langchain_neo4j` that requires neo4j for storing the extracted graph. But neo4j is neither open source nor relying on open standards.
The project thus needs to convert that format to open standards and migrate to more open databases.

## Why RDF ?

Because RDF allows for

- explicit means to describe in an integrated format both the data and the model of the data ([RDFS](https://en.wikipedia.org/wiki/RDF_Schema) standing for RDF Schema) following classical conceptual modeling approaches. This provides much freedom/plasticity for
  - in moving the frontier between the data and its model (think of promoting data to concepts)
  - in remodelling data to adapt it to new model (or [DSL](https://en.wikipedia.org/wiki/Domain-specific_language))
  - blending/merging/evolving models
  - same data represented with multiple/diverse models

A **must have** need:

- descriptions/data can be added to edges (refer to [RDF star](https://www.ontotext.com/knowledgehub/fundamentals/what-is-rdf-star/)). Here are some classic examples of data that has to live/be-attached to edges:
  - a comparison between two documents (books seen as nodes)
  - different interpretations of a single concept (that can take the form of remark/article i.e. another document)

Needs "nice" to be satisfied
  
- many existing ontologies and thus concrete means not to re-invent the wheel ([NIH](https://en.wikipedia.org/wiki/Not_invented_here) tendency)
- easily adapting the display (data decorated by/with semantics) without heavy refactoring (e.g. node colors are plastically inherited from properties among which can be the ref:type)

## Concrete needs

- data volume estimates: a maximum of a hundred markdown books/articles as input. If we estimate that each document source converts to 2k nodes and estimate a global node overlap of 50%, we end up with **100k nodes** that will produce several hundred thousand triples. A gross/early estimation is a need to represent 500k triples (a maximum of 1M triples looks comfortable).
- expected query patterns: the query shall be read only and not heavy (neither in number nor in complication)
- concurrency requirements: none (each deployment has a single end-use) at the prototyping stage
- deployment constraints: local (or cloud maybe someday) but container based
- latency targets: not considered at this stage.

## Existing and recommendable triple-stores

### Oxigraph

- While written in Rust, it is designed from the ground up with first-class Python support.
- Docker Setup: Extremely lightweight and fast official Docker images (oxigraph/oxigraph).
- Inference/Reasoning: Minimal (primarily raw data storage)
- Python Integration
  - the native, highly optimized Python bindings (pip install oxigraph) is dedicated to this DB but useful when used as in-process library within your Python application. If inter-operability (or migration to more scalable triple-stores like GraphDB free) then spin it up as a standalone server in Docker and query it via SPARQL endpoints through e.g. [SPARQLWrapper](https://github.com/rdflib/sparqlwrapper) or [rdflib's SPARQLStore](https://github.com/RDFLib/rdflib/blob/main/rdflib/plugins/stores/sparqlstore.py).
- Capacity: under 100 Million Triples
- Best for: fast setup, low memory footprint, and tight Python integration are priorities.
- Note: modeling of triples-about-triples (property graphs) must be done as `Triple Terms` with the updated RDF 1.2 / SPARQL 1.2 (working draft) syntax using `<< >>` special brackets

### GraphDB Free

[GraphDB](https://graphdb.ontotext.com/) is a triple-store (a.k.a. semantic graph database) targeting the enterprise:

- GraphDB is proprietary code (not open source)
- GraphDB "free" is a feature/performance limited (1 concurrent query at a time) but free (as in free beer) version
- Inference/Reasoning: advanced structural reasoning (RDFS, OWL profiles, custom rules)
- Docker images: [Ontotext](https://hub.docker.com/r/ontotext/graphdb/) (provides a standardized vanilla engine) or [khaller/graphdb-free](https://hub.docker.com/r/khaller/graphdb-free) (embeds automated helper scripts)
- compliant with W3C Standards: RDF 1.1 and SPARQL 1.1, with RDF-Star and SPARQL-Star extensions
- Limitations: restricted to one concurrent query
- Best For: Projects that want enterprise-grade visual profiling, semantic engineering tools, and ontologically advanced reasoning without upfront licensing costs
- Note: GraphDB sticks to `Triple Terms` support (just as Oxigraph does)

### Apache Jena

- [Apache Jena](https://jena.apache.org/) is free and open source
- **Java** framework for building Semantic Web and Linked Data applications. Not very useful for jejune since the project tool stack is Python centered. 
- Yet Apache Jena usage can be limited to its [Fuseki2](https://jena.apache.org/documentation/fuseki2/index.html) SPARQL server (backed by the Apache Jena TDB RDF triple store for persistence)
  - offers a web UI,
  - [RDF-star support](https://jena.apache.org/documentation/rdf-star/)
  - [SPARQL-star](https://jena.apache.org/documentation/rdf-star/#sparql-star) and its [web wrapping](https://www.w3.org/TR/sparql11-http-rdf-update/) (Graph Store HTTP Protocol) which in turn allows for [simple Python turtle importation](https://jena.apache.org/documentation/fuseki2/soh.html) ([and also](https://stackoverflow.com/questions/54549464/programmaticaly-upload-dataset-to-fuseki/56862436#56862436))
  - [docker images](https://hub.docker.com/r/stain/jena-fuseki)
  - note: Fuseki2 is open source and with a free license
- Best For: Standard, production-grade applications that need strict W3C compliance, stability, and a rich web UI for managing datasets.

## Python wrappers

| **Feature**               | **`SPARQLWrapper`**                                | **`SPARQLStore` (RDFLib)**                             |
|---------------------------|----------------------------------------------------|--------------------------------------------------------|
| **Primary Philosophy**    | Raw HTTP Request Client                            | Graph Database Abstraction                             |
| **Output Data Type**      | Python dicts (JSON) or XML strings                 | RDFLib `URIRef`, `Literal`, and `Graph` objects        |
| **Memory Footprint**      | **Very Low** (streams or directly parses response) | **Higher** (instantiates complex Python objects)       |
| **Execution Performance** | **Faster** (minimal serialization overhead)        | **Slower** (substantial Python abstraction overhead)   |
| **Pythonic Manipulation** | Complex (you manually extract data from dict trees) | Easy (supports `.triples()`, `.subjects()`, `g1 + g2`) |
| **Dependencies**          | Standalone package                                 | Requires `rdflib`                                      |

Note: the project has no need for "write operations"

## Conclusion

There are two development stages for the project.

### Prototype

At this prototyping stage the project must remain independent from proprietary solutions (no funding).
The representation needs (in terms of number of nodes) are lightweight/reasonable (1M triples tops).
We thus can choose the `Oxigraph / SPARQLStore (RDFLib)` tandem.
The reasons for choosing `SPARQLStore (RDFLib)` at this stage is for reducing the migration costs if the project reaches the second production stage.

### Production

This not yet clearly foreseen stage shall not be driven by a much higher number of triples (they are not that many books/documents of quality in the domain) but probably by a higher number of simultaneous users (consulting the same DB). Although this concurrency access disqualifies GraphDB-Free for production (because of its concurrency limitation), GraphDB-Free could be used as development tool that is fully compatible with the commercial version. The project can thus accept to release its open-source/free constraint and adopt the `graphDB-free / SPARQLStore (RDFLib)` tandem when production needs end-up in disqualifying Oxigraph.

## References

- [GraphDB vs Neo4j: Key Differences Explained](https://www.puppygraph.com/blog/graphdb-vs-neo4j) by Matt Tanner
- [Neo4j's Developers guide to GraphRAG](https://go.neo4j.com/rs/710-RRC-335/images/Developers-Guide-GraphRAG.pdf), [local copy](./Neo4j_Developers_Guide_GraphRAG.pdf) by Alison Cossette, Zach Blumenfeld, Damaso Sanoja
- [Top 10 Open Source Graph Databases](https://www.geeksforgeeks.org/blogs/open-source-graph-databases/)
