# Knowledge Graph Visualization

Interactive web application for visualizing RDF knowledge graphs using vis-network.

## Features

- Load and parse RDF files (Turtle format)
- Interactive graph visualization with node/edge selection
- View node metadata and edge properties
- Edit node and edge labels in-memory
- File upload for custom RDF data

## Prerequisites

- Node.js (v18+)
- npm

## Commands

- `npm install`: install package dependencies
- `npm run build`: compiles TypeScript and builds the production bundle to `dist/`
- `npm run preview`: serves the production build locally for testing
- `npm run dev`: starts a development server at `http://localhost:5173`
- `npm run lint`: runs ESLint on the codebase.

## Visualizing the sample graph

### Visualizing the default sample graph

The default graph is the file [`src/data/sample.ttl`](./src/data/sample.ttl)

```bash
npm run dev
open http://localhost:5173
```

### Visualizing an output of [Neo4jToRDF converter](../Neo4jToRDF/README.md)

Either use the "Load RDF File" button or

```bash
mv src/data/sample.ttl src/data/sample.ttl.orig
ln -s ../Neo4jToRDF/output.ttl src/data/sample.ttl
npm run dev
open http://localhost:5173
```
