from fastapi import APIRouter, Depends

from app.api.dependencies import get_market_data_service
from app.schemas.market_data_schema import (
    DataQualityResponse,
    MarketAsset,
    MarketDataModuleStatus,
    PricePoint,
    ReturnPoint,
    VolatilityResponse,
)
from app.services.market_data_service import MarketDataService

router = APIRouter(prefix="/market-data", tags=["market-data"])


@router.get("/status", response_model=MarketDataModuleStatus)
def get_market_data_status(
    service: MarketDataService = Depends(get_market_data_service),
) -> MarketDataModuleStatus:
    return service.get_module_status()


@router.get("/assets", response_model=list[MarketAsset])
def list_assets(
    service: MarketDataService = Depends(get_market_data_service),
) -> list[MarketAsset]:
    return service.list_assets()


@router.get("/prices/{symbol}", response_model=list[PricePoint])
def get_prices(
    symbol: str,
    service: MarketDataService = Depends(get_market_data_service),
) -> list[PricePoint]:
    return service.get_prices(symbol)


@router.get("/returns/{symbol}", response_model=list[ReturnPoint])
def get_returns(
    symbol: str,
    service: MarketDataService = Depends(get_market_data_service),
) -> list[ReturnPoint]:
    return service.get_returns(symbol)


@router.get("/volatility/{symbol}", response_model=VolatilityResponse)
def get_volatility(
    symbol: str,
    service: MarketDataService = Depends(get_market_data_service),
) -> VolatilityResponse:
    return service.get_volatility(symbol)


@router.get("/data-quality/{symbol}", response_model=DataQualityResponse)
def get_data_quality(
    symbol: str,
    service: MarketDataService = Depends(get_market_data_service),
) -> DataQualityResponse:
    return service.get_data_quality(symbol)
