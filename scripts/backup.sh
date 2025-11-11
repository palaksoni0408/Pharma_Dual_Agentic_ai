#!/bin/bash

BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"

mkdir -p $BACKUP_DIR

# Backup reports

cp -r backend/reports $BACKUP_DIR/

# Backup database

docker-compose exec -T redis redis-cli SAVE

# Try to copy dump from the redis container dynamically
REDIS_CONTAINER=$(docker-compose ps -q redis)
if [ -n "$REDIS_CONTAINER" ]; then
  docker cp ${REDIS_CONTAINER}:/data/dump.rdb $BACKUP_DIR/ || echo "⚠️ Could not copy Redis dump.rdb"
else
  echo "⚠️ Redis container not found"
fi

echo "✅ Backup created: $BACKUP_DIR"
