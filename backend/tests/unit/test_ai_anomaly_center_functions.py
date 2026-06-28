from __future__ import annotations

from datetime import UTC, datetime, timedelta

from app.modules.ai_anomaly_center.domain.anomaly_rules import apply_review_action
from app.modules.ai_anomaly_center.domain.anomaly_scoring import build_anomaly, score_anomaly
from app.modules.ai_anomaly_center.domain.limit_anomalies import detect_limit_anomalies
from app.modules.ai_anomaly_center.domain.market_data_anomalies import detect_market_data_anomalies
from app.modules.ai_anomaly_center.domain.pnl_anomalies import detect_pnl_anomalies
from app.modules.ai_anomaly_center.domain.portfolio_anomalies import detect_portfolio_anomalies
from app.modules.ai_anomaly_center.domain.rates_options_anomalies import detect_rates_options_anomalies
from app.modules.ai_anomaly_center.domain.reconciliation_anomalies import detect_reconciliation_anomalies
from app.modules.ai_anomaly_center.domain.risk_anomalies import detect_risk_anomalies
from app.modules.ai_anomaly_center.domain.stress_anomalies import detect_stress_anomalies
from app.modules.ai_anomaly_center.domain.trade_anomalies import detect_trade_anomalies
from app.modules.ai_anomaly_center.schemas import AnomalyReviewRequest


def test_market_data_rules_detect_missing_stale_price_return_benchmark_and_fx() -> None:
    records = detect_market_data_anomalies(
        {
            "portfolio": {"benchmark": "SPY", "base_currency": "USD"},
            "positions": [{"symbol": "SHOP", "currency": "CAD"}],
            "prices": {
                "AAPL": [
                    {"date": "2026-05-30", "close": 100},
                    {"date": "2026-06-01", "close": 150},
                ],
                "BAD": [{"date": "2026-06-28", "close": 0}],
                "EMPTY": [],
            },
        },
        "pf_test",
    )

    anomaly_types = {record.anomaly_type for record in records}

    assert "benchmark_missing" in anomaly_types
    assert "fx_data_unavailable" in anomaly_types
    assert "stale_price" in anomaly_types
    assert "abnormal_return" in anomaly_types
    assert "invalid_price" in anomaly_types
    assert "missing_latest_price" in anomaly_types


def test_portfolio_rules_detect_concentration_cash_and_allocation_drift() -> None:
    records = detect_portfolio_anomalies(
        {
            "portfolio": {
                "cash": -100,
                "target_allocation": {"equity": 0.40, "fixed_income": 0.50, "cash": 0.10},
            },
            "positions": [
                {
                    "id": "pos_aapl",
                    "symbol": "AAPL",
                    "quantity": 100,
                    "current_price": 90,
                    "sector": "Technology",
                    "asset_type": "equity",
                },
                {
                    "id": "pos_msft",
                    "symbol": "MSFT",
                    "quantity": 10,
                    "current_price": 20,
                    "sector": "Technology",
                    "asset_type": "equity",
                },
            ],
        },
        "pf_test",
    )

    anomaly_types = {record.anomaly_type for record in records}

    assert "negative_cash" in anomaly_types
    assert "low_cash" in anomaly_types
    assert "single_name_concentration" in anomaly_types
    assert "sector_concentration" in anomaly_types
    assert "allocation_drift" in anomaly_types


def test_trade_rules_detect_large_trade_cost_warning_rejections_turnover_and_missing_note() -> None:
    records = detect_trade_anomalies(
        {
            "portfolio": {"total_value": 10_000},
            "trade_blotter": [
                {
                    "trade_id": "trd_large",
                    "symbol": "NVDA",
                    "status": "approved",
                    "estimated_trade_value": 3_000,
                    "cost_estimate": 70,
                    "slippage_estimate": 20,
                    "constraint_status": "warning",
                    "suitability_status": "suitable",
                },
                {"trade_id": "trd_rej_1", "symbol": "AAPL", "status": "rejected", "estimated_trade_value": 1_000},
                {"trade_id": "trd_rej_2", "symbol": "MSFT", "status": "rejected", "estimated_trade_value": 1_000},
                {"trade_id": "trd_rej_3", "symbol": "AMZN", "status": "rejected", "estimated_trade_value": 1_000},
            ],
        },
        "pf_test",
    )

    anomaly_types = {record.anomaly_type for record in records}

    assert "large_trade_notional" in anomaly_types
    assert "high_transaction_cost" in anomaly_types
    assert "approved_trade_with_warnings" in anomaly_types
    assert "missing_review_note_on_high_risk_trade" in anomaly_types
    assert "repeated_rejections" in anomaly_types
    assert "high_trade_turnover" in anomaly_types


def test_pnl_rules_detect_loss_single_contributor_unexplained_and_benchmark_gap() -> None:
    records = detect_pnl_anomalies(
        {
            "pnl_history": [
                {
                    "analysis_id": "pnl_1",
                    "portfolio_id": "pf_test",
                    "total_pnl_percent": -0.10,
                    "total_pnl": -1_000,
                    "unexplained_pnl": 100,
                    "position_contributions": [{"symbol": "NVDA", "total_pnl": -700}],
                    "benchmark_comparison": {"active_return": -0.07},
                }
            ]
        },
        "pf_test",
    )

    anomaly_types = {record.anomaly_type for record in records}

    assert "large_period_loss" in anomaly_types
    assert "single_contributor_dominance" in anomaly_types
    assert "unexplained_pnl" in anomaly_types
    assert "benchmark_underperformance" in anomaly_types


