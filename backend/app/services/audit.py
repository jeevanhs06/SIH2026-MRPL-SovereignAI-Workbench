import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.config import get_settings

REDACT_KEYS = {"password", "token", "secret", "api_key", "authorization"}
LONG_TEXT_KEYS = {"content", "document_text", "raw_text", "prompt"}


class AuditLogger:
    def __init__(self, file_path: Path | None = None) -> None:
        settings = get_settings()
        self.file_path = file_path or (settings.audit_dir / "audit.jsonl")
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def log_event(self, event_type: str, payload: dict[str, Any]) -> None:
        safe_payload = self._redact(payload)
        record = {
            "timestamp": datetime.now(UTC).isoformat(),
            "event_type": event_type,
            "payload": safe_payload,
        }
        with self.file_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    def _redact(self, value: Any) -> Any:
        if isinstance(value, dict):
            result: dict[str, Any] = {}
            for key, nested_value in value.items():
                if key.lower() in REDACT_KEYS:
                    result[key] = "***REDACTED***"
                elif key.lower() in LONG_TEXT_KEYS:
                    result[key] = "***REDACTED_CONTENT***"
                else:
                    result[key] = self._redact(nested_value)
            return result
        if isinstance(value, list):
            return [self._redact(item) for item in value]
        if isinstance(value, str):
            masked = re.sub(r"(?i)(bearer\s+)[a-z0-9\-._~+/]+=*", r"\1***REDACTED***", value)
            if len(masked) > 500:
                return masked[:500] + "..."
            return masked
        return value
