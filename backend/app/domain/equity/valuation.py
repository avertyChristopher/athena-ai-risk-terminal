from __future__ import annotations

from collections.abc import Sequence


def calculate_gordon_growth_value(
    dividend_next_year: float,
    required_return: float,
    growth_rate: float,
) -> float:
    _validate_non_negative(dividend_next_year, "dividend_next_year")
    _validate_rate(required_return, "required_return")
    _validate_rate(growth_rate, "growth_rate")

    if required_return <= growth_rate:
        raise ValueError("Required return must be greater than growth rate.")

    return dividend_next_year / (required_return - growth_rate)


def calculate_dividend_discount_value(
    dividends: Sequence[float],
    required_return: float,
    terminal_value: float = 0.0,
) -> float:
    if not dividends:
        raise ValueError("At least one dividend is required.")

    _validate_rate(required_return, "required_return")
    _validate_non_negative(terminal_value, "terminal_value")

    present_value = 0.0
    for period, dividend in enumerate(dividends, start=1):
        _validate_non_negative(dividend, "dividend")
        present_value += dividend / ((1.0 + required_return) ** period)

    if terminal_value:
        present_value += terminal_value / ((1.0 + required_return) ** len(dividends))

    return present_value


def calculate_implied_cost_of_equity(
    dividend_next_year: float,
    current_price: float,
    growth_rate: float,
) -> float:
    _validate_non_negative(dividend_next_year, "dividend_next_year")
    _validate_positive(current_price, "current_price")
    _validate_rate(growth_rate, "growth_rate")
    return (dividend_next_year / current_price) + growth_rate


def calculate_implied_growth_rate(
    dividend_next_year: float,
    current_price: float,
    required_return: float,
) -> float:
    _validate_non_negative(dividend_next_year, "dividend_next_year")
    _validate_positive(current_price, "current_price")
    _validate_rate(required_return, "required_return")
    return required_return - (dividend_next_year / current_price)


def calculate_pe_ratio(price: float, earnings_per_share: float) -> float:
    _validate_positive(price, "price")
    _validate_positive(earnings_per_share, "earnings_per_share")
    return price / earnings_per_share


def calculate_pb_ratio(price: float, book_value_per_share: float) -> float:
    _validate_positive(price, "price")
    _validate_positive(book_value_per_share, "book_value_per_share")
    return price / book_value_per_share


def calculate_ps_ratio(market_cap: float, revenue: float) -> float:
    _validate_positive(market_cap, "market_cap")
    _validate_positive(revenue, "revenue")
    return market_cap / revenue


def calculate_ev_ebitda(enterprise_value: float, ebitda: float) -> float:
    _validate_positive(enterprise_value, "enterprise_value")
    _validate_positive(ebitda, "ebitda")
    return enterprise_value / ebitda


def calculate_dividend_yield(dividend_per_share: float, price: float) -> float:
    _validate_non_negative(dividend_per_share, "dividend_per_share")
    _validate_positive(price, "price")
    return dividend_per_share / price


def calculate_earnings_yield(earnings_per_share: float, price: float) -> float:
    _validate_positive(earnings_per_share, "earnings_per_share")
    _validate_positive(price, "price")
    return earnings_per_share / price


def calculate_free_cash_flow_yield(free_cash_flow: float, market_cap: float) -> float:
    _validate_positive(market_cap, "market_cap")
    return free_cash_flow / market_cap


def calculate_margin_of_safety(
    intrinsic_value: float,
    market_price: float,
) -> float:
    _validate_positive(intrinsic_value, "intrinsic_value")
    _validate_positive(market_price, "market_price")
    return (intrinsic_value - market_price) / intrinsic_value


def _validate_rate(value: float, field_name: str) -> None:
    if value <= -1.0:
        raise ValueError(f"{field_name} must be greater than -100%.")


def _validate_positive(value: float, field_name: str) -> None:
    if value <= 0:
        raise ValueError(f"{field_name} must be positive.")


def _validate_non_negative(value: float, field_name: str) -> None:
    if value < 0:
        raise ValueError(f"{field_name} must be non-negative.")
