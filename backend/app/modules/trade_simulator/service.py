from fastapi import HTTPException

from app.modules.market_data.repository import MarketDataRepository
from app.modules.risk_analytics.schemas import RealizedRiskResult
from app.modules.risk_analytics.service import RiskAnalyticsService
from app.modules.trade_simulator.domain.constraints import build_constraint_warnings
from app.modules.trade_simulator.domain.execution_quality import (
    calculate_price_shortfall,
    describe_order_type_impact,
    detect_liquidity_warning,
    simulate_execution_price,
)
from app.modules.trade_simulator.domain.suitability import (
    build_athena_commentary,
    build_suitability_commentary,
    determine_suitability_status,
)
from app.modules.trade_simulator.domain.trade_impact import (
    apply_trade_to_positions,
    calculate_cash_after_trade,
    calculate_portfolio_metrics,
    decorate_positions,
    estimate_cvar_95,
    estimate_max_drawdown,
    estimate_tracking_error,
    estimate_var_95,
    calculate_information_ratio,
)
from app.modules.trade_simulator.domain.transaction_costs import (
    calculate_cost_percent,
    calculate_gross_trade_value,
    calculate_total_implementation_cost,
    estimate_commission,
    estimate_fees,
    estimate_market_impact,
    estimate_slippage,
    estimate_spread_cost,
)
from app.modules.trade_simulator.repository import TradeSimulatorRepository
from app.modules.trade_simulator.schemas import (
    AthenaTradeCommentaryResponse,
    BenchmarkActiveRiskResponse,
    ConstraintWarning,
    ExecutionQualityResponse,
    ImpactMetric,
    PreTradeImpactResponse,
    RiskImpactResponse,
    SimulationResultSummary,
    SuitabilityReviewResponse,
    TradeModuleStatus,
    TradeSimulationRequest,
    TradeSimulationResponse,
    TradeTicketSummary,
    TransactionCostAnalysisResponse,
)


