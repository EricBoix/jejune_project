# Roles<!-- omit in toc -->

## Table of content<!-- omit in toc -->

- [Document Steward](#document-steward)
- [Catalog Curator](#catalog-curator)
- [Deployer](#deployer)

## Document Steward

The Document Steward is responsible for the lifecycle of an individual `jejune_doc_<name>` repository:
bringing a new document into the system and keeping its metadata accurate.

Responsibilities:

- Creates a new `jejune_doc_<name>` repository and populates it with the source document
  (markdown and/or PDF in `original_data/`).
- Adds a `doc.yaml` file at the repository root specifying the document's title, authors,
  year, keywords, ISBN (if applicable), and the relative paths to its markdown file,
  optional PDF, and optional sentences file.
  This file is editorial content and is committed to the repository.
- Runs `jejune convert` to convert a PDF source to markdown when needed.
- Runs `jejune graph extract <doc_dir>` to build the knowledge graph for the document.
- Optionally makes a simple single document deployment to improve the document content.
- Notifies the [Catalog Curator](#catalog-curator) when a new document is ready to be
  registered in the full catalog.

## Catalog Curator

The Catalog Curator is responsible for the collection as a whole: knowing which documents
exist, keeping their catalog entries accurate, and making the collection available for
deployment.

Responsibilities:

- Maintains [`jejune_docs_server/DockerContext/full-catalog.yaml`](https://github.com/EricBoix/jejune_docs_server):
  the canonical reference of all known `jejune_doc_*` repositories (`name`, `url`, `public` fields).
  This file is the single source of truth; any deployment catalog must be a validated subset of it.
- Registers new documents (upon notification from a [Document Steward](#document-steward))
  by adding an entry to `full-catalog.yaml`.
- Runs `jejune catalog check` periodically to validate that catalog entries match actual
  GitHub repository visibility.
- Runs `jejune catalog sync` to detect locally cloned `jj_doc_*` repositories that are
  not yet in the catalog.

## Deployer

The Deployer configures a specific deployment of the jejune system.

Responsibilities:

- Creates a deployment-specific catalog at `jj_deployments/deploy_<name>/catalog.yaml`:
  a subset of `full-catalog.yaml`, selecting the documents relevant for that deployment.
  `build_docs.py` validates names and URLs against `full-catalog.yaml` at build time and
  rejects any entry not present in it.
- Validates the deployment catalog before building:

  ```sh
  jejune catalog check-deployment /path/to/jj_deployments/deploy_<name>
  ```

- Builds `jejune_docs_server` with the deployment catalog injected as a Docker secret.
  When `CATALOG_FILE` is not set, the full catalog is used by default.

  ```sh
  CATALOG_FILE=/path/to/jj_deployments/deploy_<name>/catalog.yaml docker compose build
  ```

- Configures deployment-specific environment (Neo4j credentials, LLM endpoint, etc.).
