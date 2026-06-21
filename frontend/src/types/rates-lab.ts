export type CouponFrequency = "annual" | "semiannual" | "quarterly" | "monthly";
export type BondType = "coupon_bond" | "zero_coupon";
export type RateScenarioType =
  | "parallel_up"
  | "parallel_down"
  | "steepener"
  | "flattener"
  | "short_rate_up"
  | "long_rate_up"
  | "short_rate_down"
  | "long_rate_down";

export type RatesLabStatus = {
  status: string;
  module: string;
  detail: string;
  engines_available: string[];
};

export type DataSourceMetadata = {
  rate_source: string;
  curve_source: string;
  portfolio_source: string;
  fallback_used: boolean;
  badges: string[];
  warnings: string[];
};

export type MethodologyMetadata = {
  method: string;
  assumptions: string[];
  limitations: string[];
  details: Record<string, unknown>;
};

export type AthenaRatesCommentary = {
  summary: string;
  key_points: string[];
  cfa_notes: string[];
  not_investment_advice: boolean;
};

export type BondInputs = {
  bond_type: BondType;
  face_value: number;
  coupon_rate: number;
  coupon_frequency: CouponFrequency;
  years_to_maturity: number;
  yield_to_maturity: number;
};

export type CashFlow = {
  period: number;
  time_years: number;
  coupon: number;
  principal: number;
  total_cash_flow: number;
  discount_factor: number;
  present_value: number;
};

export type BondPricingResponse = {
  bond_type: BondType;
  clean_price: number;
  dirty_price: number;
  accrued_interest: number;
  present_value_of_cashflows: number;
  price_status: string;
  cash_flow_schedule: CashFlow[];
  yield_assumptions: Record<string, unknown>;
  methodology: MethodologyMetadata;
  data_source: DataSourceMetadata;
  athena_commentary: AthenaRatesCommentary;
};

export type YieldAnalysisResponse = {
  yield_to_maturity: number | null;
  current_yield: number;
  holding_period_return: number | null;
  convergence_status: string;
  iterations: number;
  pricing_error: number;
  price_status: string;
  interpretation: string;
  methodology: MethodologyMetadata;
  data_source: DataSourceMetadata;
  athena_commentary: AthenaRatesCommentary;
};

export type DurationConvexityResponse = {
  price: number;
  macaulay_duration: number;
  modified_duration: number;
  convexity: number;
  dv01: number;
  pvbp: number;
  rate_shock_bps: number;
  estimated_price_change_duration: number;
  estimated_price_change_duration_convexity: number;
  estimated_stressed_price_duration: number;
  estimated_stressed_price_duration_convexity: number;
  risk_interpretation: string;
  methodology: MethodologyMetadata;
  risk_monitor_payload: Record<string, unknown>;
  data_source: DataSourceMetadata;
  athena_commentary: AthenaRatesCommentary;
};

export type CurvePoint = { maturity: number; rate: number };
export type ForwardRatePoint = {
  start_maturity: number;
  end_maturity: number;
  forward_rate: number;
};

export type YieldCurveResponse = {
  input_curve: CurvePoint[];
  interpolated_curve: CurvePoint[];
  spot_rates: CurvePoint[];
  forward_rates: ForwardRatePoint[];
  curve_slope: number;
  curve_slope_bps: number;
  curve_shape: string;
  curve_interpretation: string;
  methodology: MethodologyMetadata;
  data_source: DataSourceMetadata;
  athena_commentary: AthenaRatesCommentary;
};

export type RateScenarioResponse = {
  scenario_type: RateScenarioType;
  shock_bps: number;
  base_price: number;
  stressed_price: number;
  price_change: number;
  percent_change: number;
  duration_estimate: number;
  convexity_adjusted_estimate: number;
  dv01_impact: number;
  base_curve: CurvePoint[];
  stressed_curve: CurvePoint[];
  scenario_interpretation: string;
  risk_warning: string;
  methodology: MethodologyMetadata;
  stress_testing_payload: Record<string, unknown>;
  data_source: DataSourceMetadata;
};

export type FixedIncomeHolding = {
  symbol: string;
  name: string;
  asset_type: string;
  market_value: number;
  weight: number;
  estimated_duration: number | null;
  estimated_dv01: number | null;
  metadata_source: string;
  warning: string | null;
};

export type PortfolioRatesExposureResponse = {
  portfolio_id: string;
  portfolio_name: string;
  fixed_income_holdings: FixedIncomeHolding[];
  fixed_income_market_value: number;
  fixed_income_allocation: number;
  weighted_average_duration: number | null;
  estimated_portfolio_dv01: number | null;
  estimated_rate_shock_loss: number | null;
  shock_bps: number;
  missing_data_warnings: string[];
  risk_monitor_payload: Record<string, unknown>;
  methodology: MethodologyMetadata;
  data_source: DataSourceMetadata;
};
