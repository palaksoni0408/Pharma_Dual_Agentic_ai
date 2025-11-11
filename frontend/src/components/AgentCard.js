import React from 'react';
import { Card, CardContent, Typography, Chip } from '@mui/material';

const AgentCard = ({ name, status, result }) => {
  return (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Typography variant="h6">{name}</Typography>
        <Chip label={status} size="small" color={status === 'completed' ? 'success' : 'info'} />
        {result && <Typography variant="body2" sx={{ mt: 1 }}>{result}</Typography>}
      </CardContent>
    </Card>
  );
};

export default AgentCard;