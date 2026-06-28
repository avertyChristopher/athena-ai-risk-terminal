from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from uuid import uuid4

from app.modules.reconciliation.schemas import (
    BreakSeverity,
    BreakStatus,
    BreakType,
    OverallStatus,
    ReconciliationBreak,
    ReviewAction,
    ReviewEvent,
    ReviewRequest,
)


def create_break(
    *,
    run_id: str,
    portfolio_id: str,
    break_type: BreakType,
    severity: BreakSeverity,
    metric: str,
    source_module: str,
    explanation: str,
    suggested_action: str,
    symbol: str | None = None,
    internal_value: float | str | None = None,
    external_value: float | str | None = None,
    difference: float | str | None = None,
    tolerance: float | str | None = None,
) -> ReconciliationBreak:
    return ReconciliationBreak(
        break_id=f"brk_{uuid4().hex[:12]}",
        run_id=run_id,
        portfolio_id=portfolio_id,
        break_type=break_type,
        severity=severity,
        symbol=symbol,
        metric=metric,
        internal_value=internal_value,
        external_value=external_value,
        difference=difference,
        tolerance=tolerance,
        source_module=source_module,
        explanation=explanation,
        suggested_action=suggested_action,
    )


def summarize_by_type(breaks: list[ReconciliationBreak]) -> dict[str, int]:
    return dict(Counter(item.break_type for item in breaks))


def summarize_by_severity(breaks: list[ReconciliationBreak]) -> dict[str, int]:
    return dict(Counter(item.severity for item in breaks))


def overall_status_from_breaks(breaks: list[ReconciliationBreak]) -> OverallStatus:
    severities = {item.severity for item in breaks if item.status not in {"resolved", "ignored"}}
    if not severities:
        return "reconciled"
    if "critical" in severities:
        return "critical_breaks"
    if "high" in severities:
        return "material_breaks"
    return "minor_breaks"


def apply_review_action(
    item: ReconciliationBreak,
    request: ReviewRequest,
) -> ReconciliationBreak:
    status_map: dict[ReviewAction, BreakStatus] = {
        "mark_under_review": "under_review",
        "explain": "explained",
        "resolve": "resolved",
        "ignore": "ignored",
        "reopen": "open",
    }
    event = ReviewEvent(
        action=request.action,
        reviewer=request.reviewer,
        note=request.note,
        decision=request.decision,
    )
    return item.model_copy(
        update={
            "status": status_map[request.action],
            "updated_at": datetime.now(UTC),
            "reviewed_by": request.reviewer,
            "review_note": request.note,
            "review_history": [*item.review_history, event],
        },
    )
