from fastapi import HTTPException

from app.modules.portfolio_builder.domain import (
    calculate_allocation_by_asset,
    calculate_allocation_by_asset_type,
    calculate_allocation_by_country,
    calculate_allocation_by_currency,
    calculate_allocation_by_region,
    calculate_allocation_by_sector,
    calculate_cash_weight,
    calculate_invested_value,
    calculate_concentration_metrics,
    calculate_portfolio_market_value,
    calculate_portfolio_weights,
    calculate_invested_weight,
    calculate_portfolio_weight,
    calculate_position_cost_basis,
    calculate_position_market_value,
    calculate_position_unrealized_pnl,
    calculate_position_unrealized_pnl_percent,
    validate_position_input,
)
from app.modules.portfolio_builder.domain.constraints import (
    check_allowed_asset_types,
    check_asset_type_limit,
    check_currency_limit,
    check_min_cash_limit,
    check_sector_limit,
    check_single_position_limit,
    summarize_constraint_breaches,
)
from app.modules.portfolio_builder.domain.behavioral import (
    create_behavioral_bias_summary,
    detect_concentration_overconfidence_warning,
    detect_home_bias_placeholder,
    detect_loss_aversion_placeholder,
)
from app.modules.portfolio_builder.domain.capm import (
    calculate_capm_required_return,
    calculate_market_risk_premium,
    calculate_weighted_portfolio_beta,
    compare_expected_return_to_required_return,
)
from app.modules.portfolio_builder.domain.diversification import (
    calculate_diversification_score,
    calculate_effective_number_of_holdings,
    calculate_hhi_concentration,
    calculate_largest_position_weight,
    calculate_top_n_holdings_weight,
    classify_concentration_level,
    identify_concentration_warnings,
)
from app.modules.portfolio_builder.domain.efficient_frontier import (
    create_efficient_frontier_demo_points,
)
from app.modules.portfolio_builder.domain.performance import (
    calculate_holding_period_return,
    calculate_return_contribution,
    calculate_time_weighted_return,
)
from app.modules.portfolio_builder.domain.performance_ratios import (
    calculate_active_return,
    calculate_information_ratio,
    calculate_jensen_alpha,
    calculate_sharpe_ratio,
    calculate_tracking_error,
    calculate_treynor_ratio,
)
from app.modules.portfolio_builder.domain.pooled_vehicles import (
    calculate_etf_exposure,
    calculate_pooled_vehicle_exposure,
    calculate_single_stock_exposure,
    classify_pooled_vehicle_usage,
)
from app.modules.portfolio_builder.domain.rebalancing import (
    create_rebalance_preview,
    detect_tolerance_band_breaches,
    calculate_rebalance_value_differences,
    estimate_turnover,
)
from app.modules.portfolio_builder.domain.risk_return import (
    calculate_asset_contribution_to_return,
    calculate_asset_contribution_to_risk_placeholder,
    calculate_diversification_benefit,
    calculate_portfolio_standard_deviation,
    calculate_portfolio_variance_from_covariance_matrix,
    calculate_weighted_expected_return,
)
from app.modules.portfolio_builder.domain.risk_tolerance import (
    classify_overall_risk_tolerance,
    create_risk_tolerance_summary,
    detect_ability_willingness_conflict,
)
from app.modules.portfolio_builder.domain.suitability import (
    classify_allocation_quality,
    classify_benchmark_alignment,
    classify_cash_level,
    classify_diversification_quality,
    compare_allocation_to_policy,
    create_default_policy,
    create_portfolio_diagnostics_summary,
    identify_policy_breaches,
    validate_policy_constraints,
)
from app.modules.portfolio_builder.domain.utility import (
    calculate_utility_score,
    classify_risk_aversion,
)
from app.modules.portfolio_builder.repository import (
    PortfolioRepository,
    PositionRepository,
)
from app.modules.portfolio_builder.schemas import (
    AllocationResponse,
    CapmResponse,
    CfaConceptsResponse,
    ConcentrationResponse,
    ConstraintsResponse,
    DeleteResponse,
    DiversificationResponse,
    EfficientFrontierResponse,
    BenchmarkResponse,
    BehavioralBiasResponse,
    InvestorProfileResponse,
    PerformanceMeasurementResponse,
    PolicyComparisonItem,
    PolicyResponse,
    PortfolioCreate,
    PortfolioConstraints,
    PortfolioDiagnosticsResponse,
    PortfolioListResponse,
    PortfolioPolicy,
    PortfolioRead,
    PortfolioSummary,
    PortfolioUpdate,
    PositionCreate,
    PositionListResponse,
    PositionRead,
    PositionUpdate,
    RebalancingPreviewResponse,
    RiskAdjustedPerformanceResponse,
    RiskReturnResponse,
    RiskToleranceResponse,
    TargetAllocation,
    TargetAllocationResponse,
    UtilityResponse,
    PooledVehicleExposureResponse,
)


