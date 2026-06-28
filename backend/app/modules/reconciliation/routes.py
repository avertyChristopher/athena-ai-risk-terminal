from fastapi import APIRouter, Depends

from app.api.dependencies import get_reconciliation_service
from app.modules.reconciliation.schemas import (
    BreakRegisterResponse,
    ReconciliationBreak,
    ReconciliationCsvExportResponse,
    ReconciliationDeleteResponse,
    ReconciliationHistoryResponse,
    ReconciliationRequest,
    ReconciliationRunResult,
    ReconciliationStatus,
    ReviewRequest,
)
from app.modules.reconciliation.service import ReconciliationService


router = APIRouter(prefix="/reconciliation", tags=["reconciliation"])


@router.get("/status", response_model=ReconciliationStatus)
def get_reconciliation_status(
    service: ReconciliationService = Depends(get_reconciliation_service),
) -> ReconciliationStatus:
    return service.get_status()


@router.post("/run", response_model=ReconciliationRunResult)
def run_reconciliation(
    payload: ReconciliationRequest,
    service: ReconciliationService = Depends(get_reconciliation_service),
) -> ReconciliationRunResult:
    return service.run(payload)


@router.get("/demo", response_model=ReconciliationRunResult)
def get_reconciliation_demo(
    service: ReconciliationService = Depends(get_reconciliation_service),
) -> ReconciliationRunResult:
    return service.demo()


@router.get("/breaks", response_model=BreakRegisterResponse)
def list_reconciliation_breaks(
    service: ReconciliationService = Depends(get_reconciliation_service),
) -> BreakRegisterResponse:
    return service.list_breaks()


@router.get("/breaks/{break_id}", response_model=ReconciliationBreak)
def get_reconciliation_break(
    break_id: str,
    service: ReconciliationService = Depends(get_reconciliation_service),
) -> ReconciliationBreak:
    return service.get_break(break_id)


@router.post("/breaks/{break_id}/review", response_model=ReconciliationBreak)
def review_reconciliation_break(
    break_id: str,
    payload: ReviewRequest,
    service: ReconciliationService = Depends(get_reconciliation_service),
) -> ReconciliationBreak:
    return service.review_break(break_id, payload)


@router.get("/history", response_model=ReconciliationHistoryResponse)
def list_reconciliation_history(
    service: ReconciliationService = Depends(get_reconciliation_service),
) -> ReconciliationHistoryResponse:
    return service.list_history()


@router.get("/history/{run_id}", response_model=ReconciliationRunResult)
def get_reconciliation_history_item(
    run_id: str,
    service: ReconciliationService = Depends(get_reconciliation_service),
) -> ReconciliationRunResult:
    return service.get_history_item(run_id)


@router.delete("/history/{run_id}", response_model=ReconciliationDeleteResponse)
def delete_reconciliation_history_item(
    run_id: str,
    service: ReconciliationService = Depends(get_reconciliation_service),
) -> ReconciliationDeleteResponse:
    return service.delete_history_item(run_id)


@router.get("/history/{run_id}/export/csv", response_model=ReconciliationCsvExportResponse)
def export_reconciliation_csv(
    run_id: str,
    service: ReconciliationService = Depends(get_reconciliation_service),
) -> ReconciliationCsvExportResponse:
    return service.export_csv(run_id)
