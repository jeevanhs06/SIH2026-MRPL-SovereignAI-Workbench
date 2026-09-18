from pathlib import Path


class IngestionService:
    def ingest_document(self, file_path: str) -> dict[str, str | bool]:
        path = Path(file_path)
        extension = path.suffix.lower()

        if extension in {".txt", ".md"}:
            text = path.read_text(encoding="utf-8", errors="ignore")
            return {
                "document_type": extension,
                "extractor": "plain_text",
                "text": text,
                "ocr_required": False,
            }

        if extension == ".pdf":
            return self._ingest_pdf(path)

        if extension in {".png", ".jpg", ".jpeg"}:
            return {
                "document_type": extension,
                "extractor": "placeholder_ocr",
                "text": "OCR/image extraction placeholder. Integrate local OCR pipeline in next iteration.",
                "ocr_required": True,
            }

        return {
            "document_type": extension,
            "extractor": "unsupported",
            "text": "Unsupported document type for starter ingestion",
            "ocr_required": False,
        }

    def _ingest_pdf(self, path: Path) -> dict[str, str | bool]:
        try:
            import fitz  # type: ignore
        except Exception:
            return {
                "document_type": ".pdf",
                "extractor": "pdf_placeholder",
                "text": "PyMuPDF not installed. PDF text extraction placeholder response.",
                "ocr_required": True,
            }

        with fitz.open(path) as doc:
            metadata = doc.metadata or {}
            text_blocks = [page.get_text("text") for page in doc]
        return {
            "document_type": ".pdf",
            "extractor": "pymupdf",
            "text": "\n".join(text_blocks).strip(),
            "metadata": str(metadata),
            "ocr_required": False,
        }
