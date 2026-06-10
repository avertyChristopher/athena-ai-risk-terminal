from app.modules.market_data.provider.base import MarketDataProvider
from app.modules.market_data.provider.demo_provider import DemoMarketDataProvider


def get_market_data_provider(provider_name: str = "demo") -> MarketDataProvider:
    if provider_name == "demo":
        return DemoMarketDataProvider()
    raise ValueError(f"Unsupported market data provider: {provider_name}.")
