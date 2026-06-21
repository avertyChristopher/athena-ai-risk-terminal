from app.modules.rates_lab.domain.bonds import price_from_cashflows
from app.modules.rates_lab.domain.cashflows import frequency_per_year


def convexity(
    cashflows: list[dict[str, float | int]],
    yield_to_maturity: float,
    coupon_frequency: str,
) -> float:
    frequency = frequency_per_year(coupon_frequency)
    price, valued_cashflows = price_from_cashflows(
        cashflows,
        yield_to_maturity,
        coupon_frequency,
    )
    periodic_denominator = (1 + yield_to_maturity / frequency) ** 2
    numerator = sum(
        float(item["present_value"])
        * float(item["time_years"])
        * (float(item["time_years"]) + 1 / frequency)
        for item in valued_cashflows
    )
    return numerator / (price * periodic_denominator)


def convexity_adjusted_price_impact(
    price: float,
    modified_duration_value: float,
    convexity_value: float,
    rate_change: float,
) -> float:
    percentage_change = (
        -modified_duration_value * rate_change
        + 0.5 * convexity_value * rate_change**2
    )
    return price * percentage_change
