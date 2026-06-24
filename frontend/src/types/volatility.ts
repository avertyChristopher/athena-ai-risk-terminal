import type { AthenaAICommentary } from "./athena-intelligence";

export type VolatilityLabStatus = {
  status: string;
  module: string;
  detail: string;
  engines_available: string[];
};

export type VolatilityAssetAnalysisRequest = {
  symbol: string;
  benchmark_symbol?: string;
  start_date?: string | null;
  end_date?: string | null;
  risk_free_rate?: number;
  rolling_window?: number;
  annualization_factor?: number;
  confidence_level?: number;
  horizon_days?: number;
};

export type VolatilityPortfolioAnalysisRequest = {
  portfolio_id: string;
  benchmark_symbol?: string;
  start_date?: string | null;
  end_date?: string | null;
  risk_free_rate?: number;
  rolling_window?: number;
  annualization_factor?: number;
  confidence_level?: number;
  horizon_days?: number;
};

export type DateFilterMetadata = {
  start_date: string | null;
  end_date: string | null;
  applied: boolean;
  valid: boolean;
  observations_after_filter: number;
  warnings: string[];
};

export type ReturnQualityMetadata = {
  total_price_rows: number;
  valid_returns: number;
  skipped_returns: number;
  skipped_reason_counts: Record<string, number>;
  has_invalid_prices: boolean;
  warnings: string[];
};

export type PortfolioCoverageMetadata = {
  total_holdings: number;
  covered_holdings: number;
  missing_holdings: number;
  covered_weight: number;
  missing_weight: number;
  coverage_ratio: number;
  weights_renormalized: boolean;
  missing_symbols: string[];
  excluded_holdings: { symbol: string; weight: number }[];
  missing_weight_warning: string | null;
  risk_understatement_warning: string | null;
  coverage_adjusted_risk_warning: string;
};

export type MethodologyMetadata = {
  volatility: Record<string, unknown>;
  ewma: Record<string, unknown>;
  historical_var: Record<string, unknown>;
  parametric_var: Record<string, unknown>;
  monte_carlo_var: Record<string, unknown>;
  covariance: Record<string, unknown>;
  correlation: Record<string, unknown>;
};

export type VarBacktestSummary = {
  observations: number;
  exceptions: number;
  exception_rate: number;
  expected_exception_rate: number;
  status: string;
  note: string;
};

export type StressScenarioSummary = {
  name: string;
  volatility_multiplier: number;
  stressed_volatility: number;
  stressed_var: number;
  stressed_cvar: number;
  risk_status: string;
  note: string;
};

export type ReturnSummary = {
  observations: number;
  arithmetic_mean_return: number;
  geometric_mean_return: number;
  holding_period_return: number;
  cumulative_return: number;
  annualized_return: number;
  excess_return: number;
  active_return: number | null;
};

export type VolatilitySummary = {
  variance: number;
  standard_deviation: number;
  daily_volatility: number;
  annualized_volatility: number;
  realized_volatility: number;
  coefficient_of_variation: number | null;
  rolling_latest: number | null;
  rolling_minimum: number | null;
  rolling_maximum: number | null;
  rolling_average: number | null;
};

export type RollingVolatilityPoint = {
  date: string;
  volatility: number;
};

export type DrawdownPoint = {
  date: string;
  drawdown: number;
};

export type EWMAVolatilitySummary = {
  latest_volatility: number | null;
  lambda_decay: number;
  annualization_factor: number;
  observations: number;
  metric_source: string;
  badge: string;
  explanation: string;
};

export type VarModelSummary = {
  confidence_level: number;
  horizon_days: number;
  historical_var: number;
  historical_cvar: number;
  parametric_var: number;
  parametric_cvar: number;
  monte_carlo_var: number | null;
  monte_carlo_cvar: number | null;
  historical_horizon_note: string;
  parametric_horizon_note: string;
  monte_carlo_status: string;
  parametric_assumption: string;
  monte_carlo_method: string;
};

export type DownsideRiskSummary = {
  downside_deviation: number;
  semi_variance: number;
  semi_deviation: number;
  worst_return: number;
  best_return: number;
  max_drawdown: number;
  probability_negative_return: number;
  historical_var: number;
  historical_cvar: number;
};

export type BenchmarkRiskSummary = {
  benchmark_symbol: string;
  covariance: number;
  correlation: number;
  beta: number;
  capm_required_return: number;
  jensen_alpha: number;
  systematic_risk_note: string;
  diversification_note: string;
};

export type DistributionSummary = {
  mean: number;
  median: number;
  minimum: number;
  maximum: number;
  skewness: number;
  kurtosis: number;
  percentiles: Record<string, number>;
  histogram: {
    bucket: number;
    lower: number;
    upper: number;
    count: number;
  }[];
  normality_note: string;
};

export type RiskAdjustedSummary = {
  sharpe_ratio: number | null;
  treynor_ratio: number | null;
  sortino_ratio: number | null;
  tracking_error: number | null;
  information_ratio: number | null;
};

