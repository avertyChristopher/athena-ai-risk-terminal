from fastapi import APIRouter, Depends

from app.api.dependencies import get_portfolio_service
from app.schemas.portfolio_schema import PortfolioListResponse
from app.services.portfolio_service import PortfolioService

router = APIRouter(prefix="/portfolios", tags=["portfolios"])


@router.get("", response_model=PortfolioListResponse)
def list_portfolios(
    service: PortfolioService = Depends(get_portfolio_service),
) -> PortfolioListResponse:
    return service.list_portfolios()
