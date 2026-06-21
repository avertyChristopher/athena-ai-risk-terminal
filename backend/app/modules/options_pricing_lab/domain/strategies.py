from app.modules.options_pricing_lab.domain.payoff import option_payoff, option_profit


def build_predefined_strategy_legs(
    strategy_type: str,
    underlying_price: float,
    contract_size: int = 100,
    quantity: int = 1,
    expiration_days: int = 60,
) -> list[dict[str, float | int | str | None]]:
    strike = round(underlying_price / 5) * 5
    stock = _stock_leg(underlying_price, contract_size * quantity)

    if strategy_type == "covered_call":
        return [
            stock,
            _option_leg("call", "short", strike, expiration_days, quantity, contract_size),
        ]
    if strategy_type == "protective_put":
        return [
            stock,
            _option_leg("put", "long", strike, expiration_days, quantity, contract_size),
        ]
    if strategy_type == "long_straddle":
        return [
            _option_leg("call", "long", strike, expiration_days, quantity, contract_size),
            _option_leg("put", "long", strike, expiration_days, quantity, contract_size),
        ]
    if strategy_type == "long_strangle":
        return [
            _option_leg("put", "long", strike * 0.95, expiration_days, quantity, contract_size),
            _option_leg("call", "long", strike * 1.05, expiration_days, quantity, contract_size),
        ]
    if strategy_type == "bull_call_spread":
        return [
            _option_leg("call", "long", strike, expiration_days, quantity, contract_size),
            _option_leg("call", "short", strike * 1.1, expiration_days, quantity, contract_size),
        ]
    if strategy_type == "bear_put_spread":
        return [
            _option_leg("put", "long", strike, expiration_days, quantity, contract_size),
            _option_leg("put", "short", strike * 0.9, expiration_days, quantity, contract_size),
        ]
    if strategy_type == "collar":
        return [
            stock,
            _option_leg("put", "long", strike * 0.95, expiration_days, quantity, contract_size),
            _option_leg("call", "short", strike * 1.05, expiration_days, quantity, contract_size),
        ]
    if strategy_type == "cash_secured_put":
        return [
            _option_leg("put", "short", strike, expiration_days, quantity, contract_size),
            _cash_leg(strike, quantity, contract_size),
        ]
    raise ValueError(f"Unsupported predefined strategy: {strategy_type}.")


def strategy_payoff_table(
    underlying_price: float,
    legs: list[dict[str, float | int | str | None]],
    contract_size: int = 100,
    scenario_shocks: list[float] | None = None,
) -> list[dict[str, float]]:
    shocks = scenario_shocks or [-0.30, -0.20, -0.10, 0.0, 0.10, 0.20, 0.30]
    scenario_prices = [underlying_price * (1.0 + shock) for shock in shocks]
    return [
        {
            "underlying_price": scenario_price,
            "payoff": sum(
                _leg_payoff(scenario_price, leg, contract_size) for leg in legs
            ),
            "profit": sum(
                _leg_profit(scenario_price, leg, contract_size) for leg in legs
            ),
        }
        for scenario_price in scenario_prices
    ]


def strategy_summary(
    strategy_type: str,
    underlying_price: float,
    legs: list[dict[str, float | int | str | None]],
    contract_size: int = 100,
    predefined: bool = True,
) -> dict[str, object]:
    table = strategy_payoff_table(underlying_price, legs, contract_size)
    net_premium = sum(_leg_net_premium(leg, contract_size) for leg in legs)
    risk = (
        analytical_strategy_risk(
            strategy_type,
            underlying_price,
            legs,
            net_premium,
            contract_size,
        )
        if predefined
        else _unknown_strategy_risk(table)
    )
    return {
        "strategy_type": strategy_type,
        "net_premium": net_premium,
        **risk,
        "payoff_table": table,
        "risk_profile": _risk_profile(strategy_type),
        "stock_leg_included": any(_leg_type(leg) == "stock" for leg in legs),
        "collateral_requirement": _collateral_requirement(legs, contract_size),
    }


