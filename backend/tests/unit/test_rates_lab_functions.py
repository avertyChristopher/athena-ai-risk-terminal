from datetime import date

import pytest

from app.modules.rates_lab.domain.bonds import (
    clean_price,
    price_dated_coupon_bond,
    price_dated_zero_coupon_bond,
    price_coupon_bond,
    price_zero_coupon_bond,
)
from app.modules.rates_lab.domain.cashflows import (
    calculate_accrued_interest,
    calculate_coupon_payment,
    generate_dated_bond_cashflows,
    generate_dated_coupon_schedule,
    generate_bond_cashflows,
    generate_coupon_schedule,
    get_next_coupon_date,
    get_previous_coupon_date,
    zero_coupon_cashflow,
)
from app.modules.rates_lab.domain.convexity import (
    convexity,
    convexity_adjusted_price_impact,
)
from app.modules.rates_lab.domain.curves import (
    calculate_forward_rates,
    classify_curve_shape,
    interpolate_curve_linear,
)
from app.modules.rates_lab.domain.duration import (
    duration_price_impact,
    dv01,
    macaulay_duration,
    modified_duration,
)
from app.modules.rates_lab.domain.scenarios import (
    apply_curve_scenario,
    calculate_effective_yield_shock,
    flattener_shift,
    parallel_shift,
    scenario_price_impact,
    steepener_shift,
)
from app.modules.rates_lab.domain.yields import (
    current_yield,
    holding_period_return,
    price_premium_discount_status,
    yield_to_maturity,
)


def test_coupon_payment_schedule_and_final_principal() -> None:
    schedule = generate_coupon_schedule(2, "semiannual")
    cashflows = generate_bond_cashflows(1000, 0.06, "semiannual", 2)

    assert schedule == [0.5, 1.0, 1.5, 2.0]
    assert calculate_coupon_payment(1000, 0.06, "semiannual") == 30
    assert len(cashflows) == 4
    assert cashflows[0]["total_cash_flow"] == 30
    assert cashflows[-1]["total_cash_flow"] == 1030
    assert cashflows[-1]["principal"] == 1000


def test_dated_coupon_bond_clean_price_is_near_par_when_coupon_equals_yield() -> None:
    settlement = date(2026, 3, 1)
    maturity = date(2030, 12, 31)
    dirty, cashflows, metadata = price_dated_coupon_bond(
        1000,
        0.05,
        "semiannual",
        settlement,
        maturity,
        0.05,
    )
    accrued = float(metadata["accrued_interest"])

    assert clean_price(dirty, accrued) == pytest.approx(1000, abs=0.15)
    assert dirty == pytest.approx(clean_price(dirty, accrued) + accrued)
    assert accrued > 0
    assert cashflows[0]["payment_date"] == date(2026, 6, 30)
    assert cashflows[-1]["payment_date"] == maturity


def test_dated_coupon_period_and_accrued_interest_boundaries() -> None:
    maturity = date(2030, 12, 31)
    coupon_settlement = date(2025, 12, 31)
    between_settlement = date(2026, 3, 1)

    assert generate_dated_coupon_schedule(coupon_settlement, maturity, "semiannual")[0] == date(2026, 6, 30)
    previous = get_previous_coupon_date(coupon_settlement, maturity, "semiannual")
    next_coupon = get_next_coupon_date(coupon_settlement, maturity, "semiannual")
    accrued_on_coupon, accrued_days, _ = calculate_accrued_interest(
        1000,
        0.05,
        "semiannual",
        coupon_settlement,
        previous,
        next_coupon,
    )
    _, between_metadata = generate_dated_bond_cashflows(
        1000,
        0.05,
        "semiannual",
        between_settlement,
        maturity,
    )

    assert accrued_on_coupon == pytest.approx(0)
    assert accrued_days == 0
    assert float(between_metadata["accrued_interest"]) > 0


