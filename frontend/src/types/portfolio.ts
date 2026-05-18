export type PortfolioSummary = {
  portfolio_id: string;
  name: string;
  base_currency: string;
  total_value: number;
  number_of_positions: number;
  benchmark: string;
  cash: number;
  cash_weight: number;
  largest_position_weight: number;
  top_5_holdings_weight: number;
};

export type PortfolioRead = {
  id: string;
  name: string;
  base_currency: string;
  benchmark: string;
  cash: number;
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
  asset_type: string;
  quantity: number;
  average_price: number;
  current_price: number;
  market_value: number;
  weight: number;
  currency: string;
  sector: string;
  country: string;
};

export type PositionCreate = {
  symbol: string;
  asset_name: string;
  asset_type: string;
  quantity: number;
  average_price: number;
  current_price: number;
  currency: string;
  sector: string;
  country: string;
};

export type PositionListResponse = {
  portfolio_id: string;
  items: PositionRead[];
};

export type AllocationItem = {
  name: string;
  market_value: number;
  weight: number;
};

export type AllocationResponse = {
  portfolio_id: string;
  allocation_type: string;
  items: AllocationItem[];
};
