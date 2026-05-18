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
