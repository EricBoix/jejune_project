# neovis.js Application

## Introduction

This repository is a straightforward [docker](https://en.wikipedia.org/wiki/Docker_(software)) based containerization of the [`neo4j-conmtrib/neovis.js`](https://github.com/neo4j-contrib/neovis.js) example.

## Running things

```bash
cd neo4j
cp env-reference .env
### Edit the resulting .env file to configure the services
docker compose up --detach
```

## Troubleshooting

```bash
Assert things went smoothly by opening `http://localhost:7475/browser/`, authenticating according to the `.env` file and launching the cypher (refer to the [neovis/README](https://github.com/neo4j-contrib/neovis.js?tab=readme-ov-file#prepare-neo4j)])
```

```bash
neo4j$ MATCH p = (:Character)-[:INTERACTS]->(:Character) RETURN p
```

### Someday

Someday the above neo4j preparation stage will become

Restore a neo4j backup

```bash
cd neo4j
docker run --interactive --tty --rm \
    --volume=`pwd`/Data:/data \
    --volume=`pwd`/Backups:/backups \
    neo4j/neo4j-admin neo4j-admin database load neo4j --from-path=/backups
docker compose up --detach
```

### Prepare Neo4j

Our graph now consists of `Character` nodes that are connected by an `INTERACTS` relationships. We can visualize the
whole graph in Neo4j Browser by running:

```cypher

MATCH p = (:Character)-[:INTERACTS]->(:Character)
RETURN p
```
