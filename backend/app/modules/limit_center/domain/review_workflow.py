from __future__ import annotations

from datetime import UTC, datetime

from app.modules.limit_center.schemas import (
    BreachReviewEvent,
    BreachStatus,
    ReviewAction,
)


TRANSITIONS: dict[BreachStatus, dict[ReviewAction, BreachStatus]] = {
    "open": {
        "mark_under_review": "under_review",
        "resolve": "resolved",
    },
    "under_review": {
        "approve_exception": "approved_exception",
        "reject": "rejected",
        "resolve": "resolved",
        "reopen": "open",
    },
    "approved_exception": {
        "resolve": "resolved",
        "reopen": "open",
    },
    "rejected": {
        "mark_under_review": "under_review",
        "resolve": "resolved",
        "reopen": "open",
    },
    "resolved": {
        "reopen": "open",
    },
}


def apply_review_action(
    current_status: BreachStatus,
    action: ReviewAction,
    reviewer: str,
    note: str | None = None,
) -> BreachReviewEvent:
    next_status = TRANSITIONS.get(current_status, {}).get(action)
    if next_status is None:
        raise ValueError(f"Action '{action}' is not valid from status '{current_status}'.")
    return BreachReviewEvent(
        action=action,
        from_status=current_status,
        to_status=next_status,
        reviewer=reviewer,
        note=note,
        decision=_decision_label(action, next_status),
        timestamp=datetime.now(UTC),
    )


def _decision_label(action: ReviewAction, next_status: BreachStatus) -> str:
    labels = {
        "mark_under_review": "Breach moved under review.",
        "approve_exception": "Temporary exception approved.",
        "reject": "Exception rejected.",
        "resolve": "Breach marked resolved.",
        "reopen": "Breach reopened for review.",
    }
    return labels.get(action, f"Breach moved to {next_status}.")
