from math import exp, sqrt

from app.modules.options_pricing_lab.domain.black_scholes import (
    d1,
    d2,
    normal_cdf,
    normal_pdf,
)


def option_greeks(
    option_type: str,
    underlying_price: float,
    strike_price: float,
    time_to_expiration_years: float,
    risk_free_rate: float,
    volatility: float,
    dividend_yield: float = 0.0,
    position_side: str = "long",
) -> dict[str, float]:
    first = d1(
        underlying_price,
        strike_price,
        time_to_expiration_years,
        risk_free_rate,
        volatility,
        dividend_yield,
    )
    second = d2(
        underlying_price,
        strike_price,
        time_to_expiration_years,
        risk_free_rate,
        volatility,
        dividend_yield,
    )
    discount_dividend = exp(-dividend_yield * time_to_expiration_years)
    discount_rate = exp(-risk_free_rate * time_to_expiration_years)
    pdf = normal_pdf(first)

    if option_type == "call":
        delta = discount_dividend * normal_cdf(first)
        theta = (
            -underlying_price
            * discount_dividend
            * pdf
            * volatility
            / (2 * sqrt(time_to_expiration_years))
            - risk_free_rate
            * strike_price
            * discount_rate
            * normal_cdf(second)
            + dividend_yield
            * underlying_price
            * discount_dividend
            * normal_cdf(first)
        )
        rho = strike_price * time_to_expiration_years * discount_rate * normal_cdf(second)
    else:
        delta = discount_dividend * (normal_cdf(first) - 1)
        theta = (
            -underlying_price
            * discount_dividend
            * pdf
            * volatility
            / (2 * sqrt(time_to_expiration_years))
            + risk_free_rate
            * strike_price
            * discount_rate
            * normal_cdf(-second)
            - dividend_yield
            * underlying_price
            * discount_dividend
            * normal_cdf(-first)
        )
        rho = -strike_price * time_to_expiration_years * discount_rate * normal_cdf(-second)

    gamma = (
        discount_dividend
        * pdf
        / (underlying_price * volatility * sqrt(time_to_expiration_years))
    )
    vega = underlying_price * discount_dividend * pdf * sqrt(time_to_expiration_years)
    sign = 1.0 if position_side == "long" else -1.0

    return {
        "delta": delta * sign,
        "gamma": gamma * sign,
        "theta_annual": theta * sign,
        "theta_daily": theta / 365 * sign,
        "vega": vega / 100 * sign,
        "rho": rho / 100 * sign,
    }
