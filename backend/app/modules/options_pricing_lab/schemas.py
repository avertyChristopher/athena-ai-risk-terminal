from __future__ import annotations

from typing import Any, Literal

from pydantic import AliasChoices, BaseModel, Field, model_validator


OptionType = Literal["call", "put"]
PositionSide = Literal["long", "short"]
PricingModel = Literal["black_scholes", "binomial"]
ParityMode = Literal["theoretical", "observed"]
StrategyType = Literal[
    "covered_call",
    "protective_put",
    "long_straddle",
    "long_strangle",
    "bull_call_spread",
    "bear_put_spread",
    "collar",
    "cash_secured_put",
]
LegType = Literal["stock", "option", "cash"]


class OptionsPricingLabStatus(BaseModel):
    status: str = "ready"
    module: str = "options-pricing-lab"
    detail: str
    engines_available: list[str]


class OptionPricingRequest(BaseModel):
    underlying_symbol: str = Field(default="AAPL", min_length=1, max_length=32)
    option_type: OptionType = "call"
    position_side: PositionSide = "long"
    underlying_price: float | None = Field(default=None, gt=0)
    strike_price: float = Field(default=200.0, gt=0)
    time_to_expiration_days: int = Field(default=60, ge=1, le=3650)
    risk_free_rate: float = 0.045
    dividend_yield: float = Field(default=0.005, ge=0)
    volatility: float | None = Field(default=None, gt=0)
    pricing_model: PricingModel = "black_scholes"
    binomial_steps: int = Field(default=75, ge=1, le=500)
    contract_size: int = Field(default=100, ge=1)
    quantity: int = Field(default=1, ge=1)
    parity_mode: ParityMode = "theoretical"
    observed_call_price: float | None = Field(default=None, ge=0)
    observed_put_price: float | None = Field(default=None, ge=0)
    spot_shocks: list[float] = Field(
        default_factory=lambda: [-30.0, -20.0, -10.0, 0.0, 10.0, 20.0, 30.0]
    )
    volatility_shocks: list[float] = Field(
        default_factory=lambda: [-10.0, -5.0, 0.0, 5.0, 10.0]
    )
    time_points_days: list[int] | None = None
    rate_shocks: list[float] = Field(default_factory=lambda: [-1.0, 0.0, 1.0])

    @model_validator(mode="after")
    def validate_analysis_inputs(self) -> "OptionPricingRequest":
        if self.parity_mode == "observed" and (
            self.observed_call_price is None or self.observed_put_price is None
        ):
            raise ValueError(
                "Observed parity mode requires observed call and put prices."
            )
        scenario_lists = {
            "spot_shocks": self.spot_shocks,
            "volatility_shocks": self.volatility_shocks,
            "rate_shocks": self.rate_shocks,
        }
        for name, values in scenario_lists.items():
            if not values or len(values) > 25:
                raise ValueError(f"{name} must contain between 1 and 25 values.")
        if any(shock <= -100 for shock in self.spot_shocks):
            raise ValueError("spot_shocks must be greater than -100 percent.")
        if self.time_points_days is not None and (
            not self.time_points_days or len(self.time_points_days) > 25
        ):
            raise ValueError(
                "time_points_days must contain between 1 and 25 values."
            )
        return self


class ImpliedVolatilityRequest(BaseModel):
    underlying_symbol: str = Field(default="AAPL", min_length=1, max_length=32)
    option_type: OptionType = "call"
    observed_option_price: float = Field(gt=0)
    underlying_price: float | None = Field(default=None, gt=0)
    strike_price: float = Field(default=200.0, gt=0)
    time_to_expiration_days: int = Field(default=60, ge=1, le=3650)
    risk_free_rate: float = 0.045
    dividend_yield: float = Field(default=0.005, ge=0)
    initial_guess: float | None = Field(default=None, gt=0, le=10)
    tolerance: float = Field(default=1e-6, gt=0, le=0.1)
    max_iterations: int = Field(default=100, ge=1, le=1000)


class StrategyLeg(BaseModel):
    leg_type: LegType = "option"
    side: PositionSide
    option_type: OptionType | None = None
    strike_price: float | None = Field(
        default=None,
        gt=0,
        validation_alias=AliasChoices("strike_price", "strike"),
    )
    expiration_days: int | None = Field(default=None, ge=1)
    premium: float | None = Field(default=None, ge=0)
    quantity: int = Field(default=1, ge=1)
    contract_size: int = Field(default=100, ge=1)
    underlying_price: float | None = Field(default=None, gt=0)
    description: str = ""

    @model_validator(mode="after")
    def validate_leg(self) -> "StrategyLeg":
        if self.leg_type == "option":
            if self.option_type is None:
                raise ValueError("option_type is required for an option leg.")
            if self.strike_price is None:
                raise ValueError("strike_price is required for an option leg.")
            if self.expiration_days is None:
                raise ValueError("expiration_days is required for an option leg.")
        return self


OptionLeg = StrategyLeg


class OptionStrategyRequest(BaseModel):
    underlying_symbol: str = Field(default="AAPL", min_length=1, max_length=32)
    underlying_price: float | None = Field(default=None, gt=0)
    risk_free_rate: float = 0.045
    volatility: float | None = Field(default=None, gt=0)
    dividend_yield: float = Field(default=0.005, ge=0)
    strategy_type: StrategyType = "covered_call"
    legs: list[StrategyLeg] = Field(default_factory=list)
    contract_size: int = Field(default=100, ge=1)
    quantity: int = Field(default=1, ge=1)


class DataSources(BaseModel):
    underlying_price_source: str
    volatility_source: str
    risk_free_rate_source: str
    dividend_yield_source: str
    fallback_used: bool
    badges: list[str]
    warnings: list[str]


class ImpliedVolatilityResponse(BaseModel):
    implied_volatility: float | None
    converged: bool
    iterations: int
    model_price_at_iv: float | None
    pricing_error: float | None
    no_arbitrage_bounds: dict[str, float]
    validation_status: str
    warnings: list[str]
    methodology: str
    data_sources: DataSources | None = None


class GreeksResponse(BaseModel):
    delta: float
    gamma: float
    theta_annual: float
    theta_daily: float
    vega: float
    rho: float
    delta_per_contract: float
    position_delta: float
    position_gamma: float
    position_theta_daily: float
    position_vega: float
    position_rho: float
    delta_adjusted_exposure: float
    interpretation: dict[str, str]
    unit_metadata: dict[str, str]


class OptionPricingResponse(BaseModel):
    input_summary: dict[str, Any]
    pricing_summary: dict[str, Any]
    payoff_summary: dict[str, Any]
    greeks: GreeksResponse
    model_details: dict[str, Any]
    parity_check: dict[str, Any]
    sensitivity_analysis: dict[str, Any]
    methodology: dict[str, Any]
    assumptions: dict[str, Any]
    data_sources: DataSources
    athena_commentary: dict[str, Any]


class StrategyRiskValue(BaseModel):
    value: float | None
    type: Literal["finite", "unlimited", "unknown"]
    explanation: str


class OptionStrategyResponse(BaseModel):
    strategy_summary: dict[str, Any]
    legs: list[dict[str, Any]]
    net_premium: float
    payoff_table: list[dict[str, Any]]
    max_profit: StrategyRiskValue
    max_loss: StrategyRiskValue
    breakeven_points: list[float]
    payoff_profile: list[str]
    risk_notes: list[str]
    stock_leg_included: bool
    collateral_requirement: float
    aggregate_greeks: dict[str, Any]
    risk_summary: dict[str, Any]
    commentary: dict[str, Any]
    data_sources: DataSources
