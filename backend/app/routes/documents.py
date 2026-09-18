from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas import DocumentUploadResponse
from app.services.audit import AuditLogger
from app.services.ingestion import IngestionService
from app.services.storage import StorageService, StorageValidationError

router = APIRouter(prefix="/documents", tags=["documents"])
storage_service = StorageService()
ingestion_service = IngestionService()
audit = AuditLogger()


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)) -> DocumentUploadResponse:
    try:
        metadata = await storage_service.save_upload(file)
    except StorageValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    ingestion = ingestion_service.ingest_document(str(metadata["stored_path"]))
    audit.log_event(
        "document_uploaded",
        {
            "document_id": metadata["document_id"],
            "filename": metadata["filename"],
            "size_bytes": metadata["size_bytes"],
            "extractor": ingestion.get("extractor", "unknown"),
        },
    )
    return DocumentUploadResponse(**metadata)
