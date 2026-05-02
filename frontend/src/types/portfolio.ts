export type PortfolioSummary = {
  id: number;
  name: string;
  base_currency: string;
};

export type PortfolioListResponse = {
  status: string;
  module: string;
  detail: string;
  items: PortfolioSummary[];
};