def analytical_strategy_risk(
    strategy_type: str,
    underlying_price: float,
    legs: list[dict[str, float | int | str | None]],
    net_premium: float,
    fallback_contract_size: int = 100,
) -> dict[str, object]:
    option_legs = [leg for leg in legs if _leg_type(leg) == "option"]
    multiplier = _position_multiplier(option_legs, fallback_contract_size)
    net_debit_per_share = net_premium / multiplier

    if strategy_type == "covered_call":
        call = _find_option(option_legs, "call", "short")
        strike = _strike(call)
        call_credit = -net_debit_per_share
        return _risk_result(
            _finite((strike - underlying_price + call_credit) * multiplier, "Upside is capped at the short-call strike."),
            _finite(max(underlying_price - call_credit, 0.0) * multiplier, "Stock can fall to zero, partly offset by call premium."),
            [underlying_price - call_credit],
            ["income", "bullish", "limited profit", "large downside risk"],
            ["Downside stock risk remains.", "Upside is capped by the short call."],
        )
    if strategy_type == "protective_put":
        put = _find_option(option_legs, "put", "long")
        strike = _strike(put)
        return _risk_result(
            _unlimited("Long stock retains theoretically unlimited upside."),
            _finite(max(underlying_price - strike + net_debit_per_share, 0.0) * multiplier, "The long put creates a downside floor."),
            [underlying_price + net_debit_per_share],
            ["hedging", "bullish", "limited risk", "unlimited profit"],
            ["Premium cost reduces return.", "Protection is effective below the put strike."],
        )
    if strategy_type == "collar":
        put = _find_option(option_legs, "put", "long")
        call = _find_option(option_legs, "call", "short")
        put_strike = _strike(put)
        call_strike = _strike(call)
        return _risk_result(
            _finite(max(call_strike - underlying_price - net_debit_per_share, 0.0) * multiplier, "The short call caps portfolio upside."),
            _finite(max(underlying_price - put_strike + net_debit_per_share, 0.0) * multiplier, "The long put limits downside loss."),
            [underlying_price + net_debit_per_share],
            ["hedging", "limited risk", "limited profit"],
            ["Downside is floored by the put.", "Upside is capped by the call."],
        )
    if strategy_type == "cash_secured_put":
        put = _find_option(option_legs, "put", "short")
        strike = _strike(put)
        premium_credit = -net_debit_per_share
        return _risk_result(
            _finite(premium_credit * multiplier, "Maximum profit is the premium received."),
            _finite(max(strike - premium_credit, 0.0) * multiplier, "Maximum loss occurs if the underlying falls to zero."),
            [strike - premium_credit],
            ["income", "bullish", "limited profit", "large downside risk"],
            ["Cash collateral must cover assignment at the strike."],
        )
    if strategy_type == "long_straddle":
        strike = _strike(_find_option(option_legs, "call", "long"))
        return _risk_result(
            _unlimited("Upside profit is theoretically unlimited."),
            _finite(net_premium, "Maximum loss is the total premium paid."),
            [strike - net_debit_per_share, strike + net_debit_per_share],
            ["neutral volatility", "limited risk", "unlimited profit"],
            ["The underlying must move beyond either breakeven before expiration."],
        )
    if strategy_type == "long_strangle":
        put_strike = _strike(_find_option(option_legs, "put", "long"))
        call_strike = _strike(_find_option(option_legs, "call", "long"))
        return _risk_result(
            _unlimited("Upside profit is theoretically unlimited."),
            _finite(net_premium, "Maximum loss is the total premium paid."),
            [put_strike - net_debit_per_share, call_strike + net_debit_per_share],
            ["neutral volatility", "limited risk", "unlimited profit"],
            ["A larger move is required than for an equivalent straddle."],
        )
    if strategy_type == "bull_call_spread":
        lower = _strike(_find_option(option_legs, "call", "long"))
        upper = _strike(_find_option(option_legs, "call", "short"))
        return _spread_risk(
            lower,
            upper,
            net_debit_per_share,
            multiplier,
            lower + net_debit_per_share,
            "bullish",
        )
    if strategy_type == "bear_put_spread":
        upper = _strike(_find_option(option_legs, "put", "long"))
        lower = _strike(_find_option(option_legs, "put", "short"))
        return _spread_risk(
            lower,
            upper,
            net_debit_per_share,
            multiplier,
            upper - net_debit_per_share,
            "bearish",
        )
    return _unknown_strategy_risk(strategy_payoff_table(underlying_price, legs, fallback_contract_size))


