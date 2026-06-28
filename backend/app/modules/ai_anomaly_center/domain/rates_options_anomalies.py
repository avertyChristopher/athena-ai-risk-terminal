from __future__ import annotations

from typing import Any

from app.modules.ai_anomaly_center.domain.anomaly_scoring import build_anomaly
from app.modules.ai_anomaly_center.schemas import AnomalyRecord


def detect_rates_options_anomalies(context: dict[str, Any], portfolio_id: str | None) -> list[AnomalyRecord]:
    positions = context.get("positions") or []
    records: list[AnomalyRecord] = []
    total_dv01 = 0.0
    for position in positions:
        symbol = str(position.get("symbol") or "").upper()
        duration = _as_float(
            position.get("duration_assumption")
            or position.get("modified_duration_assumption")
            or position.get("duration")
        )
        dv01 = _as_float(position.get("dv01_assumption") or position.get("dv01"))
        vega = _as_float(position.get("vega") or position.get("vega_exposure"))
        gamma = _as_float(position.get("gamma") or position.get("gamma_exposure"))
        if dv01:
            total_dv01 += abs(dv01)
        if duration and duration > 7:
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id,
                    module_name="Rates Lab",
                    category="rates_options",
                    anomaly_type="high_duration",
                    title=f"{symbol} duration is high",
                    description=f"Duration is {duration:.2f}.",
                    metric_name="duration",
                    observed_value=duration,
                    threshold=7,
                    score=min(78, 28 + duration * 6),
                    source_record_id=str(position.get("id") or symbol),
                    source_payload=position,
                    suggested_action="Review rate shock impact and DV01 exposure.",
                ),
            )
        asset_class = str(position.get("asset_class") or position.get("asset_type") or "").lower()
        if "option" in asset_class or symbol.endswith(("C", "P")):
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id,
                    module_name="Options Pricing Lab",
                    category="rates_options",
                    anomaly_type="option_exposure_placeholder",
                    title=f"{symbol} option-like exposure requires Greeks review",
                    description="Option-like position detected; contract-level Greeks should be reviewed when available.",
                    metric_name="option_position_detected",
                    observed_value=True,
                    threshold="Greeks review",
                    score=38,
                    source_record_id=str(position.get("id") or symbol),
                    source_payload=position,
                    suggested_action="Review delta, gamma, vega and theta exposure in Options Pricing Lab.",
                ),
            )
        if vega is not None and abs(vega) > 5000:
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id,
                    module_name="Options Pricing Lab",
                    category="rates_options",
                    anomaly_type="high_vega_exposure",
                    title=f"{symbol} Vega exposure is high",
                    description=f"Vega exposure is {vega:.2f}.",
                    metric_name="vega",
                    observed_value=vega,
                    threshold=5000,
                    score=63,
                    source_record_id=str(position.get("id") or symbol),
                    source_payload=position,
                    suggested_action="Review implied volatility sensitivity and option hedging assumptions.",
                ),
            )
        if gamma is not None and abs(gamma) > 100:
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id,
                    module_name="Options Pricing Lab",
                    category="rates_options",
                    anomaly_type="high_gamma_exposure",
                    title=f"{symbol} Gamma exposure is high",
                    description=f"Gamma exposure is {gamma:.2f}.",
                    metric_name="gamma",
                    observed_value=gamma,
                    threshold=100,
                    score=59,
                    source_record_id=str(position.get("id") or symbol),
                    source_payload=position,
                    suggested_action="Review convexity of option exposure under underlying price shocks.",
                ),
            )
    if total_dv01 > 500:
        records.append(
            build_anomaly(
                portfolio_id=portfolio_id,
                module_name="Rates Lab",
                category="rates_options",
                anomaly_type="high_dv01",
                title="Portfolio DV01 is high",
                description=f"Estimated DV01 is {total_dv01:.2f}.",
                metric_name="portfolio_dv01",
                observed_value=total_dv01,
                threshold=500,
                score=62,
                suggested_action="Review fixed-income rate sensitivity and stress loss.",
            ),
        )
    return records


def _as_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
