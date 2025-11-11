import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const processQuery = async (query, provider = 'openai', model = null) => {
  const response = await api.post('/api/query', { query, provider, model });
  return response.data;
};

export const sendChatMessage = async (messages, provider = 'openai') => {
  const response = await api.post('/api/chat', { messages, provider });
  return response.data;
};

export const getUsageStats = async () => {
  const response = await api.get('/api/usage');
  return response.data;
};

export const downloadReport = (filename) => {
  return `${API_URL}/api/reports/${filename}`;
};

export const uploadDocuments = async (files) => {
  const formData = new FormData();
  files.forEach(file => formData.append('files', file));
  
  const response = await api.post('/api/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export default api;