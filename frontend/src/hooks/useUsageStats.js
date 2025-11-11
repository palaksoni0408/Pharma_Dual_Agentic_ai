import { useState, useEffect } from 'react';
import { getUsageStats } from '../services/api';

export const useUsageStats = (refreshInterval = 30000) => {
  const [stats, setStats] = useState(null);

  const fetchStats = async () => {
    try {
      const data = await getUsageStats();
      setStats(data);
    } catch (err) {
      console.error('Error fetching usage stats:', err);
    }
  };

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, refreshInterval);
    return () => clearInterval(interval);
  }, [refreshInterval]);

  return { stats, refresh: fetchStats };
};