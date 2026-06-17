from sqlalchemy.orm import Session

from app.modules.market_data.provider import get_market_data_provider
from app.repositories.persistent_market_data_store import PersistentMarketDataStore


class MarketDataRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.provider = get_market_data_provider("demo")

    def get_supported_symbols(self) -> list[str]:
        return [asset["symbol"] for asset in self.list_assets()]

    def list_assets(self) -> list[dict[str, object]]:
        assets_by_symbol = {
            str(asset["symbol"]).upper(): asset
            for asset in self.provider.list_assets()
        }

        for asset in PersistentMarketDataStore.list_assets(self.db):
            symbol = str(asset["symbol"]).upper()
            if symbol not in assets_by_symbol:
                assets_by_symbol[symbol] = asset

        return list(assets_by_symbol.values())

    def get_prices(self, symbol: str) -> list[dict[str, object]]:
        rows_by_date = {
            str(row["date"]): row
            for row in self.provider.get_prices(symbol)
        }

        for row in PersistentMarketDataStore.get_prices(self.db, symbol):
            rows_by_date[str(row["date"])] = row

        return list(rows_by_date.values())

    def import_prices(
        self,
        rows: list[dict[str, object]],
    ) -> tuple[int, list[str]]:
        return PersistentMarketDataStore.import_prices(self.db, rows)
