from __future__ import annotations

from typing import Any

from app.modules.reconciliation.domain.break_classification import create_break
from app.modules.reconciliation.domain.severity import classify_position_severity
from app.modules.reconciliation.schemas import (
    PositionReconciliationItem,
    ReconciliationBreak,
    ReconciliationTolerance,
)


def reconcile_positions(
    *,
    run_id: str,
    portfolio_id: str,
    internal_positions: list[dict[str, Any]],
    external_positions: list[dict[str, Any]],
    tolerance: ReconciliationTolerance,
) -> tuple[list[PositionReconciliationItem], list[ReconciliationBreak]]:
    rows: list[PositionReconciliationItem] = []
    breaks: list[ReconciliationBreak] = []
    internal_by_symbol = {str(item.get("symbol", "")).upper(): item for item in internal_positions}
    external_by_symbol = {str(item.get("symbol", "")).upper(): item for item in external_positions}
    for symbol in sorted(set(internal_by_symbol) | set(external_by_symbol)):
        internal = internal_by_symbol.get(symbol)
        external = external_by_symbol.get(symbol)
        internal_quantity = _quantity(internal)
        external_quantity = _quantity(external)
        internal_mv = _market_value(internal)
        external_mv = _market_value(external)
        if internal is None:
            status = "missing_internal"
            quantity_diff = None
            mv_diff = None
            severity = "high"
            explanation = f"{symbol} exists in the external reference but is missing internally."
        elif external is None:
            status = "missing_external"
            quantity_diff = None
            mv_diff = None
            severity = "high"
            explanation = f"{symbol} exists internally but is missing from the external reference."
        else:
            quantity_diff = (internal_quantity or 0.0) - (external_quantity or 0.0)
            mv_diff = (internal_mv or 0.0) - (external_mv or 0.0)
            if abs(quantity_diff) <= tolerance.position_quantity_tolerance and abs(mv_diff) <= tolerance.market_value_tolerance:
                status = "matched"
                severity = None
                explanation = f"{symbol} position reconciles within tolerance."
            elif abs(mv_diff) <= tolerance.market_value_tolerance:
                status = "within_tolerance"
                severity = "low"
                explanation = f"{symbol} has a small quantity or value difference within market value tolerance."
            else:
                status = "break"
                severity = classify_position_severity(
                    quantity_diff,
                    mv_diff,
                    tolerance.market_value_tolerance,
                )
                explanation = f"{symbol} position differs between Athena and the external reference."
        difference_percent = _safe_div(mv_diff or 0.0, internal_mv or external_mv or 0.0) if internal_mv or external_mv else None
        row = PositionReconciliationItem(
            symbol=symbol,
            internal_quantity=internal_quantity,
            external_quantity=external_quantity,
            quantity_difference=quantity_diff,
            internal_market_value=internal_mv,
            external_market_value=external_mv,
            market_value_difference=mv_diff,
            difference_percent=difference_percent,
            tolerance=tolerance.market_value_tolerance,
            status=status,
            severity=severity,
            explanation=explanation,
        )
        rows.append(row)
        if status not in {"matched", "within_tolerance"}:
            breaks.append(
                create_break(
                    run_id=run_id,
                    portfolio_id=portfolio_id,
                    break_type="position",
                    severity=severity or "low",
                    symbol=symbol,
                    metric="position_market_value",
                    internal_value=internal_mv,
                    external_value=external_mv,
                    difference=mv_diff,
                    tolerance=tolerance.market_value_tolerance,
                    source_module="Portfolio Builder",
                    explanation=explanation,
                    suggested_action="Review position quantity, pending trades and custodian settlement timing.",
                ),
            )
    return rows, breaks


def _quantity(position: dict[str, Any] | None) -> float | None:
    if position is None:
        return None
    return _as_float(position.get("quantity"))


def _market_value(position: dict[str, Any] | None) -> float | None:
    if position is None:
        return None
    if position.get("market_value") is not None:
        return _as_float(position.get("market_value"))
    quantity = _as_float(position.get("quantity")) or 0.0
    price = _as_float(position.get("current_price") or position.get("price")) or 0.0
    return quantity * price


def _safe_div(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def _as_float(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
