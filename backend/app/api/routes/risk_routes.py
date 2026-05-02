from fastapi import APIRouter, Depends

from app.api.dependencies import get_risk_service
from app.schemas.risk_schema import RiskModuleStatus
from app.services.risk_service import RiskService

router = APIRouter(prefix="/risk", tags=["risk"])


@router.get("/status", response_model=RiskModuleStatus)
def get_risk_status(
    service: RiskService = Depends(get_risk_service),
) -> RiskModuleStatus:
    return service.get_module_status()
