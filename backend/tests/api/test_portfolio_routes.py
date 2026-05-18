from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_portfolio_summary_uses_demo_positions() -> None:
    response = client.get("/api/portfolios/pf_001/summary")

    assert response.status_code == 200
    body = response.json()
    assert body["portfolio_id"] == "pf_001"
    assert body["name"] == "Athena Demo Portfolio"
    assert body["total_value"] == 77692.0
    assert body["number_of_positions"] == 5


def test_portfolio_can_be_created() -> None:
    response = client.post(
        "/api/portfolios",
        json={
            "name": "Regression Test Portfolio",
            "base_currency": "CAD",
            "benchmark": "SPY",
            "cash": 0,
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Regression Test Portfolio"
    assert body["base_currency"] == "CAD"

    summary_response = client.get(f"/api/portfolios/{body['id']}/summary")
    assert summary_response.status_code == 200
    assert summary_response.json()["total_value"] == 0


def test_portfolio_name_is_required() -> None:
    response = client.post(
        "/api/portfolios",
        json={"name": "", "base_currency": "CAD", "benchmark": "SPY", "cash": 0},
    )

    assert response.status_code == 422


def test_base_currency_is_required() -> None:
    response = client.post(
        "/api/portfolios",
        json={"name": "No Currency", "base_currency": "", "benchmark": "SPY"},
    )

    assert response.status_code == 422


def test_position_lifecycle_updates_portfolio_summary() -> None:
    portfolio_response = client.post(
        "/api/portfolios",
        json={
            "name": "Position Lifecycle Portfolio",
            "base_currency": "USD",
            "benchmark": "SPY",
            "cash": 1000,
        },
    )
    portfolio_id = portfolio_response.json()["id"]

    position_response = client.post(
        f"/api/portfolios/{portfolio_id}/positions",
        json={
            "symbol": "AAPL",
            "asset_name": "Apple Inc.",
            "asset_type": "equity",
            "quantity": 10,
            "average_price": 180,
            "current_price": 200,
            "currency": "USD",
            "sector": "Technology",
            "country": "United States",
        },
    )

    assert position_response.status_code == 201
    position = position_response.json()
    assert position["market_value"] == 2000
    assert position["weight"] == 2 / 3

    summary_response = client.get(f"/api/portfolios/{portfolio_id}/summary")
    assert summary_response.json()["total_value"] == 3000

    delete_response = client.delete(
        f"/api/portfolios/{portfolio_id}/positions/{position['id']}",
    )
    assert delete_response.status_code == 200

    updated_summary_response = client.get(f"/api/portfolios/{portfolio_id}/summary")
    assert updated_summary_response.json()["total_value"] == 1000


def test_position_with_negative_quantity_is_rejected() -> None:
    response = client.post(
        "/api/portfolios/pf_001/positions",
        json={
            "symbol": "AAPL",
            "asset_name": "Apple Inc.",
            "asset_type": "equity",
            "quantity": -1,
            "average_price": 180,
            "current_price": 200,
            "currency": "USD",
            "sector": "Technology",
            "country": "United States",
        },
    )

    assert response.status_code == 422


def test_position_with_negative_price_is_rejected() -> None:
    response = client.post(
        "/api/portfolios/pf_001/positions",
        json={
            "symbol": "AAPL",
            "asset_name": "Apple Inc.",
            "asset_type": "equity",
            "quantity": 1,
            "average_price": 180,
            "current_price": -200,
            "currency": "USD",
            "sector": "Technology",
            "country": "United States",
        },
    )

    assert response.status_code == 422
