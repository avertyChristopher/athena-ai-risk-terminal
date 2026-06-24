from __future__ import annotations

from datetime import UTC, datetime

from app.modules.stress_testing.domain.commentary import generate_stress_commentary
from app.modules.stress_testing.domain.contributors import (
    aggregate_impacts,
    rank_worst_contributors,
)
from app.modules.stress_testing.domain.portfolio_impact import (
    calculate_portfolio_stress_value,
)
from app.modules.stress_testing.domain.risk_impact import (
    build_risk_metric_snapshot,
    detect_stress_limit_breaches,
    estimate_stress_severity,
)
from app.modules.stress_testing.domain.scenarios import (
    build_custom_scenario,
    get_predefined_scenario,
    list_predefined_scenarios,
)
from app.modules.stress_testing.repository import StressTestingRepository
from app.modules.stress_testing.schemas import (
    AthenaStressCommentary,
    FixedIncomeStressSummary,
    IntegrationStatus,
    OptionsRiskIntegration,
    RiskMetricComparison,
    RiskMonitorStressPayload,
    ScenarioLibraryResponse,
    SelectedPortfolio,
    ShockAssumptions,
    StressMethodology,
    StressScenarioDefinition,
    StressSeverityAssessment,
    StressTestingResponse,
    StressTestingRunRequest,
    StressTestingStatus,
)


