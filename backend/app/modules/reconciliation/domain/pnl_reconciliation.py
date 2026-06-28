from __future__ import annotations

from app.modules.reconciliation.domain.break_classification import create_break
from app.modules.reconciliation.domain.severity import classify_amount_severity
from app.modules.reconciliation.schemas import PnlReconciliationItem, ReconciliationBreak, ReconciliationTolerance


def reconcile_pnl(
    *,
    run_id: str,
    portfolio_id: str,
    internal_total_pnl: float | None,
    external_total_pnl: float | None,
    starting_value: float | None,
    tolerance: ReconciliationTolerance,
) -> tuple[list[PnlReconciliationItem], list[ReconciliationBreak], list[str]]:
    warnings: list[str] = []
    if internal_total_pnl is None or external_total_pnl is None:
        warnings.append("P&L data unavailable; P&L reconciliation is incomplete.")
        return [
            PnlReconciliationItem(
                internal_total_pnl=internal_total_pnl,
                external_total_pnl=external_total_pnl,
                pnl_difference=None,
                pnl_difference_percent=None,
                tolerance=tolerance.pnl_tolerance,
                unexplained_pnl=None,
                status="missing_pnl_data",
                severity="medium",
                explanation="Internal or external P&L data is missing.",
            ),
        ], [], warnings
    difference = internal_total_pnl - external_total_pnl
    difference_percent = difference / starting_value if starting_value else 0.0
    if abs(difference) <= tolerance.pnl_tolerance:
        status = "matched" if difference == 0 else "within_tolerance"
        severity = None if difference == 0 else "low"
        explanation = "Calculated P&L reconciles within tolerance."
        breaks: list[ReconciliationBreak] = []
    else:
        status = "break"
        severity = classify_amount_severity(
            difference,
            tolerance.pnl_tolerance,
            high_multiple=4.0,
            critical_multiple=12.0,
            critical_absolute=25000.0,
        )
        explanation = "Unexplained P&L differs from external value movement beyond tolerance."
        breaks = [
            create_break(
                run_id=run_id,
                portfolio_id=portfolio_id,
                break_type="pnl",
                severity=severity,
                metric="unexplained_pnl",
                internal_value=internal_total_pnl,
                external_value=external_total_pnl,
                difference=difference,
                tolerance=tolerance.pnl_tolerance,
                source_module="P&L Attribution",
                explanation=explanation,
                suggested_action="Review value movement, income, costs, FX and missing trades.",
            ),
        ]
    return [
        PnlReconciliationItem(
            internal_total_pnl=internal_total_pnl,
            external_total_pnl=external_total_pnl,
            pnl_difference=difference,
            pnl_difference_percent=difference_percent,
            tolerance=tolerance.pnl_tolerance,
            unexplained_pnl=difference,
            status=status,
            severity=severity,
            explanation=explanation,
        ),
    ], breaks, warnings
