from math import sqrt
from statistics import stdev
from typing import Sequence

TRADING_DAYS_PER_YEAR = 252


def calculate_daily_volatility(returns: Sequence[float]) -> float:
    _validate_returns(returns, minimum_length=2)

    return stdev(returns)


def calculate_annualized_volatility(
    returns: Sequence[float],
    trading_days: int = TRADING_DAYS_PER_YEAR,
) -> float:
    if trading_days <= 0:
        raise ValueError("Trading days must be positive.")

    return calculate_daily_volatility(returns) * sqrt(trading_days)


def rolling_volatility(
    returns: Sequence[float],
    window: int,
    trading_days: int | None = None,
) -> list[float]:
    _validate_returns(returns, minimum_length=window)

    if window < 2:
        raise ValueError("Rolling volatility window must be at least 2.")

    if trading_days is not None and trading_days <= 0:
        raise ValueError("Trading days must be positive.")

    values = [
        stdev(returns[index - window : index])
        for index in range(window, len(returns) + 1)
    ]

    if trading_days is None:
        return values

    return [value * sqrt(trading_days) for value in values]


def _validate_returns(returns: Sequence[float], minimum_length: int) -> None:
    if len(returns) < minimum_length:
        raise ValueError(f"At least {minimum_length} returns are required.")


daily_volatility = calculate_daily_volatility
annualized_volatility = calculate_annualized_volatility
