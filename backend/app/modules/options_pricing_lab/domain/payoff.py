def long_call_payoff(underlying_price: float, strike_price: float) -> float:
    return max(underlying_price - strike_price, 0.0)


def short_call_payoff(underlying_price: float, strike_price: float) -> float:
    return -long_call_payoff(underlying_price, strike_price)


def long_put_payoff(underlying_price: float, strike_price: float) -> float:
    return max(strike_price - underlying_price, 0.0)


def short_put_payoff(underlying_price: float, strike_price: float) -> float:
    return -long_put_payoff(underlying_price, strike_price)


def option_payoff(
    underlying_price: float,
    strike_price: float,
    option_type: str,
    side: str,
) -> float:
    if option_type == "call":
        payoff = long_call_payoff(underlying_price, strike_price)
    else:
        payoff = long_put_payoff(underlying_price, strike_price)
    return payoff if side == "long" else -payoff


def option_profit(payoff: float, premium: float, side: str) -> float:
    return payoff - premium if side == "long" else payoff + premium


def breakeven_call(strike_price: float, premium: float) -> float:
    return strike_price + premium


def breakeven_put(strike_price: float, premium: float) -> float:
    return strike_price - premium


def call_intrinsic_value(underlying_price: float, strike_price: float) -> float:
    return long_call_payoff(underlying_price, strike_price)


def put_intrinsic_value(underlying_price: float, strike_price: float) -> float:
    return long_put_payoff(underlying_price, strike_price)


def intrinsic_value(
    underlying_price: float,
    strike_price: float,
    option_type: str,
) -> float:
    if option_type == "call":
        return call_intrinsic_value(underlying_price, strike_price)
    return put_intrinsic_value(underlying_price, strike_price)


def time_value(premium: float, intrinsic: float) -> float:
    return max(premium - intrinsic, 0.0)
