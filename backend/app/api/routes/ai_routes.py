from fastapi import APIRouter, Depends

from app.api.dependencies import get_ai_service
from app.schemas.common_schema import ModuleStatus
from app.services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["ai"])


@router.get("/status", response_model=ModuleStatus)
def get_ai_status(
    service: AIService = Depends(get_ai_service),
) -> ModuleStatus:
    return service.get_module_status()
