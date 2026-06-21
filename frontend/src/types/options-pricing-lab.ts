export type OptionType = "call" | "put";
export type OptionSide = "long" | "short";
export type PricingModel = "black_scholes" | "binomial";
export type ParityMode = "theoretical" | "observed";
export type StrategyLegType = "stock" | "option" | "cash";
export type OptionStrategyType =
  | "covered_call"
  | "protective_put"
  | "long_straddle"
  | "long_strangle"
  | "bull_call_spread"
  | "bear_put_spread"
  | "collar"
  | "cash_secured_put";

export type OptionsPricingLabStatus = {
  status: string;
  module: string;
  detail: string;
  engines_available: string[];
};

export type OptionPricingRequest = {
  underlying_symbol: string;
  option_type: OptionType;
  position_side: OptionSide;
  underlying_price?: number | null;
  strike_price: number;
  time_to_expiration_days: number;
  risk_free_rate: number;
  dividend_yield: number;
  volatility?: number | null;
  pricing_model: PricingModel;
  binomial_steps: number;
  contract_size: number;
  quantity: number;
  parity_mode: ParityMode;
  observed_call_price?: number | null;
  observed_put_price?: number | null;
  spot_shocks?: number[];
  volatility_shocks?: number[];
  time_points_days?: number[] | null;
  rate_shocks?: number[];
};

export type OptionLeg = {
  leg_type: StrategyLegType;
  option_type: OptionType | null;
  side: OptionSide;
  strike_price: number | null;
  expiration_days: number | null;
  quantity: number;
  contract_size: number;
  underlying_price: number | null;
  description: string;
  premium: number | null;
};

export type OptionStrategyRequest = {
  underlying_symbol: string;
  underlying_price?: number | null;
  risk_free_rate: number;
  volatility?: number | null;
  dividend_yield: number;
  strategy_type: OptionStrategyType;
  legs?: OptionLeg[];
  contract_size: number;
  quantity: number;
};

export type ImpliedVolatilityRequest = {
  underlying_symbol: string;
  option_type: OptionType;
  observed_option_price: number;
  underlying_price?: number | null;
  strike_price: number;
  time_to_expiration_days: number;
  risk_free_rate: number;
  dividend_yield: number;
  initial_guess?: number | null;
  tolerance?: number;
  max_iterations?: number;
};

export type ImpliedVolatilityResponse = {
  implied_volatility: number | null;
  converged: boolean;
  iterations: number;
  model_price_at_iv: number | null;
  pricing_error: number | null;
  no_arbitrage_bounds: { lower_bound: number; upper_bound: number };
  validation_status: string;
  warnings: string[];
  methodology: string;
  data_sources: DataSources | null;
};

export type DataSources = {
  underlying_price_source: string;
  volatility_source: string;
  risk_free_rate_source: string;
  dividend_yield_source: string;
  fallback_used: boolean;
  badges: string[];
  warnings: string[];
};

export type GreeksResponse = {
  delta: number;
  gamma: number;
  theta_annual: number;
  theta_daily: number;
  vega: number;
  rho: number;
  delta_per_contract: number;
  position_delta: number;
  position_gamma: number;
  position_theta_daily: number;
  position_vega: number;
  position_rho: number;
  delta_adjusted_exposure: number;
  interpretation: Record<string, string>;
  unit_metadata: Record<string, string>;
};

export type OptionPayoffPoint = {
  underlying_price: number;
  payoff: number;
  profit: number;
};

export type OptionSensitivityPoint = {
  input?: string;
  value?: number;
  underlying_price?: number;
  volatility?: number;
  days?: number;
  risk_free_rate?: number;
  option_price?: number;
  delta?: number;
  gamma?: number;
  theta_daily?: number;
  vega?: number;
  rho?: number;
};

