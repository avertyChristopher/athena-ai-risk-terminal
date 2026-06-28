from __future__ import annotations

from app.modules.trade_blotter.schemas import TradeBlotterEntry


def build_trade_blotter_summary(entry: TradeBlotterEntry) -> dict[str, str]:
    return {
        "headline": f"{entry.action} {entry.quantity:g} {entry.symbol} at {entry.price:.2f}",
        "notional": f"{entry.estimated_trade_value:.2f} {entry.currency}",
        "status": entry.status,
        "source": entry.source_module,
    }
