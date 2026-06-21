from app.modules.rates_lab.domain.bonds import price_coupon_bond
from app.modules.rates_lab.domain.cashflows import frequency_per_year


def current_yield(
    face_value: float,
    coupon_rate: float,
    market_price: float,
) -> float:
    if market_price <= 0:
        raise ValueError("Market price must be positive.")
    return face_value * coupon_rate / market_price


def holding_period_return(
    beginning_price: float,
    ending_price: float,
    coupon_received: float = 0.0,
) -> float:
    if beginning_price <= 0:
        raise ValueError("Beginning price must be positive.")
    return (ending_price - beginning_price + coupon_received) / beginning_price


def yield_to_maturity(
    price: float,
    face_value: float,
    coupon_rate: float,
    coupon_frequency: str,
    years_to_maturity: float,
    tolerance: float = 1e-9,
    max_iterations: int = 200,
) -> dict[str, float | int | bool | str]:
    if price <= 0:
        raise ValueError("Price must be positive.")

    frequency = frequency_per_year(coupon_frequency)
    lower = -0.99
    upper = 1.0

    def pricing_error(rate: float) -> float:
        model_price, _ = price_coupon_bond(
            face_value,
            coupon_rate,
            coupon_frequency,
            years_to_maturity,
            rate,
        )
        return model_price - price

    lower_error = pricing_error(lower)
    upper_error = pricing_error(upper)
    while lower_error * upper_error > 0 and upper < 100:
        upper *= 2
        upper_error = pricing_error(upper)

    if lower_error * upper_error > 0:
        return {
            "yield_to_maturity": 0.0,
            "converged": False,
            "iterations": 0,
            "pricing_error": upper_error,
            "warning": "Unable to bracket a yield for the supplied price.",
        }

    midpoint = 0.0
    error = 0.0
    for iteration in range(1, max_iterations + 1):
        midpoint = (lower + upper) / 2
        error = pricing_error(midpoint)
        if abs(error) <= tolerance:
            return {
                "yield_to_maturity": midpoint,
                "converged": True,
                "iterations": iteration,
                "pricing_error": error,
                "warning": "",
            }
        if lower_error * error > 0:
            lower = midpoint
            lower_error = error
        else:
            upper = midpoint

    return {
        "yield_to_maturity": midpoint,
        "converged": False,
        "iterations": max_iterations,
        "pricing_error": error,
        "warning": "YTM solver reached the iteration limit.",
    }


def price_premium_discount_status(
    price: float,
    face_value: float,
    tolerance: float = 0.001,
) -> str:
    relative_difference = (price - face_value) / face_value
    if abs(relative_difference) <= tolerance:
        return "par"
    return "premium" if relative_difference > 0 else "discount"
