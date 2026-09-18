import json

from app.config import get_settings


class KnowledgeBaseService:
    def __init__(self) -> None:
        settings = get_settings()
        self.knowledge_base_root = settings.knowledge_base_dir.resolve()
        self.index_file = settings.vector_store_dir / "knowledge_index.json"

    def ingest_collection(self, collection: str) -> dict[str, int | str]:
        base = (self.knowledge_base_root / collection).resolve()
        if self.knowledge_base_root not in base.parents:
            raise ValueError("Invalid knowledge collection path")
        if not base.exists() or not base.is_dir():
            raise ValueError("Source directory does not exist")

        indexed_docs: list[dict[str, str]] = []
        for file_path in sorted(base.rglob("*")):
            if file_path.is_file() and file_path.suffix.lower() in {".txt", ".md"}:
                indexed_docs.append(
                    {
                        "source": str(file_path),
                        "content": file_path.read_text(encoding="utf-8", errors="ignore"),
                    }
                )

        self.index_file.write_text(json.dumps(indexed_docs, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"message": "Knowledge ingestion complete", "documents_indexed": len(indexed_docs)}

    def search(self, query: str, limit: int = 5) -> list[dict[str, str | int]]:
        if not self.index_file.exists():
            return []

        docs = json.loads(self.index_file.read_text(encoding="utf-8"))
        terms = [item.lower() for item in query.split() if item.strip()]
        scored: list[dict[str, str | int]] = []
        for doc in docs:
            content = str(doc.get("content", ""))
            lc = content.lower()
            score = sum(lc.count(term) for term in terms)
            if score > 0:
                scored.append(
                    {
                        "source": str(doc.get("source", "")),
                        "score": score,
                        "snippet": content[:300],
                    }
                )

        scored.sort(key=lambda item: int(item["score"]), reverse=True)
        return scored[:limit]
