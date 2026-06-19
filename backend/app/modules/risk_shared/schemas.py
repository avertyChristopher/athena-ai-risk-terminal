from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

from app.modules.risk_shared.metadata import (
    RISK_PAYLOAD_VERSION,
    VOLATILITY_SOURCE_MODULE,
)


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
    missing_symbols: list[str]
    coverage_ratio: float | None = None
    fallback_used: bool
    warnings: list[str]
    generated_at: datetime
