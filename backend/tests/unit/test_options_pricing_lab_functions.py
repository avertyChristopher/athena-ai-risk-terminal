import pytest

from app.modules.options_pricing_lab.domain.binomial import binomial_option_price
from app.modules.options_pricing_lab.domain.black_scholes import (
    black_scholes_call_price,
    black_scholes_price,
    black_scholes_put_price,
    d1,
    d2,
)
from app.modules.options_pricing_lab.domain.greeks import (
    aggregate_strategy_greeks,
    option_greeks,
)
from app.modules.options_pricing_lab.domain.implied_volatility import (
    solve_implied_volatility,
)
from app.modules.options_pricing_lab.domain.moneyness import classify_moneyness
from app.modules.options_pricing_lab.domain.payoff import (
    breakeven_call,
    breakeven_put,
    option_payoff,
    option_profit,
)
from app.modules.options_pricing_lab.domain.put_call_parity import (
    put_call_parity_check,
)
from app.modules.options_pricing_lab.domain.risk_summary import (
    single_option_risk_summary,
)
from app.modules.options_pricing_lab.domain.scenarios import sensitivity_analysis
from app.modules.options_pricing_lab.domain.strategies import (
    build_predefined_strategy_legs,
    strategy_summary,
)


def test_call_and_put_payoff_profit_and_breakeven_logic() -> None:
    assert option_payoff(120, 100, "call", "long") == 20
    assert option_payoff(120, 100, "call", "short") == -20
    assert option_payoff(80, 100, "put", "long") == 20
    assert option_payoff(80, 100, "put", "short") == -20
    assert option_profit(20, 5, "long") == 15
    assert option_profit(-20, 5, "short") == -15
    assert breakeven_call(100, 5) == 105
    assert breakeven_put(100, 5) == 95


def test_moneyness_classification_handles_calls_puts_and_atm() -> None:
    assert classify_moneyness(110, 100, "call") == "in_the_money"
    assert classify_moneyness(90, 100, "call") == "out_of_the_money"
    assert classify_moneyness(90, 100, "put") == "in_the_money"
    assert classify_moneyness(110, 100, "put") == "out_of_the_money"
    assert classify_moneyness(100.5, 100, "call") == "at_the_money"


def test_black_scholes_prices_and_put_call_parity_are_consistent() -> None:
    call_price = black_scholes_call_price(100, 100, 1, 0.05, 0.2)
    put_price = black_scholes_put_price(100, 100, 1, 0.05, 0.2)
    parity = put_call_parity_check(call_price, put_price, 100, 100, 1, 0.05)

    assert call_price == pytest.approx(10.4506, rel=1e-4)
    assert put_price == pytest.approx(5.5735, rel=1e-4)
    assert d1(100, 100, 1, 0.05, 0.2) == pytest.approx(0.35)
    assert d2(100, 100, 1, 0.05, 0.2) == pytest.approx(0.15)
    assert parity["status"] == "aligned"
    assert parity["parity_gap"] == pytest.approx(0.0)


def test_black_scholes_rejects_invalid_inputs() -> None:
    with pytest.raises(ValueError):
        black_scholes_price("call", 0, 100, 1, 0.05, 0.2)


def test_greeks_return_expected_signs_and_contract_exposures() -> None:
    long_call = option_greeks("call", 100, 100, 1, 0.05, 0.2)
    short_put = option_greeks("put", 100, 100, 1, 0.05, 0.2, position_side="short")

    assert 0 < long_call["delta"] < 1
    assert long_call["gamma"] > 0
    assert long_call["vega"] > 0
    assert long_call["theta_daily"] < 0
    assert short_put["delta"] > 0
    assert short_put["gamma"] < 0
    assert short_put["vega"] < 0


def test_binomial_price_converges_near_black_scholes() -> None:
    binomial = binomial_option_price("call", 100, 100, 1, 0.05, 0.2, steps=150)
    black_scholes = black_scholes_call_price(100, 100, 1, 0.05, 0.2)

    assert binomial["price"] == pytest.approx(black_scholes, rel=1e-2)
    assert 0 < binomial["risk_neutral_probability"] < 1
    assert binomial["no_arbitrage_valid"] is True


def test_binomial_reports_invalid_no_arbitrage_parameters_without_clipping() -> None:
    result = binomial_option_price("call", 100, 100, 1, 1.0, 0.01, steps=1)

    assert result["no_arbitrage_valid"] is False
    assert result["price"] is None
    assert result["risk_neutral_probability"] > 1
    assert "no-arbitrage" in str(result["warning"])


def test_strategy_summary_reports_defined_risk_spread() -> None:
    summary = strategy_summary(
        "bull_call_spread",
        100,
        [
            {
                "option_type": "call",
                "side": "long",
                "strike": 100,
                "expiration_days": 60,
                "quantity": 1,
                "premium": 5,
            },
            {
                "option_type": "call",
                "side": "short",
                "strike": 110,
                "expiration_days": 60,
                "quantity": 1,
                "premium": 2,
            },
        ],
    )

    assert summary["net_premium"] == pytest.approx(300)
    assert summary["max_loss"]["value"] == pytest.approx(300)
    assert summary["max_profit"]["value"] == pytest.approx(700)
    assert summary["breakeven_points"] == pytest.approx([103])
    assert "Defined-risk bullish" in str(summary["risk_profile"])
    assert summary["payoff_table"]


