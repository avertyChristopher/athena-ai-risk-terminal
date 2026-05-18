from pydantic import BaseModel

from app.schemas.common_schema import ModuleStatus


class MarketDataModuleStatus(ModuleStatus):
    assets_tracked: int = 0


class MarketAsset(BaseModel):
    symbol: str
    name: str
    asset_type: str
    currency: str
    sector: str
    country: str


class PricePoint(BaseModel):
    date: str
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: int


class ReturnPoint(BaseModel):
    date: str
    symbol: str
    simple_return: float
    log_return: float
    cumulative_return: float
    drawdown: float


class VolatilityResponse(BaseModel):
    symbol: str
    daily_volatility: float
    annualized_volatility: float


class DataQualityResponse(BaseModel):
    symbol: str
    rows: int
    missing_price_dates: list[str]
    duplicate_dates: list[str]
    outlier_indexes: list[int]
    is_valid: bool
