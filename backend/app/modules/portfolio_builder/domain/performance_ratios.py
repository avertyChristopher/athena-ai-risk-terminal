from collections.abc import Sequence


def calculate_sharpe_ratio(
    portfolio_return: float,
    risk_free_rate: float,
    standard_deviation: float | None,
) -> float | None:
    if not standard_deviation:
        return None
    return (portfolio_return - risk_free_rate) / standard_deviation


def calculate_treynor_ratio(
    portfolio_return: float,
    risk_free_rate: float,
    beta: float | None,
) -> float | None:
    if not beta:
        return None
    return (portfolio_return - risk_free_rate) / beta


def calculate_jensen_alpha(
    portfolio_return: float,
    required_return: float,
) -> float:
    return portfolio_return - required_return


def calculate_active_return(
    portfolio_return: float,
    benchmark_return: float,
) -> float:
    return portfolio_return - benchmark_return


def calculate_tracking_error(active_returns: Sequence[float]) -> float | None:
    if len(active_returns) < 2:
        return None

    mean = sum(active_returns) / len(active_returns)
    variance = sum((active_return - mean) ** 2 for active_return in active_returns) / (
        len(active_returns) - 1
    )
    return variance**0.5


def calculate_information_ratio(
    active_return: float,
    tracking_error: float | None,
) -> float | None:
    if not tracking_error:
        return None
    return active_return / tracking_error
