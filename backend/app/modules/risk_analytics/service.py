from app.modules.market_data.domain.panels import build_returns_panel
from app.modules.market_data.repository import MarketDataRepository
from app.modules.risk_analytics.domain import (
    align_return_series_by_symbol,
    calculate_annualized_return,
    calculate_annualized_volatility,
    calculate_covariance_matrix,
    calculate_historical_cvar,
    calculate_historical_var,
    calculate_max_drawdown_from_returns,
    calculate_portfolio_variance_from_covariance,
    calculate_sharpe_ratio,
    calculate_tracking_error,
    calculate_weighted_portfolio_returns,
)
from app.modules.risk_analytics.schemas import (
    RealizedRiskResult,
    ReturnSeriesResult,
)


class RiskAnalyticsService:
    def __init__(self, market_data_repository: MarketDataRepository) -> None:
        self.market_data_repository = market_data_repository

    def get_return_series(
        self,
        symbols: list[str],
        start_date: str | None = None,
        end_date: str | None = None,
        return_type: str = "price_return",
    ) -> ReturnSeriesResult:
        requested_symbols = _normalize_symbols(symbols)
        available_symbols = {
            symbol.upper()
            for symbol in self.market_data_repository.get_supported_symbols()
        }
        found_symbols = [
            symbol for symbol in requested_symbols if symbol in available_symbols
        ]
        missing_symbols = [
            symbol for symbol in requested_symbols if symbol not in available_symbols
        ]
        series_by_symbol = {
            symbol: self._filter_rows_by_date(
                self.market_data_repository.get_prices(symbol),
                start_date,
                end_date,
            )
            for symbol in found_symbols
        }
        panel_rows = build_returns_panel(series_by_symbol, return_type)
        dates, return_series_by_symbol = align_return_series_by_symbol(
            panel_rows,
            found_symbols,
        )
        quality_warnings = []
        if missing_symbols:
            quality_warnings.append(
                f"Missing return history for: {', '.join(missing_symbols)}.",
            )
        if found_symbols and len(dates) < 2:
            quality_warnings.append("Insufficient aligned return observations.")
        if not found_symbols:
            quality_warnings.append("No requested symbols are available in Market Data.")

        return ReturnSeriesResult(
            symbols_requested=requested_symbols,
            symbols_found=found_symbols,
            symbols_missing=missing_symbols,
            dates=dates,
            return_series_by_symbol=return_series_by_symbol,
            observations=len(dates),
            data_source="market_data_demo",
            quality_warnings=quality_warnings,
        )

    def calculate_realized_portfolio_risk(
        self,
        weights_by_symbol: dict[str, float],
        benchmark_symbol: str | None = None,
        annual_risk_free_rate: float = 0.02,
    ) -> RealizedRiskResult:
        requested_symbols = _normalize_symbols(list(weights_by_symbol))
        symbols_for_returns = list(requested_symbols)
        normalized_benchmark = benchmark_symbol.upper() if benchmark_symbol else None
        if normalized_benchmark and normalized_benchmark not in symbols_for_returns:
            symbols_for_returns.append(normalized_benchmark)

        return_series = self.get_return_series(symbols_for_returns)
        missing_portfolio_symbols = [
            symbol
            for symbol in requested_symbols
            if symbol not in return_series.symbols_found
        ]
        if missing_portfolio_symbols or return_series.observations < 2:
            return self._fallback_result(
                return_series,
                fallback_reason=(
                    "Realized Market Data return series unavailable. Falling back to deterministic demo assumptions."
                ),
                benchmark_symbol=normalized_benchmark,
            )

        normalized_weights = {
            symbol.upper(): weight
            for symbol, weight in weights_by_symbol.items()
            if symbol.upper() in return_series.return_series_by_symbol
        }
        total_weight = sum(normalized_weights.values())
        if total_weight <= 0:
            return self._fallback_result(
                return_series,
                fallback_reason="Portfolio weights are unavailable for realized risk analytics.",
                benchmark_symbol=normalized_benchmark,
            )
        normalized_weights = {
            symbol: weight / total_weight
            for symbol, weight in normalized_weights.items()
        }
        portfolio_returns = calculate_weighted_portfolio_returns(
            return_series.return_series_by_symbol,
            normalized_weights,
        )
        if len(portfolio_returns) < 2:
            return self._fallback_result(
                return_series,
                fallback_reason="Insufficient weighted portfolio return observations.",
                benchmark_symbol=normalized_benchmark,
            )

        covariance_symbols = list(normalized_weights)
        covariance_matrix = calculate_covariance_matrix(
            return_series.return_series_by_symbol,
            covariance_symbols,
        )
        covariance_weights = [normalized_weights[symbol] for symbol in covariance_symbols]
        covariance_volatility = (
            calculate_portfolio_variance_from_covariance(
                covariance_weights,
                covariance_matrix,
            )
            ** 0.5
        )
        benchmark_returns = (
            return_series.return_series_by_symbol.get(normalized_benchmark, [])
            if normalized_benchmark
            else []
        )
        tracking_error = (
            calculate_tracking_error(portfolio_returns, benchmark_returns)
            if len(benchmark_returns) >= 2
            else None
        )
        warnings = list(return_series.quality_warnings)
        if normalized_benchmark and not benchmark_returns:
            warnings.append("Benchmark return history is unavailable.")

        return RealizedRiskResult(
            metric_source="realized_market_data",
            fallback_used=False,
            fallback_reason=None,
            observations=len(portfolio_returns),
            symbols_found=return_series.symbols_found,
            symbols_missing=return_series.symbols_missing,
            quality_warnings=warnings,
            portfolio_returns=portfolio_returns,
            benchmark_returns=benchmark_returns,
            realized_annualized_return=calculate_annualized_return(portfolio_returns),
            realized_volatility=covariance_volatility
            or calculate_annualized_volatility(portfolio_returns),
            covariance_matrix=covariance_matrix,
            covariance_symbols=covariance_symbols,
            portfolio_var_95=calculate_historical_var(portfolio_returns),
            portfolio_cvar_95=calculate_historical_cvar(portfolio_returns),
            tracking_error=tracking_error,
            realized_sharpe_ratio=calculate_sharpe_ratio(
                portfolio_returns,
                annual_risk_free_rate,
            ),
            max_drawdown=calculate_max_drawdown_from_returns(portfolio_returns),
        )

    def _fallback_result(
        self,
        return_series: ReturnSeriesResult,
        *,
        fallback_reason: str,
        benchmark_symbol: str | None,
    ) -> RealizedRiskResult:
        return RealizedRiskResult(
            metric_source="deterministic_demo",
            fallback_used=True,
            fallback_reason=fallback_reason,
            observations=return_series.observations,
            symbols_found=return_series.symbols_found,
            symbols_missing=return_series.symbols_missing,
            quality_warnings=[
                *return_series.quality_warnings,
                fallback_reason,
            ],
            portfolio_returns=[],
            benchmark_returns=return_series.return_series_by_symbol.get(
                benchmark_symbol,
                [],
            )
            if benchmark_symbol
            else [],
            realized_annualized_return=None,
            realized_volatility=None,
            covariance_matrix=[],
            covariance_symbols=[],
            portfolio_var_95=None,
            portfolio_cvar_95=None,
            tracking_error=None,
            realized_sharpe_ratio=None,
            max_drawdown=None,
        )

    def _filter_rows_by_date(
        self,
        rows: list[dict[str, object]],
        start_date: str | None,
        end_date: str | None,
    ) -> list[dict[str, object]]:
        return [
            row
            for row in rows
            if (start_date is None or str(row["date"]) >= start_date)
            and (end_date is None or str(row["date"]) <= end_date)
        ]


def _normalize_symbols(symbols: list[str]) -> list[str]:
    normalized_symbols: list[str] = []
    for symbol in symbols:
        normalized_symbol = symbol.strip().upper()
        if normalized_symbol and normalized_symbol not in normalized_symbols:
            normalized_symbols.append(normalized_symbol)
    return normalized_symbols
