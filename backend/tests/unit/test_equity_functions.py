import pytest

from app.domain.equity import (
    calculate_current_ratio,
    calculate_debt_to_equity,
    calculate_dividend_payout_ratio,
    calculate_dividend_yield,
    calculate_gordon_growth_value,
    calculate_gross_margin,
    calculate_implied_cost_of_equity,
    calculate_margin_of_safety,
    calculate_net_margin,
    calculate_operating_margin,
    calculate_pb_ratio,
    calculate_pe_ratio,
    calculate_retention_ratio,
    calculate_roe,
    calculate_sustainable_growth_rate,
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


def test_valuation_multiples_and_yields() -> None:
    assert calculate_pe_ratio(price=100.0, earnings_per_share=5.0) == pytest.approx(20)
    assert calculate_pb_ratio(price=100.0, book_value_per_share=25.0) == pytest.approx(
        4,
    )
    assert calculate_dividend_yield(
        dividend_per_share=2.0,
        price=100.0,
    ) == pytest.approx(0.02)


def test_margin_of_safety() -> None:
    assert calculate_margin_of_safety(
        intrinsic_value=120.0,
        market_price=100.0,
    ) == pytest.approx(1 / 6)


def test_profitability_ratios() -> None:
    assert calculate_gross_margin(gross_profit=40.0, revenue=100.0) == pytest.approx(
        0.40,
    )
    assert calculate_operating_margin(
        operating_income=25.0,
        revenue=100.0,
    ) == pytest.approx(0.25)
    assert calculate_net_margin(net_income=18.0, revenue=100.0) == pytest.approx(0.18)
    assert calculate_roe(net_income=18.0, total_equity=60.0) == pytest.approx(0.30)


def test_balance_sheet_and_dividend_ratios() -> None:
    assert calculate_debt_to_equity(total_debt=30.0, total_equity=60.0) == pytest.approx(
        0.50,
    )
    assert calculate_current_ratio(
        current_assets=150.0,
        current_liabilities=100.0,
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
