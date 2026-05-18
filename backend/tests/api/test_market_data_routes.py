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
