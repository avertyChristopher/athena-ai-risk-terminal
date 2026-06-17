from datetime import date, timedelta
from math import prod
from typing import Any

from fastapi import HTTPException

from app.modules.volatility_lab.domain.beta import (
    calculate_beta,
    capm_required_return,
    jensen_alpha,
)
from app.modules.volatility_lab.domain.commentary import (
    build_asset_commentary,
    build_portfolio_commentary,
)
from app.modules.volatility_lab.domain.correlation import (
    correlation,
    correlation_matrix,
)
from app.modules.volatility_lab.domain.covariance import (
    covariance,
    covariance_matrix,
)
from app.modules.volatility_lab.domain.distribution import distribution_summary
from app.modules.volatility_lab.domain.downside_risk import (
    downside_deviation,
    max_drawdown_from_returns,
    probability_negative_return,
    semi_deviation,
    semi_variance,
)
from app.modules.volatility_lab.domain.ewma import ewma_volatility
from app.modules.volatility_lab.domain.portfolio_volatility import (
    diversification_benefit,
    portfolio_volatility,
    risk_contribution,
    weighted_portfolio_returns,
)
from app.modules.volatility_lab.domain.regimes import classify_volatility_regime
from app.modules.volatility_lab.domain.returns import (
    active_return,
    align_return_series,
    annualized_return,
    arithmetic_mean,
    calculate_cumulative_returns,
    calculate_simple_returns,
    excess_return,
    geometric_mean,
    holding_period_return,
)
from app.modules.volatility_lab.domain.risk_adjusted import (
    information_ratio,
    sharpe_ratio,
    sortino_ratio,
    tracking_error,
    treynor_ratio,
)
from app.modules.volatility_lab.domain.rolling_volatility import (
    rolling_summary,
    rolling_volatility,
)
from app.modules.volatility_lab.domain.volatility import (
    annualized_volatility,
    coefficient_of_variation,
    standard_deviation,
    variance,
)
from app.modules.volatility_lab.domain.var_models import (
    historical_cvar,
    historical_var,
    monte_carlo_cvar,
    monte_carlo_var,
    parametric_cvar,
    parametric_var,
)
from app.modules.volatility_lab.repository import VolatilityLabRepository
from app.modules.volatility_lab.schemas import (
    AdvancedModelsStatus,
    AthenaVolatilityCommentary,
    BenchmarkRiskSummary,
    DistributionSummary,
    DrawdownPoint,
    DownsideRiskSummary,
    EWMAVolatilitySummary,
    MatrixSummary,
    PortfolioRiskSummary,
    ReturnSummary,
    RiskMonitorPayload,
    RiskAdjustedSummary,
    RiskContributionItem,
    RollingVolatilityPoint,
    VarModelSummary,
    VolatilityAssetAnalysisRequest,
    VolatilityAssetAnalysisResponse,
    VolatilityDataSource,
    VolatilityLabStatus,
    VolatilityPortfolioAnalysisRequest,
    VolatilityPortfolioAnalysisResponse,
    VolatilityRegimeSummary,
    VolatilitySummary,
)


