from pydantic import BaseModel, Field


class PortfolioBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    base_currency: str = Field(min_length=3, max_length=3)
    benchmark: str = Field(default="SPY", min_length=1, max_length=32)
    cash: float = Field(default=0.0, ge=0)


class PortfolioCreate(PortfolioBase):
    pass


class PortfolioUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    base_currency: str | None = Field(default=None, min_length=3, max_length=3)
    benchmark: str | None = Field(default=None, min_length=1, max_length=32)
    cash: float | None = Field(default=None, ge=0)


class PortfolioRead(PortfolioBase):
    id: str


class PortfolioSummary(BaseModel):
    portfolio_id: str
    name: str
    base_currency: str
    total_value: float
    number_of_positions: int
    benchmark: str
    cash: float
    cash_weight: float
    largest_position_weight: float
    top_5_holdings_weight: float


class AllocationItem(BaseModel):
    name: str
    market_value: float
    weight: float


class AllocationResponse(BaseModel):
    portfolio_id: str
    allocation_type: str
    items: list[AllocationItem]


class ConcentrationResponse(BaseModel):
    portfolio_id: str
    largest_position_weight: float
    top_5_holdings_weight: float
    number_of_positions: int
    diversification_score: float


class PortfolioListResponse(BaseModel):
    status: str = "ready"
    module: str = "portfolios"
    detail: str
    items: list[PortfolioRead]


class DeleteResponse(BaseModel):
    status: str
    id: str


class PositionBase(BaseModel):
    symbol: str = Field(min_length=1, max_length=32)
    asset_name: str = Field(min_length=1, max_length=255)
    asset_type: str = Field(min_length=1, max_length=64)
    quantity: float = Field(ge=0)
    average_price: float = Field(ge=0)
    current_price: float = Field(ge=0)
    currency: str = Field(min_length=3, max_length=3)
    sector: str = Field(min_length=1, max_length=80)
    country: str = Field(min_length=1, max_length=80)


class PositionCreate(PositionBase):
    pass


class PositionUpdate(BaseModel):
    symbol: str | None = Field(default=None, min_length=1, max_length=32)
    asset_name: str | None = Field(default=None, min_length=1, max_length=255)
    asset_type: str | None = Field(default=None, min_length=1, max_length=64)
    quantity: float | None = Field(default=None, ge=0)
    average_price: float | None = Field(default=None, ge=0)
    current_price: float | None = Field(default=None, ge=0)
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    sector: str | None = Field(default=None, min_length=1, max_length=80)
    country: str | None = Field(default=None, min_length=1, max_length=80)


class PositionRead(PositionBase):
    id: str
    portfolio_id: str
    market_value: float
    weight: float


class PositionListResponse(BaseModel):
    portfolio_id: str
    items: list[PositionRead]
