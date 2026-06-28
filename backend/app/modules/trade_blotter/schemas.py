from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


TradeBlotterAction = Literal["BUY", "SELL", "SHORT", "COVER", "OPTION", "BOND"]
TradeBlotterStatusValue = Literal[
    "draft",
    "pending_review",
    "approved",
    "rejected",
    "simulated",
    "cancelled",
]
TradeReviewAction = Literal[
    "submit_for_review",
    "approve",
    "reject",
    "simulate",
    "cancel",
    "reopen",
]


class TradeBlotterStatus(BaseModel):
    status: str = "ready"
    module: str = "trade-blotter"
    detail: str
    persistence_enabled: bool = True
    entries_count: int
    review_workflow_enabled: bool = True
    source_modules: list[str]


class TradeReviewEvent(BaseModel):
    action: TradeReviewAction
    from_status: TradeBlotterStatusValue
    to_status: TradeBlotterStatusValue
    reviewer: str
    note: str | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class TradeBlotterEntryCreate(BaseModel):
    portfolio_id: str = Field(default="pf_001", min_length=1)
    symbol: str = Field(min_length=1, max_length=32)
    action: TradeBlotterAction
    quantity: float = Field(gt=0)
    price: float = Field(gt=0)
    currency: str = Field(default="USD", min_length=3, max_length=8)
    status: TradeBlotterStatusValue = "draft"
    trade_date: date = Field(default_factory=lambda: date(2026, 6, 3))
    settlement_date: date | None = None
    source_module: str = "trade_blotter"
    cost_estimate: float = Field(default=0.0, ge=0)
    slippage_estimate: float = Field(default=0.0, ge=0)
    suitability_status: str | None = None
    constraint_status: str | None = None
    risk_summary: dict[str, Any] = Field(default_factory=dict)
    source_payload: dict[str, Any] = Field(default_factory=dict)
    athena_ai_commentary: dict[str, Any] | None = None

    @model_validator(mode="after")
    def normalize_symbol_and_currency(self) -> "TradeBlotterEntryCreate":
        self.symbol = self.symbol.upper()
        self.currency = self.currency.upper()
        return self


class TradeBlotterEntryUpdate(BaseModel):
    portfolio_id: str | None = Field(default=None, min_length=1)
    symbol: str | None = Field(default=None, min_length=1, max_length=32)
    action: TradeBlotterAction | None = None
    quantity: float | None = Field(default=None, gt=0)
    price: float | None = Field(default=None, gt=0)
    currency: str | None = Field(default=None, min_length=3, max_length=8)
    status: TradeBlotterStatusValue | None = None
    trade_date: date | None = None
    settlement_date: date | None = None
    cost_estimate: float | None = Field(default=None, ge=0)
    slippage_estimate: float | None = Field(default=None, ge=0)
    suitability_status: str | None = None
    constraint_status: str | None = None
    risk_summary: dict[str, Any] | None = None
    source_payload: dict[str, Any] | None = None
    athena_ai_commentary: dict[str, Any] | None = None


class TradeBlotterReviewRequest(BaseModel):
    action: TradeReviewAction
    reviewer: str = Field(default="analyst", min_length=1, max_length=120)
    note: str | None = Field(default=None, max_length=1000)


class TradeBlotterEntry(BaseModel):
    trade_id: str
    portfolio_id: str
    symbol: str
    action: TradeBlotterAction
    quantity: float
    price: float
    estimated_trade_value: float
    currency: str = "USD"
    status: TradeBlotterStatusValue
    trade_date: date
    settlement_date: date | None = None
    source_module: str
    cost_estimate: float = 0.0
    slippage_estimate: float = 0.0
    suitability_status: str | None = None
    constraint_status: str | None = None
    risk_summary: dict[str, Any] = Field(default_factory=dict)
    source_payload: dict[str, Any] = Field(default_factory=dict)
    review_history: list[TradeReviewEvent] = Field(default_factory=list)
    athena_ai_commentary: dict[str, Any] | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    reviewed_by: str | None = None
    review_note: str | None = None


class TradeBlotterListResponse(BaseModel):
    status: str = "ready"
    module: str = "trade-blotter"
    total_entries: int
    entries: list[TradeBlotterEntry]


class TradeBlotterReviewResponse(BaseModel):
    entry: TradeBlotterEntry
    event: TradeReviewEvent


class TradeBlotterDeleteResponse(BaseModel):
    deleted: bool
    trade_id: str


class TradeBlotterFromSimulationRequest(BaseModel):
    simulation: dict[str, Any]
    initial_status: TradeBlotterStatusValue = "simulated"
    reviewer: str = "trade_simulator"
    note: str | None = "Saved from Trade Simulator simulation."


class TradeBlotterDemoResponse(BaseModel):
    status: str = "ready"
    module: str = "trade-blotter"
    entries: list[TradeBlotterEntry]
