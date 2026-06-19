from fastapi import APIRouter, Depends

from app.api.dependencies import get_options_pricing_lab_service
from app.modules.options_pricing_lab.schemas import (
    OptionPricingRequest,
    OptionPricingResponse,
    OptionsPricingLabStatus,
    OptionStrategyRequest,
    OptionStrategyResponse,
)
from app.modules.options_pricing_lab.service import OptionsPricingLabService

router = APIRouter(prefix="/options-pricing-lab", tags=["options-pricing-lab"])


@router.get("/status", response_model=OptionsPricingLabStatus)
def get_options_pricing_lab_status(
    service: OptionsPricingLabService = Depends(get_options_pricing_lab_service),
) -> OptionsPricingLabStatus:
    return service.get_status()


@router.post("/price", response_model=OptionPricingResponse)
def price_option(
    payload: OptionPricingRequest,
    service: OptionsPricingLabService = Depends(get_options_pricing_lab_service),
) -> OptionPricingResponse:
    return service.price_option(payload)


@router.post("/strategy", response_model=OptionStrategyResponse)
def analyze_option_strategy(
    payload: OptionStrategyRequest,
    service: OptionsPricingLabService = Depends(get_options_pricing_lab_service),
) -> OptionStrategyResponse:
    return service.analyze_strategy(payload)


@router.get("/demo", response_model=OptionPricingResponse)
def get_options_pricing_lab_demo(
    service: OptionsPricingLabService = Depends(get_options_pricing_lab_service),
) -> OptionPricingResponse:
    return service.demo()
