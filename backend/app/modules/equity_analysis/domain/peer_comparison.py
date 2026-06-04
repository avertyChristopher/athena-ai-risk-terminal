from statistics import median
from typing import Any


def calculate_relative_performance_vs_benchmark(
    asset_return: float | None,
    benchmark_return: float | None,
) -> float | None:
    if asset_return is None or benchmark_return is None:
        return None
    return asset_return - benchmark_return


def compare_profitability_to_peers(
    company_roe: float | None,
    peer_roes: list[float],
) -> str:
    return _compare_to_peer_median(company_roe, peer_roes, higher_is_better=True)


def compare_growth_to_peers(
    company_growth: float | None,
    peer_growth_rates: list[float],
) -> str:
    return _compare_to_peer_median(company_growth, peer_growth_rates, higher_is_better=True)


def compare_valuation_to_peers(
    company_multiple: float | None,
    peer_multiples: list[float],
) -> str:
    return _compare_to_peer_median(
        company_multiple,
        peer_multiples,
        higher_is_better=False,
    )


def create_peer_comparison_summary(
    *,
    company_symbol: str,
    peer_symbols: list[str],
    profitability_signal: str,
    growth_signal: str,
    valuation_signal: str,
) -> str:
    peers = ", ".join(peer_symbols)
    return (
        f"{company_symbol} is compared against {peers}. Profitability screens as "
        f"{profitability_signal.lower()}, growth as {growth_signal.lower()}, and "
        f"valuation as {valuation_signal.lower()} relative to the demo peer group."
    )


def calculate_peer_medians(peer_rows: list[dict[str, Any]]) -> dict[str, float | None]:
    return {
        "pe_ratio": _median_from_rows(peer_rows, "pe_ratio"),
        "pb_ratio": _median_from_rows(peer_rows, "pb_ratio"),
        "ps_ratio": _median_from_rows(peer_rows, "ps_ratio"),
        "ev_ebitda": _median_from_rows(peer_rows, "ev_ebitda"),
        "roe": _median_from_rows(peer_rows, "roe"),
        "revenue_growth": _median_from_rows(peer_rows, "revenue_growth"),
    }


def _compare_to_peer_median(
    company_value: float | None,
    peer_values: list[float],
    *,
    higher_is_better: bool,
) -> str:
    if company_value is None or not peer_values:
        return "Insufficient data"

    peer_median = median(peer_values)
    if company_value >= peer_median * 1.1:
        return "Above peers" if higher_is_better else "Premium to peers"
    if company_value <= peer_median * 0.9:
        return "Below peers" if higher_is_better else "Discount to peers"
    return "In line with peers"


def _median_from_rows(rows: list[dict[str, Any]], field_name: str) -> float | None:
    values = [
        float(row[field_name])
        for row in rows
        if row.get(field_name) is not None
    ]
    return median(values) if values else None
