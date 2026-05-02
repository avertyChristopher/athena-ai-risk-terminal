from pydantic import BaseModel

from app.schemas.common_schema import ModuleStatus


class BondPricingRequest(BaseModel):
    face_value: float
    coupon_rate: float
    years_to_maturity: float
    yield_to_maturity: float


class RatesModuleStatus(ModuleStatus):
    analytics_available: list[str] = []
