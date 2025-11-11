import React from 'react';
import {
  Box,
  Typography,
  Link,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  Divider
} from '@mui/material';
import { OpenInNew as OpenInNewIcon, Article as ArticleIcon, Language as LanguageIcon } from '@mui/icons-material';
import ReactMarkdown from 'react-markdown';

const AgentResultDisplay = ({ data }) => {
  if (!data) return null;

  // If data is a string, treat it as markdown
  if (typeof data === 'string') {
    return (
      <Box className="markdown-content">
        <ReactMarkdown>{data}</ReactMarkdown>
      </Box>
    );
  }

  // If data has an 'analysis' field, use that
  if (data.analysis) {
    return (
      <Box className="markdown-content">
        <ReactMarkdown>{data.analysis}</ReactMarkdown>
      </Box>
    );
  }

  // Format structured data
  return (
    <Box>
      {/* Summary */}
      {data.summary && (
        <Box sx={{ mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Summary
          </Typography>
          <Box className="markdown-content">
            <ReactMarkdown>{data.summary}</ReactMarkdown>
          </Box>
        </Box>
      )}

      {/* PubMed Papers */}
      {data.pubmed_papers && Array.isArray(data.pubmed_papers) && data.pubmed_papers.length > 0 && (
        <Box sx={{ mb: 3 }}>
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <ArticleIcon /> Research Papers ({data.pubmed_papers.length})
          </Typography>
          <TableContainer component={Paper} variant="outlined" sx={{ mt: 1 }}>
            <Table size="small">
              <TableHead>
                <TableRow sx={{ bgcolor: '#f5f5f5' }}>
                  <TableCell><strong>Title</strong></TableCell>
                  <TableCell><strong>Authors</strong></TableCell>
                  <TableCell><strong>Source</strong></TableCell>
                  <TableCell><strong>Year</strong></TableCell>
                  <TableCell><strong>Link</strong></TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {data.pubmed_papers.map((paper, index) => (
                  <TableRow key={index} hover>
                    <TableCell>{paper.title || 'N/A'}</TableCell>
                    <TableCell>
                      {paper.authors && Array.isArray(paper.authors)
                        ? paper.authors.slice(0, 3).join(', ') + (paper.authors.length > 3 ? ' et al.' : '')
                        : 'N/A'}
                    </TableCell>
                    <TableCell>{paper.source || 'N/A'}</TableCell>
                    <TableCell>{paper.pubdate || 'N/A'}</TableCell>
                    <TableCell>
                      {paper.url ? (
                        <Link
                          href={paper.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}
                        >
                          View <OpenInNewIcon fontSize="small" />
                        </Link>
                      ) : (
                        paper.pmid ? (
                          <Link
                            href={`https://pubmed.ncbi.nlm.nih.gov/${paper.pmid}/`}
                            target="_blank"
                            rel="noopener noreferrer"
                            sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}
                          >
                            PubMed <OpenInNewIcon fontSize="small" />
                          </Link>
                        ) : 'N/A'
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Box>
      )}

      {/* Web Sources */}
      {data.web_sources && Array.isArray(data.web_sources) && data.web_sources.length > 0 && (
        <Box sx={{ mb: 3 }}>
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <LanguageIcon /> Web Sources ({data.web_sources.length})
          </Typography>
          <Box sx={{ mt: 1 }}>
            {data.web_sources.map((source, index) => (
              <Paper
                key={index}
                elevation={0}
                sx={{
                  p: 2,
                  mb: 1,
                  border: '1px solid #e0e0e0',
                  '&:hover': { bgcolor: '#f9f9f9' }
                }}
              >
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                  <Box sx={{ flex: 1 }}>
                    <Typography variant="subtitle2" gutterBottom>
                      {source.title || 'Untitled'}
                    </Typography>
                    {source.snippet && (
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                        {source.snippet}
                      </Typography>
                    )}
                    <Box sx={{ display: 'flex', gap: 1, alignItems: 'center', flexWrap: 'wrap' }}>
                      {source.source && (
                        <Chip label={source.source} size="small" variant="outlined" />
                      )}
                      {source.url && (
                        <Link
                          href={source.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          sx={{ display: 'flex', alignItems: 'center', gap: 0.5, fontSize: '0.875rem' }}
                        >
                          Visit Source <OpenInNewIcon fontSize="small" />
                        </Link>
                      )}
                    </Box>
                  </Box>
                </Box>
              </Paper>
            ))}
          </Box>
        </Box>
      )}

      {/* Key Statistics */}
      {(data.total_sources || data.key_papers) && (
        <Box sx={{ mb: 3 }}>
          <Divider sx={{ my: 2 }} />
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
            {data.total_sources && (
              <Chip
                label={`Total Sources: ${data.total_sources}`}
                color="primary"
                variant="outlined"
              />
            )}
            {data.key_papers && (
              <Chip
                label={`Key Papers: ${data.key_papers}`}
                color="secondary"
                variant="outlined"
              />
            )}
            {data.analysis_type && (
              <Chip
                label={`Type: ${data.analysis_type}`}
                variant="outlined"
              />
            )}
          </Box>
        </Box>
      )}

      {/* Other data fields as key-value pairs */}
      {Object.entries(data).map(([key, value]) => {
        // Skip already displayed fields
        if (['summary', 'pubmed_papers', 'web_sources', 'total_sources', 'key_papers', 'analysis_type', 'analysis'].includes(key)) {
          return null;
        }
        
        // Skip if value is null, undefined, or empty
        if (!value || (typeof value === 'object' && Object.keys(value).length === 0)) {
          return null;
        }

        return (
          <Box key={key} sx={{ mb: 2 }}>
            <Typography variant="subtitle2" gutterBottom sx={{ textTransform: 'capitalize' }}>
              {key.replace(/_/g, ' ')}
            </Typography>
            {typeof value === 'object' ? (
              <Box component="pre" sx={{ 
                bgcolor: '#f5f5f5', 
                p: 2, 
                borderRadius: 1, 
                overflow: 'auto',
                fontSize: '0.875rem'
              }}>
                {JSON.stringify(value, null, 2)}
              </Box>
            ) : (
              <Typography variant="body2">{String(value)}</Typography>
            )}
          </Box>
        );
      })}
    </Box>
  );
};

export default AgentResultDisplay;

