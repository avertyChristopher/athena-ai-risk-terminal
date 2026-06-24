from pydantic import BaseModel, Field

from app.modules.risk_shared.schemas import (
    ModuleIntegrationStatus,
    OptionsRiskPayload,
    RatesRiskPayload,
)


class RiskMonitorStatus(BaseModel):
    status: str = "ready"
    module: str = "risk-monitor"
    detail: str
    engines_available: list[str]


class RiskLimitOverrides(BaseModel):
    max_single_position_weight: float | None = Field(default=None, ge=0, le=1)
    max_sector_exposure: float | None = Field(default=None, ge=0, le=1)
    max_asset_type_exposure: float | None = Field(default=None, ge=0, le=1)
    minimum_cash_reserve: float | None = Field(default=None, ge=0, le=1)
    max_top_3_concentration: float | None = Field(default=None, ge=0, le=1)
    max_portfolio_volatility: float | None = Field(default=None, ge=0, le=1)
    max_var_95: float | None = Field(default=None, ge=0, le=1)
    max_cvar_95: float | None = Field(default=None, ge=0, le=1)
    max_drawdown: float | None = Field(default=None, ge=0, le=1)
    max_tracking_error: float | None = Field(default=None, ge=0, le=1)
    max_active_exposure: float | None = Field(default=None, ge=0, le=1)


class StressShockOverrides(BaseModel):
    equity_market_shock: float | None = Field(default=None, ge=-1, le=0)
    technology_sector_shock: float | None = Field(default=None, ge=-1, le=0)
    interest_rate_shock: float | None = Field(default=None, ge=-1, le=0)
    largest_holding_shock: float | None = Field(default=None, ge=-1, le=0)


class RiskMonitorAnalyzeRequest(BaseModel):
    portfolio_id: str = Field(min_length=1)
    benchmark_symbol: str = Field(default="SPY", min_length=1, max_length=32)
    confidence_level: float = Field(default=0.95, gt=0, lt=1)
    risk_free_rate: float = 0.02
    limits: RiskLimitOverrides | None = None
    stress_shocks: StressShockOverrides | None = None


class RiskSourceMetadata(BaseModel):
    metric_source: str
    fallback_used: bool
    fallback_reason: str | None
    observations: int
    symbols_found: list[str]
    symbols_missing: list[str]
    quality_warnings: list[str]
    badges: list[str]


class RiskMonitorAssumptions(BaseModel):
    limits: dict[str, float]
    stress_shocks: dict[str, float]


class RiskMetric(BaseModel):
    name: str
    value: float | None
    unit: str = "ratio"
    source: str
    status: str = "ok"
    description: str


class ConcentrationExposure(BaseModel):
    name: str
    weight: float
    limit: float | None = None
    status: str = "ok"


class ConcentrationAnalysis(BaseModel):
    largest_position: ConcentrationExposure | None
    top_3_weight: float
    top_5_weight: float
    sector_exposures: list[ConcentrationExposure]
    asset_type_exposures: list[ConcentrationExposure]
    cash_weight: float
    concentration_score: float
    warnings: list[str]


class RiskLimitBreach(BaseModel):
    rule_name: str
    category: str
    current_value: float
    limit_value: float
    severity: str
    explanation: str
    suggested_action: str


class StressScenarioResult(BaseModel):
    name: str
    estimated_impact_percent: float
    estimated_loss: float
    most_affected_holdings: list[str]
    severity: str
    explanation: str


class RiskContributionItem(BaseModel):
    name: str
    weight: float
    contribution: float
    contribution_percent: float
    source: str


class RiskContributionResponse(BaseModel):
    contribution_source: str
    method: str
    by_asset: list[RiskContributionItem]
    by_sector: list[RiskContributionItem]
    largest_risk_contributor: str | None
    diversification_warning: str | None


class BenchmarkRiskResponse(BaseModel):
    benchmark_symbol: str
    beta: float | None
    active_exposure: float
    tracking_error: float | None
    information_ratio: float | None
    active_risk_status: str
    warnings: list[str]
    badges: list[str]


class RiskAlert(BaseModel):
    title: str
    severity: str
    message: str
    suggested_action: str


class AthenaRiskCommentary(BaseModel):
    summary: str
    main_drivers: list[str]
    suggested_actions: list[str]


class RiskMonitorAnalysisResponse(BaseModel):
    portfolio_id: str
    portfolio_name: str
    benchmark_symbol: str
    total_value: float
    global_risk_score: int
    global_risk_status: str
    main_drivers: list[str]
    risk_metrics: list[RiskMetric]
    concentration: ConcentrationAnalysis
    limit_breaches: list[RiskLimitBreach]
    stress_tests: list[StressScenarioResult]
    risk_contribution: RiskContributionResponse
    benchmark_risk: BenchmarkRiskResponse
    alerts: list[RiskAlert]
    athena_commentary: AthenaRiskCommentary
    risk_source: RiskSourceMetadata
    assumptions: RiskMonitorAssumptions
    integration_statuses: list[ModuleIntegrationStatus] = Field(default_factory=list)
    rates_risk_payload: RatesRiskPayload | None = None
    options_risk_payload: OptionsRiskPayload | None = None