export type VolatilityRegimeSummary = {
  regime: string;
  latest_volatility: number | null;
  reference_percentile: number | null;
  explanation: string;
};

export type VolatilityDataSource = {
  metric_source: string;
  fallback_used: boolean;
  fallback_reason: string | null;
  observations: number;
  symbols_found: string[];
  symbols_missing: string[];
  warnings: string[];
  badges: string[];
};

export type MatrixSummary = {
  symbols: string[];
  matrix: number[][];
  interpretation: string;
};

export type RiskContributionItem = {
  symbol: string;
  weight: number;
  contribution: number;
};

export type AdvancedModelsStatus = {
  ewma: string;
  garch: string;
  implied_volatility: string;
  volatility_surface: string;
  options_implied_skew: string;
};

export type RiskMonitorPayload = {
  payload_version: string;
  source_module: string;
  module_name: string;
  portfolio_id: string | null;
  symbol: string | null;
  benchmark_symbol: string;
  analysis_mode: "asset" | "portfolio";
  confidence_level: number;
  annualized_volatility: number;
  ewma_volatility: number | null;
  historical_var: number;
  historical_cvar: number;
  parametric_var: number;
  parametric_cvar: number;
  monte_carlo_var: number | null;
  monte_carlo_cvar: number | null;
  beta: number;
  correlation: number;
  tracking_error: number | null;
  sharpe_ratio: number | null;
  sortino_ratio: number | null;
  max_drawdown: number;
  risk_contribution: RiskContributionItem[];
  covariance_summary: Record<string, unknown> | null;
  correlation_summary: Record<string, unknown> | null;
  data_source: VolatilityDataSource;
  metric_source: string;
  methodology: string | Record<string, unknown> | null;
  assumptions: string[];
  limitations: string[];
  missing_symbols: string[];
  coverage_ratio: number | null;
  fallback_used: boolean;
  warnings: string[];
  generated_at: string;
};

export type PortfolioRiskSummary = {
  portfolio_volatility: number;
  covariance_based_volatility: number;
  weighted_average_asset_volatility: number;
  diversification_benefit: number;
  largest_risk_contributor: string | null;
  beta: number;
  tracking_error: number | null;
};

export type AthenaVolatilityCommentary = {
  summary: string;
  key_points: string[];
  trade_simulator_reuse_note: string;
  cfa_notes: string[];
};

export type VolatilityAssetAnalysisResponse = {
  symbol: string;
  benchmark_symbol: string;
  latest_price: number | null;
  return_summary: ReturnSummary;
  volatility_summary: VolatilitySummary;
  rolling_volatility: RollingVolatilityPoint[];
  drawdown_series: DrawdownPoint[];
  ewma_volatility: EWMAVolatilitySummary;
  var_models: VarModelSummary;
  downside_risk: DownsideRiskSummary;
  benchmark_risk: BenchmarkRiskSummary;
  distribution: DistributionSummary;
  risk_adjusted: RiskAdjustedSummary;
  volatility_regime: VolatilityRegimeSummary;
  advanced_models: AdvancedModelsStatus;
  risk_monitor_payload: RiskMonitorPayload;
  data_source: VolatilityDataSource;
  date_filter: DateFilterMetadata;
  return_quality: ReturnQualityMetadata;
  methodology: MethodologyMetadata;
  var_backtest: VarBacktestSummary;
  stress_scenarios: StressScenarioSummary[];
  athena_commentary: AthenaVolatilityCommentary;
  athena_ai_commentary?: AthenaAICommentary | null;
};

export type VolatilityPortfolioAnalysisResponse = {
  portfolio_id: string;
  portfolio_name: string;
  benchmark_symbol: string;
  holdings_included: string[];
  holdings_missing: string[];
  return_summary: ReturnSummary;
  volatility_summary: VolatilitySummary;
  rolling_volatility: RollingVolatilityPoint[];
  drawdown_series: DrawdownPoint[];
  ewma_volatility: EWMAVolatilitySummary;
  var_models: VarModelSummary;
  downside_risk: DownsideRiskSummary;
  portfolio_risk: PortfolioRiskSummary;
  covariance_matrix: MatrixSummary;
  correlation_matrix: MatrixSummary;
  risk_contribution: RiskContributionItem[];
  distribution: DistributionSummary;
  risk_adjusted: RiskAdjustedSummary;
  volatility_regime: VolatilityRegimeSummary;
  advanced_models: AdvancedModelsStatus;
  risk_monitor_payload: RiskMonitorPayload;
  data_source: VolatilityDataSource;
  date_filter: DateFilterMetadata;
  return_quality: ReturnQualityMetadata;
  portfolio_coverage: PortfolioCoverageMetadata;
  methodology: MethodologyMetadata;
  var_backtest: VarBacktestSummary;
  stress_scenarios: StressScenarioSummary[];
  athena_commentary: AthenaVolatilityCommentary;
  athena_ai_commentary?: AthenaAICommentary | null;
};

export type VolatilityAnalysis =
  | VolatilityAssetAnalysisResponse
  | VolatilityPortfolioAnalysisResponse;
