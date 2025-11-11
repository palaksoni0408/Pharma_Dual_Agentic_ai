#!/bin/bash

echo "🚀 Deploying Pharma AI System..."

# Build and deploy

docker-compose -f docker-compose.prod.yml build

docker-compose -f docker-compose.prod.yml up -d

echo "✅ Deployment complete!"

echo "Access at: http://your-domain.com"
