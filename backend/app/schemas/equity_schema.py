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
    latest_price: float
    benchmark_symbol: str
    security_profile: dict[str, object]
    industry_analysis: dict[str, object]
    business_model: dict[str, object]


class EquityFundamentalsResponse(BaseModel):
    symbol: str
    revenue: float
    gross_profit: float
    ebit: float
    ebitda: float
    net_income: float
    eps: float
    dividends_per_share: float
    assets: float
    liabilities: float
    equity: float
    debt: float
    cash: float
    current_assets: float
    current_liabilities: float
    receivables: float
    marketable_securities: float
    interest_expense: float
    operating_cash_flow: float
    free_cash_flow: float
    shares_outstanding: float
    book_value_per_share: float
    enterprise_value: float


class EquityRatiosResponse(BaseModel):
    symbol: str
    gross_margin: float
    operating_margin: float
    net_margin: float
    roe: float
    roa: float
    debt_to_equity: float
    current_ratio: float
    quick_ratio: float
    interest_coverage: float
    dividend_payout_ratio: float
    retention_ratio: float
    sustainable_growth_rate: float


class EquityValuationResponse(BaseModel):
    symbol: str
    required_return: float
    growth_rate: float
    dividend_next_year: float
    gordon_growth_value: float
    dividend_discount_value: float
    implied_cost_of_equity: float
    implied_growth_rate: float
    pe_ratio: float
    pb_ratio: float
    ps_ratio: float
    ev_ebitda: float
    dividend_yield: float
    earnings_yield: float
    free_cash_flow_yield: float
    intrinsic_value: float
    market_price: float
    margin_of_safety: float
    sector_pe_ratio: float


class EquityDiagnosticsResponse(BaseModel):
    symbol: str
    valuation_status: str
    profitability_quality: str
    balance_sheet_quality: str
    strengths: list[str]
    risks: list[str]
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
