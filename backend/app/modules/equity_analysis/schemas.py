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
    price_source: str = "demo"
    price_timestamp: str | None = None
    benchmark_source: str = "demo"
    beta_source: str = "demo"
    risk_free_rate_source: str = "demo"
    data_source_notes: list[str] = []


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


class EquityCapmResponse(BaseModel):
    symbol: str
    risk_free_rate: float | None
    beta: float | None
    expected_market_return: float
    market_risk_premium: float | None
    capm_required_return: float | None
    expected_return: float | None
    expected_return_vs_required_return: float | None
    capm_signal: str
    price_source: str
    price_timestamp: str | None
    benchmark_source: str
    beta_source: str
    risk_free_rate_source: str
    data_source_notes: list[str]
    warnings: list[str]


class EquityDupontResponse(BaseModel):
    symbol: str
    net_margin: float | None
    asset_turnover: float | None
    financial_leverage: float | None
    three_step_roe: float | None
    reported_roe: float | None
    tax_burden: float | None
    interest_burden: float | None
    ebit_margin: float | None
    extended_dupont_roe: float | None
    drivers: list[str]
    warnings: list[str]


class EquityEarningsQualityResponse(BaseModel):
    symbol: str
    cash_conversion_ratio: float | None
    accruals_ratio: float | None
    fcf_conversion_ratio: float | None
    net_income_vs_operating_cash_flow: str
    earnings_quality: str
    earnings_persistence_placeholder: str
    non_recurring_items_placeholder: str
    working_capital_quality: str
    revenue_quality_placeholder: str
    warnings: list[str]


class HistoricalFundamentalRow(BaseModel):
    year: int
    revenue: float | None
    gross_profit: float | None
    operating_income: float | None
    net_income: float | None
    eps: float | None
    dividends_per_share: float | None
    assets: float | None
    liabilities: float | None
    equity: float | None
    debt: float | None
    cash: float | None
    operating_cash_flow: float | None
    capital_expenditures: float | None
    free_cash_flow: float | None


class EquityHistoricalFundamentalsResponse(BaseModel):
    symbol: str
    rows: list[HistoricalFundamentalRow]
    revenue_cagr: float | None
    eps_cagr: float | None
    revenue_growth: list[dict[str, float | int | None]]
    margin_trends: dict[str, list[dict[str, float | int | None]]]
    ratio_trends: dict[str, list[dict[str, float | int | None]]]
    trend_diagnostics: list[str]
    warnings: list[str]


class DcfRequest(BaseModel):
    symbol: str
    revenue_growth_rate: float = 0.05
    ebit_margin: float = 0.25
    tax_rate: float = 0.21
    depreciation_percent_of_revenue: float = 0.03
    capex_percent_of_revenue: float = 0.05
    working_capital_percent_of_revenue: float = 0.01
    net_borrowing: float = 0.0
    wacc: float = 0.09
    cost_of_equity: float = 0.09
    terminal_growth_rate: float = 0.03
    forecast_years: int = 5


class DcfForecastRow(BaseModel):
    year: int
    revenue: float
    ebit: float
    depreciation: float
    capital_expenditures: float
    change_in_working_capital: float
    fcff: float
    fcfe: float


class EquityDcfResponse(BaseModel):
    symbol: str
    assumptions: dict[str, float | int]
    forecast: list[DcfForecastRow]
    enterprise_value_fcff: float
    equity_value_fcff: float
    intrinsic_value_per_share_fcff: float
    equity_value_fcfe: float
    intrinsic_value_per_share_fcfe: float
    market_price: float
    margin_of_safety_fcff: float
    margin_of_safety_fcfe: float
    sensitivity_table: list[dict[str, float | None]]
    warnings: list[str]


class EquityDataQualityResponse(BaseModel):
    symbol: str
    missing_fields: list[str]
    negative_value_warnings: list[str]
    stale_data_warning: str | None
    market_cap_consistent: bool
    fcf_consistent: bool
    peer_data_available: bool
    benchmark_available: bool
    demo_data_warning: str
    quality_score: float
    is_usable: bool
    warnings: list[str]


class EquitySectorInterpretationResponse(BaseModel):
    symbol: str
    sector: str
    industry: str
    ratio_emphasis: list[str]
    interpretation_notes: list[str]


class EquityInstitutionalSignalsResponse(BaseModel):
    symbol: str
    signal: str
    portfolio_builder_bridge: dict[str, float | str | None]
    data_source_notes: list[str]
