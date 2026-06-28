from __future__ import annotations

from app.modules.reconciliation.schemas import BreakSeverity


def classify_amount_severity(
    difference: float,
    tolerance: float,
    *,
    high_multiple: float = 5.0,
    critical_multiple: float = 15.0,
    critical_absolute: float | None = None,
) -> BreakSeverity:
    magnitude = abs(difference)
    if critical_absolute is not None and magnitude >= critical_absolute:
        return "critical"
    if tolerance <= 0:
        return "high" if magnitude else "low"
    ratio = magnitude / tolerance
    if ratio >= critical_multiple:
        return "critical"
    if ratio >= high_multiple:
        return "high"
    if ratio > 1.0:
        return "medium"
    return "low"


def classify_position_severity(
    quantity_difference: float,
    market_value_difference: float,
    market_value_tolerance: float,
) -> BreakSeverity:
    if abs(market_value_difference) >= max(market_value_tolerance * 15.0, 25000.0):
        return "critical"
    if abs(quantity_difference) > 0 and abs(market_value_difference) >= market_value_tolerance * 5.0:
        return "high"
    if abs(quantity_difference) > 0:
        return "medium"
    return classify_amount_severity(market_value_difference, market_value_tolerance)


def classify_price_severity(price_difference_bps: float, tolerance_bps: float, stale: bool = False) -> BreakSeverity:
    if stale and abs(price_difference_bps) > tolerance_bps:
        return "medium"
    if stale:
        return "low"
    return classify_amount_severity(price_difference_bps, tolerance_bps, high_multiple=6.0, critical_multiple=25.0)
