from fastapi import APIRouter, Depends

from app.api.dependencies import get_trade_simulator_service
from app.modules.trade_simulator.schemas import (
    TradeModuleStatus,
    TradeSimulationRequest,
    TradeSimulationResponse,
)
from app.modules.trade_simulator.service import TradeSimulatorService

router = APIRouter(prefix="/trade-simulator", tags=["trade-simulator"])


@router.get("/status", response_model=TradeModuleStatus)
def get_trade_simulator_status(
    service: TradeSimulatorService = Depends(get_trade_simulator_service),
) -> TradeModuleStatus:
    return service.get_module_status()


@router.post("/simulate", response_model=TradeSimulationResponse)
def simulate_trade(
    payload: TradeSimulationRequest,
    service: TradeSimulatorService = Depends(get_trade_simulator_service),
) -> TradeSimulationResponse:
    return service.simulate_trade(payload)
