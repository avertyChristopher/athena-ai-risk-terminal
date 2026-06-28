from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

from app.modules.athena_intelligence.schemas import AthenaAICommentary


AnomalySeverity = Literal["low", "medium", "high", "critical"]
AnomalyStatus = Literal["open", "under_review", "explained", "resolved", "ignored"]
AnomalyCategory = Literal[
    "market_data",
    "portfolio",
    "trades",
    "pnl",
    "risk",
    "reconciliation",
    "limits",
    "stress",
    "rates_options",
]
AnomalyScanScope = Literal[
    "all",
    "market_data",
    "portfolio",
    "trades",
    "pnl",
    "risk",
    "reconciliation",
    "limits",
    "stress",
    "rates_options",
]
AnomalyReviewAction = Literal["mark_under_review", "explain", "resolve", "ignore", "reopen"]
AnomalyConfidence = Literal["low", "medium", "high"]
AnomalyLanguage = Literal["en", "fr"]


class AIAnomalyCenterStatus(BaseModel):
    status: str = "ready"
    module: str = "ai-anomaly-center"
    detail: str
    detection_mode: str = "deterministic_rule_based"
    persistence_enabled: bool = True
    review_workflow_enabled: bool = True
    categories: list[AnomalyCategory]
    source_modules: list[str]
    limitations: list[str]


class AnomalyReviewEvent(BaseModel):
    action: AnomalyReviewAction
    from_status: AnomalyStatus
    to_status: AnomalyStatus
    reviewer: str
    note: str | None = None
    decision: str | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class AnomalyRecord(BaseModel):
    anomaly_id: str
    portfolio_id: str | None = None
    module_name: str
    anomaly_type: str
    category: AnomalyCategory
    severity: AnomalySeverity
    status: AnomalyStatus = "open"
    title: str
    description: str
    metric_name: str
    observed_value: Any
    expected_value: Any | None = None
    threshold: Any | None = None
    z_score: float | None = None
    anomaly_score: float = Field(default=0.0, ge=0, le=100)
    confidence: AnomalyConfidence = "medium"
    source_record_id: str | None = None
    source_module: str
    source_payload: dict[str, Any] = Field(default_factory=dict)
    suggested_action: str
    explanation: str
    review_history: list[AnomalyReviewEvent] = Field(default_factory=list)
    generated_by: str = "rule_based_detection"
    detected_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class AnomalyScanRequest(BaseModel):
    portfolio_id: str | None = Field(default="pf_001", min_length=1)
    scan_scope: AnomalyScanScope = "all"
    lookback_days: int = Field(default=30, ge=1, le=365)
    severity_threshold: AnomalySeverity = "low"
    persist_results: bool = True
    language: AnomalyLanguage = "en"


class AnomalyMethodology(BaseModel):
    detection_mode: str
    score_mapping: dict[str, str]
    factors: list[str]
    data_sources: list[str]
    limitations: list[str]


class AnomalyScanResponse(BaseModel):
    scan_id: str
    portfolio_id: str | None
    scan_scope: AnomalyScanScope
    lookback_days: int
    total_records_scanned: int
    anomalies_detected: int
    anomalies_by_category: dict[str, int]
    anomalies_by_severity: dict[str, int]
    highest_severity: AnomalySeverity | None
    anomaly_records: list[AnomalyRecord]
    warnings: list[str] = Field(default_factory=list)
    methodology: AnomalyMethodology
    limitations: list[str] = Field(default_factory=list)
    athena_ai_commentary: AthenaAICommentary | None = None
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class AnomalyListResponse(BaseModel):
    status: str = "ready"
    module: str = "ai-anomaly-center"
    total_anomalies: int
    items: list[AnomalyRecord]


class AnomalyReviewRequest(BaseModel):
    action: AnomalyReviewAction
    reviewer: str = Field(default="analyst", min_length=1, max_length=120)
    note: str | None = Field(default=None, max_length=1000)
    decision: str | None = Field(default=None, max_length=1000)


class AnomalyReviewResponse(BaseModel):
    anomaly: AnomalyRecord
    event: AnomalyReviewEvent


class AnomalyDeleteResponse(BaseModel):
    deleted: bool
    anomaly_id: str


class AnomalyHistoryResponse(BaseModel):
    status: str = "ready"
    module: str = "ai-anomaly-center"
    recent_count: int
    items: list[AnomalyRecord]


class AnomalyCsvExportResponse(BaseModel):
    content_type: str = "text/csv"
    csv: str
    included_tables: list[str]
