import pytest

from app.modules.options_pricing_lab.domain.binomial import binomial_option_price
from app.modules.options_pricing_lab.domain.black_scholes import (
    black_scholes_call_price,
    black_scholes_price,
    black_scholes_put_price,
    d1,
    d2,
)
from app.modules.options_pricing_lab.domain.greeks import option_greeks
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
from app.modules.options_pricing_lab.domain.strategies import strategy_summary


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
    assert summary["max_loss"] >= 0
    assert "Defined-risk bullish" in str(summary["risk_profile"])
    assert summary["payoff_table"]
