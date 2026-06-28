from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


DemoLanguage = Literal["en", "fr"]
PersistenceStatus = Literal["persistent_history", "sqlite_demo", "in_memory_fallback", "not_persisted"]


class DemoRunRequest(BaseModel):
    portfolio_id: str = Field(default="pf_004", min_length=1)
    language: DemoLanguage = "en"
    include_report: bool = True


class DemoModuleRun(BaseModel):
    module: str
    status: Literal["completed", "warning", "failed"]
    detail: str
    records_created: int = 0
    output_id: str | None = None


class DemoPersistenceItem(BaseModel):
    object_name: str
    module: str
    status: PersistenceStatus
    storage: str
    notes: str


class DemoWorkflowStatus(BaseModel):
    status: str = "ready"
    module: str = "demo-workflow"
    detail: str
    demo_portfolio_id: str = "pf_004"
    active_modules: int = 16
    database_connected: bool = True
    persistence: list[DemoPersistenceItem]
    endpoints: list[str]
    limitations: list[str]


class DemoRunSummary(BaseModel):
    demo_run_id: str
    portfolio_id: str
    portfolio_name: str | None = None
    modules_run: list[str]
    module_results: list[DemoModuleRun]
    records_created: dict[str, int]
    warnings: list[str] = Field(default_factory=list)
    generated_report_id: str | None = None
    highest_risk_status: str | None = None
    open_breaks: int | None = None
    limit_breaches: int | None = None
    anomalies_detected: int | None = None
    total_pnl: float | None = None
    risk_score: int | None = None
    quick_links: dict[str, str]
    persistence: list[DemoPersistenceItem]
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class DemoRunHistoryResponse(BaseModel):
    status: str = "ready"
    module: str = "demo-workflow"
    total_runs: int
    items: list[DemoRunSummary]
