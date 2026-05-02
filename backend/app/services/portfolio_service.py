from app.repositories.portfolio_repository import PortfolioRepository
from app.schemas.portfolio_schema import PortfolioListResponse, PortfolioSummary


class PortfolioService:
    def __init__(self, repository: PortfolioRepository) -> None:
        self.repository = repository

    def list_portfolios(self) -> PortfolioListResponse:
        return PortfolioListResponse(
            detail="Portfolio workflows are scaffolded and ready for persistence logic.",
            items=[
                PortfolioSummary.model_validate(portfolio)
                for portfolio in self.repository.list_portfolios()
            ],
        )
