from sqlalchemy.orm import Session

from app.repositories.demo_data_store import DemoDataStore


class MarketDataRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_supported_symbols(self) -> list[str]:
        return [asset["symbol"] for asset in DemoDataStore.list_assets()]

    def list_assets(self) -> list[dict[str, object]]:
        return DemoDataStore.list_assets()

    def get_prices(self, symbol: str) -> list[dict[str, object]]:
        return DemoDataStore.list_prices(symbol)
