from __future__ import annotations


def apply_volatility_shock(base_volatility: float, volatility_shock: float) -> float:
    return max(base_volatility * (1.0 + volatility_shock), 0.0)


def estimate_stressed_volatility(
    base_volatility: float,
    volatility_shock: float,
    loss_percent: float,
) -> float:
    loss_amplifier = max(loss_percent, 0.0) * 0.35
    return apply_volatility_shock(base_volatility, volatility_shock) + loss_amplifier
