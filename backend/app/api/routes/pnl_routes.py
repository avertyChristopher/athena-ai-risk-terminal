from fastapi import APIRouter, Depends

from app.api.dependencies import get_pnl_service
from app.schemas.pnl_schema import PnlModuleStatus
from app.services.pnl_service import PnlService

router = APIRouter(prefix="/pnl", tags=["pnl"])


@router.get("/status", response_model=PnlModuleStatus)
def get_pnl_status(
    service: PnlService = Depends(get_pnl_service),
) -> PnlModuleStatus:
    return service.get_module_status()
