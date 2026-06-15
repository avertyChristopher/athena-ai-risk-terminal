export type TradeModuleStatus = {
  status: string;
  module: string;
  detail: string;
  simulation_ready: boolean;
};

export type TradeAction = "BUY" | "SELL";
export type OrderType = "Market" | "Limit" | "Stop";
export type TimeInForce = "Day" | "GTC";
export type TradeRationale =
  | "Rebalancing"
  | "Risk reduction"
  | "Growth opportunity"
  | "Income objective"
  | "Hedging"
  | "Liquidity need"
  | "Valuation view"
  | "Momentum view";

export type TradeSimulationRequest = {
  portfolio_id: string;
  action: TradeAction;
  symbol: string;
  asset_name?: string | null;
  asset_type: string;
  quantity: number;
  estimated_price: number;
  order_type: OrderType;
  limit_price?: number | null;
  time_in_force: TimeInForce;
  trade_rationale: TradeRationale;
};

export type ImpactMetric = {
  name: string;
  before: number | string | null;
  after: number | string | null;
  change: number | null;
  limit: number | null;
  status: string;
};

export type TradeTicketSummary = {
  portfolio_id: string;
  action: TradeAction;
  symbol: string;
  asset_name: string;
  asset_type: string;
  quantity: number;
  estimated_price: number;
  order_type: OrderType;
  limit_price: number | null;
  time_in_force: TimeInForce;
  trade_rationale: TradeRationale;
  gross_trade_value: number;
  estimated_commission: number;
  estimated_fees: number;
  estimated_spread_cost: number;
  estimated_slippage: number;
  estimated_market_impact: number;
  estimated_total_implementation_cost: number;
  cash_impact: number;
  estimated_cash_after_trade: number;
  demo_assumptions: string[];
};

export type PreTradeImpactResponse = {
  metrics: ImpactMetric[];
  interpretation: string;
};

export type RiskImpactResponse = {
  metrics: ImpactMetric[];
  message: string;
  badges: string[];
  metric_source: string;
  fallback_used: boolean;
  fallback_reason: string | null;
  observations: number;
  symbols_found: string[];
  symbols_missing: string[];
  quality_warnings: string[];
};

export type SuitabilityReviewResponse = {
  status: "Suitable" | "Requires Review" | "Not Suitable";
  commentary: string;
  investor_type: string;
  risk_tolerance: string;
  time_horizon: string;
  liquidity_needs: string;
  factors: string[];
};

export type ConstraintWarning = {
  name: string;
  severity: "low" | "medium" | "high";
  actual: number;
  limit: number;
  status: string;
  message: string;
};

export type TransactionCostAnalysisResponse = {
  gross_trade_value: number;
  explicit_costs: Record<string, number>;
  implicit_costs: Record<string, number>;
  total_estimated_cost: number;
  cost_as_percent_of_trade_value: number;
  estimated_net_trade_value: number;
  implementation_shortfall_placeholder: number;
  note: string;
  badges: string[];
};

export type ExecutionQualityResponse = {
  expected_execution_price: number;
  simulated_execution_price: number;
  price_improvement_or_shortfall: number;
  implementation_shortfall: number;
  order_type_impact: string;
  liquidity_warning: string | null;
  badge: string;
};

export type BenchmarkActiveRiskResponse = {
  benchmark_name: string;
  active_weight_before: number;
  active_weight_after: number;
  active_exposure_after_trade: number;
  tracking_error_impact: number;
  information_ratio_impact: number | null;
  active_management_warning: string;
  badge: string;
};

export type AthenaTradeCommentaryResponse = {
  summary: string;
  bullets: string[];
};

export type SimulationResultSummary = {
  trade_status: "Approved" | "Requires Review" | "Rejected";
  main_reason: string;
  key_warnings: string[];
  estimated_cost: number;
  risk_impact: string;
  suitability_result: string;
  notice: string;
};

export type TradeSimulationResponse = {
  status: string;
  module: string;
  trade_ticket: TradeTicketSummary;
  pre_trade_impact: PreTradeImpactResponse;
  risk_impact: RiskImpactResponse;
  suitability_review: SuitabilityReviewResponse;
  constraints_warnings: ConstraintWarning[];
  transaction_cost_analysis: TransactionCostAnalysisResponse;
  execution_quality: ExecutionQualityResponse;
  benchmark_active_risk: BenchmarkActiveRiskResponse;
  athena_commentary: AthenaTradeCommentaryResponse;
  simulation_result: SimulationResultSummary;
};
