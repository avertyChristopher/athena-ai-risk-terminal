from app.modules.equity_analysis.domain.valuation import (
    calculate_ev_ebitda,
    calculate_pb_ratio,
    calculate_pe_ratio,
    calculate_ps_ratio,
)


def calculate_forward_pe_ratio(
    price: float,
    forward_eps: float | None,
) -> float | None:
    return calculate_pe_ratio(price, forward_eps)


def calculate_ev(
    market_cap: float,
    total_debt: float | None,
    cash_and_equivalents: float | None,
) -> float:
    return market_cap + (total_debt or 0.0) - (cash_and_equivalents or 0.0)


def calculate_ev_sales(enterprise_value: float, revenue: float | None) -> float | None:
    if not revenue:
        return None
    return enterprise_value / revenue


def calculate_peg_ratio(
    pe_ratio: float | None,
    eps_growth_rate: float | None,
) -> float | None:
    if pe_ratio is None or not eps_growth_rate:
        return None
    return pe_ratio / (eps_growth_rate * 100)


def classify_multiple_level(
    multiple: float | None,
    peer_median: float | None,
) -> str:
    if multiple is None or peer_median is None:
        return "Insufficient data"
    if multiple >= peer_median * 1.25:
        return "Premium"
    if multiple <= peer_median * 0.75:
        return "Discount"
    return "In line"


def compare_multiple_to_peer_median(
    multiple: float | None,
    peer_median: float | None,
) -> float | None:
    if multiple is None or not peer_median:
        return None
    return (multiple / peer_median) - 1.0


__all__ = [
    "calculate_ev",
    "calculate_ev_ebitda",
    "calculate_ev_sales",
    "calculate_forward_pe_ratio",
    "calculate_pb_ratio",
    "calculate_pe_ratio",
    "calculate_peg_ratio",
    "calculate_ps_ratio",
    "classify_multiple_level",
    "compare_multiple_to_peer_median",
]
