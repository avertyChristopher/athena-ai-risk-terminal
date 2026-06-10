def calculate_cash_conversion_ratio(
    operating_cash_flow: float | None,
    net_income: float | None,
) -> float | None:
    return _safe_divide(operating_cash_flow, net_income)


def calculate_accruals_ratio(
    net_income: float | None,
    operating_cash_flow: float | None,
    average_assets: float | None,
) -> float | None:
    if net_income is None or operating_cash_flow is None or average_assets in (None, 0):
        return None
    return (net_income - operating_cash_flow) / average_assets


def calculate_fcf_conversion_ratio(
    free_cash_flow: float | None,
    net_income: float | None,
) -> float | None:
    return _safe_divide(free_cash_flow, net_income)


def compare_net_income_to_operating_cash_flow(
    net_income: float | None,
    operating_cash_flow: float | None,
) -> str:
    ratio = calculate_cash_conversion_ratio(operating_cash_flow, net_income)
    if ratio is None:
        return "Insufficient cash flow inputs"
    if ratio >= 1.0:
        return "Operating cash flow covers reported earnings"
    if ratio >= 0.75:
        return "Cash conversion is acceptable but worth monitoring"
    return "Operating cash flow lags reported earnings"


def classify_earnings_quality(
    cash_conversion_ratio: float | None,
    accruals_ratio: float | None,
    fcf_conversion_ratio: float | None,
) -> str:
    if cash_conversion_ratio is None or accruals_ratio is None or fcf_conversion_ratio is None:
        return "Insufficient data"
    if cash_conversion_ratio >= 1 and accruals_ratio <= 0 and fcf_conversion_ratio >= 0.75:
        return "High earnings quality"
    if cash_conversion_ratio >= 0.75 and accruals_ratio <= 0.10:
        return "Acceptable earnings quality"
    return "Earnings quality review required"


def create_earnings_quality_warnings(
    cash_conversion_ratio: float | None,
    accruals_ratio: float | None,
    fcf_conversion_ratio: float | None,
) -> list[str]:
    warnings = []
    if cash_conversion_ratio is None:
        warnings.append("Operating cash flow or net income is missing.")
    elif cash_conversion_ratio < 0.75:
        warnings.append("Operating cash flow is low relative to net income.")
    if accruals_ratio is None:
        warnings.append("Accruals ratio cannot be calculated.")
    elif accruals_ratio > 0.10:
        warnings.append("Positive accruals are elevated relative to assets.")
    if fcf_conversion_ratio is None:
        warnings.append("Free cash flow conversion cannot be calculated.")
    elif fcf_conversion_ratio < 0.50:
        warnings.append("Free cash flow conversion is weak.")
    return warnings


def _safe_divide(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator in (None, 0):
        return None
    return numerator / denominator
