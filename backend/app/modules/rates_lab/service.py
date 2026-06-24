from fastapi import HTTPException

from app.modules.rates_lab.domain.bonds import (
    clean_price,
    price_dated_coupon_bond,
    price_dated_zero_coupon_bond,
    price_coupon_bond,
    price_zero_coupon_bond,
)
from app.modules.rates_lab.domain.cashflows import (
    generate_bond_cashflows,
    zero_coupon_cashflow,
)
from app.modules.rates_lab.domain.commentary import (
    bond_commentary,
    curve_commentary,
)
from app.modules.rates_lab.domain.convexity import (
    convexity,
    convexity_adjusted_price_impact,
)
from app.modules.rates_lab.domain.curves import (
    calculate_forward_rates,
    classify_curve_shape,
    curve_slope,
    interpolate_curve_linear,
)
from app.modules.rates_lab.domain.duration import (
    duration_price_impact,
    dv01,
    macaulay_duration,
    modified_duration,
    pvbp,
)
from app.modules.rates_lab.domain.scenarios import (
    apply_curve_scenario,
    scenario_price_impact,
)
from app.modules.rates_lab.domain.yields import (
    current_yield,
    holding_period_return,
    price_premium_discount_status,
    yield_to_maturity,
)
from app.modules.rates_lab.repository import RatesLabRepository
from app.modules.rates_lab.schemas import (
    BondPricingRequest,
    BondPricingResponse,
    DataQualityMetadata,
    DataSourceMetadata,
    DurationConvexityRequest,
    DurationConvexityResponse,
    MethodologyMetadata,
    PortfolioRatesExposureRequest,
    PortfolioRatesExposureResponse,
    RateScenarioRequest,
    RateScenarioResponse,
    RatesLabStatus,
    YieldAnalysisRequest,
    YieldAnalysisResponse,
    YieldCurveRequest,
    YieldCurveResponse,
)
from app.modules.risk_shared.schemas import RatesRiskPayload


