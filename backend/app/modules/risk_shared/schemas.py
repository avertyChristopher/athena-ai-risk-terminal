from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

from app.modules.risk_shared.metadata import (
    ANALYTICS_PAYLOAD_VERSION,
    OPTIONS_SOURCE_MODULE,
    RATES_SOURCE_MODULE,
    RISK_PAYLOAD_VERSION,
    TRADE_SOURCE_MODULE,
    VOLATILITY_SOURCE_MODULE,
)


class CommonAnalyticsMetadata(BaseModel):
    payload_version: str = ANALYTICS_PAYLOAD_VERSION
    module_name: str
    portfolio_id: str | None = None
    symbol: str | None = None
    analysis_mode: str = "standalone"
    data_source: str
    metric_source: str
    methodology: str | dict[str, Any] | None = None
    assumptions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    fallback_used: bool = False
    missing_symbols: list[str] = Field(default_factory=list)
    coverage_ratio: float | None = None
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class SharedRiskDataSource(BaseModel):
    metric_source: str
    fallback_used: bool
    fallback_reason: str | None = None
    observations: int
    symbols_found: list[str]
    symbols_missing: list[str]
    warnings: list[str]
    badges: list[str]


class SharedRiskContributionItem(BaseModel):
    symbol: str
    weight: float
    contribution: float


class SharedRiskPayload(BaseModel):
    payload_version: str = RISK_PAYLOAD_VERSION
    source_module: str = VOLATILITY_SOURCE_MODULE
    module_name: str = VOLATILITY_SOURCE_MODULE
    portfolio_id: str | None = None
    symbol: str | None = None
    benchmark_symbol: str
    analysis_mode: Literal["asset", "portfolio"]
    annualized_volatility: float
    ewma_volatility: float | None
    historical_var: float
    historical_cvar: float
    parametric_var: float
    parametric_cvar: float
    monte_carlo_var: float | None = None
    monte_carlo_cvar: float | None = None
    beta: float
    correlation: float
    tracking_error: float | None
    sharpe_ratio: float | None
    sortino_ratio: float | None
    max_drawdown: float
    risk_contribution: list[SharedRiskContributionItem] = Field(default_factory=list)
    covariance_summary: dict[str, Any] | None = None
    correlation_summary: dict[str, Any] | None = None
    data_source: SharedRiskDataSource
    metric_source: str
    methodology: str | dict[str, Any] | None = None
    assumptions: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    missing_symbols: list[str]
    coverage_ratio: float | None = None
    fallback_used: bool
    warnings: list[str]
    generated_at: datetime


class RiskAnalyticsPayload(SharedRiskPayload):
    source_module: str = VOLATILITY_SOURCE_MODULE
    module_name: str = VOLATILITY_SOURCE_MODULE


class OptionsRiskPayload(BaseModel):
    payload_version: str = ANALYTICS_PAYLOAD_VERSION
    source_module: str = OPTIONS_SOURCE_MODULE
    module_name: str = OPTIONS_SOURCE_MODULE
    underlying_symbol: str
    strategy_name: str | None = None
    option_type: str | None = None
    position_side: str | None = None
    option_price: float | None = None
    intrinsic_value: float | None = None
    time_value: float | None = None
    moneyness: str | None = None
    delta: float | None = None
    gamma: float | None = None
    theta: float | None = None
    vega: float | None = None
    rho: float | None = None
    delta_adjusted_exposure: float | None = None
    max_profit: float | None = None
    max_loss: float | None = None
    breakeven_points: list[float] = Field(default_factory=list)
    implied_volatility: float | None = None
    methodology: str | dict[str, Any] | None = None
    warnings: list[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class RatesRiskPayload(BaseModel):
    payload_version: str = ANALYTICS_PAYLOAD_VERSION
    source_module: str = RATES_SOURCE_MODULE
    module_name: str = RATES_SOURCE_MODULE
    portfolio_id: str | None = None
    symbol: str | None = None
    clean_price: float | None = None
    dirty_price: float | None = None
    accrued_interest: float | None = None
    ytm: float | None = None
    macaulay_duration: float | None = None
    modified_duration: float | None = None
    convexity: float | None = None
    dv01: float | None = None
    pvbp: float | None = None
    curve_scenario_impact: float | None = None
    rate_shock_bps: float | None = None
    fixed_income_market_value: float | None = None
    fixed_income_allocation: float | None = None
    estimated_rate_shock_loss: float | None = None
    methodology: str | dict[str, Any] | None = None
    warnings: list[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class TradeImpactPayload(BaseModel):
    payload_version: str = ANALYTICS_PAYLOAD_VERSION
    source_module: str = TRADE_SOURCE_MODULE
    module_name: str = TRADE_SOURCE_MODULE
    portfolio_id: str
    action: str
    symbol: str
    estimated_trade_value: float
    before_weights: dict[str, float] = Field(default_factory=dict)
    after_weights: dict[str, float] = Field(default_factory=dict)
    before_risk: dict[str, float | None] = Field(default_factory=dict)
    after_risk: dict[str, float | None] = Field(default_factory=dict)
    constraints: list[dict[str, Any]] = Field(default_factory=list)
    suitability_status: str
    transaction_costs: dict[str, float] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ModuleIntegrationStatus(BaseModel):
    module: str
    status: str
    data_source: str
    payload_available: bool = False
    generated_at: datetime | None = None
    warnings: list[str] = Field(default_factory=list)
    required_data: list[str] = Field(default_factory=list)
