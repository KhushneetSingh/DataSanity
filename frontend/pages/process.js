import Head from 'next/head';
import { useState } from 'react';
import DataTable from '../components/DataTable';
import DownloadButtons from '../components/DownloadButtons';

const API_URL = process.env.NEXT_PUBLIC_API_URL || '';

function ProcessPage() {
  const [prompt, setPrompt] = useState('');
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('prompt', prompt);
      console.log('Prompt entered:', prompt);

      if (file) {
        console.log('File selected:', file.name);
        formData.append('file', file);
      } else {
        console.log('No file selected');
      }
      console.log('FormData prepared:', formData);
      const response = await fetch(`${API_URL}/api/process`, {
        method: 'POST',
        body: formData,
      });
      console.log(response);
      if (!response.ok) {
        throw new Error(`Server responded with status ${response.status}`);
      }

      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Error processing request:', error);
      alert('An error occurred while processing the request. See console for details.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>Process Data — DataSanity</title>
        <meta name="description" content="Clean, generate, and enrich datasets with AI" />
      </Head>

      <div className="card" style={{ marginBottom: 24 }}>
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: 16 }}>
            <label
              htmlFor="prompt"
              style={{ display: 'block', fontSize: 13, fontWeight: 600, color: 'var(--ds-text-muted)', marginBottom: 8 }}
            >
              Data Processing Prompt
            </label>
            <textarea
              id="prompt"
              style={{
                width: '100%',
                minHeight: 100,
                padding: '12px 14px',
                background: 'var(--ds-bg)',
                border: '1px solid var(--ds-border)',
                borderRadius: 10,
                color: 'var(--ds-text)',
                fontSize: 14,
                fontFamily: 'inherit',
                resize: 'vertical',
                outline: 'none',
              }}
              placeholder="Describe what you want to do with your data… e.g., 'Clean this dataset and generate 30 new noisy examples'"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              required
            />
          </div>

          <div style={{ marginBottom: 16 }}>
            <label
              htmlFor="file-input"
              style={{ display: 'block', fontSize: 13, fontWeight: 600, color: 'var(--ds-text-muted)', marginBottom: 8 }}
            >
              Upload CSV Dataset (Optional)
            </label>
            <input
              type="file"
              id="file-input"
              accept=".csv"
              onChange={(e) => {
                setFile(e.target.files[0]);
                console.log('Selected file:', e.target.files[0]);
              }}
              style={{
                width: '100%',
                padding: 10,
                background: 'var(--ds-bg)',
                border: '1px solid var(--ds-border)',
                borderRadius: 10,
                color: 'var(--ds-text)',
                fontSize: 13,
              }}
            />
          </div>

          <button
            type="submit"
            className={`btn ${loading ? 'btn-ghost' : 'btn-primary'}`}
            disabled={loading}
            id="process-btn"
          >
            {loading ? 'Processing…' : 'Process Data'}
          </button>
        </form>
      </div>

      {results && (
        <div className="card">
          <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>Results</h2>

          {results.cleanedData && <DataTable data={results.cleanedData} title="Cleaned Data" />}
          {results.generatedData && <DataTable data={results.generatedData} title="Generated Data" />}
          {results.vectorizedData && <DataTable data={results.vectorizedData} title="Vectorized Data" />}
          {results.enrichedData && <DataTable data={results.enrichedData} title="Enriched Data" />}

          <DownloadButtons />
        </div>
      )}
    </>
  );
}

ProcessPage.pageTitle = 'Process Data';
export default ProcessPage;