def _spread_risk(
    lower_strike: float,
    upper_strike: float,
    net_debit_per_share: float,
    multiplier: float,
    breakeven: float,
    profile: str,
) -> dict[str, object]:
    width = upper_strike - lower_strike
    return _risk_result(
        _finite(max(width - net_debit_per_share, 0.0) * multiplier, "Profit is capped by the spread width."),
        _finite(max(net_debit_per_share, 0.0) * multiplier, "Maximum loss is the net premium paid."),
        [breakeven],
        [profile, "limited risk", "limited profit"],
        ["Both maximum profit and maximum loss are defined at entry."],
    )


def _risk_result(
    max_profit: dict[str, float | str | None],
    max_loss: dict[str, float | str | None],
    breakeven_points: list[float],
    payoff_profile: list[str],
    risk_notes: list[str],
) -> dict[str, object]:
    return {
        "max_profit": max_profit,
        "max_loss": max_loss,
        "breakeven_points": [point for point in breakeven_points if point >= 0],
        "payoff_profile": payoff_profile,
        "risk_notes": risk_notes,
    }


def _finite(value: float, explanation: str) -> dict[str, float | str | None]:
    return {"value": max(value, 0.0), "type": "finite", "explanation": explanation}


def _unlimited(explanation: str) -> dict[str, float | str | None]:
    return {"value": None, "type": "unlimited", "explanation": explanation}


def _unknown_strategy_risk(
    table: list[dict[str, float]],
) -> dict[str, object]:
    unknown = {
        "value": None,
        "type": "unknown",
        "explanation": "Analytical extrema are not available for custom legs.",
    }
    return _risk_result(
        unknown,
        unknown.copy(),
        _estimate_breakevens(table),
        ["custom"],
        ["Scenario results are illustrative and do not define theoretical extrema."],
    )


def _find_option(
    legs: list[dict[str, float | int | str | None]],
    option_type: str,
    side: str,
) -> dict[str, float | int | str | None]:
    return next(
        leg
        for leg in legs
        if str(leg.get("option_type")) == option_type and str(leg.get("side")) == side
    )


def _position_multiplier(
    option_legs: list[dict[str, float | int | str | None]],
    fallback_contract_size: int,
) -> float:
    if not option_legs:
        return float(fallback_contract_size)
    reference = option_legs[0]
    return float(
        int(reference.get("contract_size", fallback_contract_size) or fallback_contract_size)
        * int(reference.get("quantity", 1) or 1)
    )


def _leg_payoff(
    scenario_price: float,
    leg: dict[str, float | int | str | None],
    fallback_contract_size: int,
) -> float:
    leg_type = _leg_type(leg)
    side_multiplier = 1.0 if str(leg.get("side", "long")) == "long" else -1.0
    quantity = int(leg.get("quantity", 1) or 1)
    size = int(leg.get("contract_size", fallback_contract_size) or fallback_contract_size)

    if leg_type == "stock":
        initial_price = float(leg.get("underlying_price") or 0.0)
        return side_multiplier * (scenario_price - initial_price) * quantity * size
    if leg_type == "cash":
        return 0.0

    return option_payoff(
        scenario_price,
        _strike(leg),
        str(leg["option_type"]),
        str(leg["side"]),
    ) * quantity * size


