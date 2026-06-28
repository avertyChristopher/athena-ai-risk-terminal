from __future__ import annotations

from datetime import UTC, datetime

from app.modules.ai_anomaly_center.domain.anomaly_scoring import SEVERITY_RANK
from app.modules.ai_anomaly_center.schemas import (
    AnomalyRecord,
    AnomalyReviewAction,
    AnomalyReviewEvent,
    AnomalyReviewRequest,
    AnomalyStatus,
)


TRANSITIONS: dict[AnomalyStatus, dict[AnomalyReviewAction, AnomalyStatus]] = {
    "open": {
        "mark_under_review": "under_review",
        "explain": "explained",
        "resolve": "resolved",
        "ignore": "ignored",
    },
    "under_review": {
        "explain": "explained",
        "resolve": "resolved",
        "ignore": "ignored",
        "reopen": "open",
    },
    "explained": {
        "resolve": "resolved",
        "ignore": "ignored",
        "reopen": "open",
    },
    "resolved": {"reopen": "open"},
    "ignored": {"reopen": "open"},
}


def apply_review_action(
    anomaly: AnomalyRecord,
    request: AnomalyReviewRequest,
) -> tuple[AnomalyRecord, AnomalyReviewEvent]:
    to_status = TRANSITIONS.get(anomaly.status, {}).get(request.action)
    if to_status is None:
        raise ValueError(f"Cannot apply review action '{request.action}' from status '{anomaly.status}'.")
    event = AnomalyReviewEvent(
        action=request.action,
        from_status=anomaly.status,
        to_status=to_status,
        reviewer=request.reviewer,
        note=request.note,
        decision=request.decision,
        timestamp=datetime.now(UTC),
    )
    updated = anomaly.model_copy(deep=True)
    updated.status = to_status
    updated.updated_at = event.timestamp
    updated.review_history.append(event)
    return updated, event


def filter_by_severity(records: list[AnomalyRecord], threshold: str) -> list[AnomalyRecord]:
    minimum = SEVERITY_RANK.get(threshold, 0)
    return [record for record in records if SEVERITY_RANK.get(record.severity, 0) >= minimum]


def highest_severity(records: list[AnomalyRecord]) -> str | None:
    if not records:
        return None
    return max(records, key=lambda record: SEVERITY_RANK.get(record.severity, 0)).severity


def count_by(records: list[AnomalyRecord], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        value = str(getattr(record, field))
        counts[value] = counts.get(value, 0) + 1
    return counts
