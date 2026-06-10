def calculate_net_margin(net_income: float | None, revenue: float | None) -> float | None:
    return _safe_divide(net_income, revenue)


def calculate_asset_turnover(revenue: float | None, average_assets: float | None) -> float | None:
    return _safe_divide(revenue, average_assets)


def calculate_financial_leverage(
    average_assets: float | None,
    average_equity: float | None,
) -> float | None:
    return _safe_divide(average_assets, average_equity)


def calculate_dupont_roe(
    net_margin: float | None,
    asset_turnover: float | None,
    financial_leverage: float | None,
) -> float | None:
    if net_margin is None or asset_turnover is None or financial_leverage is None:
        return None
    return net_margin * asset_turnover * financial_leverage


def calculate_tax_burden(net_income: float | None, pretax_income: float | None) -> float | None:
    return _safe_divide(net_income, pretax_income)


def calculate_interest_burden(pretax_income: float | None, ebit: float | None) -> float | None:
    return _safe_divide(pretax_income, ebit)


def calculate_extended_dupont_roe(
    tax_burden: float | None,
    interest_burden: float | None,
    ebit_margin: float | None,
    asset_turnover: float | None,
    financial_leverage: float | None,
) -> float | None:
    inputs = [tax_burden, interest_burden, ebit_margin, asset_turnover, financial_leverage]
    if any(value is None for value in inputs):
        return None
    result = 1.0
    for value in inputs:
        result *= float(value)
    return result


def explain_dupont_drivers(
    net_margin: float | None,
    asset_turnover: float | None,
    financial_leverage: float | None,
) -> list[str]:
    notes = []
    if net_margin is not None:
        notes.append("Profitability driver is strong." if net_margin >= 0.15 else "Profitability driver is modest.")
    if asset_turnover is not None:
        notes.append("Asset productivity is high." if asset_turnover >= 0.8 else "Asset productivity is moderate.")
    if financial_leverage is not None:
        notes.append("Financial leverage amplifies ROE." if financial_leverage >= 2.0 else "Financial leverage is contained.")
    return notes or ["DuPont drivers require complete margin, turnover and leverage inputs."]


def _safe_divide(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator in (None, 0):
        return None
    return numerator / denominator
