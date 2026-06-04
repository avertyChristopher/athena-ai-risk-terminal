export type SecurityProfile = {
  equity_type: string;
  voting_rights: string;
  dividend_profile: string;
  book_value_context: string;
  risk_return_notes: string[];
};

export type IndustryAnalysis = {
  classification: string;
  industry_overview: string;
  porter_forces: string[];
  pestle: string[];
  competitive_position: string;
  barriers_to_entry: string;
  pricing_power: string;
  substitution_risk: string;
  competitive_rivalry: string;
};

export type BusinessModel = {
  summary: string;
  revenue_drivers: string[];
  pricing_power: string;
  cyclicality: string;
  operating_leverage: string;
  capital_intensity: string;
};

export type SegmentRow = {
  name: string;
  revenue?: number;
  weight: number;
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
  free_float_market_cap: number | null;
  shares_outstanding: number;
  latest_price: number;
  beta: number | null;
  benchmark_symbol: string;
  business_description: string;
  data_source: string;
  is_demo_data: boolean;
  security_profile: SecurityProfile;
  industry_analysis: IndustryAnalysis;
  business_model: BusinessModel;
};

export type EquitySecurityProfileResponse = {
  symbol: string;
  security_type: string;
  exchange: string;
  currency: string;
  voting_rights: string;
  dividend_profile: string;
  liquidity_note: string;
  book_value_per_share: number | null;
  market_to_book_value: number | null;
  market_cap: number;
  free_float_market_cap: number | null;
  summary: Record<string, string | number | null>;
  placeholders: string[];
};

export type EquityIndustryResponse = {
  symbol: string;
  sector: string;
  industry: string;
  classification: string;
  industry_overview: string;
  porter_forces: string[];
  pestle: string[];
  competitive_position: string;
  barriers_to_entry: string;
  pricing_power: string;
  substitution_risk: string;
  competitive_rivalry: string;
};

export type EquityBusinessModelResponse = {
  symbol: string;
  summary: string;
  business_description: string;
  revenue_drivers: string[];
  revenue_segments: SegmentRow[];
  geographic_exposure: SegmentRow[];
  pricing_power: string;
  cyclicality: string;
  operating_leverage: string;
  capital_intensity: string;
  placeholders: string[];
};

export type EquityFundamentalsResponse = {
  symbol: string;
  revenue: number | null;
  gross_profit: number | null;
  operating_income: number | null;
  ebit: number | null;
  ebitda: number | null;
  net_income: number | null;
  eps: number | null;
  dividends_per_share: number | null;
  assets: number | null;
  liabilities: number | null;
  equity: number | null;
  debt: number | null;
  cash: number | null;
  current_assets: number | null;
  current_liabilities: number | null;
  receivables: number | null;
  marketable_securities: number | null;
  inventory: number | null;
  interest_expense: number | null;
  operating_cash_flow: number | null;
  capital_expenditures: number | null;
  free_cash_flow: number | null;
  shares_outstanding: number;
  book_value_per_share: number | null;
  working_capital: number | null;
  enterprise_value: number;
  warnings: string[];
};

export type EquityRatiosResponse = {
  symbol: string;
  gross_margin: number | null;
  operating_margin: number | null;
  ebit_margin: number | null;
  ebitda_margin: number | null;
  net_margin: number | null;
  roe: number | null;
  roa: number | null;
  roic: number | null;
  debt_to_equity: number | null;
  debt_to_assets: number | null;
  net_debt: number | null;
  net_debt_to_ebitda: number | null;
  current_ratio: number | null;
  quick_ratio: number | null;
  interest_coverage: number | null;
  asset_turnover: number | null;
  receivables_turnover: number | null;
  inventory_turnover: number | null;
  free_cash_flow_margin: number | null;
  dividend_payout_ratio: number | null;
  retention_ratio: number | null;
  sustainable_growth_rate: number | null;
  quality_score: number;
  warnings: string[];
};

export type EquityGrowthResponse = {
  symbol: string;
  revenue_growth: number | null;
  eps_growth: number | null;
  operating_income_growth: number | null;
  dividend_growth_rate: number | null;
  sustainable_growth_rate: number | null;
  retention_ratio: number | null;
  roe: number | null;
  growth_profile: string;
  forecast_assumptions: string[];
  warnings: string[];
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
  pe_ratio: number | null;
  forward_pe_ratio: number | null;
  pb_ratio: number | null;
  ps_ratio: number | null;
  enterprise_value: number;
  ev_ebitda: number | null;
  ev_sales: number | null;
  peg_ratio: number | null;
  dividend_yield: number;
  earnings_yield: number | null;
  free_cash_flow_yield: number | null;
  intrinsic_value: number;
  market_price: number;
  margin_of_safety: number;
  valuation_status: string;
  sector_pe_ratio: number;
  sensitivity_table: SensitivityCell[];
  warnings: string[];
};

export type EquityRelativeValuationResponse = {
  symbol: string;
  multiples: Record<string, number | null>;
  peer_medians: Record<string, number | null>;
  multiple_status: Record<string, string>;
  premium_discount_to_peers: Record<string, number | null>;
  warnings: string[];
};

export type EquityPeerComparisonResponse = {
  symbol: string;
  benchmark_symbol: string;
  peer_symbols: string[];
  peer_rows: Array<Record<string, string | number | null>>;
  profitability_vs_peers: string;
  growth_vs_peers: string;
  valuation_vs_peers: string;
  relative_performance_vs_benchmark: number | null;
  sector_relative_summary: string;
};

export type EquityCorporateActionsResponse = {
  symbol: string;
  dividend_profile: string;
  dividend_yield: number;
  payout_ratio: number | null;
  retention_ratio: number | null;
  stock_split_summary: string;
  share_repurchases_summary: string;
  buyback_yield: number | null;
  total_shareholder_yield: number | null;
  timeline: Array<Record<string, string>>;
  placeholders: string[];
};

export type EquityDiagnosticsResponse = {
  symbol: string;
  valuation_status: string;
  valuation_profile: string;
  profitability_quality: string;
  balance_sheet_quality: string;
  growth_profile: string;
  dividend_profile: string;
  risk_profile: string;
  strengths: string[];
  weaknesses: string[];
  risks: string[];
  watchlist_flags: string[];
  bull_base_bear: Record<string, string>;
  governance: Record<string, string>;
  esg_considerations: Record<string, string>;
  risk_factors: Record<string, string[]>;
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
