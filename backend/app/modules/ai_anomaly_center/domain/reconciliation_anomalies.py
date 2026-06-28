from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from typing import Any

from app.modules.ai_anomaly_center.domain.anomaly_scoring import build_anomaly
from app.modules.ai_anomaly_center.schemas import AnomalyRecord


def detect_reconciliation_anomalies(context: dict[str, Any], portfolio_id: str | None) -> list[AnomalyRecord]:
    breaks = context.get("reconciliation_breaks") or []
    records: list[AnomalyRecord] = []
    symbol_counts = Counter(str(item.get("symbol") or item.get("metric") or "unknown") for item in breaks)
    for item in breaks:
        break_id = str(item.get("break_id") or "")
        severity = str(item.get("severity") or "").lower()
        status = str(item.get("status") or "").lower()
        if severity == "critical":
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id or item.get("portfolio_id"),
                    module_name="Reconciliation Center",
                    category="reconciliation",
                    anomaly_type="critical_break",
                    title="Critical reconciliation break",
                    description=str(item.get("explanation") or "Critical reconciliation break detected."),
                    metric_name=str(item.get("metric") or "break"),
                    observed_value=item.get("difference"),
                    threshold="critical severity",
                    score=86,
                    source_record_id=break_id,
                    source_payload=item,
                    suggested_action="Escalate the break and document operational resolution.",
                ),
            )
        created_at = _parse_datetime(item.get("created_at"))
        if status == "open" and created_at and (datetime.now(UTC) - created_at).days > 7:
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id or item.get("portfolio_id"),
                    module_name="Reconciliation Center",
                    category="reconciliation",
                    anomaly_type="old_open_break",
                    title="Open reconciliation break is aging",
                    description="An open break is older than seven days.",
                    metric_name="break_age_days",
                    observed_value=(datetime.now(UTC) - created_at).days,
                    threshold=7,
                    score=55,
                    source_record_id=break_id,
                    source_payload=item,
                    suggested_action="Assign owner, explain the break or resolve it.",
                ),
            )
    for symbol, count in symbol_counts.items():
        if symbol and symbol != "None" and count >= 3:
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id,
                    module_name="Reconciliation Center",
                    category="reconciliation",
                    anomaly_type="recurring_break",
                    title=f"Recurring reconciliation breaks for {symbol}",
                    description=f"{count} reconciliation breaks share the same symbol or metric.",
                    metric_name="recurring_break_count",
                    observed_value=count,
                    threshold=3,
                    score=64,
                    suggested_action="Review source mapping, stale prices and recurring operational breaks.",
                ),
            )
    return records


def _parse_datetime(value: Any) -> datetime | None:
    if value is None:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)
    except ValueError:
        return None
