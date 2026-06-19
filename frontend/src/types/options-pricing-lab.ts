export type OptionType = "call" | "put";
export type OptionSide = "long" | "short";
export type PricingModel = "black_scholes" | "binomial";
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
};

export type OptionLeg = {
  option_type: OptionType;
  side: OptionSide;
  strike: number;
  expiration_days: number;
  quantity: number;
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
  delta_adjusted_exposure: number;
  interpretation: Record<string, string>;
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
    binomial_price: number;
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
      price: number;
      up_factor: number;
      down_factor: number;
      risk_neutral_probability: number;
      steps: number;
    };
    model_difference: number;
  };
  parity_check: {
    left_side: number;
    right_side: number;
    parity_gap: number;
    status: string;
    note: string;
  };
  sensitivity_analysis: {
    price: OptionSensitivityPoint[];
    volatility: OptionSensitivityPoint[];
    time_decay: OptionSensitivityPoint[];
    rates: OptionSensitivityPoint[];
    greeks_by_price: OptionSensitivityPoint[];
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
  max_profit: number | null;
  max_loss: number | null;
  breakeven_points: number[];
  aggregate_greeks: Record<string, number>;
  risk_summary: Record<string, string>;
  commentary: {
    summary: string;
    key_points: string[];
    cfa_notes: string[];
    limitations?: string[];
  };
  data_sources: DataSources;
};
