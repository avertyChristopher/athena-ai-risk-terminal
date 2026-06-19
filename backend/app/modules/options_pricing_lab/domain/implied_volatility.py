from app.modules.options_pricing_lab.domain.black_scholes import black_scholes_price


def implied_volatility_placeholder() -> dict[str, str]:
    return {
        "status": "planned",
        "note": "Implied volatility requires observed option market prices or an options chain.",
    }


def estimate_implied_volatility(
    market_price: float,
    option_type: str,
    underlying_price: float,
    strike_price: float,
    time_to_expiration_years: float,
    risk_free_rate: float,
    dividend_yield: float = 0.0,
    iterations: int = 60,
) -> float | None:
    if market_price <= 0:
        return None

    low = 0.0001
    high = 5.0
    for _ in range(iterations):
        mid = (low + high) / 2
        price = black_scholes_price(
            option_type,
            underlying_price,
            strike_price,
            time_to_expiration_years,
            risk_free_rate,
            mid,
            dividend_yield,
        )
        if price > market_price:
            high = mid
        else:
            low = mid
    return (low + high) / 2
