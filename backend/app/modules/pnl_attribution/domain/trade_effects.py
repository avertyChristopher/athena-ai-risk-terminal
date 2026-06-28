from __future__ import annotations

from typing import Any

from app.modules.pnl_attribution.schemas import TradeEffect


def calculate_trade_effects(
    transactions: list[dict[str, Any]],
    starting_value: float,
    include_trades: bool,
) -> TradeEffect:
    if not include_trades:
        return TradeEffect(
            status="disabled",
            total_trade_costs=0.0,
            estimated_slippage=0.0,
            turnover=0.0,
            trade_impact_on_cash=0.0,
            warnings=[],
        )

    if not transactions:
        return TradeEffect(
            status="unavailable",
            total_trade_costs=0.0,
            estimated_slippage=0.0,
            turnover=0.0,
            trade_impact_on_cash=0.0,
            trades=[],
            warnings=[
                "No portfolio transactions or persisted Trade Blotter entries found for the selected period.",
            ],
        )

    trade_value = 0.0
    costs = 0.0
    slippage = 0.0
    cash_impact = 0.0
    for trade in transactions:
        quantity = _as_float(trade.get("quantity")) or 0.0
        price = _as_float(trade.get("price") or trade.get("execution_price")) or 0.0
        value = quantity * price
        trade_value += abs(value)
        explicit_cost = _as_float(trade.get("cost") or trade.get("commission")) or value * 0.0005
        slip = _as_float(trade.get("slippage")) or value * 0.0003
        costs += explicit_cost
        slippage += slip
        action = str(trade.get("action") or trade.get("side") or "").upper()
        cash_impact += value if action == "SELL" else -value

    return TradeEffect(
        status="available",
        total_trade_costs=costs,
        estimated_slippage=slippage,
        turnover=trade_value / starting_value if starting_value else 0.0,
        trade_impact_on_cash=cash_impact,
        trades=transactions,
        warnings=[],
    )


def _as_float(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
