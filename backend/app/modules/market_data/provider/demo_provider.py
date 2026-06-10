from app.modules.market_data.provider.base import MarketDataProvider
from app.repositories.demo_data_store import DemoDataStore


class DemoMarketDataProvider(MarketDataProvider):
    def list_assets(self) -> list[dict[str, object]]:
        return DemoDataStore.list_assets()

    def get_prices(self, symbol: str) -> list[dict[str, object]]:
        return DemoDataStore.list_prices(symbol)
