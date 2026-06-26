import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


DEMO_PORTFOLIO_IDS = ("pf_001", "pf_002", "pf_003", "pf_004")


def test_portfolio_summary_uses_demo_positions() -> None:
    response = client.get("/api/portfolios/pf_001/summary")

    assert response.status_code == 200
    body = response.json()
    assert body["portfolio_id"] == "pf_001"
    assert body["name"] == "Athena Balanced Growth Portfolio"
    assert body["total_value"] == pytest.approx(250000.0, rel=1e-5)
    assert body["total_market_value"] == pytest.approx(250000.0, rel=1e-5)
    assert body["invested_value"] == pytest.approx(237500.0, rel=1e-5)
    assert body["cash_weight"] == pytest.approx(0.05, rel=1e-5)
    assert body["largest_position"] == "SPY"
    assert body["data_source"] == "Athena SQLite portfolio store seeded from demo data"
    assert body["number_of_positions"] == 9


def test_portfolio_list_includes_realistic_demo_profiles() -> None:
    response = client.get("/api/portfolios")

    assert response.status_code == 200
    portfolios = response.json()["items"]
    by_id = {portfolio["id"]: portfolio for portfolio in portfolios}
    assert set(DEMO_PORTFOLIO_IDS) <= set(by_id)
    assert by_id["pf_001"]["name"] == "Athena Balanced Growth Portfolio"
    assert by_id["pf_001"]["demo_profile"] is True
    assert by_id["pf_001"]["strategy_type"] == "Balanced Growth"
    assert by_id["pf_002"]["strategy_type"] == "Conservative Income"
    assert by_id["pf_003"]["strategy_type"] == "Tech Concentration"
    assert by_id["pf_004"]["strategy_type"] == "Multi-Asset Institutional"
    assert by_id["pf_001"]["target_allocation"]
    assert by_id["pf_001"]["transaction_history"]
    assert "Market Data coverage" in by_id["pf_001"]["data_source_badges"]


def test_balanced_growth_portfolio_has_diversified_allocation() -> None:
    summary = client.get("/api/portfolios/pf_001/summary").json()
    concentration = client.get("/api/portfolios/pf_001/concentration").json()
    policy = client.get("/api/portfolios/pf_001/policy").json()

    assert summary["cash_weight"] == pytest.approx(0.05, rel=1e-5)
    assert summary["number_of_asset_classes"] >= 5
    assert concentration["largest_position_weight"] < 0.25
    assert concentration["top_3_holdings_weight"] < 0.65
    assert concentration["warnings"] == []
    assert policy["breaches"] == []
    assert {item["status"] for item in policy["comparison"]} == {"Within tolerance"}


def test_tech_concentration_portfolio_triggers_concentration_warning() -> None:
    concentration = client.get("/api/portfolios/pf_003/concentration").json()
    sectors = client.get("/api/portfolios/pf_003/allocation/sectors").json()["items"]
    technology = next(item for item in sectors if item["name"] == "Technology")

    assert concentration["largest_position_weight"] > 0.25
    assert concentration["top_3_holdings_weight"] > 0.65
    assert concentration["concentration_level"] == "High concentration"
    assert concentration["warnings"]
    assert technology["weight"] > 0.85


def test_conservative_income_portfolio_has_fixed_income_exposure() -> None:
    exposure = client.post(
        "/api/rates-lab/portfolio-exposure",
        json={"portfolio_id": "pf_002", "shock_bps": 100},
    )

    assert exposure.status_code == 200
    body = exposure.json()
    symbols = {holding["symbol"] for holding in body["fixed_income_holdings"]}
    assert {"BND", "IEF", "TLT"} <= symbols
    assert body["fixed_income_allocation"] == pytest.approx(0.55, rel=1e-4)
    assert body["weighted_average_duration"] > 7
    assert body["estimated_rate_shock_loss"] < 0


def test_multi_asset_demo_has_multiple_asset_classes() -> None:
    summary = client.get("/api/portfolios/pf_004/summary").json()
    positions = client.get("/api/portfolios/pf_004/positions").json()["items"]
    asset_classes = {position["asset_class"] for position in positions}
    symbols = {position["symbol"] for position in positions}

    assert summary["total_value"] == pytest.approx(500000.0, rel=1e-5)
    assert summary["number_of_asset_classes"] >= 5
    assert {"SPY", "VXUS", "BND", "IEF", "TLT", "GLD"} <= symbols
    assert {"US Equity", "International Equity", "Fixed Income", "Alternatives"} <= asset_classes


def test_demo_portfolio_allocation_cash_and_sector_sums() -> None:
    for portfolio_id in DEMO_PORTFOLIO_IDS:
        summary = client.get(f"/api/portfolios/{portfolio_id}/summary").json()
        sectors = client.get(
            f"/api/portfolios/{portfolio_id}/allocation/sectors",
        ).json()["items"]
        asset_types = client.get(
            f"/api/portfolios/{portfolio_id}/allocation/asset-types",
        ).json()["items"]

        assert summary["cash_weight"] >= 0
        assert sum(item["weight"] for item in sectors) == pytest.approx(1)
        assert sum(item["weight"] for item in asset_types) == pytest.approx(1)


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
