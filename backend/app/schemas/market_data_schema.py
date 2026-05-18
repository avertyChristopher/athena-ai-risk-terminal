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


class MarketDataAnalyticsResponse(BaseModel):
    symbol: str
    benchmark_symbol: str
    latest_price: float
    latest_return: float
    holding_period_return: float
    cumulative_return: float
    arithmetic_mean_return: float
    geometric_mean_return: float
    annualized_return: float
    variance: float
    standard_deviation: float
    daily_volatility: float
    annualized_volatility: float
    max_drawdown: float
    skewness: float
    kurtosis: float
    percentiles: dict[str, float]
    outlier_indexes: list[int]
    benchmark_latest_return: float
    active_return_vs_benchmark: float
    correlation_with_benchmark: float
    covariance_with_benchmark: float
    beta_vs_benchmark: float
    sharpe_ratio: float
    moving_average_5: float | None
    moving_average_20: float | None
    momentum_5_day: float | None
    risk_free_rate_proxy: float
    adjusted_close_latest: float
    corporate_action_status: str
    average_volume_20: float
    latest_dollar_volume: float
    liquidity_score: float
    normal_distribution_coverage: float
    fx_rate_to_usd: float
    currency_consistency_status: str
    yield_curve_2y: float
    yield_curve_10y: float
    commodity_proxy_symbol: str
    commodity_proxy_latest_price: float
