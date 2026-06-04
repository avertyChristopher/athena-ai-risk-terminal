from math import sqrt
from statistics import mean
from typing import Sequence

from app.modules.market_data.domain.returns import calculate_drawdown

TRADING_DAYS_PER_YEAR = 252


def calculate_arithmetic_mean_return(returns: Sequence[float]) -> float:
    _validate_returns(returns)
    return mean(returns)


def calculate_geometric_mean_return(returns: Sequence[float]) -> float:
    _validate_returns(returns)
    compounded_return = 1.0

    for period_return in returns:
        compounded_return *= 1.0 + period_return

    return compounded_return ** (1.0 / len(returns)) - 1.0


def calculate_annualized_return(
    returns: Sequence[float],
    trading_days: int = TRADING_DAYS_PER_YEAR,
) -> float:
    if trading_days <= 0:
        raise ValueError("Trading days must be positive.")

    geometric_mean = calculate_geometric_mean_return(returns)
    return (1.0 + geometric_mean) ** trading_days - 1.0


def calculate_variance(returns: Sequence[float]) -> float:
    _validate_returns(returns, minimum_length=2)
    average_return = mean(returns)
    return sum((value - average_return) ** 2 for value in returns) / (len(returns) - 1)


def calculate_standard_deviation(returns: Sequence[float]) -> float:
    return sqrt(calculate_variance(returns))


def calculate_skewness(returns: Sequence[float]) -> float:
    _validate_returns(returns, minimum_length=3)
    average_return = mean(returns)
    population_variance = sum((value - average_return) ** 2 for value in returns) / len(
        returns,
    )

    if population_variance == 0:
        return 0.0

    third_moment = (
        sum((value - average_return) ** 3 for value in returns) / len(returns)
    )
    return third_moment / (population_variance ** 1.5)


def calculate_kurtosis(returns: Sequence[float]) -> float:
    _validate_returns(returns, minimum_length=4)
    average_return = mean(returns)
    population_variance = sum((value - average_return) ** 2 for value in returns) / len(
        returns,
    )

    if population_variance == 0:
        return 0.0

    fourth_moment = sum((value - average_return) ** 4 for value in returns) / len(
        returns,
    )
    return fourth_moment / (population_variance**2) - 3.0


def calculate_percentiles(
    values: Sequence[float],
    percentiles: Sequence[float] = (5, 25, 50, 75, 95),
) -> dict[str, float]:
    _validate_returns(values)

    sorted_values = sorted(values)
    percentile_values = {}

    for percentile in percentiles:
        if percentile < 0 or percentile > 100:
            raise ValueError("Percentiles must be between 0 and 100.")

        rank = (percentile / 100) * (len(sorted_values) - 1)
        lower_index = int(rank)
        upper_index = min(lower_index + 1, len(sorted_values) - 1)
        weight = rank - lower_index
        value = sorted_values[lower_index] * (1 - weight) + sorted_values[
            upper_index
        ] * weight
        percentile_values[f"p{int(percentile)}"] = value

    return percentile_values


def calculate_max_drawdown(values: Sequence[float]) -> float:
    return min(calculate_drawdown(values))


def calculate_covariance(
    first_returns: Sequence[float],
    second_returns: Sequence[float],
) -> float:
    first, second = _align_return_series(first_returns, second_returns)
    first_mean = mean(first)
    second_mean = mean(second)

    return sum(
        (first_value - first_mean) * (second_value - second_mean)
        for first_value, second_value in zip(first, second)
    ) / (len(first) - 1)


def calculate_correlation(
    first_returns: Sequence[float],
    second_returns: Sequence[float],
) -> float:
    first, second = _align_return_series(first_returns, second_returns)
    first_stdev = calculate_standard_deviation(first)
    second_stdev = calculate_standard_deviation(second)

    if first_stdev == 0 or second_stdev == 0:
        return 0.0

    return calculate_covariance(first, second) / (first_stdev * second_stdev)


def calculate_beta(
    asset_returns: Sequence[float],
    benchmark_returns: Sequence[float],
) -> float:
    _, benchmark = _align_return_series(asset_returns, benchmark_returns)
    benchmark_variance = calculate_variance(benchmark)

    if benchmark_variance == 0:
        return 0.0

    return calculate_covariance(asset_returns, benchmark_returns) / benchmark_variance


def calculate_sharpe_ratio(
    returns: Sequence[float],
    annual_risk_free_rate: float = 0.02,
    trading_days: int = TRADING_DAYS_PER_YEAR,
) -> float:
    if trading_days <= 0:
        raise ValueError("Trading days must be positive.")

    standard_deviation = calculate_standard_deviation(returns)
    if standard_deviation == 0:
        return 0.0

    daily_risk_free_rate = annual_risk_free_rate / trading_days
    excess_return = mean(returns) - daily_risk_free_rate
    return (excess_return / standard_deviation) * sqrt(trading_days)


def calculate_moving_average(values: Sequence[float], window: int) -> float | None:
    if window <= 0:
        raise ValueError("Moving average window must be positive.")

    if len(values) < window:
        return None

    return mean(values[-window:])


def _validate_returns(returns: Sequence[float], minimum_length: int = 1) -> None:
    if len(returns) < minimum_length:
        raise ValueError(f"At least {minimum_length} returns are required.")


def _align_return_series(
    first_returns: Sequence[float],
    second_returns: Sequence[float],
) -> tuple[list[float], list[float]]:
    length = min(len(first_returns), len(second_returns))
    if length < 2:
        raise ValueError("At least two aligned returns are required.")

    return list(first_returns[-length:]), list(second_returns[-length:])
