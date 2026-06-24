from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_stress_testing_service
from app.modules.stress_testing.schemas import (
    ScenarioLibraryResponse,
    StressTestingResponse,
    StressTestingRunRequest,
    StressTestingStatus,
)
from app.modules.stress_testing.service import StressTestingService


router = APIRouter(prefix="/stress-testing", tags=["stress-testing"])


def _validated_call(call):
    try:
        return call()
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/status", response_model=StressTestingStatus)
def get_status(
    service: StressTestingService = Depends(get_stress_testing_service),
) -> StressTestingStatus:
    return service.get_status()


@router.get("/scenarios", response_model=ScenarioLibraryResponse)
def list_scenarios(
    service: StressTestingService = Depends(get_stress_testing_service),
) -> ScenarioLibraryResponse:
    return service.list_scenarios()


@router.post("/run", response_model=StressTestingResponse)
def run_stress_test(
    payload: StressTestingRunRequest,
    service: StressTestingService = Depends(get_stress_testing_service),
) -> StressTestingResponse:
    return _validated_call(lambda: service.run(payload))


@router.post("/custom-scenario", response_model=StressTestingResponse)
def run_custom_scenario(
    payload: StressTestingRunRequest,
    service: StressTestingService = Depends(get_stress_testing_service),
) -> StressTestingResponse:
    return _validated_call(lambda: service.run(payload))


@router.get("/demo", response_model=StressTestingResponse)
def demo(
    service: StressTestingService = Depends(get_stress_testing_service),
) -> StressTestingResponse:
    return _validated_call(service.demo)
