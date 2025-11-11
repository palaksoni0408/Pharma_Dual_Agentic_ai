import { useState } from 'react';
import { processQuery } from '../services/api';

export const useQuery = () => {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const executeQuery = async (query, provider) => {
    setLoading(true);
    setError(null);

    try {
      const data = await processQuery(query, provider);
      setResults(data.data);
      return data;
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { loading, results, error, executeQuery };
};