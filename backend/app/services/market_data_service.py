from app.repositories.market_data_repository import MarketDataRepository
from app.schemas.market_data_schema import MarketDataModuleStatus


class MarketDataService:
    def __init__(self, repository: MarketDataRepository) -> None:
        self.repository = repository

    def get_module_status(self) -> MarketDataModuleStatus:
        return MarketDataModuleStatus(
            module="market-data",
            detail="Market data provider integration will be added in a later increment.",
            assets_tracked=len(self.repository.get_supported_symbols()),
        )
