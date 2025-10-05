import React from 'react';

const DataTable = ({ data, title }) => {
  if (!data) return null;

  // Parse CSV data if it's a string
  const parseCSV = (csvString) => {
    const lines = csvString.trim().split('\n');
    const headers = lines[0].split(',');
    const rows = lines.slice(1).map(line => line.split(','));
    
    return { headers, rows };
  };

  // Parse JSON data if it's a string
  const parseJSON = (jsonString) => {
    try {
      const data = JSON.parse(jsonString);
      if (data.data && Array.isArray(data.data)) {
        const headers = Object.keys(data.data[0] || {});
        const rows = data.data.map(row => Object.values(row));
        return { headers, rows };
      }
      return { headers: [], rows: [] };
    } catch (e) {
      return { headers: ['Error'], rows: [[`Failed to parse JSON: ${e.message}`]] };
    }
  };

  // Determine data type and parse accordingly
  let parsedData = { headers: [], rows: [] };
  if (typeof data === 'string') {
    if (data.startsWith('{') || data.startsWith('[')) {
      parsedData = parseJSON(data);
    } else {
      parsedData = parseCSV(data);
    }
  } else if (typeof data === 'object') {
    parsedData = parseJSON(JSON.stringify(data));
  }

  const { headers, rows } = parsedData;

  return (
    <div className="mb-8">
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border border-gray-200">
          <thead>
            <tr className="bg-gray-100">
              {headers.map((header, index) => (
                <th key={index} className="py-2 px-4 border-b text-left">
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, rowIndex) => (
              <tr key={rowIndex} className={rowIndex % 2 === 0 ? 'bg-gray-50' : 'bg-white'}>
                {row.map((cell, cellIndex) => (
                  <td key={cellIndex} className="py-2 px-4 border-b">
                    {cell}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DataTable;
