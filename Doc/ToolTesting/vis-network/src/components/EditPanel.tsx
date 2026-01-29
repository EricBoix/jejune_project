import { useState, useEffect } from 'react';
import { useGraph } from '../context/GraphContext';

export function EditPanel() {
  const { selection, getSelectedNode, getSelectedEdge, updateNode, updateEdge } = useGraph();
  const [editLabel, setEditLabel] = useState('');

  const selectedNode = getSelectedNode();
  const selectedEdge = getSelectedEdge();

  useEffect(() => {
    if (selection.type === 'node' && selectedNode) {
      setEditLabel(selectedNode.label);
    } else if (selection.type === 'edge' && selectedEdge) {
      setEditLabel(selectedEdge.label);
    } else {
      setEditLabel('');
    }
  }, [selection, selectedNode, selectedEdge]);

  const handleSave = () => {
    if (selection.type === 'node' && selection.id) {
      updateNode(selection.id, { label: editLabel });
    } else if (selection.type === 'edge' && selection.id) {
      updateEdge(selection.id, { label: editLabel });
    }
  };

  if (!selection.type) {
    return (
      <div style={styles.panel}>
        <p style={styles.placeholder}>Select a node or edge to edit</p>
      </div>
    );
  }

  return (
    <div style={styles.panel}>
      <h3 style={styles.title}>
        Edit {selection.type === 'node' ? 'Node' : 'Edge'}
      </h3>
      <div style={styles.field}>
        <label style={styles.label}>Label:</label>
        <input
          type="text"
          value={editLabel}
          onChange={(e) => setEditLabel(e.target.value)}
          style={styles.input}
        />
      </div>
      <button onClick={handleSave} style={styles.button}>
        Save
      </button>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  panel: {
    padding: '16px',
    backgroundColor: '#fff',
    borderLeft: '1px solid #ccc',
    height: '100%',
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
  field: {
    marginBottom: '16px',
  },
  label: {
    display: 'block',
    marginBottom: '4px',
    fontWeight: 'bold',
  },
  input: {
    width: '100%',
    padding: '8px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    fontSize: '14px',
    boxSizing: 'border-box',
  },
  button: {
    backgroundColor: '#2B7CE9',
    color: 'white',
    border: 'none',
    padding: '8px 16px',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
  },
};
