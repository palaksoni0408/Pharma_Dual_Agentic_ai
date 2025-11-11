# Pharma AI Frontend

React-based frontend for the pharmaceutical research AI system.

## Prerequisites

- Node.js 18+ and npm

## Setup

```bash
npm install
cp .env.example .env
```

Update `.env` as needed (e.g., `REACT_APP_API_BASE_URL`).

## Run (development)

```bash
npm start
```

Runs on `http://localhost:3000` by default.

## Build (production)

```bash
npm run build
```

Outputs static files to `build/`.

## Preview production build

```bash
npx serve -s build
```

## Troubleshooting

- If the backend runs on a different port/host, set `REACT_APP_API_BASE_URL` in `.env`.
- If port 3000 is busy, set `PORT=3001` in `.env` before `npm start`.