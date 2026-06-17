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
    exchange: str | None = None
    industry: str | None = None
    benchmark_eligible: bool = True
    is_etf: bool = False
    is_index: bool = False
    is_fx_pair: bool = False
    is_commodity: bool = False
    data_source: str = "demo"
    primary_benchmark: str = "SPY"


class PricePoint(BaseModel):
    date: str
    symbol: str
    open: float
    high: float
    low: float
    close: float
    adjusted_close: float | None = None
    split_factor: float = 1.0
    dividend_amount: float = 0.0
    corporate_action_flag: bool = False
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


class LatestPrice(BaseModel):
    symbol: str
    date: str
    close: float
    adjusted_close: float
    currency: str
    data_source: str
    stale: bool


class LatestPricesResponse(BaseModel):
    symbols: list[str]
    items: list[LatestPrice]
    missing_symbols: list[str]


class PricePanelResponse(BaseModel):
    symbols: list[str]
    start_date: str | None
    end_date: str | None
    rows: list[dict[str, float | str]]
    missing_symbols: list[str]
    warnings: list[str]


class ReturnsPanelResponse(BaseModel):
    symbols: list[str]
    return_type: str
    rows: list[dict[str, float | str]]
    missing_symbols: list[str]
    warnings: list[str]


class AssetMetadata(MarketAsset):
    latest_price_available: bool
    latest_price_date: str | None


class AssetValidationResponse(BaseModel):
    symbol: str
    exists: bool
    metadata: AssetMetadata | None
    warnings: list[str]


class MarketDataQualityReport(BaseModel):
    symbol: str
    rows: int
    missing_price_dates: list[str]
    duplicate_dates: list[str]
    outlier_indexes: list[int]
    is_valid: bool
    latest_price_date: str | None
    stale_latest_price: bool
    currency: str | None
    currency_mismatch: bool
    warnings: list[str]


class PortfolioMarketDataQualityReport(BaseModel):
    symbols: list[str]
    expected_currency: str
    reports: list[MarketDataQualityReport]
    missing_symbols: list[str]
    stale_symbols: list[str]
    currency_mismatch_symbols: list[str]
    quality_score: float
    is_valid_for_portfolio: bool
    warnings: list[str]


class PortfolioMarketDataCoverageResponse(BaseModel):
    symbols: list[str]
    covered_symbols: list[str]
    missing_symbols: list[str]
    coverage_ratio: float
    latest_price_dates: dict[str, str | None]
    warnings: list[str]


class MarketDataImportRow(BaseModel):
    date: str
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    name: str | None = None
    asset_type: str = "equity"
    currency: str = "USD"
    sector: str = "Imported"
    country: str = "United States"
    exchange: str | None = None
    industry: str | None = None


class MarketDataImportRequest(BaseModel):
    rows: list[MarketDataImportRow]


class MarketDataImportResponse(BaseModel):
    imported_rows: int
    imported_symbols: list[str]
    warnings: list[str]


class BenchmarkReturnsResponse(BaseModel):
    benchmark_symbol: str
    return_type: str
    returns: list[ReturnPoint]


class FXRateResponse(BaseModel):
    base: str
    quote: str
    date: str
    rate: float
    data_source: str


class RiskFreeRateResponse(BaseModel):
    currency: str
    tenor: str
    rate: float
    data_source: str


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
