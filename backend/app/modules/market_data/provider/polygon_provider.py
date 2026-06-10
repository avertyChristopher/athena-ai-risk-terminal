from app.modules.market_data.provider.base import MarketDataProvider


class PolygonMarketDataProvider(MarketDataProvider):
    def list_assets(self) -> list[dict[str, object]]:
        raise NotImplementedError("Polygon provider is a placeholder.")

    def get_prices(self, symbol: str) -> list[dict[str, object]]:
        raise NotImplementedError("Polygon provider is a placeholder.")
