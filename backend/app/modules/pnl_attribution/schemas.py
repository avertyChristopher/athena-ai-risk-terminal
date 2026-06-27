from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


AttributionMethod = Literal["simple", "Brinson-lite", "contribution"]
PnlLanguage = Literal["en", "fr"]
PnlStatusValue = Literal["generated", "generated_with_warnings"]


class PnlAttributionStatus(BaseModel):
    status: str = "ready"
    module: str = "pnl-attribution"
    detail: str
    attribution_ready: bool = True
    history_enabled: bool = True
    export_formats: list[str] = Field(default_factory=lambda: ["json", "csv"])
    source_modules: list[str]
    demo_mode: bool = True


class PnlAttributionRequest(BaseModel):
    portfolio_id: str = Field(default="pf_001", min_length=1)
    start_date: date = date(2026, 5, 13)
    end_date: date = date(2026, 6, 3)
    benchmark_symbol: str = Field(default="SPY", min_length=1, max_length=32)
    attribution_method: AttributionMethod = "contribution"
    include_income: bool = True
    include_fx: bool = True
    include_trades: bool = True
    include_rates: bool = True
    include_options: bool = True
    language: PnlLanguage = "en"

    @model_validator(mode="after")
    def validate_period(self) -> "PnlAttributionRequest":
        if self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date.")
        return self


class PnlPeriod(BaseModel):
    start_date: date
    end_date: date
    days: int


class PositionPnlContribution(BaseModel):
    symbol: str
    name: str
    asset_type: str
    asset_class: str
    sector: str
    currency: str
    starting_price: float
    ending_price: float
    quantity: float
    starting_value: float
    ending_value: float
    price_pnl: float
    income_pnl: float
    realized_pnl: float
    unrealized_pnl: float
    fees_and_costs: float
    fx_pnl: float
    total_pnl: float
    total_pnl_percent: float
    contribution_to_total_pnl: float
    contribution_to_portfolio_return: float
    data_source: str
    warnings: list[str] = Field(default_factory=list)


class GroupPnlContribution(BaseModel):
    name: str
    starting_value: float
    ending_value: float
    total_pnl: float
    pnl_percent: float
    contribution_to_total_pnl: float
    contribution_to_portfolio_return: float
    weight_start: float
    weight_end: float


class BenchmarkComparison(BaseModel):
    benchmark_symbol: str
    portfolio_return: float
    benchmark_return: float | None
    active_return: float | None
    relative_performance: str
    allocation_effect: float | None = None
    selection_effect: float | None = None
    interaction_effect: float | None = None
    tracking_note: str


class TradeEffect(BaseModel):
    status: str
    total_trade_costs: float
    estimated_slippage: float
    turnover: float
    trade_impact_on_cash: float
    trades: list[dict[str, Any]] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class FixedIncomeEffect(BaseModel):
    symbol: str
    duration_effect: float
    convexity_effect: float
    income_effect: float
    rate_shock_bps: float
    estimated_rate_pnl: float
    residual_pnl: float
    duration_source: str
    limitations: list[str] = Field(default_factory=list)


class OptionsEffect(BaseModel):
    status: str
    delta_contribution: float
    gamma_contribution: float
    vega_contribution: float
    theta_contribution: float
    rho_contribution: float
    residual_pnl: float
    notes: list[str] = Field(default_factory=list)


class FxEffect(BaseModel):
    currency: str
    base_currency: str
    local_currency_pnl: float
    fx_translation_pnl: float
    fx_data_source: str


class PnlMethodology(BaseModel):
    attribution_method: AttributionMethod
    assumptions: list[str]
    data_sources: list[str]
    limitations: list[str]


class PnlAttributionResult(BaseModel):
    analysis_id: str
    portfolio_id: str
    portfolio_name: str
    period: PnlPeriod
    starting_value: float
    ending_value: float
    total_pnl: float
    total_pnl_percent: float
    realized_pnl: float
    unrealized_pnl: float
    income_pnl: float
    fees_and_costs: float
    fx_pnl: float
    price_pnl: float
    position_contributions: list[PositionPnlContribution]
    asset_class_contributions: list[GroupPnlContribution]
    sector_contributions: list[GroupPnlContribution]
    currency_contributions: list[GroupPnlContribution]
    trade_effects: TradeEffect
    fixed_income_effects: list[FixedIncomeEffect]
    options_effects: OptionsEffect
    fx_effects: list[FxEffect] = Field(default_factory=list)
    benchmark_comparison: BenchmarkComparison
    top_winners: list[PositionPnlContribution]
    top_losers: list[PositionPnlContribution]
    warnings: list[str] = Field(default_factory=list)
    methodology: PnlMethodology
    limitations: list[str] = Field(default_factory=list)
    athena_ai_commentary: dict[str, Any] | None = None
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    status: PnlStatusValue = "generated"


class PnlHistoryItem(BaseModel):
    analysis_id: str
    portfolio_id: str
    portfolio_name: str
    start_date: date
    end_date: date
    total_pnl: float
    total_pnl_percent: float
    generated_at: datetime
    status: PnlStatusValue
    warnings_count: int


class PnlHistoryResponse(BaseModel):
    status: str = "ready"
    module: str = "pnl-attribution"
    total_analyses: int
    items: list[PnlHistoryItem]


class PnlDeleteResponse(BaseModel):
    deleted: bool
    analysis_id: str


class PnlCsvExportResponse(BaseModel):
    analysis_id: str
    content_type: str = "text/csv"
    csv: str
    included_tables: list[str]
