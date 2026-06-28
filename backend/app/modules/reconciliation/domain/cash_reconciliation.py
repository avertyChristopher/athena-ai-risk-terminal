from __future__ import annotations

from app.modules.reconciliation.domain.break_classification import create_break
from app.modules.reconciliation.domain.severity import classify_amount_severity
from app.modules.reconciliation.schemas import CashReconciliationItem, ReconciliationBreak, ReconciliationTolerance


def reconcile_cash(
    *,
    run_id: str,
    portfolio_id: str,
    currency: str,
    internal_cash: float | None,
    external_cash: float | None,
    tolerance: ReconciliationTolerance,
) -> tuple[list[CashReconciliationItem], list[ReconciliationBreak], list[str]]:
    warnings: list[str] = []
    if internal_cash is None or external_cash is None:
        warnings.append("Missing cash data; cash reconciliation is incomplete.")
        return [
            CashReconciliationItem(
                internal_cash=internal_cash,
                external_cash=external_cash,
                cash_difference=None,
                cash_difference_percent=None,
                currency=currency,
                tolerance=tolerance.cash_tolerance,
                status="missing_cash_data",
                severity="medium",
                explanation="Internal or external cash data is missing.",
            ),
        ], [], warnings
    difference = internal_cash - external_cash
    difference_percent = difference / internal_cash if internal_cash else 0.0
    if abs(difference) <= tolerance.cash_tolerance:
        severity = "low" if difference else None
        status = "within_tolerance" if difference else "matched"
        explanation = "Cash balance reconciles within tolerance."
        breaks: list[ReconciliationBreak] = []
    else:
        severity = classify_amount_severity(
            difference,
            tolerance.cash_tolerance,
            critical_absolute=10000.0,
        )
        status = "break"
        explanation = "Cash balance differs between Athena and the external reference."
        breaks = [
            create_break(
                run_id=run_id,
                portfolio_id=portfolio_id,
                break_type="cash",
                severity=severity,
                metric="cash_balance",
                internal_value=internal_cash,
                external_value=external_cash,
                difference=difference,
                tolerance=tolerance.cash_tolerance,
                source_module="Portfolio Builder",
                explanation=explanation,
                suggested_action="Review recent cash movements, fees and unsettled trades.",
            ),
        ]
    return [
        CashReconciliationItem(
            internal_cash=internal_cash,
            external_cash=external_cash,
            cash_difference=difference,
            cash_difference_percent=difference_percent,
            currency=currency,
            tolerance=tolerance.cash_tolerance,
            status=status,
            severity=severity,
            explanation=explanation,
        ),
    ], breaks, warnings
