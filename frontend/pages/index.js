import Head from 'next/head';
import { useState } from 'react';
import DataTable from '../components/DataTable';
import DownloadButtons from '../components/DownloadButtons';

export default function Home() {
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
      if (file) {
        formData.append('file', file);
      }
      
      const response = await fetch('/api/process', {
        method: 'POST',
        body: formData,
      });
      
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Error processing request:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <Head>
        <title>DataSanity - AI-Powered Data Processing</title>
        <meta name="description" content="Clean, generate, and enrich datasets with AI" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="container mx-auto py-8">
        <h1 className="text-3xl font-bold text-center mb-8">DataSanity</h1>
        
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="prompt">
                Data Processing Prompt
              </label>
              <textarea
                id="prompt"
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="Describe what you want to do with your data... e.g., 'Clean this dataset and generate 30 new noisy examples'"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                rows={4}
              />
            </div>
            
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="file">
                Upload CSV Dataset (Optional)
              </label>
              <input
                type="file"
                id="file"
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                accept=".csv"
                onChange={(e) => setFile(e.target.files[0])}
              />
            </div>
            
            <div className="flex items-center justify-between">
              <button
                type="submit"
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                disabled={loading}
              >
                {loading ? 'Processing...' : 'Process Data'}
              </button>
            </div>
          </form>
        </div>
        
        {results && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold mb-4">Results</h2>
            
            <DataTable data={results.cleanedData} title="Cleaned Data" />
            <DataTable data={results.generatedData} title="Generated Data" />
            <DataTable data={results.vectorizedData} title="Vectorized Data" />
            <DataTable data={results.enrichedData} title="Enriched Data" />
            
            <DownloadButtons />
          </div>
        )}
      </main>
    </div>
  );
}