def test_risk_rules_detect_score_var_jump_volatility_and_coverage() -> None:
    records = detect_risk_anomalies(
        {
            "risk_monitor": {
                "global_risk_score": 82,
                "risk_metrics": [
                    {"name": "VaR 95%", "value": 0.06, "prior_value": 0.03},
                    {"name": "Volatility", "value": 0.42},
                ],
                "risk_source": {"coverage_ratio": 0.70},
            }
        },
        "pf_test",
    )

    anomaly_types = {record.anomaly_type for record in records}

    assert "high_risk_score" in anomaly_types
    assert "var_elevated" in anomaly_types
    assert "var_jump" in anomaly_types
    assert "volatility_spike" in anomaly_types
    assert "low_coverage_ratio" in anomaly_types


def test_reconciliation_limit_stress_and_rates_options_rules() -> None:
    old_date = (datetime.now(UTC) - timedelta(days=8)).isoformat()

    reconciliation_types = {
        record.anomaly_type
        for record in detect_reconciliation_anomalies(
            {
                "reconciliation_breaks": [
                    {
                        "break_id": "brk_1",
                        "symbol": "NVDA",
                        "severity": "critical",
                        "status": "open",
                        "created_at": old_date,
                        "metric": "price",
                        "difference": 10,
                    },
                    {"break_id": "brk_2", "symbol": "NVDA", "severity": "high", "status": "open"},
                    {"break_id": "brk_3", "symbol": "NVDA", "severity": "medium", "status": "open"},
                ]
            },
            "pf_test",
        )
    }
    limit_types = {
        record.anomaly_type
        for record in detect_limit_anomalies(
            {
                "limit_breaches": [
                    {
                        "breach_id": "lim_1",
                        "rule_id": "max_var",
                        "severity": "critical",
                        "status": "open",
                        "metric_key": "var",
                        "current_value": 0.08,
                        "limit_value": 0.05,
                    },
                    {"breach_id": "lim_2", "rule_id": "max_var", "severity": "high", "status": "open"},
                    {"breach_id": "lim_3", "rule_id": "max_var", "severity": "medium", "status": "open"},
                    {"breach_id": "lim_4", "rule_id": "max_cash", "severity": "medium", "status": "open"},
                    {"breach_id": "lim_5", "rule_id": "max_cash", "status": "approved_exception"},
                ]
            },
            "pf_test",
        )
    }
    stress_types = {
        record.anomaly_type
        for record in detect_stress_anomalies(
            {
                "stress_runs": [
                    {"run_id": "stress_1", "scenario_id": "risk_off", "percent_loss": 0.30, "severity": "critical"},
                    {"run_id": "stress_0", "scenario_id": "risk_off", "percent_loss": 0.10, "severity": "medium"},
                ]
            },
            "pf_test",
        )
    }
    rates_options_types = {
        record.anomaly_type
        for record in detect_rates_options_anomalies(
            {
                "positions": [
                    {
                        "id": "opt_1",
                        "symbol": "AAPL_C",
                        "asset_type": "option",
                        "duration": 8.5,
                        "dv01": 650,
                        "vega": 6_100,
                        "gamma": 140,
                    }
                ]
            },
            "pf_test",
        )
    }

    assert {"critical_break", "old_open_break", "recurring_break"} <= reconciliation_types
    assert {"critical_limit_breach", "exception_without_note", "open_breach_cluster", "repeated_limit_breach"} <= limit_types
    assert {"severe_stress_loss", "critical_stress_severity", "stress_deterioration"} <= stress_types
    assert {"high_duration", "option_exposure_placeholder", "high_dv01", "high_vega_exposure", "high_gamma_exposure"} <= rates_options_types


def test_scoring_mapping_and_review_workflow_transitions() -> None:
    score, severity, confidence, explanation = score_anomaly(
        magnitude=0.9,
        portfolio_impact=0.8,
        recurrence=3,
        data_quality_penalty=10,
    )
    anomaly = build_anomaly(
        portfolio_id="pf_test",
        module_name="Risk Monitor",
        category="risk",
        anomaly_type="test",
        title="Test anomaly",
        description="Synthetic test anomaly.",
        metric_name="test_metric",
        observed_value=1,
        threshold=0,
        score=score,
        severity=severity,
        confidence=confidence,
        explanation=explanation,
    )

    assert score > 76
    assert anomaly.severity == "critical"
    assert anomaly.confidence == "high"

    under_review, event_1 = apply_review_action(
        anomaly,
        AnomalyReviewRequest(action="mark_under_review", reviewer="risk"),
    )
    explained, event_2 = apply_review_action(
        under_review,
        AnomalyReviewRequest(action="explain", reviewer="risk", note="Known data issue."),
    )
    resolved, event_3 = apply_review_action(
        explained,
        AnomalyReviewRequest(action="resolve", reviewer="risk", decision="Closed."),
    )
    reopened, event_4 = apply_review_action(
        resolved,
        AnomalyReviewRequest(action="reopen", reviewer="risk"),
    )
    ignored, event_5 = apply_review_action(
        reopened,
        AnomalyReviewRequest(action="ignore", reviewer="risk", decision="Immaterial."),
    )
    reopened_again, event_6 = apply_review_action(
        ignored,
        AnomalyReviewRequest(action="reopen", reviewer="risk"),
    )

    assert event_1.to_status == "under_review"
    assert event_2.to_status == "explained"
    assert event_3.to_status == "resolved"
    assert event_4.to_status == "open"
    assert event_5.to_status == "ignored"
    assert event_6.to_status == "open"
    assert len(reopened_again.review_history) == 6
