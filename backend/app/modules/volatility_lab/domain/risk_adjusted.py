from app.modules.volatility_lab.domain.downside_risk import downside_deviation
from app.modules.volatility_lab.domain.returns import annualized_return
from app.modules.volatility_lab.domain.volatility import annualized_volatility, standard_deviation


def sharpe_ratio(
    returns: list[float],
    risk_free_rate: float = 0.02,
    periods_per_year: int = 252,
) -> float | None:
    volatility = annualized_volatility(returns, periods_per_year)
    if volatility == 0:
        return None
    return (annualized_return(returns, periods_per_year) - risk_free_rate) / volatility


def sortino_ratio(
    returns: list[float],
    risk_free_rate: float = 0.02,
    periods_per_year: int = 252,
) -> float | None:
    downside = downside_deviation(returns, 0.0, periods_per_year)
    if downside == 0:
        return None
    return (annualized_return(returns, periods_per_year) - risk_free_rate) / downside


def treynor_ratio(
    returns: list[float],
    beta: float,
    risk_free_rate: float = 0.02,
    periods_per_year: int = 252,
) -> float | None:
    if beta == 0:
        return None
    return (annualized_return(returns, periods_per_year) - risk_free_rate) / beta


def tracking_error(
    asset_returns: list[float],
    benchmark_returns: list[float],
    periods_per_year: int = 252,
) -> float | None:
    length = min(len(asset_returns), len(benchmark_returns))
    if length < 2:
        return None
    active_returns = [
        asset_returns[-length + index] - benchmark_returns[-length + index]
        for index in range(length)
    ]
    return standard_deviation(active_returns) * (periods_per_year ** 0.5)


def information_ratio(
    asset_returns: list[float],
    benchmark_returns: list[float],
    periods_per_year: int = 252,
) -> float | None:
    length = min(len(asset_returns), len(benchmark_returns))
    if length < 2:
        return None
    active_return = annualized_return(asset_returns[-length:], periods_per_year) - annualized_return(
        benchmark_returns[-length:],
        periods_per_year,
    )
    tracking_error_value = tracking_error(
        asset_returns[-length:],
        benchmark_returns[-length:],
        periods_per_year,
    )
    if tracking_error_value in {None, 0}:
        return None
    return active_return / tracking_error_value
