from __future__ import annotations

from typing import Any


def calculate_realized_pnl_for_symbol(
    symbol: str,
    transactions: list[dict[str, Any]],
    fallback_cost_basis: float,
) -> float:
    realized = 0.0
    for trade in transactions:
        if str(trade.get("symbol", "")).upper() != symbol.upper():
            continue
        action = str(trade.get("action") or trade.get("side") or "").upper()
        if action != "SELL":
            continue
        quantity = _as_float(trade.get("quantity")) or 0.0
        price = _as_float(trade.get("price") or trade.get("execution_price")) or 0.0
        cost_basis = _as_float(trade.get("cost_basis") or trade.get("average_price"))
        if cost_basis is None:
            cost_basis = fallback_cost_basis
        realized += (price - cost_basis) * quantity
    return realized


def split_realized_unrealized(price_pnl: float, realized_pnl: float) -> tuple[float, float]:
    return realized_pnl, price_pnl - realized_pnl


def _as_float(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
