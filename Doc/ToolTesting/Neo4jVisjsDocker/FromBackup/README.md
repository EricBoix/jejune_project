# neovis.js Application

## Introduction

This directory is an adaptation of [containerization of the `neovis.js` demo](../Standard/README.md). Instead of using the so called `GameOfThrone` dataset, it loads the dump it encounters in the `neo4j/Backup/` subdirectory.

**WARNING** As documented in [`index.html`](./neovis/index.html#62) displaying the node names (the `id` property of the `Concept` nodes) DOES NOT WORK. This seems to be a [known issue](https://github.com/neo4j-contrib/neovis.js/issues/378) that remains unresolved since [Neovis seems to be no longer maintained](https://github.com/neo4j-contrib/neovis.js/issues/391).

## Running things

Running things doesn't differ from the [Standard demo](../Standard/README.md) and boils down to (for default ports)

```bash
docker compose up --detach
```

and with opening `http://localhost:8080` with a web browser.

## Troubleshooting

On launching the `docker compose up`, the error message

```bash
neo4j-initializer-1  | Failed to load database 'neo4j': Database already exists: neo4j
```

indicates the previous existence of a `neo4j/Data` directory (probably due to a previous execution). Removing that directory (e.g. with `\rm -fr neo4j/Data`) should solve the issue.

MATCH (n:Concept)-[r:RELATED_TO]->(m:Concept) RETURN *