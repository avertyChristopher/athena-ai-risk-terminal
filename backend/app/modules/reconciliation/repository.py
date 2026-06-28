from __future__ import annotations

from copy import deepcopy
from datetime import date
from typing import Any

from sqlalchemy.orm import Session

from app.modules.market_data.repository import MarketDataRepository
from app.modules.portfolio_builder.repository import PortfolioRepository, PositionRepository
from app.modules.reconciliation.schemas import ReconciliationBreak, ReconciliationRunResult


class ReconciliationRepository:
    _runs: dict[str, ReconciliationRunResult] = {}
    _breaks: dict[str, ReconciliationBreak] = {}

    def __init__(self, db: Session | None = None) -> None:
        self.db = db
        self.portfolios = PortfolioRepository(db) if db is not None else None
        self.positions = PositionRepository(db) if db is not None else None
        self.market_data = MarketDataRepository(db) if db is not None else None

    def get_portfolio(self, portfolio_id: str) -> dict[str, Any] | None:
        if self.portfolios is None:
            return None
        return self.portfolios.get_portfolio(portfolio_id)

    def list_positions(self, portfolio_id: str) -> list[dict[str, Any]]:
        if self.positions is None:
            return []
        return self.positions.list_positions(portfolio_id)

    def latest_market_price(self, symbol: str) -> dict[str, Any]:
        if self.market_data is None:
            return {}
        rows = self.market_data.get_prices(symbol)
        if not rows:
            return {}
        latest = rows[-1]
        return {
            "price": float(latest["close"]),
            "timestamp": str(latest["date"]),
            "data_source": "Market Data",
        }

    def build_demo_external_data(
        self,
        *,
        portfolio: dict[str, Any],
        positions: list[dict[str, Any]],
        reconciliation_date: date,
        source: str,
        internal_total_pnl: float | None,
    ) -> tuple[dict[str, Any], list[str]]:
        warnings: list[str] = []
        if source != "demo_custodian":
            warnings.append(
                f"{source} is not connected in this demo build; deterministic demo custodian reference is used.",
            )
        portfolio_id = str(portfolio["id"])
        external_positions = [self._external_position(position, portfolio_id, reconciliation_date) for position in positions]
        external_cash = float(portfolio.get("cash") or 0.0) + self._cash_adjustment(portfolio_id)
        external_trades = self._external_trades(portfolio_id)
        if portfolio_id == "pf_003":
            for row in external_positions:
                if row["symbol"] == "NVDA":
                    row["quantity"] = max(float(row["quantity"]) - 2.0, 0.0)
                    row["market_value"] = row["quantity"] * row["price"]
                    break
            external_positions.append(
                {
                    "symbol": "AMD",
                    "asset_name": "Advanced Micro Devices Inc.",
                    "quantity": 10.0,
                    "price": 160.0,
                    "market_value": 1600.0,
                    "currency": "USD",
                    "price_timestamp": reconciliation_date.isoformat(),
                    "stale_price": False,
                },
            )
        if portfolio_id == "pf_004":
            for row in external_positions:
                if row["symbol"] in {"VXUS", "GLD"}:
                    row["price"] = round(float(row["price"]) * 0.994, 2)
                    row["market_value"] = row["quantity"] * row["price"]
                if row["symbol"] == "IEF":
                    row["stale_price"] = True
                    row["price_timestamp"] = "2026-05-29"
        external_total_pnl = None if internal_total_pnl is None else internal_total_pnl + self._pnl_adjustment(portfolio_id)
        return {
            "source": "demo_custodian",
            "valuation_date": reconciliation_date.isoformat(),
            "positions": external_positions,
            "cash": external_cash,
            "currency": str(portfolio.get("base_currency") or "USD"),
            "pending_trades": external_trades,
            "fees": self._fees(portfolio_id),
            "fx_rates": self._fx_rates(portfolio_id),
            "total_pnl": external_total_pnl,
        }, warnings

    def save_run(self, run: ReconciliationRunResult) -> ReconciliationRunResult:
        self._runs[run.run_id] = run
        for item in run.breaks:
            self._breaks[item.break_id] = item
        return run

    def list_runs(self) -> list[ReconciliationRunResult]:
        return sorted(self._runs.values(), key=lambda item: item.generated_at, reverse=True)

    def get_run(self, run_id: str) -> ReconciliationRunResult | None:
        return self._runs.get(run_id)

    def delete_run(self, run_id: str) -> bool:
        run = self._runs.pop(run_id, None)
        if run is None:
            return False
        for item in run.breaks:
            self._breaks.pop(item.break_id, None)
        return True

    def list_breaks(self) -> list[ReconciliationBreak]:
        return sorted(self._breaks.values(), key=lambda item: item.created_at, reverse=True)

    def get_break(self, break_id: str) -> ReconciliationBreak | None:
        return self._breaks.get(break_id)

    def save_break(self, item: ReconciliationBreak) -> ReconciliationBreak:
        self._breaks[item.break_id] = item
        run = self._runs.get(item.run_id)
        if run is not None:
            updated_breaks = [item if row.break_id == item.break_id else row for row in run.breaks]
            self._runs[item.run_id] = run.model_copy(update={"breaks": updated_breaks})
        return item

    def clear(self) -> None:
        self._runs.clear()
        self._breaks.clear()

    def _external_position(
        self,
        position: dict[str, Any],
        portfolio_id: str,
        reconciliation_date: date,
    ) -> dict[str, Any]:
        row = deepcopy(position)
        symbol = str(row.get("symbol", "")).upper()
        quantity = float(row.get("quantity") or 0.0)
        latest = self.latest_market_price(symbol)
        price = float(latest.get("price") or row.get("current_price") or row.get("average_price") or 0.0)
        price *= self._price_multiplier(portfolio_id, symbol)
        stale = self._is_stale_price(portfolio_id, symbol)
        timestamp = "2026-05-29" if stale else str(latest.get("timestamp") or reconciliation_date.isoformat())
        return {
            "symbol": symbol,
            "asset_name": str(row.get("asset_name") or row.get("name") or symbol),
            "quantity": quantity,
            "price": round(price, 4),
            "market_value": round(quantity * price, 4),
            "currency": str(row.get("currency") or "USD"),
            "price_timestamp": timestamp,
            "stale_price": stale,
        }

    def _price_multiplier(self, portfolio_id: str, symbol: str) -> float:
        if portfolio_id == "pf_001" and symbol == "AAPL":
            return 0.9985
        if portfolio_id == "pf_001" and symbol == "MSFT":
            return 0.9992
        if portfolio_id == "pf_002" and symbol in {"BND", "IEF", "TLT"}:
            return 0.994
        if portfolio_id == "pf_003" and symbol in {"NVDA", "QQQ"}:
            return 0.985
        return 1.0

    def _cash_adjustment(self, portfolio_id: str) -> float:
        return {
            "pf_001": -120.0,
            "pf_002": 35.0,
            "pf_003": -750.0,
            "pf_004": -420.0,
        }.get(portfolio_id, -25.0)

    def _pnl_adjustment(self, portfolio_id: str) -> float:
        return {
            "pf_001": -90.0,
            "pf_002": -420.0,
            "pf_003": -2500.0,
            "pf_004": 1450.0,
        }.get(portfolio_id, -75.0)

    def _fees(self, portfolio_id: str) -> float:
        return {"pf_003": 120.0, "pf_004": 180.0}.get(portfolio_id, 25.0)

    def _fx_rates(self, portfolio_id: str) -> dict[str, float]:
        if portfolio_id == "pf_004":
            return {"EUR": 1.082, "CAD": 0.731}
        return {"EUR": 1.084, "CAD": 0.733}

    def _external_trades(self, portfolio_id: str) -> list[dict[str, Any]]:
        if portfolio_id == "pf_003":
            return [
                {"trade_id": "ext_nvda_sell_001", "symbol": "NVDA", "action": "SELL", "quantity": 2, "price": 138.5},
            ]
        if portfolio_id == "pf_004":
            return [
                {"trade_id": "ext_vxus_buy_001", "symbol": "VXUS", "action": "BUY", "quantity": 12, "price": 63.2},
            ]
        return []

    def _is_stale_price(self, portfolio_id: str, symbol: str) -> bool:
        return (portfolio_id == "pf_002" and symbol in {"BND", "IEF", "TLT"}) or (
            portfolio_id == "pf_004" and symbol == "IEF"
        )
