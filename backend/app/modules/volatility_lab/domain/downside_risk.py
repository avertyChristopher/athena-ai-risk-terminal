from app.modules.volatility_lab.domain.returns import calculate_cumulative_returns


def semi_variance(returns: list[float], target_return: float = 0.0) -> float:
    downside_returns = [value for value in returns if value < target_return]
    if not downside_returns:
        return 0.0
    return (
        sum((value - target_return) ** 2 for value in downside_returns)
        / len(downside_returns)
    )


def semi_deviation(returns: list[float], target_return: float = 0.0) -> float:
    return semi_variance(returns, target_return) ** 0.5


def downside_deviation(
    returns: list[float],
    target_return: float = 0.0,
    periods_per_year: int = 252,
) -> float:
    return semi_deviation(returns, target_return) * (periods_per_year ** 0.5)


def max_drawdown_from_returns(returns: list[float]) -> float:
    wealth_path = [1.0 + value for value in calculate_cumulative_returns(returns)]
    peak = 1.0
    max_drawdown = 0.0
    for wealth in wealth_path:
        peak = max(peak, wealth)
        drawdown = (wealth / peak) - 1.0
        max_drawdown = min(max_drawdown, drawdown)
    return max_drawdown


def historical_var(returns: list[float], confidence_level: float = 0.95) -> float:
    if not returns:
        return 0.0
    sorted_returns = sorted(returns)
    index = max(0, min(len(sorted_returns) - 1, int((1.0 - confidence_level) * len(sorted_returns))))
    return abs(min(sorted_returns[index], 0.0))


def historical_cvar(returns: list[float], confidence_level: float = 0.95) -> float:
    if not returns:
        return 0.0
    sorted_returns = sorted(returns)
    index = max(0, min(len(sorted_returns) - 1, int((1.0 - confidence_level) * len(sorted_returns))))
    tail_returns = sorted_returns[: index + 1]
    return abs(min(sum(tail_returns) / len(tail_returns), 0.0))


def probability_negative_return(returns: list[float]) -> float:
    if not returns:
        return 0.0
    return len([value for value in returns if value < 0]) / len(returns)
