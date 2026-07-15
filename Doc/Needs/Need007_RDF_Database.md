# Database related needs and rationale for choice

## Why RDF ?

Because RDF allows for

- explicit means to describe the model of the data ([RDFS](https://en.wikipedia.org/wiki/RDF_Schema) standing for RDF Schema) following classical conceptual modeling approaches,
- many existing ontologies and thus concrete means not to re-invent the wheel ([NIH](https://en.wikipedia.org/wiki/Not_invented_here) tendency)
- yet a great plasticity between data and the data model which allows to
  - easily evolve the model (of the data) (or [DSL](https://en.wikipedia.org/wiki/Domain-specific_language)
  - easily adapt the display (data decorated by/with semantics) without heavy refactoring (e.g. node colors are plastically inherited from properties among which can be the ref:type)
- descriptions can be added to edges (refer to [RDF star](https://www.ontotext.com/knowledgehub/fundamentals/what-is-rdf-star/))

## Existing triple-stores

### Apache Jena

[Apache Jena](https://jena.apache.org/) free and open source **Java** :fire:  framework for building
Semantic Web and Linked Data applications. Yet we can limit our usage to its [Fuseki2](https://jena.apache.org/documentation/fuseki2/index.html) SPARQL server (backed by the Apache Jena TDB RDF triple store) for persistence that offers

- a web UI,
- [RDF-star support](https://jena.apache.org/documentation/rdf-star/)
- [SPARQL-star](https://jena.apache.org/documentation/rdf-star/#sparql-star) and its [web wrapping](https://www.w3.org/TR/sparql11-http-rdf-update/) (Graph Store HTTP Protocol) which in turn allows for [simple Python turtle importation](https://stackoverflow.com/questions/54549464/programmaticaly-upload-dataset-to-fuseki/56862436#56862436)
- [docker images](https://hub.docker.com/r/stain/jena-fuseki)
- note: Fuseki2 is open source and with a free license

### GraphDB free

[GraphDB](https://graphdb.ontotext.com/) is a triple-store (a.k.a. semantic graph database) targeting the enterprise:

- GraphDB is proprietary code (not open source)
- GraphDB "free" is a feature/performance limited but free (as in free beer) version
- [Ontotext docker images](https://hub.docker.com/r/ontotext/graphdb/) or [khaller/graphdb-free](https://hub.docker.com/r/khaller/graphdb-free)
- compliant with W3C Standards: RDF 1.1 and SPARQL 1.1, with RDF-Star and SPARQL-Star extensions

## References

- [GraphDB vs Neo4j: Keu Differences Explained](https://www.puppygraph.com/blog/graphdb-vs-neo4j) by Matt Tanner
- [Neo4j's Developers guide to GraphRAG](https://go.neo4j.com/rs/710-RRC-335/images/Developers-Guide-GraphRAG.pdf), [local copy](./Neo4j_Developers_Guide_GraphRAG.pdf) by Alison Cossette, Zach Blumenfeld, Damaso Sanoja
- [Top 10 Open Source Graph Databases](https://www.geeksforgeeks.org/blogs/open-source-graph-databases/)
