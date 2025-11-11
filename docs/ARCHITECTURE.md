# System Architecture

## Components

1. **Master Agent** - Orchestrates workflow
2. **Worker Agents** - Specialized research agents
3. **LLM Manager** - Manages AI API calls
4. **Web Scraper** - Fetches external data
5. **Report Generator** - Creates PDF reports

## Data Flow

1. User submits query
2. Master Agent decomposes query
3. Worker Agents execute in parallel
4. Results synthesized
5. Report generated
