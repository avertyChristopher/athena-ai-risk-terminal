from fastapi import HTTPException

from app.modules.market_data.repository import MarketDataRepository
from app.modules.risk_analytics.service import RiskAnalyticsService
from app.modules.risk_monitor.domain.alerts import build_risk_alerts
from app.modules.risk_monitor.domain.commentary import build_athena_risk_commentary
from app.modules.risk_monitor.domain.risk_contribution import calculate_risk_contribution
from app.modules.risk_monitor.domain.risk_limits import (
    DEFAULT_RISK_LIMITS,
    evaluate_limit_breaches,
)
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
from app.modules.risk_monitor.domain.stress_testing import (
    DEFAULT_STRESS_SHOCKS,
    run_stress_scenarios,
)
from app.modules.risk_monitor.repository import RiskMonitorRepository
from app.modules.risk_monitor.schemas import (
    AthenaRiskCommentary,
    BenchmarkRiskResponse,
    ConcentrationAnalysis,
    ConcentrationExposure,
    RiskAlert,
    RiskContributionItem,
    RiskContributionResponse,
    RiskLimitBreach,
    RiskMetric,
    RiskMonitorAssumptions,
    RiskMonitorAnalysisResponse,
    RiskMonitorAnalyzeRequest,
    RiskMonitorStatus,
    RiskSourceMetadata,
    StressScenarioResult,
)
from app.modules.risk_shared.mappers import shared_payload_to_risk_source
from app.modules.risk_shared.schemas import (
    ModuleIntegrationStatus,
    OptionsRiskPayload,
    RatesRiskPayload,
    SharedRiskPayload,
)
from app.modules.risk_shared.status import integration_status


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
                "volatility_lab_payload_consumer",
                "rates_lab_payload_consumer",
                "options_pricing_payload_consumer",
            ],
        )

    def analyze(self, payload: RiskMonitorAnalyzeRequest) -> RiskMonitorAnalysisResponse:
        portfolio = self.repository.get_portfolio(payload.portfolio_id)
        if portfolio is None:
            raise HTTPException(status_code=404, detail="Portfolio not found.")

        positions = self.repository.list_positions(payload.portfolio_id)
        limit_overrides = (
            payload.limits.model_dump(exclude_none=True) if payload.limits else {}
        )
        stress_overrides = (
            payload.stress_shocks.model_dump(exclude_none=True)
            if payload.stress_shocks
            else {}
        )
        applied_limits = {**DEFAULT_RISK_LIMITS, **limit_overrides}
        applied_stress_shocks = {**DEFAULT_STRESS_SHOCKS, **stress_overrides}
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
        sector_exposures = calculate_exposure_by_key(decorated_positions, "sector")
        asset_type_exposures = calculate_exposure_by_key(
            decorated_positions,
            "asset_type",
        )
        breaches = evaluate_limit_breaches(
            decorated_positions=decorated_positions,
            sector_exposures=sector_exposures,
            asset_type_exposures=asset_type_exposures,
            cash_weight=cash_weight,
            top_3_weight=top_3_weight,
            volatility=volatility,
            var_95=var_95,
            cvar_95=cvar_95,
            max_drawdown=max_drawdown,
            tracking_error=tracking_error,
            active_exposure=active_exposure,
            limit_overrides=limit_overrides,
        )
        stress_tests = run_stress_scenarios(
            decorated_positions,
            total_value,
            shock_overrides=stress_overrides,
        )
        risk_contribution = calculate_risk_contribution(
            decorated_positions=decorated_positions,
            covariance_matrix=realized_risk.covariance_matrix,
            covariance_symbols=realized_risk.covariance_symbols,
        )
        benchmark_warnings = ["Benchmark constituent weights are not connected yet."]
        if realized_risk.tracking_error is None:
            benchmark_warnings.append("Requires benchmark return history for realized tracking error.")
        breach_severities = [str(breach["severity"]) for breach in breaches]
        global_risk_score = calculate_risk_score(
            volatility=volatility,
            var_95=var_95,
            cvar_95=cvar_95,
            max_drawdown=max_drawdown,
            top_3_weight=top_3_weight,
            cash_weight=cash_weight,
            active_exposure=active_exposure,
            breach_severities=breach_severities,
        )
        global_risk_status = classify_global_risk_status(global_risk_score)
        main_drivers = self._main_drivers(
            decorated_positions,
            top_3_weight,
            breaches,
            stress_tests,
        )
        alerts = build_risk_alerts(breaches, stress_tests)
        commentary = build_athena_risk_commentary(
            status=global_risk_status,
            main_drivers=main_drivers,
            breaches=breaches,
            stress_tests=stress_tests,
            benchmark_warnings=benchmark_warnings,
        )

        return RiskMonitorAnalysisResponse(
            portfolio_id=payload.portfolio_id,
            portfolio_name=str(portfolio["name"]),
            benchmark_symbol=payload.benchmark_symbol.upper(),
            total_value=total_value,
            global_risk_score=global_risk_score,
            global_risk_status=global_risk_status,
            main_drivers=main_drivers,
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
            limit_breaches=[RiskLimitBreach.model_validate(breach) for breach in breaches],
            stress_tests=[
                StressScenarioResult.model_validate(scenario)
                for scenario in stress_tests
            ],
            risk_contribution=RiskContributionResponse.model_validate(risk_contribution),
            benchmark_risk=BenchmarkRiskResponse(
                benchmark_symbol=payload.benchmark_symbol.upper(),
                beta=beta,
                active_exposure=active_exposure,
                tracking_error=tracking_error,
                information_ratio=information_ratio,
                active_risk_status=self._benchmark_status(active_exposure, tracking_error),
                warnings=benchmark_warnings,
                badges=self._benchmark_badges(realized_risk.tracking_error),
            ),
            alerts=[RiskAlert.model_validate(alert) for alert in alerts],
            athena_commentary=AthenaRiskCommentary.model_validate(commentary),
            risk_source=self._risk_source_metadata(realized_risk),
            assumptions=RiskMonitorAssumptions(
                limits=applied_limits,
                stress_shocks=applied_stress_shocks,
            ),
            integration_statuses=self._integration_statuses(
                market_warnings=realized_risk.quality_warnings,
                market_payload_available=not realized_risk.fallback_used,
            ),
        )

    def analyze_from_volatility(
        self,
        payload: SharedRiskPayload,
    ) -> RiskMonitorAnalysisResponse:
        portfolio = (
            self.repository.get_portfolio(payload.portfolio_id)
            if payload.portfolio_id
            else None
        )
        positions = (
            self.repository.list_positions(payload.portfolio_id)
            if payload.portfolio_id and portfolio is not None
            else []
        )
        cash = float(portfolio["cash"]) if portfolio is not None else 0.0
        decorated_positions = decorate_positions(positions, cash)
        total_value = calculate_total_value(decorated_positions, cash)
        cash_weight = cash / total_value if total_value else 0.0
        top_3_weight = calculate_top_n_weight(decorated_positions, 3)
        sector_exposures = calculate_exposure_by_key(decorated_positions, "sector")
        asset_type_exposures = calculate_exposure_by_key(
            decorated_positions,
            "asset_type",
        )
        active_exposure = 0.0
        expected_return = 0.0
        volatility = payload.annualized_volatility
        var_95 = payload.historical_var
        cvar_95 = payload.historical_cvar
        max_drawdown = payload.max_drawdown
        tracking_error = payload.tracking_error
        sharpe_ratio = payload.sharpe_ratio
        sortino_ratio = payload.sortino_ratio
        beta = payload.beta
        information_ratio = calculate_information_ratio(
            expected_return,
            tracking_error,
        )
        breaches = evaluate_limit_breaches(
            decorated_positions=decorated_positions,
            sector_exposures=sector_exposures,
            asset_type_exposures=asset_type_exposures,
            cash_weight=cash_weight,
            top_3_weight=top_3_weight,
            volatility=volatility,
            var_95=var_95,
            cvar_95=cvar_95,
            max_drawdown=max_drawdown,
            tracking_error=tracking_error,
            active_exposure=active_exposure,
            limit_overrides=None,
        )
        stress_tests = (
            run_stress_scenarios(decorated_positions, total_value)
            if decorated_positions
            else []
        )
        breach_severities = [str(breach["severity"]) for breach in breaches]
        global_risk_score = calculate_risk_score(
            volatility=volatility,
            var_95=var_95,
            cvar_95=cvar_95,
            max_drawdown=max_drawdown,
            top_3_weight=top_3_weight,
            cash_weight=cash_weight,
            active_exposure=active_exposure,
            breach_severities=breach_severities,
        )
        global_risk_status = classify_global_risk_status(global_risk_score)
        benchmark_warnings = [
            "Using Volatility Lab risk payload.",
            f"Payload generated at {payload.generated_at.isoformat()}.",
        ]
        if payload.fallback_used:
            benchmark_warnings.append(
                "Volatility Lab payload includes fallback or partial data assumptions.",
            )
        main_drivers = self._main_drivers(
            decorated_positions,
            top_3_weight,
            breaches,
            stress_tests,
        )
        if payload.warnings:
            main_drivers = [*payload.warnings[:2], *main_drivers][:5]
        alerts = build_risk_alerts(breaches, stress_tests)
        commentary = build_athena_risk_commentary(
            status=global_risk_status,
            main_drivers=main_drivers,
            breaches=breaches,
            stress_tests=stress_tests,
            benchmark_warnings=benchmark_warnings,
        )

        return RiskMonitorAnalysisResponse(
            portfolio_id=payload.portfolio_id or payload.symbol or "volatility-payload",
            portfolio_name=(
                str(portfolio["name"])
                if portfolio is not None
                else payload.symbol or "Volatility Lab Payload"
            ),
            benchmark_symbol=payload.benchmark_symbol.upper(),
            total_value=total_value,
            global_risk_score=global_risk_score,
            global_risk_status=global_risk_status,
            main_drivers=main_drivers,
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
                source=payload.metric_source,
            ),
            concentration=self._concentration_analysis(
                decorated_positions,
                cash_weight,
                top_3_weight,
            ),
            limit_breaches=[RiskLimitBreach.model_validate(breach) for breach in breaches],
            stress_tests=[
                StressScenarioResult.model_validate(scenario)
                for scenario in stress_tests
            ],
            risk_contribution=self._payload_risk_contribution(payload),
            benchmark_risk=BenchmarkRiskResponse(
                benchmark_symbol=payload.benchmark_symbol.upper(),
                beta=beta,
                active_exposure=active_exposure,
                tracking_error=tracking_error,
                information_ratio=information_ratio,
                active_risk_status=self._benchmark_status(
                    active_exposure,
                    tracking_error,
                ),
                warnings=benchmark_warnings,
                badges=["Volatility Lab Payload", payload.metric_source],
            ),
            alerts=[RiskAlert.model_validate(alert) for alert in alerts],
            athena_commentary=AthenaRiskCommentary.model_validate(commentary),
            risk_source=shared_payload_to_risk_source(payload),
            assumptions=RiskMonitorAssumptions(
                limits=DEFAULT_RISK_LIMITS,
                stress_shocks=DEFAULT_STRESS_SHOCKS,
            ),
            integration_statuses=self._integration_statuses(
                volatility_payload=payload,
                market_warnings=payload.warnings,
                market_payload_available=not payload.fallback_used,
            ),
        )

    def analyze_from_rates(
        self,
        payload: RatesRiskPayload,
    ) -> RiskMonitorAnalysisResponse:
        if payload.portfolio_id:
            analysis = self.analyze(
                RiskMonitorAnalyzeRequest(portfolio_id=payload.portfolio_id),
            )
            analysis.rates_risk_payload = payload
            analysis.integration_statuses = self._integration_statuses(
                rates_payload=payload,
            )
            analysis.main_drivers = [self._rates_driver(payload), *analysis.main_drivers][:5]
            analysis.risk_metrics = [
                *analysis.risk_metrics,
                *self._rates_payload_metrics(payload),
            ]
            return analysis

        return self._standalone_rates_analysis(payload)

    def analyze_from_options(
        self,
        payload: OptionsRiskPayload,
    ) -> RiskMonitorAnalysisResponse:
        return self._standalone_options_analysis(payload)

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

    def _rates_payload_metrics(self, payload: RatesRiskPayload) -> list[RiskMetric]:
        return [
            self._metric("Modified duration", payload.modified_duration, "rates_lab_payload", "Fixed-income price sensitivity to a 100% yield move."),
            self._metric("Convexity", payload.convexity, "rates_lab_payload", "Second-order bond price sensitivity to yield changes."),
            self._metric("DV01", payload.dv01, "rates_lab_payload", "Estimated dollar value of a one-basis-point rate move."),
            self._metric("+/- rate scenario loss", payload.estimated_rate_shock_loss, "rates_lab_payload", "Estimated portfolio or instrument impact from the supplied rate shock."),
        ]

    def _options_payload_metrics(self, payload: OptionsRiskPayload) -> list[RiskMetric]:
        return [
            self._metric("Delta-adjusted exposure", payload.delta_adjusted_exposure, "options_pricing_payload", "Option exposure adjusted by position Delta."),
            self._metric("Gamma", payload.gamma, "options_pricing_payload", "Change in Delta for a $1 move in the underlying."),
            self._metric("Theta", payload.theta, "options_pricing_payload", "Estimated daily time decay."),
            self._metric("Vega", payload.vega, "options_pricing_payload", "Option value sensitivity to a 1 percentage point volatility move."),
            self._metric("Rho", payload.rho, "options_pricing_payload", "Option value sensitivity to a 1 percentage point rate move."),
            self._metric("Max loss", payload.max_loss, "options_pricing_payload", "Analytical maximum loss when available."),
        ]

    def _standalone_rates_analysis(
        self,
        payload: RatesRiskPayload,
    ) -> RiskMonitorAnalysisResponse:
        total_value = max(
            abs(payload.fixed_income_market_value or 0.0),
            abs(payload.dirty_price or payload.clean_price or 0.0),
            abs(payload.estimated_rate_shock_loss or 0.0),
            1.0,
        )
        stress_tests = []
        if payload.estimated_rate_shock_loss is not None:
            stress_tests.append(
                StressScenarioResult(
                    name=f"{payload.rate_shock_bps or 0:g} bps rate shock",
                    estimated_impact_percent=payload.estimated_rate_shock_loss / total_value,
                    estimated_loss=payload.estimated_rate_shock_loss,
                    most_affected_holdings=[payload.symbol or "fixed_income_payload"],
                    severity="medium" if payload.estimated_rate_shock_loss < 0 else "low",
                    explanation="Rates Lab fixed-income payload consumed by Risk Monitor.",
                ),
            )
        drivers = [self._rates_driver(payload)]
        if payload.warnings:
            drivers = [*payload.warnings[:2], *drivers][:5]

        return RiskMonitorAnalysisResponse(
            portfolio_id=payload.portfolio_id or payload.symbol or "rates-payload",
            portfolio_name=payload.symbol or "Rates Lab Payload",
            benchmark_symbol="SPY",
            total_value=total_value,
            global_risk_score=55 if payload.warnings else 45,
            global_risk_status=classify_global_risk_status(55 if payload.warnings else 45),
            main_drivers=drivers,
            risk_metrics=self._rates_payload_metrics(payload),
            concentration=self._empty_concentration("Standalone Rates Lab payload; no Portfolio Builder positions supplied."),
            limit_breaches=[],
            stress_tests=stress_tests,
            risk_contribution=self._payload_contribution(
                name=payload.symbol or "fixed_income_payload",
                source="rates_lab_payload",
            ),
            benchmark_risk=self._empty_benchmark("Rates payload does not include benchmark-relative equity risk."),
            alerts=[],
            athena_commentary=AthenaRiskCommentary(
                summary="Risk Monitor consumed a Rates Lab fixed-income risk payload.",
                main_drivers=drivers,
                suggested_actions=["Review DV01, duration and supplied rate-shock loss before changing fixed-income exposure."],
            ),
            risk_source=self._standalone_risk_source(
                metric_source="rates_lab_payload",
                warnings=payload.warnings,
                badges=["Rates Lab Payload", "Fixed Income Risk Available"],
            ),
            assumptions=RiskMonitorAssumptions(
                limits=DEFAULT_RISK_LIMITS,
                stress_shocks=DEFAULT_STRESS_SHOCKS,
            ),
            integration_statuses=self._integration_statuses(rates_payload=payload),
            rates_risk_payload=payload,
        )

    def _standalone_options_analysis(
        self,
        payload: OptionsRiskPayload,
    ) -> RiskMonitorAnalysisResponse:
        total_value = max(
            abs(payload.delta_adjusted_exposure or 0.0),
            abs(payload.option_price or 0.0),
            abs(payload.max_loss or 0.0),
            1.0,
        )
        drivers = [
            f"{payload.underlying_symbol} option exposure has Delta-adjusted notional of {(payload.delta_adjusted_exposure or 0.0):,.2f}.",
        ]
        if payload.vega is not None:
            drivers.append(f"Vega exposure is {payload.vega:,.2f}.")
        if payload.warnings:
            drivers = [*payload.warnings[:2], *drivers][:5]

        return RiskMonitorAnalysisResponse(
            portfolio_id=payload.underlying_symbol,
            portfolio_name=payload.strategy_name or f"{payload.underlying_symbol} Option Payload",
            benchmark_symbol="SPY",
            total_value=total_value,
            global_risk_score=65 if payload.max_loss is None else 50,
            global_risk_status=classify_global_risk_status(65 if payload.max_loss is None else 50),
            main_drivers=drivers,
            risk_metrics=self._options_payload_metrics(payload),
            concentration=self._empty_concentration("Standalone Options Pricing payload; no Portfolio Builder positions supplied."),
            limit_breaches=[],
            stress_tests=[],
            risk_contribution=self._payload_contribution(
                name=payload.underlying_symbol,
                source="options_pricing_payload",
            ),
            benchmark_risk=self._empty_benchmark("Options payload does not include benchmark-relative equity risk."),
            alerts=[],
            athena_commentary=AthenaRiskCommentary(
                summary="Risk Monitor consumed an Options Pricing Lab derivatives risk payload.",
                main_drivers=drivers,
                suggested_actions=["Review Delta, Vega, Theta and max-loss exposure before adding the strategy to a portfolio."],
            ),
            risk_source=self._standalone_risk_source(
                metric_source="options_pricing_payload",
                warnings=payload.warnings,
                badges=["Options Pricing Payload", "Greeks Ready"],
            ),
            assumptions=RiskMonitorAssumptions(
                limits=DEFAULT_RISK_LIMITS,
                stress_shocks=DEFAULT_STRESS_SHOCKS,
            ),
            integration_statuses=self._integration_statuses(options_payload=payload),
            options_risk_payload=payload,
        )

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

    def _payload_risk_contribution(
        self,
        payload: SharedRiskPayload,
    ) -> RiskContributionResponse:
        by_asset = [
            RiskContributionItem(
                name=item.symbol,
                weight=item.weight,
                contribution=item.contribution,
                contribution_percent=item.contribution,
                source="volatility_lab_payload",
            )
            for item in payload.risk_contribution
        ]
        largest = max(
            by_asset,
            key=lambda item: item.contribution,
            default=None,
        )
        return RiskContributionResponse(
            contribution_source="volatility_lab_payload",
            method="Reused from Volatility Lab risk_monitor_payload.",
            by_asset=by_asset,
            by_sector=[],
            largest_risk_contributor=largest.name if largest else None,
            diversification_warning=None,
        )

    def _payload_contribution(
        self,
        *,
        name: str,
        source: str,
    ) -> RiskContributionResponse:
        return RiskContributionResponse(
            contribution_source=source,
            method="Standalone module payload contribution placeholder.",
            by_asset=[
                RiskContributionItem(
                    name=name,
                    weight=1.0,
                    contribution=1.0,
                    contribution_percent=1.0,
                    source=source,
                ),
            ],
            by_sector=[],
            largest_risk_contributor=name,
            diversification_warning="Requires Portfolio Builder positions for diversified contribution.",
        )

    def _empty_concentration(self, warning: str) -> ConcentrationAnalysis:
        return ConcentrationAnalysis(
            largest_position=None,
            top_3_weight=0.0,
            top_5_weight=0.0,
            sector_exposures=[],
            asset_type_exposures=[],
            cash_weight=0.0,
            concentration_score=0.0,
            warnings=[warning],
        )

    def _empty_benchmark(self, warning: str) -> BenchmarkRiskResponse:
        return BenchmarkRiskResponse(
            benchmark_symbol="SPY",
            beta=None,
            active_exposure=0.0,
            tracking_error=None,
            information_ratio=None,
            active_risk_status="Requires portfolio context",
            warnings=[warning],
            badges=["Requires Portfolio Builder"],
        )

    def _standalone_risk_source(
        self,
        *,
        metric_source: str,
        warnings: list[str],
        badges: list[str],
    ) -> RiskSourceMetadata:
        return RiskSourceMetadata(
            metric_source=metric_source,
            fallback_used=False,
            fallback_reason=None,
            observations=0,
            symbols_found=[],
            symbols_missing=[],
            quality_warnings=warnings,
            badges=badges,
        )

    def _rates_driver(self, payload: RatesRiskPayload) -> str:
        if payload.estimated_rate_shock_loss is not None:
            return (
                f"Rate shock of {payload.rate_shock_bps or 0:g} bps implies "
                f"{payload.estimated_rate_shock_loss:,.2f} estimated loss."
            )
        if payload.dv01 is not None:
            return f"DV01 is {payload.dv01:,.2f}; fixed-income rate sensitivity is available."
        return "Rates Lab payload available, but duration/DV01 metadata is partial."

    def _integration_statuses(
        self,
        *,
        volatility_payload: SharedRiskPayload | None = None,
        rates_payload: RatesRiskPayload | None = None,
        options_payload: OptionsRiskPayload | None = None,
        market_warnings: list[str] | None = None,
        market_payload_available: bool = True,
    ) -> list[ModuleIntegrationStatus]:
        return [
            integration_status(
                module="Portfolio Builder",
                status="Connected",
                data_source="portfolio_builder",
                payload_available=True,
            ),
            integration_status(
                module="Market Data",
                status="Connected" if market_payload_available else "Connected with fallback",
                data_source="market_data",
                payload_available=market_payload_available,
                warnings=market_warnings,
                required_data=[] if market_payload_available else ["Price and return history"],
            ),
            integration_status(
                module="Volatility Lab",
                status="Payload Available" if volatility_payload else "Connected",
                data_source="volatility_lab",
                payload_available=volatility_payload is not None,
                generated_at=volatility_payload.generated_at if volatility_payload else None,
                warnings=volatility_payload.warnings if volatility_payload else [],
                required_data=[] if volatility_payload else ["RiskAnalyticsPayload"],
            ),
            integration_status(
                module="Rates Lab",
                status="Fixed Income Risk Available" if rates_payload else "Connected",
                data_source="rates_lab",
                payload_available=rates_payload is not None,
                generated_at=rates_payload.generated_at if rates_payload else None,
                warnings=rates_payload.warnings if rates_payload else [],
                required_data=[] if rates_payload else ["RatesRiskPayload"],
            ),
            integration_status(
                module="Options Pricing Lab",
                status="Greeks Ready" if options_payload else "Connected",
                data_source="options_pricing_lab",
                payload_available=options_payload is not None,
                generated_at=options_payload.generated_at if options_payload else None,
                warnings=options_payload.warnings if options_payload else [],
                required_data=[] if options_payload else ["OptionsRiskPayload"],
            ),
            integration_status(
                module="Trade Simulator",
                status="Pre-Trade Warnings Ready",
                data_source="trade_simulator",
                payload_available=False,
                required_data=["TradeImpactPayload"],
            ),
        ]

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

    def _main_drivers(
        self,
        decorated_positions: list[dict[str, object]],
        top_3_weight: float,
        breaches: list[dict[str, object]],
        stress_tests: list[dict[str, object]],
    ) -> list[str]:
        drivers = [
            str(breach["explanation"])
            for breach in breaches
            if str(breach["severity"]) in {"high", "critical"}
        ][:4]
        if not drivers:
            drivers = self._basic_drivers(decorated_positions, top_3_weight)

        worst_stress = min(
            stress_tests,
            key=lambda scenario: float(scenario["estimated_impact_percent"]),
            default=None,
        )
        if worst_stress is not None:
            drivers.append(
                f"{worst_stress['name']} impact estimated at "
                f"{float(worst_stress['estimated_impact_percent']):.1%}.",
            )
        return drivers[:5]

    def _benchmark_status(
        self,
        active_exposure: float,
        tracking_error: float | None,
    ) -> str:
        if active_exposure >= 0.80 or (tracking_error is not None and tracking_error >= 0.08):
            return "High active risk"
        if active_exposure >= 0.50 or (tracking_error is not None and tracking_error >= 0.05):
            return "Elevated active risk"
        return "Within active-risk watch"

    def _benchmark_badges(self, realized_tracking_error: float | None) -> list[str]:
        badges = ["Requires Benchmark Constituent Feed"]
        if realized_tracking_error is None:
            badges.append("Requires Benchmark History")
        else:
            badges.append("Realized")
        return badges

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
