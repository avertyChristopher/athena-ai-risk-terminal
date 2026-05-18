from fastapi import HTTPException

from app.domain.market_data import (
    calculate_cumulative_returns,
    calculate_drawdown,
    calculate_log_returns,
    calculate_simple_returns,
    detect_duplicate_dates,
    detect_missing_prices,
    detect_outliers,
    extract_close_prices,
    sort_price_series,
    validate_price_data,
)
from app.domain.volatility import (
    calculate_annualized_volatility,
    calculate_daily_volatility,
)
from app.repositories.market_data_repository import MarketDataRepository
from app.schemas.market_data_schema import (
    DataQualityResponse,
    MarketAsset,
    MarketDataModuleStatus,
    PricePoint,
    ReturnPoint,
    VolatilityResponse,
)


class MarketDataService:
    def __init__(self, repository: MarketDataRepository) -> None:
        self.repository = repository

    def get_module_status(self) -> MarketDataModuleStatus:
        return MarketDataModuleStatus(
            module="market-data",
            detail="Demo market data is loaded and ready for analytics.",
            assets_tracked=len(self.repository.get_supported_symbols()),
        )

    def list_assets(self) -> list[MarketAsset]:
        return [
            MarketAsset.model_validate(asset)
            for asset in self.repository.list_assets()
        ]

    def get_prices(self, symbol: str) -> list[PricePoint]:
        rows = self._get_price_rows(symbol)
        return [PricePoint.model_validate(row) for row in rows]

    def get_returns(self, symbol: str) -> list[ReturnPoint]:
        rows = self._get_price_rows(symbol)
        close_prices = extract_close_prices(rows)
        simple_returns = calculate_simple_returns(close_prices)
        log_returns = calculate_log_returns(close_prices)
        cumulative_returns = calculate_cumulative_returns(simple_returns)
        drawdowns = calculate_drawdown(close_prices)

        sorted_rows = sort_price_series(rows)
        return [
            ReturnPoint(
                date=str(sorted_rows[index]["date"]),
                symbol=symbol.upper(),
                simple_return=simple_return,
                log_return=log_return,
                cumulative_return=cumulative_return,
                drawdown=drawdowns[index],
            )
            for index, (simple_return, log_return, cumulative_return) in enumerate(
                zip(simple_returns, log_returns, cumulative_returns),
                start=1,
            )
        ]

    def get_volatility(self, symbol: str) -> VolatilityResponse:
        close_prices = extract_close_prices(self._get_price_rows(symbol))
        simple_returns = calculate_simple_returns(close_prices)

        return VolatilityResponse(
            symbol=symbol.upper(),
            daily_volatility=calculate_daily_volatility(simple_returns),
            annualized_volatility=calculate_annualized_volatility(simple_returns),
        )

    def get_data_quality(self, symbol: str) -> DataQualityResponse:
        rows = self._get_price_rows(symbol)
        close_prices = extract_close_prices(rows)

        return DataQualityResponse(
            symbol=symbol.upper(),
            rows=len(rows),
            missing_price_dates=detect_missing_prices(rows),
            duplicate_dates=detect_duplicate_dates(rows),
            outlier_indexes=detect_outliers(close_prices, threshold=2.5),
            is_valid=validate_price_data(rows),
        )

    def _get_price_rows(self, symbol: str) -> list[dict[str, object]]:
        rows = sort_price_series(self.repository.get_prices(symbol))
        if not rows:
            raise HTTPException(
                status_code=404,
                detail=f"No prices found for {symbol}.",
            )

        return rows
