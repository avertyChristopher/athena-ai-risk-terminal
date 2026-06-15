from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_risk_monitor_status_is_ready() -> None:
    response = client.get("/api/risk-monitor/status")

    assert response.status_code == 200
    body = response.json()
    assert body["module"] == "risk-monitor"
    assert body["status"] == "ready"
    assert "risk_metrics" in body["engines_available"]


def test_risk_monitor_analyze_returns_surveillance_dashboard() -> None:
    response = client.post(
        "/api/risk-monitor/analyze",
        json={"portfolio_id": "pf_001", "benchmark_symbol": "SPY"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["portfolio_id"] == "pf_001"
    assert body["global_risk_score"] > 0
    assert body["global_risk_status"] in {
        "Low Risk",
        "Moderate Risk",
        "Elevated Risk",
        "High Risk",
        "Critical Risk",
    }
    assert len(body["risk_metrics"]) >= 10
    assert len(body["limit_breaches"]) >= 1
    assert len(body["stress_tests"]) == 6
    assert body["risk_contribution"]["by_asset"]
    assert body["benchmark_risk"]["benchmark_symbol"] == "SPY"
    assert body["athena_commentary"]["summary"]
    assert body["risk_source"]["metric_source"] == "realized_market_data"


def test_risk_monitor_demo_endpoint_uses_demo_portfolio() -> None:
    response = client.get("/api/risk-monitor/demo")

    assert response.status_code == 200
    body = response.json()
    assert body["portfolio_id"] == "pf_001"
    assert body["portfolio_name"] == "Athena Demo Portfolio"