class RatesLabService:
    def __init__(self, repository: RatesLabRepository) -> None:
        self.repository = repository

    def get_status(self) -> RatesLabStatus:
        return RatesLabStatus(
            detail=(
                "Rates Lab is ready for bond pricing, yield, duration, convexity, "
                "DV01, yield-curve and deterministic rate-scenario analytics."
            ),
            engines_available=[
                "discounted_cash_flow",
                "yield_to_maturity",
                "duration",
                "convexity",
                "dv01",
                "linear_yield_curve",
                "rate_scenarios",
                "portfolio_fixed_income_exposure",
            ],
        )

    def price_bond(self, payload: BondPricingRequest) -> BondPricingResponse:
        date_metadata: dict[str, object] = {}
        if payload.settlement_date is not None and payload.maturity_date is not None:
            if payload.bond_type == "zero_coupon":
                dirty, cashflows, date_metadata = price_dated_zero_coupon_bond(
                    payload.face_value,
                    payload.settlement_date,
                    payload.maturity_date,
                    payload.yield_to_maturity,
                    payload.coupon_frequency,
                    payload.day_count_convention,
                )
            else:
                dirty, cashflows, date_metadata = price_dated_coupon_bond(
                    payload.face_value,
                    payload.coupon_rate,
                    payload.coupon_frequency,
                    payload.settlement_date,
                    payload.maturity_date,
                    payload.yield_to_maturity,
                    payload.day_count_convention,
                )
            accrued = float(date_metadata["accrued_interest"])
        else:
            dirty, cashflows = self._price_bond_inputs(payload)
            accrued = 0.0
        clean = clean_price(dirty, accrued)
        status = price_premium_discount_status(clean, payload.face_value)
        methodology = self._bond_methodology(payload, date_metadata)
        data_quality = self._pricing_data_quality(payload)
        data_source = self._manual_data_source()
        return BondPricingResponse(
            bond_type=payload.bond_type,
            clean_price=clean,
            dirty_price=dirty,
            accrued_interest=accrued,
            present_value_of_cashflows=dirty,
            price_status=status,
            cash_flow_schedule=cashflows,
            yield_assumptions={
                "yield_to_maturity": payload.yield_to_maturity,
                "coupon_rate": payload.coupon_rate,
                "coupon_frequency": payload.coupon_frequency,
                "price_yield_relationship": "inverse",
            },
            methodology=methodology,
            data_quality=data_quality,
            data_source=data_source,
            rates_risk_payload=RatesRiskPayload(
                clean_price=clean,
                dirty_price=dirty,
                accrued_interest=accrued,
                ytm=payload.yield_to_maturity,
                methodology=methodology.method,
                warnings=[*data_quality.warnings, *data_source.warnings],
            ),
            athena_commentary=bond_commentary(
                status,
                payload.coupon_rate,
                payload.yield_to_maturity,
                language=payload.language,
            ),
        )

    def analyze_yield(
        self,
        payload: YieldAnalysisRequest,
    ) -> YieldAnalysisResponse:
        result = yield_to_maturity(
            payload.price,
            payload.face_value,
            payload.coupon_rate,
            payload.coupon_frequency,
            payload.years_to_maturity,
        )
        market_price = payload.current_market_price or payload.price
        current = current_yield(
            payload.face_value,
            payload.coupon_rate,
            market_price,
        )
        hpr = None
        if payload.beginning_price is not None and payload.ending_price is not None:
            hpr = holding_period_return(
                payload.beginning_price,
                payload.ending_price,
                payload.coupon_received or 0.0,
            )
        status = price_premium_discount_status(payload.price, payload.face_value)
        solved_yield = (
            float(result["yield_to_maturity"])
            if bool(result["converged"])
            else None
        )
        interpretations = (
            {
                "discount": "Un prix sous le pair implique generalement un rendement superieur au coupon.",
                "premium": "Un prix au-dessus du pair implique generalement un rendement inferieur au coupon.",
                "par": "Un prix pres du pair implique generalement un rendement proche du coupon.",
            }
            if payload.language == "fr"
            else {
                "discount": "Price below par generally implies YTM above the coupon rate.",
                "premium": "Price above par generally implies YTM below the coupon rate.",
                "par": "Price near par generally implies YTM near the coupon rate.",
            }
        )
        interpretation = interpretations[status]
        return YieldAnalysisResponse(
            yield_to_maturity=solved_yield,
            current_yield=current,
            holding_period_return=hpr,
            convergence_status="converged" if result["converged"] else "not_converged",
            iterations=int(result["iterations"]),
            pricing_error=float(result["pricing_error"]),
            price_status=status,
            interpretation=interpretation,
            methodology=MethodologyMetadata(
                method="numerical_solver",
                assumptions=["Constant yield across all cash flows"],
                limitations=["YTM assumes coupons can be reinvested at the same yield"],
                details={
                    "solver": "bisection",
                    "convergence_status": "converged" if result["converged"] else "not_converged",
                    "iterations": int(result["iterations"]),
                    "warning": str(result["warning"]),
                },
            ),
            data_quality=DataQualityMetadata(
                missing_fields=(
                    []
                    if hpr is not None
                    else ["beginning_price", "ending_price", "coupon_received"]
                ),
                warnings=([str(result["warning"])] if result["warning"] else []),
                limitations=["Holding-period return requires optional holding data"],
            ),
            data_source=self._manual_data_source(),
            athena_commentary=bond_commentary(
                status,
                payload.coupon_rate,
                solved_yield if solved_yield is not None else 0.0,
                language=payload.language,
            ),
        )

    def analyze_duration_convexity(
        self,
        payload: DurationConvexityRequest,
    ) -> DurationConvexityResponse:
        price, cashflows = self._price_bond_inputs(payload)
        analysis_price = payload.price or price
        macaulay = macaulay_duration(
            cashflows,
            payload.yield_to_maturity,
            payload.coupon_frequency,
        )
        modified = modified_duration(
            macaulay,
            payload.yield_to_maturity,
            payload.coupon_frequency,
        )
        convexity_value = convexity(
            cashflows,
            payload.yield_to_maturity,
            payload.coupon_frequency,
        )
        dv01_value = dv01(analysis_price, modified)
        pvbp_value = pvbp(analysis_price, modified)
        shock = payload.rate_shock_bps / 10_000
        duration_change = duration_price_impact(analysis_price, modified, shock)
        convexity_change = convexity_adjusted_price_impact(
            analysis_price,
            modified,
            convexity_value,
            shock,
        )
        risk_level = "high" if modified >= 8 else "moderate" if modified >= 4 else "low"
        risk_interpretation = (
            {
                "high": "Sensibilite elevee aux taux d'interet.",
                "moderate": "Sensibilite moderee aux taux d'interet.",
                "low": "Sensibilite faible aux taux d'interet.",
            }[risk_level]
            if payload.language == "fr"
            else f"{risk_level.title()} interest-rate sensitivity."
        )
        return DurationConvexityResponse(
            price=analysis_price,
            macaulay_duration=macaulay,
            modified_duration=modified,
            convexity=convexity_value,
            dv01=dv01_value,
            pvbp=pvbp_value,
            rate_shock_bps=payload.rate_shock_bps,
            estimated_price_change_duration=duration_change,
            estimated_price_change_duration_convexity=convexity_change,
            estimated_stressed_price_duration=analysis_price + duration_change,
            estimated_stressed_price_duration_convexity=analysis_price + convexity_change,
            risk_interpretation=risk_interpretation,
            methodology=MethodologyMetadata(
                method="present_value_weighted_cashflows",
                assumptions=["Parallel yield change", "Fixed cash flows"],
                limitations=["Duration is linear; convexity remains an approximation"],
                details={
                    "macaulay_method": "present_value_weighted_cashflows",
                    "modified_duration_formula": "macaulay_duration / (1 + yield / frequency)",
                    "convexity_method": "cashflow_convexity_approximation",
                    "dv01_method": "modified_duration_price_sensitivity",
                    "basis_point_size": 0.0001,
                },
            ),
            data_quality=DataQualityMetadata(
                limitations=["Parallel-shift duration and convexity approximation"],
            ),
            risk_monitor_payload={
                "module": "rates_lab",
                "price": analysis_price,
                "modified_duration": modified,
                "convexity": convexity_value,
                "dv01": dv01_value,
                "shock_bps": payload.rate_shock_bps,
                "estimated_loss": min(0.0, convexity_change),
            },
            rates_risk_payload=RatesRiskPayload(
                clean_price=analysis_price,
                dirty_price=analysis_price,
                accrued_interest=0.0,
                ytm=payload.yield_to_maturity,
                macaulay_duration=macaulay,
                modified_duration=modified,
                convexity=convexity_value,
                dv01=dv01_value,
                pvbp=pvbp_value,
                rate_shock_bps=payload.rate_shock_bps,
                estimated_rate_shock_loss=min(0.0, convexity_change),
                methodology="present_value_weighted_cashflows",
                warnings=[],
            ),
            data_source=self._manual_data_source(),
            athena_commentary=bond_commentary(
                price_premium_discount_status(analysis_price, payload.face_value),
                payload.coupon_rate,
                payload.yield_to_maturity,
                modified,
                payload.rate_shock_bps,
                payload.language,
            ),
        )

    def analyze_yield_curve(self, payload: YieldCurveRequest) -> YieldCurveResponse:
        supplied_points = [point.model_dump() for point in payload.curve_points]
        base_curve = supplied_points or self.repository.get_demo_curve()
        requested = payload.requested_maturities or [
            0.25,
            0.5,
            1,
            2,
            3,
            5,
            7,
            10,
            20,
            30,
        ]
        interpolated = interpolate_curve_linear(base_curve, requested)
        slope = curve_slope(interpolated)
        shape = classify_curve_shape(interpolated)
        source = "manual_input" if supplied_points else "demo_curve"
        commentary = curve_commentary(shape, slope, payload.language)
        return YieldCurveResponse(
            input_curve=base_curve,
            interpolated_curve=interpolated,
            spot_rates=interpolated,
            forward_rates=calculate_forward_rates(interpolated),
            curve_slope=slope,
            curve_slope_bps=slope * 10_000,
            curve_shape=shape,
            curve_interpretation=str(commentary["summary"]),
            methodology=MethodologyMetadata(
                method="linear_interpolation_demo",
                assumptions=["Annual compounding for implied forward rates"],
                limitations=[
                    "Flat endpoint extrapolation",
                    "Par rates are treated as spot-rate proxies in this educational beta",
                ],
                details={"curve_type": payload.curve_type, "source": source},
            ),
            data_quality=DataQualityMetadata(
                fallback_used=not bool(supplied_points),
                demo_curve_used=not bool(supplied_points),
                warnings=(
                    ["Deterministic demo curve used; live Treasury data is not connected."]
                    if not supplied_points
                    else []
                ),
                limitations=["Par rates are treated as spot-rate proxies in this beta"],
            ),
            data_source=self._curve_data_source(bool(supplied_points)),
            athena_commentary=commentary,
        )

    def analyze_rate_scenario(
        self,
        payload: RateScenarioRequest,
    ) -> RateScenarioResponse:
        price, cashflows = self._price_bond_inputs(payload)
        macaulay = macaulay_duration(
            cashflows,
            payload.yield_to_maturity,
            payload.coupon_frequency,
        )
        modified = modified_duration(
            macaulay,
            payload.yield_to_maturity,
            payload.coupon_frequency,
        )
        convexity_value = convexity(
            cashflows,
            payload.yield_to_maturity,
            payload.coupon_frequency,
        )
        supplied_curve = [point.model_dump() for point in payload.curve_points]
        base_curve = supplied_curve or self.repository.get_demo_curve()
        stressed_curve = apply_curve_scenario(
            base_curve,
            payload.scenario_type,
            payload.shock_bps,
        )
        result = scenario_price_impact(
            payload.face_value,
            payload.coupon_rate if payload.bond_type == "coupon_bond" else 0.0,
            payload.coupon_frequency,
            payload.years_to_maturity,
            payload.yield_to_maturity,
            modified,
            convexity_value,
            payload.scenario_type,
            payload.shock_bps,
            base_curve,
            stressed_curve,
        )
        change = float(result["price_change"])
        scenario_dv01 = dv01(float(result["base_price"]), modified)
        scenario_pvbp = pvbp(float(result["base_price"]), modified)
        if payload.language == "fr":
            interpretation = (
                "Le choc selectionne reduit le prix de l'obligation."
                if change < 0
                else "Le choc selectionne augmente le prix de l'obligation."
            )
            risk_warning = (
                "Les scenarios sont des estimations deterministes, pas des previsions. "
                "Les chocs non paralleles utilisent des ponderations simplifiees par maturite."
            )
        else:
            interpretation = (
                "The selected shock lowers the bond price."
                if change < 0
                else "The selected shock raises the bond price."
            )
            risk_warning = (
                "Scenario results are deterministic estimates, not forecasts. "
                "Non-parallel shifts use simplified maturity weights."
            )
        return RateScenarioResponse(
            scenario_type=payload.scenario_type,
            shock_bps=payload.shock_bps,
            base_price=float(result["base_price"]),
            stressed_price=float(result["stressed_price"]),
            price_change=change,
            percent_change=float(result["percent_change"]),
            base_yield_at_maturity=float(result["base_yield_at_maturity"]),
            shocked_yield_at_maturity=float(result["shocked_yield_at_maturity"]),
            effective_shock_bps=float(result["effective_shock_bps"]),
            duration_estimate=float(result["duration_estimate"]),
            convexity_adjusted_estimate=float(result["convexity_adjusted_estimate"]),
            dv01_impact=float(result["dv01_impact"]),
            base_curve=base_curve,
            stressed_curve=stressed_curve,
            scenario_interpretation=interpretation,
            risk_warning=risk_warning,
            methodology=MethodologyMetadata(
                method="deterministic_rate_shock",
                assumptions=["Fixed cash flows", "Immediate yield shock"],
                limitations=["No credit-spread or optionality model"],
                details={
                    "scenario_type": payload.scenario_type,
                    "shock_bps": payload.shock_bps,
                    "effective_shock_bps": result["effective_shock_bps"],
                    "base_yield_at_maturity": result["base_yield_at_maturity"],
                    "shocked_yield_at_maturity": result["shocked_yield_at_maturity"],
                    "shocked_curve": stressed_curve,
                },
            ),
            data_quality=DataQualityMetadata(
                fallback_used=not bool(supplied_curve),
                demo_curve_used=not bool(supplied_curve),
                warnings=[risk_warning],
                limitations=["No credit-spread or embedded-option scenario model"],
            ),
            stress_testing_payload={
                "module": "rates_lab",
                "scenario": payload.scenario_type,
                "shock_bps": payload.shock_bps,
                "price_change": change,
                "percent_change": result["percent_change"],
                "status": "ready_for_future_stress_testing",
            },
            rates_risk_payload=RatesRiskPayload(
                clean_price=float(result["base_price"]),
                dirty_price=float(result["base_price"]),
                accrued_interest=0.0,
                ytm=float(result["base_yield_at_maturity"]),
                macaulay_duration=macaulay,
                modified_duration=modified,
                convexity=convexity_value,
                dv01=scenario_dv01,
                pvbp=scenario_pvbp,
                curve_scenario_impact=change,
                rate_shock_bps=float(result["effective_shock_bps"]),
                estimated_rate_shock_loss=min(0.0, change),
                methodology="deterministic_rate_shock",
                warnings=[risk_warning],
            ),
            data_source=self._curve_data_source(bool(supplied_curve)),
        )

    def analyze_portfolio_exposure(
        self,
        payload: PortfolioRatesExposureRequest,
    ) -> PortfolioRatesExposureResponse:
        portfolio = self.repository.get_portfolio(payload.portfolio_id)
        if portfolio is None:
            raise HTTPException(status_code=404, detail="Portfolio not found.")
        positions = self.repository.list_positions(payload.portfolio_id)
        holdings = []
        warnings = []
        total_market_value = float(portfolio.get("cash", 0.0))
        for position in positions:
            market_value = float(position["quantity"]) * float(position["current_price"])
            total_market_value += market_value
            if not self._is_fixed_income(position):
                continue
            duration_value = self.repository.get_duration_metadata(str(position["symbol"]))
            warning = None
            if duration_value is None:
                warning = (
                    f"{position['symbol']}: bond metadata or ETF duration input is required."
                )
                warnings.append(warning)
            holdings.append(
                {
                    "symbol": str(position["symbol"]),
                    "name": str(position.get("asset_name") or position["symbol"]),
                    "asset_type": str(position["asset_type"]),
                    "market_value": market_value,
                    "weight": 0.0,
                    "estimated_duration": duration_value,
                    "estimated_dv01": (
                        market_value * duration_value * 0.0001
                        if duration_value is not None
                        else None
                    ),
                    "metadata_source": (
                        "demo_etf_duration"
                        if duration_value is not None
                        else "requires_bond_metadata"
                    ),
                    "warning": warning,
                }
            )
        fixed_income_value = sum(item["market_value"] for item in holdings)
        for item in holdings:
            item["weight"] = item["market_value"] / max(total_market_value, 1.0)
        covered = [item for item in holdings if item["estimated_duration"] is not None]
        covered_value = sum(item["market_value"] for item in covered)
        weighted_duration = (
            sum(item["market_value"] * item["estimated_duration"] for item in covered)
            / covered_value
            if covered_value > 0
            else None
        )
        portfolio_dv01 = (
            sum(item["estimated_dv01"] for item in covered)
            if covered
            else None
        )
        shock_loss = (
            -portfolio_dv01 * payload.shock_bps
            if portfolio_dv01 is not None
            else None
        )
        if not holdings:
            warnings.append("No fixed-income or bond-like holdings were identified.")
        return PortfolioRatesExposureResponse(
            portfolio_id=payload.portfolio_id,
            portfolio_name=str(portfolio["name"]),
            fixed_income_holdings=holdings,
            fixed_income_market_value=fixed_income_value,
            fixed_income_allocation=fixed_income_value / max(total_market_value, 1.0),
            weighted_average_duration=weighted_duration,
            estimated_portfolio_dv01=portfolio_dv01,
            estimated_rate_shock_loss=shock_loss,
            shock_bps=payload.shock_bps,
            missing_data_warnings=warnings,
            risk_monitor_payload={
                "module": "rates_lab",
                "portfolio_id": payload.portfolio_id,
                "fixed_income_market_value": fixed_income_value,
                "weighted_average_duration": weighted_duration,
                "portfolio_dv01": portfolio_dv01,
                "shock_bps": payload.shock_bps,
                "estimated_loss": shock_loss,
                "status": "risk_monitor_ready" if portfolio_dv01 is not None else "incomplete_metadata",
            },
            rates_risk_payload=RatesRiskPayload(
                portfolio_id=payload.portfolio_id,
                clean_price=None,
                dirty_price=None,
                accrued_interest=None,
                macaulay_duration=weighted_duration,
                modified_duration=weighted_duration,
                dv01=portfolio_dv01,
                pvbp=portfolio_dv01,
                rate_shock_bps=payload.shock_bps,
                fixed_income_market_value=fixed_income_value,
                fixed_income_allocation=fixed_income_value / max(total_market_value, 1.0),
                estimated_rate_shock_loss=shock_loss,
                methodology="duration_weighted_portfolio_exposure",
                warnings=warnings,
            ),
            methodology=MethodologyMetadata(
                method="duration_weighted_portfolio_exposure",
                assumptions=["ETF effective duration is approximated from demo metadata"],
                limitations=["Requires security-level bond or ETF duration metadata"],
                details={
                    "covered_market_value": covered_value,
                    "fixed_income_market_value": fixed_income_value,
                    "metadata_coverage_ratio": (
                        covered_value / fixed_income_value if fixed_income_value > 0 else 0.0
                    ),
                },
            ),
            data_quality=DataQualityMetadata(
                missing_fields=warnings,
                fallback_used=True,
                demo_curve_used=True,
                warnings=warnings,
                limitations=["ETF effective duration uses deterministic demo metadata"],
            ),
            data_source=DataSourceMetadata(
                rate_source="demo_curve",
                curve_source="demo_curve",
                portfolio_source="portfolio_builder",
                fallback_used=True,
                badges=["Portfolio Builder", "Demo Duration", "Risk Monitor Ready"],
                warnings=warnings,
            ),
        )

    def demo(self) -> BondPricingResponse:
        return self.price_bond(BondPricingRequest())

    def _price_bond_inputs(self, payload: object) -> tuple[float, list[dict[str, object]]]:
        bond_type = str(getattr(payload, "bond_type"))
        face_value = float(getattr(payload, "face_value"))
        years = float(getattr(payload, "years_to_maturity"))
        ytm = float(getattr(payload, "yield_to_maturity"))
        frequency = str(getattr(payload, "coupon_frequency"))
        if bond_type == "zero_coupon":
            return price_zero_coupon_bond(face_value, years, ytm, frequency)
        return price_coupon_bond(
            face_value,
            float(getattr(payload, "coupon_rate")),
            frequency,
            years,
            ytm,
        )

    def _bond_methodology(
        self,
        payload: BondPricingRequest,
        date_metadata: dict[str, object] | None = None,
    ) -> MethodologyMetadata:
        dated = payload.settlement_date is not None and payload.maturity_date is not None
        metadata = date_metadata or {}
        return MethodologyMetadata(
            method="discounted_cash_flow",
            assumptions=["Fixed coupons", "Constant yield", "No default"],
            limitations=[
                "No embedded-option or credit-spread model",
                *([] if dated else ["Simplified pricing uses a year-based cash-flow schedule"]),
            ],
            details={
                "pricing_mode": "dated" if dated else "simplified",
                "coupon_frequency": payload.coupon_frequency,
                "compounding_frequency": payload.coupon_frequency,
                "day_count_convention": payload.day_count_convention,
                "settlement_date": payload.settlement_date,
                "maturity_date": payload.maturity_date,
                "previous_coupon_date": metadata.get("previous_coupon_date"),
                "next_coupon_date": metadata.get("next_coupon_date"),
                "accrued_days": metadata.get("accrued_days", 0),
                "coupon_period_days": metadata.get("coupon_period_days", 0),
                "accrued_interest": metadata.get("accrued_interest", 0.0),
                "clean_dirty_method": "clean_price_equals_dirty_price_minus_accrued_interest",
            },
        )

    def _manual_data_source(self) -> DataSourceMetadata:
        return DataSourceMetadata(
            rate_source="manual_input",
            curve_source="not_required",
            portfolio_source="not_required",
            fallback_used=False,
            badges=["Manual Input", "CFA Level 1"],
            warnings=[],
        )

    def _pricing_data_quality(
        self,
        payload: BondPricingRequest,
    ) -> DataQualityMetadata:
        dated = payload.settlement_date is not None and payload.maturity_date is not None
        return DataQualityMetadata(
            simplified_pricing_used=not dated,
            warnings=(
                []
                if dated
                else ["Simplified year-based pricing is used because dates were not supplied."]
            ),
            limitations=["No credit spread, default or embedded-option model"],
        )

    def _curve_data_source(self, manual: bool) -> DataSourceMetadata:
        return DataSourceMetadata(
            rate_source="manual_input" if manual else "demo_curve",
            curve_source="manual_input" if manual else "demo_curve",
            portfolio_source="not_required",
            fallback_used=not manual,
            badges=["Manual Input" if manual else "Demo Curve", "Requires Market Data"],
            warnings=(
                []
                if manual
                else ["Deterministic demo curve used; live Treasury data is not connected."]
            ),
        )

    @staticmethod
    def _is_fixed_income(position: dict[str, object]) -> bool:
        asset_type = str(position.get("asset_type", "")).lower()
        sector = str(position.get("sector", "")).lower()
        symbol = str(position.get("symbol", "")).upper()
        return (
            asset_type in {"bond", "fixed_income", "fixed income"}
            or "fixed income" in sector
            or symbol in {"BND", "AGG", "IEF", "TLT", "LQD", "HYG"}
        )
