from fastapi import APIRouter, Depends

from app.api.dependencies import get_trade_service
from app.modules.trade_simulator.schemas import TradeModuleStatus
from app.modules.trade_simulator.service import TradeSimulatorService

router = APIRouter(prefix="/trades", tags=["trades"])


@router.get("/status", response_model=TradeModuleStatus)
def get_trade_status(
    service: TradeSimulatorService = Depends(get_trade_service),
) -> TradeModuleStatus:
    return service.get_module_status()
