from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_trade_simulator_status_is_ready() -> None:
    response = client.get("/api/trade-simulator/status")

    assert response.status_code == 200
    body = response.json()
    assert body["module"] == "trade-simulator"
    assert body["simulation_ready"] is True


def test_legacy_trade_status_still_works() -> None:
    response = client.get("/api/trades/status")

    assert response.status_code == 200
    assert response.json()["module"] == "trade-simulator"


def test_trade_simulator_returns_full_pre_trade_analysis() -> None:
    response = client.post(
        "/api/trade-simulator/simulate",
        json={
            "portfolio_id": "pf_001",
            "action": "BUY",
            "symbol": "NVDA",
            "asset_name": "NVIDIA Corporation",
            "asset_type": "equity",
            "quantity": 5,
            "estimated_price": 125,
            "order_type": "Market",
            "time_in_force": "Day",
            "trade_rationale": "Growth opportunity",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["module"] == "trade-simulator"
    assert body["trade_ticket"]["symbol"] == "NVDA"
    assert body["trade_ticket"]["gross_trade_value"] == 625
    assert body["risk_impact"]["badges"]
    assert body["risk_impact"]["metric_source"] == "realized_market_data"
    assert body["risk_impact"]["fallback_used"] is False
    assert "Realized" in body["risk_impact"]["badges"]
    assert body["risk_impact"]["observations"] >= 2
    assert "Simulation only" in body["simulation_result"]["notice"]
    assert body["transaction_cost_analysis"]["total_estimated_cost"] > 0
    assert any(
        status["module"] == "Portfolio Builder" and status["payload_available"] is True
        for status in body["module_source_metadata"]
    )
    assert body["trade_impact_payload"]["module_name"] == "trade_simulator"
    assert body["trade_impact_payload"]["portfolio_id"] == "pf_001"
    assert body["trade_impact_payload"]["before_weights"]
    assert body["trade_impact_payload"]["after_risk"]["portfolio_volatility"] is not None


def test_trade_simulator_falls_back_when_market_returns_are_missing() -> None:
    response = client.post(
        "/api/trade-simulator/simulate",
        json={
            "portfolio_id": "pf_001",
            "action": "BUY",
            "symbol": "XYZ",
            "asset_name": "Missing Return Series Corp.",
            "asset_type": "equity",
            "quantity": 3,
            "estimated_price": 50,
            "order_type": "Market",
            "time_in_force": "Day",
            "trade_rationale": "Growth opportunity",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["risk_impact"]["metric_source"] == "deterministic_demo"
    assert body["risk_impact"]["fallback_used"] is True
    assert "XYZ" in body["risk_impact"]["symbols_missing"]
    assert "Requires Market Data" in body["risk_impact"]["badges"]
    assert any(
        status["module"] == "Market Data" and status["required_data"]
        for status in body["module_source_metadata"]
    )
    assert (
        "Realized Market Data return series unavailable. Falling back to deterministic demo assumptions."
        in body["risk_impact"]["message"]
    )


def test_trade_simulator_rejects_sell_above_available_quantity() -> None:
    response = client.post(
        "/api/trade-simulator/simulate",
        json={
            "portfolio_id": "pf_001",
            "action": "SELL",
            "symbol": "AAPL",
            "asset_type": "equity",
            "quantity": 10_000,
            "estimated_price": 180,
            "order_type": "Limit",
            "limit_price": 181,
            "time_in_force": "GTC",
            "trade_rationale": "Risk reduction",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["simulation_result"]["trade_status"] == "Rejected"
    assert any(
        warning["name"] == "Sell quantity"
        for warning in body["constraints_warnings"]
    )
