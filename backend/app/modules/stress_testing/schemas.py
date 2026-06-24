from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field, model_validator


class StressTestingStatus(BaseModel):
    status: str = "ready"
    module: str = "stress-testing"
    detail: str
    engines_available: list[str]


class CustomStressScenario(BaseModel):
    name: str = Field(default="Custom Scenario", min_length=1, max_length=120)
    description: str = "User-defined multi-asset stress scenario."
    equity_shock: float = Field(default=0.0, ge=-1.0, le=1.0)
    asset_class_shocks: dict[str, float] = Field(default_factory=dict)
    sector_shocks: dict[str, float] = Field(default_factory=dict)
    symbol_shocks: dict[str, float] = Field(default_factory=dict)
    rate_shock_bps: float = Field(default=0.0, ge=-5000.0, le=5000.0)
    volatility_shock: float = Field(default=0.0, ge=-0.95, le=5.0)
    fx_shock: float = Field(default=0.0, ge=-1.0, le=1.0)
    credit_spread_shock_bps: float = Field(default=0.0, ge=-500.0, le=5000.0)
    liquidity_multiplier: float = Field(default=1.0, ge=1.0, le=5.0)

    @model_validator(mode="after")
    def validate_shock_maps(self) -> "CustomStressScenario":
        for map_name in ("asset_class_shocks", "sector_shocks", "symbol_shocks"):
            shock_map = getattr(self, map_name)
            if len(shock_map) > 50:
                raise ValueError(f"{map_name} cannot contain more than 50 shocks.")
            for value in shock_map.values():
                if value < -1.0 or value > 1.0:
                    raise ValueError(f"{map_name} shock values must be between -100% and +100%.")
        return self


class StressTestingRunRequest(BaseModel):
    portfolio_id: str = Field(min_length=1)
    scenario_id: str | None = Field(default="risk_off_combined", min_length=1)
    custom_scenario: CustomStressScenario | None = None
    benchmark_symbol: str = Field(default="SPY", min_length=1, max_length=32)
    confidence_level: float = Field(default=0.95, gt=0.0, lt=1.0)
    include_position_impacts: bool = True
    include_risk_metrics: bool = True
    include_module_links: bool = True


class ShockAssumptions(BaseModel):
    asset_class_shocks: dict[str, float]
    sector_shocks: dict[str, float]
    symbol_shocks: dict[str, float]
    rate_shock_bps: float
    volatility_shock: float
    fx_shock: float
    credit_spread_shock_bps: float
    liquidity_multiplier: float


class StressScenarioDefinition(BaseModel):
    id: str
    name: str
    description: str
    shocks: ShockAssumptions


class ScenarioLibraryResponse(BaseModel):
    status: str = "ready"
    module: str = "stress-testing"
    scenarios: list[StressScenarioDefinition]


class SelectedPortfolio(BaseModel):
    portfolio_id: str
    name: str
    base_currency: str
    benchmark_symbol: str
    positions: int
    cash: float


class PositionStressImpact(BaseModel):
    position_id: str
    symbol: str
    name: str
    asset_class: str
    sector: str
    currency: str
    base_value: float
    shock_applied: float
    shock_source: str
    stressed_value: float
    dollar_impact: float
    percent_impact: float
    contribution_to_loss: float
    duration: float | None
    dv01: float | None
    rate_impact: float
    credit_impact: float
    fx_impact: float
    liquidity_impact: float
    data_source: str
    warnings: list[str]


class GroupStressImpact(BaseModel):
    name: str
    base_value: float
    stressed_value: float
    dollar_impact: float
    percent_impact: float
    loss_contribution: float


class WorstContributor(BaseModel):
    name: str
    label: str
    dollar_loss: float
    percent_impact: float
    contribution_to_loss: float


class RiskMetricComparison(BaseModel):
    metric: str
    before: float | None
    after: float | None
    unit: str
    source: str


class FixedIncomeStressSummary(BaseModel):
    fixed_income_exposure: float
    fixed_income_weight: float
    weighted_average_duration: float | None
    estimated_dv01: float | None
    rate_shock_bps: float
    credit_spread_shock_bps: float
    rate_risk_impact: float
    data_source: str
    warnings: list[str]


class OptionsRiskIntegration(BaseModel):
    status: str
    options_pricing_lab_ready: bool
    option_positions_detected: bool
    delta_adjusted_exposure: float | None = None
    gamma_effect: float | None = None
    vega_effect: float | None = None
    theta_decay: float | None = None
    warnings: list[str]


class IntegrationStatus(BaseModel):
    module: str
    status: str
    data_source: str
    warnings: list[str]


class StressLimitBreach(BaseModel):
    rule_name: str
    category: str
    current_value: float
    limit_value: float
    severity: str
    explanation: str
    suggested_action: str


class StressSeverityAssessment(BaseModel):
    severity: str
    score: int
    main_drivers: list[str]


class StressMethodology(BaseModel):
    method: str
    assumptions: list[str]
    limitations: list[str]
    data_sources: list[str]
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class AthenaStressCommentary(BaseModel):
    summary: str
    key_points: list[str]
    suggested_actions: list[str]
    not_investment_advice: bool


class RiskMonitorStressPayload(BaseModel):
    portfolio_id: str
    scenario_id: str
    stressed_value: float
    percent_loss: float
    worst_contributors: list[WorstContributor]
    stressed_var: float | None
    stressed_cvar: float | None
    stressed_volatility: float | None
    breached_limits: list[StressLimitBreach]
    severity: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class StressTestingResponse(BaseModel):
    selected_portfolio: SelectedPortfolio
    selected_scenario: StressScenarioDefinition
    base_portfolio_value: float
    stressed_portfolio_value: float
    dollar_loss: float
    percent_loss: float
    severity: StressSeverityAssessment
    position_impacts: list[PositionStressImpact]
    asset_class_impacts: list[GroupStressImpact]
    sector_impacts: list[GroupStressImpact]
    currency_impacts: list[GroupStressImpact]
    worst_contributors: list[WorstContributor]
    risk_metrics: list[RiskMetricComparison]
    fixed_income_stress: FixedIncomeStressSummary
    options_risk: OptionsRiskIntegration
    integrations: list[IntegrationStatus]
    limit_breaches: list[StressLimitBreach]
    warnings: list[str]
    methodology: StressMethodology
    risk_monitor_payload: RiskMonitorStressPayload
    athena_commentary: AthenaStressCommentary
    module_links: dict[str, str] = Field(default_factory=dict)


class ErrorDetail(BaseModel):
    detail: str
