#!/usr/bin/env bash
set -euo pipefail

API_BASE_URL="${API_BASE_URL:-http://127.0.0.1:8000}"
response="$(curl -fsS "$API_BASE_URL/security/network-status")"

echo "$response" | python -m json.tool

if echo "$response" | grep -q '"offline_mode": true'; then
  echo "[offline-check] offline_mode is enabled"
else
  echo "[offline-check] offline_mode is not enabled"
  exit 1
fi
