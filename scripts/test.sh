#!/bin/bash

echo "🧪 Running tests..."

# Backend tests

cd backend

pytest

# Frontend tests

cd ../frontend

npm test -- --watchAll=false

echo "✅ Tests complete!"
