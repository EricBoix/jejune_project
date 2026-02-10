# JS/webGL based graph layout and visualization libraries<!-- omit from toc -->

## Table of contents<!-- omit from toc -->

- [Needs and required features](#needs-and-required-features)
- [Candidate popular libraries](#candidate-popular-libraries)
- [Summary of features](#summary-of-features)
- [Libraries](#libraries)

## Needs and required features

- JS (webGL)
- Distinguish edges from arcs/arrows
- Self-loops and multiple edge/arcs adjacent to same two vertices : e.g.  curved arrows to avoid overlap of two arrows having same node adjacency
- **Dynamic** data: varying nodes, edges and/or their attributes across time. Possibility to extend the set of existing nodes/edges (as opposed to having to provide them all at once)
- **Compounding**/Grouping/["Clustering"](https://visjs.github.io/vis-network/examples/network/other/clustering.html) nodes in a box/container
- **Layout** algorithms
  - some nodes position is manually given (and fixed)
  - provided automatics algorithms
  - dynamic/progressive layout adaptation (e.g. when adding a new node)
  - some nodes can be "fixed" (constrained to remain at manually given canvas position)
- Interactions:
  - Selectable edges
  - Draggable nodes: select a node, drag it and release it (node should then remain in place but surrounding "unfixed" nodes should adapt their position)
- **Licence**: must be open source and license has to be open enough...

## Candidate popular libraries

Commonly referred/mentioned libraries (refer below to survey articles)

- `cytoscape.js`: [on github](https://github.com/cytoscape/cytoscape.js), [website](https://js.cytoscape.org/), [examples](https://js.cytoscape.org/)
- `sigma.js`: [github](https://github.com/jacomyal/sigma.js), [website](https://www.sigmajs.org/)
- `vis.js-network`: [github](https://github.com/visjs/vis-network), [website](https://visjs.org/), [examples](https://visjs.github.io/vis-network/examples/)
- [G6](https://github.com/antvis/G6) that has a [strong Chinese bias](https://github.com/antvis/G6/issues)

Also sometimes mentioned

- [d3.js network/graph](https://d3-graph-gallery.com/network.html)
- [gephi](https://github.com/gephi/gephi): the open graph viz platform

Survey articles references

- [Ranking of JavaScript Graph Visualization Libraries by MingYi Zhao, Mar 2021](https://mingyizhao.medium.com/background-b553fda47349)
- [JavaScript Graph Drawing Libraries](https://github.com/anvaka/graph-drawing-libraries)
- [List of graph visualization libraries, by Elise Devau, 2019](https://elise-deux.medium.com/the-list-of-graph-visualization-libraries-7a7b89aab6a6)
- [How to visualize Node and Edge Sizes in Neo4j According to Property Values](https://www.youtube.com/watch?v=z-lM-zurdN8)

## Summary of features

| Feature | `Cytoscape.js` | `vis.js` | `Sigma.js` |
| ------- | -------------- | -------- | ---------- |
| edges vs arcs | | :white_check_mark: | :question: |
| Self-loop and multiple edges | | :white_check_mark: | :x: |
| Dynamic data | | :white_check_mark: | :question: |
| Compounding | :white_check_mark: | :white_check_mark: | :x: |
| LayoutS | | :white_check_mark: | :white_check_mark: |
| Interactions | | :white_check_mark: | :white_check_mark: |
| Open License | :white_check_mark: | :white_check_mark: | :white_check_mark: |

## Libraries

### Cytoscape.js

Features:

- :question: Edges and arrow types
- :question: Self loop and multiple edges
- :question: Dynamic data
- :white_check_mark: [Compounding nodes](https://github.com/cytoscape/cytoscape.js-compound-drag-and-drop) (and dragging the compound): BUT the extension has [many limitations](https://github.com/cytoscape/cytoscape.js-compound-drag-and-drop#caveats)
- :question: Layouts: has a [`cola.js` (COnstrained LAyout) extension](https://github.com/cytoscape/cytoscape.js-cola)
- :question: Interactions
- :white_check_mark: Licence: MIT for the core library and all first-party extensions

Notes and references:

- [Cytoscape.js examples](https://js.cytoscape.org/)
- [Many applications](https://apps.cytoscape.org/) using the library (mainly biology oriented).

### vis.js - network

Features

- :white_check_mark: [edges and arcs arrow types](https://visjs.github.io/vis-network/examples/network/edgeStyles/arrowTypes.html)
- :white_check_mark: [self loop](https://visjs.github.io/vis-network/examples/network/edgeStyles/selfReference.html) and [multiple edges](https://visjs.github.io/vis-network/examples/network/events/interactionEvents.html) (use this demo to add many edges linking the same two nodes)
- :white_check_mark: [Dynamic data](https://visjs.github.io/vis-network/examples/network/data/datasets.html)
- :white_check_mark: Compounding nodes: [various compounding/"clustering" criteria example](https://visjs.github.io/vis-network/examples/network/other/clustering.html), [clustering by zoom level](https://visjs.github.io/vis-network/examples/network/other/clusteringByZoom.html)
- :white_check_mark: Layouts: spring mass and some [hierarchically constrained possibilities](https://visjs.github.io/vis-network/examples/)
- :white_check_mark: Interactions: [edge selection](https://visjs.github.io/vis-network/examples/network/other/cursorChange.html) (yet dragging seems to act on the whole network) and [node displacement](https://visjs.github.io/vis-network/examples/network/events/interactionEvents.html) (with [`fixed` nodes with or without `physics`])
- :white_check_mark: Licence: MIT and Apache2.0

Additional features and notes:

- [Neovis.js](https://github.com/neo4j-contrib/neovis.js) adds a simplified access to data from Neo4j and is powered by vis.js
- [Scalable node and edges](https://visjs.github.io/vis-network/examples/network/data/scalingNodesEdges.html)
- [Dot language](https://visjs.github.io/vis-network/examples/network/data/dotLanguage/dotPlayground.html) _partially_ supported (although no support of [dot clusters](https://graphviz.org/Gallery/directed/cluster.html))

Notes and references:

- [Vis.js examples](https://visjs.github.io/vis-network/examples/)

### Sigma.js

- :question: Edges and arrow types
- :x: no [self-loops support](https://github.com/jacomyal/sigma.js/issues/1429), (:question:) multiple edges
- :question: Dynamic data
- :x: Compounding nodes: [no node grouping](https://github.com/jacomyal/sigma.js/issues/586)
- :white_check_mark: Layouts: [diverse layout algorithms](https://github.com/jacomyal/sigma.js/issues/939), curved arrows ([here](https://github.com/jacomyal/sigma.js/issues/951), [there](https://stackoverflow.com/questions/48909462/sigma-curve-and-curvedarrow-edge-type-renders-as-a-line))
- :white_check_mark: Interactions: [edge selection](https://stackoverflow.com/questions/49873693/sigma-js-how-to-keep-edge-selected-onclick), [draggable nodes](https://stackoverflow.com/questions/20541831/sigma-js-is-there-a-way-to-drag-one-node-individually)
- :white_check_mark: Licence: [MIT](https://github.com/jacomyal/sigma.js/blob/main/LICENSE.txt)

Notes and references:

- Sigma.js uses [graphology](https://github.com/graphology/graphology) JS library for its Graph (object) data backend.
- Tutorial [7 Helpful Sigma.js Examples to Master Graph Visualization, by Rapidops](https://rapidops.medium.com/7-helpful-sigma-js-examples-to-master-graph-visualization-a8cadf9e9b14)
- Arrested development [since 2024](https://github.com/jacomyal/sigma.js/commits/main/)

### NVL (Neo4j Visualisation Library)

Features:

- :x: License: not an open source project (source is not available), yet usage at npm package level is free [as far as you use it in conjunction with neo4j database](https://youtu.be/uVxhYgWsHZw?t=4039) data.

Notes and references:

- :x: Framework has to be a React network. Otherwise (e.g. with Angular) only the base library is available.
- [Neo4j Live: Stunning Graph Visualizations with NVL](https://www.youtube.com/watch?v=uVxhYgWsHZw): a demo targeting the package users.
