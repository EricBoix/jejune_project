# neovis.js Application

## Introduction

This directory is an adaptation of [containerization of the `neovis.js` demo](../Standard/README.md). Instead of using the so called `GameOfThrone` dataset, it loads the dump it encounters in the `neo4j/Backup/` subdirectory.

## Running things

Running things doesn't differ from the [Standard demo](../Standard/README.md) and boils down to (for default ports)

```bash
docker compose up --detach
```

and with opening `http://localhost:8080` with a web browser.
