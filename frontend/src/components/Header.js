import React from 'react';
import { AppBar, Toolbar, Typography, Chip } from '@mui/material';
import { Science as ScienceIcon, AutoAwesome as AIIcon } from '@mui/icons-material';

const Header = ({ provider, usageStats }) => {
  return (
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
  );
};

export default Header;