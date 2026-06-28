from __future__ import annotations

from datetime import date
from typing import Any

from sqlalchemy.orm import Session

from app.modules.market_data.repository import MarketDataRepository
from app.modules.pnl_attribution.schemas import PnlAttributionResult
from app.modules.portfolio_builder.repository import PortfolioRepository, PositionRepository
from app.persistence.repositories import PnlAnalysisPersistenceRepository, TradeBlotterPersistenceRepository


class PnlAttributionRepository:
    _history: dict[str, PnlAttributionResult] = {}

    def __init__(self, db: Session | None = None) -> None:
        self.db = db
        self.portfolios = PortfolioRepository(db) if db is not None else None
        self.positions = PositionRepository(db) if db is not None else None
        self.market_data = MarketDataRepository(db) if db is not None else None
        self.persistence = PnlAnalysisPersistenceRepository(db)
        self.trade_blotter = TradeBlotterPersistenceRepository(db)

    def get_portfolio(self, portfolio_id: str) -> dict[str, Any] | None:
        if self.portfolios is None:
            return None
        return self.portfolios.get_portfolio(portfolio_id)

    def list_positions(self, portfolio_id: str) -> list[dict[str, Any]]:
        if self.positions is None:
            return []
        return self.positions.list_positions(portfolio_id)

    def get_price_snapshot(
        self,
        symbol: str,
        start_date: date,
        end_date: date,
    ) -> dict[str, Any]:
        if self.market_data is None:
            return {"warnings": ["Market Data repository unavailable."]}
        rows = self.market_data.get_prices(symbol)
        filtered = [
            row
            for row in rows
            if start_date.isoformat() <= str(row["date"]) <= end_date.isoformat()
        ]
        if len(filtered) >= 2:
            return {
                "starting_price": float(filtered[0]["close"]),
                "ending_price": float(filtered[-1]["close"]),
                "starting_date": str(filtered[0]["date"]),
                "ending_date": str(filtered[-1]["date"]),
                "data_source": "Market Data demo price history",
                "warnings": [],
            }
        if rows:
            return {
                "starting_price": float(rows[0]["close"]),
                "ending_price": float(rows[-1]["close"]),
                "starting_date": str(rows[0]["date"]),
                "ending_date": str(rows[-1]["date"]),
                "data_source": "Market Data full demo history fallback",
                "warnings": [f"{symbol}: no full price coverage for selected period; full demo range used."],
            }
        return {"warnings": [f"{symbol}: no Market Data prices found; Portfolio Builder prices used."]}

    def save(self, analysis: PnlAttributionResult) -> PnlAttributionResult:
        self._history[analysis.analysis_id] = analysis
        self.persistence.save(analysis)
        return analysis

    def list_history(self) -> list[PnlAttributionResult]:
        persisted = self.persistence.list()
        if persisted:
            return persisted
        return sorted(
            self._history.values(),
            key=lambda analysis: analysis.generated_at,
            reverse=True,
        )

    def get(self, analysis_id: str) -> PnlAttributionResult | None:
        return self.persistence.get(analysis_id) or self._history.get(analysis_id)

    def delete(self, analysis_id: str) -> bool:
        deleted_from_memory = self._history.pop(analysis_id, None) is not None
        return self.persistence.delete(analysis_id) or deleted_from_memory

    def clear(self) -> None:
        self._history.clear()
        self.persistence.clear()

    def list_trade_blotter_entries(
        self,
        portfolio_id: str,
        start_date: date,
        end_date: date,
    ) -> list[dict[str, Any]]:
        rows = self.trade_blotter.list()
        allowed_statuses = {"approved", "simulated", "pending_review"}
        selected: list[dict[str, Any]] = []
        for row in rows:
            if str(row.get("portfolio_id")) != portfolio_id:
                continue
            if str(row.get("status") or "").lower() not in allowed_statuses:
                continue
            trade_date = str(row.get("trade_date") or "")[:10]
            if trade_date and not (start_date.isoformat() <= trade_date <= end_date.isoformat()):
                continue
            selected.append(row)
        return selected
