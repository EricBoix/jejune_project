import { graph, parse, NamedNode, Literal, BlankNode, Statement } from 'rdflib';

export interface RdfTriple {
  subject: string;
  predicate: string;
  object: string;
  objectType: 'uri' | 'literal' | 'blank';
  objectValue: string;
}

export interface ParsedRdf {
  triples: RdfTriple[];
  subjects: Set<string>;
}

function getTermValue(term: NamedNode | Literal | BlankNode): string {
  if (term instanceof NamedNode) {
    return term.uri;
  }
  if (term instanceof Literal) {
    return term.value;
  }
  if (term instanceof BlankNode) {
    return term.value;
  }
  return String(term);
}

function getTermType(term: NamedNode | Literal | BlankNode): 'uri' | 'literal' | 'blank' {
  if (term instanceof NamedNode) return 'uri';
  if (term instanceof Literal) return 'literal';
  if (term instanceof BlankNode) return 'blank';
  return 'literal';
}

export function parseRdfTurtle(turtleContent: string, baseUri: string = 'http://example.org/'): ParsedRdf {
  const store = graph();
  parse(turtleContent, store, baseUri, 'text/turtle');

  const triples: RdfTriple[] = [];
  const subjects = new Set<string>();

  store.statements.forEach((statement: Statement) => {
    const subjectValue = getTermValue(statement.subject as NamedNode | BlankNode);
    subjects.add(subjectValue);

    triples.push({
      subject: subjectValue,
      predicate: getTermValue(statement.predicate as NamedNode),
      object: getTermValue(statement.object as NamedNode | Literal | BlankNode),
      objectType: getTermType(statement.object as NamedNode | Literal | BlankNode),
      objectValue: getTermValue(statement.object as NamedNode | Literal | BlankNode),
    });
  });

  return { triples, subjects };
}

export function getLocalName(uri: string): string {
  const hashIndex = uri.lastIndexOf('#');
  if (hashIndex !== -1) {
    return uri.substring(hashIndex + 1);
  }
  const slashIndex = uri.lastIndexOf('/');
  if (slashIndex !== -1) {
    return uri.substring(slashIndex + 1);
  }
  return uri;
}
