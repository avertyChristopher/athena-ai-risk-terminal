from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


ExternalSource = Literal["demo_custodian", "uploaded_file_placeholder", "manual_reference"]
CheckType = Literal["positions", "cash", "prices", "trades", "pnl", "fx"]
BreakType = Literal["position", "cash", "price", "trade", "pnl", "fx", "data_quality"]
BreakSeverity = Literal["low", "medium", "high", "critical"]
BreakStatus = Literal["open", "under_review", "explained", "resolved", "ignored"]
OverallStatus = Literal["reconciled", "minor_breaks", "material_breaks", "critical_breaks"]
ReviewAction = Literal["mark_under_review", "explain", "resolve", "ignore", "reopen"]
ReconLanguage = Literal["en", "fr"]


class ReconciliationTolerance(BaseModel):
    position_quantity_tolerance: float = Field(default=0.0001, ge=0)
    market_value_tolerance: float = Field(default=50.0, ge=0)
    cash_tolerance: float = Field(default=100.0, ge=0)
    price_tolerance_bps: float = Field(default=10.0, ge=0)
    pnl_tolerance: float = Field(default=250.0, ge=0)


class ReconciliationRequest(BaseModel):
    portfolio_id: str = Field(default="pf_001", min_length=1)
    reconciliation_date: date = date(2026, 6, 3)
    external_source: ExternalSource = "demo_custodian"
    checks: list[CheckType] = Field(default_factory=lambda: ["positions", "cash", "prices", "trades", "pnl", "fx"])
    tolerance: ReconciliationTolerance = Field(default_factory=ReconciliationTolerance)
    language: ReconLanguage = "en"


class ReviewRequest(BaseModel):
    action: ReviewAction
    reviewer: str = Field(default="analyst", min_length=1)
    note: str | None = None
    decision: str | None = None


class ReviewEvent(BaseModel):
    action: ReviewAction
    reviewer: str
    note: str | None = None
    decision: str | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ReconciliationBreak(BaseModel):
    break_id: str
    run_id: str
    portfolio_id: str
    break_type: BreakType
    severity: BreakSeverity
    status: BreakStatus = "open"
    symbol: str | None = None
    metric: str
    internal_value: float | str | None = None
    external_value: float | str | None = None
    difference: float | str | None = None
    tolerance: float | str | None = None
    source_module: str
    explanation: str
    suggested_action: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    reviewed_by: str | None = None
    review_note: str | None = None
    review_history: list[ReviewEvent] = Field(default_factory=list)


class PositionReconciliationItem(BaseModel):
    symbol: str
    internal_quantity: float | None
    external_quantity: float | None
    quantity_difference: float | None
    internal_market_value: float | None
    external_market_value: float | None
    market_value_difference: float | None
    difference_percent: float | None
    tolerance: float
    status: str
    severity: BreakSeverity | None = None
    explanation: str


class CashReconciliationItem(BaseModel):
    internal_cash: float | None
    external_cash: float | None
    cash_difference: float | None
    cash_difference_percent: float | None
    currency: str
    tolerance: float
    status: str
    severity: BreakSeverity | None = None
    explanation: str


class PriceReconciliationItem(BaseModel):
    symbol: str
    internal_price: float | None
    external_price: float | None
    price_difference: float | None
    price_difference_bps: float | None
    internal_price_timestamp: str | None
    external_price_timestamp: str | None
    tolerance_bps: float
    status: str
    severity: BreakSeverity | None = None
    explanation: str


class TradeReconciliationItem(BaseModel):
    trade_id: str
    symbol: str
    action: str
    quantity: float
    internal_trade_value: float | None
    external_trade_value: float | None
    status: str
    severity: BreakSeverity | None = None
    explanation: str


class PnlReconciliationItem(BaseModel):
    internal_total_pnl: float | None
    external_total_pnl: float | None
    pnl_difference: float | None
    pnl_difference_percent: float | None
    tolerance: float
    unexplained_pnl: float | None
    status: str
    severity: BreakSeverity | None = None
    explanation: str


class FxReconciliationItem(BaseModel):
    currency: str
    internal_fx_rate: float | None
    external_fx_rate: float | None
    fx_difference: float | None
    translation_difference: float | None
    status: str
    severity: BreakSeverity | None = None
    explanation: str


class ReconciliationMethodology(BaseModel):
    checks_performed: list[CheckType]
    tolerances: ReconciliationTolerance
    data_sources: list[str]
    assumptions: list[str]
    limitations: list[str]


class ReconciliationRunResult(BaseModel):
    run_id: str
    portfolio_id: str
    portfolio_name: str
    reconciliation_date: date
    external_source: ExternalSource
    overall_status: OverallStatus
    total_breaks: int
    open_breaks: int
    critical_breaks: int
    breaks_by_type: dict[str, int]
    breaks_by_severity: dict[str, int]
    checks_performed: list[CheckType]
    position_breaks: list[PositionReconciliationItem] = Field(default_factory=list)
    cash_breaks: list[CashReconciliationItem] = Field(default_factory=list)
    price_breaks: list[PriceReconciliationItem] = Field(default_factory=list)
    trade_breaks: list[TradeReconciliationItem] = Field(default_factory=list)
    pnl_breaks: list[PnlReconciliationItem] = Field(default_factory=list)
    fx_breaks: list[FxReconciliationItem] = Field(default_factory=list)
    breaks: list[ReconciliationBreak] = Field(default_factory=list)
    unresolved_items: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    methodology: ReconciliationMethodology
    limitations: list[str] = Field(default_factory=list)
    athena_ai_commentary: dict[str, Any] | None = None
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ReconciliationStatus(BaseModel):
    status: str = "ready"
    module: str = "reconciliation"
    detail: str
    checks_available: list[CheckType]
    source_modules: list[str]
    external_sources: list[ExternalSource]
    history_enabled: bool = True
    review_workflow_enabled: bool = True
    export_formats: list[str] = Field(default_factory=lambda: ["json", "csv"])


class ReconciliationHistoryItem(BaseModel):
    run_id: str
    portfolio_id: str
    portfolio_name: str
    reconciliation_date: date
    external_source: ExternalSource
    overall_status: OverallStatus
    total_breaks: int
    critical_breaks: int
    generated_at: datetime


class ReconciliationHistoryResponse(BaseModel):
    status: str = "ready"
    module: str = "reconciliation"
    total_runs: int
    items: list[ReconciliationHistoryItem]


class BreakRegisterResponse(BaseModel):
    status: str = "ready"
    module: str = "reconciliation"
    total_breaks: int
    items: list[ReconciliationBreak]


class ReconciliationDeleteResponse(BaseModel):
    deleted: bool
    run_id: str


class ReconciliationCsvExportResponse(BaseModel):
    run_id: str
    content_type: str = "text/csv"
    csv: str
    included_tables: list[str]
