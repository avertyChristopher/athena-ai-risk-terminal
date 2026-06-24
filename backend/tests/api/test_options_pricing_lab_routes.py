import pytest
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
    assert "implied_volatility" in body["engines_available"]


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
    assert body["risk_payload"]["module_name"] == "options_pricing_lab"
    assert body["risk_payload"]["underlying_symbol"] == "AAPL"
    assert body["risk_payload"]["delta_adjusted_exposure"] == body["greeks"]["delta_adjusted_exposure"]
    assert body["risk_payload"]["max_loss"] == body["payoff_summary"]["max_loss"]
    assert body["parity_check"]["status"] == "aligned"
    assert body["data_sources"]["underlying_price_source"] == "manual_input"
    assert body["data_sources"]["volatility_source"] == "manual_input"
    assert body["athena_commentary"]["key_points"]
    assert body["athena_ai_commentary"]["generated_by"] == "deterministic_fallback"
    assert "not investment advice" in body["athena_ai_commentary"]["disclaimer"]


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
    assert body["risk_payload"]["strategy_name"] == "long_straddle"
    assert body["risk_payload"]["gamma"] == body["aggregate_greeks"]["aggregate_gamma"]
    assert body["risk_payload"]["breakeven_points"] == body["breakeven_points"]
    assert "cfa_explanation" in body["risk_summary"]
    assert body["commentary"]["key_points"]
    assert body["athena_ai_commentary"]["source_modules"] == ["options_pricing_lab"]


def test_covered_call_endpoint_includes_stock_risk_and_scaled_greeks() -> None:
    response = client.post(
        "/api/options-pricing-lab/strategy",
        json={
            "underlying_symbol": "AAPL",
            "underlying_price": 100,
            "volatility": 0.2,
            "strategy_type": "covered_call",
            "contract_size": 100,
            "quantity": 2,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["stock_leg_included"] is True
    assert [leg["leg_type"] for leg in body["legs"]] == ["stock", "option"]
    assert body["max_profit"]["type"] == "finite"
    assert body["aggregate_greeks"]["aggregate_delta"] > 0
    assert body["aggregate_greeks"]["legs"][0]["position_greeks"]["delta"] == 200


def test_observed_parity_mode_uses_submitted_market_prices() -> None:
    response = client.post(
        "/api/options-pricing-lab/price",
        json={
            "underlying_price": 100,
            "strike_price": 100,
            "time_to_expiration_days": 365,
            "volatility": 0.2,
            "risk_free_rate": 0.05,
            "dividend_yield": 0,
            "parity_mode": "observed",
            "observed_call_price": 12,
            "observed_put_price": 1,
        },
    )

    assert response.status_code == 200
    parity = response.json()["parity_check"]
    assert parity["mode"] == "observed"
    assert parity["call_price"] == 12
    assert parity["put_price"] == 1
    assert parity["status"] == "potential_arbitrage"


def test_implied_volatility_endpoint_recovers_known_volatility() -> None:
    response = client.post(
        "/api/options-pricing-lab/implied-volatility",
        json={
            "underlying_symbol": "AAPL",
            "option_type": "call",
            "observed_option_price": 10.4505835722,
            "underlying_price": 100,
            "strike_price": 100,
            "time_to_expiration_days": 365,
            "risk_free_rate": 0.05,
            "dividend_yield": 0,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["converged"] is True
    assert body["implied_volatility"] == pytest.approx(0.2, rel=1e-5)
    assert body["validation_status"] == "valid"


def test_implied_volatility_endpoint_returns_structured_invalid_bounds() -> None:
    response = client.post(
        "/api/options-pricing-lab/implied-volatility",
        json={
            "option_type": "call",
            "observed_option_price": 101,
            "underlying_price": 100,
            "strike_price": 100,
            "time_to_expiration_days": 365,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["converged"] is False
    assert body["implied_volatility"] is None
    assert body["validation_status"] == "outside_no_arbitrage_bounds"


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