export type OptionPricingResponse = {
  input_summary: {
    underlying_symbol: string;
    underlying_price: number;
    option_type: OptionType;
    position_side: OptionSide;
    strike_price: number;
    time_to_expiration_days: number;
    volatility: number;
    risk_free_rate: number;
    dividend_yield: number;
    contract_size: number;
    quantity: number;
  };
  pricing_summary: {
    option_price: number;
    black_scholes_price: number;
    binomial_price: number | null;
    intrinsic_value: number;
    time_value: number;
    moneyness: string;
    moneyness_ratio: number;
    breakeven_price: number;
    contract_premium: number;
    contract_notional: number;
  };
  payoff_summary: {
    payoff_at_spot: number;
    profit_at_spot: number;
    max_profit: number | null;
    max_profit_label: string;
    max_loss: number | null;
    risk_note: string;
    payoff_table: OptionPayoffPoint[];
  };
  greeks: GreeksResponse;
  model_details: {
    selected_model: PricingModel;
    black_scholes: {
      d1: number;
      d2: number;
      assumptions: string[];
    };
    binomial: {
      price: number | null;
      up_factor: number;
      down_factor: number;
      risk_neutral_probability: number;
      steps: number;
      no_arbitrage_valid: boolean;
      warning: string | null;
    };
    model_difference: number | null;
  };
  parity_check: {
    mode: ParityMode;
    call_price: number;
    put_price: number;
    model_call_price: number | null;
    model_put_price: number | null;
    present_value_strike: number;
    dividend_adjusted_spot: number;
    left_side: number;
    right_side: number;
    parity_gap: number;
    absolute_gap: number;
    percentage_gap: number;
    status: string;
    label: string;
    note: string;
    caveat: string;
  };
  sensitivity_analysis: {
    price: OptionSensitivityPoint[];
    volatility: OptionSensitivityPoint[];
    time_decay: OptionSensitivityPoint[];
    rates: OptionSensitivityPoint[];
    greeks_by_price: OptionSensitivityPoint[];
    scenario_metadata: {
      spot_shocks_percent: number[];
      volatility_shocks_percentage_points: number[];
      rate_shocks_percentage_points: number[];
      time_points_days: number[];
      expiration_days: number;
      time_scenarios_capped: boolean;
      note: string;
    };
  };
  methodology: Record<string, unknown>;
  assumptions: Record<string, unknown>;
  data_sources: DataSources;
  athena_commentary: {
    summary: string;
    key_points: string[];
    cfa_notes: string[];
    limitations?: string[];
  };
};

export type OptionStrategyResponse = {
  strategy_summary: {
    strategy_type: OptionStrategyType;
    underlying_symbol: string;
    underlying_price: number;
    risk_profile: string;
  };
  legs: OptionLeg[];
  net_premium: number;
  payoff_table: OptionPayoffPoint[];
  max_profit: StrategyRiskValue;
  max_loss: StrategyRiskValue;
  breakeven_points: number[];
  payoff_profile: string[];
  risk_notes: string[];
  stock_leg_included: boolean;
  collateral_requirement: number;
  aggregate_greeks: {
    aggregate_delta: number;
    aggregate_gamma: number;
    aggregate_theta: number;
    aggregate_vega: number;
    aggregate_rho: number;
    delta_adjusted_exposure: number;
    legs: StrategyLegGreeks[];
    unit_metadata: Record<string, string>;
  };
  risk_summary: Record<string, string>;
  commentary: {
    summary: string;
    key_points: string[];
    cfa_notes: string[];
    limitations?: string[];
  };
  data_sources: DataSources;
};

export type StrategyRiskValue = {
  value: number | null;
  type: "finite" | "unlimited" | "unknown";
  explanation: string;
};

export type StrategyLegGreeks = {
  leg_type: StrategyLegType;
  description: string;
  contract_size: number;
  quantity: number;
  raw_greeks: Record<string, number>;
  contract_greeks: Record<string, number>;
  position_greeks: Record<string, number>;
};
