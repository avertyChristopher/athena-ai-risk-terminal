from fastapi.testclient import TestClient

from app.main import app
from app.modules.pnl_attribution.repository import PnlAttributionRepository
from app.modules.reconciliation.repository import ReconciliationRepository
from app.modules.trade_blotter.repository import TradeBlotterRepository


client = TestClient(app)


def setup_function() -> None:
    TradeBlotterRepository().clear()
    PnlAttributionRepository().clear()
    ReconciliationRepository().clear()


def test_trade_blotter_status_create_list_get_update_review_delete_workflow() -> None:
    status = client.get("/api/trade-blotter/status")
    assert status.status_code == 200
    assert status.json()["module"] == "trade-blotter"
    assert "No real market execution" in status.json()["detail"]

    created = client.post(
        "/api/trade-blotter/trades",
        json={
            "portfolio_id": "pf_001",
            "symbol": "AAPL",
            "action": "BUY",
            "quantity": 3,
            "price": 190,
            "status": "draft",
            "trade_date": "2026-05-20",
        },
    )
    assert created.status_code == 200
    trade_id = created.json()["trade_id"]
    assert created.json()["estimated_trade_value"] == 570

    listed = client.get("/api/trade-blotter/trades")
    detail = client.get(f"/api/trade-blotter/trades/{trade_id}")
    updated = client.put(f"/api/trade-blotter/trades/{trade_id}", json={"quantity": 4})
    submitted = client.post(
        f"/api/trade-blotter/trades/{trade_id}/review",
        json={"action": "submit_for_review", "reviewer": "ops"},
    )
    approved = client.post(
        f"/api/trade-blotter/trades/{trade_id}/review",
        json={"action": "approve", "reviewer": "cio", "note": "Approved for demo."},
    )
    invalid = client.post(
        f"/api/trade-blotter/trades/{trade_id}/review",
        json={"action": "approve", "reviewer": "cio"},
    )
    deleted = client.delete(f"/api/trade-blotter/trades/{trade_id}")
    missing = client.get(f"/api/trade-blotter/trades/{trade_id}")

    assert listed.status_code == 200
    assert listed.json()["total_entries"] == 1
    assert detail.status_code == 200
    assert updated.json()["estimated_trade_value"] == 760
    assert submitted.json()["entry"]["status"] == "pending_review"
    assert approved.json()["entry"]["status"] == "approved"
    assert len(approved.json()["entry"]["review_history"]) == 2
    assert invalid.status_code == 422
    assert deleted.json()["deleted"] is True
    assert missing.status_code == 404


def test_trade_blotter_from_simulation_and_trade_simulator_save_to_blotter() -> None:
    simulation_response = client.post(
        "/api/trade-simulator/simulate",
        json={
            "portfolio_id": "pf_001",
            "action": "BUY",
            "symbol": "MSFT",
            "asset_type": "equity",
            "quantity": 2,
            "estimated_price": 420,
            "order_type": "Market",
            "time_in_force": "Day",
            "trade_rationale": "Rebalancing",
            "save_to_blotter": True,
        },
    )

    assert simulation_response.status_code == 200
    simulation = simulation_response.json()
    assert simulation["save_status"] == "saved_to_trade_blotter"
    assert simulation["trade_id"]

    created = client.post(
        "/api/trade-blotter/from-simulation",
        json={"simulation": simulation, "initial_status": "simulated"},
    )
    assert created.status_code == 200
    assert created.json()["source_module"] == "trade_simulator"
    assert created.json()["status"] == "simulated"


def test_pnl_and_reconciliation_consume_persisted_trade_blotter_entries() -> None:
    trade = client.post(
        "/api/trade-blotter/trades",
        json={
            "portfolio_id": "pf_001",
            "symbol": "AAPL",
            "action": "BUY",
            "quantity": 2,
            "price": 190,
            "status": "approved",
            "trade_date": "2026-05-20",
            "cost_estimate": 4,
            "slippage_estimate": 2,
        },
    ).json()

    pnl = client.post(
        "/api/pnl-attribution/analyze",
        json={
            "portfolio_id": "pf_001",
            "start_date": "2026-05-13",
            "end_date": "2026-06-03",
            "include_trades": True,
        },
    )
    reconciliation = client.post(
        "/api/reconciliation/run",
        json={"portfolio_id": "pf_001", "checks": ["trades"]},
    )

    assert pnl.status_code == 200
    assert any(
        row.get("trade_id") == trade["trade_id"]
        for row in pnl.json()["trade_effects"]["trades"]
    )
    assert pnl.json()["trade_effects"]["total_trade_costs"] >= 4
    assert reconciliation.status_code == 200
    assert any(
        row["trade_id"] == trade["trade_id"]
        for row in reconciliation.json()["trade_breaks"]
    )