class PortfolioService:
    def __init__(
        self,
        repository: PortfolioRepository,
        position_repository: PositionRepository,
    ) -> None:
        self.repository = repository
        self.position_repository = position_repository

    def list_portfolios(self) -> PortfolioListResponse:
        return PortfolioListResponse(
            detail="Demo portfolios are available for builder workflows.",
            items=[
                PortfolioRead.model_validate(portfolio)
                for portfolio in self.repository.list_portfolios()
            ],
        )

    def get_portfolio(self, portfolio_id: str) -> PortfolioRead:
        return PortfolioRead.model_validate(self._get_portfolio_or_404(portfolio_id))

    def create_portfolio(self, payload: PortfolioCreate) -> PortfolioRead:
        portfolio = self.repository.create_portfolio(payload.model_dump())
        return PortfolioRead.model_validate(portfolio)

    def update_portfolio(
        self,
        portfolio_id: str,
        payload: PortfolioUpdate,
    ) -> PortfolioRead:
        self._get_portfolio_or_404(portfolio_id)
        portfolio = self.repository.update_portfolio(
            portfolio_id,
            payload.model_dump(exclude_none=True),
        )
        if portfolio is None:
            raise HTTPException(status_code=404, detail="Portfolio not found.")

        return PortfolioRead.model_validate(portfolio)

    def delete_portfolio(self, portfolio_id: str) -> DeleteResponse:
        self._get_portfolio_or_404(portfolio_id)
        self.repository.delete_portfolio(portfolio_id)
        return DeleteResponse(status="deleted", id=portfolio_id)

    def get_summary(self, portfolio_id: str) -> PortfolioSummary:
        portfolio = self._get_portfolio_or_404(portfolio_id)
        positions = self._decorated_positions(portfolio_id)
        market_values = [float(position["market_value"]) for position in positions]
        cash = float(portfolio["cash"])
        invested_value = calculate_invested_value(market_values)
        total_market_value = calculate_portfolio_market_value(market_values, cash)
        invested_weights = [float(position["invested_weight"]) for position in positions]

        return PortfolioSummary(
            portfolio_id=portfolio_id,
            name=str(portfolio["name"]),
            base_currency=str(portfolio["base_currency"]),
            benchmark=str(portfolio["benchmark"]),
            total_market_value=total_market_value,
            total_value=total_market_value,
            invested_value=invested_value,
            cash=cash,
            cash_weight=calculate_cash_weight(market_values, cash),
            number_of_positions=len(positions),
            number_of_asset_classes=len({str(position["asset_type"]) for position in positions}),
            number_of_sectors=len({str(position["sector"]) for position in positions}),
            number_of_currencies=len({str(position["currency"]) for position in positions}),
            largest_position=self._largest_position_symbol(positions),
            largest_position_weight=calculate_largest_position_weight(invested_weights),
            top_5_holdings_weight=calculate_top_n_holdings_weight(invested_weights, 5),
            diversification_score=calculate_diversification_score(invested_weights),
            data_source="Athena deterministic demo portfolio store",
        )

    def get_allocation(
        self,
        portfolio_id: str,
        allocation_type: str,
    ) -> AllocationResponse:
        self._get_portfolio_or_404(portfolio_id)
        positions = self._decorated_positions(portfolio_id)
        calculators = {
            "assets": calculate_allocation_by_asset,
            "sectors": calculate_allocation_by_sector,
            "currencies": calculate_allocation_by_currency,
            "countries": calculate_allocation_by_country,
            "asset-types": calculate_allocation_by_asset_type,
            "regions": calculate_allocation_by_region,
        }
        calculator = calculators[allocation_type]

        return AllocationResponse(
            portfolio_id=portfolio_id,
            allocation_type=allocation_type,
            items=calculator(positions),
        )

    def get_concentration(self, portfolio_id: str) -> ConcentrationResponse:
        self._get_portfolio_or_404(portfolio_id)
        positions = self._decorated_positions(portfolio_id)
        metrics = self._concentration_metrics(positions)

        return ConcentrationResponse(portfolio_id=portfolio_id, **metrics)

    def get_diversification(self, portfolio_id: str) -> DiversificationResponse:
        positions = self._decorated_positions(portfolio_id)
        metrics = self._concentration_metrics(positions)

        return DiversificationResponse(
            portfolio_id=portfolio_id,
            sector_concentration=self._allocation_weight_map(
                calculate_allocation_by_sector(positions),
            ),
            currency_concentration=self._allocation_weight_map(
                calculate_allocation_by_currency(positions),
            ),
            asset_type_concentration=self._allocation_weight_map(
                calculate_allocation_by_asset_type(positions),
            ),
            **metrics,
        )

    def get_risk_return(self, portfolio_id: str) -> RiskReturnResponse:
        positions = self._decorated_positions(portfolio_id)
        weights = [float(position["invested_weight"]) for position in positions]
        expected_returns = [
            self._expected_return_for_asset_type(str(position["asset_type"]))
            for position in positions
        ]
        expected_return = calculate_weighted_expected_return(expected_returns, weights)
        volatilities = [
            self._volatility_for_asset_type(str(position["asset_type"]))
            for position in positions
        ]
        covariance_matrix = self._demo_covariance_matrix(volatilities)
        variance = calculate_portfolio_variance_from_covariance_matrix(
            weights,
            covariance_matrix,
        )
        standard_deviation = calculate_portfolio_standard_deviation(variance)
        weighted_average_volatility = sum(
            weight * volatility for weight, volatility in zip(weights, volatilities)
        )

        return RiskReturnResponse(
            portfolio_id=portfolio_id,
            expected_return=expected_return,
            variance=variance,
            standard_deviation=standard_deviation,
            diversification_benefit=calculate_diversification_benefit(
                weighted_average_volatility,
                standard_deviation,
            ),
            risk_return_profile=self._risk_return_profile(expected_return, standard_deviation),
            covariance_matrix_status="Demo covariance scaffold based on asset-type volatilities.",
            correlation_matrix_status="Placeholder correlation assumptions; no full return history yet.",
            contributions=[
                {
                    "symbol": str(position["symbol"]),
                    "weight": weight,
                    "expected_return": expected_return_value,
                    "return_contribution": calculate_asset_contribution_to_return(
                        weight,
                        expected_return_value,
                    ),
                    "risk_contribution_placeholder": calculate_asset_contribution_to_risk_placeholder(
                        weight,
                    ),
                }
                for position, weight, expected_return_value in zip(
                    positions,
                    weights,
                    expected_returns,
                )
            ],
            notes=[
                "Expected returns and covariance are deterministic demo scaffolding.",
                "No VaR, CVaR or advanced risk engine is calculated in Portfolio Builder.",
            ],
        )

    def get_benchmark(self, portfolio_id: str) -> BenchmarkResponse:
        portfolio = self._get_portfolio_or_404(portfolio_id)
        positions = self._decorated_positions(portfolio_id)
        holdings = []
        for position in positions:
            symbol = str(position["symbol"])
            benchmark_weight = 1.0 if symbol == str(portfolio["benchmark"]) else 0.0
            portfolio_weight = float(position["portfolio_weight"])
            holdings.append(
                {
                    "name": symbol,
                    "portfolio_weight": portfolio_weight,
                    "benchmark_weight": benchmark_weight,
                    "active_weight": portfolio_weight - benchmark_weight,
                }
            )

        return BenchmarkResponse(
            portfolio_id=portfolio_id,
            benchmark_symbol=str(portfolio["benchmark"]),
            total_active_weight=sum(abs(row["active_weight"]) for row in holdings) / 2,
            active_return=None,
            tracking_difference=None,
            tracking_error=None,
            holdings=holdings,
            notes=[
                "Benchmark weights are placeholders until a benchmark constituent feed exists.",
                "Active return and tracking error require benchmark return history.",
            ],
        )

    def get_policy(self, portfolio_id: str) -> PolicyResponse:
        portfolio = self._get_portfolio_or_404(portfolio_id)
        policy_data = self.repository.get_policy(portfolio_id) or create_default_policy(
            str(portfolio["benchmark"]),
        )
        policy = PortfolioPolicy.model_validate(policy_data)
        comparison = self._policy_comparison(portfolio_id, policy)

        return PolicyResponse(
            portfolio_id=portfolio_id,
            policy=policy,
            comparison=comparison,
            breaches=identify_policy_breaches([item.model_dump() for item in comparison]),
            warnings=validate_policy_constraints(policy.model_dump()),
        )

    def update_policy(
        self,
        portfolio_id: str,
        policy: PortfolioPolicy,
    ) -> PolicyResponse:
        self._get_portfolio_or_404(portfolio_id)
        self.repository.update_policy(portfolio_id, policy.model_dump())
        return self.get_policy(portfolio_id)

    def get_target_allocation(self, portfolio_id: str) -> TargetAllocationResponse:
        policy_response = self.get_policy(portfolio_id)
        return TargetAllocationResponse(
            portfolio_id=portfolio_id,
            items=policy_response.comparison,
            rebalance_needed=any(
                item.status != "Within tolerance" for item in policy_response.comparison
            ),
        )

    def update_target_allocation(
        self,
        portfolio_id: str,
        target_allocation: list[TargetAllocation],
    ) -> TargetAllocationResponse:
        policy_response = self.get_policy(portfolio_id)
        policy = policy_response.policy
        policy.target_allocation = target_allocation
        self.repository.update_policy(portfolio_id, policy.model_dump())
        return self.get_target_allocation(portfolio_id)

    def get_rebalancing_preview(self, portfolio_id: str) -> RebalancingPreviewResponse:
        summary = self.get_summary(portfolio_id)
        positions = self._decorated_positions(portfolio_id)
        target_weights = self._default_symbol_target_weights(positions, summary.cash_weight)
        items = create_rebalance_preview(
            positions,
            summary.total_market_value,
            target_weights,
        )
        value_differences = {
            str(item["name"]): float(item["value_difference"]) for item in items
        }

        return RebalancingPreviewResponse(
            portfolio_id=portfolio_id,
            turnover_estimate=estimate_turnover(
                value_differences,
                summary.total_market_value,
            ),
            items=items,
            notes=[
                "Preview only. No trades are executed.",
                "Targets are equal-weight demo targets across current invested holdings.",
            ],
        )

    def get_performance_measurement(
        self,
        portfolio_id: str,
    ) -> PerformanceMeasurementResponse:
        summary = self.get_summary(portfolio_id)
        positions = self._decorated_positions(portfolio_id)
        beginning_value = sum(float(position["cost_basis"]) for position in positions) + summary.cash
        ending_value = summary.total_market_value
        holding_period_return = calculate_holding_period_return(
            beginning_value,
            ending_value,
        )

        return PerformanceMeasurementResponse(
            portfolio_id=portfolio_id,
            beginning_value=beginning_value,
            ending_value=ending_value,
            external_cash_flows=0.0,
            holding_period_return=holding_period_return,
            time_weighted_return=calculate_time_weighted_return(
                [holding_period_return],
            ),
            money_weighted_return=None,
            return_contributions=[
                {
                    "symbol": str(position["symbol"]),
                    "weight": float(position["invested_weight"]),
                    "expected_return": float(position["unrealized_pnl_percent"]),
                    "return_contribution": calculate_return_contribution(
                        float(position["invested_weight"]),
                        float(position["unrealized_pnl_percent"]),
                    ),
                    "risk_contribution_placeholder": float(position["invested_weight"]),
                }
                for position in positions
            ],
            notes=[
                "Holding-period return uses cost basis as beginning value in demo mode.",
                "Money-weighted return is a placeholder until dated cash flows exist.",
            ],
        )

    def get_constraints(self, portfolio_id: str) -> ConstraintsResponse:
        self._get_portfolio_or_404(portfolio_id)
        constraints_data = self.repository.get_constraints(portfolio_id) or PortfolioConstraints().model_dump()
        constraints = PortfolioConstraints.model_validate(constraints_data)
        return ConstraintsResponse(
            portfolio_id=portfolio_id,
            constraints=constraints,
            breaches=self._constraint_breaches(portfolio_id, constraints),
        )

    def update_constraints(
        self,
        portfolio_id: str,
        constraints: PortfolioConstraints,
    ) -> ConstraintsResponse:
        self._get_portfolio_or_404(portfolio_id)
        self.repository.update_constraints(portfolio_id, constraints.model_dump())
        return self.get_constraints(portfolio_id)

    def get_diagnostics(self, portfolio_id: str) -> PortfolioDiagnosticsResponse:
        summary = self.get_summary(portfolio_id)
        diversification = self.get_diversification(portfolio_id)
        benchmark = self.get_benchmark(portfolio_id)
        policy = self.get_policy(portfolio_id)
        constraints = self.get_constraints(portfolio_id)
        target = self.get_target_allocation(portfolio_id)
        allocation_quality = classify_allocation_quality(
            summary.number_of_asset_classes,
            constraints.breaches,
        )
        diversification_quality = classify_diversification_quality(
            diversification.effective_number_of_holdings,
        )
        cash_level = classify_cash_level(summary.cash_weight)
        benchmark_alignment = classify_benchmark_alignment(benchmark.total_active_weight)
        policy_alignment = "Aligned" if not policy.breaches else "Policy review required"
        rebalancing_need = "Rebalance review needed" if target.rebalance_needed else "Within target bands"

        return PortfolioDiagnosticsResponse(
            portfolio_id=portfolio_id,
            allocation_quality=allocation_quality,
            diversification_quality=diversification_quality,
            concentration_risk=diversification.concentration_level,
            cash_level=cash_level,
            benchmark_alignment=benchmark_alignment,
            policy_alignment=policy_alignment,
            rebalancing_need=rebalancing_need,
            data_quality_limitations=[
                "DemoDataStore is in-memory and resets on backend restart.",
                "No live market data refresh or FX conversion is connected yet.",
                "Benchmark, covariance and MWR analytics are placeholders.",
            ],
            next_analytical_steps=[
                "Connect positions to persisted database tables.",
                "Use Market Data return series for realized performance and covariance.",
                "Add benchmark constituent weights for true active management analytics.",
            ],
            summary=create_portfolio_diagnostics_summary(
                allocation_quality=allocation_quality,
                diversification_quality=diversification_quality,
                concentration_level=diversification.concentration_level,
                cash_level=cash_level,
                benchmark_alignment=benchmark_alignment,
                policy_breaches=policy.breaches,
            ),
        )

    def get_cfa_concepts(self, portfolio_id: str) -> CfaConceptsResponse:
        policy = self.get_policy(portfolio_id).policy
        positions = self._decorated_positions(portfolio_id)
        risk_return = self.get_risk_return(portfolio_id)
        performance = self.get_performance_measurement(portfolio_id)
        concentration = self.get_concentration(portfolio_id)
        risk_free_rate = 0.04
        expected_market_return = 0.08
        benchmark_return = 0.06
        market_risk_premium = calculate_market_risk_premium(
            expected_market_return,
            risk_free_rate,
        )
        portfolio_beta = calculate_weighted_portfolio_beta(
            positions,
            self._demo_beta_by_symbol(positions),
        )
        required_return = calculate_capm_required_return(
            risk_free_rate,
            portfolio_beta,
            market_risk_premium,
        )
        expected_return = risk_return.expected_return
        variance = risk_return.variance or 0.0
        active_return = calculate_active_return(expected_return, benchmark_return)
        tracking_error = calculate_tracking_error([active_return, active_return * 0.8])
        behavioral_warnings = [
            detect_home_bias_placeholder(positions, home_country="United States"),
            detect_concentration_overconfidence_warning(
                concentration.largest_position_weight,
            ),
            *[
                detect_loss_aversion_placeholder(
                    float(position["unrealized_pnl_percent"]),
                )
                for position in positions
            ],
        ]
        active_behavioral_warnings = [
            warning for warning in behavioral_warnings if warning is not None
        ]
        pooled_exposure = calculate_pooled_vehicle_exposure(positions)

        return CfaConceptsResponse(
            portfolio_id=portfolio_id,
            portfolio_management_process=[
                {
                    "phase": "Planning",
                    "description": "Define IPS objectives, constraints, risk tolerance and strategic target allocation.",
                },
                {
                    "phase": "Execution",
                    "description": "Translate the policy into holdings, pooled vehicles, position sizing and rebalancing actions.",
                },
                {
                    "phase": "Feedback",
                    "description": "Monitor performance, drift, suitability, behavioral warnings and policy alignment.",
                },
            ],
            investor_profile=InvestorProfileResponse(
                investor_type=policy.investor_type,
                liability_profile=policy.liability_profile,
                liquidity_needs=policy.liquidity_needs,
                time_horizon=policy.time_horizon,
                return_objective=policy.return_objective,
                risk_objective=policy.risk_objective,
                tax_considerations=policy.tax_considerations,
                legal_regulatory_constraints=policy.legal_regulatory_constraints,
                unique_circumstances=policy.unique_circumstances,
            ),
            risk_tolerance=RiskToleranceResponse(
                ability_to_take_risk=policy.ability_to_take_risk,
                willingness_to_take_risk=policy.willingness_to_take_risk,
                overall_risk_tolerance=classify_overall_risk_tolerance(
                    policy.ability_to_take_risk,
                    policy.willingness_to_take_risk,
                ),
                conflict_detected=detect_ability_willingness_conflict(
                    policy.ability_to_take_risk,
                    policy.willingness_to_take_risk,
                ),
                summary=create_risk_tolerance_summary(
                    policy.ability_to_take_risk,
                    policy.willingness_to_take_risk,
                ),
            ),
            utility=UtilityResponse(
                expected_return=expected_return,
                variance=variance,
                risk_aversion_coefficient=policy.risk_aversion_coefficient,
                risk_aversion_classification=classify_risk_aversion(
                    policy.risk_aversion_coefficient,
                ),
                utility_score=calculate_utility_score(
                    expected_return,
                    variance,
                    policy.risk_aversion_coefficient,
                ),
            ),
            capm=CapmResponse(
                risk_free_rate=risk_free_rate,
                expected_market_return=expected_market_return,
                market_risk_premium=market_risk_premium,
                portfolio_beta=portfolio_beta,
                capm_required_return=required_return,
                expected_return_gap=expected_return - required_return,
                interpretation=compare_expected_return_to_required_return(
                    expected_return,
                    required_return,
                ),
            ),
            risk_adjusted_performance=RiskAdjustedPerformanceResponse(
                portfolio_return=performance.holding_period_return,
                benchmark_return=benchmark_return,
                risk_free_rate=risk_free_rate,
                sharpe_ratio=calculate_sharpe_ratio(
                    expected_return,
                    risk_free_rate,
                    risk_return.standard_deviation,
                ),
                treynor_ratio=calculate_treynor_ratio(
                    expected_return,
                    risk_free_rate,
                    portfolio_beta,
                ),
                jensen_alpha=calculate_jensen_alpha(expected_return, required_return),
                active_return=active_return,
                tracking_error=tracking_error,
                information_ratio=calculate_information_ratio(
                    active_return,
                    tracking_error,
                ),
                notes=[
                    "Sharpe, Treynor, alpha and information ratio use deterministic demo inputs.",
                    "Tracking error is illustrative until return series and benchmark history are connected.",
                ],
            ),
            behavioral_biases=BehavioralBiasResponse(
                warnings=active_behavioral_warnings,
                summary=create_behavioral_bias_summary(active_behavioral_warnings),
            ),
            pooled_vehicle_exposure=PooledVehicleExposureResponse(
                etf_exposure=calculate_etf_exposure(positions),
                single_stock_exposure=calculate_single_stock_exposure(positions),
                pooled_vehicle_exposure=pooled_exposure,
                usage_classification=classify_pooled_vehicle_usage(pooled_exposure),
            ),
            efficient_frontier=EfficientFrontierResponse(
                points=create_efficient_frontier_demo_points(
                    expected_return,
                    risk_return.standard_deviation,
                ),
                status="Illustrative three-point frontier until optimizer inputs are available.",
            ),
        )

    def _get_portfolio_or_404(self, portfolio_id: str) -> dict[str, object]:
        portfolio = self.repository.get_portfolio(portfolio_id)
        if portfolio is None:
            raise HTTPException(status_code=404, detail="Portfolio not found.")

        return portfolio

    def _decorated_positions(self, portfolio_id: str) -> list[dict[str, object]]:
        portfolio = self._get_portfolio_or_404(portfolio_id)
        positions = self.position_repository.list_positions(portfolio_id)
        market_values = [
            calculate_position_market_value(
                float(position["quantity"]),
                float(position["current_price"]),
            )
            for position in positions
        ]
        total_market_value = calculate_portfolio_market_value(
            market_values,
            float(portfolio["cash"]),
        )
        invested_value = calculate_invested_value(market_values)

        return [
            {
                **position,
                "name": str(position.get("name") or position.get("asset_name")),
                "market_value": market_value,
                "weight": calculate_portfolio_weight(market_value, total_market_value),
                "portfolio_weight": calculate_portfolio_weight(
                    market_value,
                    total_market_value,
                ),
                "invested_weight": calculate_invested_weight(
                    market_value,
                    invested_value,
                ),
                "cost_basis": calculate_position_cost_basis(
                    float(position["quantity"]),
                    float(position["average_price"]),
                ),
                "unrealized_pnl": calculate_position_unrealized_pnl(
                    float(position["quantity"]),
                    float(position["average_price"]),
                    float(position["current_price"]),
                ),
                "unrealized_pnl_percent": calculate_position_unrealized_pnl_percent(
                    float(position["quantity"]),
                    float(position["average_price"]),
                    float(position["current_price"]),
                ),
            }
            for position, market_value in zip(positions, market_values)
        ]

    def _concentration_metrics(
        self,
        positions: list[dict[str, object]],
    ) -> dict[str, object]:
        weights = [float(position["invested_weight"]) for position in positions]
        largest_weight = calculate_largest_position_weight(weights)
        top_5_weight = calculate_top_n_holdings_weight(weights, 5)
        return {
            "largest_position_weight": largest_weight,
            "top_3_holdings_weight": calculate_top_n_holdings_weight(weights, 3),
            "top_5_holdings_weight": top_5_weight,
            "number_of_positions": len(positions),
            "hhi_concentration": calculate_hhi_concentration(weights),
            "effective_number_of_holdings": calculate_effective_number_of_holdings(
                weights,
            ),
            "diversification_score": calculate_diversification_score(weights),
            "concentration_level": classify_concentration_level(
                largest_weight,
                top_5_weight,
            ),
            "warnings": identify_concentration_warnings(positions),
        }

    def _largest_position_symbol(
        self,
        positions: list[dict[str, object]],
    ) -> str | None:
        if not positions:
            return None

        largest_position = max(
            positions,
            key=lambda position: float(position["market_value"]),
        )
        return str(largest_position["symbol"])

    def _allocation_weight_map(
        self,
        allocation: list[dict[str, float | str]],
    ) -> dict[str, float]:
        return {str(item["name"]): float(item["weight"]) for item in allocation}

    def _current_asset_type_allocation_with_cash(
        self,
        portfolio_id: str,
    ) -> dict[str, float]:
        summary = self.get_summary(portfolio_id)
        positions = self._decorated_positions(portfolio_id)
        allocation: dict[str, float] = {"cash": summary.cash_weight}
        for position in positions:
            asset_type = str(position["asset_type"])
            allocation[asset_type] = allocation.get(asset_type, 0.0) + float(
                position["portfolio_weight"],
            )
        return allocation

    def _policy_comparison(
        self,
        portfolio_id: str,
        policy: PortfolioPolicy,
    ) -> list[PolicyComparisonItem]:
        current_allocation = self._current_asset_type_allocation_with_cash(portfolio_id)
        comparison = compare_allocation_to_policy(
            current_allocation,
            [item.model_dump() for item in policy.target_allocation],
        )
        return [PolicyComparisonItem.model_validate(item) for item in comparison]

    def _constraint_breaches(
        self,
        portfolio_id: str,
        constraints: PortfolioConstraints,
    ) -> list[dict[str, object]]:
        summary = self.get_summary(portfolio_id)
        positions = self._decorated_positions(portfolio_id)
        sector_allocation = calculate_allocation_by_sector(positions)
        asset_type_allocation = calculate_allocation_by_asset_type(positions)
        currency_allocation = calculate_allocation_by_currency(positions)

        return summarize_constraint_breaches(
            check_single_position_limit(
                positions,
                constraints.max_single_position_weight,
            ),
            check_sector_limit(sector_allocation, constraints.max_sector_weight),
            check_asset_type_limit(
                asset_type_allocation,
                constraints.max_asset_type_weight,
            ),
            check_currency_limit(currency_allocation, constraints.max_currency_weight),
            check_min_cash_limit(summary.cash_weight, constraints.minimum_cash_weight),
            check_allowed_asset_types(positions, constraints.allowed_asset_types),
        )

    def _expected_return_for_asset_type(self, asset_type: str) -> float:
        return {
            "equity": 0.08,
            "etf": 0.06,
            "fixed_income": 0.035,
            "bond": 0.035,
            "cash": 0.02,
        }.get(asset_type.lower(), 0.05)

    def _volatility_for_asset_type(self, asset_type: str) -> float:
        return {
            "equity": 0.22,
            "etf": 0.16,
            "fixed_income": 0.06,
            "bond": 0.06,
            "cash": 0.01,
        }.get(asset_type.lower(), 0.15)

    def _demo_covariance_matrix(self, volatilities: list[float]) -> list[list[float]]:
        correlation = 0.35
        matrix: list[list[float]] = []
        for row_index, row_volatility in enumerate(volatilities):
            row = []
            for column_index, column_volatility in enumerate(volatilities):
                if row_index == column_index:
                    row.append(row_volatility * row_volatility)
                else:
                    row.append(row_volatility * column_volatility * correlation)
            matrix.append(row)
        return matrix

    def _risk_return_profile(
        self,
        expected_return: float,
        standard_deviation: float,
    ) -> str:
        if standard_deviation >= 0.18 and expected_return >= 0.07:
            return "Growth-oriented"
        if standard_deviation <= 0.10:
            return "Defensive"
        return "Balanced"

    def _default_symbol_target_weights(
        self,
        positions: list[dict[str, object]],
        cash_weight: float,
    ) -> dict[str, float]:
        if not positions:
            return {}

        invested_target = max(0.0, 1.0 - cash_weight)
        equal_weight = invested_target / len(positions)
        return {str(position["symbol"]): equal_weight for position in positions}

    def _demo_beta_by_symbol(
        self,
        positions: list[dict[str, object]],
    ) -> dict[str, float]:
        beta_by_asset_type = {
            "equity": 1.05,
            "etf": 0.95,
            "fixed_income": 0.20,
            "bond": 0.20,
            "cash": 0.0,
        }
        known_betas = {
            "AAPL": 1.20,
            "MSFT": 1.05,
            "NVDA": 1.60,
            "SPY": 1.00,
            "QQQ": 1.15,
            "BND": 0.20,
        }
        return {
            str(position["symbol"]).upper(): known_betas.get(
                str(position["symbol"]).upper(),
                beta_by_asset_type.get(str(position["asset_type"]).lower(), 1.0),
            )
            for position in positions
        }


