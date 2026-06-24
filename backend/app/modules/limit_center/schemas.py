from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

from app.modules.athena_intelligence.schemas import AthenaAICommentary


ComparisonOperator = Literal[
    "greater_than",
    "greater_than_or_equal",
    "less_than",
    "less_than_or_equal",
    "equal",
    "not_equal",
]
LimitSeverity = Literal["low", "medium", "high", "critical"]
LimitCategory = Literal[
    "portfolio",
    "risk",
    "stress",
    "fixed_income",
    "options",
    "trade",
]
LimitSourceModule = Literal[
    "portfolio_builder",
    "risk_monitor",
    "volatility_lab",
    "options_pricing_lab",
    "rates_lab",
    "stress_testing",
    "trade_simulator",
    "limit_center",
]
BreachStatus = Literal[
    "open",
    "under_review",
    "approved_exception",
    "rejected",
    "resolved",
]
ReviewAction = Literal[
    "mark_under_review",
    "approve_exception",
    "reject",
    "resolve",
    "reopen",
]
OverallLimitStatus = Literal[
    "within_limits",
    "watchlist",
    "breached",
    "severe_breach",
    "critical_breach",
]


class LimitCenterStatus(BaseModel):
    status: str = "ready"
    module: str = "limit-center"
    detail: str
    engines_available: list[str]
    active_rules: int
    supported_source_modules: list[str]


class LimitRule(BaseModel):
    rule_id: str
    name: str = Field(min_length=1, max_length=160)
    category: LimitCategory
    metric_key: str = Field(min_length=1, max_length=120)
    limit_value: float | bool
    comparison_operator: ComparisonOperator
    severity_if_breached: LimitSeverity
    enabled: bool = True
    description: str
    source_modules: list[LimitSourceModule]
    methodology: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class LimitRuleCreate(BaseModel):
    rule_id: str | None = Field(default=None, min_length=1, max_length=80)
    name: str = Field(min_length=1, max_length=160)
    category: LimitCategory
    metric_key: str = Field(min_length=1, max_length=120)
    limit_value: float | bool
    comparison_operator: ComparisonOperator
    severity_if_breached: LimitSeverity = "medium"
    enabled: bool = True
    description: str = Field(default="User-defined risk governance limit.")
    source_modules: list[LimitSourceModule] = Field(default_factory=list)
    methodology: str = "User-defined rule evaluated against structured module payloads."


class LimitRuleUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=160)
    category: LimitCategory | None = None
    metric_key: str | None = Field(default=None, min_length=1, max_length=120)
    limit_value: float | bool | None = None
    comparison_operator: ComparisonOperator | None = None
    severity_if_breached: LimitSeverity | None = None
    enabled: bool | None = None
    description: str | None = None
    source_modules: list[LimitSourceModule] | None = None
    methodology: str | None = None


class LimitRuleListResponse(BaseModel):
    total_rules: int
    active_rules: int
    rules: list[LimitRule]


class EvaluatedLimitRule(BaseModel):
    rule_id: str
    rule_name: str
    category: LimitCategory
    source_module: LimitSourceModule
    metric_key: str
    current_value: float | bool | None
    limit_value: float | bool
    comparison_operator: ComparisonOperator
    breached: bool
    severity: LimitSeverity | None = None
    enabled: bool
    warning: str | None = None


class BreachReviewEvent(BaseModel):
    action: ReviewAction
    from_status: BreachStatus
    to_status: BreachStatus
    reviewer: str
    note: str | None = None
    decision: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class LimitBreach(BaseModel):
    breach_id: str
    rule_id: str
    rule_name: str
    portfolio_id: str
    source_module: LimitSourceModule
    metric_key: str
    current_value: float | bool
    limit_value: float | bool
    comparison_operator: ComparisonOperator
    severity: LimitSeverity
    status: BreachStatus = "open"
    explanation: str
    suggested_action: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    reviewed_by: str | None = None
    review_note: str | None = None
    review_history: list[BreachReviewEvent] = Field(default_factory=list)


class LimitEvaluationSummary(BaseModel):
    portfolio_id: str
    source_module: LimitSourceModule
    evaluated_rule_count: int
    breach_count: int
    open_breach_count: int
    critical_breach_count: int
    highest_severity: LimitSeverity | None
    overall_status: OverallLimitStatus
    source_modules: list[LimitSourceModule]


class LimitEvaluationRequest(BaseModel):
    portfolio_id: str = Field(default="pf_001", min_length=1)
    source_module: LimitSourceModule
    payload: dict[str, Any] = Field(default_factory=dict)
    ruleset: list[LimitRule] | None = None
    language: Literal["en", "fr"] = "en"


class LimitEvaluationResponse(BaseModel):
    portfolio_id: str
    source_module: LimitSourceModule
    evaluated_rules: list[EvaluatedLimitRule]
    breaches: list[LimitBreach]
    warnings: list[str]
    summary: LimitEvaluationSummary
    highest_severity: LimitSeverity | None
    overall_status: OverallLimitStatus
    athena_ai_commentary: AthenaAICommentary
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class BreachListResponse(BaseModel):
    total_breaches: int
    open_breaches: int
    critical_breaches: int
    approved_exceptions: int
    resolved_breaches: int
    breaches: list[LimitBreach]


class BreachReviewRequest(BaseModel):
    action: ReviewAction
    reviewer: str = Field(min_length=1, max_length=120)
    note: str | None = Field(default=None, max_length=1000)


class BreachReviewResponse(BaseModel):
    breach: LimitBreach
    event: BreachReviewEvent


class SourceModuleCard(BaseModel):
    module: LimitSourceModule
    display_name: str
    connected: bool
    payload_available: bool
    metrics_provided: list[str]
    last_evaluated: datetime | None = None
    warnings: list[str] = Field(default_factory=list)
