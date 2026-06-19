from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_options_pricing_lab_status_is_ready() -> None:
    response = client.get("/api/options-pricing-lab/status")

    assert response.status_code == 200
    body = response.json()
    assert body["module"] == "options-pricing-lab"
    assert body["status"] == "ready"
    assert "black_scholes" in body["engines_available"]
    assert "greeks" in body["engines_available"]


def test_options_pricing_lab_prices_single_option() -> None:
    response = client.post(
        "/api/options-pricing-lab/price",
        json={
            "underlying_symbol": "AAPL",
            "option_type": "call",
            "position_side": "long",
            "underlying_price": 100,
            "strike_price": 100,
            "time_to_expiration_days": 365,
            "risk_free_rate": 0.05,
            "dividend_yield": 0,
            "volatility": 0.2,
            "pricing_model": "black_scholes",
            "binomial_steps": 100,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["input_summary"]["underlying_symbol"] == "AAPL"
    assert body["pricing_summary"]["option_price"] > 0
    assert body["pricing_summary"]["black_scholes_price"] > 0
    assert body["pricing_summary"]["binomial_price"] > 0
    assert body["pricing_summary"]["moneyness"] == "at_the_money"
    assert body["payoff_summary"]["payoff_table"]
    assert body["greeks"]["delta"] > 0
    assert body["parity_check"]["status"] == "aligned"
    assert body["data_sources"]["underlying_price_source"] == "manual_input"
    assert body["data_sources"]["volatility_source"] == "manual_input"
    assert body["athena_commentary"]["key_points"]


def test_options_pricing_lab_strategy_endpoint_returns_analytics() -> None:
    response = client.post(
        "/api/options-pricing-lab/strategy",
        json={
            "underlying_symbol": "AAPL",
            "underlying_price": 100,
            "risk_free_rate": 0.05,
            "dividend_yield": 0,
            "volatility": 0.2,
            "strategy_type": "long_straddle",
            "contract_size": 100,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["strategy_summary"]["strategy_type"] == "long_straddle"
    assert len(body["legs"]) == 2
    assert body["net_premium"] > 0
    assert body["payoff_table"]
    assert body["aggregate_greeks"]["gamma"] > 0
    assert "cfa_explanation" in body["risk_summary"]
    assert body["commentary"]["key_points"]


def test_options_pricing_lab_demo_endpoint_uses_default_contract() -> None:
    response = client.get("/api/options-pricing-lab/demo")

    assert response.status_code == 200
    body = response.json()
    assert body["input_summary"]["underlying_symbol"] == "AAPL"
    assert body["pricing_summary"]["option_price"] > 0


def test_options_pricing_lab_rejects_invalid_contract_inputs() -> None:
    response = client.post(
        "/api/options-pricing-lab/price",
        json={"underlying_symbol": "AAPL", "strike_price": -1},
    )

    assert response.status_code == 422
