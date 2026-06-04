from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_equity_overview_returns_demo_company() -> None:
    response = client.get("/api/equity/AAPL/overview")

    assert response.status_code == 200
    body = response.json()
    assert body["symbol"] == "AAPL"
    assert body["company_name"] == "Apple Inc."
    assert body["market_cap"] > 0


def test_equity_valuation_returns_model_outputs() -> None:
    response = client.get("/api/equity/MSFT/valuation")

    assert response.status_code == 200
    body = response.json()
    assert body["symbol"] == "MSFT"
    assert body["pe_ratio"] > 0
    assert body["gordon_growth_value"] > 0
    assert "margin_of_safety" in body
    assert "Model-implied" in body["valuation_status"]
    assert any("GGM" in warning for warning in body["warnings"])


def test_equity_growth_flags_extreme_sustainable_growth() -> None:
    response = client.get("/api/equity/AAPL/growth")

    assert response.status_code == 200
    body = response.json()
    assert body["sustainable_growth_rate"] > 0.25
    assert any(
        "Sustainable growth rate is unusually high" in warning
        for warning in body["warnings"]
    )


def test_equity_ggm_endpoint_rejects_invalid_spread() -> None:
    response = client.post(
        "/api/equity/valuation/ggm",
        json={
            "dividend_next_year": 3.0,
            "required_return": 0.03,
            "growth_rate": 0.04,
        },
    )

    assert response.status_code == 422


def test_equity_extended_dashboard_endpoints_return_data() -> None:
    endpoints = [
        "/api/equity/AAPL/security-profile",
        "/api/equity/AAPL/industry",
        "/api/equity/AAPL/business-model",
        "/api/equity/AAPL/growth",
        "/api/equity/AAPL/relative-valuation",
        "/api/equity/AAPL/peer-comparison",
        "/api/equity/AAPL/corporate-actions",
        "/api/equity/AAPL/diagnostics",
    ]

    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200
        assert response.json()["symbol"] == "AAPL"
