#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "[bootstrap] Installing backend dependencies"
python -m pip install -r "$REPO_ROOT/backend/requirements-dev.txt"

echo "[bootstrap] Installing frontend dependencies"
cd "$REPO_ROOT/frontend"
npm install

echo "[bootstrap] Complete"
