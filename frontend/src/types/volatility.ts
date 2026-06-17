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
  downside_risk: DownsideRiskSummary;
  benchmark_risk: BenchmarkRiskSummary;
  distribution: DistributionSummary;
  risk_adjusted: RiskAdjustedSummary;
  volatility_regime: VolatilityRegimeSummary;
  data_source: VolatilityDataSource;
  athena_commentary: AthenaVolatilityCommentary;
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
  downside_risk: DownsideRiskSummary;
  portfolio_risk: PortfolioRiskSummary;
  covariance_matrix: MatrixSummary;
  correlation_matrix: MatrixSummary;
  risk_contribution: RiskContributionItem[];
  distribution: DistributionSummary;
  risk_adjusted: RiskAdjustedSummary;
  volatility_regime: VolatilityRegimeSummary;
  data_source: VolatilityDataSource;
  athena_commentary: AthenaVolatilityCommentary;
};

export type VolatilityAnalysis =
  | VolatilityAssetAnalysisResponse
  | VolatilityPortfolioAnalysisResponse;
