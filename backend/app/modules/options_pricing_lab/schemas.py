from typing import Any, Literal

from pydantic import BaseModel, Field


OptionType = Literal["call", "put"]
PositionSide = Literal["long", "short"]
PricingModel = Literal["black_scholes", "binomial"]
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


class OptionLeg(BaseModel):
    option_type: OptionType
    side: PositionSide
    strike: float = Field(gt=0)
    expiration_days: int = Field(default=60, ge=1)
    quantity: int = Field(default=1, ge=1)
    premium: float | None = Field(default=None, ge=0)


class OptionStrategyRequest(BaseModel):
    underlying_symbol: str = Field(default="AAPL", min_length=1, max_length=32)
    underlying_price: float | None = Field(default=None, gt=0)
    risk_free_rate: float = 0.045
    volatility: float | None = Field(default=None, gt=0)
    dividend_yield: float = Field(default=0.005, ge=0)
    strategy_type: StrategyType = "covered_call"
    legs: list[OptionLeg] = Field(default_factory=list)
    contract_size: int = Field(default=100, ge=1)


class DataSources(BaseModel):
    underlying_price_source: str
    volatility_source: str
    risk_free_rate_source: str
    dividend_yield_source: str
    fallback_used: bool
    badges: list[str]
    warnings: list[str]


class GreeksResponse(BaseModel):
    delta: float
    gamma: float
    theta_annual: float
    theta_daily: float
    vega: float
    rho: float
    delta_per_contract: float
    delta_adjusted_exposure: float
    interpretation: dict[str, str]


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


class OptionStrategyResponse(BaseModel):
    strategy_summary: dict[str, Any]
    legs: list[dict[str, Any]]
    net_premium: float
    payoff_table: list[dict[str, Any]]
    max_profit: float | None
    max_loss: float | None
    breakeven_points: list[float]
    aggregate_greeks: dict[str, float]
    risk_summary: dict[str, Any]
    commentary: dict[str, Any]
    data_sources: DataSources
