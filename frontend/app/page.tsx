'use client';

import { useState } from 'react';
import { searchRecipes } from '@/lib/api';

export default function Home() {
  const [result, setResult] = useState<string>('');

  const testAPI = async () => {
    try {
      const data = await searchRecipes(['chicken', 'rice']);
      setResult(JSON.stringify(data, null, 2));
    } catch (error) {
      setResult('Error: ' + error);
    }
  };

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">API Test</h1>
      
      <button 
        onClick={testAPI}
        className="px-4 py-2 bg-blue-500 text-white rounded"
      >
        Test API
      </button>

      <pre className="mt-4 p-4 bg-gray-100 rounded">
        {result || 'Click button to test'}
      </pre>
    </div>
  );
}