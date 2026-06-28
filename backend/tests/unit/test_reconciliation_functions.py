from app.modules.reconciliation.domain.break_classification import (
    apply_review_action,
    create_break,
    overall_status_from_breaks,
)
from app.modules.reconciliation.domain.cash_reconciliation import reconcile_cash
from app.modules.reconciliation.domain.fx_reconciliation import reconcile_fx
from app.modules.reconciliation.domain.pnl_reconciliation import reconcile_pnl
from app.modules.reconciliation.domain.position_reconciliation import reconcile_positions
from app.modules.reconciliation.domain.price_reconciliation import reconcile_prices
from app.modules.reconciliation.domain.severity import (
    classify_amount_severity,
    classify_position_severity,
    classify_price_severity,
)
from app.modules.reconciliation.domain.trade_reconciliation import reconcile_trades
from app.modules.reconciliation.schemas import ReconciliationTolerance, ReviewRequest


def test_position_reconciliation_detects_matches_mismatches_and_missing_positions() -> None:
    tolerance = ReconciliationTolerance(market_value_tolerance=50)
    matched_rows, matched_breaks = reconcile_positions(
        run_id="run_1",
        portfolio_id="pf_test",
        internal_positions=[{"symbol": "AAPL", "quantity": 10, "market_value": 1000}],
        external_positions=[{"symbol": "AAPL", "quantity": 10, "market_value": 1000}],
        tolerance=tolerance,
    )
    break_rows, breaks = reconcile_positions(
        run_id="run_2",
        portfolio_id="pf_test",
        internal_positions=[
            {"symbol": "AAPL", "quantity": 10, "market_value": 1000},
            {"symbol": "MSFT", "quantity": 5, "market_value": 2500},
        ],
        external_positions=[
            {"symbol": "AAPL", "quantity": 8, "market_value": 800},
            {"symbol": "NVDA", "quantity": 2, "market_value": 1900},
        ],
        tolerance=tolerance,
    )

    assert matched_rows[0].status == "matched"
    assert matched_breaks == []
    assert {row.status for row in break_rows} == {"break", "missing_external", "missing_internal"}
    assert len(breaks) == 3
    assert {item.break_type for item in breaks} == {"position"}


def test_cash_reconciliation_handles_match_mismatch_and_missing_data() -> None:
    tolerance = ReconciliationTolerance(cash_tolerance=100)
    matched_rows, matched_breaks, matched_warnings = reconcile_cash(
        run_id="run_1",
        portfolio_id="pf_test",
        currency="USD",
        internal_cash=1000,
        external_cash=950,
        tolerance=tolerance,
    )
    break_rows, breaks, warnings = reconcile_cash(
        run_id="run_2",
        portfolio_id="pf_test",
        currency="USD",
        internal_cash=1000,
        external_cash=700,
        tolerance=tolerance,
    )
    missing_rows, missing_breaks, missing_warnings = reconcile_cash(
        run_id="run_3",
        portfolio_id="pf_test",
        currency="USD",
        internal_cash=1000,
        external_cash=None,
        tolerance=tolerance,
    )

    assert matched_rows[0].status == "within_tolerance"
    assert matched_breaks == []
    assert matched_warnings == []
    assert break_rows[0].status == "break"
    assert breaks[0].break_type == "cash"
    assert warnings == []
    assert missing_rows[0].status == "missing_cash_data"
    assert missing_breaks == []
    assert missing_warnings


def test_price_reconciliation_detects_price_break_stale_price_and_missing_price_warning() -> None:
    tolerance = ReconciliationTolerance(price_tolerance_bps=10)
    rows, breaks, warnings = reconcile_prices(
        run_id="run_1",
        portfolio_id="pf_test",
        internal_prices={
            "AAPL": {"price": 100, "timestamp": "2026-06-03"},
            "BND": {"price": 90, "timestamp": "2026-06-03"},
        },
        external_positions=[
            {"symbol": "AAPL", "price": 99, "price_timestamp": "2026-06-03"},
            {"symbol": "BND", "price": 90, "price_timestamp": "2026-05-29", "stale_price": True},
            {"symbol": "ZZZZ", "price": 10, "price_timestamp": "2026-06-03"},
        ],
        tolerance=tolerance,
    )

    assert {row.status for row in rows} == {"break", "stale_price", "missing_price"}
    assert len(breaks) == 2
    assert any(item.symbol == "BND" for item in breaks)
    assert any("ZZZZ" in warning for warning in warnings)


