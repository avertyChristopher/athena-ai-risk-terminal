from pydantic import BaseModel, Field


class PortfolioBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    base_currency: str = Field(min_length=3, max_length=3)
    benchmark: str = Field(default="SPY", min_length=1, max_length=32)
    cash: float = Field(default=0.0, ge=0)


class PortfolioCreate(PortfolioBase):
    pass


class PortfolioUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    base_currency: str | None = Field(default=None, min_length=3, max_length=3)
    benchmark: str | None = Field(default=None, min_length=1, max_length=32)
    cash: float | None = Field(default=None, ge=0)


class PortfolioRead(PortfolioBase):
    id: str


class PortfolioSummary(BaseModel):
    portfolio_id: str
    name: str
    base_currency: str
    benchmark: str
    total_market_value: float
    total_value: float
    invested_value: float
    cash: float
    cash_weight: float
    number_of_positions: int
    number_of_asset_classes: int
    number_of_sectors: int
    number_of_currencies: int
    largest_position: str | None
    largest_position_weight: float
    top_5_holdings_weight: float
    diversification_score: float
    data_source: str


class AllocationItem(BaseModel):
    name: str
    market_value: float
    weight: float
    weight_basis: str = "invested"


class AllocationResponse(BaseModel):
    portfolio_id: str
    allocation_type: str
    items: list[AllocationItem]


class ConcentrationResponse(BaseModel):
    portfolio_id: str
    largest_position_weight: float
    top_3_holdings_weight: float
    top_5_holdings_weight: float
    number_of_positions: int
    hhi_concentration: float
    effective_number_of_holdings: float
    diversification_score: float
    concentration_level: str
    warnings: list[str]


class PortfolioListResponse(BaseModel):
    status: str = "ready"
    module: str = "portfolios"
    detail: str
    items: list[PortfolioRead]


class DeleteResponse(BaseModel):
    status: str
    id: str


class PositionBase(BaseModel):
    symbol: str = Field(min_length=1, max_length=32)
    asset_name: str = Field(min_length=1, max_length=255)
    name: str | None = Field(default=None, min_length=1, max_length=255)
    asset_type: str = Field(min_length=1, max_length=64)
    quantity: float = Field(gt=0)
    average_price: float = Field(gt=0)
    current_price: float = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)
    sector: str = Field(min_length=1, max_length=80)
    country: str = Field(min_length=1, max_length=80)
    exchange: str | None = None
    industry: str | None = None
    region: str | None = None


class PositionCreate(PositionBase):
    pass


class PositionUpdate(BaseModel):
    symbol: str | None = Field(default=None, min_length=1, max_length=32)
    asset_name: str | None = Field(default=None, min_length=1, max_length=255)
    name: str | None = Field(default=None, min_length=1, max_length=255)
    asset_type: str | None = Field(default=None, min_length=1, max_length=64)
    quantity: float | None = Field(default=None, gt=0)
    average_price: float | None = Field(default=None, gt=0)
    current_price: float | None = Field(default=None, gt=0)
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    sector: str | None = Field(default=None, min_length=1, max_length=80)
    country: str | None = Field(default=None, min_length=1, max_length=80)
    exchange: str | None = None
    industry: str | None = None
    region: str | None = None


class PositionRead(PositionBase):
    id: str
    portfolio_id: str
    market_value: float
    weight: float
    portfolio_weight: float
    invested_weight: float
    cost_basis: float
    unrealized_pnl: float
    unrealized_pnl_percent: float


class PositionListResponse(BaseModel):
    portfolio_id: str
    items: list[PositionRead]


class DiversificationResponse(ConcentrationResponse):
    sector_concentration: dict[str, float]
    currency_concentration: dict[str, float]
    asset_type_concentration: dict[str, float]


class RiskReturnAssetContribution(BaseModel):
    symbol: str
    weight: float
    expected_return: float
    return_contribution: float
    risk_contribution_placeholder: float


class RiskReturnResponse(BaseModel):
    portfolio_id: str
    expected_return: float
    variance: float | None
    standard_deviation: float | None
    diversification_benefit: float | None
    risk_return_profile: str
    covariance_matrix_status: str
    correlation_matrix_status: str
    contributions: list[RiskReturnAssetContribution]
    notes: list[str]


class BenchmarkHolding(BaseModel):
    name: str
    portfolio_weight: float
    benchmark_weight: float
    active_weight: float


class BenchmarkResponse(BaseModel):
    portfolio_id: str
    benchmark_symbol: str
    total_active_weight: float
    active_return: float | None
    tracking_difference: float | None
    tracking_error: float | None
    holdings: list[BenchmarkHolding]
    notes: list[str]


class TargetAllocation(BaseModel):
    name: str
    target_weight: float = Field(ge=0, le=1)
    tolerance_band: float = Field(default=0.05, ge=0, le=1)


class PortfolioPolicy(BaseModel):
    investor_type: str = "Individual"
    investment_objective: str
    return_objective: str
    risk_objective: str = "Balance growth with moderate drawdown tolerance."
    risk_tolerance: str
    ability_to_take_risk: str = "Moderate"
    willingness_to_take_risk: str = "Moderate"
    risk_aversion_coefficient: float = Field(default=3.0, ge=0)
    time_horizon: str
    liability_profile: str = "No explicit liability schedule modeled."
    liquidity_needs: str
    tax_considerations: str
    legal_regulatory_constraints: str
    unique_circumstances: str
    permitted_asset_classes: list[str]
    prohibited_asset_classes: list[str]
    benchmark: str
    target_allocation: list[TargetAllocation]


