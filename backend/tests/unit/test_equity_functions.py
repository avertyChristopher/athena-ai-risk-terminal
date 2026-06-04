import pytest

from app.modules.equity_analysis.domain import (
    calculate_debt_to_assets,
    calculate_current_ratio,
    calculate_debt_to_equity,
    calculate_dividend_payout_ratio,
    calculate_dividend_yield,
    calculate_earnings_yield,
    calculate_ebitda_margin,
    calculate_ev_ebitda,
    calculate_free_cash_flow_yield,
    calculate_gordon_growth_value,
    calculate_gross_margin,
    calculate_implied_cost_of_equity,
    calculate_implied_growth_rate,
    calculate_margin_of_safety,
    calculate_net_margin,
    calculate_operating_margin,
    calculate_pb_ratio,
    calculate_pe_ratio,
    calculate_ps_ratio,
    calculate_quick_ratio,
    calculate_roa,
    calculate_retention_ratio,
    calculate_roe,
    calculate_sustainable_growth_rate,
    calculate_valuation_status,
    classify_balance_sheet_quality,
    classify_dividend_profile,
    classify_equity_risk_profile,
    classify_growth_profile,
    classify_profitability_quality,
    classify_valuation_profile,
)


def test_gordon_growth_model_valuation() -> None:
    value = calculate_gordon_growth_value(
        dividend_next_year=3.0,
        required_return=0.09,
        growth_rate=0.03,
    )

    assert value == pytest.approx(50.0)


def test_gordon_growth_rejects_required_return_below_growth() -> None:
    with pytest.raises(ValueError, match="greater than growth"):
        calculate_gordon_growth_value(
            dividend_next_year=3.0,
            required_return=0.03,
            growth_rate=0.03,
        )


def test_implied_cost_of_equity() -> None:
    assert calculate_implied_cost_of_equity(
        dividend_next_year=2.0,
        current_price=50.0,
        growth_rate=0.04,
    ) == pytest.approx(0.08)


def test_implied_growth_rate() -> None:
    assert calculate_implied_growth_rate(
        dividend_next_year=2.0,
        current_price=50.0,
        required_return=0.08,
    ) == pytest.approx(0.04)


def test_valuation_multiples_and_yields() -> None:
    assert calculate_pe_ratio(price=100.0, earnings_per_share=5.0) == pytest.approx(20)
    assert calculate_pb_ratio(price=100.0, book_value_per_share=25.0) == pytest.approx(
        4,
    )
    assert calculate_ps_ratio(market_cap=1000.0, revenue=250.0) == pytest.approx(4.0)
    assert calculate_ev_ebitda(
        enterprise_value=1200.0,
        ebitda=200.0,
    ) == pytest.approx(6.0)
    assert calculate_dividend_yield(
        dividend_per_share=2.0,
        price=100.0,
    ) == pytest.approx(0.02)
    assert calculate_earnings_yield(
        earnings_per_share=5.0,
        price=100.0,
    ) == pytest.approx(0.05)
    assert calculate_free_cash_flow_yield(
        free_cash_flow=50.0,
        market_cap=1000.0,
    ) == pytest.approx(0.05)


def test_margin_of_safety() -> None:
    assert calculate_margin_of_safety(
        intrinsic_value=120.0,
        market_price=100.0,
    ) == pytest.approx(1 / 6)


def test_valuation_status_uses_model_signal_wording() -> None:
    assert calculate_valuation_status(0.20) == "Model-implied discount"
    assert calculate_valuation_status(-0.20) == "Model-implied premium"
    assert calculate_valuation_status(0.02) == "Near model fair value"
    assert calculate_valuation_status(None) == "Insufficient valuation inputs"


def test_profitability_ratios() -> None:
    assert calculate_gross_margin(gross_profit=40.0, revenue=100.0) == pytest.approx(
        0.40,
    )
    assert calculate_operating_margin(
        operating_income=25.0,
        revenue=100.0,
    ) == pytest.approx(0.25)
    assert calculate_ebitda_margin(ebitda=30.0, revenue=100.0) == pytest.approx(0.30)
    assert calculate_net_margin(net_income=18.0, revenue=100.0) == pytest.approx(0.18)
    assert calculate_roe(net_income=18.0, total_equity=60.0) == pytest.approx(0.30)
    assert calculate_roa(net_income=18.0, total_assets=120.0) == pytest.approx(0.15)


def test_balance_sheet_and_dividend_ratios() -> None:
    assert calculate_debt_to_equity(total_debt=30.0, total_equity=60.0) == pytest.approx(
        0.50,
    )
    assert calculate_debt_to_assets(total_debt=30.0, total_assets=120.0) == pytest.approx(
        0.25,
    )
    assert calculate_current_ratio(
        current_assets=150.0,
        current_liabilities=100.0,
    ) == pytest.approx(1.50)
    assert calculate_quick_ratio(
        cash_and_equivalents=20.0,
        receivables=30.0,
        marketable_securities=10.0,
        current_liabilities=40.0,
    ) == pytest.approx(1.50)

    payout = calculate_dividend_payout_ratio(
        dividend_per_share=1.0,
        earnings_per_share=4.0,
    )
    retention = calculate_retention_ratio(payout)

    assert payout == pytest.approx(0.25)
    assert retention == pytest.approx(0.75)
    assert calculate_sustainable_growth_rate(
        return_on_equity=0.20,
        retention_ratio=retention,
    ) == pytest.approx(0.15)


def test_liquidity_ratio_formulas_are_current_assets_and_quick_assets() -> None:
    assert calculate_current_ratio(
        current_assets=250.0,
        current_liabilities=125.0,
    ) == pytest.approx(2.0)
    assert calculate_quick_ratio(
        cash_and_equivalents=25.0,
        receivables=45.0,
        marketable_securities=30.0,
        current_liabilities=125.0,
    ) == pytest.approx(0.8)


def test_quality_classification_functions() -> None:
    assert classify_profitability_quality(
        net_margin=0.25,
        return_on_equity=0.30,
    ) == "High quality"
    assert classify_balance_sheet_quality(
        debt_to_equity=0.5,
        current_ratio=1.4,
        interest_coverage=15.0,
    ) == "Conservative"
    assert classify_growth_profile(
        revenue_growth=0.12,
        eps_growth=0.15,
        sustainable_growth_rate=0.09,
    ) == "Moderate growth"
    assert classify_dividend_profile(
        dividend_yield=0.025,
        payout_ratio=0.35,
    ) == "Income-oriented"
    assert classify_valuation_profile(
        margin_of_safety=-0.20,
        multiple_level="Premium",
    ) == "Valuation sensitivity elevated"
    assert classify_equity_risk_profile(
        beta=1.6,
        debt_to_equity=0.4,
        valuation_profile="Balanced model signal",
    ) == "Elevated equity risk"


def test_missing_denominators_return_none() -> None:
    assert calculate_pe_ratio(price=100.0, earnings_per_share=0.0) is None
    assert calculate_pb_ratio(price=100.0, book_value_per_share=0.0) is None
    assert calculate_ps_ratio(market_cap=1000.0, revenue=0.0) is None
    assert calculate_current_ratio(
        current_assets=100.0,
        current_liabilities=0.0,
    ) is None
    assert calculate_quick_ratio(
        cash_and_equivalents=20.0,
        receivables=30.0,
        marketable_securities=10.0,
        current_liabilities=0.0,
    ) is None
