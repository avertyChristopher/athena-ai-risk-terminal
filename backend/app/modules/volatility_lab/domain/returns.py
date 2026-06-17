from math import prod
from typing import Any


def calculate_simple_returns(prices: list[float]) -> list[float]:
    return [
        (prices[index] / prices[index - 1]) - 1.0
        for index in range(1, len(prices))
        if prices[index - 1] != 0
    ]


def calculate_cumulative_returns(returns: list[float]) -> list[float]:
    wealth = 1.0
    cumulative_returns = []
    for daily_return in returns:
        wealth *= 1.0 + daily_return
        cumulative_returns.append(wealth - 1.0)
    return cumulative_returns


def arithmetic_mean(returns: list[float]) -> float:
    return sum(returns) / len(returns) if returns else 0.0


def geometric_mean(returns: list[float]) -> float:
    if not returns:
        return 0.0
    compounded = prod(1.0 + daily_return for daily_return in returns)
    return compounded ** (1.0 / len(returns)) - 1.0


def holding_period_return(prices: list[float]) -> float:
    if len(prices) < 2 or prices[0] == 0:
        return 0.0
    return (prices[-1] / prices[0]) - 1.0


def annualized_return(returns: list[float], periods_per_year: int = 252) -> float:
    if not returns:
        return 0.0
    return (1.0 + geometric_mean(returns)) ** periods_per_year - 1.0


def excess_return(asset_return: float, risk_free_rate: float) -> float:
    return asset_return - risk_free_rate


def active_return(asset_return: float, benchmark_return: float) -> float:
    return asset_return - benchmark_return


def align_return_series(
    series_by_symbol: dict[str, list[dict[str, Any]]],
) -> tuple[list[str], list[str], dict[str, list[float]]]:
    if not series_by_symbol:
        return [], [], {}

    common_dates = set.intersection(
        *[
            {str(point["date"]) for point in series}
            for series in series_by_symbol.values()
            if series
        ],
    )
    dates = sorted(common_dates)
    aligned: dict[str, list[float]] = {}

    for symbol, series in series_by_symbol.items():
        values_by_date = {
            str(point["date"]): float(point["return"])
            for point in series
            if str(point["date"]) in common_dates
        }
        aligned[symbol] = [values_by_date[date] for date in dates]

    return dates, list(series_by_symbol), aligned
