import pytest

from app.modules.equity_analysis.domain.capm import (
    calculate_capm_required_return,
    calculate_market_risk_premium,
    classify_required_return_signal,
    create_capm_warnings,
)
from app.modules.equity_analysis.domain.data_quality import (
    create_equity_data_quality_score,
    detect_missing_fundamental_fields,
    validate_fcf_consistency,
    validate_market_cap_consistency,
)
from app.modules.equity_analysis.domain.dcf import (
    calculate_enterprise_value_from_fcff,
    calculate_equity_value_from_enterprise_value,
    calculate_fcfe,
    calculate_fcff,
    calculate_intrinsic_value_per_share,
    calculate_terminal_value_gordon,
    discount_cash_flows,
)
from app.modules.equity_analysis.domain.dupont import (
    calculate_dupont_roe,
    calculate_extended_dupont_roe,
    calculate_financial_leverage,
)
from app.modules.equity_analysis.domain.earnings_quality import (
    calculate_accruals_ratio,
    calculate_cash_conversion_ratio,
    calculate_fcf_conversion_ratio,
    classify_earnings_quality,
)
from app.modules.equity_analysis.domain.historical_fundamentals import (
    calculate_cagr,
    calculate_margin_trends,
    calculate_year_over_year_growth,
)


def test_capm_required_return_and_warnings() -> None:
    premium = calculate_market_risk_premium(0.08, 0.04)

    assert premium == pytest.approx(0.04)
    assert calculate_capm_required_return(0.04, 1.2, premium) == pytest.approx(0.088)
    assert classify_required_return_signal(0.03) == "Expected return exceeds required return"
    assert "negative" in create_capm_warnings(-0.2, 0.04, 0.04)[0].lower()
    assert "missing" in create_capm_warnings(None, 0.04, 0.04)[0].lower()


def test_dupont_three_step_and_extended_fallback() -> None:
    leverage = calculate_financial_leverage(120, 60)

    assert leverage == pytest.approx(2.0)
    assert calculate_dupont_roe(0.10, 1.5, leverage) == pytest.approx(0.30)
    assert calculate_dupont_roe(0.10, None, leverage) is None
    assert calculate_extended_dupont_roe(None, 0.9, 0.2, 1.5, 2.0) is None
    assert calculate_extended_dupont_roe(0.8, 0.9, 0.2, 1.5, 2.0) == pytest.approx(0.432)


def test_earnings_quality_ratios_and_classification() -> None:
    cash_conversion = calculate_cash_conversion_ratio(120, 100)
    accruals = calculate_accruals_ratio(100, 120, 500)
    fcf_conversion = calculate_fcf_conversion_ratio(80, 100)

    assert cash_conversion == pytest.approx(1.2)
    assert accruals == pytest.approx(-0.04)
    assert fcf_conversion == pytest.approx(0.8)
    assert classify_earnings_quality(
        cash_conversion,
        accruals,
        fcf_conversion,
    ) == "High earnings quality"


def test_historical_fundamentals_trends() -> None:
    history = [
        {"year": 2024, "revenue": 100.0, "net_income": 10.0},
        {"year": 2025, "revenue": 110.0, "net_income": 14.0},
    ]

    assert calculate_cagr(100, 121, 2) == pytest.approx(0.10)
    assert calculate_year_over_year_growth(history, "revenue")[0]["growth"] == pytest.approx(0.10)
    assert calculate_margin_trends(history, "net_income")[1]["margin"] == pytest.approx(14 / 110)


def test_dcf_foundation_functions() -> None:
    fcff = calculate_fcff(100, 0.25, 10, 20, 5)
    fcfe = calculate_fcfe(70, 10, 20, 5, 3)

    assert fcff == pytest.approx(60)
    assert fcfe == pytest.approx(58)
    assert discount_cash_flows([100], 0.10)[0] == pytest.approx(90.9090909)
    assert calculate_terminal_value_gordon(100, 0.10, 0.03) == pytest.approx(1471.428571)
    enterprise_value = calculate_enterprise_value_from_fcff([60, 65], 0.10, 0.03)
    assert enterprise_value > 800
    assert calculate_equity_value_from_enterprise_value(1000, 200, 50) == 850
    assert calculate_intrinsic_value_per_share(850, 10) == 85

    with pytest.raises(ValueError, match="greater than terminal growth"):
        calculate_terminal_value_gordon(100, 0.03, 0.03)


def test_equity_data_quality_helpers() -> None:
    fundamentals = {"revenue": 100, "eps": None, "free_cash_flow": 80}

    assert detect_missing_fundamental_fields(fundamentals) == [
        "eps",
        "assets",
        "liabilities",
        "equity",
        "debt",
        "cash",
        "operating_cash_flow",
        "capital_expenditures",
    ]
    assert validate_market_cap_consistency(1000, 100, 10) is True
    assert validate_fcf_consistency(80, 100, 20) is True
    assert create_equity_data_quality_score(["warning"], ["eps"]) == pytest.approx(0.82)
