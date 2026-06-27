import type { AthenaAICommentary } from "./athena-intelligence";

export type AttributionMethod = "simple" | "Brinson-lite" | "contribution";
export type PnlLanguage = "en" | "fr";

export type PnlAttributionStatus = {
  status: string;
  module: string;
  detail: string;
  attribution_ready: boolean;
  history_enabled: boolean;
  export_formats: string[];
  source_modules: string[];
  demo_mode: boolean;
};

export type PnlAttributionRequest = {
  portfolio_id: string;
  start_date: string;
  end_date: string;
  benchmark_symbol: string;
  attribution_method: AttributionMethod;
  include_income: boolean;
  include_fx: boolean;
  include_trades: boolean;
  include_rates: boolean;
  include_options: boolean;
  language: PnlLanguage;
};

export type PnlPeriod = {
  start_date: string;
  end_date: string;
  days: number;
};

export type PositionPnlContribution = {
  symbol: string;
  name: string;
  asset_type: string;
  asset_class: string;
  sector: string;
  currency: string;
  starting_price: number;
  ending_price: number;
  quantity: number;
  starting_value: number;
  ending_value: number;
  price_pnl: number;
  income_pnl: number;
  realized_pnl: number;
  unrealized_pnl: number;
  fees_and_costs: number;
  fx_pnl: number;
  total_pnl: number;
  total_pnl_percent: number;
  contribution_to_total_pnl: number;
  contribution_to_portfolio_return: number;
  data_source: string;
  warnings: string[];
};

export type GroupPnlContribution = {
  name: string;
  starting_value: number;
  ending_value: number;
  total_pnl: number;
  pnl_percent: number;
  contribution_to_total_pnl: number;
  contribution_to_portfolio_return: number;
  weight_start: number;
  weight_end: number;
};

export type BenchmarkComparison = {
  benchmark_symbol: string;
  portfolio_return: number;
  benchmark_return: number | null;
  active_return: number | null;
  relative_performance: string;
  allocation_effect: number | null;
  selection_effect: number | null;
  interaction_effect: number | null;
  tracking_note: string;
};

export type TradeEffect = {
  status: string;
  total_trade_costs: number;
  estimated_slippage: number;
  turnover: number;
  trade_impact_on_cash: number;
  trades: Record<string, unknown>[];
  warnings: string[];
};

export type FixedIncomeEffect = {
  symbol: string;
  duration_effect: number;
  convexity_effect: number;
  income_effect: number;
  rate_shock_bps: number;
  estimated_rate_pnl: number;
  residual_pnl: number;
  duration_source: string;
  limitations: string[];
};

export type OptionsEffect = {
  status: string;
  delta_contribution: number;
  gamma_contribution: number;
  vega_contribution: number;
  theta_contribution: number;
  rho_contribution: number;
  residual_pnl: number;
  notes: string[];
};

export type FxEffect = {
  currency: string;
  base_currency: string;
  local_currency_pnl: number;
  fx_translation_pnl: number;
  fx_data_source: string;
};

export type PnlMethodology = {
  attribution_method: AttributionMethod;
  assumptions: string[];
  data_sources: string[];
  limitations: string[];
};

export type PnlAttributionResult = {
  analysis_id: string;
  portfolio_id: string;
  portfolio_name: string;
  period: PnlPeriod;
  starting_value: number;
  ending_value: number;
  total_pnl: number;
  total_pnl_percent: number;
  realized_pnl: number;
  unrealized_pnl: number;
  income_pnl: number;
  fees_and_costs: number;
  fx_pnl: number;
  price_pnl: number;
  position_contributions: PositionPnlContribution[];
  asset_class_contributions: GroupPnlContribution[];
  sector_contributions: GroupPnlContribution[];
  currency_contributions: GroupPnlContribution[];
  trade_effects: TradeEffect;
  fixed_income_effects: FixedIncomeEffect[];
  options_effects: OptionsEffect;
  fx_effects: FxEffect[];
  benchmark_comparison: BenchmarkComparison;
  top_winners: PositionPnlContribution[];
  top_losers: PositionPnlContribution[];
  warnings: string[];
  methodology: PnlMethodology;
  limitations: string[];
  athena_ai_commentary: AthenaAICommentary | null;
  generated_at: string;
  status: "generated" | "generated_with_warnings";
};

export type PnlHistoryItem = {
  analysis_id: string;
  portfolio_id: string;
  portfolio_name: string;
  start_date: string;
  end_date: string;
  total_pnl: number;
  total_pnl_percent: number;
  generated_at: string;
  status: "generated" | "generated_with_warnings";
  warnings_count: number;
};

export type PnlHistoryResponse = {
  status: string;
  module: string;
  total_analyses: number;
  items: PnlHistoryItem[];
};

export type PnlCsvExportResponse = {
  analysis_id: string;
  content_type: string;
  csv: string;
  included_tables: string[];
};
