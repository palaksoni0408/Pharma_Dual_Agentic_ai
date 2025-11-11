import React, { useState, useRef, useEffect } from 'react';
import {
  Container,
  Box,
  AppBar,
  Toolbar,
  Typography,
  TextField,
  Button,
  Paper,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Card,
  CardContent,
  CircularProgress,
  Chip,
  Grid,
  Divider,
  Alert
} from '@mui/material';
import {
  Send as SendIcon,
  Download as DownloadIcon,
  Assessment as AssessmentIcon,
  Science as ScienceIcon,
  AutoAwesome as AIIcon
} from '@mui/icons-material';
import ReactMarkdown from 'react-markdown';
import AgentResultDisplay from './components/AgentResultDisplay';
import axios from 'axios';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [query, setQuery] = useState('');
  const [provider, setProvider] = useState('openai');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [usageStats, setUsageStats] = useState(null);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
    fetchUsageStats();
  }, [results]);

  const fetchUsageStats = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/usage`);
      setUsageStats(response.data);
    } catch (err) {
      console.error('Error fetching usage stats:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${API_URL}/api/query`, {
        query: query,
        provider: provider
      });

      setResults(response.data.data);
      setUsageStats(response.data.usage_stats);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const downloadReport = async () => {
    if (!results?.report_path) return;

    const filename = results.report_path.split('/').pop();
    window.open(`${API_URL}/api/reports/${filename}`, '_blank');
  };

  const sampleQueries = [
    "Find molecules for treating rare respiratory diseases with low competition",
    "Identify repurposing opportunities for metformin in oncology",
    "Analyze patent landscape for GLP-1 agonists",
    "Research unmet needs in pediatric inflammatory diseases"
  ];

  return (
    <Box sx={{ flexGrow: 1, minHeight: '100vh', bgcolor: '#f5f7fa' }}>
      <AppBar position="static" sx={{ bgcolor: '#1a237e' }}>
        <Toolbar>
          <ScienceIcon sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Pharmaceutical Agentic AI Research Platform
          </Typography>
          <Chip 
            icon={<AIIcon />} 
            label={provider === 'openai' ? 'ChatGPT' : 'Gemini 2.5'}
            color="secondary"
            sx={{ mr: 2 }}
          />
          {usageStats && (
            <Chip 
              label={`$${usageStats.total_cost_usd.toFixed(4)}`}
              color="warning"
              size="small"
            />
          )}
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card elevation={3}>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                  <AssessmentIcon sx={{ mr: 1 }} />
                  Research Query
                </Typography>
                
                <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
                  <FormControl fullWidth sx={{ mb: 2 }}>
                    <InputLabel>AI Provider</InputLabel>
                    <Select
                      value={provider}
                      label="AI Provider"
                      onChange={(e) => setProvider(e.target.value)}
                    >
                      <MenuItem value="openai">ChatGPT (GPT-4)</MenuItem>
                      <MenuItem value="gemini">Gemini 2.5 Flash</MenuItem>
                    </Select>
                  </FormControl>

                  <TextField
                    fullWidth
                    multiline
                    rows={6}
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Enter your pharmaceutical research query..."
                    variant="outlined"
                    sx={{ mb: 2 }}
                  />

                  <Button
                    type="submit"
                    variant="contained"
                    fullWidth
                    size="large"
                    disabled={loading || !query.trim()}
                    startIcon={loading ? <CircularProgress size={20} /> : <SendIcon />}
                    sx={{ bgcolor: '#1a237e' }}
                  >
                    {loading ? 'Researching...' : 'Start Research'}
                  </Button>
                </Box>

                <Divider sx={{ my: 3 }} />

                <Typography variant="subtitle2" gutterBottom color="text.secondary">
                  Sample Queries:
                </Typography>
                {sampleQueries.map((sq, idx) => (
                  <Chip
                    key={idx}
                    label={sq}
                    onClick={() => setQuery(sq)}
                    sx={{ m: 0.5 }}
                    size="small"
                    variant="outlined"
                  />
                ))}

                {usageStats && (
                  <Box sx={{ mt: 3 }}>
                    <Typography variant="subtitle2" gutterBottom>
                      Usage Statistics:
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      OpenAI: {usageStats.tokens_used.openai} tokens (${usageStats.total_cost.openai.toFixed(4)})
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Gemini: {usageStats.tokens_used.gemini} tokens (${usageStats.total_cost.gemini.toFixed(4)})
                    </Typography>
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={8}>
            <Card elevation={3} sx={{ minHeight: '600px' }}>
              <CardContent>
                {error && (
                  <Alert severity="error" sx={{ mb: 2 }}>
                    {error}
                  </Alert>
                )}

                {!results && !loading && (
                  <Box sx={{ textAlign: 'center', py: 8 }}>
                    <ScienceIcon sx={{ fontSize: 80, color: '#ccc', mb: 2 }} />
                    <Typography variant="h5" color="text.secondary">
                      Ready to Research
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                      Enter a query to start multi-agent pharmaceutical research
                    </Typography>
                  </Box>
                )}

                {loading && (
                  <Box sx={{ textAlign: 'center', py: 8 }}>
                    <CircularProgress size={60} />
                    <Typography variant="h6" sx={{ mt: 2 }}>
                      AI Agents Working...
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Analyzing clinical trials, patents, market data, and scientific literature
                    </Typography>
                  </Box>
                )}

                {results && (
                  <Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                      <Typography variant="h6">
                        Research Results
                      </Typography>
                      {results.report_path && (
                        <Button
                          variant="contained"
                          startIcon={<DownloadIcon />}
                          onClick={downloadReport}
                          size="small"
                        >
                          Download Report
                        </Button>
                      )}
                    </Box>

                    <Paper elevation={1} sx={{ p: 2, mb: 2, bgcolor: '#f5f5f5' }}>
                      <Typography variant="subtitle2" color="primary">
                        Query: {results.query}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Intent: {results.plan.intent}
                      </Typography>
                    </Paper>

                    <Paper elevation={1} sx={{ p: 3, mb: 2 }}>
                      <Typography variant="h6" gutterBottom>
                        Executive Summary
                      </Typography>
                      <Box className="markdown-content">
                        <ReactMarkdown>{results.synthesis}</ReactMarkdown>
                      </Box>
                    </Paper>

                    <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
                      Detailed Agent Findings
                    </Typography>
                    
                    {Object.entries(results.agent_results).map(([agentName, agentResult]) => (
                      <Paper key={agentName} elevation={1} sx={{ p: 2, mb: 2 }}>
                        <Typography variant="subtitle1" color="primary" gutterBottom>
                          {agentName.replace(/_/g, ' ').toUpperCase()}
                        </Typography>
                        <AgentResultDisplay data={agentResult.data} />
                      </Paper>
                    ))}

                    <div ref={messagesEndRef} />
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}

export default App;
