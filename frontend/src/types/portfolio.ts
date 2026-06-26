export type PortfolioSummary = {
  portfolio_id: string;
  name: string;
  base_currency: string;
  benchmark: string;
  total_market_value: number;
  total_value: number;
  invested_value: number;
  cash: number;
  cash_weight: number;
  number_of_positions: number;
  number_of_asset_classes: number;
  number_of_sectors: number;
  number_of_currencies: number;
  largest_position: string | null;
  largest_position_weight: number;
  top_5_holdings_weight: number;
  diversification_score: number;
  data_source: string;
};

export type PortfolioRead = {
  id: string;
  name: string;
  base_currency: string;
  benchmark: string;
  cash: number;
  strategy_type?: string | null;
  investment_objective?: string | null;
  risk_tolerance?: string | null;
  time_horizon?: string | null;
  target_allocation?: {
    name: string;
    target_weight: number;
    tolerance_band?: number;
  }[];
  strategy_description?: string | null;
  ips_summary?: string | null;
  data_source?: string | null;
  risk_profile?: string | null;
  demo_profile?: boolean;
  data_source_badges?: string[];
  market_data_coverage?: string | null;
  fixed_income_assumptions?: string | null;
  transaction_history?: Record<string, unknown>[];
  commentary_focus?: string[];
};

export type PortfolioCreate = {
  name: string;
  base_currency: string;
  benchmark: string;
  cash: number;
};

export type PortfolioListResponse = {
  status: string;
  module: string;
  detail: string;
  items: PortfolioRead[];
};

export type PositionRead = {
  id: string;
  portfolio_id: string;
  symbol: string;
  asset_name: string;
  name: string | null;
  asset_type: string;
  quantity: number;
  average_price: number;
  current_price: number;
  market_value: number;
  weight: number;
  portfolio_weight: number;
  invested_weight: number;
  currency: string;
  sector: string;
  country: string;
  exchange?: string | null;
  industry?: string | null;
  region?: string | null;
  asset_class?: string | null;
  risk_bucket?: string | null;
  liquidity_profile?: string | null;
  beta_assumption?: number | null;
  volatility_assumption?: number | null;
  duration_assumption?: number | null;
  modified_duration_assumption?: number | null;
  dv01_assumption?: number | null;
  dividend_yield?: number | null;
  data_source?: string | null;
  cost_basis: number;
  unrealized_pnl: number;
  unrealized_pnl_percent: number;
};

export type PositionCreate = {
  symbol: string;
  asset_name: string;
  name?: string | null;
  asset_type: string;
  quantity: number;
  average_price: number;
  current_price: number;
  currency: string;
  sector: string;
  country: string;
  exchange?: string | null;
  industry?: string | null;
  region?: string | null;
  asset_class?: string | null;
  risk_bucket?: string | null;
  liquidity_profile?: string | null;
  beta_assumption?: number | null;
  volatility_assumption?: number | null;
  duration_assumption?: number | null;
  modified_duration_assumption?: number | null;
  dv01_assumption?: number | null;
  dividend_yield?: number | null;
  data_source?: string | null;
};

export type PositionUpdate = Partial<PositionCreate>;

export type PositionListResponse = {
  portfolio_id: string;
  items: PositionRead[];
};

export type AllocationItem = {
  name: string;
  market_value: number;
  weight: number;
  weight_basis: string;
};

export type AllocationResponse = {
  portfolio_id: string;
  allocation_type: string;
  items: AllocationItem[];
};

export type ConcentrationResponse = {
  portfolio_id: string;
  largest_position_weight: number;
  top_3_holdings_weight: number;
  top_5_holdings_weight: number;
  number_of_positions: number;
  hhi_concentration: number;
  effective_number_of_holdings: number;
  diversification_score: number;
  concentration_level: string;
  warnings: string[];
};

export type RiskReturnResponse = {
  portfolio_id: string;
  expected_return: number;
  variance: number | null;
  standard_deviation: number | null;
  diversification_benefit: number | null;
  risk_return_profile: string;
  covariance_matrix_status: string;
  correlation_matrix_status: string;
  notes: string[];
  metric_source: string;
  fallback_used: boolean;
  fallback_reason: string | null;
  observations: number;
  symbols_found: string[];
  symbols_missing: string[];
  quality_warnings: string[];
  realized_annualized_return: number | null;
  realized_volatility: number | null;
  realized_sharpe_ratio: number | null;
  historical_var_95: number | null;
  historical_cvar_95: number | null;
  max_drawdown: number | null;
  tracking_error: number | null;
  covariance_symbols: string[];
};

