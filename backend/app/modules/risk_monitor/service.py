from fastapi import HTTPException

from app.modules.market_data.repository import MarketDataRepository
from app.modules.risk_analytics.service import RiskAnalyticsService
from app.modules.risk_monitor.domain.risk_metrics import (
    calculate_active_exposure,
    calculate_demo_beta,
    calculate_demo_cvar,
    calculate_demo_expected_return,
    calculate_demo_max_drawdown,
    calculate_demo_var,
    calculate_demo_volatility,
    calculate_exposure_by_key,
    calculate_information_ratio,
    calculate_risk_score,
    calculate_sharpe_ratio,
    calculate_sortino_ratio,
    calculate_top_n_weight,
    calculate_total_value,
    calculate_tracking_error_fallback,
    calculate_weight_by_symbol,
    classify_global_risk_status,
    decorate_positions,
)
from app.modules.risk_monitor.repository import RiskMonitorRepository
from app.modules.risk_monitor.schemas import (
    AthenaRiskCommentary,
    BenchmarkRiskResponse,
    ConcentrationAnalysis,
    ConcentrationExposure,
    RiskContributionResponse,
    RiskMetric,
    RiskMonitorAnalysisResponse,
    RiskMonitorAnalyzeRequest,
    RiskMonitorStatus,
    RiskSourceMetadata,
)