class PositionService:
    def __init__(
        self,
        repository: PositionRepository,
        portfolio_repository: PortfolioRepository,
    ) -> None:
        self.repository = repository
        self.portfolio_repository = portfolio_repository

    def list_positions(self, portfolio_id: str) -> PositionListResponse:
        self._get_portfolio_or_404(portfolio_id)
        return PositionListResponse(
            portfolio_id=portfolio_id,
            items=self._decorated_positions(portfolio_id),
        )

    def create_position(
        self,
        portfolio_id: str,
        payload: PositionCreate,
    ) -> PositionRead:
        self._get_portfolio_or_404(portfolio_id)
        validate_position_input(
            symbol=payload.symbol,
            asset_type=payload.asset_type,
            currency=payload.currency,
            quantity=payload.quantity,
            current_price=payload.current_price,
            average_price=payload.average_price,
        )
        created_position = self.repository.create_position(
            portfolio_id,
            payload.model_dump(),
        )
        positions = self._decorated_positions(portfolio_id)
        return next(
            position
            for position in positions
            if position.id == created_position["id"]
        )

    def update_position(
        self,
        portfolio_id: str,
        position_id: str,
        payload: PositionUpdate,
    ) -> PositionRead:
        self._get_portfolio_or_404(portfolio_id)
        existing_position = self.repository.get_position(portfolio_id, position_id)
        if existing_position is None:
            raise HTTPException(status_code=404, detail="Position not found.")
        updated_payload = {**existing_position, **payload.model_dump(exclude_none=True)}
        validate_position_input(
            symbol=str(updated_payload["symbol"]),
            asset_type=str(updated_payload["asset_type"]),
            currency=str(updated_payload["currency"]),
            quantity=float(updated_payload["quantity"]),
            current_price=float(updated_payload["current_price"]),
            average_price=float(updated_payload["average_price"]),
        )
        position = self.repository.update_position(
            portfolio_id,
            position_id,
            payload.model_dump(exclude_none=True),
        )
        if position is None:
            raise HTTPException(status_code=404, detail="Position not found.")

        positions = self._decorated_positions(portfolio_id)
        return next(position for position in positions if position.id == position_id)

    def delete_position(self, portfolio_id: str, position_id: str) -> DeleteResponse:
        self._get_portfolio_or_404(portfolio_id)
        deleted = self.repository.delete_position(portfolio_id, position_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Position not found.")

        return DeleteResponse(status="deleted", id=position_id)

    def _get_portfolio_or_404(self, portfolio_id: str) -> dict[str, object]:
        portfolio = self.portfolio_repository.get_portfolio(portfolio_id)
        if portfolio is None:
            raise HTTPException(status_code=404, detail="Portfolio not found.")

        return portfolio

    def _decorated_positions(self, portfolio_id: str) -> list[PositionRead]:
        portfolio = self._get_portfolio_or_404(portfolio_id)
        positions = self.repository.list_positions(portfolio_id)
        market_values = [
            calculate_position_market_value(
                float(position["quantity"]),
                float(position["current_price"]),
            )
            for position in positions
        ]
        total_market_value = calculate_portfolio_market_value(
            market_values,
            float(portfolio["cash"]),
        )
        invested_value = calculate_invested_value(market_values)

        return [
            PositionRead.model_validate(
                {
                    **position,
                    "name": str(position.get("name") or position.get("asset_name")),
                    "market_value": market_value,
                    "weight": calculate_portfolio_weight(
                        market_value,
                        total_market_value,
                    ),
                    "portfolio_weight": calculate_portfolio_weight(
                        market_value,
                        total_market_value,
                    ),
                    "invested_weight": calculate_invested_weight(
                        market_value,
                        invested_value,
                    ),
                    "cost_basis": calculate_position_cost_basis(
                        float(position["quantity"]),
                        float(position["average_price"]),
                    ),
                    "unrealized_pnl": calculate_position_unrealized_pnl(
                        float(position["quantity"]),
                        float(position["average_price"]),
                        float(position["current_price"]),
                    ),
                    "unrealized_pnl_percent": calculate_position_unrealized_pnl_percent(
                        float(position["quantity"]),
                        float(position["average_price"]),
                        float(position["current_price"]),
                    ),
                },
            )
            for position, market_value in zip(positions, market_values)
        ]
