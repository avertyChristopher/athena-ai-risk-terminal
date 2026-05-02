from fastapi import APIRouter, Depends

from app.api.dependencies import get_market_data_service
from app.schemas.market_data_schema import MarketDataModuleStatus
from app.services.market_data_service import MarketDataService

router = APIRouter(prefix="/market-data", tags=["market-data"])


@router.get("/status", response_model=MarketDataModuleStatus)
def get_market_data_status(
    service: MarketDataService = Depends(get_market_data_service),
) -> MarketDataModuleStatus:
    return service.get_module_status()
