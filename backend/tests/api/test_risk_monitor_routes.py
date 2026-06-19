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
    assert body["assumptions"]["limits"]["max_portfolio_volatility"] == 0.20


def test_risk_monitor_accepts_configurable_limits_and_stress_shocks() -> None:
    response = client.post(
        "/api/risk-monitor/analyze",
        json={
            "portfolio_id": "pf_001",
            "benchmark_symbol": "SPY",
            "limits": {"max_portfolio_volatility": 0.01},
            "stress_shocks": {"technology_sector_shock": -0.25},
        },
    )

    assert response.status_code == 200
    body = response.json()
    rule_names = {breach["rule_name"] for breach in body["limit_breaches"]}
    scenario_names = {scenario["name"] for scenario in body["stress_tests"]}
    assert body["assumptions"]["limits"]["max_portfolio_volatility"] == 0.01
    assert body["assumptions"]["stress_shocks"]["technology_sector_shock"] == -0.25
    assert "Max portfolio volatility" in rule_names
    assert "Technology sector shock -25%" in scenario_names


def test_risk_monitor_can_analyze_volatility_lab_payload() -> None:
    volatility_response = client.post(
        "/api/volatility-lab/analyze-portfolio",
        json={"portfolio_id": "pf_001", "benchmark_symbol": "SPY"},
    )
    payload = volatility_response.json()["risk_monitor_payload"]

    response = client.post(
        "/api/risk-monitor/analyze-from-volatility",
        json=payload,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["portfolio_id"] == "pf_001"
    assert body["risk_source"]["metric_source"] == payload["metric_source"]
    assert "Volatility Lab" in body["risk_source"]["badges"]
    assert body["benchmark_risk"]["warnings"][0] == "Using Volatility Lab risk payload."


def test_risk_monitor_demo_endpoint_uses_demo_portfolio() -> None:
    response = client.get("/api/risk-monitor/demo")

    assert response.status_code == 200
    body = response.json()
    assert body["portfolio_id"] == "pf_001"
    assert body["portfolio_name"] == "Athena Demo Portfolio"