class StressTestingService:
    def __init__(self, repository: StressTestingRepository) -> None:
        self.repository = repository

    def get_status(self) -> StressTestingStatus:
        return StressTestingStatus(
            detail="Portfolio stress testing is connected to Portfolio Builder with Market Data, Rates, Volatility, Options and Risk Monitor integration contracts.",
            engines_available=[
                "scenario_library",
                "portfolio_impact",
                "rates_duration",
                "volatility_risk_metrics",
                "options_greeks_placeholder",
                "risk_monitor_payload",
            ],
        )

    def list_scenarios(self) -> ScenarioLibraryResponse:
        return ScenarioLibraryResponse(
            scenarios=[self._scenario_definition(scenario) for scenario in list_predefined_scenarios()]
        )

    def run(self, payload: StressTestingRunRequest) -> StressTestingResponse:
        portfolio = self.repository.get_portfolio(payload.portfolio_id)
        if portfolio is None:
            raise ValueError(f"Portfolio '{payload.portfolio_id}' was not found.")

        scenario = self._resolve_scenario(payload)
        positions = self.repository.list_positions(payload.portfolio_id)
        if not positions:
            raise ValueError("Stress testing requires at least one portfolio position.")

        base_currency = str(portfolio.get("base_currency", "USD"))
        impact = calculate_portfolio_stress_value(
            positions,
            float(portfolio.get("cash", 0.0)),
            scenario,
            base_currency,
        )
        position_impacts = impact["position_impacts"] if payload.include_position_impacts else []
        asset_class_impacts = aggregate_impacts(position_impacts, "asset_class")
        sector_impacts = aggregate_impacts(position_impacts, "sector")
        currency_impacts = aggregate_impacts(position_impacts, "currency")
        worst_contributors = rank_worst_contributors(position_impacts)

        base_volatility, symbols_found, symbols_missing = self.repository.estimate_portfolio_volatility(
            positions,
            float(impact["base_portfolio_value"]),
        )
        risk_snapshot = build_risk_metric_snapshot(
            float(impact["base_portfolio_value"]),
            base_volatility,
            float(scenario.get("volatility_shock", 0.0)),
            max(float(impact["percent_loss"]), 0.0),
            payload.confidence_level,
        )
        fixed_income_summary = self._fixed_income_summary(
            position_impacts,
            float(impact["base_portfolio_value"]),
            scenario,
        )
        limit_breaches = detect_stress_limit_breaches(
            max(float(impact["percent_loss"]), 0.0),
            sector_impacts,
            asset_class_impacts,
            abs(fixed_income_summary.rate_risk_impact) / fixed_income_summary.fixed_income_exposure
            if fixed_income_summary.fixed_income_exposure > 0
            else 0.0,
            float(scenario.get("liquidity_multiplier", 1.0)),
        )
        severity = estimate_stress_severity(
            max(float(impact["percent_loss"]), 0.0),
            max(float(impact["dollar_loss"]), 0.0),
            len(limit_breaches),
            risk_snapshot["var_deterioration"],
            worst_contributors[0]["contribution_to_loss"] if worst_contributors else 0.0,
            float(scenario.get("liquidity_multiplier", 1.0)) > 1.0,
        )
        warnings = self._warnings(position_impacts, symbols_missing)
        options_risk = self._options_integration(position_impacts)
        commentary = generate_stress_commentary(
            str(scenario["name"]),
            str(severity["severity"]),
            max(float(impact["percent_loss"]), 0.0),
            worst_contributors[0]["name"] if worst_contributors else None,
            any(
                str(row.get("name", "")).lower() == "fixed_income"
                and float(row.get("dollar_impact", 0.0)) > 0
                for row in asset_class_impacts
            ),
            len(limit_breaches),
        )

        risk_metrics = self._risk_metrics(risk_snapshot) if payload.include_risk_metrics else []
        generated_at = datetime.now(UTC)
        return StressTestingResponse(
            selected_portfolio=SelectedPortfolio(
                portfolio_id=str(portfolio["id"]),
                name=str(portfolio["name"]),
                base_currency=base_currency,
                benchmark_symbol=payload.benchmark_symbol.upper(),
                positions=len(positions),
                cash=float(portfolio.get("cash", 0.0)),
            ),
            selected_scenario=self._scenario_definition(scenario),
            base_portfolio_value=float(impact["base_portfolio_value"]),
            stressed_portfolio_value=float(impact["stressed_portfolio_value"]),
            dollar_loss=float(impact["dollar_loss"]),
            percent_loss=float(impact["percent_loss"]),
            severity=StressSeverityAssessment(**severity),
            position_impacts=position_impacts,
            asset_class_impacts=asset_class_impacts,
            sector_impacts=sector_impacts,
            currency_impacts=currency_impacts,
            worst_contributors=worst_contributors,
            risk_metrics=risk_metrics,
            fixed_income_stress=fixed_income_summary,
            options_risk=options_risk,
            integrations=self._integrations(symbols_found, symbols_missing, fixed_income_summary, options_risk),
            limit_breaches=limit_breaches,
            warnings=warnings,
            methodology=StressMethodology(
                method="Deterministic scenario shock engine with position-level repricing.",
                assumptions=[
                    "Portfolio Builder positions are the source of current holdings and values.",
                    "Equity, sector, currency, rate, credit and liquidity shocks are deterministic.",
                    "Fixed-income stress uses duration/DV01 approximations when security-level analytics are unavailable.",
                    "Risk metrics scale realized/demo volatility by the scenario volatility shock.",
                ],
                limitations=[
                    "No full revaluation for complex derivatives yet.",
                    "FX stress uses translation approximations when non-USD holdings exist.",
                    "Credit spread impact is duration-based and does not model default migration.",
                    "Outputs are for analysis and are not investment advice.",
                ],
                data_sources=[
                    "Portfolio Builder",
                    "Market Data",
                    "Volatility Lab methodology",
                    "Rates Lab duration assumptions",
                    "Options Pricing Lab integration contract",
                    "Risk Monitor payload contract",
                ],
                generated_at=generated_at,
            ),
            risk_monitor_payload=RiskMonitorStressPayload(
                portfolio_id=str(portfolio["id"]),
                scenario_id=str(scenario["id"]),
                stressed_value=float(impact["stressed_portfolio_value"]),
                percent_loss=float(impact["percent_loss"]),
                worst_contributors=worst_contributors,
                stressed_var=risk_snapshot["stressed_var"] if payload.include_risk_metrics else None,
                stressed_cvar=risk_snapshot["stressed_cvar"] if payload.include_risk_metrics else None,
                stressed_volatility=risk_snapshot["stressed_volatility"] if payload.include_risk_metrics else None,
                breached_limits=limit_breaches,
                severity=str(severity["severity"]),
                generated_at=generated_at,
            ),
            athena_commentary=AthenaStressCommentary(**commentary),
            module_links=self._module_links(payload.portfolio_id, payload.benchmark_symbol)
            if payload.include_module_links
            else {},
        )

    def demo(self) -> StressTestingResponse:
        return self.run(
            StressTestingRunRequest(
                portfolio_id="pf_001",
                scenario_id="risk_off_combined",
            )
        )

    def _resolve_scenario(self, payload: StressTestingRunRequest) -> dict[str, object]:
        if payload.custom_scenario is not None:
            return build_custom_scenario(payload.custom_scenario.model_dump())
        scenario_id = payload.scenario_id or "risk_off_combined"
        scenario = get_predefined_scenario(scenario_id)
        if scenario is None:
            raise ValueError(f"Unknown stress scenario '{scenario_id}'.")
        return scenario

    def _scenario_definition(self, scenario: dict[str, object]) -> StressScenarioDefinition:
        return StressScenarioDefinition(
            id=str(scenario["id"]),
            name=str(scenario["name"]),
            description=str(scenario["description"]),
            shocks=ShockAssumptions(
                asset_class_shocks=dict(scenario.get("asset_class_shocks") or {}),
                sector_shocks=dict(scenario.get("sector_shocks") or {}),
                symbol_shocks=dict(scenario.get("symbol_shocks") or {}),
                rate_shock_bps=float(scenario.get("rate_shock_bps", 0.0)),
                volatility_shock=float(scenario.get("volatility_shock", 0.0)),
                fx_shock=float(scenario.get("fx_shock", 0.0)),
                credit_spread_shock_bps=float(scenario.get("credit_spread_shock_bps", 0.0)),
                liquidity_multiplier=float(scenario.get("liquidity_multiplier", 1.0)),
            ),
        )

    def _risk_metrics(self, snapshot: dict[str, float]) -> list[RiskMetricComparison]:
        return [
            RiskMetricComparison(
                metric="Annualized volatility",
                before=snapshot["before_volatility"],
                after=snapshot["stressed_volatility"],
                unit="ratio",
                source="Volatility Lab / deterministic fallback",
            ),
            RiskMetricComparison(
                metric="VaR",
                before=snapshot["before_var"],
                after=snapshot["stressed_var"],
                unit="currency",
                source="Historical/parametric approximation",
            ),
            RiskMetricComparison(
                metric="CVaR",
                before=snapshot["before_cvar"],
                after=snapshot["stressed_cvar"],
                unit="currency",
                source="Tail-loss approximation",
            ),
        ]

    def _fixed_income_summary(
        self,
        position_impacts: list[dict[str, object]],
        portfolio_value: float,
        scenario: dict[str, object],
    ) -> FixedIncomeStressSummary:
        fixed_income = [
            impact
            for impact in position_impacts
            if impact.get("duration") is not None or str(impact.get("asset_class", "")).lower() == "fixed_income"
        ]
        exposure = sum(float(impact["base_value"]) for impact in fixed_income)
        duration_numerator = sum(
            float(impact["base_value"]) * float(impact["duration"])
            for impact in fixed_income
            if impact.get("duration") is not None
        )
        weighted_duration = duration_numerator / exposure if exposure > 0 else None
        estimated_dv01 = sum(float(impact.get("dv01") or 0.0) for impact in fixed_income) or None
        rate_impact = sum(
            float(impact.get("rate_impact", 0.0)) + float(impact.get("credit_impact", 0.0))
            for impact in fixed_income
        )
        warnings = []
        if exposure == 0:
            warnings.append("No fixed-income positions detected.")
        elif weighted_duration is None:
            warnings.append("Fixed-income exposure found but duration metadata is unavailable.")
        return FixedIncomeStressSummary(
            fixed_income_exposure=exposure,
            fixed_income_weight=exposure / portfolio_value if portfolio_value > 0 else 0.0,
            weighted_average_duration=weighted_duration,
            estimated_dv01=estimated_dv01,
            rate_shock_bps=float(scenario.get("rate_shock_bps", 0.0)),
            credit_spread_shock_bps=float(scenario.get("credit_spread_shock_bps", 0.0)),
            rate_risk_impact=rate_impact,
            data_source="Rates Lab / Demo Duration" if exposure else "No fixed income",
            warnings=warnings,
        )

    def _options_integration(self, position_impacts: list[dict[str, object]]) -> OptionsRiskIntegration:
        option_positions = [
            impact
            for impact in position_impacts
            if "option" in str(impact.get("asset_class", "")).lower()
            or str(impact.get("symbol", "")).upper().endswith(("C", "P"))
        ]
        if not option_positions:
            return OptionsRiskIntegration(
                status="No option positions detected. Options Pricing Lab ready; Greeks integration prepared.",
                options_pricing_lab_ready=True,
                option_positions_detected=False,
                warnings=["Options Greeks stress is prepared but inactive for the current portfolio."],
            )
        return OptionsRiskIntegration(
            status="Option-like positions detected. Delta/Vega stress placeholder applied until contract metadata is stored.",
            options_pricing_lab_ready=True,
            option_positions_detected=True,
            delta_adjusted_exposure=sum(float(item["base_value"]) for item in option_positions),
            gamma_effect=0.0,
            vega_effect=0.0,
            theta_decay=0.0,
            warnings=["Contract-level Greeks are not yet persisted in Portfolio Builder."],
        )

    def _integrations(
        self,
        symbols_found: list[str],
        symbols_missing: list[str],
        fixed_income_summary: FixedIncomeStressSummary,
        options_risk: OptionsRiskIntegration,
    ) -> list[IntegrationStatus]:
        market_status = "Connected" if symbols_found else "Demo"
        return [
            IntegrationStatus(
                module="Portfolio Builder",
                status="Connected",
                data_source="Persistent portfolio store",
                warnings=[],
            ),
            IntegrationStatus(
                module="Market Data",
                status=market_status if not symbols_missing else "Partial Data",
                data_source="Demo market feed + imported prices",
                warnings=[f"Missing return history: {', '.join(symbols_missing)}"] if symbols_missing else [],
            ),
            IntegrationStatus(
                module="Volatility Lab",
                status="Connected" if symbols_found else "Demo",
                data_source="Realized volatility proxy from Market Data",
                warnings=[]
                if symbols_found
                else ["Volatility Lab payload unavailable. Stress risk metrics use deterministic demo assumptions."],
            ),
            IntegrationStatus(
                module="Rates Lab",
                status="Connected" if fixed_income_summary.fixed_income_exposure else "Prepared",
                data_source=fixed_income_summary.data_source,
                warnings=fixed_income_summary.warnings,
            ),
            IntegrationStatus(
                module="Options Pricing Lab",
                status="Prepared",
                data_source="Greeks integration contract",
                warnings=options_risk.warnings,
            ),
            IntegrationStatus(
                module="Risk Monitor",
                status="Risk Monitor Ready",
                data_source="stress_result_payload",
                warnings=["Risk Monitor integration prepared."],
            ),
        ]

    def _warnings(
        self,
        position_impacts: list[dict[str, object]],
        symbols_missing: list[str],
    ) -> list[str]:
        warnings = []
        for impact in position_impacts:
            warnings.extend(str(warning) for warning in impact.get("warnings", []))
        if symbols_missing:
            warnings.append(
                "Volatility Lab payload unavailable for some holdings. Stress risk metrics use deterministic demo assumptions."
            )
        return sorted(set(warnings))

    def _module_links(self, portfolio_id: str, benchmark_symbol: str) -> dict[str, str]:
        return {
            "portfolio_builder": f"/api/portfolios/{portfolio_id}/summary",
            "market_data": f"/api/market-data/coverage?symbols={benchmark_symbol}",
            "volatility_lab": "/api/volatility-lab/analyze-portfolio",
            "rates_lab": "/api/rates-lab/portfolio-exposure",
            "options_pricing_lab": "/api/options-pricing-lab/status",
            "risk_monitor": "/api/risk-monitor/analyze",
        }
