from __future__ import annotations

from collections import Counter
from typing import Any

from app.modules.ai_anomaly_center.domain.anomaly_scoring import build_anomaly
from app.modules.ai_anomaly_center.schemas import AnomalyRecord


def detect_limit_anomalies(context: dict[str, Any], portfolio_id: str | None) -> list[AnomalyRecord]:
    breaches = context.get("limit_breaches") or []
    records: list[AnomalyRecord] = []
    open_count = sum(1 for breach in breaches if str(breach.get("status") or "").lower() == "open")
    rule_counts = Counter(str(breach.get("rule_id") or breach.get("rule_name") or "unknown") for breach in breaches)
    for breach in breaches:
        breach_id = str(breach.get("breach_id") or "")
        severity = str(breach.get("severity") or "").lower()
        status = str(breach.get("status") or "").lower()
        if severity == "critical":
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id or breach.get("portfolio_id"),
                    module_name="Limit Center",
                    category="limits",
                    anomaly_type="critical_limit_breach",
                    title="Critical limit breach",
                    description=str(breach.get("explanation") or "Critical governance breach detected."),
                    metric_name=str(breach.get("metric_key") or "limit"),
                    observed_value=breach.get("current_value"),
                    threshold=breach.get("limit_value"),
                    score=88,
                    source_record_id=breach_id,
                    source_payload=breach,
                    suggested_action="Escalate governance review and document remediation or exception.",
                ),
            )
        if status == "approved_exception" and not breach.get("review_note"):
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id or breach.get("portfolio_id"),
                    module_name="Limit Center",
                    category="limits",
                    anomaly_type="exception_without_note",
                    title="Limit exception lacks review note",
                    description="A breach was approved as exception without a review note.",
                    metric_name="review_note",
                    observed_value=None,
                    threshold="required",
                    score=42,
                    source_record_id=breach_id,
                    source_payload=breach,
                    suggested_action="Add exception rationale and reviewer evidence.",
                ),
            )
    if open_count > 3:
        records.append(
            build_anomaly(
                portfolio_id=portfolio_id,
                module_name="Limit Center",
                category="limits",
                anomaly_type="open_breach_cluster",
                title="Cluster of open limit breaches",
                description=f"{open_count} open limit breaches were detected.",
                metric_name="open_breach_count",
                observed_value=open_count,
                threshold=3,
                score=66,
                suggested_action="Prioritize governance queue and resolve or explain breaches.",
            ),
        )
    for rule, count in rule_counts.items():
        if count >= 3:
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id,
                    module_name="Limit Center",
                    category="limits",
                    anomaly_type="repeated_limit_breach",
                    title=f"Repeated limit breach: {rule}",
                    description=f"{count} breaches map to the same rule.",
                    metric_name="rule_breach_count",
                    observed_value=count,
                    threshold=3,
                    score=57,
                    suggested_action="Review whether the limit is structurally breached or needs portfolio action.",
                ),
            )
    return records
