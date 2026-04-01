#!/bin/bash
# Health check script

set -e

APP_URL=${APP_URL:-http://localhost:8000}
TIMEOUT=${TIMEOUT:-30}
INTERVAL=${INTERVAL:-5}

echo "Checking health of $APP_URL..."

elapsed=0
while [ $elapsed -lt $TIMEOUT ]; do
    if curl -sf "${APP_URL}/health" > /dev/null 2>&1; then
        echo "✓ Application is healthy"
        exit 0
    fi
    
    echo "Waiting for application to be healthy..."
    sleep $INTERVAL
    elapsed=$((elapsed + INTERVAL))
done

echo "✗ Application failed to become healthy within $TIMEOUT seconds"
exit 1
