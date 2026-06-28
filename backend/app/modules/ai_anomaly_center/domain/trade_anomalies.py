from __future__ import annotations

from typing import Any

from app.modules.ai_anomaly_center.domain.anomaly_scoring import build_anomaly
from app.modules.ai_anomaly_center.schemas import AnomalyRecord


def detect_trade_anomalies(context: dict[str, Any], portfolio_id: str | None) -> list[AnomalyRecord]:
    portfolio = context.get("portfolio") or {}
    trades = context.get("trade_blotter") or []
    positions = context.get("positions") or []
    portfolio_value = _portfolio_value(portfolio, positions)
    records: list[AnomalyRecord] = []
    rejected_count = 0
    total_notional = 0.0
    for trade in trades:
        trade_id = str(trade.get("trade_id") or "")
        notional = _as_float(trade.get("estimated_trade_value")) or (
            (_as_float(trade.get("quantity")) or 0.0) * (_as_float(trade.get("price")) or 0.0)
        )
        total_notional += abs(notional)
        cost = (_as_float(trade.get("cost_estimate")) or 0.0) + (_as_float(trade.get("slippage_estimate")) or 0.0)
        status = str(trade.get("status") or "").lower()
        constraint_status = str(trade.get("constraint_status") or "").lower()
        suitability = str(trade.get("suitability_status") or "").lower()
        review_note = trade.get("review_note") or trade.get("review_comment") or trade.get("decision_note")
        if portfolio_value and notional / portfolio_value > 0.20:
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id,
                    module_name="Trade Blotter",
                    category="trades",
                    anomaly_type="large_trade_notional",
                    title=f"{trade.get('symbol')} trade size is unusually large",
                    description=f"Trade notional is {notional / portfolio_value:.1%} of portfolio value.",
                    metric_name="trade_notional_weight",
                    observed_value=notional / portfolio_value,
                    threshold=0.20,
                    score=min(95, 45 + (notional / portfolio_value) * 140),
                    source_record_id=trade_id,
                    source_payload=trade,
                    suggested_action="Review pre-trade approval, liquidity and concentration impact.",
                ),
            )
        if notional and cost / notional > 0.01:
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id,
                    module_name="Trade Blotter",
                    category="trades",
                    anomaly_type="high_transaction_cost",
                    title=f"{trade.get('symbol')} trade cost is high",
                    description=f"Estimated costs are {cost / notional:.2%} of notional.",
                    metric_name="estimated_cost_percent",
                    observed_value=cost / notional,
                    threshold=0.01,
                    score=min(88, 32 + (cost / notional) * 2200),
                    source_record_id=trade_id,
                    source_payload=trade,
                    suggested_action="Review order type, liquidity and execution assumptions.",
                ),
            )
        if status == "rejected":
            rejected_count += 1
        if status == "approved" and ("warning" in constraint_status or "not suitable" in suitability):
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id,
                    module_name="Trade Blotter",
                    category="trades",
                    anomaly_type="approved_trade_with_warnings",
                    title=f"{trade.get('symbol')} approved despite warnings",
                    description="An approved trade still carries constraint or suitability warnings.",
                    metric_name="approval_control",
                    observed_value=status,
                    expected_value="approved only when warnings are resolved",
                    threshold="no unresolved warnings",
                    score=82,
                    source_record_id=trade_id,
                    source_payload=trade,
                    suggested_action="Recheck the review note and document the exception rationale.",
                ),
            )
        if status == "approved" and not review_note and portfolio_value and notional / portfolio_value > 0.20:
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id,
                    module_name="Trade Blotter",
                    category="trades",
                    anomaly_type="missing_review_note_on_high_risk_trade",
                    title=f"{trade.get('symbol')} high-risk approval lacks review note",
                    description="A large approved trade does not have reviewer rationale attached.",
                    metric_name="review_note",
                    observed_value=None,
                    threshold="required for high-risk approval",
                    score=58,
                    source_record_id=trade_id,
                    source_payload=trade,
                    suggested_action="Add reviewer rationale or reopen the trade for additional review.",
                ),
            )
    if rejected_count > 2:
        records.append(
            build_anomaly(
                portfolio_id=portfolio_id,
                module_name="Trade Blotter",
                category="trades",
                anomaly_type="repeated_rejections",
                title="Repeated rejected trades",
                description=f"{rejected_count} rejected trades were detected in the lookback window.",
                metric_name="rejected_trade_count",
                observed_value=rejected_count,
                threshold=2,
                score=54,
                suggested_action="Review strategy, constraints and trade submission quality.",
            ),
        )
    if portfolio_value and total_notional / portfolio_value > 0.50:
        records.append(
            build_anomaly(
                portfolio_id=portfolio_id,
                module_name="Trade Blotter",
                category="trades",
                anomaly_type="high_trade_turnover",
                title="Trade turnover is unusually high",
                description=f"Lookback trade notional is {total_notional / portfolio_value:.1%} of portfolio value.",
                metric_name="trade_turnover",
                observed_value=total_notional / portfolio_value,
                threshold=0.50,
                score=min(86, 38 + (total_notional / portfolio_value) * 70),
                suggested_action="Review rebalance rationale, execution costs and portfolio churn.",
            ),
        )
    return records


def _portfolio_value(portfolio: dict[str, Any], positions: list[dict[str, Any]]) -> float:
    value = _as_float(portfolio.get("total_value"))
    if value:
        return value
    cash = _as_float(portfolio.get("cash")) or 0.0
    return cash + sum((_as_float(row.get("quantity")) or 0.0) * (_as_float(row.get("current_price")) or _as_float(row.get("average_price")) or 0.0) for row in positions)


def _as_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
