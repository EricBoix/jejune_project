# Knowledge graph basic needs

## Introduction

It seems that the implementation needs can be expressed in terms of [Property Graph](https://en.wikipedia.org/wiki/Property_graph) which is one (among others) possible implementations for Knowledge Graphs.

## Descriptions/data can be added to edges

### Classic examples of data that has to live/be-attached to edges

- In a graph where nodes represent documents (books, articles) a comparison between two documents lives on "comparison" edge that is adjacent to the two compared nodes.
- In a KG graph where one considers two concept/notions nodes, says `concept_A` and `notion_B` (as extracted by some knowledge extraction method) and some edge (similarly extracted by, maybe, the same knowledge extraction method) adjacent to those two nodes. This edge is a predicate that probably originates from a sentence/paragraph that mention both `concept_A` and `notion_B`. A KG designer might wish to keep track of the document (sentence/paragraph) out of which this relationship emerged.

### Implementation in RDF

[`RDF 1.2`](https://w3c.github.io/sparql-concepts/spec/) / [`SPARQL 1.2`](https://www.w3.org/TR/sparql12-update/) (working drafts) favor the usage `Triple Terms`
(informally also known as `triples-about-triples`) using the `<< >>` special brackets.

Notes: [`RDF*` aka RDF-star](https://w3c-cg.github.io/rdf-star/cg-spec/editors_draft.html) extension was dropped from `RDF 1.2` evolution.
