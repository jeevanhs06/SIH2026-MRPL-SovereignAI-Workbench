# API (Scaffold)

Base URL: `http://localhost:8000`

- `GET /health`
- `GET /auth/status`
- `POST /documents/upload` (multipart `file`)
- `POST /knowledge/ingest` (`{"collection":"manuals|sops|templates|sample_documents"}`)
- `POST /knowledge/search` (`{"query":"...","limit":5}`)
- `GET /tasks`
- `POST /tasks`
- `GET /tasks/{task_id}`
- `POST /tasks/{task_id}/review`
- `GET /security/network-status`

See schema models in `backend/app/schemas.py`.
