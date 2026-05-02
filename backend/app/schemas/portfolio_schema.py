from pydantic import BaseModel, ConfigDict


class PortfolioSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    base_currency: str


class PortfolioListResponse(BaseModel):
    status: str = "placeholder"
    module: str = "portfolios"
    detail: str
    items: list[PortfolioSummary]
