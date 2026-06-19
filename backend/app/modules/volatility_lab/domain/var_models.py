from random import Random
from statistics import NormalDist

from math import sqrt

from app.modules.volatility_lab.domain.volatility import standard_deviation


def historical_var(returns: list[float], confidence_level: float = 0.95) -> float:
    if not returns:
        return 0.0
    sorted_returns = sorted(returns)
    index = _tail_index(len(sorted_returns), confidence_level)
    return abs(min(sorted_returns[index], 0.0))


def historical_cvar(returns: list[float], confidence_level: float = 0.95) -> float:
    if not returns:
        return 0.0
    sorted_returns = sorted(returns)
    index = _tail_index(len(sorted_returns), confidence_level)
    tail_returns = sorted_returns[: index + 1]
    return abs(min(sum(tail_returns) / len(tail_returns), 0.0))


def parametric_var(
    returns: list[float],
    confidence_level: float = 0.95,
    horizon_days: int = 1,
) -> float:
    if not returns:
        return 0.0
    mean_return = sum(returns) / len(returns)
    sigma = standard_deviation(returns)
    lower_tail_z = NormalDist().inv_cdf(1.0 - confidence_level)
    lower_tail_return = mean_return + lower_tail_z * sigma
    return abs(min(lower_tail_return, 0.0)) * sqrt(max(horizon_days, 1))


def parametric_cvar(
    returns: list[float],
    confidence_level: float = 0.95,
    horizon_days: int = 1,
) -> float:
    if not returns:
        return 0.0
    mean_return = sum(returns) / len(returns)
    sigma = standard_deviation(returns)
    if sigma == 0:
        return abs(min(mean_return, 0.0)) * sqrt(max(horizon_days, 1))
    tail_probability = 1.0 - confidence_level
    lower_tail_z = NormalDist().inv_cdf(tail_probability)
    density = _standard_normal_pdf(lower_tail_z)
    expected_tail_return = mean_return - sigma * density / tail_probability
    return abs(min(expected_tail_return, 0.0)) * sqrt(max(horizon_days, 1))


def monte_carlo_var(
    returns: list[float],
    confidence_level: float = 0.95,
    simulations: int = 2000,
    seed: int = 42,
) -> float:
    simulated_returns = _simulate_normal_returns(returns, simulations, seed)
    return historical_var(simulated_returns, confidence_level)


def monte_carlo_cvar(
    returns: list[float],
    confidence_level: float = 0.95,
    simulations: int = 2000,
    seed: int = 42,
) -> float:
    simulated_returns = _simulate_normal_returns(returns, simulations, seed)
    return historical_cvar(simulated_returns, confidence_level)


def _simulate_normal_returns(
    returns: list[float],
    simulations: int,
    seed: int,
) -> list[float]:
    if not returns:
        return []
    mean_return = sum(returns) / len(returns)
    sigma = standard_deviation(returns)
    rng = Random(seed)
    return [rng.gauss(mean_return, sigma) for _ in range(simulations)]


def _tail_index(length: int, confidence_level: float) -> int:
    return max(0, min(length - 1, int((1.0 - confidence_level) * length)))


def _standard_normal_pdf(value: float) -> float:
    return NormalDist().pdf(value)
