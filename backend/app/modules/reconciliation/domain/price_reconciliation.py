from __future__ import annotations

from typing import Any

from app.modules.reconciliation.domain.break_classification import create_break
from app.modules.reconciliation.domain.severity import classify_price_severity
from app.modules.reconciliation.schemas import PriceReconciliationItem, ReconciliationBreak, ReconciliationTolerance


def reconcile_prices(
    *,
    run_id: str,
    portfolio_id: str,
    internal_prices: dict[str, dict[str, Any]],
    external_positions: list[dict[str, Any]],
    tolerance: ReconciliationTolerance,
) -> tuple[list[PriceReconciliationItem], list[ReconciliationBreak], list[str]]:
    rows: list[PriceReconciliationItem] = []
    breaks: list[ReconciliationBreak] = []
    warnings: list[str] = []
    for external in external_positions:
        symbol = str(external.get("symbol", "")).upper()
        internal = internal_prices.get(symbol, {})
        internal_price = _as_float(internal.get("price"))
        external_price = _as_float(external.get("price"))
        internal_ts = internal.get("timestamp")
        external_ts = external.get("price_timestamp")
        stale = bool(external.get("stale_price"))
        if internal_price is None or external_price is None:
            warnings.append(f"{symbol}: missing internal or external price.")
            row = PriceReconciliationItem(
                symbol=symbol,
                internal_price=internal_price,
                external_price=external_price,
                price_difference=None,
                price_difference_bps=None,
                internal_price_timestamp=str(internal_ts) if internal_ts else None,
                external_price_timestamp=str(external_ts) if external_ts else None,
                tolerance_bps=tolerance.price_tolerance_bps,
                status="missing_price",
                severity="medium",
                explanation="Missing price prevents full price reconciliation.",
            )
            rows.append(row)
            continue
        difference = internal_price - external_price
        difference_bps = difference / internal_price * 10000.0 if internal_price else 0.0
        if abs(difference_bps) <= tolerance.price_tolerance_bps and not stale:
            status = "matched" if difference == 0 else "within_tolerance"
            severity = None if difference == 0 else "low"
            explanation = f"{symbol} price reconciles within tolerance."
        else:
            status = "stale_price" if stale else "break"
            severity = classify_price_severity(difference_bps, tolerance.price_tolerance_bps, stale)
            explanation = f"{symbol} has a stale or mismatched external price."
            breaks.append(
                create_break(
                    run_id=run_id,
                    portfolio_id=portfolio_id,
                    break_type="price",
                    severity=severity,
                    symbol=symbol,
                    metric="price",
                    internal_value=internal_price,
                    external_value=external_price,
                    difference=difference_bps,
                    tolerance=tolerance.price_tolerance_bps,
                    source_module="Market Data",
                    explanation=explanation,
                    suggested_action="Review external price timestamp and Market Data close price.",
                ),
            )
        rows.append(
            PriceReconciliationItem(
                symbol=symbol,
                internal_price=internal_price,
                external_price=external_price,
                price_difference=difference,
                price_difference_bps=difference_bps,
                internal_price_timestamp=str(internal_ts) if internal_ts else None,
                external_price_timestamp=str(external_ts) if external_ts else None,
                tolerance_bps=tolerance.price_tolerance_bps,
                status=status,
                severity=severity,
                explanation=explanation,
            ),
        )
    return rows, breaks, warnings


def _as_float(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
