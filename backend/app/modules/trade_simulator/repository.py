from sqlalchemy.orm import Session

from app.repositories.demo_data_store import DemoDataStore
from app.repositories.persistent_portfolio_store import PersistentPortfolioStore


class TradeSimulatorRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def simulation_available(self) -> bool:
        return True

    def list_portfolios(self) -> list[dict[str, object]]:
        return PersistentPortfolioStore.list_portfolios(self.db)

    def get_portfolio(self, portfolio_id: str) -> dict[str, object] | None:
        return PersistentPortfolioStore.get_portfolio(self.db, portfolio_id)

    def list_positions(self, portfolio_id: str) -> list[dict[str, object]]:
        return PersistentPortfolioStore.list_positions(self.db, portfolio_id)

    def get_asset_metadata(self, symbol: str) -> dict[str, object] | None:
        normalized_symbol = symbol.upper()
        for asset in DemoDataStore.list_assets():
            if str(asset["symbol"]).upper() == normalized_symbol:
                return asset

        return None
