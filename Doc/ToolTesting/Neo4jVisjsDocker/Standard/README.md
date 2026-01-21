# neovis.js Application

## Introduction

This repository is a straightforward [docker](https://en.wikipedia.org/wiki/Docker_(software)) based containerization of the [`neo4j-conmtrib/neovis.js`](https://github.com/neo4j-contrib/neovis.js) demo/example.

## Running things

Try running the default configuration with

```bash
docker compose up --detach
```

and proceed with opening `http://localhost:8080` with a web browser.

> Note: In case of conflict with already used ports, you might try to
> - `cp env-reference .env`
> - edit the resulting `.env` file to configure the noe4j service
> - run the demo with `docker compose up --detach`

In order to try some other cypher query, you can try to "submit" the following cypher (refer to the [neovis/README](https://github.com/neo4j-contrib/neovis.js?tab=readme-ov-file#prepare-neo4j))

```bash
MATCH p = (:Character)-[:INTERACTS]->(:Character) RETURN p
```

## Troubleshooting

In case no graph gets displayed by neovis, assert that the neo4j browser is available by opening `http://localhost:7475/browser/` and authenticating according to the `.env` file content. Then trying connecting the neo4j-UI to `neo4j://localhost:7687` (mutatis mutandis with the `NEO4J_PORT_BOLT` port number you configured in the `.env` file).

## Current limitations of this "dockerisation"

Neovis now has an hardwired designation of to the neo4j database server as defined by the `config.neo4j` variable in [Neovis/index.html](./neovis/index.html#36).

And in theory, the `index.html` file has to be manually aligned with the values configured in the `.env` file.

> Note: Interestingly enough the current value of `config.neo4j` is
>
> ```bash
> serverUrl: "bolt://localhost:7688",    # <--- NOT the default port !?
> serverUser: "neo4j",
> serverPassword: "my_password"
> ```
>
> which points to an erroneous default configuration of the neo4j server. Yet the demo remains functional...

### TODO/Someday (for the developers)

Someday the above neo4j preparation stage will become restore a neo4j backup

```bash
cd neo4j
docker run --interactive --tty --rm \
    --volume=`pwd`/Data:/data \
    --volume=`pwd`/Backups:/backups \
    neo4j/neo4j-admin neo4j-admin database load neo4j --from-path=/backups
docker compose up --detach
```
