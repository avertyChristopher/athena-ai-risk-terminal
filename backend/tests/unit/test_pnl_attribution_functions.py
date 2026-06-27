from app.modules.pnl_attribution.domain.fixed_income_pnl import estimate_fixed_income_effects
from app.modules.pnl_attribution.domain.pnl_calculation import (
    calculate_contribution_to_portfolio_return,
    calculate_position_price_pnl,
    calculate_total_pnl,
    calculate_total_pnl_percent,
)
from app.modules.pnl_attribution.domain.trade_effects import calculate_trade_effects
from app.modules.pnl_attribution.schemas import PositionPnlContribution


def test_core_pnl_formulas() -> None:
    total = calculate_total_pnl(1120, 1000)

    assert total == 120
    assert calculate_total_pnl_percent(total, 1000) == 0.12
    assert calculate_position_price_pnl(100, 112, 10) == 120
    assert calculate_contribution_to_portfolio_return(120, 1000) == 0.12


def test_duration_based_pnl_fallback_for_bond_like_holding() -> None:
    position = PositionPnlContribution(
        symbol="BND",
        name="Bond ETF",
        asset_type="fixed_income",
        asset_class="fixed_income",
        sector="Fixed Income",
        currency="USD",
        starting_price=70,
        ending_price=72,
        quantity=100,
        starting_value=7000,
        ending_value=7200,
        price_pnl=200,
        income_pnl=20,
        realized_pnl=0,
        unrealized_pnl=200,
        fees_and_costs=0,
        fx_pnl=0,
        total_pnl=220,
        total_pnl_percent=220 / 7000,
        contribution_to_total_pnl=1,
        contribution_to_portfolio_return=0.022,
        data_source="test",
    )

    effects, warnings = estimate_fixed_income_effects([position], [{}], True)

    assert effects
    assert effects[0].duration_source == "Demo Duration"
    assert warnings


def test_missing_trade_blotter_returns_prepared_warning() -> None:
    effect = calculate_trade_effects([], 100000, True)

    assert effect.status == "unavailable"
    assert "Future Trade Blotter integration prepared." in effect.warnings
