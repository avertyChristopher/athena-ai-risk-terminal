from __future__ import annotations

from typing import Any

from app.modules.ai_anomaly_center.domain.anomaly_scoring import build_anomaly
from app.modules.ai_anomaly_center.schemas import AnomalyRecord


def detect_pnl_anomalies(context: dict[str, Any], portfolio_id: str | None) -> list[AnomalyRecord]:
    records: list[AnomalyRecord] = []
    for pnl in context.get("pnl_history", []):
        analysis_id = str(pnl.get("analysis_id") or "")
        total_return = _as_float(pnl.get("total_pnl_percent")) or 0.0
        if total_return < -0.05:
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id or pnl.get("portfolio_id"),
                    module_name="P&L Attribution",
                    category="pnl",
                    anomaly_type="large_period_loss",
                    title="Large negative P&L move",
                    description=f"Portfolio P&L return is {total_return:.2%}.",
                    metric_name="total_pnl_percent",
                    observed_value=total_return,
                    threshold=-0.05,
                    score=min(94, 45 + abs(total_return) * 650),
                    source_record_id=analysis_id,
                    source_payload=pnl,
                    suggested_action="Review top contributors, market data and trade costs for the period.",
                ),
            )
        total_pnl = abs(_as_float(pnl.get("total_pnl")) or 0.0)
        unexplained_ratio = _as_float(pnl.get("unexplained_pnl_percent"))
        if unexplained_ratio is None and total_pnl:
            unexplained_ratio = abs(_as_float(pnl.get("unexplained_pnl")) or 0.0) / total_pnl
        if unexplained_ratio is not None and abs(unexplained_ratio) > 0.02:
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id or pnl.get("portfolio_id"),
                    module_name="P&L Attribution",
                    category="pnl",
                    anomaly_type="unexplained_pnl",
                    title="Unexplained P&L exceeds tolerance",
                    description=f"Unexplained P&L is {unexplained_ratio:.2%} of the reference amount.",
                    metric_name="unexplained_pnl_percent",
                    observed_value=unexplained_ratio,
                    threshold=0.02,
                    score=min(90, 42 + abs(unexplained_ratio) * 900),
                    source_record_id=analysis_id,
                    source_payload=pnl,
                    suggested_action="Reconcile prices, FX, income, fees and trade effects before closing the period.",
                ),
            )
        for row in pnl.get("position_contributions", []) or []:
            contribution = abs(_as_float(row.get("total_pnl")) or 0.0)
            if total_pnl and contribution / total_pnl > 0.60:
                records.append(
                    build_anomaly(
                        portfolio_id=portfolio_id or pnl.get("portfolio_id"),
                        module_name="P&L Attribution",
                        category="pnl",
                        anomaly_type="single_contributor_dominance",
                        title=f"{row.get('symbol')} dominates P&L",
                        description=f"One position contributes {contribution / total_pnl:.1%} of absolute P&L.",
                        metric_name="single_position_pnl_share",
                        observed_value=contribution / total_pnl,
                        threshold=0.60,
                        score=58,
                        source_record_id=analysis_id,
                        source_payload=row,
                        suggested_action="Review single-name exposure, price move and data quality.",
                    ),
                )
        benchmark = pnl.get("benchmark_comparison") or {}
        active_return = _as_float(benchmark.get("active_return"))
        if active_return is not None and active_return < -0.05:
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id or pnl.get("portfolio_id"),
                    module_name="P&L Attribution",
                    category="pnl",
                    anomaly_type="benchmark_underperformance",
                    title="Large negative active return",
                    description=f"Portfolio underperformed benchmark by {active_return:.2%}.",
                    metric_name="active_return",
                    observed_value=active_return,
                    threshold=-0.05,
                    score=52,
                    source_record_id=analysis_id,
                    source_payload=benchmark,
                    suggested_action="Review allocation, selection and benchmark mapping assumptions.",
                ),
            )
    return records


def _as_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