def test_dated_zero_coupon_has_no_accrued_interest() -> None:
    dirty, cashflows, metadata = price_dated_zero_coupon_bond(
        1000,
        date(2026, 1, 1),
        date(2031, 1, 1),
        0.05,
    )

    assert dirty < 1000
    assert cashflows[-1]["principal"] == 1000
    assert metadata["accrued_interest"] == 0


def test_fractional_maturity_creates_final_stub_at_actual_maturity() -> None:
    cashflows = generate_bond_cashflows(1000, 0.05, "semiannual", 5.2)
    duration = macaulay_duration(cashflows, 0.05, "semiannual")

    assert cashflows[-2]["time_years"] == pytest.approx(5.0)
    assert cashflows[-1]["time_years"] == pytest.approx(5.2)
    assert cashflows[-1]["principal"] == 1000
    assert cashflows[-1]["accrual_fraction"] == pytest.approx(0.4)
    assert 0 < duration < 5.2


@pytest.mark.parametrize(
    ("frequency", "periods"),
    [("annual", 2), ("semiannual", 4), ("quarterly", 8), ("monthly", 24)],
)
def test_coupon_frequency_controls_cashflow_count(
    frequency: str,
    periods: int,
) -> None:
    assert len(generate_coupon_schedule(2, frequency)) == periods


def test_zero_coupon_bond_price_matches_discounted_face_value() -> None:
    price, cashflows = price_zero_coupon_bond(1000, 5, 0.05)

    assert price == pytest.approx(1000 / 1.05**5)
    assert cashflows[-1]["principal"] == 1000


def test_coupon_bond_is_par_when_coupon_rate_equals_yield() -> None:
    price, _ = price_coupon_bond(1000, 0.05, "semiannual", 10, 0.05)

    assert price == pytest.approx(1000, rel=1e-10)
    assert price_premium_discount_status(price, 1000) == "par"


def test_discount_and_premium_bond_relationships() -> None:
    discount_price, _ = price_coupon_bond(1000, 0.04, "annual", 5, 0.06)
    premium_price, _ = price_coupon_bond(1000, 0.07, "annual", 5, 0.05)

    assert discount_price < 1000
    assert premium_price > 1000
    assert price_premium_discount_status(discount_price, 1000) == "discount"
    assert price_premium_discount_status(premium_price, 1000) == "premium"


def test_current_yield_ytm_solver_and_holding_period_return() -> None:
    market_price, _ = price_coupon_bond(1000, 0.05, "semiannual", 7, 0.06)
    solved = yield_to_maturity(
        market_price,
        1000,
        0.05,
        "semiannual",
        7,
    )

    assert current_yield(1000, 0.05, 950) == pytest.approx(50 / 950)
    assert solved["converged"] is True
    assert solved["yield_to_maturity"] == pytest.approx(0.06, rel=1e-7)
    assert holding_period_return(950, 980, 25) == pytest.approx(55 / 950)


def test_duration_convexity_and_dv01_have_expected_properties() -> None:
    cashflows = generate_bond_cashflows(1000, 0.05, "semiannual", 10)
    price, _ = price_coupon_bond(1000, 0.05, "semiannual", 10, 0.06)
    macaulay = macaulay_duration(cashflows, 0.06, "semiannual")
    modified = modified_duration(macaulay, 0.06, "semiannual")
    convexity_value = convexity(cashflows, 0.06, "semiannual")
    duration_change = duration_price_impact(price, modified, 0.01)
    adjusted_change = convexity_adjusted_price_impact(
        price,
        modified,
        convexity_value,
        0.01,
    )

    assert macaulay > 0
    assert modified < macaulay
    assert convexity_value > 0
    assert dv01(price, modified) > 0
    assert duration_change < 0
    assert adjusted_change != pytest.approx(duration_change)
    assert adjusted_change > duration_change


def test_zero_coupon_macaulay_duration_equals_maturity() -> None:
    cashflows = zero_coupon_cashflow(1000, 8)

    assert macaulay_duration(cashflows, 0.05, "annual") == pytest.approx(8)