class PolicyComparisonItem(BaseModel):
    name: str
    current_weight: float
    target_weight: float
    drift: float
    tolerance_band: float
    status: str


class PolicyResponse(BaseModel):
    portfolio_id: str
    policy: PortfolioPolicy
    comparison: list[PolicyComparisonItem]
    breaches: list[str]
    warnings: list[str]


class TargetAllocationResponse(BaseModel):
    portfolio_id: str
    items: list[PolicyComparisonItem]
    rebalance_needed: bool


class RebalancePreviewItem(BaseModel):
    name: str
    current_market_value: float
    target_market_value: float
    value_difference: float
    estimated_quantity_difference: float
    action: str


class RebalancingPreviewResponse(BaseModel):
    portfolio_id: str
    turnover_estimate: float
    items: list[RebalancePreviewItem]
    notes: list[str]


class PerformanceMeasurementResponse(BaseModel):
    portfolio_id: str
    beginning_value: float
    ending_value: float
    external_cash_flows: float
    holding_period_return: float
    time_weighted_return: float
    money_weighted_return: float | None
    return_contributions: list[RiskReturnAssetContribution]
    notes: list[str]


class PortfolioConstraints(BaseModel):
    max_single_position_weight: float = Field(default=0.25, ge=0, le=1)
    max_sector_weight: float = Field(default=0.50, ge=0, le=1)
    max_asset_type_weight: float = Field(default=0.80, ge=0, le=1)
    max_currency_weight: float = Field(default=1.0, ge=0, le=1)
    minimum_cash_weight: float = Field(default=0.02, ge=0, le=1)
    allowed_asset_types: list[str] = ["equity", "etf", "fixed_income", "cash"]
    benchmark_required: bool = False
    max_number_of_positions: int | None = None


class ConstraintBreach(BaseModel):
    constraint: str
    name: str
    actual: float
    limit: float
    severity: str


class ConstraintsResponse(BaseModel):
    portfolio_id: str
    constraints: PortfolioConstraints
    breaches: list[ConstraintBreach]


class PortfolioDiagnosticsResponse(BaseModel):
    portfolio_id: str
    allocation_quality: str
    diversification_quality: str
    concentration_risk: str
    cash_level: str
    benchmark_alignment: str
    policy_alignment: str
    rebalancing_need: str
    data_quality_limitations: list[str]
    next_analytical_steps: list[str]
    summary: str


class PortfolioMarketDataIntegrationResponse(BaseModel):
    portfolio_id: str
    symbols: list[str]
    return_series_endpoint: str | None
    aligned_returns_endpoint: str | None
    data_quality_endpoint: str | None
    current_status: str
    integration_message: str
    current_assumptions: list[str]
    planned_analytics: list[str]
    limitations: list[str]
    readiness_badges: list[str]


class ProcessStep(BaseModel):
    phase: str
    description: str


class InvestorProfileResponse(BaseModel):
    investor_type: str
    liability_profile: str
    liquidity_needs: str
    time_horizon: str
    return_objective: str
    risk_objective: str
    tax_considerations: str
    legal_regulatory_constraints: str
    unique_circumstances: str


class RiskToleranceResponse(BaseModel):
    ability_to_take_risk: str
    willingness_to_take_risk: str
    overall_risk_tolerance: str
    conflict_detected: bool
    summary: str


class UtilityResponse(BaseModel):
    expected_return: float
    variance: float
    risk_aversion_coefficient: float
    risk_aversion_classification: str
    utility_score: float


class CapmResponse(BaseModel):
    risk_free_rate: float
    expected_market_return: float
    market_risk_premium: float
    portfolio_beta: float
    capm_required_return: float
    expected_return_gap: float
    interpretation: str


class RiskAdjustedPerformanceResponse(BaseModel):
    portfolio_return: float
    benchmark_return: float
    risk_free_rate: float
    sharpe_ratio: float | None
    treynor_ratio: float | None
    jensen_alpha: float
    active_return: float
    tracking_error: float | None
    information_ratio: float | None
    notes: list[str]


class BehavioralBiasResponse(BaseModel):
    warnings: list[str]
    summary: str


class PooledVehicleExposureResponse(BaseModel):
    etf_exposure: float
    single_stock_exposure: float
    pooled_vehicle_exposure: float
    usage_classification: str


class EfficientFrontierResponse(BaseModel):
    points: list[dict[str, float | str]]
    status: str


class CfaConceptsResponse(BaseModel):
    portfolio_id: str
    portfolio_management_process: list[ProcessStep]
    investor_profile: InvestorProfileResponse
    risk_tolerance: RiskToleranceResponse
    utility: UtilityResponse
    capm: CapmResponse
    risk_adjusted_performance: RiskAdjustedPerformanceResponse
    behavioral_biases: BehavioralBiasResponse
    pooled_vehicle_exposure: PooledVehicleExposureResponse
    efficient_frontier: EfficientFrontierResponse
