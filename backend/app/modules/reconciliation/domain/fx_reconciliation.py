from __future__ import annotations

from typing import Any

from app.modules.reconciliation.domain.break_classification import create_break
from app.modules.reconciliation.domain.severity import classify_amount_severity
from app.modules.reconciliation.schemas import FxReconciliationItem, ReconciliationBreak


def reconcile_fx(
    *,
    run_id: str,
    portfolio_id: str,
    base_currency: str,
    internal_rates: dict[str, float],
    external_rates: dict[str, float],
    external_positions: list[dict[str, Any]],
) -> tuple[list[FxReconciliationItem], list[ReconciliationBreak], list[str]]:
    currencies = sorted({
        str(position.get("currency") or base_currency).upper()
        for position in external_positions
        if str(position.get("currency") or base_currency).upper() != base_currency.upper()
    })
    if not currencies:
        return [], [], ["No non-base-currency positions detected; FX reconciliation not required."]
    rows: list[FxReconciliationItem] = []
    breaks: list[ReconciliationBreak] = []
    warnings: list[str] = []
    for currency in currencies:
        internal = internal_rates.get(currency)
        external = external_rates.get(currency)
        if internal is None or external is None:
            warnings.append(f"{currency}: missing FX rate; FX reconciliation is incomplete.")
            rows.append(
                FxReconciliationItem(
                    currency=currency,
                    internal_fx_rate=internal,
                    external_fx_rate=external,
                    fx_difference=None,
                    translation_difference=None,
                    status="missing_fx_data",
                    severity="medium",
                    explanation="Missing internal or external FX rate.",
                ),
            )
            continue
        exposure = sum(
            float(position.get("market_value") or 0.0)
            for position in external_positions
            if str(position.get("currency") or "").upper() == currency
        )
        difference = internal - external
        translation = exposure * difference
        if abs(difference) <= 0.0025:
            status = "matched" if difference == 0 else "within_tolerance"
            severity = None if difference == 0 else "low"
            explanation = f"{currency} FX rate reconciles within demo tolerance."
        else:
            status = "break"
            severity = classify_amount_severity(difference, 0.0025, high_multiple=4.0, critical_multiple=12.0)
            explanation = f"{currency} FX rate differs from external reference."
            breaks.append(
                create_break(
                    run_id=run_id,
                    portfolio_id=portfolio_id,
                    break_type="fx",
                    severity=severity,
                    symbol=currency,
                    metric="fx_rate",
                    internal_value=internal,
                    external_value=external,
                    difference=difference,
                    tolerance=0.0025,
                    source_module="Market Data",
                    explanation=explanation,
                    suggested_action="Review FX source, valuation time and base-currency translation.",
                ),
            )
        rows.append(
            FxReconciliationItem(
                currency=currency,
                internal_fx_rate=internal,
                external_fx_rate=external,
                fx_difference=difference,
                translation_difference=translation,
                status=status,
                severity=severity,
                explanation=explanation,
            ),
        )
    return rows, breaks, warnings
