from __future__ import annotations

from typing import Any

from app.modules.ai_anomaly_center.domain.anomaly_scoring import build_anomaly
from app.modules.ai_anomaly_center.schemas import AnomalyRecord


def detect_risk_anomalies(context: dict[str, Any], portfolio_id: str | None) -> list[AnomalyRecord]:
    risk = context.get("risk_monitor") or {}
    records: list[AnomalyRecord] = []
    score = _as_float(risk.get("global_risk_score"))
    if score is not None and score > 75:
        records.append(
            build_anomaly(
                portfolio_id=portfolio_id,
                module_name="Risk Monitor",
                category="risk",
                anomaly_type="high_risk_score",
                title="Risk score is elevated",
                description=f"Risk Monitor score is {score:.0f}.",
                metric_name="global_risk_score",
                observed_value=score,
                threshold=75,
                score=min(95, 40 + score * 0.65),
                source_payload=risk,
                suggested_action="Review risk drivers, concentration and recent market changes.",
            ),
        )
    for metric in risk.get("risk_metrics", []) or []:
        name = str(metric.get("name") or metric.get("metric") or "")
        value = _as_float(metric.get("value") or metric.get("current_value"))
        prior_value = _as_float(metric.get("prior_value") or metric.get("previous_value"))
        if value is None:
            continue
        if name.lower() in {"var 95%", "var", "portfolio var"} and abs(value) > 0.05:
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id,
                    module_name="Risk Monitor",
                    category="risk",
                    anomaly_type="var_elevated",
                    title="VaR is elevated",
                    description=f"{name} is {value:.2%}.",
                    metric_name=name,
                    observed_value=value,
                    threshold=0.05,
                    score=61,
                    source_payload=metric,
                    suggested_action="Review VaR inputs, volatility and portfolio concentration.",
                ),
            )
        if name.lower() in {"var 95%", "var", "portfolio var"} and prior_value and abs(value) > abs(prior_value) * 1.5:
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id,
                    module_name="Risk Monitor",
                    category="risk",
                    anomaly_type="var_jump",
                    title="VaR increased materially",
                    description=f"{name} increased by more than 50% versus the previous snapshot.",
                    metric_name=name,
                    observed_value=value,
                    expected_value=prior_value,
                    threshold="50% increase",
                    score=68,
                    source_payload=metric,
                    suggested_action="Review volatility inputs, position changes and benchmark coverage.",
                ),
            )
        if "volatility" in name.lower() and value > 0.35:
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id,
                    module_name="Risk Monitor",
                    category="risk",
                    anomaly_type="volatility_spike",
                    title="Portfolio volatility is elevated",
                    description=f"{name} is {value:.2%}.",
                    metric_name=name,
                    observed_value=value,
                    threshold=0.35,
                    score=56,
                    source_payload=metric,
                    suggested_action="Compare realized volatility with Volatility Lab inputs and Market Data coverage.",
                ),
            )
    coverage = _as_float((risk.get("risk_source") or {}).get("coverage_ratio"))
    if coverage is not None and coverage < 0.80:
        records.append(
            build_anomaly(
                portfolio_id=portfolio_id,
                module_name="Risk Monitor",
                category="risk",
                anomaly_type="low_coverage_ratio",
                title="Risk data coverage is low",
                description=f"Risk coverage ratio is {coverage:.1%}.",
                metric_name="coverage_ratio",
                observed_value=coverage,
                threshold=0.80,
                score=50,
                source_payload=risk.get("risk_source") or {},
                suggested_action="Refresh Market Data and verify benchmark return coverage.",
            ),
        )
    return records


def _as_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
