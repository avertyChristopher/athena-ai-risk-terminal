from fastapi import APIRouter

from app.core.config import settings
from app.schemas.common_schema import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
def get_health() -> HealthResponse:
    return HealthResponse(status="ok", service=settings.service_name)
