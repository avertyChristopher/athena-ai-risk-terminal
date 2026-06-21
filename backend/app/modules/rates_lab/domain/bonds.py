from app.modules.rates_lab.domain.cashflows import (
    frequency_per_year,
    generate_bond_cashflows,
    zero_coupon_cashflow,
)


def price_from_cashflows(
    cashflows: list[dict[str, float | int]],
    yield_to_maturity: float,
    coupon_frequency: str,
) -> tuple[float, list[dict[str, float | int]]]:
    frequency = frequency_per_year(coupon_frequency)
    periodic_rate = yield_to_maturity / frequency
    if periodic_rate <= -1:
        raise ValueError("Yield per period must be greater than -100 percent.")

    present_value = 0.0
    valued_cashflows = []
    for cashflow in cashflows:
        periods = float(cashflow["time_years"]) * frequency
        discount_factor = (1 + periodic_rate) ** periods
        pv = float(cashflow["total_cash_flow"]) / discount_factor
        present_value += pv
        valued_cashflows.append(
            {
                **cashflow,
                "discount_factor": discount_factor,
                "present_value": pv,
            }
        )
    return present_value, valued_cashflows


def price_coupon_bond(
    face_value: float,
    coupon_rate: float,
    coupon_frequency: str,
    years_to_maturity: float,
    yield_to_maturity: float,
) -> tuple[float, list[dict[str, float | int]]]:
    cashflows = generate_bond_cashflows(
        face_value,
        coupon_rate,
        coupon_frequency,
        years_to_maturity,
    )
    return price_from_cashflows(cashflows, yield_to_maturity, coupon_frequency)


def price_zero_coupon_bond(
    face_value: float,
    years_to_maturity: float,
    yield_to_maturity: float,
    coupon_frequency: str = "annual",
) -> tuple[float, list[dict[str, float | int]]]:
    cashflows = zero_coupon_cashflow(face_value, years_to_maturity)
    return price_from_cashflows(cashflows, yield_to_maturity, coupon_frequency)


def clean_price(dirty_price_value: float, accrued_interest_value: float) -> float:
    return dirty_price_value - accrued_interest_value


def dirty_price(clean_price_value: float, accrued_interest_value: float) -> float:
    return clean_price_value + accrued_interest_value
