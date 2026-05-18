import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_market_data_returns_are_available() -> None:
    response = client.get("/api/market-data/returns/AAPL")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 7
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
    assert body["rows"] == 8
    assert body["missing_price_dates"] == []
    assert body["duplicate_dates"] == []
    assert body["is_valid"] is True
