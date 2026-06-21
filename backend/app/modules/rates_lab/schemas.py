from datetime import UTC, date, datetime
from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field, model_validator


BondType = Literal["coupon_bond", "zero_coupon"]
CouponFrequency = Literal["annual", "semiannual", "quarterly", "monthly"]
DayCountConvention = Literal["actual_actual", "30_360"]
ScenarioType = Literal[
    "parallel_up",
    "parallel_down",
    "steepener",
    "flattener",
    "short_rate_up",
    "long_rate_up",
    "short_rate_down",
    "long_rate_down",
]
Language = Literal["en", "fr"]
PositiveMaturity = Annotated[float, Field(gt=0, le=100, allow_inf_nan=False)]
FiniteRate = Annotated[float, Field(gt=-1, le=10, allow_inf_nan=False)]


class RatesLabStatus(BaseModel):
    status: str = "ready"
    module: str = "rates-lab"
    detail: str
    engines_available: list[str]


class CashFlow(BaseModel):
    period: int
    time_years: float
    coupon: float
    principal: float
    total_cash_flow: float
    frequency: int
    accrual_fraction: float = 1.0
    payment_date: date | None = None
    discount_factor: float
    present_value: float


class CurvePoint(BaseModel):
    maturity: PositiveMaturity
    rate: FiniteRate


class ForwardRatePoint(BaseModel):
    start_maturity: float
    end_maturity: float
    forward_rate: float


class MethodologyMetadata(BaseModel):
    method: str
    assumptions: list[str]
    limitations: list[str]
    details: dict[str, Any] = Field(default_factory=dict)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class DataQualityMetadata(BaseModel):
    missing_fields: list[str] = Field(default_factory=list)
    fallback_used: bool = False
    demo_curve_used: bool = False
    simplified_pricing_used: bool = False
    dated_pricing_available: bool = True
    warnings: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class DataSourceMetadata(BaseModel):
    rate_source: str
    curve_source: str
    portfolio_source: str
    fallback_used: bool
    badges: list[str]
    warnings: list[str]


class AthenaRatesCommentary(BaseModel):
    summary: str
    key_points: list[str]
    cfa_notes: list[str]
    not_investment_advice: bool
    input_relationship: dict[str, float] | None = None


class BondInputs(BaseModel):
    bond_type: BondType = "coupon_bond"
    face_value: float = Field(default=1000, gt=0, allow_inf_nan=False)
    coupon_rate: float = Field(default=0.05, ge=0, le=10, allow_inf_nan=False)
    coupon_frequency: CouponFrequency = "semiannual"
    years_to_maturity: float = Field(default=5, gt=0, le=100, allow_inf_nan=False)
    yield_to_maturity: float = Field(
        default=0.045,
        gt=-0.99,
        le=10,
        allow_inf_nan=False,
    )
    language: Language = "en"

    @model_validator(mode="after")
    def validate_periodic_yield(self) -> "BondInputs":
        frequency = {
            "annual": 1,
            "semiannual": 2,
            "quarterly": 4,
            "monthly": 12,
        }[self.coupon_frequency]
        if 1 + self.yield_to_maturity / frequency <= 0:
            raise ValueError("Yield per period must be greater than -100 percent.")
        return self


class BondPricingRequest(BondInputs):
    settlement_date: date | None = None
    maturity_date: date | None = None
    day_count_convention: DayCountConvention = "actual_actual"
    clean_or_dirty: Literal["clean", "dirty"] = "clean"

    @model_validator(mode="after")
    def validate_dates(self) -> "BondPricingRequest":
        if (
            self.settlement_date is not None
            and self.maturity_date is not None
            and self.settlement_date >= self.maturity_date
        ):
            raise ValueError("settlement_date must be before maturity_date.")
        return self


class BondPricingResponse(BaseModel):
    bond_type: BondType
    clean_price: float
    dirty_price: float
    accrued_interest: float
    present_value_of_cashflows: float
    price_status: str
    cash_flow_schedule: list[CashFlow]
    yield_assumptions: dict[str, Any]
    methodology: MethodologyMetadata
    data_quality: DataQualityMetadata
    data_source: DataSourceMetadata
    athena_commentary: AthenaRatesCommentary


class YieldAnalysisRequest(BaseModel):
    price: float = Field(default=1000, gt=0)
    face_value: float = Field(default=1000, gt=0)
    coupon_rate: float = Field(default=0.05, ge=0)
    coupon_frequency: CouponFrequency = "semiannual"
    years_to_maturity: float = Field(
        default=5,
        gt=0,
        le=100,
        allow_inf_nan=False,
    )
    current_market_price: float | None = Field(default=None, gt=0)
    holding_period: float | None = Field(default=None, gt=0)
    beginning_price: float | None = Field(default=None, gt=0)
    ending_price: float | None = Field(default=None, gt=0)
    coupon_received: float | None = Field(default=None, ge=0)
    language: Language = "en"


