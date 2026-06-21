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


def generate_dated_coupon_schedule(
    settlement_date: date,
    maturity_date: date,
    coupon_frequency: str,
) -> list[date]:
    if settlement_date >= maturity_date:
        raise ValueError("Settlement date must be before maturity date.")
    frequency = frequency_per_year(coupon_frequency)
    months = 12 // frequency
    schedule = []
    period_offset = 0
    payment_date = maturity_date
    while payment_date > settlement_date:
        schedule.append(payment_date)
        period_offset += 1
        payment_date = _add_months(maturity_date, -months * period_offset)
    return list(reversed(schedule))


def get_previous_coupon_date(
    settlement_date: date,
    maturity_date: date,
    coupon_frequency: str,
) -> date:
    previous, _ = _coupon_period_dates(
        settlement_date,
        maturity_date,
        coupon_frequency,
    )
    return previous


def get_next_coupon_date(
    settlement_date: date,
    maturity_date: date,
    coupon_frequency: str,
) -> date:
    _, next_coupon = _coupon_period_dates(
        settlement_date,
        maturity_date,
        coupon_frequency,
    )
    return next_coupon


def calculate_accrued_interest(
    face_value: float,
    coupon_rate: float,
    coupon_frequency: str,
    settlement_date: date,
    previous_coupon_date: date,
    next_coupon_date: date,
    day_count_convention: str = "actual_actual",
) -> tuple[float, int, int]:
    if not previous_coupon_date <= settlement_date < next_coupon_date:
        raise ValueError("Settlement must fall within the supplied coupon period.")
    accrued_days = _day_count(
        previous_coupon_date,
        settlement_date,
        day_count_convention,
    )
    coupon_period_days = _day_count(
        previous_coupon_date,
        next_coupon_date,
        day_count_convention,
    )
    fraction = accrued_days / max(coupon_period_days, 1)
    amount = calculate_coupon_payment(
        face_value,
        coupon_rate,
        coupon_frequency,
    ) * fraction
    return amount, accrued_days, coupon_period_days


def generate_dated_bond_cashflows(
    face_value: float,
    coupon_rate: float,
    coupon_frequency: str,
    settlement_date: date,
    maturity_date: date,
    day_count_convention: str = "actual_actual",
) -> tuple[list[dict[str, float | int | date]], dict[str, object]]:
    frequency = frequency_per_year(coupon_frequency)
    schedule = generate_dated_coupon_schedule(
        settlement_date,
        maturity_date,
        coupon_frequency,
    )
    previous_coupon, next_coupon = _coupon_period_dates(
        settlement_date,
        maturity_date,
        coupon_frequency,
    )
    accrued, accrued_days, coupon_period_days = calculate_accrued_interest(
        face_value,
        coupon_rate,
        coupon_frequency,
        settlement_date,
        previous_coupon,
        next_coupon,
        day_count_convention,
    )
    days_to_next_coupon = _day_count(
        settlement_date,
        next_coupon,
        day_count_convention,
    )
    first_period_fraction = days_to_next_coupon / max(coupon_period_days, 1)
    coupon = calculate_coupon_payment(face_value, coupon_rate, coupon_frequency)
    cashflows = []
    for period, payment_date in enumerate(schedule, start=1):
        periods_from_settlement = first_period_fraction + period - 1
        principal = face_value if payment_date == maturity_date else 0.0
        cashflows.append(
            {
                "period": period,
                "time_years": periods_from_settlement / frequency,
                "payment_date": payment_date,
                "coupon": coupon,
                "principal": principal,
                "total_cash_flow": coupon + principal,
                "frequency": frequency,
            }
        )
    return cashflows, {
        "previous_coupon_date": previous_coupon,
        "next_coupon_date": next_coupon,
        "accrued_days": accrued_days,
        "coupon_period_days": coupon_period_days,
        "accrued_interest": accrued,
    }


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

    previous_coupon, next_coupon = _coupon_period_dates(
        settlement_date,
        maturity_date,
        coupon_frequency,
    )
    amount, _, _ = calculate_accrued_interest(
        face_value,
        coupon_rate,
        coupon_frequency,
        settlement_date,
        previous_coupon,
        next_coupon,
        day_count_convention,
    )
    return amount


def year_fraction(
    start: date,
    end: date,
    day_count_convention: str = "actual_actual",
) -> float:
    if end <= start:
        raise ValueError("End date must be after start date.")
    if day_count_convention == "30_360":
        return _days_30_360(start, end) / 360
    return (end - start).days / 365.25


def _coupon_period_dates(
    settlement_date: date,
    maturity_date: date,
    coupon_frequency: str,
) -> tuple[date, date]:
    if settlement_date >= maturity_date:
        raise ValueError("Settlement date must be before maturity date.")
    frequency = frequency_per_year(coupon_frequency)
    months = 12 // frequency
    period_offset = 1
    next_coupon = maturity_date
    previous_coupon = _add_months(maturity_date, -months * period_offset)
    while previous_coupon > settlement_date:
        next_coupon = previous_coupon
        period_offset += 1
        previous_coupon = _add_months(maturity_date, -months * period_offset)
    return previous_coupon, next_coupon


def _day_count(start: date, end: date, convention: str) -> int:
    if convention == "30_360":
        return _days_30_360(start, end)
    return (end - start).days


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
