from __future__ import annotations


_DURATION_ASSUMPTIONS = {
    "BND": 6.0,
    "AGG": 6.3,
    "TLT": 17.0,
    "IEF": 7.5,
    "SHY": 1.9,
    "LQD": 8.2,
    "HYG": 3.7,
}


def is_fixed_income(asset_type: str | None, symbol: str | None = None) -> bool:
    normalized_type = (asset_type or "").strip().lower()
    normalized_symbol = (symbol or "").strip().upper()
    return normalized_type in {"fixed_income", "bond", "bonds"} or normalized_symbol in _DURATION_ASSUMPTIONS


def duration_assumption(symbol: str, asset_type: str | None = None) -> tuple[float | None, str]:
    normalized_symbol = symbol.upper()
    if normalized_symbol in _DURATION_ASSUMPTIONS:
        return _DURATION_ASSUMPTIONS[normalized_symbol], "Demo Duration"
    if is_fixed_income(asset_type, symbol):
        return 5.5, "Generic Fixed Income Duration"
    return None, "Not Fixed Income"


def estimate_bond_price_impact_from_duration(
    market_value: float,
    duration: float | None,
    rate_shock_bps: float,
) -> float:
    if duration is None:
        return 0.0
    return -market_value * duration * (rate_shock_bps / 10_000)


def estimate_dv01_loss(
    market_value: float,
    duration: float | None,
    shock_bps: float,
) -> float:
    if duration is None:
        return 0.0
    dv01 = market_value * duration * 0.0001
    return -dv01 * shock_bps
