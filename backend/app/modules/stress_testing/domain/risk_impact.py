from __future__ import annotations

from app.modules.stress_testing.domain.volatility_shocks import estimate_stressed_volatility


def _z_score(confidence_level: float) -> float:
    if confidence_level >= 0.995:
        return 2.58
    if confidence_level >= 0.99:
        return 2.33
    if confidence_level >= 0.975:
        return 1.96
    return 1.65


def estimate_stressed_var(
    portfolio_value: float,
    volatility: float,
    confidence_level: float,
) -> float:
    return portfolio_value * volatility / (252**0.5) * _z_score(confidence_level)


def estimate_stressed_cvar(var_value: float, confidence_level: float) -> float:
    tail_multiplier = 1.45 if confidence_level <= 0.95 else 1.35
    return var_value * tail_multiplier


def estimate_stress_severity(
    percent_loss: float,
    dollar_loss: float,
    breached_limits: int,
    var_deterioration: float,
    largest_loss_contribution: float,
    liquidity_stress: bool,
) -> dict[str, object]:
    loss_score = min(max(percent_loss, 0.0) / 0.35 * 70.0, 70.0)
    breach_score = min(breached_limits * 6.0, 18.0)
    var_score = min(max(var_deterioration, 0.0) * 12.0, 8.0)
    concentration_score = 7.0 if largest_loss_contribution >= 0.45 else 0.0
    liquidity_score = 5.0 if liquidity_stress else 0.0
    score = round(min(loss_score + breach_score + var_score + concentration_score + liquidity_score, 100.0))

    if percent_loss < 0.02:
        label = "Low"
    elif percent_loss < 0.05:
        label = "Moderate"
    elif percent_loss < 0.10:
        label = "Elevated"
    elif percent_loss < 0.20:
        label = "High"
    elif percent_loss < 0.35:
        label = "Severe"
    else:
        label = "Critical"

    drivers = []
    if percent_loss >= 0.05:
        drivers.append(f"Estimated portfolio loss of {percent_loss:.1%}.")
    if dollar_loss > 0:
        drivers.append(f"Estimated dollar loss of {dollar_loss:,.0f}.")
    if largest_loss_contribution >= 0.35:
        drivers.append("Losses are concentrated in a small number of positions.")
    if breached_limits:
        drivers.append(f"{breached_limits} stress limits breached.")
    if liquidity_stress:
        drivers.append("Liquidity multiplier increases stressed losses.")

    return {"severity": label, "score": score, "main_drivers": drivers or ["Stress impact remains contained."]}


def detect_stress_limit_breaches(
    percent_loss: float,
    sector_impacts: list[dict[str, object]],
    asset_class_impacts: list[dict[str, object]],
    fixed_income_loss_percent: float,
    liquidity_multiplier: float,
) -> list[dict[str, object]]:
    breaches = []
    if percent_loss > 0.10:
        breaches.append(
            {
                "rule_name": "Stress loss limit",
                "category": "Portfolio",
                "current_value": percent_loss,
                "limit_value": 0.10,
                "severity": "High" if percent_loss < 0.20 else "Severe",
                "explanation": "Portfolio stress loss exceeds the 10% policy threshold.",
                "suggested_action": "Review hedge, cash buffer and concentration controls.",
            }
        )
    for row in sector_impacts[:1]:
        if float(row["loss_contribution"]) > 0.50:
            breaches.append(
                {
                    "rule_name": "Sector loss concentration",
                    "category": "Concentration",
                    "current_value": float(row["loss_contribution"]),
                    "limit_value": 0.50,
                    "severity": "Elevated",
                    "explanation": "One sector explains more than half of the stressed loss.",
                    "suggested_action": "Review sector diversification and drawdown hedges.",
                }
            )
    if fixed_income_loss_percent > 0.05:
        breaches.append(
            {
                "rule_name": "Fixed-income duration stress",
                "category": "Rates",
                "current_value": fixed_income_loss_percent,
                "limit_value": 0.05,
                "severity": "Elevated",
                "explanation": "Fixed-income rate or credit stress exceeds 5% of fixed-income exposure.",
                "suggested_action": "Review duration exposure and credit spread sensitivity.",
            }
        )
    if liquidity_multiplier > 1.5:
        breaches.append(
            {
                "rule_name": "Liquidity stress",
                "category": "Liquidity",
                "current_value": liquidity_multiplier,
                "limit_value": 1.5,
                "severity": "Moderate",
                "explanation": "Liquidity multiplier materially increases concentrated-position haircuts.",
                "suggested_action": "Check position size, average daily volume and exit assumptions.",
            }
        )
    _ = asset_class_impacts
    return breaches


def build_risk_metric_snapshot(
    portfolio_value: float,
    base_volatility: float,
    volatility_shock: float,
    percent_loss: float,
    confidence_level: float,
) -> dict[str, float]:
    stressed_volatility = estimate_stressed_volatility(
        base_volatility,
        volatility_shock,
        percent_loss,
    )
    before_var = estimate_stressed_var(portfolio_value, base_volatility, confidence_level)
    after_var = estimate_stressed_var(portfolio_value, stressed_volatility, confidence_level)
    before_cvar = estimate_stressed_cvar(before_var, confidence_level)
    after_cvar = estimate_stressed_cvar(after_var, confidence_level)
    return {
        "before_volatility": base_volatility,
        "stressed_volatility": stressed_volatility,
        "before_var": before_var,
        "stressed_var": after_var,
        "before_cvar": before_cvar,
        "stressed_cvar": after_cvar,
        "var_deterioration": after_var / before_var - 1.0 if before_var else 0.0,
    }
