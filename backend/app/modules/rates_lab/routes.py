from fastapi import APIRouter, Depends

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
    return service.price_bond(payload)


@router.post("/yield-analysis", response_model=YieldAnalysisResponse)
def analyze_yield(
    payload: YieldAnalysisRequest,
    service: RatesLabService = Depends(get_rates_lab_service),
) -> YieldAnalysisResponse:
    return service.analyze_yield(payload)


@router.post("/duration-convexity", response_model=DurationConvexityResponse)
def analyze_duration_convexity(
    payload: DurationConvexityRequest,
    service: RatesLabService = Depends(get_rates_lab_service),
) -> DurationConvexityResponse:
    return service.analyze_duration_convexity(payload)


@router.post("/yield-curve", response_model=YieldCurveResponse)
def analyze_yield_curve(
    payload: YieldCurveRequest,
    service: RatesLabService = Depends(get_rates_lab_service),
) -> YieldCurveResponse:
    return service.analyze_yield_curve(payload)


@router.post("/rate-scenarios", response_model=RateScenarioResponse)
def analyze_rate_scenario(
    payload: RateScenarioRequest,
    service: RatesLabService = Depends(get_rates_lab_service),
) -> RateScenarioResponse:
    return service.analyze_rate_scenario(payload)


@router.post("/portfolio-exposure", response_model=PortfolioRatesExposureResponse)
def analyze_portfolio_exposure(
    payload: PortfolioRatesExposureRequest,
    service: RatesLabService = Depends(get_rates_lab_service),
) -> PortfolioRatesExposureResponse:
    return service.analyze_portfolio_exposure(payload)


@router.get("/demo", response_model=BondPricingResponse)
def get_rates_lab_demo(
    service: RatesLabService = Depends(get_rates_lab_service),
) -> BondPricingResponse:
    return service.demo()
