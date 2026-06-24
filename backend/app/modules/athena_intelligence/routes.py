from fastapi import APIRouter, Depends

from app.api.dependencies import get_athena_intelligence_service
from app.modules.athena_intelligence.schemas import (
    AthenaAICommentary,
    AthenaIntelligenceRequest,
    AthenaIntelligenceStatus,
    AthenaMetricExplanationRequest,
    AthenaMetricExplanationResponse,
    AthenaRiskSynthesisRequest,
    AthenaRiskSynthesisResponse,
)
from app.modules.athena_intelligence.service import AthenaIntelligenceService

router = APIRouter(prefix="/athena-intelligence", tags=["athena-intelligence"])


@router.get("/status", response_model=AthenaIntelligenceStatus)
def get_athena_intelligence_status(
    service: AthenaIntelligenceService = Depends(get_athena_intelligence_service),
) -> AthenaIntelligenceStatus:
    return service.get_status()


@router.post("/commentary", response_model=AthenaAICommentary)
def generate_module_commentary(
    payload: AthenaIntelligenceRequest,
    service: AthenaIntelligenceService = Depends(get_athena_intelligence_service),
) -> AthenaAICommentary:
    return service.generate_commentary(payload)


@router.post("/risk-synthesis", response_model=AthenaRiskSynthesisResponse)
def generate_risk_synthesis(
    payload: AthenaRiskSynthesisRequest,
    service: AthenaIntelligenceService = Depends(get_athena_intelligence_service),
) -> AthenaRiskSynthesisResponse:
    return service.generate_risk_synthesis(payload)


@router.post("/explain-metric", response_model=AthenaMetricExplanationResponse)
def explain_metric(
    payload: AthenaMetricExplanationRequest,
    service: AthenaIntelligenceService = Depends(get_athena_intelligence_service),
) -> AthenaMetricExplanationResponse:
    return service.explain_metric(payload)


@router.get("/demo", response_model=AthenaAICommentary)
def get_athena_intelligence_demo(
    service: AthenaIntelligenceService = Depends(get_athena_intelligence_service),
) -> AthenaAICommentary:
    return service.demo()
