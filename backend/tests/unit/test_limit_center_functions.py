from app.modules.limit_center.domain.breach_detection import evaluate_limit_payload
from app.modules.limit_center.domain.limit_rules import compare_values
from app.modules.limit_center.domain.review_workflow import apply_review_action
from app.modules.limit_center.domain.severity import (
    classify_breach_severity,
    determine_overall_status,
)
from app.modules.limit_center.domain.source_mapping import extract_limit_metrics
from app.modules.limit_center.repository import LimitCenterRepository


def test_default_rules_include_required_governance_categories() -> None:
    repository = LimitCenterRepository()
    repository.reset_demo_state()

    categories = {rule.category for rule in repository.list_rules()}

    assert {
        "portfolio",
        "risk",
        "stress",
        "fixed_income",
        "options",
        "trade",
    }.issubset(categories)


def test_comparison_operators_detect_breaches() -> None:
    assert compare_values(0.31, 0.25, "greater_than") is True
    assert compare_values(0.04, 0.05, "less_than") is True
    assert compare_values(True, True, "equal") is True
    assert compare_values(0.20, 0.25, "greater_than") is False


def test_extract_portfolio_builder_metrics() -> None:
    metrics, warnings = extract_limit_metrics(
        "portfolio_builder",
        {
            "concentration": {
                "largest_position": {"weight": 0.31},
                "top_3_weight": 0.72,
                "sector_exposures": [{"name": "Technology", "weight": 0.64}],
                "cash_weight": 0.03,
            }
        },
    )

    assert warnings == []
    assert metrics["single_position_weight"] == 0.31
    assert metrics["top_3_concentration"] == 0.72
    assert metrics["sector_exposure"] == 0.64
    assert metrics["cash_weight"] == 0.03


def test_extract_options_unlimited_loss_metric() -> None:
    metrics, warnings = extract_limit_metrics(
        "options_pricing_lab",
        {
            "max_loss": {"type": "unlimited", "value": None},
            "aggregate_greeks": {
                "delta_adjusted_exposure": 125000,
                "aggregate_vega": 6200,
            },
        },
    )

    assert warnings == []
    assert metrics["unlimited_loss"] is True
    assert metrics["delta_adjusted_exposure"] == 125000
    assert metrics["vega_exposure"] == 6200


def test_severity_classification_escalates_material_breaches() -> None:
    assert (
        classify_breach_severity(
            current_value=0.26,
            limit_value=0.25,
            operator="greater_than",
            base_severity="medium",
            metric_key="single_position_weight",
        )
        == "medium"
    )
    assert (
        classify_breach_severity(
            current_value=0.50,
            limit_value=0.25,
            operator="greater_than",
            base_severity="medium",
            metric_key="single_position_weight",
        )
        == "critical"
    )
    assert (
        classify_breach_severity(
            current_value=True,
            limit_value=True,
            operator="equal",
            base_severity="high",
            metric_key="unlimited_loss",
        )
        == "critical"
    )


def test_overall_status_escalates_with_multiple_high_breaches() -> None:
    repository = LimitCenterRepository()
    repository.reset_demo_state()
    rules = repository.list_rules()
    _, breaches, warnings = evaluate_limit_payload(
        portfolio_id="pf_001",
        source_module="risk_monitor",
        payload={
            "global_risk_score": 82,
            "risk_metrics": [
                {"name": "Portfolio volatility", "value": 0.31},
                {"name": "CVaR 95%", "value": 0.07},
            ],
        },
        rules=rules,
    )

    assert warnings
    assert determine_overall_status(breaches, warnings) == "critical_breach"


def test_review_workflow_valid_transitions() -> None:
    first = apply_review_action("open", "mark_under_review", "risk.manager", "Review required.")
    second = apply_review_action(first.to_status, "approve_exception", "cro", "Temporary exception.")
    reopened = apply_review_action("resolved", "reopen", "risk.manager")

    assert first.to_status == "under_review"
    assert second.to_status == "approved_exception"
    assert reopened.to_status == "open"


def test_review_workflow_rejects_invalid_transition() -> None:
    try:
        apply_review_action("open", "approve_exception", "risk.manager")
    except ValueError as exc:
        assert "not valid" in str(exc)
    else:
        raise AssertionError("Invalid transition should raise ValueError.")


def test_missing_payload_fields_return_warnings_not_crashes() -> None:
    repository = LimitCenterRepository()
    repository.reset_demo_state()

    evaluated, breaches, warnings = evaluate_limit_payload(
        portfolio_id="pf_001",
        source_module="rates_lab",
        payload={"module_name": "rates_lab"},
        rules=repository.list_rules(),
    )

    assert evaluated
    assert breaches == []
    assert warnings
