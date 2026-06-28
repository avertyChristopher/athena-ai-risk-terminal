from __future__ import annotations

from typing import Any


def estimated_trade_value(quantity: float, price: float) -> float:
    return round(abs(quantity * price), 6)


def normalize_trade_payload(payload: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(payload)
    if "symbol" in normalized and normalized["symbol"] is not None:
        normalized["symbol"] = str(normalized["symbol"]).upper()
    if "currency" in normalized and normalized["currency"] is not None:
        normalized["currency"] = str(normalized["currency"]).upper()
    if "action" in normalized and normalized["action"] is not None:
        normalized["action"] = str(normalized["action"]).upper()
    return normalized
