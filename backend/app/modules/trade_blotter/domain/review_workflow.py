from __future__ import annotations

from datetime import UTC, datetime

from app.modules.trade_blotter.domain.trade_status import next_status
from app.modules.trade_blotter.schemas import (
    TradeBlotterEntry,
    TradeBlotterReviewRequest,
    TradeReviewEvent,
)


def apply_review_action(
    entry: TradeBlotterEntry,
    request: TradeBlotterReviewRequest,
) -> tuple[TradeBlotterEntry, TradeReviewEvent]:
    to_status = next_status(entry.status, request.action)
    event = TradeReviewEvent(
        action=request.action,
        from_status=entry.status,
        to_status=to_status,
        reviewer=request.reviewer,
        note=request.note,
        timestamp=datetime.now(UTC),
    )
    updated = entry.model_copy(deep=True)
    updated.status = to_status
    updated.updated_at = event.timestamp
    updated.reviewed_by = request.reviewer
    updated.review_note = request.note
    updated.review_history.append(event)
    return updated, event
