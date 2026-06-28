from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_trade_blotter_service
from app.modules.trade_blotter.schemas import (
    TradeBlotterDemoResponse,
    TradeBlotterDeleteResponse,
    TradeBlotterEntry,
    TradeBlotterEntryCreate,
    TradeBlotterEntryUpdate,
    TradeBlotterFromSimulationRequest,
    TradeBlotterListResponse,
    TradeBlotterReviewRequest,
    TradeBlotterReviewResponse,
    TradeBlotterStatus,
)
from app.modules.trade_blotter.service import TradeBlotterService


router = APIRouter(prefix="/trade-blotter", tags=["trade-blotter"])


@router.get("/status", response_model=TradeBlotterStatus)
def get_status(
    service: TradeBlotterService = Depends(get_trade_blotter_service),
) -> TradeBlotterStatus:
    return service.get_status()


@router.get("/trades", response_model=TradeBlotterListResponse)
@router.get("/entries", response_model=TradeBlotterListResponse)
def list_entries(
    portfolio_id: str | None = Query(default=None),
    symbol: str | None = Query(default=None),
    status: str | None = Query(default=None),
    service: TradeBlotterService = Depends(get_trade_blotter_service),
) -> TradeBlotterListResponse:
    return service.list_entries(portfolio_id=portfolio_id, symbol=symbol, status=status)


@router.post("/trades", response_model=TradeBlotterEntry)
@router.post("/entries", response_model=TradeBlotterEntry)
def create_entry(
    payload: TradeBlotterEntryCreate,
    service: TradeBlotterService = Depends(get_trade_blotter_service),
) -> TradeBlotterEntry:
    return service.create_entry(payload)


@router.get("/trades/{trade_id}", response_model=TradeBlotterEntry)
@router.get("/entries/{trade_id}", response_model=TradeBlotterEntry)
def get_entry(
    trade_id: str,
    service: TradeBlotterService = Depends(get_trade_blotter_service),
) -> TradeBlotterEntry:
    return service.get_entry(trade_id)


@router.put("/trades/{trade_id}", response_model=TradeBlotterEntry)
@router.patch("/trades/{trade_id}", response_model=TradeBlotterEntry)
@router.patch("/entries/{trade_id}", response_model=TradeBlotterEntry)
def update_entry(
    trade_id: str,
    payload: TradeBlotterEntryUpdate,
    service: TradeBlotterService = Depends(get_trade_blotter_service),
) -> TradeBlotterEntry:
    return service.update_entry(trade_id, payload)


@router.post("/trades/{trade_id}/review", response_model=TradeBlotterReviewResponse)
@router.post("/entries/{trade_id}/review", response_model=TradeBlotterReviewResponse)
def review_entry(
    trade_id: str,
    payload: TradeBlotterReviewRequest,
    service: TradeBlotterService = Depends(get_trade_blotter_service),
) -> TradeBlotterReviewResponse:
    return service.review_entry(trade_id, payload)


@router.delete("/trades/{trade_id}", response_model=TradeBlotterDeleteResponse)
@router.delete("/entries/{trade_id}", response_model=TradeBlotterDeleteResponse)
def delete_entry(
    trade_id: str,
    service: TradeBlotterService = Depends(get_trade_blotter_service),
) -> TradeBlotterDeleteResponse:
    return service.delete_entry(trade_id)


@router.post("/from-simulation", response_model=TradeBlotterEntry)
def create_from_simulation(
    payload: TradeBlotterFromSimulationRequest,
    service: TradeBlotterService = Depends(get_trade_blotter_service),
) -> TradeBlotterEntry:
    return service.create_from_simulation(payload)


@router.get("/demo", response_model=TradeBlotterDemoResponse)
def demo(
    service: TradeBlotterService = Depends(get_trade_blotter_service),
) -> TradeBlotterDemoResponse:
    return service.demo()
