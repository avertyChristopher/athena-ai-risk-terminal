from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


AthenaModuleName = Literal[
    "portfolio_builder",
    "risk_monitor",
    "volatility_lab",
    "options_pricing_lab",
    "rates_lab",
    "trade_simulator",
    "market_data",
    "equity_analysis",
    "limit_center",
]
AthenaAnalysisMode = Literal[
    "portfolio",
    "symbol",
    "trade",
    "options",
    "rates",
    "risk",
    "limit",
]
AthenaLanguage = Literal["en", "fr"]
AthenaStyle = Literal["concise", "professional", "educational", "executive"]
AthenaConfidence = Literal["low", "medium", "high"]
AthenaGeneratedBy = Literal["ai_provider", "deterministic_fallback"]


class AthenaIntelligenceStatus(BaseModel):
    status: str = "ready"
    module: str = "athena-intelligence"
    detail: str
    provider_mode: str
    provider_available: bool
    model: str | None = None
    fallback_enabled: bool = True
    safety_rules: list[str] = Field(default_factory=list)


class AthenaIntelligenceRequest(BaseModel):
    module_name: AthenaModuleName
    analysis_mode: AthenaAnalysisMode
    language: AthenaLanguage = "en"
    payload: dict[str, Any] = Field(default_factory=dict)
    style: AthenaStyle = "professional"
    max_points: int = Field(default=5, ge=1, le=10)


class AthenaAICommentary(BaseModel):
    summary: str
    main_risks: list[str] = Field(default_factory=list)
    risk_drivers: list[str] = Field(default_factory=list)
    breaches: list[str] = Field(default_factory=list)
    suggested_actions: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    confidence_level: AthenaConfidence = "medium"
    generated_by: AthenaGeneratedBy = "deterministic_fallback"
    source_modules: list[str] = Field(default_factory=list)
    disclaimer: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class AthenaRiskSynthesisPayloads(BaseModel):
    risk_analytics_payload: dict[str, Any] | None = None
    options_risk_payload: dict[str, Any] | None = None
    rates_risk_payload: dict[str, Any] | None = None
    trade_impact_payload: dict[str, Any] | None = None
    portfolio_payload: dict[str, Any] | None = None
    market_data_payload: dict[str, Any] | None = None


class AthenaRiskSynthesisRequest(BaseModel):
    portfolio_id: str = Field(min_length=1)
    language: AthenaLanguage = "en"
    payloads: AthenaRiskSynthesisPayloads = Field(
        default_factory=AthenaRiskSynthesisPayloads,
    )
    style: AthenaStyle = "executive"
    max_points: int = Field(default=6, ge=1, le=10)


class AthenaRiskSynthesisResponse(BaseModel):
    executive_summary: str
    overall_risk_level: str
    top_risk_drivers: list[str] = Field(default_factory=list)
    cross_module_findings: list[str] = Field(default_factory=list)
    breached_limits: list[str] = Field(default_factory=list)
    portfolio_vulnerabilities: list[str] = Field(default_factory=list)
    suggested_next_actions: list[str] = Field(default_factory=list)
    module_specific_notes: dict[str, list[str]] = Field(default_factory=dict)
    assumptions: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    generated_by: AthenaGeneratedBy = "deterministic_fallback"
    disclaimer: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class AthenaMetricExplanationRequest(BaseModel):
    metric_name: str = Field(min_length=1)
    metric_value: float | str | None = None
    module_name: AthenaModuleName
    context: dict[str, Any] = Field(default_factory=dict)
    language: AthenaLanguage = "en"


class AthenaMetricExplanationResponse(BaseModel):
    explanation: str
    interpretation: str
    risk_meaning: str
    limitations: list[str] = Field(default_factory=list)
    cfa_note: str | None = None
    disclaimer: str
    generated_by: AthenaGeneratedBy = "deterministic_fallback"
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
