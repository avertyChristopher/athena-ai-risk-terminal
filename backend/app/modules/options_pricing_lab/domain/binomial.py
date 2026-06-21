from math import exp, sqrt

from app.modules.options_pricing_lab.domain.payoff import intrinsic_value


def binomial_option_price(
    option_type: str,
    underlying_price: float,
    strike_price: float,
    time_to_expiration_years: float,
    risk_free_rate: float,
    volatility: float,
    dividend_yield: float = 0.0,
    steps: int = 50,
) -> dict[str, float | bool | str | None]:
    if steps < 1:
        raise ValueError("steps must be at least 1.")
    if min(underlying_price, strike_price, time_to_expiration_years, volatility) <= 0:
        raise ValueError("underlying, strike, time and volatility must be positive.")

    dt = time_to_expiration_years / steps
    up = exp(volatility * sqrt(dt))
    down = 1.0 / up
    growth = exp((risk_free_rate - dividend_yield) * dt)
    probability = (growth - down) / (up - down)
    no_arbitrage_valid = down < growth < up
    if not no_arbitrage_valid:
        return {
            "price": None,
            "up_factor": up,
            "down_factor": down,
            "risk_neutral_probability": probability,
            "steps": float(steps),
            "no_arbitrage_valid": False,
            "warning": (
                "Binomial parameters violate the no-arbitrage condition. "
                "Review volatility, rate, dividend yield or step count."
            ),
        }
    discount = exp(-risk_free_rate * dt)

    values = [
        intrinsic_value(
            underlying_price * (up ** (steps - index)) * (down ** index),
            strike_price,
            option_type,
        )
        for index in range(steps + 1)
    ]

    for _ in range(steps, 0, -1):
        values = [
            discount
            * (probability * values[index] + (1.0 - probability) * values[index + 1])
            for index in range(len(values) - 1)
        ]

    return {
        "price": values[0],
        "up_factor": up,
        "down_factor": down,
        "risk_neutral_probability": probability,
        "steps": float(steps),
        "no_arbitrage_valid": True,
        "warning": None,
    }