class TradeSimulatorService:
    def __init__(self, repository: TradeSimulatorRepository) -> None:
        self.repository = repository
        self.risk_analytics_service = RiskAnalyticsService(
            MarketDataRepository(repository.db),
        )

    def get_module_status(self) -> TradeModuleStatus:
        return TradeModuleStatus(
            detail="Trade Simulator is ready for deterministic pre-trade analysis.",
            simulation_ready=self.repository.simulation_available(),
        )

    def simulate_trade(
        self,
        payload: TradeSimulationRequest,
    ) -> TradeSimulationResponse:
        portfolio = self.repository.get_portfolio(payload.portfolio_id)
        if portfolio is None:
            raise HTTPException(status_code=404, detail="Portfolio not found.")

        positions = self.repository.list_positions(payload.portfolio_id)
        asset_metadata = self.repository.get_asset_metadata(payload.symbol) or {}
        symbol = payload.symbol.upper()
        asset_name = payload.asset_name or str(
            asset_metadata.get("name") or asset_metadata.get("asset_name") or symbol,
        )
        asset_type = payload.asset_type or str(asset_metadata.get("asset_type") or "equity")
        sector = str(asset_metadata.get("sector") or self._position_field(positions, symbol, "sector") or "Unknown")
        country = str(asset_metadata.get("country") or self._position_field(positions, symbol, "country") or "United States")
        currency = str(asset_metadata.get("currency") or self._position_field(positions, symbol, "currency") or portfolio["base_currency"])
        cash_before = float(portfolio["cash"])
        decorated_before = decorate_positions(positions, cash_before)
        portfolio_value_before = sum(float(position["market_value"]) for position in decorated_before) + cash_before

        gross_trade_value = calculate_gross_trade_value(
            payload.quantity,
            payload.estimated_price,
        )
        commission = estimate_commission(gross_trade_value)
        fees = estimate_fees(gross_trade_value)
        spread_cost = estimate_spread_cost(gross_trade_value, asset_type)
        slippage = estimate_slippage(gross_trade_value, payload.order_type)
        market_impact = estimate_market_impact(gross_trade_value, portfolio_value_before)
        total_cost = calculate_total_implementation_cost(
            commission,
            fees,
            spread_cost,
            slippage,
            market_impact,
        )
        cash_after = calculate_cash_after_trade(
            cash_before=cash_before,
            action=payload.action,
            gross_trade_value=gross_trade_value,
            total_implementation_cost=total_cost,
        )
        positions_after = apply_trade_to_positions(
            positions,
            action=payload.action,
            symbol=symbol,
            quantity=payload.quantity,
            estimated_price=payload.estimated_price,
            asset_name=asset_name,
            asset_type=asset_type,
            currency=currency,
            sector=sector,
            country=country,
        )
        metrics_before = calculate_portfolio_metrics(positions, cash_before, symbol)
        metrics_after = calculate_portfolio_metrics(positions_after, cash_after, symbol)
        decorated_after = decorate_positions(positions_after, cash_after)
        realized_risk_before = self.risk_analytics_service.calculate_realized_portfolio_risk(
            self._weights_by_symbol(decorated_before, "invested_weight"),
            benchmark_symbol=str(portfolio["benchmark"]),
        )
        realized_risk_after = self.risk_analytics_service.calculate_realized_portfolio_risk(
            self._weights_by_symbol(decorated_after, "invested_weight"),
            benchmark_symbol=str(portfolio["benchmark"]),
        )
        risk_source = self._risk_source_metadata(
            realized_risk_before,
            realized_risk_after,
        )
        existing_quantity = self._existing_quantity(positions, symbol)
        constraint_warnings = build_constraint_warnings(
            action=payload.action,
            symbol=symbol,
            requested_quantity=payload.quantity,
            available_quantity=existing_quantity,
            gross_trade_value=gross_trade_value,
            portfolio_value_after=float(metrics_after["portfolio_value"]),
            metrics_after=metrics_after,
            sector_name=sector,
            asset_type=asset_type,
        )
        risk_metrics = self._risk_impact_metrics(
            metrics_before,
            metrics_after,
            realized_risk_before,
            realized_risk_after,
        )
        suitability_status = determine_suitability_status(
            constraint_warnings,
            risk_increase=float(metrics_after["portfolio_volatility"])
            - float(metrics_before["portfolio_volatility"]),
            concentration_increase=float(metrics_after["largest_position_weight"])
            - float(metrics_before["largest_position_weight"]),
            cash_after=cash_after,
        )
        suitability_commentary = build_suitability_commentary(
            action=payload.action,
            symbol=symbol,
            suitability_status=suitability_status,
            warnings=constraint_warnings,
            expected_return_change=float(metrics_after["expected_return"])
            - float(metrics_before["expected_return"]),
            volatility_change=float(metrics_after["portfolio_volatility"])
            - float(metrics_before["portfolio_volatility"]),
            concentration_change=float(metrics_after["largest_position_weight"])
            - float(metrics_before["largest_position_weight"]),
        )
        simulated_price = simulate_execution_price(
            action=payload.action,
            estimated_price=payload.estimated_price,
            order_type=payload.order_type,
        )
        price_shortfall = calculate_price_shortfall(
            action=payload.action,
            expected_price=payload.estimated_price,
            simulated_price=simulated_price,
        )
        tracking_error_before = estimate_tracking_error(
            float(metrics_before["expected_return"]),
            float(metrics_before["largest_position_weight"]),
        )
        tracking_error_after = estimate_tracking_error(
            float(metrics_after["expected_return"]),
            float(metrics_after["largest_position_weight"]),
        )
        information_ratio_before = calculate_information_ratio(
            float(metrics_before["expected_return"]),
            tracking_error_before,
        )
        information_ratio_after = calculate_information_ratio(
            float(metrics_after["expected_return"]),
            tracking_error_after,
        )
        ticket = TradeTicketSummary(
            portfolio_id=payload.portfolio_id,
            action=payload.action,
            symbol=symbol,
            asset_name=asset_name,
            asset_type=asset_type,
            quantity=payload.quantity,
            estimated_price=payload.estimated_price,
            order_type=payload.order_type,
            limit_price=payload.limit_price,
            time_in_force=payload.time_in_force,
            trade_rationale=payload.trade_rationale,
            gross_trade_value=gross_trade_value,
            estimated_commission=commission,
            estimated_fees=fees,
            estimated_spread_cost=spread_cost,
            estimated_slippage=slippage,
            estimated_market_impact=market_impact,
            estimated_total_implementation_cost=total_cost,
            cash_impact=cash_after - cash_before,
            estimated_cash_after_trade=cash_after,
            demo_assumptions=[
                "Demo prices are user-entered or sourced from deterministic demo data.",
                "Spread, slippage and market impact are deterministic assumptions.",
                "No real trade execution or order routing occurs.",
            ],
        )
        response_warnings = [
            ConstraintWarning.model_validate(warning)
            for warning in constraint_warnings
        ]
        trade_status = self._trade_status(suitability_status, response_warnings)
        athena_summary = build_athena_commentary(
            action=payload.action,
            symbol=symbol,
            expected_return_change=float(metrics_after["expected_return"])
            - float(metrics_before["expected_return"]),
            volatility_change=float(metrics_after["portfolio_volatility"])
            - float(metrics_before["portfolio_volatility"]),
            concentration_change=float(metrics_after["largest_position_weight"])
            - float(metrics_before["largest_position_weight"]),
            suitability_status=suitability_status,
            warnings=constraint_warnings,
        )

        return TradeSimulationResponse(
            trade_ticket=ticket,
            pre_trade_impact=PreTradeImpactResponse(
                metrics=self._portfolio_impact_metrics(metrics_before, metrics_after),
                interpretation=self._impact_interpretation(metrics_before, metrics_after),
            ),
            risk_impact=RiskImpactResponse(
                metrics=risk_metrics,
                message=str(risk_source["message"]),
                badges=list(risk_source["badges"]),
                metric_source=str(risk_source["metric_source"]),
                fallback_used=bool(risk_source["fallback_used"]),
                fallback_reason=risk_source["fallback_reason"],
                observations=int(risk_source["observations"]),
                symbols_found=list(risk_source["symbols_found"]),
                symbols_missing=list(risk_source["symbols_missing"]),
                quality_warnings=list(risk_source["quality_warnings"]),
            ),
            suitability_review=SuitabilityReviewResponse(
                status=suitability_status,
                commentary=suitability_commentary,
                investor_type="Individual",
                risk_tolerance="Moderate",
                time_horizon="Long-term",
                liquidity_needs="Maintain minimum cash reserve",
                factors=[
                    "Investment Policy Statement",
                    "Current portfolio concentration",
                    "Sector limits",
                    "Minimum cash reserve",
                    "Benchmark deviation",
                    "Turnover impact",
                ],
            ),
            constraints_warnings=response_warnings,
            transaction_cost_analysis=TransactionCostAnalysisResponse(
                gross_trade_value=gross_trade_value,
                explicit_costs={"commission": commission, "fees": fees},
                implicit_costs={
                    "bid_ask_spread": spread_cost,
                    "slippage": slippage,
                    "market_impact": market_impact,
                },
                total_estimated_cost=total_cost,
                cost_as_percent_of_trade_value=calculate_cost_percent(
                    total_cost,
                    gross_trade_value,
                ),
                estimated_net_trade_value=(
                    gross_trade_value + total_cost
                    if payload.action == "BUY"
                    else gross_trade_value - total_cost
                ),
                implementation_shortfall_placeholder=price_shortfall * payload.quantity,
                note=(
                    "Transaction costs reduce realized portfolio performance and "
                    "should be considered before execution."
                ),
                badges=["Demo execution model", "Placeholder market impact"],
            ),
            execution_quality=ExecutionQualityResponse(
                expected_execution_price=payload.estimated_price,
                simulated_execution_price=simulated_price,
                price_improvement_or_shortfall=price_shortfall,
                implementation_shortfall=price_shortfall * payload.quantity,
                order_type_impact=describe_order_type_impact(payload.order_type),
                liquidity_warning=detect_liquidity_warning(
                    gross_trade_value=gross_trade_value,
                    portfolio_value=portfolio_value_before,
                ),
                badge="Demo execution model",
            ),
            benchmark_active_risk=BenchmarkActiveRiskResponse(
                benchmark_name=str(portfolio["benchmark"]),
                active_weight_before=self._active_weight(metrics_before, portfolio, symbol),
                active_weight_after=self._active_weight(metrics_after, portfolio, symbol),
                active_exposure_after_trade=self._active_exposure(metrics_after, portfolio, symbol),
                tracking_error_impact=tracking_error_after - tracking_error_before,
                information_ratio_impact=(
                    None
                    if information_ratio_before is None or information_ratio_after is None
                    else information_ratio_after - information_ratio_before
                ),
                active_management_warning=(
                    f"Portfolio remains highly active versus {portfolio['benchmark']} "
                    "benchmark because benchmark constituents are placeholders."
                ),
                badge="Requires benchmark constituent feed",
            ),
            athena_commentary=AthenaTradeCommentaryResponse(
                summary=athena_summary,
                bullets=[
                    f"Expected return change: {float(metrics_after['expected_return']) - float(metrics_before['expected_return']):.2%}.",
                    f"Volatility change: {float(metrics_after['portfolio_volatility']) - float(metrics_before['portfolio_volatility']):.2%}.",
                    f"Concentration change: {float(metrics_after['largest_position_weight']) - float(metrics_before['largest_position_weight']):.2%}.",
                    f"Suitability status: {suitability_status}.",
                ],
            ),
            simulation_result=SimulationResultSummary(
                trade_status=trade_status,
                main_reason=self._main_reason(
                    trade_status,
                    response_warnings,
                    suitability_status,
                ),
                key_warnings=[warning.message for warning in response_warnings[:4]],
                estimated_cost=total_cost,
                risk_impact=self._risk_impact_label(metrics_before, metrics_after),
                suitability_result=suitability_status,
                notice="Simulation only. No trades are executed.",
            ),
        )

    def _portfolio_impact_metrics(
        self,
        before: dict[str, float | str],
        after: dict[str, float | str],
    ) -> list[ImpactMetric]:
        metric_specs = [
            ("Portfolio value", "portfolio_value", None),
            ("Cash", "cash", 0.02),
            ("Position weight", "position_weight", 0.25),
            ("Sector exposure", "sector_exposure", 0.50),
            ("Asset type allocation", "asset_type_allocation", 0.80),
            ("Currency exposure", "currency_exposure", 1.00),
            ("Largest position weight", "largest_position_weight", 0.25),
            ("Top 3 holdings concentration", "top_3_holdings_concentration", 0.80),
            ("Diversification score", "diversification_score", None),
            ("Expected return", "expected_return", None),
            ("Portfolio volatility", "portfolio_volatility", None),
        ]
        return [
            self._impact_metric(label, key, before, after, limit)
            for label, key, limit in metric_specs
        ]

    def _risk_impact_metrics(
        self,
        before: dict[str, float | str],
        after: dict[str, float | str],
        realized_before: RealizedRiskResult,
        realized_after: RealizedRiskResult,
    ) -> list[ImpactMetric]:
        portfolio_value_before = float(before["portfolio_value"])
        portfolio_value_after = float(after["portfolio_value"])
        volatility_before = float(before["portfolio_volatility"])
        volatility_after = float(after["portfolio_volatility"])
        tracking_error_before = estimate_tracking_error(
            float(before["expected_return"]),
            float(before["largest_position_weight"]),
        )
        tracking_error_after = estimate_tracking_error(
            float(after["expected_return"]),
            float(after["largest_position_weight"]),
        )
        information_ratio_before = calculate_information_ratio(
            float(before["expected_return"]),
            tracking_error_before,
        )
        information_ratio_after = calculate_information_ratio(
            float(after["expected_return"]),
            tracking_error_after,
        )
        realized_available = self._realized_risk_available(
            realized_before,
            realized_after,
        )
        expected_return_before = float(before["expected_return"])
        expected_return_after = float(after["expected_return"])
        sharpe_before = self._sharpe(expected_return_before, volatility_before)
        sharpe_after = self._sharpe(expected_return_after, volatility_after)
        var_before = estimate_var_95(portfolio_value_before, volatility_before)
        var_after = estimate_var_95(portfolio_value_after, volatility_after)
        cvar_before = estimate_cvar_95(portfolio_value_before, volatility_before)
        cvar_after = estimate_cvar_95(portfolio_value_after, volatility_after)
        max_drawdown_before = estimate_max_drawdown(volatility_before)
        max_drawdown_after = estimate_max_drawdown(volatility_after)

        if realized_available:
            expected_return_before = (
                realized_before.realized_annualized_return
                if realized_before.realized_annualized_return is not None
                else expected_return_before
            )
            expected_return_after = (
                realized_after.realized_annualized_return
                if realized_after.realized_annualized_return is not None
                else expected_return_after
            )
            volatility_before = realized_before.realized_volatility or volatility_before
            volatility_after = realized_after.realized_volatility or volatility_after
            sharpe_before = realized_before.realized_sharpe_ratio
            sharpe_after = realized_after.realized_sharpe_ratio
            var_before = (
                realized_before.portfolio_var_95 * portfolio_value_before
                if realized_before.portfolio_var_95 is not None
                else var_before
            )
            var_after = (
                realized_after.portfolio_var_95 * portfolio_value_after
                if realized_after.portfolio_var_95 is not None
                else var_after
            )
            cvar_before = (
                realized_before.portfolio_cvar_95 * portfolio_value_before
                if realized_before.portfolio_cvar_95 is not None
                else cvar_before
            )
            cvar_after = (
                realized_after.portfolio_cvar_95 * portfolio_value_after
                if realized_after.portfolio_cvar_95 is not None
                else cvar_after
            )
            max_drawdown_before = (
                realized_before.max_drawdown
                if realized_before.max_drawdown is not None
                else max_drawdown_before
            )
            max_drawdown_after = (
                realized_after.max_drawdown
                if realized_after.max_drawdown is not None
                else max_drawdown_after
            )
            tracking_error_before = (
                realized_before.tracking_error
                if realized_before.tracking_error is not None
                else tracking_error_before
            )
            tracking_error_after = (
                realized_after.tracking_error
                if realized_after.tracking_error is not None
                else tracking_error_after
            )
            information_ratio_before = calculate_information_ratio(
                expected_return_before,
                tracking_error_before,
            )
            information_ratio_after = calculate_information_ratio(
                expected_return_after,
                tracking_error_after,
            )

        risk_values = {
            "Expected return": (
                expected_return_before,
                expected_return_after,
            ),
            "Volatility": (volatility_before, volatility_after),
            "Sharpe ratio": (
                sharpe_before,
                sharpe_after,
            ),
            "Beta": (float(before["portfolio_beta"]), float(after["portfolio_beta"])),
            "VaR 95%": (
                var_before,
                var_after,
            ),
            "CVaR 95%": (
                cvar_before,
                cvar_after,
            ),
            "Max drawdown": (
                max_drawdown_before,
                max_drawdown_after,
            ),
            "Tracking error": (tracking_error_before, tracking_error_after),
            "Information ratio": (information_ratio_before, information_ratio_after),
            "Concentration risk": (
                float(before["largest_position_weight"]),
                float(after["largest_position_weight"]),
            ),
        }
        return [
            ImpactMetric(
                name=name,
                before=before_value,
                after=after_value,
                change=None
                if before_value is None or after_value is None
                else float(after_value) - float(before_value),
                status="review"
                if after_value is not None
                and before_value is not None
                and name in {"Volatility", "VaR 95%", "CVaR 95%", "Concentration risk"}
                and float(after_value) > float(before_value)
                else "ok",
            )
            for name, (before_value, after_value) in risk_values.items()
        ]

    def _impact_metric(
        self,
        label: str,
        key: str,
        before: dict[str, float | str],
        after: dict[str, float | str],
        limit: float | None,
    ) -> ImpactMetric:
        before_value = float(before[key])
        after_value = float(after[key])
        status = "ok"
        if limit is not None:
            if label == "Cash":
                status = "breach" if float(after["cash_weight"]) < limit else "ok"
            else:
                status = "breach" if after_value > limit else "ok"

        return ImpactMetric(
            name=label,
            before=before_value,
            after=after_value,
            change=after_value - before_value,
            limit=limit,
            status=status,
        )

    def _impact_interpretation(
        self,
        before: dict[str, float | str],
        after: dict[str, float | str],
    ) -> str:
        return_change = float(after["expected_return"]) - float(before["expected_return"])
        risk_change = float(after["portfolio_volatility"]) - float(before["portfolio_volatility"])
        concentration_change = float(after["largest_position_weight"]) - float(before["largest_position_weight"])
        return (
            f"Expected return change {return_change:.2%}; "
            f"volatility change {risk_change:.2%}; "
            f"largest-position concentration change {concentration_change:.2%}."
        )

    def _risk_source_metadata(
        self,
        realized_before: RealizedRiskResult,
        realized_after: RealizedRiskResult,
    ) -> dict[str, object]:
        fallback_used = realized_before.fallback_used or realized_after.fallback_used
        fallback_reason = realized_before.fallback_reason or realized_after.fallback_reason
        quality_warnings = self._unique_values(
            [
                *realized_before.quality_warnings,
                *realized_after.quality_warnings,
            ],
        )
        symbols_missing = self._unique_values(
            [
                *realized_before.symbols_missing,
                *realized_after.symbols_missing,
            ],
        )
        symbols_found = self._unique_values(
            [
                *realized_before.symbols_found,
                *realized_after.symbols_found,
            ],
        )
        observations = min(realized_before.observations, realized_after.observations)

        if fallback_used:
            badges = [
                "Demo",
                "Requires Market Data",
                "Placeholder VaR/CVaR",
            ]
            if symbols_missing:
                badges.append("Partial Data")
            return {
                "metric_source": "deterministic_demo",
                "fallback_used": True,
                "fallback_reason": fallback_reason,
                "observations": observations,
                "symbols_found": symbols_found,
                "symbols_missing": symbols_missing,
                "quality_warnings": quality_warnings,
                "message": (
                    "Realized Market Data return series unavailable. "
                    "Falling back to deterministic demo assumptions."
                ),
                "badges": badges,
            }

        badges = ["Realized", "Market Data returns"]
        if quality_warnings:
            badges.append("Partial Data")
        if (
            realized_before.tracking_error is None
            or realized_after.tracking_error is None
        ):
            badges.append("Requires benchmark history")

        return {
            "metric_source": "realized_market_data",
            "fallback_used": False,
            "fallback_reason": None,
            "observations": observations,
            "symbols_found": symbols_found,
            "symbols_missing": symbols_missing,
            "quality_warnings": quality_warnings,
            "message": (
                "Risk impact uses realized Market Data return series for volatility, "
                "VaR, CVaR, Sharpe ratio and tracking error when benchmark history is available."
            ),
            "badges": badges,
        }

    def _realized_risk_available(
        self,
        realized_before: RealizedRiskResult,
        realized_after: RealizedRiskResult,
    ) -> bool:
        return (
            not realized_before.fallback_used
            and not realized_after.fallback_used
            and realized_before.realized_volatility is not None
            and realized_after.realized_volatility is not None
        )

    def _weights_by_symbol(
        self,
        positions: list[dict[str, object]],
        weight_key: str,
    ) -> dict[str, float]:
        weights: dict[str, float] = {}
        for position in positions:
            symbol = str(position["symbol"]).upper()
            weights[symbol] = weights.get(symbol, 0.0) + float(position[weight_key])
        return weights

    def _unique_values(self, values: list[str]) -> list[str]:
        unique_values: list[str] = []
        for value in values:
            if value not in unique_values:
                unique_values.append(value)
        return unique_values

    def _position_field(
        self,
        positions: list[dict[str, object]],
        symbol: str,
        field_name: str,
    ) -> object | None:
        for position in positions:
            if str(position["symbol"]).upper() == symbol.upper():
                return position.get(field_name)
        return None

    def _existing_quantity(
        self,
        positions: list[dict[str, object]],
        symbol: str,
    ) -> float:
        for position in positions:
            if str(position["symbol"]).upper() == symbol.upper():
                return float(position["quantity"])
        return 0.0

    def _trade_status(
        self,
        suitability_status: str,
        warnings: list[ConstraintWarning],
    ) -> str:
        if suitability_status == "Not Suitable" or any(
            warning.name == "Sell quantity" for warning in warnings
        ):
            return "Rejected"
        if suitability_status == "Requires Review" or warnings:
            return "Requires Review"
        return "Approved"

    def _main_reason(
        self,
        trade_status: str,
        warnings: list[ConstraintWarning],
        suitability_status: str,
    ) -> str:
        if warnings:
            return warnings[0].message
        if trade_status == "Approved":
            return "No major demo policy breach detected."
        return f"Suitability result is {suitability_status}."

    def _risk_impact_label(
        self,
        before: dict[str, float | str],
        after: dict[str, float | str],
    ) -> str:
        if float(after["portfolio_volatility"]) > float(before["portfolio_volatility"]):
            return "Risk increases"
        if float(after["portfolio_volatility"]) < float(before["portfolio_volatility"]):
            return "Risk decreases"
        return "Risk unchanged"

    def _active_weight(
        self,
        metrics: dict[str, float | str],
        portfolio: dict[str, object],
        symbol: str,
    ) -> float:
        benchmark_weight = 1.0 if symbol.upper() == str(portfolio["benchmark"]).upper() else 0.0
        return float(metrics["position_weight"]) - benchmark_weight

    def _active_exposure(
        self,
        metrics: dict[str, float | str],
        portfolio: dict[str, object],
        symbol: str,
    ) -> float:
        return abs(self._active_weight(metrics, portfolio, symbol))

    def _sharpe(self, expected_return: float, volatility: float) -> float | None:
        if volatility <= 0:
            return None
        return (expected_return - 0.04) / volatility
