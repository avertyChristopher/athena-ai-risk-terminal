from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_athena_intelligence_status_endpoint_uses_fallback_mode() -> None:
    response = client.get("/api/athena-intelligence/status")

    assert response.status_code == 200
    body = response.json()
    assert body["module"] == "athena-intelligence"
    assert body["status"] == "ready"
    assert body["provider_mode"] == "fallback"
    assert body["fallback_enabled"] is True


def test_athena_intelligence_commentary_endpoint_returns_fallback() -> None:
    response = client.post(
        "/api/athena-intelligence/commentary",
        json={
            "module_name": "risk_monitor",
            "analysis_mode": "risk",
            "language": "en",
            "payload": {
                "global_risk_score": 72,
                "global_risk_status": "High Risk",
                "risk_metrics": [
                    {"name": "VaR 95%", "value": 0.035},
                    {"name": "CVaR 95%", "value": 0.052},
                    {"name": "Portfolio volatility", "value": 0.28},
                ],
                "concentration": {"top_3_weight": 0.72},
                "limit_breaches": [
                    {
                        "rule_name": "Top 3 concentration",
                        "explanation": "Top 3 holdings exceed the surveillance limit.",
                    },
                ],
            },
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["generated_by"] == "deterministic_fallback"
    assert "not investment advice" in body["disclaimer"]
    assert body["main_risks"]
    assert body["breaches"]


def test_athena_intelligence_risk_synthesis_endpoint() -> None:
    response = client.post(
        "/api/athena-intelligence/risk-synthesis",
        json={
            "portfolio_id": "pf_001",
            "language": "en",
            "payloads": {
                "risk_analytics_payload": {
                    "global_risk_score": 62,
                    "annualized_volatility": 0.21,
                    "historical_cvar": 0.041,
                },
                "rates_risk_payload": {
                    "modified_duration": 7.5,
                    "dv01": 42.0,
                },
                "options_risk_payload": {
                    "delta_adjusted_exposure": 12500,
                },
            },
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["generated_by"] == "deterministic_fallback"
    assert body["top_risk_drivers"]
    assert "not investment advice" in body["disclaimer"]


def test_athena_intelligence_commentary_differs_by_demo_portfolio_profile() -> None:
    balanced = client.post(
        "/api/risk-monitor/analyze",
        json={"portfolio_id": "pf_001", "benchmark_symbol": "SPY"},
    ).json()
    tech = client.post(
        "/api/risk-monitor/analyze",
        json={"portfolio_id": "pf_003", "benchmark_symbol": "SPY"},
    ).json()
    conservative_rates = client.post(
        "/api/rates-lab/portfolio-exposure",
        json={"portfolio_id": "pf_002", "shock_bps": 100},
    ).json()

    balanced_commentary = balanced["athena_ai_commentary"]
    tech_commentary = tech["athena_ai_commentary"]
    rates_commentary = conservative_rates["athena_ai_commentary"]

    assert balanced["portfolio_name"] == "Athena Balanced Growth Portfolio"
    assert tech["portfolio_name"] == "Athena Tech Concentration Portfolio"
    assert conservative_rates["portfolio_name"] == "Athena Conservative Income Portfolio"
    assert balanced_commentary["summary"] != tech_commentary["summary"]
    assert "Moderate Risk" in balanced_commentary["summary"]
    assert "Critical Risk" in tech_commentary["summary"]
    assert any("concentration" in item.lower() for item in tech_commentary["main_risks"])
    assert any("nvda" in item.lower() for item in tech_commentary["breaches"])
    assert any("duration" in item.lower() for item in rates_commentary["main_risks"])
    assert any("dv01" in item.lower() for item in rates_commentary["risk_drivers"])
    assert "not investment advice" in tech_commentary["disclaimer"]


def test_athena_intelligence_explain_metric_endpoint() -> None:
    response = client.post(
        "/api/athena-intelligence/explain-metric",
        json={
            "metric_name": "DV01",
            "metric_value": 42.0,
            "module_name": "rates_lab",
            "context": {"modified_duration": 7.5},
            "language": "en",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["generated_by"] == "deterministic_fallback"
    assert "DV01" in body["explanation"]
    assert body["cfa_note"]


def test_athena_intelligence_demo_endpoint() -> None:
    response = client.get("/api/athena-intelligence/demo")

    assert response.status_code == 200
    body = response.json()
    assert body["summary"]
    assert body["generated_by"] == "deterministic_fallback"
