from math import exp, log, sqrt
from statistics import NormalDist


NORMAL = NormalDist()


def normal_cdf(value: float) -> float:
    return NORMAL.cdf(value)


def normal_pdf(value: float) -> float:
    return NORMAL.pdf(value)


def d1(
    underlying_price: float,
    strike_price: float,
    time_to_expiration_years: float,
    risk_free_rate: float,
    volatility: float,
    dividend_yield: float = 0.0,
) -> float:
    _validate_inputs(
        underlying_price,
        strike_price,
        time_to_expiration_years,
        volatility,
    )
    numerator = log(underlying_price / strike_price) + (
        risk_free_rate
        - dividend_yield
        + 0.5 * volatility**2
    ) * time_to_expiration_years
    denominator = volatility * sqrt(time_to_expiration_years)
    return numerator / denominator


def d2(
    underlying_price: float,
    strike_price: float,
    time_to_expiration_years: float,
    risk_free_rate: float,
    volatility: float,
    dividend_yield: float = 0.0,
) -> float:
    return d1(
        underlying_price,
        strike_price,
        time_to_expiration_years,
        risk_free_rate,
        volatility,
        dividend_yield,
    ) - volatility * sqrt(time_to_expiration_years)


def black_scholes_call_price(
    underlying_price: float,
    strike_price: float,
    time_to_expiration_years: float,
    risk_free_rate: float,
    volatility: float,
    dividend_yield: float = 0.0,
) -> float:
    first = d1(
        underlying_price,
        strike_price,
        time_to_expiration_years,
        risk_free_rate,
        volatility,
        dividend_yield,
    )
    second = first - volatility * sqrt(time_to_expiration_years)
    return (
        underlying_price
        * exp(-dividend_yield * time_to_expiration_years)
        * normal_cdf(first)
        - strike_price
        * exp(-risk_free_rate * time_to_expiration_years)
        * normal_cdf(second)
    )


def black_scholes_put_price(
    underlying_price: float,
    strike_price: float,
    time_to_expiration_years: float,
    risk_free_rate: float,
    volatility: float,
    dividend_yield: float = 0.0,
) -> float:
    first = d1(
        underlying_price,
        strike_price,
        time_to_expiration_years,
        risk_free_rate,
        volatility,
        dividend_yield,
    )
    second = first - volatility * sqrt(time_to_expiration_years)
    return (
        strike_price
        * exp(-risk_free_rate * time_to_expiration_years)
        * normal_cdf(-second)
        - underlying_price
        * exp(-dividend_yield * time_to_expiration_years)
        * normal_cdf(-first)
    )


def black_scholes_price(
    option_type: str,
    underlying_price: float,
    strike_price: float,
    time_to_expiration_years: float,
    risk_free_rate: float,
    volatility: float,
    dividend_yield: float = 0.0,
) -> float:
    if option_type == "call":
        return black_scholes_call_price(
            underlying_price,
            strike_price,
            time_to_expiration_years,
            risk_free_rate,
            volatility,
            dividend_yield,
        )
    return black_scholes_put_price(
        underlying_price,
        strike_price,
        time_to_expiration_years,
        risk_free_rate,
        volatility,
        dividend_yield,
    )


def _validate_inputs(
    underlying_price: float,
    strike_price: float,
    time_to_expiration_years: float,
    volatility: float,
) -> None:
    if underlying_price <= 0:
        raise ValueError("underlying_price must be positive.")
    if strike_price <= 0:
        raise ValueError("strike_price must be positive.")
    if time_to_expiration_years <= 0:
        raise ValueError("time_to_expiration_years must be positive.")
    if volatility <= 0:
        raise ValueError("volatility must be positive.")
