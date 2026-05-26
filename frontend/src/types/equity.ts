export type SecurityProfile = {
  equity_type: string;
  voting_rights: string;
  dividend_profile: string;
  book_value_context: string;
  risk_return_notes: string[];
};

export type IndustryAnalysis = {
  classification: string;
  porter_forces: string[];
  pestle: string[];
  competitive_position: string;
};

export type BusinessModel = {
  summary: string;
  revenue_drivers: string[];
  pricing_power: string;
  operating_leverage: string;
};

export type EquityOverviewResponse = {
  symbol: string;
  company_name: string;
  ticker: string;
  exchange: string;
  sector: string;
  industry: string;
  country: string;
  currency: string;
  market_cap: number;
  latest_price: number;
  benchmark_symbol: string;
  security_profile: SecurityProfile;
  industry_analysis: IndustryAnalysis;
  business_model: BusinessModel;
};

export type EquityFundamentalsResponse = {
  symbol: string;
  revenue: number;
  gross_profit: number;
  ebit: number;
  ebitda: number;
  net_income: number;
  eps: number;
  dividends_per_share: number;
  assets: number;
  liabilities: number;
  equity: number;
  debt: number;
  cash: number;
  current_assets: number;
  current_liabilities: number;
  receivables: number;
  marketable_securities: number;
  interest_expense: number;
  operating_cash_flow: number;
  free_cash_flow: number;
  shares_outstanding: number;
  book_value_per_share: number;
  enterprise_value: number;
};

export type EquityRatiosResponse = {
  symbol: string;
  gross_margin: number;
  operating_margin: number;
  net_margin: number;
  roe: number;
  roa: number;
  debt_to_equity: number;
  current_ratio: number;
  quick_ratio: number;
  interest_coverage: number;
  dividend_payout_ratio: number;
  retention_ratio: number;
  sustainable_growth_rate: number;
};

export type EquityValuationResponse = {
  symbol: string;
  required_return: number;
  growth_rate: number;
  dividend_next_year: number;
  gordon_growth_value: number;
  dividend_discount_value: number;
  implied_cost_of_equity: number;
  implied_growth_rate: number;
  pe_ratio: number;
  pb_ratio: number;
  ps_ratio: number;
  ev_ebitda: number;
  dividend_yield: number;
  earnings_yield: number;
  free_cash_flow_yield: number;
  intrinsic_value: number;
  market_price: number;
  margin_of_safety: number;
  sector_pe_ratio: number;
};

export type EquityDiagnosticsResponse = {
  symbol: string;
  valuation_status: string;
  profitability_quality: string;
  balance_sheet_quality: string;
  strengths: string[];
  risks: string[];
  analyst_summary: string;
  educational_note: string;
};

export type GgmValuationRequest = {
  dividend_next_year: number;
  required_return: number;
  growth_rate: number;
};

export type GgmValuationResponse = {
  intrinsic_value: number;
  spread: number;
};

export type SensitivityRequest = {
  dividend_next_year: number;
  required_returns: number[];
  growth_rates: number[];
};

export type SensitivityCell = {
  required_return: number;
  growth_rate: number;
  intrinsic_value: number | null;
};

export type SensitivityResponse = {
  cells: SensitivityCell[];
};
