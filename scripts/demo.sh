#!/usr/bin/env bash
set -euo pipefail

API_BASE_URL="${API_BASE_URL:-http://127.0.0.1:8000}"

echo "[demo] Health"
curl -fsS "$API_BASE_URL/health" | python -m json.tool

echo "[demo] Security status"
curl -fsS "$API_BASE_URL/security/network-status" | python -m json.tool
