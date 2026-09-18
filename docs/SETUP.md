# Setup

## Local

```bash
cp .env.example .env
python -m pip install -r backend/requirements-dev.txt
cd frontend && npm install && cd ..
cd backend && uvicorn main:app --reload --port 8000
cd frontend && npm run dev
```

## Docker

```bash
docker compose up --build
```

## Validation

```bash
PYTHONPATH=backend pytest tests/unit -q
cd frontend && npm run build && npm run test -- --run
```
