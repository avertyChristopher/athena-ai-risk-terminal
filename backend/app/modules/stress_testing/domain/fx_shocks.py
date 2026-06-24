from __future__ import annotations


def apply_currency_shock(
    position_currency: str | None,
    base_currency: str,
    fx_shock: float,
) -> tuple[float, str | None]:
    if not position_currency:
        return 0.0, "Missing currency metadata; no FX translation shock applied."
    if position_currency.upper() == base_currency.upper():
        return 0.0, None
    return -float(fx_shock), None


def estimate_currency_translation_impact(
    market_value: float,
    position_currency: str | None,
    base_currency: str,
    fx_shock: float,
) -> float:
    shock, _ = apply_currency_shock(position_currency, base_currency, fx_shock)
    return market_value * shock
