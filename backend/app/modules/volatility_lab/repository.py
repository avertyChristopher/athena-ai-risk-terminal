from sqlalchemy.orm import Session

from app.modules.market_data.repository import MarketDataRepository
from app.modules.portfolio_builder.repository import (
    PortfolioRepository,
    PositionRepository,
)


class VolatilityLabRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.market_data = MarketDataRepository(db)
        self.portfolios = PortfolioRepository(db)
        self.positions = PositionRepository(db)

    def get_prices(self, symbol: str) -> list[dict[str, object]]:
        return self.market_data.get_prices(symbol)

    def get_portfolio(self, portfolio_id: str) -> dict[str, object] | None:
        return self.portfolios.get_portfolio(portfolio_id)

    def list_positions(self, portfolio_id: str) -> list[dict[str, object]]:
        return self.positions.list_positions(portfolio_id)
