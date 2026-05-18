from pydantic import BaseModel, Field


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
