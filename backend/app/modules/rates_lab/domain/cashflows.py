from calendar import monthrange
from datetime import date


FREQUENCIES = {
    "annual": 1,
    "semiannual": 2,
    "quarterly": 4,
    "monthly": 12,
}


def frequency_per_year(coupon_frequency: str) -> int:
    try:
        return FREQUENCIES[coupon_frequency]
    except KeyError as exc:
        raise ValueError(f"Unsupported coupon frequency: {coupon_frequency}.") from exc


def calculate_coupon_payment(
    face_value: float,
    coupon_rate: float,
    coupon_frequency: str,
) -> float:
    return face_value * coupon_rate / frequency_per_year(coupon_frequency)


def generate_coupon_schedule(
    years_to_maturity: float,
    coupon_frequency: str,
) -> list[float]:
    frequency = frequency_per_year(coupon_frequency)
    periods = max(1, round(years_to_maturity * frequency))
    return [period / frequency for period in range(1, periods + 1)]


def generate_bond_cashflows(
    face_value: float,
    coupon_rate: float,
    coupon_frequency: str,
    years_to_maturity: float,
) -> list[dict[str, float | int]]:
    frequency = frequency_per_year(coupon_frequency)
    schedule = generate_coupon_schedule(years_to_maturity, coupon_frequency)
    coupon = calculate_coupon_payment(face_value, coupon_rate, coupon_frequency)
    cashflows = []
    for period, time_years in enumerate(schedule, start=1):
        principal = face_value if period == len(schedule) else 0.0
        cashflows.append(
            {
                "period": period,
                "time_years": time_years,
                "coupon": coupon,
                "principal": principal,
                "total_cash_flow": coupon + principal,
                "frequency": frequency,
            }
        )
    return cashflows


def zero_coupon_cashflow(
    face_value: float,
    years_to_maturity: float,
) -> list[dict[str, float | int]]:
    return [
        {
            "period": 1,
            "time_years": years_to_maturity,
            "coupon": 0.0,
            "principal": face_value,
            "total_cash_flow": face_value,
            "frequency": 1,
        }
    ]


def accrued_interest(
    face_value: float,
    coupon_rate: float,
    coupon_frequency: str,
    settlement_date: date | None = None,
    maturity_date: date | None = None,
    day_count_convention: str = "actual_actual",
) -> float:
    if settlement_date is None or maturity_date is None:
        return 0.0
    if settlement_date >= maturity_date:
        return 0.0

    frequency = frequency_per_year(coupon_frequency)
    months = 12 // frequency
    next_coupon = maturity_date
    previous_coupon = _add_months(next_coupon, -months)
    while previous_coupon > settlement_date:
        next_coupon = previous_coupon
        previous_coupon = _add_months(next_coupon, -months)

    if day_count_convention == "30_360":
        elapsed = _days_30_360(previous_coupon, settlement_date)
        period_days = _days_30_360(previous_coupon, next_coupon)
    else:
        elapsed = (settlement_date - previous_coupon).days
        period_days = (next_coupon - previous_coupon).days

    fraction = min(1.0, max(0.0, elapsed / max(period_days, 1)))
    return calculate_coupon_payment(
        face_value,
        coupon_rate,
        coupon_frequency,
    ) * fraction


def _add_months(value: date, months: int) -> date:
    month_index = value.year * 12 + value.month - 1 + months
    year, month_zero = divmod(month_index, 12)
    month = month_zero + 1
    day = min(value.day, monthrange(year, month)[1])
    return date(year, month, day)


def _days_30_360(start: date, end: date) -> int:
    start_day = min(start.day, 30)
    end_day = min(end.day, 30) if start_day == 30 else end.day
    return (
        (end.year - start.year) * 360
        + (end.month - start.month) * 30
        + end_day
        - start_day
    )
