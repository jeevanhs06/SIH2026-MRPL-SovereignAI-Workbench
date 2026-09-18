# Architecture

## Current scaffold

- `frontend/`: React + TypeScript + Vite dashboard.
- `backend/`: FastAPI API with modular routes/services.
- `data/`: local storage roots for inputs, outputs, tmp, vector index, audit logs.
- `knowledge_base/`: manuals/SOP/template/sample source documents.

## Backend modules

- Routes: `health`, `auth`, `documents`, `knowledge`, `tasks`, `security`
- Services: storage validation, ingestion, mock model gateway, knowledge index/search, task orchestration, output generation, audit log, network status

## Placeholder boundaries

- OCR for images is currently placeholder-only.
- Model inference is mock/local placeholder.
- Retrieval is deterministic lexical search over local JSON index.
