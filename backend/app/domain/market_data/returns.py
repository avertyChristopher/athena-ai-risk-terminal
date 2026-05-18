from math import log
from typing import Sequence


def calculate_simple_returns(prices: Sequence[float]) -> list[float]:
    _validate_prices(prices)

    return [
        (current_price / previous_price) - 1.0
        for previous_price, current_price in zip(prices, prices[1:])
    ]


def calculate_log_returns(prices: Sequence[float]) -> list[float]:
    _validate_prices(prices)

    return [
        log(current_price / previous_price)
        for previous_price, current_price in zip(prices, prices[1:])
    ]


def calculate_cumulative_returns(returns: Sequence[float]) -> list[float]:
    if not returns:
        raise ValueError("At least one return is required.")

    cumulative_return = 1.0
    cumulative_returns = []

    for period_return in returns:
        cumulative_return *= 1.0 + period_return
        cumulative_returns.append(cumulative_return - 1.0)

    return cumulative_returns


def calculate_drawdown(values: Sequence[float]) -> list[float]:
    if not values:
        raise ValueError("At least one value is required.")

    if any(value <= 0 for value in values):
        raise ValueError("Values must be strictly positive.")

    running_peak = values[0]
    drawdowns = []

    for value in values:
        running_peak = max(running_peak, value)
        drawdowns.append((value / running_peak) - 1.0)

    return drawdowns


def _validate_prices(prices: Sequence[float]) -> None:
    if len(prices) < 2:
        raise ValueError("At least two prices are required to calculate returns.")

    if any(price <= 0 for price in prices):
        raise ValueError("Prices must be strictly positive.")
