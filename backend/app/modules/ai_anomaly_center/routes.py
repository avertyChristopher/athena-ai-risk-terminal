from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_ai_anomaly_center_service
from app.modules.ai_anomaly_center.schemas import (
    AIAnomalyCenterStatus,
    AnomalyCsvExportResponse,
    AnomalyDeleteResponse,
    AnomalyHistoryResponse,
    AnomalyListResponse,
    AnomalyRecord,
    AnomalyReviewRequest,
    AnomalyReviewResponse,
    AnomalyScanRequest,
    AnomalyScanResponse,
)
from app.modules.ai_anomaly_center.service import AIAnomalyCenterService


router = APIRouter(prefix="/ai-anomaly-center", tags=["ai-anomaly-center"])


@router.get("/status", response_model=AIAnomalyCenterStatus)
def get_status(
    service: AIAnomalyCenterService = Depends(get_ai_anomaly_center_service),
) -> AIAnomalyCenterStatus:
    return service.get_status()


@router.post("/scan", response_model=AnomalyScanResponse)
def scan(
    payload: AnomalyScanRequest,
    service: AIAnomalyCenterService = Depends(get_ai_anomaly_center_service),
) -> AnomalyScanResponse:
    return service.scan(payload)


@router.get("/anomalies", response_model=AnomalyListResponse)
def list_anomalies(
    portfolio_id: str | None = Query(default=None),
    severity: str | None = Query(default=None),
    module_name: str | None = Query(default=None),
    status: str | None = Query(default=None),
    service: AIAnomalyCenterService = Depends(get_ai_anomaly_center_service),
) -> AnomalyListResponse:
    return service.list_anomalies(
        portfolio_id=portfolio_id,
        severity=severity,
        module_name=module_name,
        status=status,
    )


@router.get("/anomalies/export/csv", response_model=AnomalyCsvExportResponse)
def export_csv(
    service: AIAnomalyCenterService = Depends(get_ai_anomaly_center_service),
) -> AnomalyCsvExportResponse:
    return service.export_csv()


@router.get("/anomalies/{anomaly_id}", response_model=AnomalyRecord)
def get_anomaly(
    anomaly_id: str,
    service: AIAnomalyCenterService = Depends(get_ai_anomaly_center_service),
) -> AnomalyRecord:
    return service.get_anomaly(anomaly_id)


@router.post("/anomalies/{anomaly_id}/review", response_model=AnomalyReviewResponse)
def review_anomaly(
    anomaly_id: str,
    payload: AnomalyReviewRequest,
    service: AIAnomalyCenterService = Depends(get_ai_anomaly_center_service),
) -> AnomalyReviewResponse:
    return service.review_anomaly(anomaly_id, payload)


@router.delete("/anomalies/{anomaly_id}", response_model=AnomalyDeleteResponse)
def delete_anomaly(
    anomaly_id: str,
    service: AIAnomalyCenterService = Depends(get_ai_anomaly_center_service),
) -> AnomalyDeleteResponse:
    return service.delete_anomaly(anomaly_id)


@router.get("/history", response_model=AnomalyHistoryResponse)
def history(
    service: AIAnomalyCenterService = Depends(get_ai_anomaly_center_service),
) -> AnomalyHistoryResponse:
    return service.history()


@router.get("/demo", response_model=AnomalyScanResponse)
def demo(
    service: AIAnomalyCenterService = Depends(get_ai_anomaly_center_service),
) -> AnomalyScanResponse:
    return service.demo()
