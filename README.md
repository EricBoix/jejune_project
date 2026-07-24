# jejune project<!-- omit in toc -->

Never let the [monkey](https://en.wikipedia.org/wiki/Monkey_mind) hinder you from sitting back on the [cushion](https://en.wikipedia.org/wiki/Zafu).

## Table of content<!-- omit in toc -->

- [Related repositories](#related-repositories)
- [Needs](#needs)
- [Roles](#roles)
- [Working with VScode](#working-with-vscode)

## Related repositories

- Tools/Components
  - [jejune_cli](https://github.com/EricBoix/jejune_cli): shell based workflow orchestrator
  - [jejune_extract_knowledge_graph](https://github.com/EricBoix/jejune_extract_knowledge_graph)
  - [jejune_neo4j_docker](https://github.com/EricBoix/jejune_neo4j_docker)
  - [jejune_markdown_browser](https://github.com/EricBoix/jejune_markdown_browser)
  - [jejune_kg-graph_viewer](https://github.com/EricBoix/jejune_kg-graph_viewer)
  - [jj_neo4j_to_rdf_ttl](https://github.com/EricBoix/jj_neo4j_to_rdf_ttl)
  - [jejune_docs_server](https://github.com/EricBoix/jejune_docs_server):
    HTTP service (REST + Swagger) that bakes designated `jejune_doc_*` repositories and exposes
    their markdown, PDF, and sentence-level content over HTTP.
    Holds the canonical `full-catalog.yaml` (maintained by the [Catalog Curator](./Role.md#catalog-curator)).

- Documents/Books:
  - [Four Noble Truths](https://github.com/EricBoix/jejune_doc_Four_Noble_Truths): a tiny document for testing things
  - [Four Hundred Stanzas](https://github.com/EricBoix/jejune_doc_Four_Hundred_Stanzas)
  - [Zen flesh, zen bones](https://github.com/EricBoix/jejune_doc_Zen_Flesh_Zen_Bones)
  - [Collecting Gold Dust](https://github.com/EricBoix/jejune_doc_Collecting_Gold_Dust)
  - [Rob Burbea](https://github.com/EricBoix/jejune_doc_Rob_Burbea)

## Needs

- Refer to [the list of Needs](./Doc/Needs/Readme.md)
- Knowledge graph visualisation: just google on that (Knowledge graph visualisation) and also PCA (Principal Component Analysis), MDS (Principal Coordinates Analysis, PCO or PCoA), Spectral Embedding of Graphs.

## Roles

See [Role.md](./Role.md) for the identified project roles (Document Steward, Catalog Curator, Deployer).

## Working with VScode

Useful extensions:

- [Matt Bierner's "Markdown Footnotes"](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-footnotes) for `[^1] footnote syntax support to VS Code's built-in Markdown preview`.
