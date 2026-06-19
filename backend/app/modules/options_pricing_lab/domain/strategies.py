from app.modules.options_pricing_lab.domain.payoff import option_payoff, option_profit


def strategy_payoff_table(
    underlying_price: float,
    legs: list[dict[str, float | int | str]],
    contract_size: int = 100,
) -> list[dict[str, float]]:
    scenario_prices = [
        underlying_price * value
        for value in [0.70, 0.80, 0.90, 1.0, 1.10, 1.20, 1.30]
    ]
    return [
        {
            "underlying_price": scenario_price,
            "payoff": sum(_leg_payoff(scenario_price, leg) for leg in legs)
            * contract_size,
            "profit": sum(_leg_profit(scenario_price, leg) for leg in legs)
            * contract_size,
        }
        for scenario_price in scenario_prices
    ]


def strategy_summary(
    strategy_type: str,
    underlying_price: float,
    legs: list[dict[str, float | int | str]],
    contract_size: int = 100,
) -> dict[str, object]:
    table = strategy_payoff_table(underlying_price, legs, contract_size)
    profits = [float(row["profit"]) for row in table]
    net_premium = sum(
        float(leg.get("premium", 0.0))
        * int(leg.get("quantity", 1))
        * (1 if str(leg.get("side")) == "long" else -1)
        * contract_size
        for leg in legs
    )
    return {
        "strategy_type": strategy_type,
        "net_premium": net_premium,
        "max_profit": max(profits) if profits else None,
        "max_loss": abs(min(profits)) if profits and min(profits) < 0 else 0.0,
        "breakeven_points": _estimate_breakevens(table),
        "payoff_table": table,
        "risk_profile": _risk_profile(strategy_type),
    }


def _leg_payoff(
    scenario_price: float,
    leg: dict[str, float | int | str],
) -> float:
    return option_payoff(
        scenario_price,
        float(leg["strike"]),
        str(leg["option_type"]),
        str(leg["side"]),
    ) * int(leg.get("quantity", 1))


def _leg_profit(
    scenario_price: float,
    leg: dict[str, float | int | str],
) -> float:
    return option_profit(
        _leg_payoff(scenario_price, {**leg, "quantity": 1}),
        float(leg.get("premium", 0.0)),
        str(leg["side"]),
    ) * int(leg.get("quantity", 1))


def _estimate_breakevens(table: list[dict[str, float]]) -> list[float]:
    breakevens = []
    for left, right in zip(table, table[1:]):
        left_profit = float(left["profit"])
        right_profit = float(right["profit"])
        if left_profit == 0:
            breakevens.append(float(left["underlying_price"]))
        if left_profit * right_profit < 0:
            span = float(right["underlying_price"]) - float(left["underlying_price"])
            fraction = abs(left_profit) / (abs(left_profit) + abs(right_profit))
            breakevens.append(float(left["underlying_price"]) + span * fraction)
    return breakevens


def _risk_profile(strategy_type: str) -> str:
    profiles = {
        "covered_call": "Generates premium but caps upside on an existing long stock position.",
        "protective_put": "Pays premium to reduce downside risk on an existing position.",
        "long_straddle": "Benefits from large moves in either direction and higher volatility.",
        "long_strangle": "Lower-cost volatility strategy requiring a larger underlying move.",
        "bull_call_spread": "Defined-risk bullish strategy with capped upside.",
        "bear_put_spread": "Defined-risk bearish strategy with capped profit.",
        "collar": "Combines downside protection with upside cap.",
        "cash_secured_put": "Earns premium while accepting downside purchase obligation.",
    }
    return profiles.get(strategy_type, "Deterministic educational strategy payoff.")
