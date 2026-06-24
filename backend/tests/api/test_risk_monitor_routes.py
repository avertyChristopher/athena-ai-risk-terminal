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
    assert any(
        status["module"] == "Market Data" and status["status"] == "Connected"
        for status in body["integration_statuses"]
    )


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
    assert any(
        status["module"] == "Volatility Lab" and status["payload_available"] is True
        for status in body["integration_statuses"]
    )


def test_risk_monitor_can_analyze_rates_lab_payload() -> None:
    rates_response = client.post(
        "/api/rates-lab/portfolio-exposure",
        json={"portfolio_id": "pf_001", "shock_bps": 100},
    )
    payload = rates_response.json()["rates_risk_payload"]

    response = client.post(
        "/api/risk-monitor/analyze-from-rates",
        json=payload,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["portfolio_id"] == "pf_001"
    assert body["rates_risk_payload"]["module_name"] == "rates_lab"
    assert any(metric["name"] == "DV01" for metric in body["risk_metrics"])
    assert any(
        status["module"] == "Rates Lab" and status["payload_available"] is True
        for status in body["integration_statuses"]
    )


def test_risk_monitor_can_analyze_options_pricing_payload() -> None:
    option_response = client.post(
        "/api/options-pricing-lab/price",
        json={
            "underlying_symbol": "AAPL",
            "underlying_price": 100,
            "strike_price": 100,
            "volatility": 0.2,
        },
    )
    payload = option_response.json()["risk_payload"]

    response = client.post(
        "/api/risk-monitor/analyze-from-options",
        json=payload,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["options_risk_payload"]["module_name"] == "options_pricing_lab"
    assert any(metric["name"] == "Delta-adjusted exposure" for metric in body["risk_metrics"])
    assert any(
        status["module"] == "Options Pricing Lab" and status["payload_available"] is True
        for status in body["integration_statuses"]
    )


def test_risk_monitor_demo_endpoint_uses_demo_portfolio() -> None:
    response = client.get("/api/risk-monitor/demo")

    assert response.status_code == 200
    body = response.json()
    assert body["portfolio_id"] == "pf_001"
    assert body["portfolio_name"] == "Athena Demo Portfolio"
