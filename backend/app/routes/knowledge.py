from fastapi import APIRouter, HTTPException

from app.schemas import KnowledgeIngestRequest, KnowledgeSearchRequest, KnowledgeSearchResult
from app.services.knowledge_base import KnowledgeBaseService

router = APIRouter(prefix="/knowledge", tags=["knowledge"])
knowledge_service = KnowledgeBaseService()


@router.post("/ingest")
def ingest_knowledge(payload: KnowledgeIngestRequest) -> dict[str, int | str]:
    try:
        return knowledge_service.ingest_collection(payload.collection)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/search", response_model=list[KnowledgeSearchResult])
def search_knowledge(payload: KnowledgeSearchRequest) -> list[KnowledgeSearchResult]:
    return [KnowledgeSearchResult(**item) for item in knowledge_service.search(payload.query, payload.limit)]
