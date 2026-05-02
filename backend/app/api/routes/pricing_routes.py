from fastapi import APIRouter, Depends

from app.api.dependencies import get_pricing_service
from app.schemas.pricing_schema import PricingModuleStatus
from app.services.pricing_service import PricingService

router = APIRouter(prefix="/pricing", tags=["pricing"])


@router.get("/status", response_model=PricingModuleStatus)
def get_pricing_status(
    service: PricingService = Depends(get_pricing_service),
) -> PricingModuleStatus:
    return service.get_module_status()
