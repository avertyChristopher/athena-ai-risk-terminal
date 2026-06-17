from pydantic import BaseModel, Field


class VolatilityLabStatus(BaseModel):
    status: str = "ready"
    module: str = "volatility-lab"
    detail: str
    engines_available: list[str]


class VolatilityAssetAnalysisRequest(BaseModel):
    symbol: str = Field(min_length=1, max_length=32)
    benchmark_symbol: str = Field(default="SPY", min_length=1, max_length=32)
    start_date: str | None = None
    end_date: str | None = None
    risk_free_rate: float = 0.02
    rolling_window: int = Field(default=20, ge=2, le=252)
    annualization_factor: int = Field(default=252, ge=1)
    confidence_level: float = Field(default=0.95, gt=0, lt=1)


class VolatilityPortfolioAnalysisRequest(BaseModel):
    portfolio_id: str = Field(min_length=1)
    benchmark_symbol: str = Field(default="SPY", min_length=1, max_length=32)
    start_date: str | None = None
    end_date: str | None = None
    risk_free_rate: float = 0.02
    rolling_window: int = Field(default=20, ge=2, le=252)
    annualization_factor: int = Field(default=252, ge=1)
    confidence_level: float = Field(default=0.95, gt=0, lt=1)


class ReturnSummary(BaseModel):
    observations: int
    arithmetic_mean_return: float
    geometric_mean_return: float
    holding_period_return: float
    cumulative_return: float
    annualized_return: float
    excess_return: float
    active_return: float | None = None


class VolatilitySummary(BaseModel):
    variance: float
    standard_deviation: float
    daily_volatility: float
    annualized_volatility: float
    realized_volatility: float
    coefficient_of_variation: float | None
    rolling_latest: float | None
    rolling_minimum: float | None
    rolling_maximum: float | None
    rolling_average: float | None


class RollingVolatilityPoint(BaseModel):
    date: str
    volatility: float


class DownsideRiskSummary(BaseModel):
    downside_deviation: float
    semi_variance: float
    semi_deviation: float
    worst_return: float
    best_return: float
    max_drawdown: float
    probability_negative_return: float
    historical_var: float
    historical_cvar: float


class BenchmarkRiskSummary(BaseModel):
    benchmark_symbol: str
    covariance: float
    correlation: float
    beta: float
    capm_required_return: float
    jensen_alpha: float
    systematic_risk_note: str
    diversification_note: str


class DistributionSummary(BaseModel):
    mean: float
    median: float
    minimum: float
    maximum: float
    skewness: float
    kurtosis: float
    percentiles: dict[str, float]
    histogram: list[dict[str, float | int]]
    normality_note: str


class RiskAdjustedSummary(BaseModel):
    sharpe_ratio: float | None
    treynor_ratio: float | None
    sortino_ratio: float | None
    tracking_error: float | None
    information_ratio: float | None


class VolatilityRegimeSummary(BaseModel):
    regime: str
    latest_volatility: float | None
    reference_percentile: float | None
    explanation: str


class VolatilityDataSource(BaseModel):
    metric_source: str
    fallback_used: bool
    fallback_reason: str | None
    observations: int
    symbols_found: list[str]
    symbols_missing: list[str]
    warnings: list[str]
    badges: list[str]


class MatrixSummary(BaseModel):
    symbols: list[str]
    matrix: list[list[float]]
    interpretation: str


class RiskContributionItem(BaseModel):
    symbol: str
    weight: float
    contribution: float


class PortfolioRiskSummary(BaseModel):
    portfolio_volatility: float
    covariance_based_volatility: float
    weighted_average_asset_volatility: float
    diversification_benefit: float
    largest_risk_contributor: str | None
    beta: float
    tracking_error: float | None


class AthenaVolatilityCommentary(BaseModel):
    summary: str
    key_points: list[str]
    trade_simulator_reuse_note: str
    cfa_notes: list[str]


class VolatilityAssetAnalysisResponse(BaseModel):
    symbol: str
    benchmark_symbol: str
    latest_price: float | None
    return_summary: ReturnSummary
    volatility_summary: VolatilitySummary
    rolling_volatility: list[RollingVolatilityPoint]
    downside_risk: DownsideRiskSummary
    benchmark_risk: BenchmarkRiskSummary
    distribution: DistributionSummary
    risk_adjusted: RiskAdjustedSummary
    volatility_regime: VolatilityRegimeSummary
    data_source: VolatilityDataSource
    athena_commentary: AthenaVolatilityCommentary


class VolatilityPortfolioAnalysisResponse(BaseModel):
    portfolio_id: str
    portfolio_name: str
    benchmark_symbol: str
    holdings_included: list[str]
    holdings_missing: list[str]
    return_summary: ReturnSummary
    volatility_summary: VolatilitySummary
    downside_risk: DownsideRiskSummary
    portfolio_risk: PortfolioRiskSummary
    covariance_matrix: MatrixSummary
    correlation_matrix: MatrixSummary
    risk_contribution: list[RiskContributionItem]
    distribution: DistributionSummary
    risk_adjusted: RiskAdjustedSummary
    volatility_regime: VolatilityRegimeSummary
    data_source: VolatilityDataSource
    athena_commentary: AthenaVolatilityCommentary
