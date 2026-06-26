from __future__ import annotations

from app.modules.stress_testing.domain.credit_shocks import apply_credit_spread_shock
from app.modules.stress_testing.domain.equity_shocks import combined_equity_shock
from app.modules.stress_testing.domain.fx_shocks import apply_currency_shock
from app.modules.stress_testing.domain.rates_shocks import (
    duration_assumption,
    estimate_bond_price_impact_from_duration,
    estimate_dv01_loss,
    is_fixed_income,
)


def calculate_position_market_value(position: dict[str, object]) -> float:
    return float(position.get("quantity", 0.0)) * float(position.get("current_price", 0.0))


def calculate_dollar_loss(base_value: float, stressed_value: float) -> float:
    return base_value - stressed_value


def calculate_percent_loss(base_value: float, stressed_value: float) -> float:
    if base_value <= 0:
        return 0.0
    return calculate_dollar_loss(base_value, stressed_value) / base_value


def calculate_contribution_to_loss(position_loss: float, total_loss: float) -> float:
    if total_loss <= 0:
        return 0.0
    return position_loss / total_loss


def _liquidity_haircut(
    weight: float,
    liquidity_multiplier: float,
) -> float:
    if liquidity_multiplier <= 1.0:
        return 0.0
    concentration_excess = max(weight - 0.10, 0.0)
    return -concentration_excess * 0.05 * liquidity_multiplier


def calculate_position_stress_value(
    position: dict[str, object],
    scenario: dict[str, object],
    portfolio_base_currency: str,
    portfolio_value: float,
) -> dict[str, object]:
    symbol = str(position.get("symbol", "")).upper()
    asset_type = str(position.get("asset_type", ""))
    sector = str(position.get("sector", ""))
    currency = str(position.get("currency", portfolio_base_currency))
    base_value = calculate_position_market_value(position)
    weight = base_value / portfolio_value if portfolio_value > 0 else 0.0

    asset_shock, shock_source = combined_equity_shock(
        symbol,
        sector,
        asset_type,
        dict(scenario.get("symbol_shocks") or {}),
        dict(scenario.get("sector_shocks") or {}),
        dict(scenario.get("asset_class_shocks") or {}),
    )
    fx_shock, fx_warning = apply_currency_shock(
        currency,
        portfolio_base_currency,
        float(scenario.get("fx_shock", 0.0)),
    )
    if position.get("duration_assumption") is not None:
        duration = float(position["duration_assumption"])
        duration_source = "Demo Duration"
    else:
        duration, duration_source = duration_assumption(symbol, asset_type)
    rate_impact = estimate_bond_price_impact_from_duration(
        base_value,
        duration,
        float(scenario.get("rate_shock_bps", 0.0)),
    )
    credit_impact = apply_credit_spread_shock(
        base_value,
        duration if is_fixed_income(asset_type, symbol) else None,
        float(scenario.get("credit_spread_shock_bps", 0.0)),
    )
    liquidity_haircut = _liquidity_haircut(
        weight,
        float(scenario.get("liquidity_multiplier", 1.0)),
    )

    linear_shock = asset_shock + fx_shock + liquidity_haircut
    linear_shock = max(linear_shock, -0.95)
    stressed_value = max(base_value * (1.0 + linear_shock) + rate_impact + credit_impact, 0.0)
    dollar_impact = stressed_value - base_value
    percent_impact = dollar_impact / base_value if base_value > 0 else 0.0

    warnings = []
    if not sector:
        warnings.append("Missing sector metadata; generic asset-class shock applied.")
    if fx_warning:
        warnings.append(fx_warning)
    if is_fixed_income(asset_type, symbol) and duration_source != "Demo Duration":
        warnings.append("Fixed-income duration uses a generic demo assumption.")

    return {
        "position_id": str(position.get("id", "")),
        "symbol": symbol,
        "name": str(position.get("asset_name") or position.get("name") or symbol),
        "asset_class": asset_type,
        "sector": sector or "Unknown",
        "currency": currency,
        "base_value": base_value,
        "shock_applied": linear_shock + (rate_impact + credit_impact) / base_value if base_value > 0 else 0.0,
        "shock_source": shock_source,
        "stressed_value": stressed_value,
        "dollar_impact": dollar_impact,
        "percent_impact": percent_impact,
        "contribution_to_loss": 0.0,
        "duration": duration,
        "dv01": base_value * duration * 0.0001 if duration is not None else None,
        "rate_impact": rate_impact,
        "credit_impact": credit_impact,
        "fx_impact": base_value * fx_shock,
        "liquidity_impact": base_value * liquidity_haircut,
        "data_source": duration_source if duration is not None else "Portfolio + Market Data",
        "warnings": warnings,
    }


def calculate_portfolio_stress_value(
    positions: list[dict[str, object]],
    cash: float,
    scenario: dict[str, object],
    base_currency: str,
) -> dict[str, object]:
    invested_value = sum(calculate_position_market_value(position) for position in positions)
    base_portfolio_value = invested_value + cash
    impacts = [
        calculate_position_stress_value(position, scenario, base_currency, base_portfolio_value)
        for position in positions
    ]
    stressed_positions_value = sum(float(impact["stressed_value"]) for impact in impacts)
    stressed_portfolio_value = stressed_positions_value + cash
    total_loss = calculate_dollar_loss(base_portfolio_value, stressed_portfolio_value)

    for impact in impacts:
        impact["contribution_to_loss"] = calculate_contribution_to_loss(
            max(-float(impact["dollar_impact"]), 0.0),
            total_loss,
        )

    return {
        "base_portfolio_value": base_portfolio_value,
        "stressed_portfolio_value": stressed_portfolio_value,
        "dollar_loss": total_loss,
        "percent_loss": calculate_percent_loss(base_portfolio_value, stressed_portfolio_value),
        "position_impacts": impacts,
        "invested_value": invested_value,
        "cash": cash,
    }
