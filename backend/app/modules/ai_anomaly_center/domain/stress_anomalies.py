from __future__ import annotations

from typing import Any

from app.modules.ai_anomaly_center.domain.anomaly_scoring import build_anomaly
from app.modules.ai_anomaly_center.schemas import AnomalyRecord


def detect_stress_anomalies(context: dict[str, Any], portfolio_id: str | None) -> list[AnomalyRecord]:
    runs = context.get("stress_runs") or []
    records: list[AnomalyRecord] = []
    by_scenario: dict[str, list[dict[str, Any]]] = {}
    for run in runs:
        scenario = str((run.get("selected_scenario") or {}).get("id") or run.get("scenario_id") or "unknown")
        by_scenario.setdefault(scenario, []).append(run)
        percent_loss = abs(_as_float(run.get("percent_loss") or run.get("estimated_loss_percent")) or 0.0)
        severity = str((run.get("severity") or {}).get("severity") if isinstance(run.get("severity"), dict) else run.get("severity") or "").lower()
        if percent_loss > 0.20:
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id or ((run.get("selected_portfolio") or {}).get("portfolio_id")),
                    module_name="Stress Testing",
                    category="stress",
                    anomaly_type="severe_stress_loss",
                    title="Stress loss is severe",
                    description=f"Stress loss is {percent_loss:.1%}.",
                    metric_name="stress_loss_percent",
                    observed_value=percent_loss,
                    threshold=0.20,
                    score=min(94, 48 + percent_loss * 180),
                    source_record_id=str(run.get("run_id") or ""),
                    source_payload=run,
                    suggested_action="Review stress scenario, worst contributors and limit breaches.",
                ),
            )
        if "critical" in severity:
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id,
                    module_name="Stress Testing",
                    category="stress",
                    anomaly_type="critical_stress_severity",
                    title="Critical stress severity",
                    description="Stress severity is critical.",
                    metric_name="stress_severity",
                    observed_value=severity,
                    threshold="below critical",
                    score=86,
                    source_payload=run,
                    suggested_action="Escalate portfolio stress review and review mitigation actions.",
                ),
            )
    for scenario, rows in by_scenario.items():
        if len(rows) < 2:
            continue
        losses = [abs(_as_float(row.get("percent_loss") or row.get("estimated_loss_percent")) or 0.0) for row in rows[:2]]
        if losses[1] and losses[0] > losses[1] * 1.5:
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id,
                    module_name="Stress Testing",
                    category="stress",
                    anomaly_type="stress_deterioration",
                    title=f"Stress deterioration for {scenario}",
                    description="Latest stress loss increased by more than 50% from prior run.",
                    metric_name="stress_loss_change",
                    observed_value=losses[0],
                    expected_value=losses[1],
                    threshold="50% increase",
                    score=65,
                    suggested_action="Compare positions, rates exposure and volatility assumptions between runs.",
                ),
            )
    return records


def _as_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
