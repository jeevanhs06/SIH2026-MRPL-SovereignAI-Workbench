import hashlib
import os
import re
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.config import get_settings


class StorageValidationError(ValueError):
    pass


class StorageService:
    FILENAME_RE = re.compile(r"[^a-zA-Z0-9._-]+")

    def __init__(self) -> None:
        self.settings = get_settings()

    def _safe_filename(self, original_name: str) -> str:
        base_name = Path(original_name).name
        sanitized = self.FILENAME_RE.sub("_", base_name).strip("._") or "upload"
        return sanitized

    def _validate_extension(self, extension: str) -> None:
        if extension.lower() not in self.settings.allowed_upload_extensions:
            raise StorageValidationError(f"Extension '{extension}' is not allowed")

    def _ensure_within_inputs(self, target: Path) -> None:
        inputs_root = self.settings.input_dir.resolve()
        target_resolved = target.resolve()
        if os.path.commonpath([str(inputs_root), str(target_resolved)]) != str(inputs_root):
            raise StorageValidationError("Path traversal attempt blocked")

    async def save_upload(self, upload: UploadFile) -> dict[str, str | int]:
        raw = await upload.read()
        size_bytes = len(raw)
        if size_bytes == 0:
            raise StorageValidationError("Empty uploads are not allowed")
        if size_bytes > self.settings.max_upload_size_bytes:
            raise StorageValidationError("Upload exceeds configured size limit")

        extension = Path(upload.filename or "").suffix.lower()
        self._validate_extension(extension)

        safe_name = self._safe_filename(upload.filename or "upload")
        document_id = str(uuid4())
        stored_name = f"{document_id}_{safe_name}"
        destination = self.settings.input_dir / stored_name
        self._ensure_within_inputs(destination)

        checksum = hashlib.sha256(raw).hexdigest()
        destination.write_bytes(raw)

        return {
            "document_id": document_id,
            "filename": safe_name,
            "extension": extension,
            "size_bytes": size_bytes,
            "checksum_sha256": checksum,
            "stored_path": str(destination),
        }
