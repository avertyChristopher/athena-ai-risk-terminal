from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from app.modules.ai_anomaly_center.schemas import AnomalyCategory, AnomalyRecord, AnomalySeverity


SEVERITY_RANK: dict[str, int] = {"low": 0, "medium": 1, "high": 2, "critical": 3}


def severity_from_score(score: float) -> AnomalySeverity:
    if score >= 76:
        return "critical"
    if score >= 51:
        return "high"
    if score >= 26:
        return "medium"
    return "low"


def score_anomaly(
    *,
    magnitude: float,
    portfolio_impact: float = 0.0,
    recurrence: int = 1,
    data_quality_penalty: float = 0.0,
    critical_rule: bool = False,
) -> tuple[float, AnomalySeverity, str, str]:
    score = min(
        100.0,
        max(0.0, magnitude * 55.0 + portfolio_impact * 25.0 + min(recurrence, 5) * 4.0 + data_quality_penalty),
    )
    if critical_rule:
        score = max(score, 82.0)
    severity = severity_from_score(score)
    confidence = "high" if recurrence >= 2 or score >= 60 else "medium" if score >= 25 else "low"
    explanation = (
        f"Rule-based score {score:.1f}/100 using magnitude, portfolio impact, recurrence, "
        "data quality and critical-rule flags."
    )
    return round(score, 2), severity, confidence, explanation


def build_anomaly(
    *,
    portfolio_id: str | None,
    module_name: str,
    category: AnomalyCategory,
    anomaly_type: str,
    title: str,
    description: str,
    metric_name: str,
    observed_value: Any,
    expected_value: Any | None = None,
    threshold: Any | None = None,
    z_score: float | None = None,
    score: float,
    severity: AnomalySeverity | None = None,
    confidence: str = "medium",
    source_record_id: str | None = None,
    source_payload: dict[str, Any] | None = None,
    suggested_action: str = "Review the source module record and document the outcome.",
    explanation: str | None = None,
) -> AnomalyRecord:
    now = datetime.now(UTC)
    return AnomalyRecord(
        anomaly_id=f"anom_{uuid4().hex[:12]}",
        portfolio_id=portfolio_id,
        module_name=module_name,
        anomaly_type=anomaly_type,
        category=category,
        severity=severity or severity_from_score(score),
        title=title,
        description=description,
        metric_name=metric_name,
        observed_value=observed_value,
        expected_value=expected_value,
        threshold=threshold,
        z_score=z_score,
        anomaly_score=round(score, 2),
        confidence=confidence,  # type: ignore[arg-type]
        source_record_id=source_record_id,
        source_module=module_name,
        source_payload=source_payload or {},
        suggested_action=suggested_action,
        explanation=explanation or "Detected by deterministic Athena rule-based monitoring.",
        generated_by="rule_based_detection",
        detected_at=now,
        updated_at=now,
    )


def severity_at_least(severity: str, threshold: str) -> bool:
    return SEVERITY_RANK.get(severity, 0) >= SEVERITY_RANK.get(threshold, 0)
