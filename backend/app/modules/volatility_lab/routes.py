from fastapi import APIRouter, Depends

from app.api.dependencies import get_volatility_lab_service
from app.modules.volatility_lab.schemas import (
    VolatilityAssetAnalysisRequest,
    VolatilityAssetAnalysisResponse,
    VolatilityLabStatus,
    VolatilityPortfolioAnalysisRequest,
    VolatilityPortfolioAnalysisResponse,
)
from app.modules.volatility_lab.service import VolatilityLabService

router = APIRouter(prefix="/volatility-lab", tags=["volatility-lab"])


@router.get("/status", response_model=VolatilityLabStatus)
def get_volatility_lab_status(
    service: VolatilityLabService = Depends(get_volatility_lab_service),
) -> VolatilityLabStatus:
    return service.get_status()


@router.post("/analyze-asset", response_model=VolatilityAssetAnalysisResponse)
def analyze_asset_volatility(
    payload: VolatilityAssetAnalysisRequest,
    service: VolatilityLabService = Depends(get_volatility_lab_service),
) -> VolatilityAssetAnalysisResponse:
    return service.analyze_asset(payload)


@router.post("/analyze-portfolio", response_model=VolatilityPortfolioAnalysisResponse)
def analyze_portfolio_volatility(
    payload: VolatilityPortfolioAnalysisRequest,
    service: VolatilityLabService = Depends(get_volatility_lab_service),
) -> VolatilityPortfolioAnalysisResponse:
    return service.analyze_portfolio(payload)


@router.get("/demo", response_model=VolatilityPortfolioAnalysisResponse)
def get_demo_volatility_lab(
    service: VolatilityLabService = Depends(get_volatility_lab_service),
) -> VolatilityPortfolioAnalysisResponse:
    return service.analyze_portfolio(
        VolatilityPortfolioAnalysisRequest(portfolio_id="pf_001"),
    )
