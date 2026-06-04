from typing import Any

from pydantic import BaseModel


class EquityOverviewResponse(BaseModel):
    symbol: str
    company_name: str
    ticker: str
    exchange: str
    sector: str
    industry: str
    country: str
    currency: str
    market_cap: float
    free_float_market_cap: float | None
    shares_outstanding: float
    latest_price: float
    beta: float | None
    benchmark_symbol: str
    business_description: str
    data_source: str
    is_demo_data: bool
    security_profile: dict[str, Any]
    industry_analysis: dict[str, Any]
    business_model: dict[str, Any]


class EquitySecurityProfileResponse(BaseModel):
    symbol: str
    security_type: str
    exchange: str
    currency: str
    voting_rights: str
    dividend_profile: str
    liquidity_note: str
    book_value_per_share: float | None
    market_to_book_value: float | None
    market_cap: float
    free_float_market_cap: float | None
    summary: dict[str, Any]
    placeholders: list[str]


class EquityIndustryResponse(BaseModel):
    symbol: str
    sector: str
    industry: str
    classification: str
    industry_overview: str
    porter_forces: list[str]
    pestle: list[str]
    competitive_position: str
    barriers_to_entry: str
    pricing_power: str
    substitution_risk: str
    competitive_rivalry: str


class EquityBusinessModelResponse(BaseModel):
    symbol: str
    summary: str
    business_description: str
    revenue_drivers: list[str]
    revenue_segments: list[dict[str, Any]]
    geographic_exposure: list[dict[str, Any]]
    pricing_power: str
    cyclicality: str
    operating_leverage: str
    capital_intensity: str
    placeholders: list[str]


class EquityFundamentalsResponse(BaseModel):
    symbol: str
    revenue: float | None
    gross_profit: float | None
    operating_income: float | None
    ebit: float | None
    ebitda: float | None
    net_income: float | None
    eps: float | None
    dividends_per_share: float | None
    assets: float | None
    liabilities: float | None
    equity: float | None
    debt: float | None
    cash: float | None
    current_assets: float | None
    current_liabilities: float | None
    receivables: float | None
    marketable_securities: float | None
    inventory: float | None
    interest_expense: float | None
    operating_cash_flow: float | None
    capital_expenditures: float | None
    free_cash_flow: float | None
    shares_outstanding: float
    book_value_per_share: float | None
    working_capital: float | None
    enterprise_value: float
    warnings: list[str]


class EquityRatiosResponse(BaseModel):
    symbol: str
    gross_margin: float | None
    operating_margin: float | None
    ebit_margin: float | None
    ebitda_margin: float | None
    net_margin: float | None
    roe: float | None
    roa: float | None
    roic: float | None
    debt_to_equity: float | None
    debt_to_assets: float | None
    net_debt: float | None
    net_debt_to_ebitda: float | None
    current_ratio: float | None
    quick_ratio: float | None
    interest_coverage: float | None
    asset_turnover: float | None
    receivables_turnover: float | None
    inventory_turnover: float | None
    free_cash_flow_margin: float | None
    dividend_payout_ratio: float | None
    retention_ratio: float | None
    sustainable_growth_rate: float | None
    quality_score: float
    warnings: list[str]


class EquityGrowthResponse(BaseModel):
    symbol: str
    revenue_growth: float | None
    eps_growth: float | None
    operating_income_growth: float | None
    dividend_growth_rate: float | None
    sustainable_growth_rate: float | None
    retention_ratio: float | None
    roe: float | None
    growth_profile: str
    forecast_assumptions: list[str]
    warnings: list[str]


class EquityValuationResponse(BaseModel):
    symbol: str
    required_return: float
    growth_rate: float
    dividend_next_year: float
    gordon_growth_value: float
    dividend_discount_value: float
    implied_cost_of_equity: float
    implied_growth_rate: float
    pe_ratio: float | None
    forward_pe_ratio: float | None
    pb_ratio: float | None
    ps_ratio: float | None
    enterprise_value: float
    ev_ebitda: float | None
    ev_sales: float | None
    peg_ratio: float | None
    dividend_yield: float
    earnings_yield: float | None
    free_cash_flow_yield: float | None
    intrinsic_value: float
    market_price: float
    margin_of_safety: float
    valuation_status: str
    sector_pe_ratio: float
    sensitivity_table: list[dict[str, Any]]
    warnings: list[str]


class EquityRelativeValuationResponse(BaseModel):
    symbol: str
    multiples: dict[str, float | None]
    peer_medians: dict[str, float | None]
    multiple_status: dict[str, str]
    premium_discount_to_peers: dict[str, float | None]
    warnings: list[str]


class EquityPeerComparisonResponse(BaseModel):
    symbol: str
    benchmark_symbol: str
    peer_symbols: list[str]
    peer_rows: list[dict[str, Any]]
    profitability_vs_peers: str
    growth_vs_peers: str
    valuation_vs_peers: str
    relative_performance_vs_benchmark: float | None
    sector_relative_summary: str


class EquityCorporateActionsResponse(BaseModel):
    symbol: str
    dividend_profile: str
    dividend_yield: float
    payout_ratio: float | None
    retention_ratio: float | None
    stock_split_summary: str
    share_repurchases_summary: str
    buyback_yield: float | None
    total_shareholder_yield: float | None
    timeline: list[dict[str, str]]
    placeholders: list[str]


class EquityDiagnosticsResponse(BaseModel):
    symbol: str
    valuation_status: str
    valuation_profile: str
    profitability_quality: str
    balance_sheet_quality: str
    growth_profile: str
    dividend_profile: str
    risk_profile: str
    strengths: list[str]
    weaknesses: list[str]
    risks: list[str]
    watchlist_flags: list[str]
    bull_base_bear: dict[str, str]
    governance: dict[str, Any]
    esg_considerations: dict[str, Any]
    risk_factors: dict[str, list[str]]
    analyst_summary: str
    educational_note: str


class GgmValuationRequest(BaseModel):
    dividend_next_year: float
    required_return: float
    growth_rate: float


class GgmValuationResponse(BaseModel):
    intrinsic_value: float
    spread: float


class SensitivityRequest(BaseModel):
    dividend_next_year: float
    required_returns: list[float]
    growth_rates: list[float]


class SensitivityCell(BaseModel):
    required_return: float
    growth_rate: float
    intrinsic_value: float | None


class SensitivityResponse(BaseModel):
    cells: list[SensitivityCell]