def test_curve_interpolation_forward_rates_and_shape_classification() -> None:
    normal_curve = [
        {"maturity": 1.0, "rate": 0.03},
        {"maturity": 5.0, "rate": 0.04},
        {"maturity": 10.0, "rate": 0.045},
    ]
    interpolated = interpolate_curve_linear(normal_curve, [1, 3, 5, 10])
    forwards = calculate_forward_rates(interpolated)

    assert interpolated[1]["rate"] == pytest.approx(0.035)
    assert len(forwards) == 3
    assert forwards[0]["forward_rate"] > interpolated[0]["rate"]
    assert classify_curve_shape(normal_curve) == "steep"
    assert classify_curve_shape(
        [{"maturity": 1, "rate": 0.05}, {"maturity": 10, "rate": 0.03}]
    ) == "inverted"
    assert classify_curve_shape(
        [{"maturity": 1, "rate": 0.04}, {"maturity": 10, "rate": 0.0405}]
    ) == "flat"


def test_rate_scenarios_move_prices_in_the_expected_direction() -> None:
    cashflows = generate_bond_cashflows(1000, 0.05, "semiannual", 5)
    macaulay = macaulay_duration(cashflows, 0.05, "semiannual")
    modified = modified_duration(macaulay, 0.05, "semiannual")
    convexity_value = convexity(cashflows, 0.05, "semiannual")
    up = scenario_price_impact(
        1000,
        0.05,
        "semiannual",
        5,
        0.05,
        modified,
        convexity_value,
        "parallel_up",
        100,
    )
    down = scenario_price_impact(
        1000,
        0.05,
        "semiannual",
        5,
        0.05,
        modified,
        convexity_value,
        "parallel_down",
        100,
    )

    assert up["stressed_price"] < up["base_price"]
    assert down["stressed_price"] > down["base_price"]


def test_curve_shift_functions_return_structured_distinct_scenarios() -> None:
    curve = [
        {"maturity": 1.0, "rate": 0.03},
        {"maturity": 10.0, "rate": 0.04},
    ]
    parallel = parallel_shift(curve, 100)
    steepener = steepener_shift(curve, 100)
    flattener = flattener_shift(curve, 100)

    assert parallel[0]["rate"] == pytest.approx(0.04)
    assert steepener[0]["rate"] < curve[0]["rate"]
    assert steepener[-1]["rate"] > curve[-1]["rate"]
    assert flattener[0]["rate"] > curve[0]["rate"]
    assert flattener[-1]["rate"] < curve[-1]["rate"]


def test_curve_scenarios_drive_the_same_effective_bond_shock() -> None:
    curve = [
        {"maturity": 1.0, "rate": 0.03},
        {"maturity": 5.0, "rate": 0.04},
        {"maturity": 10.0, "rate": 0.05},
    ]
    parallel = apply_curve_scenario(curve, "parallel_up", 100)
    steepener = apply_curve_scenario(curve, "steepener", 100)
    flattener = apply_curve_scenario(curve, "flattener", 100)
    effective_shock = calculate_effective_yield_shock(curve, steepener, 5.0)

    assert all(
        stressed["rate"] - base["rate"] == pytest.approx(0.01)
        for base, stressed in zip(curve, parallel)
    )
    assert steepener[-1]["rate"] - steepener[0]["rate"] > curve[-1]["rate"] - curve[0]["rate"]
    assert flattener[-1]["rate"] - flattener[0]["rate"] < curve[-1]["rate"] - curve[0]["rate"]

    cashflows = generate_bond_cashflows(1000, 0.05, "semiannual", 5)
    macaulay = macaulay_duration(cashflows, 0.05, "semiannual")
    modified = modified_duration(macaulay, 0.05, "semiannual")
    result = scenario_price_impact(
        1000,
        0.05,
        "semiannual",
        5,
        0.05,
        modified,
        convexity(cashflows, 0.05, "semiannual"),
        "steepener",
        100,
        curve,
        steepener,
    )

    assert result["effective_shock_bps"] == pytest.approx(effective_shock)
    assert result["shocked_yield_at_maturity"] == pytest.approx(steepener[1]["rate"])
    assert result["stressed_price"] != pytest.approx(result["base_price"])
