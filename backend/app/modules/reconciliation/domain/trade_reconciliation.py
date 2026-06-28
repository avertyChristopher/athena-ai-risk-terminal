from __future__ import annotations

from typing import Any

from app.modules.reconciliation.domain.break_classification import create_break
from app.modules.reconciliation.schemas import ReconciliationBreak, TradeReconciliationItem


def reconcile_trades(
    *,
    run_id: str,
    portfolio_id: str,
    internal_trades: list[dict[str, Any]],
    external_trades: list[dict[str, Any]],
) -> tuple[list[TradeReconciliationItem], list[ReconciliationBreak], list[str]]:
    warnings = []
    rows: list[TradeReconciliationItem] = []
    breaks: list[ReconciliationBreak] = []
    internal_by_id = {_trade_id(trade): trade for trade in internal_trades}
    external_by_id = {_trade_id(trade): trade for trade in external_trades}
    if not internal_by_id and not external_by_id:
        warnings.append("No internal or external trades available for reconciliation.")
        return rows, breaks, warnings
    if not internal_by_id:
        warnings.append("No internal Trade Blotter or portfolio trades found for reconciliation.")
    if not external_by_id:
        warnings.append("No external pending trades found in the demo custodian reference.")
    for trade_id in sorted(set(internal_by_id) | set(external_by_id)):
        internal = internal_by_id.get(trade_id)
        external = external_by_id.get(trade_id)
        source = internal or external or {}
        symbol = str(source.get("symbol", "")).upper()
        action = str(source.get("action") or source.get("side") or "UNKNOWN").upper()
        quantity = _as_float(source.get("quantity")) or 0.0
        internal_value = _trade_value(internal)
        external_value = _trade_value(external)
        if internal is None:
            status = "missing_internal_trade"
            severity = "medium"
            explanation = f"{trade_id} exists externally but not in Athena transaction history."
        elif external is None:
            status = "missing_external_trade"
            severity = "medium"
            explanation = f"{trade_id} exists internally but is not reflected in the external reference."
        elif abs((_as_float(internal.get("quantity")) or 0.0) - (_as_float(external.get("quantity")) or 0.0)) > 0.0001:
            status = "quantity_mismatch"
            severity = "medium"
            explanation = f"{trade_id} trade quantity differs between Athena and external reference."
        elif _settlement_date(internal) and _settlement_date(external) and _settlement_date(internal) != _settlement_date(external):
            status = "settlement_date_mismatch"
            severity = "medium"
            explanation = f"{trade_id} settlement date differs between Athena and external reference."
        elif abs((internal_value or 0.0) - (external_value or 0.0)) > 50.0:
            status = "cost_or_value_mismatch"
            severity = "medium"
            explanation = f"{trade_id} trade value differs beyond tolerance."
        else:
            status = "matched"
            severity = None
            explanation = f"{trade_id} trade reconciles."
        rows.append(
            TradeReconciliationItem(
                trade_id=trade_id,
                symbol=symbol,
                action=action,
                quantity=quantity,
                internal_trade_value=internal_value,
                external_trade_value=external_value,
                status=status,
                severity=severity,
                explanation=explanation,
            ),
        )
        if severity is not None:
            breaks.append(
                create_break(
                    run_id=run_id,
                    portfolio_id=portfolio_id,
                    break_type="trade",
                    severity=severity,
                    symbol=symbol,
                    metric="trade_value",
                    internal_value=internal_value,
                    external_value=external_value,
                    difference=(internal_value or 0.0) - (external_value or 0.0),
                    tolerance=50.0,
                    source_module="Trade Simulator",
                    explanation=explanation,
                    suggested_action="Review trade settlement timing, costs and pending external trades.",
                ),
            )
    return rows, breaks, warnings


def _trade_id(trade: dict[str, Any]) -> str:
    return str(trade.get("trade_id") or trade.get("id") or f"{trade.get('symbol')}-{trade.get('action')}-{trade.get('quantity')}")


def _trade_value(trade: dict[str, Any] | None) -> float | None:
    if trade is None:
        return None
    quantity = _as_float(trade.get("quantity")) or 0.0
    price = _as_float(trade.get("price") or trade.get("execution_price") or trade.get("estimated_price")) or 0.0
    cost = _as_float(trade.get("cost") or trade.get("commission")) or 0.0
    return quantity * price + cost


def _settlement_date(trade: dict[str, Any] | None) -> str | None:
    if trade is None:
        return None
    value = trade.get("settlement_date") or trade.get("settle_date")
    return str(value)[:10] if value else None


def _as_float(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
