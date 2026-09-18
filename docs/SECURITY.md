# Security and Sovereignty (Starter)

- Local-only defaults (`SOVAI_OFFLINE_MODE=true`, local model endpoint).
- Upload validation: extension allowlist + size limits.
- Path traversal protection for stored uploads.
- Append-only JSONL audit logging with basic redaction.
- No arbitrary shell execution.

## Not yet production hardening

- Full authentication/authorization
- Host firewall proof and SIEM integration
- Full malware scanning, DLP, and encryption-at-rest controls
