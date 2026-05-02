from pydantic import BaseModel

from app.schemas.common_schema import ModuleStatus


class BlackScholesRequest(BaseModel):
    spot: float
    strike: float
    time_to_maturity: float
    risk_free_rate: float
    volatility: float


class PricingModuleStatus(ModuleStatus):
    supported_models: list[str] = []
