from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.dependencies import get_demo_workflow_service
from app.modules.demo_workflow.schemas import (
    DemoRunHistoryResponse,
    DemoRunRequest,
    DemoRunSummary,
    DemoWorkflowStatus,
)
from app.modules.demo_workflow.service import DemoWorkflowService


router = APIRouter(prefix="/demo", tags=["demo-workflow"])


@router.get("/status", response_model=DemoWorkflowStatus)
def get_status(
    service: DemoWorkflowService = Depends(get_demo_workflow_service),
) -> DemoWorkflowStatus:
    return service.get_status()


@router.post("/run-athena-demo", response_model=DemoRunSummary)
def run_athena_demo(
    payload: DemoRunRequest,
    service: DemoWorkflowService = Depends(get_demo_workflow_service),
) -> DemoRunSummary:
    return service.run_athena_demo(payload)


@router.get("/history", response_model=DemoRunHistoryResponse)
def list_runs(
    service: DemoWorkflowService = Depends(get_demo_workflow_service),
) -> DemoRunHistoryResponse:
    return service.list_runs()
