from __future__ import annotations

from app.modules.pnl_attribution.schemas import OptionsEffect, PositionPnlContribution


def estimate_options_effects(
    positions: list[PositionPnlContribution],
    include_options: bool,
) -> tuple[OptionsEffect, list[str]]:
    warnings: list[str] = []
    if not include_options:
        return _empty_effect("Options P&L attribution disabled by request."), warnings

    option_positions = [
        position
        for position in positions
        if "option" in position.asset_type.lower() or "option" in position.asset_class.lower()
    ]
    if not option_positions:
        return OptionsEffect(
            status="prepared",
            delta_contribution=0.0,
            gamma_contribution=0.0,
            vega_contribution=0.0,
            theta_contribution=0.0,
            rho_contribution=0.0,
            residual_pnl=0.0,
            notes=[
                "No option positions detected.",
                "Options Pricing Lab ready for future P&L attribution.",
            ],
        ), warnings

    total_pnl = sum(position.total_pnl for position in option_positions)
    effect = OptionsEffect(
        status="demo_estimate",
        delta_contribution=total_pnl * 0.55,
        gamma_contribution=total_pnl * 0.12,
        vega_contribution=total_pnl * 0.18,
        theta_contribution=total_pnl * -0.08,
        rho_contribution=total_pnl * 0.03,
        residual_pnl=total_pnl * 0.20,
        notes=["Greeks attribution uses deterministic demo splits until option position payloads are persisted."],
    )
    warnings.append("Options Greeks P&L uses demo factor split for option-like holdings.")
    return effect, warnings


def _empty_effect(note: str) -> OptionsEffect:
    return OptionsEffect(
        status="disabled",
        delta_contribution=0.0,
        gamma_contribution=0.0,
        vega_contribution=0.0,
        theta_contribution=0.0,
        rho_contribution=0.0,
        residual_pnl=0.0,
        notes=[note],
    )
