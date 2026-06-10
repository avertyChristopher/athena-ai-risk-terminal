from abc import ABC, abstractmethod


class MarketDataProvider(ABC):
    @abstractmethod
    def list_assets(self) -> list[dict[str, object]]:
        raise NotImplementedError

    @abstractmethod
    def get_prices(self, symbol: str) -> list[dict[str, object]]:
        raise NotImplementedError
