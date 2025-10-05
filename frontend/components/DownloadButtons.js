import React from 'react';

const DownloadButtons = () => {
  const handleDownload = (type) => {
    // In a real implementation, this would call the appropriate backend endpoint
    // For this MVP, we'll just log the action
    console.log(`Download ${type} requested`);
    
    // Create a temporary link element to trigger download
    const link = document.createElement('a');
    link.href = `/api/download/${type}`;
    link.download = `processed_data.${type}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="flex space-x-4 mb-4">
      <button 
        onClick={() => handleDownload('csv')}
        className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
      >
        Download CSV
      </button>
      <button 
        onClick={() => handleDownload('json')}
        className="bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded"
      >
        Download JSON
      </button>
      <button 
        onClick={() => handleDownload('faiss')}
        className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
      >
        Download FAISS Index
      </button>
    </div>
  );
};

export default DownloadButtons;
