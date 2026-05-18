from fastapi import APIRouter, Depends

from app.api.dependencies import get_portfolio_service, get_position_service
from app.schemas.portfolio_schema import (
    AllocationResponse,
    ConcentrationResponse,
    DeleteResponse,
    PortfolioCreate,
    PortfolioListResponse,
    PortfolioRead,
    PortfolioSummary,
    PortfolioUpdate,
)
from app.schemas.position_schema import (
    PositionCreate,
    PositionListResponse,
    PositionRead,
    PositionUpdate,
)
from app.services.portfolio_service import PortfolioService
from app.services.position_service import PositionService

router = APIRouter(prefix="/portfolios", tags=["portfolios"])


@router.get("", response_model=PortfolioListResponse)
def list_portfolios(
    service: PortfolioService = Depends(get_portfolio_service),
) -> PortfolioListResponse:
    return service.list_portfolios()


@router.post("", response_model=PortfolioRead, status_code=201)
def create_portfolio(
    payload: PortfolioCreate,
    service: PortfolioService = Depends(get_portfolio_service),
) -> PortfolioRead:
    return service.create_portfolio(payload)


@router.get("/{portfolio_id}", response_model=PortfolioRead)
def get_portfolio(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> PortfolioRead:
    return service.get_portfolio(portfolio_id)


@router.put("/{portfolio_id}", response_model=PortfolioRead)
def update_portfolio(
    portfolio_id: str,
    payload: PortfolioUpdate,
    service: PortfolioService = Depends(get_portfolio_service),
) -> PortfolioRead:
    return service.update_portfolio(portfolio_id, payload)


@router.delete("/{portfolio_id}", response_model=DeleteResponse)
def delete_portfolio(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> DeleteResponse:
    return service.delete_portfolio(portfolio_id)


@router.get("/{portfolio_id}/summary", response_model=PortfolioSummary)
def get_portfolio_summary(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> PortfolioSummary:
    return service.get_summary(portfolio_id)


@router.get("/{portfolio_id}/positions", response_model=PositionListResponse)
def list_positions(
    portfolio_id: str,
    service: PositionService = Depends(get_position_service),
) -> PositionListResponse:
    return service.list_positions(portfolio_id)


@router.post("/{portfolio_id}/positions", response_model=PositionRead, status_code=201)
def create_position(
    portfolio_id: str,
    payload: PositionCreate,
    service: PositionService = Depends(get_position_service),
) -> PositionRead:
    return service.create_position(portfolio_id, payload)


@router.put("/{portfolio_id}/positions/{position_id}", response_model=PositionRead)
def update_position(
    portfolio_id: str,
    position_id: str,
    payload: PositionUpdate,
    service: PositionService = Depends(get_position_service),
) -> PositionRead:
    return service.update_position(portfolio_id, position_id, payload)


@router.delete("/{portfolio_id}/positions/{position_id}", response_model=DeleteResponse)
def delete_position(
    portfolio_id: str,
    position_id: str,
    service: PositionService = Depends(get_position_service),
) -> DeleteResponse:
    return service.delete_position(portfolio_id, position_id)


@router.get("/{portfolio_id}/allocation/assets", response_model=AllocationResponse)
def get_asset_allocation(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> AllocationResponse:
    return service.get_allocation(portfolio_id, "assets")


@router.get("/{portfolio_id}/allocation/sectors", response_model=AllocationResponse)
def get_sector_allocation(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> AllocationResponse:
    return service.get_allocation(portfolio_id, "sectors")


@router.get("/{portfolio_id}/allocation/currencies", response_model=AllocationResponse)
def get_currency_allocation(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> AllocationResponse:
    return service.get_allocation(portfolio_id, "currencies")


@router.get("/{portfolio_id}/allocation/countries", response_model=AllocationResponse)
def get_country_allocation(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> AllocationResponse:
    return service.get_allocation(portfolio_id, "countries")


@router.get("/{portfolio_id}/allocation/asset-types", response_model=AllocationResponse)
def get_asset_type_allocation(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> AllocationResponse:
    return service.get_allocation(portfolio_id, "asset-types")


@router.get("/{portfolio_id}/concentration", response_model=ConcentrationResponse)
def get_concentration(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> ConcentrationResponse:
    return service.get_concentration(portfolio_id)
