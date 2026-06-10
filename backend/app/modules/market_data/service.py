from datetime import date, datetime

from fastapi import HTTPException

from app.modules.market_data.domain import (
    calculate_annualized_return,
    calculate_arithmetic_mean_return,
    calculate_beta,
    calculate_correlation,
    calculate_covariance,
    calculate_cumulative_returns,
    calculate_drawdown,
    calculate_geometric_mean_return,
    calculate_kurtosis,
    calculate_log_returns,
    calculate_max_drawdown,
    calculate_moving_average,
    calculate_percentiles,
    calculate_sharpe_ratio,
    calculate_simple_returns,
    calculate_skewness,
    calculate_standard_deviation,
    calculate_variance,
    detect_duplicate_dates,
    detect_missing_prices,
    detect_outliers,
    extract_close_prices,
    sort_price_series,
    validate_price_data,
)
from app.modules.market_data.domain.adjustments import (
    calculate_total_return,
    validate_adjusted_close,
)
from app.modules.market_data.domain.consumer_quality import (
    create_data_quality_score,
    detect_currency_mismatches,
    detect_missing_symbols,
    detect_stale_prices,
    summarize_data_quality_for_symbols,
    validate_portfolio_market_data,
)
from app.modules.market_data.domain.panels import (
    build_price_panel,
    build_returns_panel,
    detect_non_overlapping_dates,
)
from app.modules.market_data.domain.reference_data import (
    get_demo_fx_rate,
    get_risk_free_rate_proxy,
)
from app.domain.volatility import (
    calculate_annualized_volatility,
    calculate_daily_volatility,
)
from app.modules.market_data.repository import MarketDataRepository
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
    MarketDataQualityReport,
    PortfolioMarketDataQualityReport,
    PricePoint,
    PricePanelResponse,
    ReturnPoint,
    ReturnsPanelResponse,
    RiskFreeRateResponse,
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
            MarketAsset.model_validate(self._enrich_asset_metadata(asset))
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

    def get_latest_price(self, symbol: str) -> LatestPrice:
        latest_row = self._get_price_rows(symbol)[-1]
        asset = self._get_asset(symbol)
        return self._latest_price_from_row(latest_row, asset)

    def get_latest_prices(self, symbols: list[str]) -> LatestPricesResponse:
        valid_symbols, missing_symbols = self._split_valid_and_missing_symbols(symbols)
        return LatestPricesResponse(
            symbols=[symbol.upper() for symbol in symbols],
            items=[self.get_latest_price(symbol) for symbol in valid_symbols],
            missing_symbols=missing_symbols,
        )

    def get_price_panel(
        self,
        symbols: list[str],
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> PricePanelResponse:
        valid_symbols, missing_symbols = self._split_valid_and_missing_symbols(symbols)
        series_by_symbol = {
            symbol: self._filter_rows_by_date(
                self._get_price_rows(symbol),
                start_date,
                end_date,
            )
            for symbol in valid_symbols
        }
        return PricePanelResponse(
            symbols=[symbol.upper() for symbol in symbols],
            start_date=start_date,
            end_date=end_date,
            rows=build_price_panel(series_by_symbol),
            missing_symbols=missing_symbols,
            warnings=detect_non_overlapping_dates(series_by_symbol),
        )

    def get_returns_panel(
        self,
        symbols: list[str],
        start_date: str | None = None,
        end_date: str | None = None,
        return_type: str = "price_return",
    ) -> ReturnsPanelResponse:
        valid_symbols, missing_symbols = self._split_valid_and_missing_symbols(symbols)
        series_by_symbol = {
            symbol: self._filter_rows_by_date(
                self._get_price_rows(symbol),
                start_date,
                end_date,
            )
            for symbol in valid_symbols
        }
        return ReturnsPanelResponse(
            symbols=[symbol.upper() for symbol in symbols],
            return_type=return_type,
            rows=build_returns_panel(series_by_symbol, return_type),
            missing_symbols=missing_symbols,
            warnings=detect_non_overlapping_dates(series_by_symbol),
        )

    def get_aligned_returns(self, symbols: list[str]) -> ReturnsPanelResponse:
        return self.get_returns_panel(symbols=symbols)

    def get_asset_metadata(self, symbol: str) -> AssetMetadata:
        asset = self._get_asset(symbol)
        rows = self._get_price_rows(symbol)
        return AssetMetadata.model_validate(
            {
                **self._enrich_asset_metadata(asset),
                "latest_price_available": bool(rows),
                "latest_price_date": str(rows[-1]["date"]) if rows else None,
            },
        )

    def validate_asset(self, symbol: str) -> AssetValidationResponse:
        try:
            metadata = self.get_asset_metadata(symbol)
        except HTTPException:
            return AssetValidationResponse(
                symbol=symbol.upper(),
                exists=False,
                metadata=None,
                warnings=[f"{symbol.upper()} is not in the asset master."],
            )

        return AssetValidationResponse(
            symbol=symbol.upper(),
            exists=True,
            metadata=metadata,
            warnings=[],
        )

    def get_portfolio_data_quality(
        self,
        symbols: list[str],
        expected_currency: str = "USD",
    ) -> PortfolioMarketDataQualityReport:
        valid_symbols, missing_symbols = self._split_valid_and_missing_symbols(symbols)
        reports = [
            self._market_data_quality_report(symbol, expected_currency)
            for symbol in valid_symbols
        ]
        stale_symbols = [
            report.symbol for report in reports if report.stale_latest_price
        ]
        assets = [self._get_asset(symbol) for symbol in valid_symbols]
        currency_mismatches = detect_currency_mismatches(assets, expected_currency)
        report_dicts = [report.model_dump() for report in reports]
        warnings = summarize_data_quality_for_symbols(report_dicts)
        warnings.extend(
            f"{symbol}: missing from asset master."
            for symbol in missing_symbols
        )

        return PortfolioMarketDataQualityReport(
            symbols=[symbol.upper() for symbol in symbols],
            expected_currency=expected_currency.upper(),
            reports=reports,
            missing_symbols=missing_symbols,
            stale_symbols=stale_symbols,
            currency_mismatch_symbols=currency_mismatches,
            quality_score=create_data_quality_score(report_dicts),
            is_valid_for_portfolio=validate_portfolio_market_data(report_dicts)
            and not missing_symbols,
            warnings=warnings,
        )

    def get_benchmark_returns(
        self,
        symbol: str,
        return_type: str = "price_return",
    ) -> BenchmarkReturnsResponse:
        return BenchmarkReturnsResponse(
            benchmark_symbol=symbol.upper(),
            return_type=return_type,
            returns=self.get_returns(symbol),
        )

    def get_fx_rate(self, base: str, quote: str) -> FXRateResponse:
        return FXRateResponse(
            base=base.upper(),
            quote=quote.upper(),
            date=self._as_of_date().isoformat(),
            rate=get_demo_fx_rate(base, quote),
            data_source="demo",
        )

    def get_risk_free_rate(
        self,
        currency: str = "USD",
        tenor: str = "3M",
    ) -> RiskFreeRateResponse:
        return RiskFreeRateResponse(
            currency=currency.upper(),
            tenor=tenor.upper(),
            rate=get_risk_free_rate_proxy(currency, tenor),
            data_source="demo",
        )

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

    def get_analytics(self, symbol: str) -> MarketDataAnalyticsResponse:
        rows = self._get_price_rows(symbol)
        close_prices = extract_close_prices(rows)
        simple_returns = calculate_simple_returns(close_prices)
        cumulative_returns = calculate_cumulative_returns(simple_returns)
        benchmark_symbol = self._select_benchmark_symbol(symbol)
        benchmark_returns = calculate_simple_returns(
            extract_close_prices(self._get_price_rows(benchmark_symbol)),
        )
        aligned_length = min(len(simple_returns), len(benchmark_returns))
        aligned_asset_returns = simple_returns[-aligned_length:]
        aligned_benchmark_returns = benchmark_returns[-aligned_length:]
        latest_return = simple_returns[-1]
        benchmark_latest_return = benchmark_returns[-1]

        return MarketDataAnalyticsResponse(
            symbol=symbol.upper(),
            benchmark_symbol=benchmark_symbol,
            latest_price=close_prices[-1],
            latest_return=latest_return,
            holding_period_return=(close_prices[-1] / close_prices[0]) - 1.0,
            cumulative_return=cumulative_returns[-1],
            arithmetic_mean_return=calculate_arithmetic_mean_return(simple_returns),
            geometric_mean_return=calculate_geometric_mean_return(simple_returns),
            annualized_return=calculate_annualized_return(simple_returns),
            variance=calculate_variance(simple_returns),
            standard_deviation=calculate_standard_deviation(simple_returns),
            daily_volatility=calculate_daily_volatility(simple_returns),
            annualized_volatility=calculate_annualized_volatility(simple_returns),
            max_drawdown=calculate_max_drawdown(close_prices),
            skewness=calculate_skewness(simple_returns),
            kurtosis=calculate_kurtosis(simple_returns),
            percentiles=calculate_percentiles(simple_returns),
            outlier_indexes=detect_outliers(simple_returns, threshold=2.5),
            benchmark_latest_return=benchmark_latest_return,
            active_return_vs_benchmark=latest_return - benchmark_latest_return,
            correlation_with_benchmark=calculate_correlation(
                aligned_asset_returns,
                aligned_benchmark_returns,
            ),
            covariance_with_benchmark=calculate_covariance(
                aligned_asset_returns,
                aligned_benchmark_returns,
            ),
            beta_vs_benchmark=calculate_beta(
                aligned_asset_returns,
                aligned_benchmark_returns,
            ),
            sharpe_ratio=calculate_sharpe_ratio(simple_returns),
            moving_average_5=calculate_moving_average(close_prices, window=5),
            moving_average_20=calculate_moving_average(close_prices, window=20),
            momentum_5_day=self._calculate_momentum(close_prices, window=5),
            risk_free_rate_proxy=0.02,
            adjusted_close_latest=self._calculate_adjusted_close(
                symbol,
                close_prices[-1],
            ),
            corporate_action_status=self._get_corporate_action_status(symbol),
            average_volume_20=self._calculate_average_volume(rows, window=20),
            latest_dollar_volume=self._calculate_latest_dollar_volume(rows),
            liquidity_score=self._calculate_liquidity_score(rows),
            normal_distribution_coverage=self._calculate_normal_distribution_coverage(
                simple_returns,
            ),
            fx_rate_to_usd=self._get_fx_rate_to_usd(symbol),
            currency_consistency_status=self._get_currency_consistency_status(symbol),
            yield_curve_2y=0.041,
            yield_curve_10y=0.046,
            commodity_proxy_symbol="GLD",
            commodity_proxy_latest_price=226.45,
        )

    def _get_price_rows(self, symbol: str) -> list[dict[str, object]]:
        rows = sort_price_series(self.repository.get_prices(symbol))
        if not rows:
            raise HTTPException(
                status_code=404,
                detail=f"No prices found for {symbol}.",
            )

        enriched_rows = [self._enrich_price_row(row) for row in rows]
        validate_adjusted_close(enriched_rows)
        return enriched_rows

    def _select_benchmark_symbol(self, symbol: str) -> str:
        normalized_symbol = symbol.upper()
        return "QQQ" if normalized_symbol == "SPY" else "SPY"

    def _calculate_momentum(self, prices: list[float], window: int) -> float | None:
        if len(prices) <= window:
            return None

        return (prices[-1] / prices[-window - 1]) - 1.0

    def _calculate_adjusted_close(self, symbol: str, latest_close: float) -> float:
        adjustment_factors = {
            "AAPL": 0.998,
            "MSFT": 0.997,
            "NVDA": 1.0,
            "SPY": 0.996,
            "BND": 0.995,
            "QQQ": 0.996,
        }
        return latest_close * adjustment_factors.get(symbol.upper(), 1.0)

    def _get_corporate_action_status(self, symbol: str) -> str:
        corporate_actions = {
            "AAPL": "Dividend adjustment active",
            "MSFT": "Dividend adjustment active",
            "NVDA": "No current corporate action",
            "SPY": "ETF distribution adjustment active",
            "BND": "ETF income distribution adjustment active",
            "QQQ": "ETF distribution adjustment active",
        }
        return corporate_actions.get(symbol.upper(), "No current corporate action")

    def _calculate_average_volume(
        self,
        rows: list[dict[str, object]],
        window: int,
    ) -> float:
        volumes = [float(row["volume"]) for row in rows[-window:]]
        return sum(volumes) / len(volumes)

    def _calculate_latest_dollar_volume(self, rows: list[dict[str, object]]) -> float:
        latest_row = rows[-1]
        return float(latest_row["close"]) * float(latest_row["volume"])

    def _calculate_liquidity_score(self, rows: list[dict[str, object]]) -> float:
        average_volume = self._calculate_average_volume(rows, window=min(20, len(rows)))
        latest_dollar_volume = self._calculate_latest_dollar_volume(rows)
        volume_score = min(average_volume / 50_000_000, 1.0)
        dollar_volume_score = min(latest_dollar_volume / 5_000_000_000, 1.0)
        return (volume_score + dollar_volume_score) / 2

    def _calculate_normal_distribution_coverage(self, returns: list[float]) -> float:
        average_return = calculate_arithmetic_mean_return(returns)
        standard_deviation = calculate_standard_deviation(returns)

        if standard_deviation == 0:
            return 1.0

        lower_bound = average_return - standard_deviation
        upper_bound = average_return + standard_deviation
        observations_inside_band = [
            value for value in returns if lower_bound <= value <= upper_bound
        ]
        return len(observations_inside_band) / len(returns)

    def _get_fx_rate_to_usd(self, symbol: str) -> float:
        asset = self._get_asset(symbol)
        return 1.0 if asset["currency"] == "USD" else 0.73

    def _get_currency_consistency_status(self, symbol: str) -> str:
        asset = self._get_asset(symbol)
        return f"{asset['currency']} prices; USD analytics base"

    def _get_asset(self, symbol: str) -> dict[str, object]:
        normalized_symbol = symbol.upper()
        for asset in self.repository.list_assets():
            if str(asset["symbol"]).upper() == normalized_symbol:
                return asset

        raise HTTPException(status_code=404, detail=f"Asset not found for {symbol}.")

    def _split_valid_and_missing_symbols(
        self,
        symbols: list[str],
    ) -> tuple[list[str], list[str]]:
        requested_symbols = [symbol.strip().upper() for symbol in symbols if symbol.strip()]
        available_symbols = self.repository.get_supported_symbols()
        missing_symbols = detect_missing_symbols(requested_symbols, available_symbols)
        valid_symbols = [
            symbol
            for symbol in requested_symbols
            if symbol not in missing_symbols
        ]
        return valid_symbols, missing_symbols

    def _enrich_asset_metadata(
        self,
        asset: dict[str, object],
    ) -> dict[str, object]:
        symbol = str(asset["symbol"]).upper()
        asset_type = str(asset["asset_type"]).lower()
        return {
            **asset,
            "exchange": asset.get("exchange") or ("NASDAQ" if symbol != "SPY" else "NYSE Arca"),
            "industry": asset.get("industry") or str(asset["sector"]),
            "benchmark_eligible": asset_type in {"etf", "equity"},
            "is_etf": asset_type == "etf",
            "is_index": symbol in {"SPY", "QQQ"},
            "is_fx_pair": False,
            "is_commodity": False,
            "data_source": "demo",
            "primary_benchmark": "SPY" if symbol != "SPY" else "QQQ",
        }

    def _enrich_price_row(self, row: dict[str, object]) -> dict[str, object]:
        adjusted_close = self._calculate_adjusted_close(
            str(row["symbol"]),
            float(row["close"]),
        )
        return {
            **row,
            "adjusted_close": adjusted_close,
            "split_factor": 1.0,
            "dividend_amount": self._demo_dividend_amount(str(row["symbol"])),
            "corporate_action_flag": self._demo_dividend_amount(str(row["symbol"])) > 0,
        }

    def _latest_price_from_row(
        self,
        row: dict[str, object],
        asset: dict[str, object],
    ) -> LatestPrice:
        stale_symbols = detect_stale_prices([row], self._as_of_date())
        return LatestPrice(
            symbol=str(row["symbol"]).upper(),
            date=str(row["date"]),
            close=float(row["close"]),
            adjusted_close=float(row["adjusted_close"]),
            currency=str(asset["currency"]),
            data_source="demo",
            stale=str(row["symbol"]).upper() in stale_symbols,
        )

    def _market_data_quality_report(
        self,
        symbol: str,
        expected_currency: str,
    ) -> MarketDataQualityReport:
        quality = self.get_data_quality(symbol)
        latest = self.get_latest_price(symbol)
        asset = self._get_asset(symbol)
        currency_mismatch = str(asset["currency"]).upper() != expected_currency.upper()
        warnings = []
        if latest.stale:
            warnings.append("Stale latest price.")
        if currency_mismatch:
            warnings.append("Currency mismatch warning.")
        if quality.missing_price_dates:
            warnings.append("Missing price dates.")

        return MarketDataQualityReport(
            symbol=symbol.upper(),
            rows=quality.rows,
            missing_price_dates=quality.missing_price_dates,
            duplicate_dates=quality.duplicate_dates,
            outlier_indexes=quality.outlier_indexes,
            is_valid=quality.is_valid,
            latest_price_date=latest.date,
            stale_latest_price=latest.stale,
            currency=str(asset["currency"]),
            currency_mismatch=currency_mismatch,
            warnings=warnings,
        )

    def _filter_rows_by_date(
        self,
        rows: list[dict[str, object]],
        start_date: str | None,
        end_date: str | None,
    ) -> list[dict[str, object]]:
        return [
            row
            for row in rows
            if (start_date is None or str(row["date"]) >= start_date)
            and (end_date is None or str(row["date"]) <= end_date)
        ]

    def _as_of_date(self) -> date:
        return date.today()

    def _demo_dividend_amount(self, symbol: str) -> float:
        return {
            "AAPL": 0.24,
            "MSFT": 0.75,
            "SPY": 1.68,
            "BND": 0.22,
            "QQQ": 0.61,
        }.get(symbol.upper(), 0.0)
