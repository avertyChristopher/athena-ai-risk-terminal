from app.modules.rates_lab.domain.bonds import price_from_cashflows
from app.modules.rates_lab.domain.cashflows import frequency_per_year


def macaulay_duration(
    cashflows: list[dict[str, float | int]],
    yield_to_maturity: float,
    coupon_frequency: str,
) -> float:
    price, valued_cashflows = price_from_cashflows(
        cashflows,
        yield_to_maturity,
        coupon_frequency,
    )
    if price <= 0:
        raise ValueError("Bond price must be positive.")
    weighted_time = sum(
        float(item["time_years"]) * float(item["present_value"])
        for item in valued_cashflows
    )
    return weighted_time / price


def modified_duration(
    macaulay_duration_value: float,
    yield_to_maturity: float,
    coupon_frequency: str,
) -> float:
    frequency = frequency_per_year(coupon_frequency)
    denominator = 1 + yield_to_maturity / frequency
    if denominator <= 0:
        raise ValueError("Yield per period must be greater than -100 percent.")
    return macaulay_duration_value / denominator


def duration_price_impact(
    price: float,
    modified_duration_value: float,
    rate_change: float,
) -> float:
    return -modified_duration_value * rate_change * price


def dv01(price: float, modified_duration_value: float) -> float:
    return abs(modified_duration_value * price * 0.0001)


def pvbp(price: float, modified_duration_value: float) -> float:
    return dv01(price, modified_duration_value)
