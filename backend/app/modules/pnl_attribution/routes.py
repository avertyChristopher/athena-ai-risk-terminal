from fastapi import APIRouter, Depends

from app.api.dependencies import get_pnl_attribution_service
from app.modules.pnl_attribution.schemas import (
    PnlAttributionRequest,
    PnlAttributionResult,
    PnlAttributionStatus,
    PnlCsvExportResponse,
    PnlDeleteResponse,
    PnlHistoryResponse,
)
from app.modules.pnl_attribution.service import PnlAttributionService


router = APIRouter(prefix="/pnl-attribution", tags=["pnl-attribution"])


@router.get("/status", response_model=PnlAttributionStatus)
def get_pnl_attribution_status(
    service: PnlAttributionService = Depends(get_pnl_attribution_service),
) -> PnlAttributionStatus:
    return service.get_status()


@router.post("/analyze", response_model=PnlAttributionResult)
def analyze_pnl_attribution(
    payload: PnlAttributionRequest,
    service: PnlAttributionService = Depends(get_pnl_attribution_service),
) -> PnlAttributionResult:
    return service.analyze(payload)


@router.get("/demo", response_model=PnlAttributionResult)
def get_pnl_attribution_demo(
    service: PnlAttributionService = Depends(get_pnl_attribution_service),
) -> PnlAttributionResult:
    return service.demo()


@router.get("/history", response_model=PnlHistoryResponse)
def list_pnl_history(
    service: PnlAttributionService = Depends(get_pnl_attribution_service),
) -> PnlHistoryResponse:
    return service.list_history()


@router.get("/history/{analysis_id}", response_model=PnlAttributionResult)
def get_pnl_history_item(
    analysis_id: str,
    service: PnlAttributionService = Depends(get_pnl_attribution_service),
) -> PnlAttributionResult:
    return service.get_history_item(analysis_id)


@router.delete("/history/{analysis_id}", response_model=PnlDeleteResponse)
def delete_pnl_history_item(
    analysis_id: str,
    service: PnlAttributionService = Depends(get_pnl_attribution_service),
) -> PnlDeleteResponse:
    return service.delete_history_item(analysis_id)


@router.get("/history/{analysis_id}/export/csv", response_model=PnlCsvExportResponse)
def export_pnl_history_csv(
    analysis_id: str,
    service: PnlAttributionService = Depends(get_pnl_attribution_service),
) -> PnlCsvExportResponse:
    return service.export_csv(analysis_id)
