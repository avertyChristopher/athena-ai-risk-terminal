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


def _validate_prices(prices: Sequence[float]) -> None:
    if len(prices) < 2:
        raise ValueError("At least two prices are required to calculate returns.")

    if any(price <= 0 for price in prices):
        raise ValueError("Prices must be strictly positive.")
