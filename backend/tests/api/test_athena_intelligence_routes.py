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
