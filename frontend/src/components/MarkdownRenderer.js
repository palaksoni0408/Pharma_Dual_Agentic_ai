import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Box } from '@mui/material';

const MarkdownRenderer = ({ content }) => {
  return (
    <Box className="markdown-content">
      <ReactMarkdown>{content}</ReactMarkdown>
    </Box>
  );
};

export default MarkdownRenderer;