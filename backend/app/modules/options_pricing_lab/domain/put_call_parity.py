from math import exp


def put_call_parity_check(
    call_price: float,
    put_price: float,
    underlying_price: float,
    strike_price: float,
    time_to_expiration_years: float,
    risk_free_rate: float,
    dividend_yield: float = 0.0,
    mode: str = "theoretical",
    model_call_price: float | None = None,
    model_put_price: float | None = None,
) -> dict[str, float | str | None]:
    present_value_strike = strike_price * exp(
        -risk_free_rate * time_to_expiration_years
    )
    dividend_adjusted_spot = underlying_price * exp(
        -dividend_yield * time_to_expiration_years
    )
    left_side = call_price + present_value_strike
    right_side = put_price + dividend_adjusted_spot
    gap = left_side - right_side
    absolute_gap = abs(gap)
    percentage_gap = absolute_gap / max(abs(right_side), 1.0)

    if percentage_gap < 0.001:
        status = "aligned"
    elif percentage_gap < 0.005:
        status = "small_deviation"
    elif percentage_gap < 0.01:
        status = "review"
    else:
        status = "potential_arbitrage"

    return {
        "mode": mode,
        "call_price": call_price,
        "put_price": put_price,
        "model_call_price": model_call_price,
        "model_put_price": model_put_price,
        "present_value_strike": present_value_strike,
        "dividend_adjusted_spot": dividend_adjusted_spot,
        "left_side": left_side,
        "right_side": right_side,
        "parity_gap": gap,
        "absolute_gap": absolute_gap,
        "percentage_gap": percentage_gap,
        "status": status,
        "label": (
            "Observed market parity check"
            if mode == "observed"
            else "Theoretical model parity"
        ),
        "note": "Put-call parity is a no-arbitrage relationship for European options.",
        "caveat": (
            "Observed deviations may reflect bid-ask spreads, transaction costs, "
            "American exercise features, dividends, stale quotes or market frictions."
        ),
    }
