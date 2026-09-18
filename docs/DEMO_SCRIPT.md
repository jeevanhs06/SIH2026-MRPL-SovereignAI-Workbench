# Demo Script

1. Start backend/frontend locally or with Docker.
2. Open frontend dashboard (`http://localhost:5173`).
3. Check health and security status cards.
4. Upload a sample `.txt` document.
5. Create a task requiring review.
6. Poll task status via UI/API until `waiting_for_review`.
7. Approve task through `POST /tasks/{id}/review`.
8. Show generated output files in `data/outputs` and audit log in `data/audit/audit.jsonl`.
