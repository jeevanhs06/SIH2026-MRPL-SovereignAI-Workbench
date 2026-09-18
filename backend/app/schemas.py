from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    service: str


class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    extension: str
    size_bytes: int
    checksum_sha256: str
    stored_path: str


class TaskStatus(str, Enum):
    created = "created"
    queued = "queued"
    running = "running"
    waiting_for_review = "waiting_for_review"
    completed = "completed"
    failed = "failed"
    rejected = "rejected"


class TaskCreateRequest(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    prompt: str = Field(min_length=3, max_length=2000)
    document_ids: list[str] = Field(default_factory=list)
    requires_review: bool = True


class TaskEvent(BaseModel):
    timestamp: datetime
    event: str
    details: dict[str, str] = Field(default_factory=dict)


class TaskResponse(BaseModel):
    task_id: str
    title: str
    prompt: str
    status: TaskStatus
    document_ids: list[str]
    requires_review: bool
    output_files: list[str]
    created_at: datetime
    updated_at: datetime
    events: list[TaskEvent]


class TaskReviewRequest(BaseModel):
    approved: bool
    notes: str = Field(default="", max_length=2000)


class KnowledgeIngestRequest(BaseModel):
    collection: Literal["manuals", "sops", "templates", "sample_documents"]


class KnowledgeSearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=1000)
    limit: int = Field(default=5, ge=1, le=20)


class KnowledgeSearchResult(BaseModel):
    source: str
    score: int
    snippet: str


class SecurityStatusResponse(BaseModel):
    offline_mode: bool
    model_endpoint: str
    model_endpoint_local: bool
    model_endpoint_reachable: bool
    note: str


class AuthStatusResponse(BaseModel):
    enabled: bool
    mode: str
