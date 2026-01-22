# Experimenting with the neovis.js package

## Introduction

This repository holds [docker](https://en.wikipedia.org/wiki/Docker_(software)) based containerization of two examples of usage of [`neo4j-contrib/neovis.js`](https://github.com/neo4j-contrib/neovis.js)

- [Standard](./Standard/README.md) smoothly run both [`simple-example.html`](https://github.com/neo4j-contrib/neovis.js/blob/master/examples/simple-example.html) and [neovis.js's advanced-example.html](https://github.com/neo4j-contrib/neovis.js/blob/master/examples/advanced-example.html) that works nicely.
- [FromBackup](./FromBackup/README.md) holds a FAILED trial to adapt the above examples on another data set

## Temporary conclusion

Until we can get the [`FromBackup/index.html`](./FromBackup/neovis/index.html#62) to properly display the node names (the `id` property of the `Concept` nodes) the usage of Neovis is a dead end (for this project).
Note failing to adapt this examples seems to be a [known issue](https://github.com/neo4j-contrib/neovis.js/issues/378) that remains unresolved since [Neovis seems to be no longer maintained](https://github.com/neo4j-contrib/neovis.js/issues/391).
