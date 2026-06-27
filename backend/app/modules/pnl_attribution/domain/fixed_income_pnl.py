from __future__ import annotations

from typing import Any

from app.modules.pnl_attribution.schemas import FixedIncomeEffect, PositionPnlContribution


def estimate_fixed_income_effects(
    positions: list[PositionPnlContribution],
    raw_positions: list[dict[str, Any]],
    include_rates: bool,
) -> tuple[list[FixedIncomeEffect], list[str]]:
    warnings: list[str] = []
    if not include_rates:
        return [], warnings

    raw_by_symbol = {str(position.get("symbol", "")).upper(): position for position in raw_positions}
    effects: list[FixedIncomeEffect] = []
    for position in positions:
        raw = raw_by_symbol.get(position.symbol.upper(), {})
        if not _is_fixed_income(position.asset_type, position.asset_class):
            continue
        duration = _as_float(raw.get("modified_duration_assumption") or raw.get("duration_assumption"))
        duration_source = "Portfolio Builder duration assumption"
        if duration is None:
            duration = _demo_duration(position.symbol, position.asset_type)
            duration_source = "Demo Duration"
            warnings.append(f"{position.symbol}: Rates Lab payload unavailable; demo duration used.")
        rate_shock_bps = _demo_rate_shock(position.symbol)
        shock_decimal = rate_shock_bps / 10000.0
        duration_effect = -duration * shock_decimal * position.starting_value
        convexity = _demo_convexity(duration)
        convexity_effect = 0.5 * convexity * (shock_decimal**2) * position.starting_value
        estimated_rate_pnl = duration_effect + convexity_effect
        residual = position.total_pnl - estimated_rate_pnl - position.income_pnl
        effects.append(
            FixedIncomeEffect(
                symbol=position.symbol,
                duration_effect=duration_effect,
                convexity_effect=convexity_effect,
                income_effect=position.income_pnl,
                rate_shock_bps=rate_shock_bps,
                estimated_rate_pnl=estimated_rate_pnl,
                residual_pnl=residual,
                duration_source=duration_source,
                limitations=["Duration-based approximation; not a full bond repricing model."],
            ),
        )
    if not effects:
        warnings.append("No fixed-income positions detected for rates P&L attribution.")
    return effects, warnings


def _is_fixed_income(asset_type: str, asset_class: str) -> bool:
    value = f"{asset_type} {asset_class}".lower()
    return any(token in value for token in ["fixed", "bond", "treasury"])


def _demo_duration(symbol: str, asset_type: str) -> float:
    symbol = symbol.upper()
    if symbol == "TLT":
        return 16.0
    if symbol == "IEF":
        return 7.2
    if symbol == "BND":
        return 6.4
    if "treasury" in asset_type.lower():
        return 7.0
    return 5.0


def _demo_rate_shock(symbol: str) -> float:
    if symbol.upper() == "TLT":
        return 18.0
    return 12.0


def _demo_convexity(duration: float) -> float:
    return max(duration * duration * 0.7, 10.0)


def _as_float(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
