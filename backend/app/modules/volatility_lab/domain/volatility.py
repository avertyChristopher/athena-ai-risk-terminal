from math import sqrt


def variance(returns: list[float]) -> float:
    if len(returns) < 2:
        return 0.0
    mean_return = sum(returns) / len(returns)
    return sum((value - mean_return) ** 2 for value in returns) / (len(returns) - 1)


def standard_deviation(returns: list[float]) -> float:
    return sqrt(variance(returns))


def annualized_volatility(
    returns: list[float],
    periods_per_year: int = 252,
) -> float:
    return standard_deviation(returns) * sqrt(periods_per_year)


def coefficient_of_variation(returns: list[float]) -> float | None:
    if not returns:
        return None
    mean_return = sum(returns) / len(returns)
    if mean_return == 0:
        return None
    return standard_deviation(returns) / abs(mean_return)
