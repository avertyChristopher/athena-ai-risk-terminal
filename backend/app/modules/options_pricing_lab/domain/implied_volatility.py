from math import exp

from app.modules.options_pricing_lab.domain.black_scholes import black_scholes_price


def no_arbitrage_bounds(
    option_type: str,
    underlying_price: float,
    strike_price: float,
    time_to_expiration_years: float,
    risk_free_rate: float,
    dividend_yield: float = 0.0,
) -> dict[str, float]:
    discounted_spot = underlying_price * exp(
        -dividend_yield * time_to_expiration_years
    )
    discounted_strike = strike_price * exp(
        -risk_free_rate * time_to_expiration_years
    )
    if option_type == "call":
        lower = max(0.0, discounted_spot - discounted_strike)
        upper = discounted_spot
    elif option_type == "put":
        lower = max(0.0, discounted_strike - discounted_spot)
        upper = discounted_strike
    else:
        raise ValueError("option_type must be 'call' or 'put'.")
    return {"lower_bound": lower, "upper_bound": upper}


def solve_implied_volatility(
    observed_option_price: float,
    option_type: str,
    underlying_price: float,
    strike_price: float,
    time_to_expiration_years: float,
    risk_free_rate: float,
    dividend_yield: float = 0.0,
    initial_guess: float | None = None,
    tolerance: float = 1e-6,
    max_iterations: int = 100,
) -> dict[str, object]:
    bounds = no_arbitrage_bounds(
        option_type,
        underlying_price,
        strike_price,
        time_to_expiration_years,
        risk_free_rate,
        dividend_yield,
    )
    lower_bound = bounds["lower_bound"]
    upper_bound = bounds["upper_bound"]
    warnings: list[str] = []

    if observed_option_price < lower_bound - tolerance or observed_option_price > upper_bound + tolerance:
        warnings.append(
            "Observed option price is outside European no-arbitrage bounds."
        )
        return _solver_result(
            bounds,
            warnings,
            validation_status="outside_no_arbitrage_bounds",
        )

    low_volatility = 1e-8
    high_volatility = max(5.0, (initial_guess or 0.25) * 2)
    low_price = black_scholes_price(
        option_type,
        underlying_price,
        strike_price,
        time_to_expiration_years,
        risk_free_rate,
        low_volatility,
        dividend_yield,
    )
    high_price = black_scholes_price(
        option_type,
        underlying_price,
        strike_price,
        time_to_expiration_years,
        risk_free_rate,
        high_volatility,
        dividend_yield,
    )

    while high_price < observed_option_price and high_volatility < 10.0:
        high_volatility = min(10.0, high_volatility * 1.5)
        high_price = black_scholes_price(
            option_type,
            underlying_price,
            strike_price,
            time_to_expiration_years,
            risk_free_rate,
            high_volatility,
            dividend_yield,
        )

    if observed_option_price < low_price - tolerance or observed_option_price > high_price + tolerance:
        warnings.append(
            "A finite implied volatility could not reproduce the observed price."
        )
        return _solver_result(
            bounds,
            warnings,
            validation_status="non_converged",
        )

    model_price = low_price
    volatility = low_volatility
    for iteration in range(1, max_iterations + 1):
        volatility = (low_volatility + high_volatility) / 2
        model_price = black_scholes_price(
            option_type,
            underlying_price,
            strike_price,
            time_to_expiration_years,
            risk_free_rate,
            volatility,
            dividend_yield,
        )
        pricing_error = model_price - observed_option_price
        if abs(pricing_error) <= tolerance:
            return _solver_result(
                bounds,
                warnings,
                implied_volatility=volatility,
                converged=True,
                iterations=iteration,
                model_price_at_iv=model_price,
                pricing_error=pricing_error,
                validation_status="valid",
            )
        if pricing_error > 0:
            high_volatility = volatility
        else:
            low_volatility = volatility

    warnings.append("Implied volatility solver reached the iteration limit.")
    return _solver_result(
        bounds,
        warnings,
        implied_volatility=volatility,
        converged=False,
        iterations=max_iterations,
        model_price_at_iv=model_price,
        pricing_error=model_price - observed_option_price,
        validation_status="non_converged",
    )


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
    result = solve_implied_volatility(
        market_price,
        option_type,
        underlying_price,
        strike_price,
        time_to_expiration_years,
        risk_free_rate,
        dividend_yield,
        max_iterations=iterations,
    )
    value = result["implied_volatility"]
    return float(value) if value is not None else None


def implied_volatility_placeholder() -> dict[str, str]:
    return {
        "status": "available",
        "note": "Use the implied-volatility endpoint with an observed option price.",
    }


def _solver_result(
    bounds: dict[str, float],
    warnings: list[str],
    *,
    implied_volatility: float | None = None,
    converged: bool = False,
    iterations: int = 0,
    model_price_at_iv: float | None = None,
    pricing_error: float | None = None,
    validation_status: str,
) -> dict[str, object]:
    return {
        "implied_volatility": implied_volatility,
        "converged": converged,
        "iterations": iterations,
        "model_price_at_iv": model_price_at_iv,
        "pricing_error": pricing_error,
        "no_arbitrage_bounds": bounds,
        "validation_status": validation_status,
        "warnings": warnings,
        "methodology": (
            "European Black-Scholes implied volatility solved by bounded bisection."
        ),
    }
