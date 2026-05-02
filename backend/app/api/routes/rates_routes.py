from fastapi import APIRouter, Depends

from app.api.dependencies import get_rates_service
from app.schemas.rates_schema import RatesModuleStatus
from app.services.rates_service import RatesService

router = APIRouter(prefix="/rates", tags=["rates"])


@router.get("/status", response_model=RatesModuleStatus)
def get_rates_status(
    service: RatesService = Depends(get_rates_service),
) -> RatesModuleStatus:
    return service.get_module_status()
