# Design notes<!-- omit from toc -->

- [Non technical constraints](#non-technical-constraints)
- [Stack](#stack)
- [Design patterns](#design-patterns)

## Non technical constraints

- Only free and open source software
- Project size: small to medium
- The graph data format must be RDF (defacto standard for knowledge graphs)
- Web app

## Stack

### Language

TypeScript (or Javascript): the [WASM](https://webassembly.org/) + python ecosystem is not mature enough

### Scaffolding

- Current choice: Vite (fast, modern, minimal)
- References: [React's create an App](https://react.dev/learn/creating-a-react-app), [choosing the right build tool](https://medium.com/@imranmsa93/choosing-the-right-build-tool-for-react-vite-parcel-or-rsbuild-5105889cc168)

Other evaluated opportunities

- [Create React App](https://github.com/facebook/create-react-app) is in long-term stasis
- [Next.js](https://nextjs.org/) is overkill for a small-medium size project

### Framework

React: comes as a consequence of choosing Vite.

### Package manager

npm: comes as a consequence of choosing Vite.

### Graph representation

**Current choice**: [vis-network](https://github.com/visjs/vis-network)

Possible alternatives: d3.js

### RDF Parsing Libraries

**Current choice**: rdflib.js - Full-featured, supports SPARQL queries, large community

## Design patterns

### vis-network + React Integration Patterns

**Current choice**: Direct DOM manipulation - vis-network manages its own canvas, React wraps it

Other evaluated opportunities

- Custom React hook: why not ? Unless vis-network interactions are too specialized.
- [vis-network-react](https://github.com/visjs/vis-network-react)
  - development was arrested in 2020
  - no documentation

### State Management for Graph Editing

**Current choice**: React context (simple, built-in)

Other evaluated opportunities

- Zustand - Lightweight, good for complex state
- Redux - Overkill unless app grows significantly  
