from __future__ import annotations

from typing import Any


def estimate_income_pnl(
    position: dict[str, Any],
    starting_value: float,
    period_days: int,
    include_income: bool,
) -> float:
    if not include_income:
        return 0.0
    dividend_yield = _as_float(position.get("dividend_yield"))
    if dividend_yield is None:
        asset_type = str(position.get("asset_type") or "").lower()
        if "fixed" in asset_type or "bond" in asset_type or "treasury" in asset_type:
            dividend_yield = 0.035
        elif asset_type == "cash":
            dividend_yield = 0.02
        else:
            dividend_yield = 0.008
    return starting_value * dividend_yield * max(period_days, 0) / 365.0


def _as_float(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
