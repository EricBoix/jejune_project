import { GraphNode, GraphEdge, GraphData } from '../types/graph.types';
import { ParsedRdf, getLocalName } from './rdfParser';

const RDFS_LABEL = 'http://www.w3.org/2000/01/rdf-schema#label';

export function convertRdfToGraph(parsedRdf: ParsedRdf): GraphData {
  const { triples, subjects } = parsedRdf;
  const nodes: GraphNode[] = [];
  const edges: GraphEdge[] = [];

  const nodeMap = new Map<string, GraphNode>();
  const labels = new Map<string, string>();
  const metadata = new Map<string, Record<string, string[]>>();

  // First pass: collect labels and identify all nodes
  for (const triple of triples) {
    if (triple.predicate === RDFS_LABEL && triple.objectType === 'literal') {
      labels.set(triple.subject, triple.objectValue);
    }
  }

  // Initialize nodes for all subjects
  for (const subjectUri of subjects) {
    const label = labels.get(subjectUri) || getLocalName(subjectUri);
    nodeMap.set(subjectUri, {
      id: subjectUri,
      label,
      uri: subjectUri,
      metadata: {},
    });
    metadata.set(subjectUri, {});
  }

  // Second pass: process all triples
  for (const triple of triples) {
    const { subject, predicate, object, objectType, objectValue } = triple;
    const predicateLocal = getLocalName(predicate);

    if (objectType === 'uri' || objectType === 'blank') {
      // URI/blank node object -> create edge
      // Also ensure the object node exists
      if (!nodeMap.has(object)) {
        nodeMap.set(object, {
          id: object,
          label: labels.get(object) || getLocalName(object),
          uri: object,
          metadata: {},
        });
        metadata.set(object, {});
      }

      const edgeId = `${subject}--${predicate}--${object}`;
      edges.push({
        id: edgeId,
        from: subject,
        to: object,
        label: predicateLocal,
        predicateUri: predicate,
      });
    } else {
      // Literal object -> add to node metadata
      const nodeMeta = metadata.get(subject);
      if (nodeMeta) {
        if (!nodeMeta[predicateLocal]) {
          nodeMeta[predicateLocal] = [];
        }
        nodeMeta[predicateLocal].push(objectValue);
      }
    }
  }

  // Attach metadata to nodes
  for (const [uri, node] of nodeMap) {
    node.metadata = metadata.get(uri) || {};
    nodes.push(node);
  }

  return { nodes, edges };
}
