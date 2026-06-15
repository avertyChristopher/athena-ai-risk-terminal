from typing import Any


def run_stress_scenarios(
    decorated_positions: list[dict[str, Any]],
    total_value: float,
) -> list[dict[str, object]]:
    scenarios = [
        {
            "name": "Equity market shock -10%",
            "explanation": "Equity and equity ETF positions are shocked lower to estimate market beta vulnerability.",
            "shock": _equity_market_shock,
        },
        {
            "name": "Technology sector shock -15%",
            "explanation": "Technology holdings are shocked to isolate sector concentration risk.",
            "shock": _technology_sector_shock,
        },
        {
            "name": "Interest rate shock: bonds -5%",
            "explanation": "Fixed-income and bond-like exposures are shocked lower under a rate selloff.",
            "shock": _interest_rate_shock,
        },
        {
            "name": "Broad risk-off scenario",
            "explanation": "Risk assets sell off together while bonds decline modestly.",
            "shock": _risk_off_shock,
        },
        {
            "name": "Single-name shock: largest holding -20%",
            "explanation": "The largest holding is shocked lower to estimate issuer concentration vulnerability.",
            "shock": _largest_holding_shock,
        },
        {
            "name": "Liquidity shock",
            "explanation": "A deterministic liquidity haircut is applied to less defensive holdings.",
            "shock": _liquidity_shock,
        },
    ]
    results = []
    for scenario in scenarios:
        impacts = scenario["shock"](decorated_positions)
        portfolio_impact = sum(impacts.values())
        affected = sorted(impacts.items(), key=lambda item: abs(item[1]), reverse=True)[:3]
        affected_symbols = [symbol for symbol, impact in affected if impact < 0]
        results.append(
            {
                "name": str(scenario["name"]),
                "estimated_impact_percent": portfolio_impact,
                "estimated_loss": total_value * portfolio_impact,
                "most_affected_holdings": affected_symbols,
                "severity": _scenario_severity(portfolio_impact),
                "explanation": str(scenario["explanation"]),
            },
        )
    return results


def _equity_market_shock(
    decorated_positions: list[dict[str, Any]],
) -> dict[str, float]:
    return {
        str(position["symbol"]): float(position["portfolio_weight"])
        * (-0.10 if str(position["asset_type"]).lower() in {"equity", "etf"} else 0.0)
        for position in decorated_positions
    }


def _technology_sector_shock(
    decorated_positions: list[dict[str, Any]],
) -> dict[str, float]:
    return {
        str(position["symbol"]): float(position["portfolio_weight"])
        * (-0.15 if str(position["sector"]).lower() == "technology" else 0.0)
        for position in decorated_positions
    }


def _interest_rate_shock(
    decorated_positions: list[dict[str, Any]],
) -> dict[str, float]:
    return {
        str(position["symbol"]): float(position["portfolio_weight"])
        * (
            -0.05
            if str(position["asset_type"]).lower() in {"fixed_income", "bond"}
            or str(position["sector"]).lower() == "fixed income"
            else 0.0
        )
        for position in decorated_positions
    }


def _risk_off_shock(decorated_positions: list[dict[str, Any]]) -> dict[str, float]:
    impacts = {}
    for position in decorated_positions:
        asset_type = str(position["asset_type"]).lower()
        shock = -0.03
        if asset_type == "equity":
            shock = -0.12
        elif asset_type == "etf":
            shock = -0.09
        elif asset_type in {"fixed_income", "bond"}:
            shock = -0.03
        impacts[str(position["symbol"])] = float(position["portfolio_weight"]) * shock
    return impacts


def _largest_holding_shock(
    decorated_positions: list[dict[str, Any]],
) -> dict[str, float]:
    largest = max(
        decorated_positions,
        key=lambda position: float(position["portfolio_weight"]),
        default=None,
    )
    return {
        str(position["symbol"]): (
            float(position["portfolio_weight"]) * -0.20
            if largest is not None and position["symbol"] == largest["symbol"]
            else 0.0
        )
        for position in decorated_positions
    }


def _liquidity_shock(decorated_positions: list[dict[str, Any]]) -> dict[str, float]:
    return {
        str(position["symbol"]): float(position["portfolio_weight"])
        * (-0.025 if str(position["asset_type"]).lower() in {"equity", "etf"} else -0.01)
        for position in decorated_positions
    }


def _scenario_severity(impact: float) -> str:
    loss = abs(impact)
    if loss >= 0.15:
        return "critical"
    if loss >= 0.10:
        return "high"
    if loss >= 0.05:
        return "medium"
    return "low"
