from math import exp


def put_call_parity_check(
    call_price: float,
    put_price: float,
    underlying_price: float,
    strike_price: float,
    time_to_expiration_years: float,
    risk_free_rate: float,
    dividend_yield: float = 0.0,
) -> dict[str, float | str]:
    left_side = call_price + strike_price * exp(-risk_free_rate * time_to_expiration_years)
    right_side = put_price + underlying_price * exp(-dividend_yield * time_to_expiration_years)
    gap = left_side - right_side
    relative_gap = abs(gap) / max(underlying_price, 1.0)
    if relative_gap < 0.001:
        status = "aligned"
    elif relative_gap < 0.01:
        status = "small_deviation"
    else:
        status = "potential_arbitrage"
    return {
        "left_side": left_side,
        "right_side": right_side,
        "parity_gap": gap,
        "status": status,
        "note": "Put-call parity is a no-arbitrage relationship for European options.",
    }
