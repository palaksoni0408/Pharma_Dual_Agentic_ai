# API Documentation

## Endpoints

### POST /api/query

Process pharmaceutical research query

**Request:**

```json
{
  "query": "string",
  "provider": "openai|gemini",
  "model": "string (optional)"
}
```

**Response:**

```json
{
  "success": true,
  "query": "string",
  "plan": {},
  "agent_results": {},
  "synthesis": "string",
  "report_path": "string",
  "timestamp": "datetime",
  "usage_stats": {}
}
```

### GET /api/usage

Get API usage statistics

### POST /api/upload

Upload documents for analysis

### GET /api/reports/{filename}

Download generated report