def test_trade_reconciliation_warns_without_blotter_and_detects_missing_trades() -> None:
    empty_rows, empty_breaks, empty_warnings = reconcile_trades(
        run_id="run_1",
        portfolio_id="pf_test",
        internal_trades=[],
        external_trades=[],
    )
    rows, breaks, warnings = reconcile_trades(
        run_id="run_2",
        portfolio_id="pf_test",
        internal_trades=[{"trade_id": "int_1", "symbol": "AAPL", "action": "BUY", "quantity": 1, "price": 100}],
        external_trades=[{"trade_id": "ext_1", "symbol": "MSFT", "action": "SELL", "quantity": 2, "price": 200}],
    )

    assert empty_rows == []
    assert empty_breaks == []
    assert empty_warnings
    assert len(rows) == 2
    assert {row.status for row in rows} == {"missing_external_trade", "missing_internal_trade"}
    assert len(breaks) == 2
    assert warnings == []


def test_pnl_reconciliation_detects_matching_and_unexplained_pnl() -> None:
    tolerance = ReconciliationTolerance(pnl_tolerance=250)
    matched_rows, matched_breaks, matched_warnings = reconcile_pnl(
        run_id="run_1",
        portfolio_id="pf_test",
        internal_total_pnl=1000,
        external_total_pnl=900,
        starting_value=100000,
        tolerance=tolerance,
    )
    break_rows, breaks, warnings = reconcile_pnl(
        run_id="run_2",
        portfolio_id="pf_test",
        internal_total_pnl=2500,
        external_total_pnl=1000,
        starting_value=100000,
        tolerance=tolerance,
    )

    assert matched_rows[0].status == "within_tolerance"
    assert matched_breaks == []
    assert matched_warnings == []
    assert break_rows[0].status == "break"
    assert breaks[0].break_type == "pnl"
    assert breaks[0].severity == "high"
    assert warnings == []


def test_fx_reconciliation_detects_mismatch_and_missing_fx_data_without_crashing() -> None:
    rows, breaks, warnings = reconcile_fx(
        run_id="run_1",
        portfolio_id="pf_test",
        base_currency="USD",
        internal_rates={"EUR": 1.09, "CAD": 0.73},
        external_rates={"EUR": 1.08},
        external_positions=[
            {"symbol": "EUR_ETF", "currency": "EUR", "market_value": 10000},
            {"symbol": "CAD_ETF", "currency": "CAD", "market_value": 5000},
        ],
    )
    no_fx_rows, no_fx_breaks, no_fx_warnings = reconcile_fx(
        run_id="run_2",
        portfolio_id="pf_test",
        base_currency="USD",
        internal_rates={},
        external_rates={},
        external_positions=[{"symbol": "AAPL", "currency": "USD", "market_value": 1000}],
    )

    assert {row.currency for row in rows} == {"EUR", "CAD"}
    assert len(breaks) == 1
    assert breaks[0].break_type == "fx"
    assert any("CAD" in warning for warning in warnings)
    assert no_fx_rows == []
    assert no_fx_breaks == []
    assert no_fx_warnings


def test_severity_and_overall_status_classification() -> None:
    low_break = create_break(
        run_id="run_1",
        portfolio_id="pf_test",
        break_type="price",
        severity="low",
        metric="price",
        source_module="Market Data",
        explanation="Small price break.",
        suggested_action="Review price.",
    )
    high_break = create_break(
        run_id="run_1",
        portfolio_id="pf_test",
        break_type="position",
        severity="high",
        metric="position",
        source_module="Portfolio Builder",
        explanation="Position break.",
        suggested_action="Review position.",
    )
    critical_break = high_break.model_copy(update={"severity": "critical"})

    assert classify_amount_severity(20, 100) == "low"
    assert classify_amount_severity(300, 100) == "medium"
    assert classify_amount_severity(700, 100) == "high"
    assert classify_amount_severity(1600, 100) == "critical"
    assert classify_position_severity(1, 600, 100) == "high"
    assert classify_price_severity(0, 10, stale=True) == "low"
    assert overall_status_from_breaks([]) == "reconciled"
    assert overall_status_from_breaks([low_break]) == "minor_breaks"
    assert overall_status_from_breaks([high_break]) == "material_breaks"
    assert overall_status_from_breaks([critical_break]) == "critical_breaks"


def test_review_action_transitions_and_reopen() -> None:
    item = create_break(
        run_id="run_1",
        portfolio_id="pf_test",
        break_type="cash",
        severity="medium",
        metric="cash",
        source_module="Portfolio Builder",
        explanation="Cash break.",
        suggested_action="Review cash.",
    )
    item = apply_review_action(item, ReviewRequest(action="mark_under_review", reviewer="ops"))
    item = apply_review_action(item, ReviewRequest(action="explain", reviewer="ops", note="Fee timing."))
    item = apply_review_action(item, ReviewRequest(action="resolve", reviewer="ops", decision="Confirmed."))
    item = apply_review_action(item, ReviewRequest(action="reopen", reviewer="ops", note="Reopened."))
    ignored = apply_review_action(item, ReviewRequest(action="ignore", reviewer="ops", note="Immaterial."))

    assert item.status == "open"
    assert len(item.review_history) == 4
    assert ignored.status == "ignored"
    assert ignored.reviewed_by == "ops"
