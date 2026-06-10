from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_market_data_service
from app.modules.market_data.schemas import (
    AssetMetadata,
    AssetValidationResponse,
    BenchmarkReturnsResponse,
    DataQualityResponse,
    FXRateResponse,
    LatestPrice,
    LatestPricesResponse,
    MarketDataAnalyticsResponse,
    MarketAsset,
    MarketDataModuleStatus,
    PortfolioMarketDataQualityReport,
    PricePoint,
    PricePanelResponse,
    ReturnPoint,
    ReturnsPanelResponse,
    RiskFreeRateResponse,
    VolatilityResponse,
)
from app.modules.market_data.service import MarketDataService

router = APIRouter(prefix="/market-data", tags=["market-data"])


@router.get("/status", response_model=MarketDataModuleStatus)
def get_market_data_status(
    service: MarketDataService = Depends(get_market_data_service),
) -> MarketDataModuleStatus:
    return service.get_module_status()


@router.get("/assets", response_model=list[MarketAsset])
def list_assets(
    service: MarketDataService = Depends(get_market_data_service),
) -> list[MarketAsset]:
    return service.list_assets()


@router.get("/assets/validate/{symbol}", response_model=AssetValidationResponse)
def validate_asset(
    symbol: str,
    service: MarketDataService = Depends(get_market_data_service),
) -> AssetValidationResponse:
    return service.validate_asset(symbol)


@router.get("/assets/{symbol}/metadata", response_model=AssetMetadata)
def get_asset_metadata(
    symbol: str,
    service: MarketDataService = Depends(get_market_data_service),
) -> AssetMetadata:
    return service.get_asset_metadata(symbol)


@router.get("/latest/{symbol}", response_model=LatestPrice)
def get_latest_price(
    symbol: str,
    service: MarketDataService = Depends(get_market_data_service),
) -> LatestPrice:
    return service.get_latest_price(symbol)


@router.get("/latest-prices", response_model=LatestPricesResponse)
def get_latest_prices(
    symbols: str = Query(...),
    service: MarketDataService = Depends(get_market_data_service),
) -> LatestPricesResponse:
    return service.get_latest_prices(_parse_symbols(symbols))


@router.get("/price-panel", response_model=PricePanelResponse)
def get_price_panel(
    symbols: str = Query(...),
    start_date: str | None = None,
    end_date: str | None = None,
    service: MarketDataService = Depends(get_market_data_service),
) -> PricePanelResponse:
    return service.get_price_panel(_parse_symbols(symbols), start_date, end_date)


@router.get("/returns-panel", response_model=ReturnsPanelResponse)
def get_returns_panel(
    symbols: str = Query(...),
    start_date: str | None = None,
    end_date: str | None = None,
    return_type: str = "price_return",
    service: MarketDataService = Depends(get_market_data_service),
) -> ReturnsPanelResponse:
    return service.get_returns_panel(
        _parse_symbols(symbols),
        start_date,
        end_date,
        return_type,
    )


@router.get("/aligned-returns", response_model=ReturnsPanelResponse)
def get_aligned_returns(
    symbols: str = Query(...),
    service: MarketDataService = Depends(get_market_data_service),
) -> ReturnsPanelResponse:
    return service.get_aligned_returns(_parse_symbols(symbols))


@router.get("/prices/{symbol}", response_model=list[PricePoint])
def get_prices(
    symbol: str,
    service: MarketDataService = Depends(get_market_data_service),
) -> list[PricePoint]:
    return service.get_prices(symbol)


@router.get("/returns/{symbol}", response_model=list[ReturnPoint])
def get_returns(
    symbol: str,
    service: MarketDataService = Depends(get_market_data_service),
) -> list[ReturnPoint]:
    return service.get_returns(symbol)


@router.get("/volatility/{symbol}", response_model=VolatilityResponse)
def get_volatility(
    symbol: str,
    service: MarketDataService = Depends(get_market_data_service),
) -> VolatilityResponse:
    return service.get_volatility(symbol)


@router.get("/data-quality/batch", response_model=PortfolioMarketDataQualityReport)
def get_batch_data_quality(
    symbols: str = Query(...),
    expected_currency: str = "USD",
    service: MarketDataService = Depends(get_market_data_service),
) -> PortfolioMarketDataQualityReport:
    return service.get_portfolio_data_quality(
        _parse_symbols(symbols),
        expected_currency,
    )


@router.get("/data-quality/{symbol}", response_model=DataQualityResponse)
def get_data_quality(
    symbol: str,
    service: MarketDataService = Depends(get_market_data_service),
) -> DataQualityResponse:
    return service.get_data_quality(symbol)


@router.get("/analytics/{symbol}", response_model=MarketDataAnalyticsResponse)
def get_analytics(
    symbol: str,
    service: MarketDataService = Depends(get_market_data_service),
) -> MarketDataAnalyticsResponse:
    return service.get_analytics(symbol)


@router.get("/benchmark/{symbol}/returns", response_model=BenchmarkReturnsResponse)
def get_benchmark_returns(
    symbol: str,
    return_type: str = "price_return",
    service: MarketDataService = Depends(get_market_data_service),
) -> BenchmarkReturnsResponse:
    return service.get_benchmark_returns(symbol, return_type)


@router.get("/fx/latest", response_model=FXRateResponse)
def get_latest_fx_rate(
    base: str = Query(...),
    quote: str = Query(...),
    service: MarketDataService = Depends(get_market_data_service),
) -> FXRateResponse:
    return service.get_fx_rate(base, quote)


@router.get("/risk-free-rate", response_model=RiskFreeRateResponse)
def get_risk_free_rate(
    currency: str = "USD",
    tenor: str = "3M",
    service: MarketDataService = Depends(get_market_data_service),
) -> RiskFreeRateResponse:
    return service.get_risk_free_rate(currency, tenor)


def _parse_symbols(symbols: str) -> list[str]:
    return [symbol.strip().upper() for symbol in symbols.split(",") if symbol.strip()]
