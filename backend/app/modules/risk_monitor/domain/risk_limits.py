from typing import Any

DEFAULT_RISK_LIMITS = {
    "max_single_position_weight": 0.25,
    "max_sector_exposure": 0.50,
    "max_asset_type_exposure": 0.80,
    "minimum_cash_reserve": 0.05,
    "max_top_3_concentration": 0.65,
    "max_portfolio_volatility": 0.20,
    "max_var_95": 0.03,
    "max_cvar_95": 0.05,
    "max_drawdown": 0.15,
    "max_tracking_error": 0.08,
    "max_active_exposure": 0.70,
}


def evaluate_limit_breaches(
    *,
    decorated_positions: list[dict[str, Any]],
    sector_exposures: dict[str, float],
    asset_type_exposures: dict[str, float],
    cash_weight: float,
    top_3_weight: float,
    volatility: float,
    var_95: float,
    cvar_95: float,
    max_drawdown: float,
    tracking_error: float | None,
    active_exposure: float,
) -> list[dict[str, object]]:
    breaches: list[dict[str, object]] = []
    for position in decorated_positions:
        weight = float(position["invested_weight"])
        if weight > DEFAULT_RISK_LIMITS["max_single_position_weight"]:
            breaches.append(
                _breach(
                    "Max single position weight",
                    "Concentration",
                    weight,
                    DEFAULT_RISK_LIMITS["max_single_position_weight"],
                    f"{position['symbol']} weight is {weight:.1%}, above the 25% single-position limit.",
                    "Trim the position or rebalance into broader diversified exposure.",
                ),
            )

    for sector, weight in sector_exposures.items():
        if weight > DEFAULT_RISK_LIMITS["max_sector_exposure"]:
            breaches.append(
                _breach(
                    "Max sector exposure",
                    "Concentration",
                    weight,
                    DEFAULT_RISK_LIMITS["max_sector_exposure"],
                    f"{sector} exposure is {weight:.1%}, above the 50% sector limit.",
                    "Reduce sector overweight or add diversifying exposures.",
                ),
            )

    for asset_type, weight in asset_type_exposures.items():
        if weight > DEFAULT_RISK_LIMITS["max_asset_type_exposure"]:
            breaches.append(
                _breach(
                    "Max asset type exposure",
                    "Allocation",
                    weight,
                    DEFAULT_RISK_LIMITS["max_asset_type_exposure"],
                    f"{asset_type} exposure is {weight:.1%}, above the 80% asset-type limit.",
                    "Rebalance toward other asset classes or cash.",
                ),
            )

    if cash_weight < DEFAULT_RISK_LIMITS["minimum_cash_reserve"]:
        breaches.append(
            _cash_breach(cash_weight, DEFAULT_RISK_LIMITS["minimum_cash_reserve"]),
        )

    checks = [
        (
            "Max top 3 concentration",
            "Concentration",
            top_3_weight,
            DEFAULT_RISK_LIMITS["max_top_3_concentration"],
            f"Top 3 holdings concentration is {top_3_weight:.1%}, above the 65% policy limit.",
            "Rebalance the largest holdings to reduce issuer concentration.",
        ),
        (
            "Max portfolio volatility",
            "Market risk",
            volatility,
            DEFAULT_RISK_LIMITS["max_portfolio_volatility"],
            f"Portfolio volatility is {volatility:.1%}, above the 20% surveillance limit.",
            "Reduce high-volatility exposures or add lower-risk assets.",
        ),
        (
            "Max VaR 95%",
            "Downside risk",
            var_95,
            DEFAULT_RISK_LIMITS["max_var_95"],
            f"VaR 95% is {var_95:.1%}, above the 3% limit.",
            "Reduce downside concentration or hedge the portfolio.",
        ),
        (
            "Max CVaR 95%",
            "Downside risk",
            cvar_95,
            DEFAULT_RISK_LIMITS["max_cvar_95"],
            f"CVaR 95% is {cvar_95:.1%}, above the 5% limit.",
            "Review tail-risk drivers and reduce vulnerable positions.",
        ),
        (
            "Max drawdown",
            "Drawdown risk",
            abs(max_drawdown),
            DEFAULT_RISK_LIMITS["max_drawdown"],
            f"Max drawdown is {abs(max_drawdown):.1%}, above the 15% limit.",
            "Lower portfolio beta or add defensive assets.",
        ),
        (
            "Max benchmark active exposure",
            "Benchmark risk",
            active_exposure,
            DEFAULT_RISK_LIMITS["max_active_exposure"],
            f"Active exposure versus benchmark is {active_exposure:.1%}, above the 70% limit.",
            "Review benchmark alignment and active mandate tolerance.",
        ),
    ]

    if tracking_error is not None:
        checks.append(
            (
                "Max tracking error",
                "Benchmark risk",
                tracking_error,
                DEFAULT_RISK_LIMITS["max_tracking_error"],
                f"Tracking error is {tracking_error:.1%}, above the 8% limit.",
                "Reduce active risk or align portfolio weights closer to benchmark exposure.",
            ),
        )

    for rule_name, category, current, limit, explanation, suggested_action in checks:
        if current > limit:
            breaches.append(
                _breach(
                    rule_name,
                    category,
                    current,
                    limit,
                    explanation,
                    suggested_action,
                ),
            )

    return breaches


def _breach(
    rule_name: str,
    category: str,
    current_value: float,
    limit_value: float,
    explanation: str,
    suggested_action: str,
) -> dict[str, object]:
    return {
        "rule_name": rule_name,
        "category": category,
        "current_value": current_value,
        "limit_value": limit_value,
        "severity": _severity_over_limit(current_value, limit_value),
        "explanation": explanation,
        "suggested_action": suggested_action,
    }


def _cash_breach(current_value: float, limit_value: float) -> dict[str, object]:
    shortfall_ratio = (limit_value - current_value) / limit_value if limit_value else 0.0
    if shortfall_ratio >= 0.75:
        severity = "critical"
    elif shortfall_ratio >= 0.50:
        severity = "high"
    elif shortfall_ratio >= 0.25:
        severity = "medium"
    else:
        severity = "low"
    return {
        "rule_name": "Minimum cash reserve",
        "category": "Liquidity",
        "current_value": current_value,
        "limit_value": limit_value,
        "severity": severity,
        "explanation": f"Cash reserve is {current_value:.1%}, below the 5% minimum.",
        "suggested_action": "Raise liquidity or reduce new buy orders until cash is rebuilt.",
    }


def _severity_over_limit(current_value: float, limit_value: float) -> str:
    ratio = current_value / limit_value if limit_value else 0.0
    if ratio >= 1.75:
        return "critical"
    if ratio >= 1.40:
        return "high"
    if ratio >= 1.15:
        return "medium"
    return "low"
