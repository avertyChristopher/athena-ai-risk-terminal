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
