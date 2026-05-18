export type MarketAsset = {
  symbol: string;
  name: string;
  asset_type: string;
  currency: string;
  sector: string;
  country: string;
};

export type PricePoint = {
  date: string;
  symbol: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
};

export type ReturnPoint = {
  date: string;
  symbol: string;
  simple_return: number;
  log_return: number;
  cumulative_return: number;
  drawdown: number;
};

export type VolatilityResponse = {
  symbol: string;
  daily_volatility: number;
  annualized_volatility: number;
};

export type DataQualityResponse = {
  symbol: string;
  rows: number;
  missing_price_dates: string[];
  duplicate_dates: string[];
  outlier_indexes: number[];
  is_valid: boolean;
};

export type MarketDataAnalyticsResponse = {
  symbol: string;
  benchmark_symbol: string;
  latest_price: number;
  latest_return: number;
  holding_period_return: number;
  cumulative_return: number;
  arithmetic_mean_return: number;
  geometric_mean_return: number;
  annualized_return: number;
  variance: number;
  standard_deviation: number;
  daily_volatility: number;
  annualized_volatility: number;
  max_drawdown: number;
  skewness: number;
  kurtosis: number;
  percentiles: Record<string, number>;
  outlier_indexes: number[];
  benchmark_latest_return: number;
  active_return_vs_benchmark: number;
  correlation_with_benchmark: number;
  covariance_with_benchmark: number;
  beta_vs_benchmark: number;
  sharpe_ratio: number;
  moving_average_5: number | null;
  moving_average_20: number | null;
  momentum_5_day: number | null;
  risk_free_rate_proxy: number;
  adjusted_close_latest: number;
  corporate_action_status: string;
  average_volume_20: number;
  latest_dollar_volume: number;
  liquidity_score: number;
  normal_distribution_coverage: number;
  fx_rate_to_usd: number;
  currency_consistency_status: string;
  yield_curve_2y: number;
  yield_curve_10y: number;
  commodity_proxy_symbol: string;
  commodity_proxy_latest_price: number;
};
