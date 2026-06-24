from typing import Literal

from pydantic import BaseModel, Field

from app.modules.athena_intelligence.schemas import AthenaAICommentary
from app.modules.risk_shared.schemas import ModuleIntegrationStatus, TradeImpactPayload


TradeAction = Literal["BUY", "SELL"]
OrderType = Literal["Market", "Limit", "Stop"]
TimeInForce = Literal["Day", "GTC"]
TradeRationale = Literal[
    "Rebalancing",
    "Risk reduction",
    "Growth opportunity",
    "Income objective",
    "Hedging",
    "Liquidity need",
    "Valuation view",
    "Momentum view",
]


class TradeModuleStatus(BaseModel):
    status: str = "ready"
    module: str = "trade-simulator"
    detail: str
    simulation_ready: bool = True


class TradeSimulationRequest(BaseModel):
    portfolio_id: str
    action: TradeAction
    symbol: str = Field(min_length=1, max_length=32)
    asset_name: str | None = None
    asset_type: str = Field(default="equity", min_length=1, max_length=64)
    quantity: float = Field(gt=0)
    estimated_price: float = Field(gt=0)
    order_type: OrderType = "Market"
    limit_price: float | None = Field(default=None, gt=0)
    time_in_force: TimeInForce = "Day"
    trade_rationale: TradeRationale = "Rebalancing"


class ImpactMetric(BaseModel):
    name: str
    before: float | str | None
    after: float | str | None
    change: float | None = None
    limit: float | None = None
    status: str = "ok"


class TradeTicketSummary(BaseModel):
    portfolio_id: str
    action: TradeAction
    symbol: str
    asset_name: str
    asset_type: str
    quantity: float
    estimated_price: float
    order_type: OrderType
    limit_price: float | None
    time_in_force: TimeInForce
    trade_rationale: TradeRationale
    gross_trade_value: float
    estimated_commission: float
    estimated_fees: float
    estimated_spread_cost: float
    estimated_slippage: float
    estimated_market_impact: float
    estimated_total_implementation_cost: float
    cash_impact: float
    estimated_cash_after_trade: float
    demo_assumptions: list[str]


class PreTradeImpactResponse(BaseModel):
    metrics: list[ImpactMetric]
    interpretation: str


class RiskImpactResponse(BaseModel):
    metrics: list[ImpactMetric]
    message: str
    badges: list[str]
    metric_source: str = "deterministic_demo"
    fallback_used: bool = True
    fallback_reason: str | None = None
    observations: int = 0
    symbols_found: list[str] = Field(default_factory=list)
    symbols_missing: list[str] = Field(default_factory=list)
    quality_warnings: list[str] = Field(default_factory=list)


class SuitabilityReviewResponse(BaseModel):
    status: Literal["Suitable", "Requires Review", "Not Suitable"]
    commentary: str
    investor_type: str
    risk_tolerance: str
    time_horizon: str
    liquidity_needs: str
    factors: list[str]


class ConstraintWarning(BaseModel):
    name: str
    severity: Literal["low", "medium", "high"]
    actual: float
    limit: float
    status: str
    message: str


class TransactionCostAnalysisResponse(BaseModel):
    gross_trade_value: float
    explicit_costs: dict[str, float]
    implicit_costs: dict[str, float]
    total_estimated_cost: float
    cost_as_percent_of_trade_value: float
    estimated_net_trade_value: float
    implementation_shortfall_placeholder: float
    note: str
    badges: list[str]


class ExecutionQualityResponse(BaseModel):
    expected_execution_price: float
    simulated_execution_price: float
    price_improvement_or_shortfall: float
    implementation_shortfall: float
    order_type_impact: str
    liquidity_warning: str | None
    badge: str


class BenchmarkActiveRiskResponse(BaseModel):
    benchmark_name: str
    active_weight_before: float
    active_weight_after: float
    active_exposure_after_trade: float
    tracking_error_impact: float
    information_ratio_impact: float | None
    active_management_warning: str
    badge: str


class AthenaTradeCommentaryResponse(BaseModel):
    summary: str
    bullets: list[str]


class SimulationResultSummary(BaseModel):
    trade_status: Literal["Approved", "Requires Review", "Rejected"]
    main_reason: str
    key_warnings: list[str]
    estimated_cost: float
    risk_impact: str
    suitability_result: str
    notice: str


class TradeSimulationResponse(BaseModel):
    status: str = "simulated"
    module: str = "trade-simulator"
    trade_ticket: TradeTicketSummary
    pre_trade_impact: PreTradeImpactResponse
    risk_impact: RiskImpactResponse
    suitability_review: SuitabilityReviewResponse
    constraints_warnings: list[ConstraintWarning]
    transaction_cost_analysis: TransactionCostAnalysisResponse
    execution_quality: ExecutionQualityResponse
    benchmark_active_risk: BenchmarkActiveRiskResponse
    module_source_metadata: list[ModuleIntegrationStatus] = Field(default_factory=list)
    trade_impact_payload: TradeImpactPayload | None = None
    athena_commentary: AthenaTradeCommentaryResponse
    athena_ai_commentary: AthenaAICommentary | None = None
    simulation_result: SimulationResultSummary