class VolatilityLabService:
    def __init__(self, repository: VolatilityLabRepository) -> None:
        self.repository = repository

    def get_status(self) -> VolatilityLabStatus:
        return VolatilityLabStatus(
            detail=(
                "Volatility Lab is ready for realized volatility, beta, "
                "covariance, VaR/CVaR and portfolio risk analysis."
            ),
            engines_available=[
                "single_asset_realized_volatility",
                "portfolio_covariance",
                "beta_capm",
                "historical_var_cvar",
                "parametric_var_cvar",
                "ewma_volatility",
                "risk_monitor_payload",
                "cfa_commentary",
            ],
        )

    def analyze_asset(
        self,
        payload: VolatilityAssetAnalysisRequest,
    ) -> VolatilityAssetAnalysisResponse:
        self._validate_date_range(payload.start_date, payload.end_date)
        symbol = payload.symbol.upper()
        benchmark_symbol = payload.benchmark_symbol.upper()
        asset_series = self._return_series_for_symbol(
            symbol,
            payload.start_date,
            payload.end_date,
        )
        benchmark_series = self._return_series_for_symbol(
            benchmark_symbol,
            payload.start_date,
            payload.end_date,
        )
        fallback_used = False
        asset_fallback_used = False
        benchmark_fallback_used = False
        warnings = []

        if not asset_series:
            asset_series = self._demo_return_series(symbol)
            fallback_used = True
            asset_fallback_used = True
            warnings.append(
                f"{symbol}: Market Data return series unavailable; demo assumptions used.",
            )
        if not benchmark_series:
            benchmark_series = self._demo_return_series(benchmark_symbol)
            fallback_used = True
            benchmark_fallback_used = True
            warnings.append(
                f"{benchmark_symbol}: benchmark return series unavailable; demo assumptions used.",
            )

        dates, _, aligned = align_return_series(
            {symbol: asset_series, benchmark_symbol: benchmark_series},
        )
        asset_returns = aligned.get(symbol, [])
        benchmark_returns = aligned.get(benchmark_symbol, [])
        if len(asset_returns) < payload.rolling_window:
            warnings.append(
                "Insufficient observations for the selected rolling window.",
            )
        latest_price = self._latest_price(symbol, payload.start_date, payload.end_date)
        rolling_points = rolling_volatility(
            asset_returns,
            dates,
            payload.rolling_window,
            payload.annualization_factor,
        )
        rolling_values = [float(point["volatility"]) for point in rolling_points]
        regime = classify_volatility_regime(
            rolling_values[-1] if rolling_values else None,
            rolling_values,
        )
        beta_value = calculate_beta(asset_returns, benchmark_returns)
        correlation_value = correlation(asset_returns, benchmark_returns)
        covariance_value = covariance(asset_returns, benchmark_returns)
        asset_annual_return = annualized_return(
            asset_returns,
            payload.annualization_factor,
        )
        benchmark_annual_return = annualized_return(
            benchmark_returns,
            payload.annualization_factor,
        )
        capm_return = capm_required_return(
            payload.risk_free_rate,
            beta_value,
            benchmark_annual_return,
        )
        max_drawdown = max_drawdown_from_returns(asset_returns)
        annual_volatility = annualized_volatility(
            asset_returns,
            payload.annualization_factor,
        )
        commentary_points = build_asset_commentary(
            symbol,
            str(regime["regime"]),
            beta_value,
            correlation_value,
            annual_volatility,
            max_drawdown,
        )
        metric_source = (
            "deterministic_demo"
            if asset_fallback_used
            else "partial_data" if benchmark_fallback_used else "realized_market_data"
        )
        data_source = self._data_source(
            metric_source=metric_source,
            fallback_used=fallback_used,
            fallback_reason=(
                "Market Data return series unavailable or incomplete."
                if fallback_used
                else None
            ),
            observations=len(asset_returns),
            symbols_found=[] if asset_fallback_used else [symbol],
            symbols_missing=[
                missing_symbol
                for missing_symbol, missing in [
                    (symbol, asset_fallback_used),
                    (benchmark_symbol, benchmark_fallback_used),
                ]
                if missing
            ],
            warnings=warnings,
        )
        volatility_summary = self._volatility_summary(
            asset_returns,
            rolling_points,
            payload.annualization_factor,
        )
        downside_summary = self._downside_summary(
            asset_returns,
            payload.confidence_level,
            payload.annualization_factor,
        )
        benchmark_risk = BenchmarkRiskSummary(
            benchmark_symbol=benchmark_symbol,
            covariance=covariance_value,
            correlation=correlation_value,
            beta=beta_value,
            capm_required_return=capm_return,
            jensen_alpha=jensen_alpha(
                asset_returns,
                benchmark_returns,
                payload.risk_free_rate,
                payload.annualization_factor,
            ),
            systematic_risk_note=self._beta_note(beta_value),
            diversification_note=self._correlation_note(correlation_value),
        )
        risk_adjusted_summary = self._risk_adjusted(
            asset_returns,
            benchmark_returns,
            beta_value,
            payload.risk_free_rate,
            payload.annualization_factor,
        )
        ewma_summary = self._ewma_summary(
            asset_returns,
            payload.annualization_factor,
            data_source,
        )
        var_summary = self._var_summary(
            asset_returns,
            payload.confidence_level,
            self._stable_seed(symbol),
        )

        return VolatilityAssetAnalysisResponse(
            symbol=symbol,
            benchmark_symbol=benchmark_symbol,
            latest_price=latest_price,
            return_summary=self._return_summary(
                asset_returns,
                payload.risk_free_rate,
                payload.annualization_factor,
                benchmark_returns,
            ),
            volatility_summary=volatility_summary,
            rolling_volatility=[
                RollingVolatilityPoint.model_validate(point)
                for point in rolling_points
            ],
            drawdown_series=self._drawdown_series(dates, asset_returns),
            ewma_volatility=ewma_summary,
            var_models=var_summary,
            downside_risk=downside_summary,
            benchmark_risk=benchmark_risk,
            distribution=self._distribution(asset_returns),
            risk_adjusted=risk_adjusted_summary,
            volatility_regime=VolatilityRegimeSummary.model_validate(regime),
            advanced_models=self._advanced_models(),
            risk_monitor_payload=self._risk_monitor_payload(
                confidence_level=payload.confidence_level,
                volatility_summary=volatility_summary,
                ewma_summary=ewma_summary,
                var_summary=var_summary,
                beta_value=beta_value,
                correlation_value=correlation_value,
                tracking_error_value=risk_adjusted_summary.tracking_error,
                risk_adjusted=risk_adjusted_summary,
                max_drawdown=downside_summary.max_drawdown,
                risk_contributions=[],
                covariance_summary=None,
                correlation_summary=None,
                data_source=data_source,
            ),
            data_source=data_source,
            athena_commentary=AthenaVolatilityCommentary(
                summary=(
                    f"{symbol} annualized return is {asset_annual_return:.1%} "
                    f"versus benchmark {benchmark_annual_return:.1%}."
                ),
                key_points=commentary_points,
                trade_simulator_reuse_note=(
                    "Volatility Lab provides realized risk inputs that can be "
                    "reused by pre-trade simulation."
                ),
                cfa_notes=self._cfa_notes(),
            ),
        )

    def analyze_portfolio(
        self,
        payload: VolatilityPortfolioAnalysisRequest,
    ) -> VolatilityPortfolioAnalysisResponse:
        self._validate_date_range(payload.start_date, payload.end_date)
        portfolio = self.repository.get_portfolio(payload.portfolio_id)
        if portfolio is None:
            raise HTTPException(status_code=404, detail="Portfolio not found.")

        positions = self.repository.list_positions(payload.portfolio_id)
        weights = self._position_weights(positions)
        series_by_symbol = {}
        missing_symbols = []

        for symbol in weights:
            series = self._return_series_for_symbol(
                symbol,
                payload.start_date,
                payload.end_date,
            )
            if series:
                series_by_symbol[symbol] = series
            else:
                missing_symbols.append(symbol)

        fallback_used = False
        if not series_by_symbol:
            fallback_used = True
            series_by_symbol = {
                symbol: self._demo_return_series(symbol)
                for symbol in weights
            }
            missing_symbols = list(weights)
        elif missing_symbols:
            fallback_used = True

        dates, included_symbols, aligned_returns = align_return_series(series_by_symbol)
        included_weights = self._normalize_weights(
            {symbol: weights[symbol] for symbol in included_symbols},
        )
        portfolio_returns = weighted_portfolio_returns(
            aligned_returns,
            included_weights,
        )
        warnings = []
        if len(portfolio_returns) < payload.rolling_window:
            warnings.append(
                "Insufficient observations for the selected rolling window.",
            )
        benchmark_symbol = payload.benchmark_symbol.upper()
        benchmark_series = self._return_series_for_symbol(
            benchmark_symbol,
            payload.start_date,
            payload.end_date,
        )
        benchmark_fallback_used = False
        if not benchmark_series:
            benchmark_fallback_used = True
            fallback_used = True
            benchmark_series = self._demo_return_series(benchmark_symbol)
            warnings.append(
                f"{benchmark_symbol}: benchmark return series unavailable; demo assumptions used.",
            )
        benchmark_returns = self._align_to_dates(benchmark_series, dates)
        cov_matrix = covariance_matrix(aligned_returns)
        corr_matrix = correlation_matrix(aligned_returns)
        portfolio_correlation = self._average_off_diagonal(corr_matrix)
        weight_list = [included_weights[symbol] for symbol in included_symbols]
        covariance_based_vol = portfolio_volatility(
            weight_list,
            cov_matrix,
            payload.annualization_factor,
        )
        asset_volatilities = {
            symbol: annualized_volatility(
                aligned_returns[symbol],
                payload.annualization_factor,
            )
            for symbol in included_symbols
        }
        weighted_average_vol = sum(
            included_weights[symbol] * asset_volatilities[symbol]
            for symbol in included_symbols
        )
        contributions = risk_contribution(included_symbols, weight_list, cov_matrix)
        largest_contributor = max(
            contributions,
            key=lambda item: float(item["contribution"]),
            default=None,
        )
        portfolio_beta = calculate_beta(portfolio_returns, benchmark_returns)
        tracking_error_value = tracking_error(
            portfolio_returns,
            benchmark_returns,
            payload.annualization_factor,
        )
        rolling_points = rolling_volatility(
            portfolio_returns,
            dates,
            payload.rolling_window,
            payload.annualization_factor,
        )
        rolling_values = [float(point["volatility"]) for point in rolling_points]
        regime = classify_volatility_regime(
            rolling_values[-1] if rolling_values else None,
            rolling_values,
        )
        diversification = diversification_benefit(
            weighted_average_vol,
            covariance_based_vol,
        )
        commentary_points = build_portfolio_commentary(
            str(portfolio["name"]),
            annualized_volatility(portfolio_returns, payload.annualization_factor),
            diversification,
            str(largest_contributor["symbol"]) if largest_contributor else None,
            tracking_error_value,
        )
        metric_source = (
            "deterministic_demo"
            if fallback_used and len(missing_symbols) == len(weights)
            else "partial_data" if fallback_used else "realized_market_data"
        )
        data_source = self._data_source(
            metric_source=metric_source,
            fallback_used=fallback_used,
            fallback_reason=(
                "Market Data return series unavailable or incomplete."
                if fallback_used
                else None
            ),
            observations=len(portfolio_returns),
            symbols_found=included_symbols,
            symbols_missing=missing_symbols
            + ([benchmark_symbol] if benchmark_fallback_used else []),
            warnings=warnings
            + [
                "Missing holdings use partial realized coverage or demo fallback."
                for _ in [0]
                if missing_symbols
            ],
        )
        volatility_summary = self._volatility_summary(
            portfolio_returns,
            rolling_points,
            payload.annualization_factor,
        )
        downside_summary = self._downside_summary(
            portfolio_returns,
            payload.confidence_level,
            payload.annualization_factor,
        )
        risk_adjusted_summary = self._risk_adjusted(
            portfolio_returns,
            benchmark_returns,
            portfolio_beta,
            payload.risk_free_rate,
            payload.annualization_factor,
        )
        ewma_summary = self._ewma_summary(
            portfolio_returns,
            payload.annualization_factor,
            data_source,
        )
        var_summary = self._var_summary(
            portfolio_returns,
            payload.confidence_level,
            self._stable_seed(payload.portfolio_id),
        )
        risk_contribution_items = [
            RiskContributionItem.model_validate(item)
            for item in contributions
        ]
        covariance_summary = {
            "symbols": included_symbols,
            "matrix_available": bool(cov_matrix),
            "method": "sample_covariance",
        }
        correlation_summary = {
            "symbols": included_symbols,
            "matrix_available": bool(corr_matrix),
            "method": "sample_correlation",
        }

        return VolatilityPortfolioAnalysisResponse(
            portfolio_id=payload.portfolio_id,
            portfolio_name=str(portfolio["name"]),
            benchmark_symbol=benchmark_symbol,
            holdings_included=included_symbols,
            holdings_missing=missing_symbols,
            return_summary=self._return_summary(
                portfolio_returns,
                payload.risk_free_rate,
                payload.annualization_factor,
                benchmark_returns,
            ),
            volatility_summary=volatility_summary,
            rolling_volatility=[
                RollingVolatilityPoint.model_validate(point)
                for point in rolling_points
            ],
            drawdown_series=self._drawdown_series(dates, portfolio_returns),
            ewma_volatility=ewma_summary,
            var_models=var_summary,
            downside_risk=downside_summary,
            portfolio_risk=PortfolioRiskSummary(
                portfolio_volatility=annualized_volatility(
                    portfolio_returns,
                    payload.annualization_factor,
                ),
                covariance_based_volatility=covariance_based_vol,
                weighted_average_asset_volatility=weighted_average_vol,
                diversification_benefit=diversification,
                largest_risk_contributor=(
                    str(largest_contributor["symbol"])
                    if largest_contributor
                    else None
                ),
                beta=portfolio_beta,
                tracking_error=tracking_error_value,
            ),
            covariance_matrix=MatrixSummary(
                symbols=included_symbols,
                matrix=cov_matrix,
                interpretation="Covariance measures how holding returns move together.",
            ),
            correlation_matrix=MatrixSummary(
                symbols=included_symbols,
                matrix=corr_matrix,
                interpretation=(
                    "Lower correlations can improve diversification; high "
                    "positive correlations reduce diversification benefit."
                ),
            ),
            risk_contribution=risk_contribution_items,
            distribution=self._distribution(portfolio_returns),
            risk_adjusted=risk_adjusted_summary,
            volatility_regime=VolatilityRegimeSummary.model_validate(regime),
            advanced_models=self._advanced_models(),
            risk_monitor_payload=self._risk_monitor_payload(
                confidence_level=payload.confidence_level,
                volatility_summary=volatility_summary,
                ewma_summary=ewma_summary,
                var_summary=var_summary,
                beta_value=portfolio_beta,
                correlation_value=portfolio_correlation,
                tracking_error_value=tracking_error_value,
                risk_adjusted=risk_adjusted_summary,
                max_drawdown=downside_summary.max_drawdown,
                risk_contributions=risk_contribution_items,
                covariance_summary=covariance_summary,
                correlation_summary=correlation_summary,
                data_source=data_source,
            ),
            data_source=data_source,
            athena_commentary=AthenaVolatilityCommentary(
                summary=(
                    f"{portfolio['name']} volatility analysis uses "
                    f"{len(included_symbols)} holdings and {len(portfolio_returns)} "
                    "aligned observations."
                ),
                key_points=commentary_points,
                trade_simulator_reuse_note=(
                    "Volatility Lab provides realized risk inputs that can be "
                    "reused by pre-trade simulation."
                ),
                cfa_notes=self._cfa_notes(),
            ),
        )

    def _return_series_for_symbol(
        self,
        symbol: str,
        start_date: str | None,
        end_date: str | None,
    ) -> list[dict[str, object]]:
        rows = self._filtered_price_rows(symbol, start_date, end_date)
        if len(rows) < 2:
            return []
        closes = [float(row["close"]) for row in rows]
        returns = calculate_simple_returns(closes)
        return [
            {"date": str(rows[index]["date"]), "return": returns[index - 1]}
            for index in range(1, len(rows))
        ]

    def _filtered_price_rows(
        self,
        symbol: str,
        start_date: str | None,
        end_date: str | None,
    ) -> list[dict[str, object]]:
        rows = sorted(
            self.repository.get_prices(symbol),
            key=lambda row: str(row["date"]),
        )
        return [
            row
            for row in rows
            if (start_date is None or str(row["date"]) >= start_date)
            and (end_date is None or str(row["date"]) <= end_date)
        ]

    def _latest_price(
        self,
        symbol: str,
        start_date: str | None,
        end_date: str | None,
    ) -> float | None:
        rows = self._filtered_price_rows(symbol, start_date, end_date)
        return float(rows[-1]["close"]) if rows else None

    def _validate_date_range(
        self,
        start_date: str | None,
        end_date: str | None,
    ) -> None:
        if start_date and end_date and start_date > end_date:
            raise HTTPException(
                status_code=422,
                detail="start_date cannot be after end_date.",
            )

    def _drawdown_series(
        self,
        dates: list[str],
        returns: list[float],
    ) -> list[DrawdownPoint]:
        wealth = 1.0
        peak = 1.0
        points = []
        for point_date, point_return in zip(dates, returns):
            wealth *= 1.0 + point_return
            peak = max(peak, wealth)
            points.append(
                DrawdownPoint(
                    date=point_date,
                    drawdown=(wealth / peak) - 1.0,
                ),
            )
        return points

    def _ewma_summary(
        self,
        returns: list[float],
        annualization_factor: int,
        data_source: VolatilityDataSource,
    ) -> EWMAVolatilitySummary:
        summary = ewma_volatility(
            returns,
            lambda_decay=0.94,
            annualization_factor=annualization_factor,
        )
        if data_source.metric_source == "partial_data":
            summary["metric_source"] = "partial_data"
            summary["badge"] = "Partial Data"
        elif data_source.fallback_used:
            summary["metric_source"] = "deterministic_demo"
            summary["badge"] = "Demo assumptions"
        return EWMAVolatilitySummary.model_validate(summary)

    def _var_summary(
        self,
        returns: list[float],
        confidence_level: float,
        seed: int,
    ) -> VarModelSummary:
        has_observations = bool(returns)
        return VarModelSummary(
            confidence_level=confidence_level,
            historical_var=historical_var(returns, confidence_level),
            historical_cvar=historical_cvar(returns, confidence_level),
            parametric_var=parametric_var(returns, confidence_level),
            parametric_cvar=parametric_cvar(returns, confidence_level),
            monte_carlo_var=monte_carlo_var(returns, confidence_level, seed=seed)
            if has_observations
            else None,
            monte_carlo_cvar=monte_carlo_cvar(returns, confidence_level, seed=seed)
            if has_observations
            else None,
            monte_carlo_status=(
                "Demo Monte Carlo with deterministic normal-return simulation."
                if has_observations
                else "Monte Carlo VaR requires return observations."
            ),
            parametric_assumption=(
                "Parametric VaR assumes normally distributed returns."
            ),
            monte_carlo_method=(
                "Deterministic seeded simulation using historical mean and "
                "sample volatility."
            ),
        )

    def _advanced_models(self) -> AdvancedModelsStatus:
        return AdvancedModelsStatus(
            ewma="available",
            garch="planned",
            implied_volatility="requires_options_data",
            volatility_surface="requires_options_chain",
            options_implied_skew="requires_options_chain",
        )

    def _risk_monitor_payload(
        self,
        *,
        confidence_level: float,
        volatility_summary: VolatilitySummary,
        ewma_summary: EWMAVolatilitySummary,
        var_summary: VarModelSummary,
        beta_value: float,
        correlation_value: float,
        tracking_error_value: float | None,
        risk_adjusted: RiskAdjustedSummary,
        max_drawdown: float,
        risk_contributions: list[RiskContributionItem],
        covariance_summary: dict[str, Any] | None,
        correlation_summary: dict[str, Any] | None,
        data_source: VolatilityDataSource,
    ) -> RiskMonitorPayload:
        return RiskMonitorPayload(
            confidence_level=confidence_level,
            annualized_volatility=volatility_summary.annualized_volatility,
            ewma_volatility=ewma_summary.latest_volatility,
            historical_var=var_summary.historical_var,
            historical_cvar=var_summary.historical_cvar,
            parametric_var=var_summary.parametric_var,
            parametric_cvar=var_summary.parametric_cvar,
            beta=beta_value,
            correlation=correlation_value,
            tracking_error=tracking_error_value,
            sharpe_ratio=risk_adjusted.sharpe_ratio,
            sortino_ratio=risk_adjusted.sortino_ratio,
            max_drawdown=max_drawdown,
            risk_contribution=risk_contributions,
            covariance_summary=covariance_summary,
            correlation_summary=correlation_summary,
            data_source=data_source,
            missing_symbols=data_source.symbols_missing,
            fallback_used=data_source.fallback_used,
        )

    def _stable_seed(self, value: str) -> int:
        return sum(ord(character) for character in value.upper()) + 42

    def _average_off_diagonal(self, matrix: list[list[float]]) -> float:
        values = [
            matrix[row][column]
            for row in range(len(matrix))
            for column in range(len(matrix[row]))
            if row != column
        ]
        return sum(values) / len(values) if values else 0.0

    def _demo_return_series(self, symbol: str) -> list[dict[str, object]]:
        seed = sum(ord(character) for character in symbol.upper())
        base_returns = [
            -0.006,
            0.004,
            0.007,
            -0.003,
            0.005,
            -0.002,
            0.009,
            -0.004,
            0.003,
            0.006,
            -0.005,
            0.002,
            0.004,
            -0.003,
            0.008,
            -0.006,
            0.005,
            0.001,
            -0.002,
            0.004,
            0.006,
            -0.004,
            0.003,
            0.005,
        ]
        scale = 0.75 + (seed % 9) / 20
        start = date(2026, 5, 1)
        return [
            {
                "date": (start + timedelta(days=index)).isoformat(),
                "return": value * scale,
            }
            for index, value in enumerate(base_returns)
        ]

    def _return_summary(
        self,
        returns: list[float],
        risk_free_rate: float,
        annualization_factor: int,
        benchmark_returns: list[float] | None = None,
    ) -> ReturnSummary:
        cumulative = calculate_cumulative_returns(returns)
        annual_return = annualized_return(returns, annualization_factor)
        benchmark_annual_return = (
            annualized_return(benchmark_returns, annualization_factor)
            if benchmark_returns
            else None
        )
        return ReturnSummary(
            observations=len(returns),
            arithmetic_mean_return=arithmetic_mean(returns),
            geometric_mean_return=geometric_mean(returns),
            holding_period_return=prod(1.0 + value for value in returns) - 1.0
            if returns
            else 0.0,
            cumulative_return=cumulative[-1] if cumulative else 0.0,
            annualized_return=annual_return,
            excess_return=excess_return(annual_return, risk_free_rate),
            active_return=active_return(annual_return, benchmark_annual_return)
            if benchmark_annual_return is not None
            else None,
        )

    def _volatility_summary(
        self,
        returns: list[float],
        rolling_points: list[dict[str, float | str]],
        annualization_factor: int,
    ) -> VolatilitySummary:
        summary = rolling_summary(rolling_points)
        daily_volatility = standard_deviation(returns)
        annual_volatility = annualized_volatility(returns, annualization_factor)
        return VolatilitySummary(
            variance=variance(returns),
            standard_deviation=daily_volatility,
            daily_volatility=daily_volatility,
            annualized_volatility=annual_volatility,
            realized_volatility=annual_volatility,
            coefficient_of_variation=coefficient_of_variation(returns),
            rolling_latest=summary["latest"],
            rolling_minimum=summary["minimum"],
            rolling_maximum=summary["maximum"],
            rolling_average=summary["average"],
        )

    def _downside_summary(
        self,
        returns: list[float],
        confidence_level: float,
        annualization_factor: int,
    ) -> DownsideRiskSummary:
        return DownsideRiskSummary(
            downside_deviation=downside_deviation(
                returns,
                0.0,
                annualization_factor,
            ),
            semi_variance=semi_variance(returns),
            semi_deviation=semi_deviation(returns),
            worst_return=min(returns) if returns else 0.0,
            best_return=max(returns) if returns else 0.0,
            max_drawdown=max_drawdown_from_returns(returns),
            probability_negative_return=probability_negative_return(returns),
            historical_var=historical_var(returns, confidence_level),
            historical_cvar=historical_cvar(returns, confidence_level),
        )

    def _distribution(self, returns: list[float]) -> DistributionSummary:
        summary = distribution_summary(returns)
        return DistributionSummary(
            **summary,
            normality_note=(
                "Skewness and kurtosis indicate whether returns deviate from "
                "a normal distribution; fat tails increase tail-risk concern."
            ),
        )

    def _risk_adjusted(
        self,
        returns: list[float],
        benchmark_returns: list[float],
        beta_value: float,
        risk_free_rate: float,
        annualization_factor: int,
    ) -> RiskAdjustedSummary:
        return RiskAdjustedSummary(
            sharpe_ratio=sharpe_ratio(returns, risk_free_rate, annualization_factor),
            treynor_ratio=treynor_ratio(
                returns,
                beta_value,
                risk_free_rate,
                annualization_factor,
            ),
            sortino_ratio=sortino_ratio(returns, risk_free_rate, annualization_factor),
            tracking_error=tracking_error(
                returns,
                benchmark_returns,
                annualization_factor,
            ),
            information_ratio=information_ratio(
                returns,
                benchmark_returns,
                annualization_factor,
            ),
        )

    def _data_source(
        self,
        *,
        metric_source: str,
        fallback_used: bool,
        fallback_reason: str | None,
        observations: int,
        symbols_found: list[str],
        symbols_missing: list[str],
        warnings: list[str],
    ) -> VolatilityDataSource:
        badges = []
        if metric_source == "realized_market_data":
            badges.append("Realized Market Data")
        elif metric_source == "partial_data":
            badges.append("Partial Data")
        else:
            badges.append("Demo assumptions")
        if fallback_used:
            badges.append("Requires Market Data")
        return VolatilityDataSource(
            metric_source=metric_source,
            fallback_used=fallback_used,
            fallback_reason=fallback_reason,
            observations=observations,
            symbols_found=symbols_found,
            symbols_missing=symbols_missing,
            warnings=warnings,
            badges=badges,
        )

    def _position_weights(
        self,
        positions: list[dict[str, object]],
    ) -> dict[str, float]:
        market_values = {
            str(position["symbol"]).upper(): float(position["quantity"])
            * float(position["current_price"])
            for position in positions
        }
        total_value = sum(market_values.values())
        if total_value == 0:
            return {}
        return {
            symbol: market_value / total_value
            for symbol, market_value in market_values.items()
        }

    def _normalize_weights(self, weights: dict[str, float]) -> dict[str, float]:
        total_weight = sum(weights.values())
        if total_weight == 0:
            return weights
        return {
            symbol: weight / total_weight
            for symbol, weight in weights.items()
        }

    def _align_to_dates(
        self,
        series: list[dict[str, object]],
        dates: list[str],
    ) -> list[float]:
        values_by_date = {
            str(point["date"]): float(point["return"])
            for point in series
        }
        return [values_by_date[date] for date in dates if date in values_by_date]

    def _beta_note(self, beta_value: float) -> str:
        if beta_value > 1:
            return "Beta above 1 indicates above-market systematic risk."
        if beta_value < 1:
            return "Beta below 1 indicates below-market systematic risk."
        return "Beta near 1 indicates market-like systematic risk."

    def _correlation_note(self, correlation_value: float) -> str:
        if correlation_value >= 0.75:
            return "High positive correlation limits diversification versus benchmark."
        if correlation_value <= 0.25:
            return "Low correlation can improve diversification."
        return "Moderate correlation gives partial diversification benefit."

    def _cfa_notes(self) -> list[str]:
        return [
            "Standard deviation measures total risk.",
            "Variance is the square of standard deviation.",
            "Covariance measures how two assets move together.",
            "Correlation standardizes covariance between -1 and +1.",
            "Lower correlation can improve diversification.",
            "Beta measures systematic risk relative to the market benchmark.",
            "CAPM connects beta to required return.",
            "Sharpe ratio uses total risk.",
            "Treynor ratio uses systematic risk.",
            "Jensen alpha compares realized return to CAPM required return.",
            "Tracking error measures active risk relative to benchmark.",
            "Information ratio measures active return per unit of active risk.",
            "Diversification reduces unsystematic risk, not market-wide systematic risk.",
        ]