export type BenchmarkResponse = {
  portfolio_id: string;
  benchmark_symbol: string;
  total_active_weight: number;
  active_return: number | null;
  tracking_difference: number | null;
  tracking_error: number | null;
  holdings: {
    name: string;
    portfolio_weight: number;
    benchmark_weight: number;
    active_weight: number;
  }[];
  notes: string[];
};

export type PolicyResponse = {
  portfolio_id: string;
  policy: {
    investment_objective: string;
    return_objective: string;
    risk_tolerance: string;
    time_horizon: string;
    liquidity_needs: string;
    benchmark: string;
    target_allocation: TargetAllocationItem[];
  };
  comparison: TargetAllocationItem[];
  breaches: string[];
  warnings: string[];
};

export type TargetAllocationItem = {
  name: string;
  current_weight: number;
  target_weight: number;
  drift: number;
  tolerance_band: number;
  status: string;
};

export type TargetAllocationResponse = {
  portfolio_id: string;
  items: TargetAllocationItem[];
  rebalance_needed: boolean;
};

export type RebalancingPreviewResponse = {
  portfolio_id: string;
  turnover_estimate: number;
  items: {
    name: string;
    current_market_value: number;
    target_market_value: number;
    value_difference: number;
    estimated_quantity_difference: number;
    action: string;
  }[];
  notes: string[];
};

export type PerformanceMeasurementResponse = {
  portfolio_id: string;
  beginning_value: number;
  ending_value: number;
  external_cash_flows: number;
  holding_period_return: number;
  time_weighted_return: number;
  money_weighted_return: number | null;
  notes: string[];
};

export type ConstraintsResponse = {
  portfolio_id: string;
  breaches: {
    constraint: string;
    name: string;
    actual: number;
    limit: number;
    severity: string;
  }[];
};

export type PortfolioDiagnosticsResponse = {
  portfolio_id: string;
  allocation_quality: string;
  diversification_quality: string;
  concentration_risk: string;
  cash_level: string;
  benchmark_alignment: string;
  policy_alignment: string;
  rebalancing_need: string;
  data_quality_limitations: string[];
  next_analytical_steps: string[];
  summary: string;
};

export type PortfolioMarketDataIntegrationResponse = {
  portfolio_id: string;
  symbols: string[];
  return_series_endpoint: string | null;
  aligned_returns_endpoint: string | null;
  data_quality_endpoint: string | null;
  current_status: string;
  integration_message: string;
  current_assumptions: string[];
  planned_analytics: string[];
  limitations: string[];
  readiness_badges: string[];
};

export type CfaConceptsResponse = {
  portfolio_id: string;
  portfolio_management_process: {
    phase: string;
    description: string;
  }[];
  investor_profile: {
    investor_type: string;
    liability_profile: string;
    liquidity_needs: string;
    time_horizon: string;
    return_objective: string;
    risk_objective: string;
    tax_considerations: string;
    legal_regulatory_constraints: string;
    unique_circumstances: string;
  };
  risk_tolerance: {
    ability_to_take_risk: string;
    willingness_to_take_risk: string;
    overall_risk_tolerance: string;
    conflict_detected: boolean;
    summary: string;
  };
  utility: {
    expected_return: number;
    variance: number;
    risk_aversion_coefficient: number;
    risk_aversion_classification: string;
    utility_score: number;
  };
  capm: {
    risk_free_rate: number;
    expected_market_return: number;
    market_risk_premium: number;
    portfolio_beta: number;
    capm_required_return: number;
    expected_return_gap: number;
    interpretation: string;
  };
  risk_adjusted_performance: {
    portfolio_return: number;
    benchmark_return: number;
    risk_free_rate: number;
    sharpe_ratio: number | null;
    treynor_ratio: number | null;
    jensen_alpha: number;
    active_return: number;
    tracking_error: number | null;
    information_ratio: number | null;
    notes: string[];
  };
  behavioral_biases: {
    warnings: string[];
    summary: string;
  };
  pooled_vehicle_exposure: {
    etf_exposure: number;
    single_stock_exposure: number;
    pooled_vehicle_exposure: number;
    usage_classification: string;
  };
  efficient_frontier: {
    points: {
      label: string;
      expected_return: number;
      risk: number;
    }[];
    status: string;
  };
};
