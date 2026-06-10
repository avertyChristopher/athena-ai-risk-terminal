from sqlalchemy.orm import Session

from app.modules.market_data.provider import get_market_data_provider


class MarketDataRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.provider = get_market_data_provider("demo")

    def get_supported_symbols(self) -> list[str]:
        return [asset["symbol"] for asset in self.provider.list_assets()]

    def list_assets(self) -> list[dict[str, object]]:
        return self.provider.list_assets()

    def get_prices(self, symbol: str) -> list[dict[str, object]]:
        return self.provider.get_prices(symbol)
