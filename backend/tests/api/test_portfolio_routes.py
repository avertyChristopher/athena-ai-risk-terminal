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
    assert body["total_market_value"] == 77692.0
    assert body["invested_value"] == 72692.0
    assert body["largest_position"] == "NVDA"
    assert body["data_source"] == "Athena SQLite portfolio store seeded from demo data"
    assert body["number_of_positions"] == 5


def test_portfolio_management_foundation_endpoints_return_data() -> None:
    endpoints = [
        "/api/portfolios/pf_001/concentration",
        "/api/portfolios/pf_001/diversification",
        "/api/portfolios/pf_001/risk-return",
        "/api/portfolios/pf_001/benchmark",
        "/api/portfolios/pf_001/policy",
        "/api/portfolios/pf_001/target-allocation",
        "/api/portfolios/pf_001/rebalancing-preview",
        "/api/portfolios/pf_001/performance-measurement",
        "/api/portfolios/pf_001/constraints",
        "/api/portfolios/pf_001/diagnostics",
        "/api/portfolios/pf_001/market-data-integration",
        "/api/portfolios/pf_001/cfa-concepts",
    ]

    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200
        assert response.json()["portfolio_id"] == "pf_001"


def test_portfolio_cfa_concepts_expose_level_one_sections() -> None:
    response = client.get("/api/portfolios/pf_001/cfa-concepts")

    assert response.status_code == 200
    body = response.json()
    assert body["portfolio_id"] == "pf_001"
    assert body["investor_profile"]["investor_type"] == "Individual"
    assert body["risk_tolerance"]["overall_risk_tolerance"] == "Moderate"
    assert "utility_score" in body["utility"]
    assert "portfolio_beta" in body["capm"]
    assert "sharpe_ratio" in body["risk_adjusted_performance"]
    assert len(body["efficient_frontier"]["points"]) == 3


def test_portfolio_market_data_integration_exposes_readiness_plan() -> None:
    response = client.get("/api/portfolios/pf_001/market-data-integration")

    assert response.status_code == 200
    body = response.json()
    assert body["portfolio_id"] == "pf_001"
    assert "AAPL" in body["symbols"]
    assert "returns-panel" in body["return_series_endpoint"]
    assert "Requires Market Data" in body["readiness_badges"]
    assert "deterministic demo assumptions" in body["integration_message"]


def test_portfolio_risk_return_uses_market_data_returns_when_available() -> None:
    response = client.get("/api/portfolios/pf_001/risk-return")

    assert response.status_code == 200
    body = response.json()
    assert body["metric_source"] == "realized_market_data"
    assert body["fallback_used"] is False
    assert body["observations"] >= 2
    assert body["realized_volatility"] is not None
    assert body["realized_sharpe_ratio"] is not None
    assert body["historical_var_95"] is not None
    assert body["historical_cvar_95"] is not None
    assert "SPY" in body["symbols_found"]


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
    assert position["portfolio_weight"] == 2 / 3
    assert position["invested_weight"] == 1
    assert position["cost_basis"] == 1800
    assert position["unrealized_pnl"] == 200

    summary_response = client.get(f"/api/portfolios/{portfolio_id}/summary")
    assert summary_response.json()["total_value"] == 3000

    delete_response = client.delete(
        f"/api/portfolios/{portfolio_id}/positions/{position['id']}",
    )
    assert delete_response.status_code == 200

    updated_summary_response = client.get(f"/api/portfolios/{portfolio_id}/summary")
    assert updated_summary_response.json()["total_value"] == 1000


def test_update_position_recalculates_values_and_metadata() -> None:
    portfolio_response = client.post(
        "/api/portfolios",
        json={
            "name": "Update Position Portfolio",
            "base_currency": "USD",
            "benchmark": "SPY",
            "cash": 500,
        },
    )
    portfolio_id = portfolio_response.json()["id"]

    position_response = client.post(
        f"/api/portfolios/{portfolio_id}/positions",
        json={
            "symbol": "AAPL",
            "asset_name": "Apple Inc.",
            "name": "Apple demo line",
            "asset_type": "equity",
            "quantity": 10,
            "average_price": 180,
            "current_price": 200,
            "currency": "USD",
            "sector": "Technology",
            "country": "United States",
            "exchange": "NASDAQ",
            "industry": "Consumer Electronics",
            "region": "North America",
        },
    )
    position_id = position_response.json()["id"]

    update_response = client.put(
        f"/api/portfolios/{portfolio_id}/positions/{position_id}",
        json={
            "symbol": "MSFT",
            "asset_name": "Microsoft Corporation",
            "name": "Microsoft edited line",
            "quantity": 4,
            "average_price": 300,
            "current_price": 350,
            "sector": "Software",
            "industry": "Infrastructure Software",
        },
    )

    assert update_response.status_code == 200
    position = update_response.json()
    assert position["symbol"] == "MSFT"
    assert position["asset_name"] == "Microsoft Corporation"
    assert position["name"] == "Microsoft edited line"
    assert position["quantity"] == 4
    assert position["market_value"] == 1400
    assert position["cost_basis"] == 1200
    assert position["unrealized_pnl"] == 200
    assert position["sector"] == "Software"
    assert position["exchange"] == "NASDAQ"
    assert position["industry"] == "Infrastructure Software"


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
