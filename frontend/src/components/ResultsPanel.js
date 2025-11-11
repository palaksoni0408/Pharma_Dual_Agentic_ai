import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Button,
  Paper,
  Box,
  CircularProgress
} from '@mui/material';
import { Download as DownloadIcon, Science as ScienceIcon } from '@mui/icons-material';
import ReactMarkdown from 'react-markdown';
import AgentResultDisplay from './AgentResultDisplay';

const ResultsPanel = ({ results, loading, error, onDownload }) => {
  if (error) {
    return (
      <Card elevation={3}>
        <CardContent>
          <Typography color="error">{error}</Typography>
        </CardContent>
      </Card>
    );
  }

  if (!results && !loading) {
    return (
      <Card elevation={3} sx={{ minHeight: '600px' }}>
        <CardContent>
          <Box sx={{ textAlign: 'center', py: 8 }}>
            <ScienceIcon sx={{ fontSize: 80, color: '#ccc', mb: 2 }} />
            <Typography variant="h5" color="text.secondary">
              Ready to Research
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              Enter a query to start multi-agent pharmaceutical research
            </Typography>
          </Box>
        </CardContent>
      </Card>
    );
  }

  if (loading) {
    return (
      <Card elevation={3} sx={{ minHeight: '600px' }}>
        <CardContent>
          <Box sx={{ textAlign: 'center', py: 8 }}>
            <CircularProgress size={60} />
            <Typography variant="h6" sx={{ mt: 2 }}>
              AI Agents Working...
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Analyzing clinical trials, patents, market data, and scientific literature
            </Typography>
          </Box>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card elevation={3} sx={{ minHeight: '600px' }}>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6">Research Results</Typography>
          {results.report_path && (
            <Button
              variant="contained"
              startIcon={<DownloadIcon />}
              onClick={onDownload}
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
      </CardContent>
    </Card>
  );
};

export default ResultsPanel;