class YieldAnalysisResponse(BaseModel):
    yield_to_maturity: float | None
    current_yield: float
    holding_period_return: float | None
    convergence_status: str
    iterations: int
    pricing_error: float
    price_status: str
    interpretation: str
    methodology: MethodologyMetadata
    data_quality: DataQualityMetadata
    data_source: DataSourceMetadata
    athena_commentary: AthenaRatesCommentary


class DurationConvexityRequest(BondInputs):
    price: float | None = Field(default=None, gt=0)
    rate_shock_bps: float = Field(default=100, ge=-5000, le=5000)


class DurationConvexityResponse(BaseModel):
    price: float
    macaulay_duration: float
    modified_duration: float
    convexity: float
    dv01: float
    pvbp: float
    rate_shock_bps: float
    estimated_price_change_duration: float
    estimated_price_change_duration_convexity: float
    estimated_stressed_price_duration: float
    estimated_stressed_price_duration_convexity: float
    risk_interpretation: str
    methodology: MethodologyMetadata
    data_quality: DataQualityMetadata
    risk_monitor_payload: dict[str, Any]
    data_source: DataSourceMetadata
    athena_commentary: AthenaRatesCommentary


class YieldCurveRequest(BaseModel):
    curve_points: list[CurvePoint] = Field(default_factory=list)
    interpolation_method: Literal["linear"] = "linear"
    requested_maturities: list[PositiveMaturity] | None = None
    curve_type: Literal["spot", "par", "treasury_demo"] = "treasury_demo"
    language: Language = "en"


class YieldCurveResponse(BaseModel):
    input_curve: list[CurvePoint]
    interpolated_curve: list[CurvePoint]
    spot_rates: list[CurvePoint]
    forward_rates: list[ForwardRatePoint]
    curve_slope: float
    curve_slope_bps: float
    curve_shape: str
    curve_interpretation: str
    methodology: MethodologyMetadata
    data_quality: DataQualityMetadata
    data_source: DataSourceMetadata
    athena_commentary: AthenaRatesCommentary


class RateScenarioRequest(BondInputs):
    scenario_type: ScenarioType = "parallel_up"
    shock_bps: float = Field(default=100, ge=0, le=5000)
    curve_points: list[CurvePoint] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_stressed_periodic_yield(self) -> "RateScenarioRequest":
        if self.scenario_type not in {
            "parallel_down",
            "short_rate_down",
            "long_rate_down",
        }:
            return self
        frequency = {
            "annual": 1,
            "semiannual": 2,
            "quarterly": 4,
            "monthly": 12,
        }[self.coupon_frequency]
        lowest_possible_yield = self.yield_to_maturity - self.shock_bps / 10_000
        if 1 + lowest_possible_yield / frequency <= 0:
            raise ValueError(
                "The downward shock would make the periodic yield less than or equal to -100 percent."
            )
        return self


class RateScenarioResult(BaseModel):
    scenario_type: ScenarioType
    shock_bps: float
    base_price: float
    stressed_price: float
    price_change: float
    percent_change: float
    base_yield_at_maturity: float
    shocked_yield_at_maturity: float
    effective_shock_bps: float
    duration_estimate: float
    convexity_adjusted_estimate: float
    dv01_impact: float
    base_curve: list[CurvePoint]
    stressed_curve: list[CurvePoint]
    scenario_interpretation: str
    risk_warning: str


class RateScenarioResponse(RateScenarioResult):
    methodology: MethodologyMetadata
    data_quality: DataQualityMetadata
    stress_testing_payload: dict[str, Any]
    data_source: DataSourceMetadata


class PortfolioRatesExposureRequest(BaseModel):
    portfolio_id: str = Field(min_length=1)
    shock_bps: float = Field(default=100, ge=0, le=5000)


class FixedIncomeHolding(BaseModel):
    symbol: str
    name: str
    asset_type: str
    market_value: float
    weight: float
    estimated_duration: float | None
    estimated_dv01: float | None
    metadata_source: str
    warning: str | None


class PortfolioRatesExposureResponse(BaseModel):
    portfolio_id: str
    portfolio_name: str
    fixed_income_holdings: list[FixedIncomeHolding]
    fixed_income_market_value: float
    fixed_income_allocation: float
    weighted_average_duration: float | None
    estimated_portfolio_dv01: float | None
    estimated_rate_shock_loss: float | None
    shock_bps: float
    missing_data_warnings: list[str]
    risk_monitor_payload: dict[str, Any]
    methodology: MethodologyMetadata
    data_quality: DataQualityMetadata
    data_source: DataSourceMetadata
