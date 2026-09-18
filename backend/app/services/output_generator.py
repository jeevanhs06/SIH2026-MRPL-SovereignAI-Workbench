import json
from pathlib import Path
from uuid import uuid4

from app.config import get_settings


class OutputGenerator:
    def __init__(self) -> None:
        self.settings = get_settings()

    def generate_json(self, task_id: str, payload: dict) -> str:
        output_path = self.settings.output_dir / f"{task_id}_result.json"
        output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        return str(output_path)

    def generate_docx_placeholder(self, task_id: str, content: str) -> str:
        return self._write_placeholder(task_id, "docx", content)

    def generate_xlsx_placeholder(self, task_id: str, content: str) -> str:
        return self._write_placeholder(task_id, "xlsx", content)

    def generate_pdf_placeholder(self, task_id: str, content: str) -> str:
        return self._write_placeholder(task_id, "pdf", content)

    def _write_placeholder(self, task_id: str, output_type: str, content: str) -> str:
        output_path = self.settings.output_dir / f"{task_id}_{output_type}.placeholder.txt"
        output_path.write_text(
            (
                f"Placeholder for {output_type.upper()} output.\n"
                "Replace this adapter with a real generator once dependencies are selected.\n\n"
                f"Task content preview:\n{content[:1000]}\n"
                f"Reference: {uuid4()}"
            ),
            encoding="utf-8",
        )
        return str(output_path)
