import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_market_data_returns_are_available() -> None:
    response = client.get("/api/market-data/returns/AAPL")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 23
    assert body[0]["symbol"] == "AAPL"
    assert body[0]["simple_return"] == pytest.approx(0.006895065718595167)


def test_market_data_volatility_is_annualized() -> None:
    response = client.get("/api/market-data/volatility/AAPL")

    assert response.status_code == 200
    body = response.json()
    assert body["daily_volatility"] > 0
    assert body["annualized_volatility"] > body["daily_volatility"]


def test_market_data_quality_response() -> None:
    response = client.get("/api/market-data/data-quality/AAPL")

    assert response.status_code == 200
    body = response.json()
    assert body["rows"] == 24
    assert body["missing_price_dates"] == []
    assert body["duplicate_dates"] == []
    assert body["is_valid"] is True


def test_market_data_analytics_response() -> None:
    response = client.get("/api/market-data/analytics/AAPL")

    assert response.status_code == 200
    body = response.json()
    assert body["symbol"] == "AAPL"
    assert body["benchmark_symbol"] == "SPY"
    assert body["latest_price"] > 191.0
    assert body["annualized_volatility"] > 0
    assert body["max_drawdown"] < 0
    assert "p50" in body["percentiles"]
    assert body["moving_average_20"] is not None
    assert body["average_volume_20"] > 0
    assert body["latest_dollar_volume"] > 0
    assert body["liquidity_score"] > 0
    assert body["normal_distribution_coverage"] > 0
    assert body["fx_rate_to_usd"] == 1.0


def test_market_data_latest_prices_batch_response() -> None:
    response = client.get("/api/market-data/latest-prices?symbols=AAPL,MSFT,XXX")

    assert response.status_code == 200
    body = response.json()
    assert body["missing_symbols"] == ["XXX"]
    assert len(body["items"]) == 2
    assert body["items"][0]["adjusted_close"] > 0


def test_market_data_price_and_returns_panels_are_aligned() -> None:
    price_response = client.get("/api/market-data/price-panel?symbols=AAPL,MSFT,NVDA")
    returns_response = client.get("/api/market-data/returns-panel?symbols=AAPL,MSFT,NVDA")

    assert price_response.status_code == 200
    assert returns_response.status_code == 200
    price_body = price_response.json()
    returns_body = returns_response.json()
    assert price_body["rows"]
    assert returns_body["rows"]
    assert {"date", "AAPL", "MSFT", "NVDA"} <= set(price_body["rows"][0])
    assert {"date", "AAPL", "MSFT", "NVDA"} <= set(returns_body["rows"][0])


def test_market_data_asset_metadata_and_validation() -> None:
    metadata_response = client.get("/api/market-data/assets/AAPL/metadata")
    validation_response = client.get("/api/market-data/assets/validate/XXX")

    assert metadata_response.status_code == 200
    assert metadata_response.json()["symbol"] == "AAPL"
    assert metadata_response.json()["latest_price_available"] is True
    assert validation_response.status_code == 200
    assert validation_response.json()["exists"] is False


def test_market_data_portfolio_quality_report_flags_missing_symbols() -> None:
    response = client.get(
        "/api/market-data/data-quality/batch?symbols=AAPL,MSFT,XXX&expected_currency=USD",
    )

    assert response.status_code == 200
    body = response.json()
    assert body["missing_symbols"] == ["XXX"]
    assert body["reports"]
    assert body["quality_score"] <= 1
    assert "XXX: missing from asset master." in body["warnings"]


def test_market_data_import_prices_adds_portfolio_coverage() -> None:
    import_response = client.post(
        "/api/market-data/import-prices",
        json={
            "rows": [
                {
                    "date": "2026-06-15",
                    "symbol": "TEST",
                    "open": 100.0,
                    "high": 103.0,
                    "low": 99.5,
                    "close": 102.0,
                    "volume": 125000,
                    "name": "Imported Test Equity",
                    "sector": "Testing",
                    "country": "United States",
                },
                {
                    "date": "2026-06-16",
                    "symbol": "TEST",
                    "open": 102.0,
                    "high": 104.0,
                    "low": 101.0,
                    "close": 103.5,
                    "volume": 130000,
                    "name": "Imported Test Equity",
                    "sector": "Testing",
                    "country": "United States",
                },
            ],
        },
    )
    coverage_response = client.get("/api/market-data/coverage?symbols=TEST,UNKNOWN")
    latest_response = client.get("/api/market-data/latest/TEST")

    assert import_response.status_code == 200
    assert import_response.json()["imported_symbols"] == ["TEST"]
    assert coverage_response.status_code == 200
    coverage_body = coverage_response.json()
    assert coverage_body["covered_symbols"] == ["TEST"]
    assert coverage_body["missing_symbols"] == ["UNKNOWN"]
    assert coverage_body["coverage_ratio"] == pytest.approx(0.5)
    assert coverage_body["latest_price_dates"]["TEST"] == "2026-06-16"
    assert latest_response.status_code == 200
    assert latest_response.json()["close"] == pytest.approx(103.5)
    assert latest_response.json()["data_source"] == "imported"


def test_market_data_benchmark_fx_and_risk_free_endpoints() -> None:
    benchmark_response = client.get("/api/market-data/benchmark/SPY/returns")
    fx_response = client.get("/api/market-data/fx/latest?base=USD&quote=CAD")
    risk_free_response = client.get("/api/market-data/risk-free-rate")

    assert benchmark_response.status_code == 200
    assert benchmark_response.json()["benchmark_symbol"] == "SPY"
    assert benchmark_response.json()["returns"]
    assert fx_response.status_code == 200
    assert fx_response.json()["rate"] == pytest.approx(1.37)
    assert risk_free_response.status_code == 200
    assert risk_free_response.json()["rate"] == pytest.approx(0.04)


def test_market_data_cors_allows_localhost_and_loopback_frontend() -> None:
    response = client.options(
        "/api/market-data/assets",
        headers={
            "Origin": "http://127.0.0.1:5173",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://127.0.0.1:5173"
