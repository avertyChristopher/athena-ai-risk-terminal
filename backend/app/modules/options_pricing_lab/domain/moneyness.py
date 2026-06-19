def classify_moneyness(
    underlying_price: float,
    strike_price: float,
    option_type: str,
    tolerance: float = 0.01,
) -> str:
    if strike_price <= 0:
        return "unknown"

    relative_gap = abs(underlying_price - strike_price) / strike_price
    if relative_gap <= tolerance:
        return "at_the_money"

    if option_type == "call":
        return "in_the_money" if underlying_price > strike_price else "out_of_the_money"

    return "in_the_money" if underlying_price < strike_price else "out_of_the_money"


def moneyness_ratio(underlying_price: float, strike_price: float) -> float:
    if strike_price <= 0:
        return 0.0
    return underlying_price / strike_price
