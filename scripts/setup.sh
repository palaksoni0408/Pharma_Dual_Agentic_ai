#!/bin/bash

echo "🚀 Setting up Pharma AI System..."

# Create directories
mkdir -p backend/reports backend/uploads backend/logs

# Copy environment files if they don't exist
if [ -f backend/.env.example ] && [ ! -f backend/.env ]; then
  cp backend/.env.example backend/.env
fi

if [ -f frontend/.env.example ] && [ ! -f frontend/.env ]; then
  cp frontend/.env.example frontend/.env
fi

if [ -f .env.example ] && [ ! -f .env ]; then
  cp .env.example .env
fi

echo "✅ Please edit .env files with your API keys"
echo ""
echo "Backend: backend/.env"
echo "Frontend: frontend/.env"
echo "Root: .env"
echo ""
echo "Then run: docker-compose up -d"
