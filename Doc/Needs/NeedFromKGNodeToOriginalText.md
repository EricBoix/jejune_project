# Need: Provide UI means to go from a Node/Transaction to the original citation

## User Story

As UI user working on some Knowledge Graph (KG), I want to go from a Node (or a Relationship) to its corresponding text source (original document) in order to explore the original textual context out of which the KG's Node was proposed/extracted.

## Requirement

When given a designated Node (id or name?), or relationship, search for the associated Document nodes (sharing a `MENTIONS` edge with the designated Node). Then display the original textual document (possibly documents) with the Node text highlighted.

## Notes

- The map between original text words and Nodes has few properties
  - the map domain is a subset of the words of the original text: some words might not have been extracted to Nodes by the KG creation algorithm,
  - the map might not be injective: some Node might correspond to a group of words (think of names of persons, or specialization e.g. "late Buddhism")
  - the map might not be [surjective](https://en.wikipedia.org/wiki/Bijection,_injection_and_surjection): some Node might be abstracted from a set of words (or e.g. a paragraph)
