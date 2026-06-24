from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_limit_center_service
from app.modules.limit_center.schemas import (
    BreachListResponse,
    BreachReviewRequest,
    BreachReviewResponse,
    LimitBreach,
    LimitCenterStatus,
    LimitEvaluationRequest,
    LimitEvaluationResponse,
    LimitRule,
    LimitRuleCreate,
    LimitRuleListResponse,
    LimitRuleUpdate,
    SourceModuleCard,
)
from app.modules.limit_center.service import LimitCenterService


router = APIRouter(prefix="/limit-center", tags=["limit-center"])


def _validated_call(call):
    try:
        return call()
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/status", response_model=LimitCenterStatus)
def get_status(
    service: LimitCenterService = Depends(get_limit_center_service),
) -> LimitCenterStatus:
    return service.get_status()


@router.get("/rules", response_model=LimitRuleListResponse)
def list_rules(
    service: LimitCenterService = Depends(get_limit_center_service),
) -> LimitRuleListResponse:
    return service.list_rules()


@router.post("/rules", response_model=LimitRule, status_code=201)
def create_rule(
    payload: LimitRuleCreate,
    service: LimitCenterService = Depends(get_limit_center_service),
) -> LimitRule:
    return _validated_call(lambda: service.create_rule(payload))


@router.put("/rules/{rule_id}", response_model=LimitRule)
def update_rule(
    rule_id: str,
    payload: LimitRuleUpdate,
    service: LimitCenterService = Depends(get_limit_center_service),
) -> LimitRule:
    return _validated_call(lambda: service.update_rule(rule_id, payload))


@router.delete("/rules/{rule_id}", response_model=dict[str, bool])
def delete_rule(
    rule_id: str,
    service: LimitCenterService = Depends(get_limit_center_service),
) -> dict[str, bool]:
    return {"deleted": service.delete_rule(rule_id)}


@router.post("/evaluate", response_model=LimitEvaluationResponse)
def evaluate(
    payload: LimitEvaluationRequest,
    service: LimitCenterService = Depends(get_limit_center_service),
) -> LimitEvaluationResponse:
    return _validated_call(lambda: service.evaluate(payload))


@router.post("/evaluate-module-payload", response_model=LimitEvaluationResponse)
def evaluate_module_payload(
    payload: LimitEvaluationRequest,
    service: LimitCenterService = Depends(get_limit_center_service),
) -> LimitEvaluationResponse:
    return _validated_call(lambda: service.evaluate(payload))


@router.get("/breaches", response_model=BreachListResponse)
def list_breaches(
    service: LimitCenterService = Depends(get_limit_center_service),
) -> BreachListResponse:
    return service.list_breaches()


@router.get("/breaches/{breach_id}", response_model=LimitBreach)
def get_breach(
    breach_id: str,
    service: LimitCenterService = Depends(get_limit_center_service),
) -> LimitBreach:
    return _validated_call(lambda: service.get_breach(breach_id))


@router.post("/breaches/{breach_id}/review", response_model=BreachReviewResponse)
def review_breach(
    breach_id: str,
    payload: BreachReviewRequest,
    service: LimitCenterService = Depends(get_limit_center_service),
) -> BreachReviewResponse:
    return _validated_call(lambda: service.review_breach(breach_id, payload))


@router.get("/source-modules", response_model=list[SourceModuleCard])
def source_modules(
    service: LimitCenterService = Depends(get_limit_center_service),
) -> list[SourceModuleCard]:
    return service.source_modules()


@router.get("/demo", response_model=LimitEvaluationResponse)
def demo(
    service: LimitCenterService = Depends(get_limit_center_service),
) -> LimitEvaluationResponse:
    return _validated_call(service.demo)
