def calculate_gross_margin(gross_profit: float, revenue: float) -> float:
    _validate_positive(revenue, "revenue")
    return gross_profit / revenue


def calculate_operating_margin(operating_income: float, revenue: float) -> float:
    _validate_positive(revenue, "revenue")
    return operating_income / revenue


def calculate_net_margin(net_income: float, revenue: float) -> float:
    _validate_positive(revenue, "revenue")
    return net_income / revenue


def calculate_roe(net_income: float, total_equity: float) -> float:
    _validate_positive(total_equity, "total_equity")
    return net_income / total_equity


def calculate_roa(net_income: float, total_assets: float) -> float:
    _validate_positive(total_assets, "total_assets")
    return net_income / total_assets


def calculate_debt_to_equity(total_debt: float, total_equity: float) -> float:
    _validate_non_negative(total_debt, "total_debt")
    _validate_positive(total_equity, "total_equity")
    return total_debt / total_equity


def calculate_current_ratio(
    current_assets: float,
    current_liabilities: float,
) -> float:
    _validate_positive(current_liabilities, "current_liabilities")
    return current_assets / current_liabilities


def calculate_quick_ratio(
    cash_and_equivalents: float,
    receivables: float,
    marketable_securities: float,
    current_liabilities: float,
) -> float:
    _validate_positive(current_liabilities, "current_liabilities")
    quick_assets = cash_and_equivalents + receivables + marketable_securities
    return quick_assets / current_liabilities


def calculate_interest_coverage(
    operating_income: float,
    interest_expense: float,
) -> float:
    _validate_positive(interest_expense, "interest_expense")
    return operating_income / interest_expense


def calculate_dividend_payout_ratio(
    dividend_per_share: float,
    earnings_per_share: float,
) -> float:
    _validate_non_negative(dividend_per_share, "dividend_per_share")
    _validate_positive(earnings_per_share, "earnings_per_share")
    return dividend_per_share / earnings_per_share


def calculate_retention_ratio(dividend_payout_ratio: float) -> float:
    if dividend_payout_ratio < 0:
        raise ValueError("dividend_payout_ratio must be non-negative.")
    return 1.0 - dividend_payout_ratio


def calculate_sustainable_growth_rate(
    return_on_equity: float,
    retention_ratio: float,
) -> float:
    return return_on_equity * retention_ratio


def _validate_positive(value: float, field_name: str) -> None:
    if value <= 0:
        raise ValueError(f"{field_name} must be positive.")


def _validate_non_negative(value: float, field_name: str) -> None:
    if value < 0:
        raise ValueError(f"{field_name} must be non-negative.")
