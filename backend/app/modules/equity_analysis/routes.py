from fastapi import APIRouter, Depends

from app.api.dependencies import get_equity_analysis_service
from app.modules.equity_analysis.schemas import (
    EquityBusinessModelResponse,
    EquityCorporateActionsResponse,
    EquityDiagnosticsResponse,
    EquityFundamentalsResponse,
    EquityGrowthResponse,
    EquityIndustryResponse,
    EquityOverviewResponse,
    EquityPeerComparisonResponse,
    EquityRatiosResponse,
    EquityRelativeValuationResponse,
    EquitySecurityProfileResponse,
    EquityValuationResponse,
    GgmValuationRequest,
    GgmValuationResponse,
    SensitivityRequest,
    SensitivityResponse,
)
from app.modules.equity_analysis.service import EquityAnalysisService

router = APIRouter(prefix="/equity", tags=["equity-analysis"])


@router.get("/{symbol}/overview", response_model=EquityOverviewResponse)
def get_equity_overview(
    symbol: str,
    service: EquityAnalysisService = Depends(get_equity_analysis_service),
) -> EquityOverviewResponse:
    return service.get_overview(symbol)


@router.get("/{symbol}/security-profile", response_model=EquitySecurityProfileResponse)
def get_equity_security_profile(
    symbol: str,
    service: EquityAnalysisService = Depends(get_equity_analysis_service),
) -> EquitySecurityProfileResponse:
    return service.get_security_profile(symbol)


@router.get("/{symbol}/industry", response_model=EquityIndustryResponse)
def get_equity_industry(
    symbol: str,
    service: EquityAnalysisService = Depends(get_equity_analysis_service),
) -> EquityIndustryResponse:
    return service.get_industry(symbol)


@router.get("/{symbol}/business-model", response_model=EquityBusinessModelResponse)
def get_equity_business_model(
    symbol: str,
    service: EquityAnalysisService = Depends(get_equity_analysis_service),
) -> EquityBusinessModelResponse:
    return service.get_business_model(symbol)


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


@router.get("/{symbol}/growth", response_model=EquityGrowthResponse)
def get_equity_growth(
    symbol: str,
    service: EquityAnalysisService = Depends(get_equity_analysis_service),
) -> EquityGrowthResponse:
    return service.get_growth(symbol)


@router.get("/{symbol}/valuation", response_model=EquityValuationResponse)
def get_equity_valuation(
    symbol: str,
    service: EquityAnalysisService = Depends(get_equity_analysis_service),
) -> EquityValuationResponse:
    return service.get_valuation(symbol)


@router.get(
    "/{symbol}/relative-valuation",
    response_model=EquityRelativeValuationResponse,
)
def get_equity_relative_valuation(
    symbol: str,
    service: EquityAnalysisService = Depends(get_equity_analysis_service),
) -> EquityRelativeValuationResponse:
    return service.get_relative_valuation(symbol)


@router.get("/{symbol}/peer-comparison", response_model=EquityPeerComparisonResponse)
def get_equity_peer_comparison(
    symbol: str,
    service: EquityAnalysisService = Depends(get_equity_analysis_service),
) -> EquityPeerComparisonResponse:
    return service.get_peer_comparison(symbol)


@router.get(
    "/{symbol}/corporate-actions",
    response_model=EquityCorporateActionsResponse,
)
def get_equity_corporate_actions(
    symbol: str,
    service: EquityAnalysisService = Depends(get_equity_analysis_service),
) -> EquityCorporateActionsResponse:
    return service.get_corporate_actions(symbol)


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
