#!/usr/bin/env bash
set -euo pipefail

API_BASE_URL="${API_BASE_URL:-http://127.0.0.1:8000}"
COLLECTION="${1:-manuals}"

curl -fsS -X POST "$API_BASE_URL/knowledge/ingest" \
  -H "Content-Type: application/json" \
  -d "{\"collection\": \"$COLLECTION\"}" | python -m json.tool
