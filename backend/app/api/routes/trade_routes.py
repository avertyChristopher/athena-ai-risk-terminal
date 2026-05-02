from fastapi import APIRouter, Depends

from app.api.dependencies import get_trade_service
from app.schemas.trade_schema import TradeModuleStatus
from app.services.trade_service import TradeService

router = APIRouter(prefix="/trades", tags=["trades"])


@router.get("/status", response_model=TradeModuleStatus)
def get_trade_status(
    service: TradeService = Depends(get_trade_service),
) -> TradeModuleStatus:
    return service.get_module_status()
