from __future__ import annotations


def apply_credit_spread_shock(
    market_value: float,
    duration: float | None,
    credit_spread_shock_bps: float,
) -> float:
    if duration is None:
        return 0.0
    return -market_value * duration * (credit_spread_shock_bps / 10_000)
