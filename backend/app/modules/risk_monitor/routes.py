from fastapi import APIRouter, Depends

from app.api.dependencies import get_risk_monitor_service
from app.modules.risk_monitor.schemas import (
    RiskMonitorAnalysisResponse,
    RiskMonitorAnalyzeRequest,
    RiskMonitorStatus,
)
from app.modules.risk_monitor.service import RiskMonitorService
from app.modules.risk_shared.schemas import SharedRiskPayload

router = APIRouter(prefix="/risk-monitor", tags=["risk-monitor"])


@router.get("/status", response_model=RiskMonitorStatus)
def get_risk_monitor_status(
    service: RiskMonitorService = Depends(get_risk_monitor_service),
) -> RiskMonitorStatus:
    return service.get_module_status()


@router.post("/analyze", response_model=RiskMonitorAnalysisResponse)
def analyze_portfolio_risk(
    payload: RiskMonitorAnalyzeRequest,
    service: RiskMonitorService = Depends(get_risk_monitor_service),
) -> RiskMonitorAnalysisResponse:
    return service.analyze(payload)


@router.post("/analyze-from-volatility", response_model=RiskMonitorAnalysisResponse)
def analyze_from_volatility_payload(
    payload: SharedRiskPayload,
    service: RiskMonitorService = Depends(get_risk_monitor_service),
) -> RiskMonitorAnalysisResponse:
    return service.analyze_from_volatility(payload)


@router.get("/demo", response_model=RiskMonitorAnalysisResponse)
def get_demo_risk_monitor(
    service: RiskMonitorService = Depends(get_risk_monitor_service),
) -> RiskMonitorAnalysisResponse:
    return service.analyze(RiskMonitorAnalyzeRequest(portfolio_id="pf_001"))
