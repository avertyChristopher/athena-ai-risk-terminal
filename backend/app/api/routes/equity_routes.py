from fastapi import APIRouter, Depends

from app.api.dependencies import get_equity_analysis_service
from app.schemas.equity_schema import (
    EquityDiagnosticsResponse,
    EquityFundamentalsResponse,
    EquityOverviewResponse,
    EquityRatiosResponse,
    EquityValuationResponse,
    GgmValuationRequest,
    GgmValuationResponse,
    SensitivityRequest,
    SensitivityResponse,
)
from app.services.equity_analysis_service import EquityAnalysisService

router = APIRouter(prefix="/equity", tags=["equity-analysis"])


@router.get("/{symbol}/overview", response_model=EquityOverviewResponse)
def get_equity_overview(
    symbol: str,
    service: EquityAnalysisService = Depends(get_equity_analysis_service),
) -> EquityOverviewResponse:
    return service.get_overview(symbol)


@router.get("/{symbol}/fundamentals", response_model=EquityFundamentalsResponse)
def get_equity_fundamentals(
    symbol: str,
    service: EquityAnalysisService = Depends(get_equity_analysis_service),
) -> EquityFundamentalsResponse:
    return service.get_fundamentals(symbol)


@router.get("/{symbol}/ratios", response_model=EquityRatiosResponse)
def get_equity_ratios(
    symbol: str,
    service: EquityAnalysisService = Depends(get_equity_analysis_service),
) -> EquityRatiosResponse:
    return service.get_ratios(symbol)


@router.get("/{symbol}/valuation", response_model=EquityValuationResponse)
def get_equity_valuation(
    symbol: str,
    service: EquityAnalysisService = Depends(get_equity_analysis_service),
) -> EquityValuationResponse:
    return service.get_valuation(symbol)


@router.get("/{symbol}/diagnostics", response_model=EquityDiagnosticsResponse)
def get_equity_diagnostics(
    symbol: str,
    service: EquityAnalysisService = Depends(get_equity_analysis_service),
) -> EquityDiagnosticsResponse:
    return service.get_diagnostics(symbol)


@router.post("/valuation/ggm", response_model=GgmValuationResponse)
def calculate_ggm_value(
    payload: GgmValuationRequest,
    service: EquityAnalysisService = Depends(get_equity_analysis_service),
) -> GgmValuationResponse:
    return service.calculate_ggm(payload)


@router.post("/valuation/sensitivity", response_model=SensitivityResponse)
def calculate_ggm_sensitivity(
    payload: SensitivityRequest,
    service: EquityAnalysisService = Depends(get_equity_analysis_service),
) -> SensitivityResponse:
    return service.calculate_sensitivity(payload)
