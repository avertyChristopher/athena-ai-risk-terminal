from __future__ import annotations

from typing import Any

from app.modules.ai_anomaly_center.domain.anomaly_scoring import build_anomaly
from app.modules.ai_anomaly_center.schemas import AnomalyRecord


def detect_portfolio_anomalies(context: dict[str, Any], portfolio_id: str | None) -> list[AnomalyRecord]:
    portfolio = context.get("portfolio") or {}
    positions = context.get("positions") or []
    records: list[AnomalyRecord] = []
    cash = _as_float(portfolio.get("cash")) or 0.0
    values = [_position_value(position) for position in positions]
    invested = sum(values)
    total_value = invested + cash
    if total_value <= 0:
        return records
    if cash < 0:
        records.append(
            build_anomaly(
                portfolio_id=portfolio_id,
                module_name="Portfolio Builder",
                category="portfolio",
                anomaly_type="negative_cash",
                title="Portfolio cash is negative",
                description="Cash is below zero and may require funding or trade review.",
                metric_name="cash",
                observed_value=cash,
                threshold=0,
                score=68,
                suggested_action="Review unsettled trades, deposits and cash reconciliation.",
            ),
        )
    if cash / total_value < 0.01:
        records.append(
            build_anomaly(
                portfolio_id=portfolio_id,
                module_name="Portfolio Builder",
                category="portfolio",
                anomaly_type="low_cash",
                title="Portfolio cash reserve is low",
                description="Cash is below 1% of portfolio value.",
                metric_name="cash_weight",
                observed_value=cash / total_value,
                threshold=0.01,
                score=31,
                suggested_action="Review liquidity needs and pending trade settlement.",
            ),
        )
    sector_values: dict[str, float] = {}
    asset_values: dict[str, float] = {}
    for position, value in zip(positions, values):
        weight = value / total_value
        symbol = str(position.get("symbol", "UNKNOWN")).upper()
        if weight > 0.25:
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id,
                    module_name="Portfolio Builder",
                    category="portfolio",
                    anomaly_type="single_name_concentration",
                    title=f"{symbol} concentration is elevated",
                    description=f"{symbol} is {weight:.1%} of portfolio value.",
                    metric_name="position_weight",
                    observed_value=weight,
                    threshold=0.25,
                    score=min(92, 35 + weight * 140),
                    source_record_id=str(position.get("id") or symbol),
                    source_payload=position,
                    suggested_action="Review concentration limits and diversify or document exception.",
                ),
            )
        sector = str(position.get("sector") or "Unknown")
        sector_values[sector] = sector_values.get(sector, 0.0) + value
        asset_type = _normalize_key(position.get("asset_type") or position.get("asset_class") or "unknown")
        asset_values[asset_type] = asset_values.get(asset_type, 0.0) + value
    for sector, value in sector_values.items():
        sector_weight = value / total_value
        if sector_weight > 0.50:
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id,
                    module_name="Portfolio Builder",
                    category="portfolio",
                    anomaly_type="sector_concentration",
                    title=f"{sector} sector exposure is high",
                    description=f"{sector} exposure is {sector_weight:.1%}.",
                    metric_name="sector_weight",
                    observed_value=sector_weight,
                    threshold=0.50,
                    score=min(90, 36 + sector_weight * 90),
                    suggested_action="Review sector concentration against IPS and limit policies.",
            ),
        )
    for asset_type, target_weight in _target_allocations(portfolio.get("target_allocation")).items():
        actual_weight = asset_values.get(asset_type, 0.0) / total_value
        drift = actual_weight - target_weight
        if abs(drift) > 0.10:
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id,
                    module_name="Portfolio Builder",
                    category="portfolio",
                    anomaly_type="allocation_drift",
                    title=f"{asset_type.title()} allocation drift is material",
                    description=f"Actual allocation differs from target by {drift:.1%}.",
                    metric_name="asset_allocation_drift",
                    observed_value=actual_weight,
                    expected_value=target_weight,
                    threshold=0.10,
                    score=min(86, 34 + abs(drift) * 240),
                    suggested_action="Review target allocation, rebalancing needs and IPS tolerance.",
                ),
            )
    top3 = sum(sorted(values, reverse=True)[:3]) / total_value if values else 0.0
    if top3 > 0.75:
        records.append(
            build_anomaly(
                portfolio_id=portfolio_id,
                module_name="Portfolio Builder",
                category="portfolio",
                anomaly_type="top3_concentration",
                title="Top 3 holdings concentration is elevated",
                description=f"Top 3 holdings represent {top3:.1%} of portfolio value.",
                metric_name="top3_weight",
                observed_value=top3,
                threshold=0.75,
                score=min(88, 40 + top3 * 70),
                suggested_action="Review issuer concentration and diversification policy.",
            ),
        )
    return records


def _position_value(position: dict[str, Any]) -> float:
    return (_as_float(position.get("quantity")) or 0.0) * (
        _as_float(position.get("current_price")) or _as_float(position.get("average_price")) or 0.0
    )


def _as_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _target_allocations(value: Any) -> dict[str, float]:
    if isinstance(value, dict):
        return {
            _normalize_key(key): float(weight)
            for key, weight in value.items()
            if _as_float(weight) is not None
        }
    if isinstance(value, list):
        targets: dict[str, float] = {}
        for item in value:
            if not isinstance(item, dict):
                continue
            key = item.get("asset_type") or item.get("asset_class") or item.get("name")
            weight = _as_float(item.get("target_weight") or item.get("weight"))
            if key and weight is not None:
                targets[_normalize_key(key)] = weight
        return targets
    return {}


def _normalize_key(value: Any) -> str:
    return str(value or "unknown").strip().lower().replace("-", "_").replace(" ", "_")
