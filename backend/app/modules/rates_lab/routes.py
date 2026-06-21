from collections.abc import Callable
from typing import TypeVar

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_rates_lab_service
from app.modules.rates_lab.schemas import (
    BondPricingRequest,
    BondPricingResponse,
    DurationConvexityRequest,
    DurationConvexityResponse,
    PortfolioRatesExposureRequest,
    PortfolioRatesExposureResponse,
    RateScenarioRequest,
    RateScenarioResponse,
    RatesLabStatus,
    YieldAnalysisRequest,
    YieldAnalysisResponse,
    YieldCurveRequest,
    YieldCurveResponse,
)
from app.modules.rates_lab.service import RatesLabService

router = APIRouter(prefix="/rates-lab", tags=["rates-lab"])
ResponseT = TypeVar("ResponseT")


@router.get("/status", response_model=RatesLabStatus)
def get_rates_lab_status(
    service: RatesLabService = Depends(get_rates_lab_service),
) -> RatesLabStatus:
    return service.get_status()


@router.post("/bond-price", response_model=BondPricingResponse)
def price_bond(
    payload: BondPricingRequest,
    service: RatesLabService = Depends(get_rates_lab_service),
) -> BondPricingResponse:
    return _validated_call(lambda: service.price_bond(payload))


@router.post("/yield-analysis", response_model=YieldAnalysisResponse)
def analyze_yield(
    payload: YieldAnalysisRequest,
    service: RatesLabService = Depends(get_rates_lab_service),
) -> YieldAnalysisResponse:
    return _validated_call(lambda: service.analyze_yield(payload))


@router.post("/duration-convexity", response_model=DurationConvexityResponse)
def analyze_duration_convexity(
    payload: DurationConvexityRequest,
    service: RatesLabService = Depends(get_rates_lab_service),
) -> DurationConvexityResponse:
    return _validated_call(lambda: service.analyze_duration_convexity(payload))


@router.post("/yield-curve", response_model=YieldCurveResponse)
def analyze_yield_curve(
    payload: YieldCurveRequest,
    service: RatesLabService = Depends(get_rates_lab_service),
) -> YieldCurveResponse:
    return _validated_call(lambda: service.analyze_yield_curve(payload))


@router.post("/rate-scenarios", response_model=RateScenarioResponse)
def analyze_rate_scenario(
    payload: RateScenarioRequest,
    service: RatesLabService = Depends(get_rates_lab_service),
) -> RateScenarioResponse:
    return _validated_call(lambda: service.analyze_rate_scenario(payload))


@router.post("/portfolio-exposure", response_model=PortfolioRatesExposureResponse)
def analyze_portfolio_exposure(
    payload: PortfolioRatesExposureRequest,
    service: RatesLabService = Depends(get_rates_lab_service),
) -> PortfolioRatesExposureResponse:
    return _validated_call(lambda: service.analyze_portfolio_exposure(payload))


@router.get("/demo", response_model=BondPricingResponse)
def get_rates_lab_demo(
    service: RatesLabService = Depends(get_rates_lab_service),
) -> BondPricingResponse:
    return _validated_call(service.demo)


def _validated_call(operation: Callable[[], ResponseT]) -> ResponseT:
    try:
        return operation()
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "invalid_financial_input",
                "message": str(exc),
            },
        ) from exc
