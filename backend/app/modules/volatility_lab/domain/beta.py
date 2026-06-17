from app.modules.volatility_lab.domain.covariance import covariance
from app.modules.volatility_lab.domain.returns import annualized_return
from app.modules.volatility_lab.domain.volatility import variance


def calculate_beta(asset_returns: list[float], benchmark_returns: list[float]) -> float:
    benchmark_variance = variance(benchmark_returns)
    if benchmark_variance == 0:
        return 0.0
    return covariance(asset_returns, benchmark_returns) / benchmark_variance


def capm_required_return(
    risk_free_rate: float,
    beta: float,
    market_return: float,
) -> float:
    return risk_free_rate + beta * (market_return - risk_free_rate)


def jensen_alpha(
    asset_returns: list[float],
    benchmark_returns: list[float],
    risk_free_rate: float,
    periods_per_year: int = 252,
) -> float:
    beta = calculate_beta(asset_returns, benchmark_returns)
    asset_return = annualized_return(asset_returns, periods_per_year)
    market_return = annualized_return(benchmark_returns, periods_per_year)
    return asset_return - capm_required_return(risk_free_rate, beta, market_return)
