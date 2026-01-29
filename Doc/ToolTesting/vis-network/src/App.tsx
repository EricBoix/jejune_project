import { useEffect, useState, useRef } from 'react';
import { GraphProvider } from './context/GraphContext';
import { GraphCanvas } from './components/GraphCanvas';
import { InfoPanel } from './components/InfoPanel';
import { EditPanel } from './components/EditPanel';
import { useRdfStore } from './hooks/useRdfStore';
import sampleTtl from './data/sample.ttl?raw';

function AppContent() {
  const { loadRdfFromString, loadRdfFromFile } = useRdfStore();
  const [activePanel, setActivePanel] = useState<'info' | 'edit'>('info');
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    loadRdfFromString(sampleTtl);
  }, [loadRdfFromString]);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      loadRdfFromFile(file);
    }
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.title}>Knowledge Graph Visualization</h1>
        <div style={styles.toolbar}>
          <input
            type="file"
            accept=".ttl,.rdf,.nt"
            onChange={handleFileUpload}
            ref={fileInputRef}
            style={{ display: 'none' }}
          />
          <button
            onClick={() => fileInputRef.current?.click()}
            style={styles.uploadButton}
          >
            Load RDF File
          </button>
        </div>
      </header>
      <div style={styles.main}>
        <div style={styles.canvasContainer}>
          <GraphCanvas />
        </div>
        <div style={styles.sidebar}>
          <div style={styles.tabs}>
            <button
              onClick={() => setActivePanel('info')}
              style={{
                ...styles.tab,
                ...(activePanel === 'info' ? styles.activeTab : {}),
              }}
            >
              Info
            </button>
            <button
              onClick={() => setActivePanel('edit')}
              style={{
                ...styles.tab,
                ...(activePanel === 'edit' ? styles.activeTab : {}),
              }}
            >
              Edit
            </button>
          </div>
          <div style={styles.panelContainer}>
            {activePanel === 'info' ? <InfoPanel /> : <EditPanel />}
          </div>
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <GraphProvider>
      <AppContent />
    </GraphProvider>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    height: '100vh',
    fontFamily: 'system-ui, -apple-system, sans-serif',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '12px 24px',
    backgroundColor: '#2B7CE9',
    color: 'white',
  },
  title: {
    margin: 0,
    fontSize: '20px',
    fontWeight: 600,
  },
  toolbar: {
    display: 'flex',
    gap: '8px',
  },
  uploadButton: {
    backgroundColor: 'white',
    color: '#2B7CE9',
    border: 'none',
    padding: '8px 16px',
    borderRadius: '4px',
    cursor: 'pointer',
    fontWeight: 500,
  },
  main: {
    display: 'flex',
    flex: 1,
    overflow: 'hidden',
  },
  canvasContainer: {
    flex: 1,
    position: 'relative',
  },
  sidebar: {
    width: '300px',
    display: 'flex',
    flexDirection: 'column',
    borderLeft: '1px solid #ccc',
  },
  tabs: {
    display: 'flex',
    borderBottom: '1px solid #ccc',
  },
  tab: {
    flex: 1,
    padding: '12px',
    border: 'none',
    backgroundColor: '#f5f5f5',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: 500,
  },
  activeTab: {
    backgroundColor: 'white',
    borderBottom: '2px solid #2B7CE9',
  },
  panelContainer: {
    flex: 1,
    overflow: 'auto',
  },
};

export default App;
