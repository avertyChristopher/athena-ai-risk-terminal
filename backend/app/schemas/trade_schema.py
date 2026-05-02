from pydantic import BaseModel

from app.schemas.common_schema import ModuleStatus


class TradeSimulationRequest(BaseModel):
    portfolio_id: int
    symbol: str
    side: str
    quantity: float


class TradeModuleStatus(ModuleStatus):
    simulation_ready: bool = False
