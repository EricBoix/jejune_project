# Knowledge Graph Workflow<!-- omit in toc -->

End-to-end data pipeline from PDF documents to interactive knowledge graph visualization with citation navigation.

- [Activity Diagram](#activity-diagram)
- [Pipeline Summary](#pipeline-summary)

## Activity Diagram

![Workflow](workflow.png)

Note: above image was generated from [workflow.puml](./workflow.puml) with `java -jar plantuml.jar -tpng workflow.puml`.

## Pipeline Summary

| Stage | Directory/Repository | Script/Tool | Input | Output |
| ----- | --------- | ----------- | ----- | ------ |
| 1. PDF to Markdown | [`Collecting Gold Dust` converter](https://github.com/EricBoix/jj_doc_Collecting_Gold_Dust/blob/main/Readme.md) | `Convert/main.py` | PDF | `.md` + `.json` |
| 2. Markdown to Neo4j | `Doc/ToolTesting/GraphRAG/` | `extracting_graph*.py` | Markdown | Neo4j DB |
| 3. Neo4j to RDF | `Doc/ToolTesting/Neo4jToRDF/` | `neo4j_to_rdf.py` | Neo4j DB | `.ttl` |
| 4. Visualization | `Doc/ToolTesting/vis-network/` | `npm run dev` | `.ttl` | Web UI |
| 5. Citation Navigation | `Doc/ToolTesting/WebbrowsingMarkdown/` | code-server + URI extension | URI + `.md` | Highlighted text |