class RiskMonitorService:
    def __init__(self, repository: RiskMonitorRepository) -> None:
        self.repository = repository
        self.risk_analytics_service = RiskAnalyticsService(
            MarketDataRepository(repository.db),
        )

    def get_module_status(self) -> RiskMonitorStatus:
        return RiskMonitorStatus(
            detail=(
                "Risk Monitor is ready for portfolio surveillance, realized "
                "Market Data metrics and deterministic fallback analytics."
            ),
            engines_available=[
                "realized_market_data",
                "deterministic_demo_fallback",
                "risk_metrics",
                "concentration_analysis",
            ],
        )

    def analyze(self, payload: RiskMonitorAnalyzeRequest) -> RiskMonitorAnalysisResponse:
        portfolio = self.repository.get_portfolio(payload.portfolio_id)
        if portfolio is None:
            raise HTTPException(status_code=404, detail="Portfolio not found.")

        positions = self.repository.list_positions(payload.portfolio_id)
        cash = float(portfolio["cash"])
        decorated_positions = decorate_positions(positions, cash)
        total_value = calculate_total_value(decorated_positions, cash)
        cash_weight = cash / total_value if total_value else 0.0
        weights_by_symbol = calculate_weight_by_symbol(
            decorated_positions,
            "invested_weight",
        )
        realized_risk = self.risk_analytics_service.calculate_realized_portfolio_risk(
            weights_by_symbol,
            benchmark_symbol=payload.benchmark_symbol,
            annual_risk_free_rate=payload.risk_free_rate,
        )

        expected_return = (
            realized_risk.realized_annualized_return
            if not realized_risk.fallback_used
            and realized_risk.realized_annualized_return is not None
            else calculate_demo_expected_return(decorated_positions, cash_weight)
        )
        volatility = (
            realized_risk.realized_volatility
            if not realized_risk.fallback_used
            and realized_risk.realized_volatility is not None
            else calculate_demo_volatility(decorated_positions, cash_weight)
        )
        var_95 = (
            realized_risk.portfolio_var_95
            if not realized_risk.fallback_used
            and realized_risk.portfolio_var_95 is not None
            else calculate_demo_var(volatility)
        )
        cvar_95 = (
            realized_risk.portfolio_cvar_95
            if not realized_risk.fallback_used
            and realized_risk.portfolio_cvar_95 is not None
            else calculate_demo_cvar(volatility)
        )
        max_drawdown = (
            realized_risk.max_drawdown
            if not realized_risk.fallback_used
            and realized_risk.max_drawdown is not None
            else calculate_demo_max_drawdown(volatility)
        )
        sharpe_ratio = (
            realized_risk.realized_sharpe_ratio
            if not realized_risk.fallback_used
            and realized_risk.realized_sharpe_ratio is not None
            else calculate_sharpe_ratio(expected_return, payload.risk_free_rate, volatility)
        )
        sortino_ratio = calculate_sortino_ratio(
            realized_risk.portfolio_returns,
            expected_return,
            payload.risk_free_rate,
            volatility,
        )
        tracking_error = (
            realized_risk.tracking_error
            if not realized_risk.fallback_used
            and realized_risk.tracking_error is not None
            else calculate_tracking_error_fallback(
                expected_return,
                calculate_top_n_weight(decorated_positions, 1),
            )
        )
        information_ratio = calculate_information_ratio(expected_return, tracking_error)
        beta = calculate_demo_beta(decorated_positions)
        active_exposure = calculate_active_exposure(
            decorated_positions,
            payload.benchmark_symbol,
        )
        top_3_weight = calculate_top_n_weight(decorated_positions, 3)
        global_risk_score = calculate_risk_score(
            volatility=volatility,
            var_95=var_95,
            cvar_95=cvar_95,
            max_drawdown=max_drawdown,
            top_3_weight=top_3_weight,
            cash_weight=cash_weight,
            active_exposure=active_exposure,
            breach_severities=[],
        )

        return RiskMonitorAnalysisResponse(
            portfolio_id=payload.portfolio_id,
            portfolio_name=str(portfolio["name"]),
            benchmark_symbol=payload.benchmark_symbol.upper(),
            total_value=total_value,
            global_risk_score=global_risk_score,
            global_risk_status=classify_global_risk_status(global_risk_score),
            main_drivers=self._basic_drivers(decorated_positions, top_3_weight),
            risk_metrics=self._risk_metrics(
                expected_return=expected_return,
                volatility=volatility,
                var_95=var_95,
                cvar_95=cvar_95,
                max_drawdown=max_drawdown,
                sharpe_ratio=sharpe_ratio,
                sortino_ratio=sortino_ratio,
                beta=beta,
                tracking_error=tracking_error,
                information_ratio=information_ratio,
                source=realized_risk.metric_source,
            ),
            concentration=self._concentration_analysis(
                decorated_positions,
                cash_weight,
                top_3_weight,
            ),
            limit_breaches=[],
            stress_tests=[],
            risk_contribution=RiskContributionResponse(
                contribution_source="placeholder",
                method="Risk contribution engine will be added in the next increment.",
                by_asset=[],
                by_sector=[],
                largest_risk_contributor=None,
                diversification_warning=None,
            ),
            benchmark_risk=BenchmarkRiskResponse(
                benchmark_symbol=payload.benchmark_symbol.upper(),
                beta=beta,
                active_exposure=active_exposure,
                tracking_error=tracking_error,
                information_ratio=information_ratio,
                active_risk_status="Monitoring",
                warnings=["Benchmark constituent weights are not connected yet."],
                badges=["Requires Benchmark Constituent Feed"],
            ),
            alerts=[],
            athena_commentary=AthenaRiskCommentary(
                summary=(
                    "Risk Monitor has calculated portfolio surveillance metrics. "
                    "Limit, stress and commentary engines are enabled in the next increment."
                ),
                main_drivers=self._basic_drivers(decorated_positions, top_3_weight),
                suggested_actions=["Review concentration and benchmark exposure."],
            ),
            risk_source=self._risk_source_metadata(realized_risk),
        )

    def _risk_metrics(
        self,
        *,
        expected_return: float,
        volatility: float,
        var_95: float,
        cvar_95: float,
        max_drawdown: float,
        sharpe_ratio: float | None,
        sortino_ratio: float | None,
        beta: float,
        tracking_error: float | None,
        information_ratio: float | None,
        source: str,
    ) -> list[RiskMetric]:
        return [
            self._metric("Expected return", expected_return, source, "Forward/realized portfolio return estimate."),
            self._metric("Portfolio volatility", volatility, source, "Annualized portfolio volatility."),
            self._metric("VaR 95%", var_95, source, "Historical or demo one-period value at risk."),
            self._metric("CVaR 95%", cvar_95, source, "Historical or demo conditional value at risk."),
            self._metric("Max drawdown", max_drawdown, source, "Worst observed or demo peak-to-trough drawdown."),
            self._metric("Sharpe ratio", sharpe_ratio, source, "Risk-adjusted excess return."),
            self._metric("Sortino ratio", sortino_ratio, source, "Downside-risk-adjusted excess return."),
            self._metric("Beta", beta, "deterministic_demo", "Demo portfolio beta versus benchmark."),
            self._metric("Tracking error", tracking_error, source, "Active return volatility versus benchmark."),
            self._metric("Information ratio", information_ratio, source, "Active return per unit of tracking error."),
        ]

    def _metric(
        self,
        name: str,
        value: float | None,
        source: str,
        description: str,
    ) -> RiskMetric:
        return RiskMetric(
            name=name,
            value=value,
            source=source,
            status="ok" if value is not None else "unavailable",
            description=description,
        )

    def _concentration_analysis(
        self,
        decorated_positions: list[dict[str, object]],
        cash_weight: float,
        top_3_weight: float,
    ) -> ConcentrationAnalysis:
        top_5_weight = calculate_top_n_weight(decorated_positions, 5)
        largest_position = max(
            decorated_positions,
            key=lambda position: float(position["invested_weight"]),
            default=None,
        )
        sector_exposures = calculate_exposure_by_key(decorated_positions, "sector")
        asset_type_exposures = calculate_exposure_by_key(decorated_positions, "asset_type")
        warnings = []
        if largest_position and float(largest_position["invested_weight"]) > 0.25:
            warnings.append(
                f"{largest_position['symbol']} is above the 25% single-position surveillance threshold.",
            )
        if top_3_weight > 0.65:
            warnings.append("Top 3 holdings concentration is above the 65% surveillance threshold.")

        return ConcentrationAnalysis(
            largest_position=(
                ConcentrationExposure(
                    name=str(largest_position["symbol"]),
                    weight=float(largest_position["invested_weight"]),
                    limit=0.25,
                    status=(
                        "breach"
                        if float(largest_position["invested_weight"]) > 0.25
                        else "ok"
                    ),
                )
                if largest_position
                else None
            ),
            top_3_weight=top_3_weight,
            top_5_weight=top_5_weight,
            sector_exposures=[
                ConcentrationExposure(
                    name=name,
                    weight=weight,
                    limit=0.50,
                    status="breach" if weight > 0.50 else "ok",
                )
                for name, weight in sorted(
                    sector_exposures.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
            ],
            asset_type_exposures=[
                ConcentrationExposure(
                    name=name,
                    weight=weight,
                    limit=0.80,
                    status="breach" if weight > 0.80 else "ok",
                )
                for name, weight in sorted(
                    asset_type_exposures.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
            ],
            cash_weight=cash_weight,
            concentration_score=min(1.0, top_3_weight),
            warnings=warnings,
        )

    def _basic_drivers(
        self,
        decorated_positions: list[dict[str, object]],
        top_3_weight: float,
    ) -> list[str]:
        drivers = []
        largest_position = max(
            decorated_positions,
            key=lambda position: float(position["invested_weight"]),
            default=None,
        )
        if largest_position is not None:
            drivers.append(
                f"{largest_position['symbol']} weight at {float(largest_position['invested_weight']):.1%}.",
            )
        drivers.append(f"Top 3 holdings weight at {top_3_weight:.1%}.")
        return drivers

    def _risk_source_metadata(self, realized_risk) -> RiskSourceMetadata:
        badges = [
            "Realized"
            if realized_risk.metric_source == "realized_market_data"
            else "Demo",
        ]
        if realized_risk.fallback_used:
            badges.append("Requires Market Data")
        if realized_risk.symbols_missing:
            badges.append("Partial Data")

        return RiskSourceMetadata(
            metric_source=realized_risk.metric_source,
            fallback_used=realized_risk.fallback_used,
            fallback_reason=realized_risk.fallback_reason,
            observations=realized_risk.observations,
            symbols_found=realized_risk.symbols_found,
            symbols_missing=realized_risk.symbols_missing,
            quality_warnings=realized_risk.quality_warnings,
            badges=badges,
        )
