from __future__ import annotations

from math import sqrt
from statistics import stdev

from sqlalchemy.orm import Session

from app.modules.market_data.repository import MarketDataRepository
from app.repositories.persistent_portfolio_store import PersistentPortfolioStore


class StressTestingRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.market_data = MarketDataRepository(db)

    def get_portfolio(self, portfolio_id: str) -> dict[str, object] | None:
        return PersistentPortfolioStore.get_portfolio(self.db, portfolio_id)

    def list_positions(self, portfolio_id: str) -> list[dict[str, object]]:
        return PersistentPortfolioStore.list_positions(self.db, portfolio_id)

    def get_latest_price(self, symbol: str) -> float | None:
        rows = self.market_data.get_prices(symbol)
        if not rows:
            return None
        latest = sorted(rows, key=lambda row: str(row.get("date", "")))[-1]
        close = latest.get("close")
        return float(close) if close is not None else None

    def get_symbol_returns(self, symbol: str) -> list[float]:
        rows = sorted(
            self.market_data.get_prices(symbol),
            key=lambda row: str(row.get("date", "")),
        )
        returns = []
        previous_close: float | None = None
        for row in rows:
            close = float(row.get("close", 0.0))
            if previous_close and previous_close > 0:
                returns.append(close / previous_close - 1.0)
            previous_close = close
        return returns

    def estimate_portfolio_volatility(
        self,
        positions: list[dict[str, object]],
        portfolio_value: float,
    ) -> tuple[float, list[str], list[str]]:
        if portfolio_value <= 0:
            return 0.186, [], ["Portfolio value is zero; volatility uses demo fallback."]

        weighted_variance = 0.0
        symbols_found: list[str] = []
        symbols_missing: list[str] = []

        for position in positions:
            symbol = str(position.get("symbol", "")).upper()
            market_value = float(position.get("quantity", 0.0)) * float(
                position.get("current_price", 0.0)
            )
            returns = self.get_symbol_returns(symbol)
            if len(returns) < 2:
                symbols_missing.append(symbol)
                continue
            symbols_found.append(symbol)
            annualized_vol = stdev(returns) * sqrt(252)
            weight = market_value / portfolio_value
            weighted_variance += (weight * annualized_vol) ** 2

        if not symbols_found:
            return 0.186, symbols_found, symbols_missing

        return max(weighted_variance**0.5, 0.03), symbols_found, symbols_missing
