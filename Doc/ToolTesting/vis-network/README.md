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

## Installation

```bash
npm install
```

## Available Scripts

### Development

```bash
npm run dev
```

Starts the development server at `http://localhost:5173`.

### Build

```bash
npm run build
```

Compiles TypeScript and builds the production bundle to `dist/`.

### Preview

```bash
npm run preview
```

Serves the production build locally for testing.

### Lint

```bash
npm run lint
```

Runs ESLint on the codebase.

## Tech Stack

- Vite + React + TypeScript
- vis-network (graph visualization)
- rdflib.js (RDF parsing)
- React Context (state management)
