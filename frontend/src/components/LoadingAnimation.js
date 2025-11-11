import React from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';

const LoadingAnimation = ({ message = "Processing..." }) => {
  return (
    <Box sx={{ textAlign: 'center', py: 8 }}>
      <CircularProgress size={60} />
      <Typography variant="h6" sx={{ mt: 2 }}>
        {message}
      </Typography>
    </Box>
  );
};

export default LoadingAnimation;