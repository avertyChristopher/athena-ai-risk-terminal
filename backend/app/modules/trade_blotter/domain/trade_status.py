from __future__ import annotations

from app.modules.trade_blotter.schemas import TradeBlotterStatusValue, TradeReviewAction


TRANSITIONS: dict[TradeBlotterStatusValue, dict[TradeReviewAction, TradeBlotterStatusValue]] = {
    "draft": {
        "submit_for_review": "pending_review",
        "approve": "approved",
        "reject": "rejected",
        "simulate": "simulated",
        "cancel": "cancelled",
    },
    "simulated": {
        "submit_for_review": "pending_review",
        "approve": "approved",
        "reject": "rejected",
        "cancel": "cancelled",
        "reopen": "draft",
    },
    "pending_review": {
        "approve": "approved",
        "reject": "rejected",
        "cancel": "cancelled",
        "reopen": "draft",
    },
    "approved": {
        "cancel": "cancelled",
        "reopen": "pending_review",
    },
    "rejected": {
        "reopen": "draft",
    },
    "cancelled": {
        "reopen": "draft",
    },
}


def next_status(
    current_status: TradeBlotterStatusValue,
    action: TradeReviewAction,
) -> TradeBlotterStatusValue:
    transition = TRANSITIONS.get(current_status, {}).get(action)
    if transition is None:
        raise ValueError(f"Cannot apply review action '{action}' from status '{current_status}'.")
    return transition
