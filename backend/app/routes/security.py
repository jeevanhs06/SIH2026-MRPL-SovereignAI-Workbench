from fastapi import APIRouter

from app.schemas import SecurityStatusResponse
from app.services.network_status import NetworkStatusService

router = APIRouter(prefix="/security", tags=["security"])
network_service = NetworkStatusService()


@router.get("/network-status", response_model=SecurityStatusResponse)
def network_status() -> SecurityStatusResponse:
    return SecurityStatusResponse(**network_service.get_status())
