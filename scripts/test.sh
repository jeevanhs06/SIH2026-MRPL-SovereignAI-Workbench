#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$REPO_ROOT"
PYTHONPATH=backend pytest tests/unit -q

cd "$REPO_ROOT/frontend"
npm run test -- --run
