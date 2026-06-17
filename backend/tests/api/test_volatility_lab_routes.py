from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_volatility_lab_status_is_ready() -> None:
    response = client.get("/api/volatility-lab/status")

    assert response.status_code == 200
    body = response.json()
    assert body["module"] == "volatility-lab"
    assert body["status"] == "ready"
    assert "beta_capm" in body["engines_available"]


def test_volatility_lab_analyze_asset_returns_cfa_metrics() -> None:
    response = client.post(
        "/api/volatility-lab/analyze-asset",
        json={"symbol": "AAPL", "benchmark_symbol": "SPY", "rolling_window": 5},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["symbol"] == "AAPL"
    assert body["return_summary"]["observations"] > 0
    assert body["volatility_summary"]["annualized_volatility"] > 0
    assert body["benchmark_risk"]["benchmark_symbol"] == "SPY"
    assert "p5" in body["distribution"]["percentiles"]
    assert body["downside_risk"]["historical_var"] >= 0
    assert body["data_source"]["metric_source"] == "realized_market_data"


def test_volatility_lab_analyze_asset_falls_back_when_market_data_missing() -> None:
    response = client.post(
        "/api/volatility-lab/analyze-asset",
        json={"symbol": "UNKNOWN", "benchmark_symbol": "SPY"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["symbol"] == "UNKNOWN"
    assert body["data_source"]["fallback_used"] is True
    assert "Requires Market Data" in body["data_source"]["badges"]


def test_volatility_lab_analyze_portfolio_returns_covariance_metrics() -> None:
    response = client.post(
        "/api/volatility-lab/analyze-portfolio",
        json={"portfolio_id": "pf_001", "benchmark_symbol": "SPY", "rolling_window": 5},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["portfolio_id"] == "pf_001"
    assert body["holdings_included"]
    assert body["return_summary"]["observations"] > 0
    assert body["portfolio_risk"]["covariance_based_volatility"] > 0
    assert body["rolling_volatility"]
    assert body["covariance_matrix"]["symbols"]
    assert body["correlation_matrix"]["matrix"]
    assert body["risk_contribution"]
    assert body["athena_commentary"]["cfa_notes"]


def test_volatility_lab_demo_endpoint_uses_demo_portfolio() -> None:
    response = client.get("/api/volatility-lab/demo")

    assert response.status_code == 200
    body = response.json()
    assert body["portfolio_id"] == "pf_001"
    assert body["portfolio_name"] == "Athena Demo Portfolio"
