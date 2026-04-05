#!/bin/bash
# health-check.sh — 檢查服務是否正常啟動
URL=${1:-http://localhost:8000/health}
MAX_RETRIES=10
RETRY_INTERVAL=3

for i in $(seq 1 $MAX_RETRIES); do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$URL" 2>/dev/null)
  if [ "$STATUS" = "200" ]; then
    echo "✅ Health check passed (attempt $i)"
    exit 0
  fi
  echo "⏳ Waiting... (attempt $i/$MAX_RETRIES)"
  sleep $RETRY_INTERVAL
done

echo "❌ Health check failed after $MAX_RETRIES attempts"
exit 1