@pytest.mark.parametrize(
    ("strategy_type", "leg_types", "sides"),
    [
        ("covered_call", ["stock", "option"], ["long", "short"]),
        ("protective_put", ["stock", "option"], ["long", "long"]),
        ("collar", ["stock", "option", "option"], ["long", "long", "short"]),
    ],
)
def test_predefined_stock_strategies_include_the_underlying_leg(
    strategy_type: str,
    leg_types: list[str],
    sides: list[str],
) -> None:
    legs = build_predefined_strategy_legs(strategy_type, 100)

    assert [leg["leg_type"] for leg in legs] == leg_types
    assert [leg["side"] for leg in legs] == sides
    assert legs[0]["quantity"] == 100
    assert legs[0]["contract_size"] == 1


def test_cash_secured_put_includes_full_cash_collateral() -> None:
    legs = build_predefined_strategy_legs("cash_secured_put", 100, 100, 2)
    legs[0]["premium"] = 4
    summary = strategy_summary("cash_secured_put", 100, legs)

    assert [leg["leg_type"] for leg in legs] == ["option", "cash"]
    assert summary["collateral_requirement"] == pytest.approx(20_000)
    assert summary["max_profit"]["value"] == pytest.approx(800)
    assert summary["max_loss"]["value"] == pytest.approx(19_200)


def test_single_option_risk_identities() -> None:
    long_call = single_option_risk_summary("call", "long", 100, 5, 100, 1)
    long_put = single_option_risk_summary("put", "long", 100, 4, 100, 1)
    short_call = single_option_risk_summary("call", "short", 100, 5, 100, 1)

    assert long_call["max_profit"] is None
    assert long_call["max_loss"] == pytest.approx(500)
    assert long_put["max_loss"] == pytest.approx(400)
    assert short_call["max_loss"] is None


def test_straddle_has_unlimited_profit_finite_loss_and_two_breakevens() -> None:
    legs = [
        _option_leg("call", "long", 100, 5),
        _option_leg("put", "long", 100, 5),
    ]
    summary = strategy_summary("long_straddle", 100, legs)

    assert summary["max_profit"]["type"] == "unlimited"
    assert summary["max_loss"]["value"] == pytest.approx(1_000)
    assert summary["breakeven_points"] == pytest.approx([90, 110])


def test_bear_put_spread_risk_and_breakeven_are_analytical() -> None:
    legs = [
        _option_leg("put", "long", 110, 8),
        _option_leg("put", "short", 100, 3),
    ]
    summary = strategy_summary("bear_put_spread", 105, legs)

    assert summary["max_profit"]["value"] == pytest.approx(500)
    assert summary["max_loss"]["value"] == pytest.approx(500)
    assert summary["breakeven_points"] == pytest.approx([105])


def test_stock_delta_and_contract_quantity_scaling_are_aggregated() -> None:
    legs = build_predefined_strategy_legs("covered_call", 100, 100, 2)
    aggregate = aggregate_strategy_greeks(legs, 100, 0.05, 0.2, 0)

    option_delta = aggregate["legs"][1]["raw_greeks"]["delta"]
    expected_delta = 200 + option_delta * 100 * 2
    assert aggregate["aggregate_delta"] == pytest.approx(expected_delta)
    assert aggregate["delta_adjusted_exposure"] == pytest.approx(
        expected_delta * 100
    )
    assert aggregate["legs"][0]["position_greeks"]["delta"] == 200


def test_observed_put_call_parity_detects_a_material_deviation() -> None:
    result = put_call_parity_check(
        12,
        1,
        100,
        100,
        1,
        0.05,
        mode="observed",
    )

    assert result["mode"] == "observed"
    assert result["status"] == "potential_arbitrage"
    assert result["absolute_gap"] > 1


@pytest.mark.parametrize("option_type", ["call", "put"])
def test_implied_volatility_recovers_known_black_scholes_volatility(
    option_type: str,
) -> None:
    market_price = black_scholes_price(option_type, 100, 100, 1, 0.05, 0.2)
    result = solve_implied_volatility(
        market_price,
        option_type,
        100,
        100,
        1,
        0.05,
    )

    assert result["converged"] is True
    assert result["validation_status"] == "valid"
    assert result["implied_volatility"] == pytest.approx(0.2, rel=1e-5)


def test_implied_volatility_rejects_prices_outside_bounds_and_handles_limits() -> None:
    outside = solve_implied_volatility(101, "call", 100, 100, 1, 0.05)
    limited = solve_implied_volatility(
        10,
        "call",
        100,
        100,
        1,
        0.05,
        tolerance=1e-12,
        max_iterations=1,
    )

    assert outside["validation_status"] == "outside_no_arbitrage_bounds"
    assert outside["implied_volatility"] is None
    assert limited["converged"] is False
    assert limited["validation_status"] == "non_converged"


def test_time_scenarios_are_capped_at_expiration() -> None:
    scenarios = sensitivity_analysis(
        "call",
        100,
        100,
        30 / 365,
        0.05,
        0.2,
        0,
        time_points_days=[1, 7, 30, 60, 90],
    )
    time_points = [row["value"] for row in scenarios["time_decay"]]

    assert time_points == [1.0, 7.0, 30.0]
    assert max(time_points) <= 30
    assert scenarios["scenario_metadata"]["time_scenarios_capped"] is True


def _option_leg(
    option_type: str,
    side: str,
    strike_price: float,
    premium: float,
) -> dict[str, object]:
    return {
        "leg_type": "option",
        "option_type": option_type,
        "side": side,
        "strike_price": strike_price,
        "expiration_days": 60,
        "quantity": 1,
        "contract_size": 100,
        "premium": premium,
    }
