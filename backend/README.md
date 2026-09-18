# Backend Service

FastAPI backend for the SovereignAI Workbench scaffold.

## Run locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn main:app --reload --port 8000
```

## Test

```bash
cd /path/to/repo
PYTHONPATH=backend pytest tests/unit -q
```

This scaffold intentionally uses local-only placeholder implementations for model and OCR-heavy flows.
