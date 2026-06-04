def calculate_gross_margin(
    gross_profit: float | None,
    revenue: float | None,
) -> float | None:
    return _safe_divide(gross_profit, revenue)


def calculate_operating_margin(
    operating_income: float | None,
    revenue: float | None,
) -> float | None:
    return _safe_divide(operating_income, revenue)


def calculate_ebit_margin(ebit: float | None, revenue: float | None) -> float | None:
    return _safe_divide(ebit, revenue)


def calculate_ebitda_margin(
    ebitda: float | None,
    revenue: float | None,
) -> float | None:
    return _safe_divide(ebitda, revenue)


def calculate_net_margin(
    net_income: float | None,
    revenue: float | None,
) -> float | None:
    return _safe_divide(net_income, revenue)


def calculate_roe(
    net_income: float | None,
    total_equity: float | None,
) -> float | None:
    return _safe_divide(net_income, total_equity)


def calculate_roa(
    net_income: float | None,
    total_assets: float | None,
) -> float | None:
    return _safe_divide(net_income, total_assets)


def calculate_roic(
    net_operating_profit_after_tax: float | None,
    invested_capital: float | None,
) -> float | None:
    return _safe_divide(net_operating_profit_after_tax, invested_capital)


def calculate_debt_to_equity(
    total_debt: float | None,
    total_equity: float | None,
) -> float | None:
    if total_debt is not None:
        _validate_non_negative(total_debt, "total_debt")
    return _safe_divide(total_debt, total_equity)


def calculate_debt_to_assets(
    total_debt: float | None,
    total_assets: float | None,
) -> float | None:
    if total_debt is not None:
        _validate_non_negative(total_debt, "total_debt")
    return _safe_divide(total_debt, total_assets)


def calculate_net_debt(
    total_debt: float | None,
    cash_and_equivalents: float | None,
) -> float | None:
    if total_debt is None or cash_and_equivalents is None:
        return None
    return total_debt - cash_and_equivalents


def calculate_net_debt_to_ebitda(
    total_debt: float | None,
    cash_and_equivalents: float | None,
    ebitda: float | None,
) -> float | None:
    return _safe_divide(calculate_net_debt(total_debt, cash_and_equivalents), ebitda)


def calculate_current_ratio(
    current_assets: float | None,
    current_liabilities: float | None,
) -> float | None:
    return _safe_divide(current_assets, current_liabilities)


def calculate_quick_ratio(
    cash_and_equivalents: float | None,
    receivables: float | None,
    marketable_securities: float | None,
    current_liabilities: float | None,
) -> float | None:
    if (
        cash_and_equivalents is None
        or receivables is None
        or marketable_securities is None
    ):
        return None
    quick_assets = cash_and_equivalents + receivables + marketable_securities
    return _safe_divide(quick_assets, current_liabilities)


def calculate_interest_coverage(
    operating_income: float | None,
    interest_expense: float | None,
) -> float | None:
    return _safe_divide(operating_income, interest_expense)


def calculate_asset_turnover(
    revenue: float | None,
    average_total_assets: float | None,
) -> float | None:
    return _safe_divide(revenue, average_total_assets)


def calculate_receivables_turnover(
    revenue: float | None,
    average_receivables: float | None,
) -> float | None:
    return _safe_divide(revenue, average_receivables)


def calculate_inventory_turnover(
    cost_of_goods_sold: float | None,
    average_inventory: float | None,
) -> float | None:
    return _safe_divide(cost_of_goods_sold, average_inventory)


def calculate_free_cash_flow_margin(
    free_cash_flow: float | None,
    revenue: float | None,
) -> float | None:
    return _safe_divide(free_cash_flow, revenue)


def calculate_dividend_payout_ratio(
    dividend_per_share: float | None,
    earnings_per_share: float | None,
) -> float | None:
    if dividend_per_share is not None:
        _validate_non_negative(dividend_per_share, "dividend_per_share")
    return _safe_divide(dividend_per_share, earnings_per_share)


def calculate_retention_ratio(dividend_payout_ratio: float | None) -> float | None:
    if dividend_payout_ratio is None:
        return None
    if dividend_payout_ratio < 0:
        raise ValueError("dividend_payout_ratio must be non-negative.")
    return 1.0 - dividend_payout_ratio


def calculate_sustainable_growth_rate(
    return_on_equity: float | None,
    retention_ratio: float | None,
) -> float | None:
    if return_on_equity is None or retention_ratio is None:
        return None
    return return_on_equity * retention_ratio


def _safe_divide(
    numerator: float | None,
    denominator: float | None,
) -> float | None:
    if numerator is None or denominator in (None, 0):
        return None
    return numerator / denominator


def _validate_positive(value: float, field_name: str) -> None:
    if value <= 0:
        raise ValueError(f"{field_name} must be positive.")


def _validate_non_negative(value: float, field_name: str) -> None:
    if value < 0:
        raise ValueError(f"{field_name} must be non-negative.")
