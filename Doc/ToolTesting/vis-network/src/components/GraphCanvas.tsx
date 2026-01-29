import { useGraph } from '../context/GraphContext';
import { useVisNetwork } from '../hooks/useVisNetwork';

export function GraphCanvas() {
  const { nodes, edges, setSelection } = useGraph();

  const { containerRef } = useVisNetwork({
    nodes,
    edges,
    onSelect: setSelection,
  });

  return (
    <div
      ref={containerRef}
      style={{
        width: '100%',
        height: '100%',
        border: '1px solid #ccc',
        backgroundColor: '#fafafa',
      }}
    />
  );
}
