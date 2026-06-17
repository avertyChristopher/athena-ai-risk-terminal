from typing import Any


DEFAULT_STRESS_SHOCKS = {
    "equity_market_shock": -0.10,
    "technology_sector_shock": -0.15,
    "interest_rate_shock": -0.05,
    "largest_holding_shock": -0.20,
}


def run_stress_scenarios(
    decorated_positions: list[dict[str, Any]],
    total_value: float,
    shock_overrides: dict[str, float] | None = None,
) -> list[dict[str, object]]:
    shocks = {
        **DEFAULT_STRESS_SHOCKS,
        **{
            key: value
            for key, value in (shock_overrides or {}).items()
            if key in DEFAULT_STRESS_SHOCKS and value is not None
        },
    }
    scenarios = [
        {
            "name": f"Equity market shock {_format_shock_label(shocks['equity_market_shock'])}",
            "explanation": "Equity and equity ETF positions are shocked lower to estimate market beta vulnerability.",
            "shock": lambda positions: _equity_market_shock(
                positions,
                shocks["equity_market_shock"],
            ),
        },
        {
            "name": f"Technology sector shock {_format_shock_label(shocks['technology_sector_shock'])}",
            "explanation": "Technology holdings are shocked to isolate sector concentration risk.",
            "shock": lambda positions: _technology_sector_shock(
                positions,
                shocks["technology_sector_shock"],
            ),
        },
        {
            "name": f"Interest rate shock: bonds {_format_shock_label(shocks['interest_rate_shock'])}",
            "explanation": "Fixed-income and bond-like exposures are shocked lower under a rate selloff.",
            "shock": lambda positions: _interest_rate_shock(
                positions,
                shocks["interest_rate_shock"],
            ),
        },
        {
            "name": "Broad risk-off scenario",
            "explanation": "Risk assets sell off together while bonds decline modestly.",
            "shock": _risk_off_shock,
        },
        {
            "name": f"Single-name shock: largest holding {_format_shock_label(shocks['largest_holding_shock'])}",
            "explanation": "The largest holding is shocked lower to estimate issuer concentration vulnerability.",
            "shock": lambda positions: _largest_holding_shock(
                positions,
                shocks["largest_holding_shock"],
            ),
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
    shock: float,
) -> dict[str, float]:
    return {
        str(position["symbol"]): float(position["portfolio_weight"])
        * (shock if str(position["asset_type"]).lower() in {"equity", "etf"} else 0.0)
        for position in decorated_positions
    }


def _technology_sector_shock(
    decorated_positions: list[dict[str, Any]],
    shock: float,
) -> dict[str, float]:
    return {
        str(position["symbol"]): float(position["portfolio_weight"])
        * (shock if str(position["sector"]).lower() == "technology" else 0.0)
        for position in decorated_positions
    }


def _interest_rate_shock(
    decorated_positions: list[dict[str, Any]],
    shock: float,
) -> dict[str, float]:
    return {
        str(position["symbol"]): float(position["portfolio_weight"])
        * (
            shock
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
    shock: float,
) -> dict[str, float]:
    largest = max(
        decorated_positions,
        key=lambda position: float(position["portfolio_weight"]),
        default=None,
    )
    return {
        str(position["symbol"]): (
            float(position["portfolio_weight"]) * shock
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


def _format_shock_label(value: float) -> str:
    return f"{value:.0%}"
