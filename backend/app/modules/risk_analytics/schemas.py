from pydantic import BaseModel


class ReturnSeriesResult(BaseModel):
    symbols_requested: list[str]
    symbols_found: list[str]
    symbols_missing: list[str]
    dates: list[str]
    return_series_by_symbol: dict[str, list[float]]
    observations: int
    data_source: str
    quality_warnings: list[str]


class RealizedRiskResult(BaseModel):
    metric_source: str
    fallback_used: bool
    fallback_reason: str | None
    observations: int
    symbols_found: list[str]
    symbols_missing: list[str]
    quality_warnings: list[str]
    portfolio_returns: list[float]
    benchmark_returns: list[float]
    realized_annualized_return: float | None
    realized_volatility: float | None
    covariance_matrix: list[list[float]]
    covariance_symbols: list[str]
    portfolio_var_95: float | None
    portfolio_cvar_95: float | None
    tracking_error: float | None
    realized_sharpe_ratio: float | None
    max_drawdown: float | None
