from datetime import UTC, date, datetime

from app.persistence.init_db import init_db
from app.persistence.repositories import (
    AthenaCommentaryPersistenceRepository,
    PortfolioSnapshotPersistenceRepository,
    TradeBlotterPersistenceRepository,
)


def setup_function() -> None:
    TradeBlotterPersistenceRepository().clear()
    AthenaCommentaryPersistenceRepository().clear()
    PortfolioSnapshotPersistenceRepository().clear()


def test_database_initializes_and_trade_blotter_repository_crud() -> None:
    assert init_db() is True

    repository = TradeBlotterPersistenceRepository()
    payload = {
        "trade_id": "test_trade_001",
        "portfolio_id": "pf_001",
        "symbol": "AAPL",
        "action": "BUY",
        "quantity": 2,
        "price": 190,
        "estimated_trade_value": 380,
        "currency": "USD",
        "status": "approved",
        "trade_date": date(2026, 6, 3).isoformat(),
        "settlement_date": None,
        "source_module": "unit_test",
        "cost_estimate": 1.0,
        "slippage_estimate": 0.5,
        "suitability_status": "Suitable",
        "constraint_status": "clear",
        "risk_summary": {"var_delta": 0.01},
        "review_history": [],
        "created_at": datetime.now(UTC).isoformat(),
        "updated_at": datetime.now(UTC).isoformat(),
    }

    assert repository.save(payload) is True
    assert repository.get("test_trade_001")["symbol"] == "AAPL"
    assert repository.list()[0]["trade_id"] == "test_trade_001"
    assert repository.delete("test_trade_001") is True
    assert repository.get("test_trade_001") is None


def test_portfolio_snapshot_and_athena_commentary_can_be_persisted_without_secrets() -> None:
    snapshot_repo = PortfolioSnapshotPersistenceRepository()
    commentary_repo = AthenaCommentaryPersistenceRepository()

    assert snapshot_repo.save_snapshot(
        portfolio_id="pf_001",
        portfolio_name="Athena Balanced Growth Portfolio",
        snapshot_type="unit_test",
        source_module="unit_test",
        payload={"value": 123},
    )
    assert commentary_repo.save(
        commentary_id="athena_unit_001",
        module_name="trade_blotter",
        portfolio_id="pf_001",
        symbol="AAPL",
        language="en",
        generated_by="deterministic_fallback",
        payload={"portfolio_id": "pf_001", "api_key": None},
        summary="Trade workflow commentary.",
    )

    rows = commentary_repo.list()
    assert rows[0]["commentary_id"] == "athena_unit_001"
    assert "secret" not in str(rows[0]["payload"]).lower()