def _leg_profit(
    scenario_price: float,
    leg: dict[str, float | int | str | None],
    fallback_contract_size: int,
) -> float:
    leg_type = _leg_type(leg)
    if leg_type in {"stock", "cash"}:
        return _leg_payoff(scenario_price, leg, fallback_contract_size)

    quantity = int(leg.get("quantity", 1) or 1)
    size = int(leg.get("contract_size", fallback_contract_size) or fallback_contract_size)
    payoff_per_option = option_payoff(
        scenario_price,
        _strike(leg),
        str(leg["option_type"]),
        str(leg["side"]),
    )
    return option_profit(
        payoff_per_option,
        float(leg.get("premium", 0.0) or 0.0),
        str(leg["side"]),
    ) * quantity * size


def _leg_net_premium(
    leg: dict[str, float | int | str | None],
    fallback_contract_size: int,
) -> float:
    if _leg_type(leg) != "option":
        return 0.0
    side_multiplier = 1.0 if str(leg.get("side")) == "long" else -1.0
    quantity = int(leg.get("quantity", 1) or 1)
    size = int(leg.get("contract_size", fallback_contract_size) or fallback_contract_size)
    return float(leg.get("premium", 0.0) or 0.0) * quantity * size * side_multiplier


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


def _collateral_requirement(
    legs: list[dict[str, float | int | str | None]],
    fallback_contract_size: int,
) -> float:
    return sum(
        float(leg.get("underlying_price", 0.0) or 0.0)
        * int(leg.get("quantity", 1) or 1)
        * int(leg.get("contract_size", fallback_contract_size) or fallback_contract_size)
        for leg in legs
        if _leg_type(leg) == "cash"
    )


def _leg_type(leg: dict[str, float | int | str | None]) -> str:
    return str(leg.get("leg_type") or "option")


def _strike(leg: dict[str, float | int | str | None]) -> float:
    return float(leg.get("strike_price") or leg.get("strike") or 0.0)


def _stock_leg(
    underlying_price: float,
    shares: int,
) -> dict[str, float | int | str | None]:
    return {
        "leg_type": "stock",
        "side": "long",
        "option_type": None,
        "strike_price": None,
        "expiration_days": None,
        "premium": None,
        "quantity": shares,
        "contract_size": 1,
        "underlying_price": underlying_price,
        "description": "Long stock underlying position",
    }


def _option_leg(
    option_type: str,
    side: str,
    strike_price: float,
    expiration_days: int,
    quantity: int,
    contract_size: int,
) -> dict[str, float | int | str | None]:
    return {
        "leg_type": "option",
        "side": side,
        "option_type": option_type,
        "strike_price": strike_price,
        "expiration_days": expiration_days,
        "premium": None,
        "quantity": quantity,
        "contract_size": contract_size,
        "underlying_price": None,
        "description": f"{side.title()} {option_type} option",
    }


def _cash_leg(
    strike_price: float,
    quantity: int,
    contract_size: int,
) -> dict[str, float | int | str | None]:
    return {
        "leg_type": "cash",
        "side": "long",
        "option_type": None,
        "strike_price": None,
        "expiration_days": None,
        "premium": None,
        "quantity": quantity,
        "contract_size": contract_size,
        "underlying_price": strike_price,
        "description": "Cash reserved as put assignment collateral",
    }


def _risk_profile(strategy_type: str) -> str:
    profiles = {
        "covered_call": "Generates premium but caps upside on an existing long stock position.",
        "protective_put": "Pays premium to reduce downside risk on an existing position.",
        "long_straddle": "Benefits from large moves in either direction and higher volatility.",
        "long_strangle": "Lower-cost volatility strategy requiring a larger underlying move.",
        "bull_call_spread": "Defined-risk bullish strategy with capped upside.",
        "bear_put_spread": "Defined-risk bearish strategy with capped profit.",
        "collar": "Combines downside protection with an upside cap on long stock.",
        "cash_secured_put": "Earns premium while reserving cash for the purchase obligation.",
    }
    return profiles.get(strategy_type, "Deterministic educational strategy payoff.")
