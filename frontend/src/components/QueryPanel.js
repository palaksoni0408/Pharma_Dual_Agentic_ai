import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Box,
  Divider,
  Chip,
  CircularProgress
} from '@mui/material';
import { Send as SendIcon, Assessment as AssessmentIcon } from '@mui/icons-material';

const QueryPanel = ({ 
  query, 
  setQuery, 
  provider, 
  setProvider, 
  loading, 
  onSubmit,
  sampleQueries,
  usageStats 
}) => {
  return (
    <Card elevation={3}>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
          <AssessmentIcon sx={{ mr: 1 }} />
          Research Query
        </Typography>
        
        <Box component="form" onSubmit={onSubmit} sx={{ mt: 2 }}>
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
  );
};

export default QueryPanel;