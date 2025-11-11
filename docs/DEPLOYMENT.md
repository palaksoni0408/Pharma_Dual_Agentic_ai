# Deployment Guide

## Prerequisites

- Docker & Docker Compose
- Domain name (for production)
- SSL certificate

## Steps

1. Clone repository
2. Configure environment variables
3. Run `make setup`
4. Run `make prod`
5. Configure nginx reverse proxy
6. Enable HTTPS

## Monitoring

- Check logs: `make logs`
- Health check: `curl http://localhost/health`
