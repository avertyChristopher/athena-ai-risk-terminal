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
    assert "Simulation only" in body["simulation_result"]["notice"]
    assert body["transaction_cost_analysis"]["total_estimated_cost"] > 0


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
