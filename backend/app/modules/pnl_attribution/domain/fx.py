from __future__ import annotations

from app.modules.pnl_attribution.schemas import FxEffect, PositionPnlContribution


def estimate_fx_effects(
    positions: list[PositionPnlContribution],
    base_currency: str,
    include_fx: bool,
) -> tuple[float, list[FxEffect], list[str]]:
    warnings: list[str] = []
    if not include_fx:
        return 0.0, [], warnings

    effects: list[FxEffect] = []
    total_fx = 0.0
    currencies = sorted({position.currency for position in positions if position.currency != base_currency})
    for currency in currencies:
        local_pnl = sum(position.price_pnl + position.income_pnl for position in positions if position.currency == currency)
        fx_translation = local_pnl * _demo_fx_move(currency)
        total_fx += fx_translation
        effects.append(
            FxEffect(
                currency=currency,
                base_currency=base_currency,
                local_currency_pnl=local_pnl,
                fx_translation_pnl=fx_translation,
                fx_data_source="deterministic_demo_fx_assumption",
            ),
        )
    if currencies:
        warnings.append("FX attribution uses deterministic demo FX assumptions, not live FX history.")
    return total_fx, effects, warnings


def _demo_fx_move(currency: str) -> float:
    return {
        "CAD": 0.004,
        "EUR": 0.006,
        "GBP": 0.005,
        "JPY": -0.003,
    }.get(currency.upper(), 0.002)
