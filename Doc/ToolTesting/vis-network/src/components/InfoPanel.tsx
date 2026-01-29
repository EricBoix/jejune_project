import { useGraph } from '../context/GraphContext';

export function InfoPanel() {
  const { selection, getSelectedNode, getSelectedEdge } = useGraph();

  if (!selection.type) {
    return (
      <div style={styles.panel}>
        <p style={styles.placeholder}>Click a node or edge to view details</p>
      </div>
    );
  }

  if (selection.type === 'node') {
    const node = getSelectedNode();
    if (!node) return null;

    return (
      <div style={styles.panel}>
        <h3 style={styles.title}>Node: {node.label}</h3>
        <div style={styles.section}>
          <strong>URI:</strong>
          <p style={styles.uri}>{node.uri}</p>
        </div>
        {Object.keys(node.metadata).length > 0 && (
          <div style={styles.section}>
            <strong>Properties:</strong>
            <ul style={styles.list}>
              {Object.entries(node.metadata).map(([key, values]) => (
                <li key={key}>
                  <span style={styles.key}>{key}:</span>{' '}
                  {values.join(', ')}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  }

  if (selection.type === 'edge') {
    const edge = getSelectedEdge();
    if (!edge) return null;

    return (
      <div style={styles.panel}>
        <h3 style={styles.title}>Edge: {edge.label}</h3>
        <div style={styles.section}>
          <strong>Predicate URI:</strong>
          <p style={styles.uri}>{edge.predicateUri}</p>
        </div>
        <div style={styles.section}>
          <strong>From:</strong> {edge.from.split('/').pop()}
        </div>
        <div style={styles.section}>
          <strong>To:</strong> {edge.to.split('/').pop()}
        </div>
      </div>
    );
  }

  return null;
}

const styles: Record<string, React.CSSProperties> = {
  panel: {
    padding: '16px',
    backgroundColor: '#fff',
    borderLeft: '1px solid #ccc',
    height: '100%',
    overflowY: 'auto',
  },
  placeholder: {
    color: '#888',
    fontStyle: 'italic',
  },
  title: {
    margin: '0 0 16px 0',
    fontSize: '18px',
    borderBottom: '1px solid #eee',
    paddingBottom: '8px',
  },
  section: {
    marginBottom: '12px',
  },
  uri: {
    fontSize: '12px',
    wordBreak: 'break-all',
    color: '#666',
    margin: '4px 0',
  },
  list: {
    margin: '8px 0',
    paddingLeft: '20px',
  },
  key: {
    fontWeight: 'bold',
    color: '#444',
  },
};
