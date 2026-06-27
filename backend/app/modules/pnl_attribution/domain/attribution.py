from __future__ import annotations

from typing import Any

from app.modules.pnl_attribution.domain.contribution import (
    aggregate_group_contributions,
    top_winners_losers,
)
from app.modules.pnl_attribution.domain.fixed_income_pnl import estimate_fixed_income_effects
from app.modules.pnl_attribution.domain.fx import estimate_fx_effects
from app.modules.pnl_attribution.domain.income import estimate_income_pnl
from app.modules.pnl_attribution.domain.options_pnl import estimate_options_effects
from app.modules.pnl_attribution.domain.pnl_calculation import (
    calculate_contribution_to_portfolio_return,
    calculate_contribution_to_total_pnl,
    calculate_position_pnl_percent,
    calculate_position_price_pnl,
    calculate_total_pnl,
    calculate_total_pnl_percent,
)
from app.modules.pnl_attribution.domain.realized_unrealized import (
    calculate_realized_pnl_for_symbol,
    split_realized_unrealized,
)
from app.modules.pnl_attribution.domain.trade_effects import calculate_trade_effects
from app.modules.pnl_attribution.schemas import (
    BenchmarkComparison,
    PnlAttributionRequest,
    PositionPnlContribution,
)


def build_position_contributions(
    *,
    positions: list[dict[str, Any]],
    price_lookup: dict[str, dict[str, Any]],
    transactions: list[dict[str, Any]],
    period_days: int,
    include_income: bool,
    portfolio_starting_value: float,
) -> list[PositionPnlContribution]:
    contributions: list[PositionPnlContribution] = []
    for position in positions:
        symbol = str(position.get("symbol", "")).upper()
        quantity = _as_float(position.get("quantity")) or 0.0
        average_price = _as_float(position.get("average_price")) or 0.0
        current_price = _as_float(position.get("current_price")) or average_price
        prices = price_lookup.get(symbol, {})
        warnings = list(prices.get("warnings", []))
        starting_price = _as_float(prices.get("starting_price")) or average_price
        ending_price = _as_float(prices.get("ending_price")) or current_price
        starting_value = starting_price * quantity
        ending_value = ending_price * quantity
        price_pnl = calculate_position_price_pnl(starting_price, ending_price, quantity)
        income_pnl = estimate_income_pnl(position, starting_value, period_days, include_income)
        realized = calculate_realized_pnl_for_symbol(symbol, transactions, average_price)
        realized_pnl, unrealized_pnl = split_realized_unrealized(price_pnl, realized)
        total_pnl = price_pnl + income_pnl
        contributions.append(
            PositionPnlContribution(
                symbol=symbol,
                name=str(position.get("asset_name") or position.get("name") or symbol),
                asset_type=str(position.get("asset_type") or "asset"),
                asset_class=str(position.get("asset_class") or position.get("asset_type") or "asset"),
                sector=str(position.get("sector") or "Unclassified"),
                currency=str(position.get("currency") or "USD"),
                starting_price=starting_price,
                ending_price=ending_price,
                quantity=quantity,
                starting_value=starting_value,
                ending_value=ending_value,
                price_pnl=price_pnl,
                income_pnl=income_pnl,
                realized_pnl=realized_pnl,
                unrealized_pnl=unrealized_pnl,
                fees_and_costs=0.0,
                fx_pnl=0.0,
                total_pnl=total_pnl,
                total_pnl_percent=calculate_position_pnl_percent(total_pnl, starting_value),
                contribution_to_total_pnl=0.0,
                contribution_to_portfolio_return=calculate_contribution_to_portfolio_return(
                    total_pnl,
                    portfolio_starting_value,
                ),
                data_source=str(prices.get("data_source") or position.get("data_source") or "Portfolio Builder fallback"),
                warnings=warnings,
            ),
        )
    return contributions


def finalize_contributions(
    positions: list[PositionPnlContribution],
    total_pnl: float,
    trade_costs: float,
    portfolio_starting_value: float,
) -> list[PositionPnlContribution]:
    if not positions:
        return positions
    total_abs_start = sum(abs(position.starting_value) for position in positions) or 1.0
    finalized: list[PositionPnlContribution] = []
    for position in positions:
        cost_allocation = trade_costs * abs(position.starting_value) / total_abs_start
        total = position.total_pnl - cost_allocation + position.fx_pnl
        finalized.append(
            position.model_copy(
                update={
                    "fees_and_costs": cost_allocation,
                    "total_pnl": total,
                    "total_pnl_percent": calculate_position_pnl_percent(total, position.starting_value),
                    "contribution_to_total_pnl": calculate_contribution_to_total_pnl(total, total_pnl),
                    "contribution_to_portfolio_return": calculate_contribution_to_portfolio_return(
                        total,
                        portfolio_starting_value,
                    ),
                },
            ),
        )
    return finalized


def build_benchmark_comparison(
    request: PnlAttributionRequest,
    portfolio_return: float,
    benchmark_return: float | None,
    asset_class_contributions: list[Any],
) -> BenchmarkComparison:
    if benchmark_return is None:
        return BenchmarkComparison(
            benchmark_symbol=request.benchmark_symbol.upper(),
            portfolio_return=portfolio_return,
            benchmark_return=None,
            active_return=None,
            relative_performance="Benchmark unavailable",
            tracking_note="Benchmark return unavailable from Market Data for the selected period.",
        )
    active = portfolio_return - benchmark_return
    allocation_effect = None
    selection_effect = None
    interaction_effect = None
    if request.attribution_method == "Brinson-lite":
        allocation_effect = sum(row.weight_start * (row.pnl_percent - benchmark_return) for row in asset_class_contributions)
        selection_effect = active - allocation_effect
        interaction_effect = 0.0
    return BenchmarkComparison(
        benchmark_symbol=request.benchmark_symbol.upper(),
        portfolio_return=portfolio_return,
        benchmark_return=benchmark_return,
        active_return=active,
        relative_performance="Outperformed" if active >= 0 else "Underperformed",
        allocation_effect=allocation_effect,
        selection_effect=selection_effect,
        interaction_effect=interaction_effect,
        tracking_note="Benchmark return is based on available demo Market Data prices.",
    )


def assemble_secondary_effects(
    *,
    request: PnlAttributionRequest,
    positions: list[PositionPnlContribution],
    raw_positions: list[dict[str, Any]],
    transactions: list[dict[str, Any]],
    starting_value: float,
    ending_value: float,
    total_pnl: float,
    base_currency: str,
) -> dict[str, Any]:
    trade_effects = calculate_trade_effects(transactions, starting_value, request.include_trades)
    fixed_income_effects, rates_warnings = estimate_fixed_income_effects(
        positions,
        raw_positions,
        request.include_rates,
    )
    options_effects, options_warnings = estimate_options_effects(positions, request.include_options)
    fx_pnl, fx_effects, fx_warnings = estimate_fx_effects(positions, base_currency, request.include_fx)
    asset_class = aggregate_group_contributions(
        positions,
        "asset_class",
        starting_value,
        ending_value,
        total_pnl,
    )
    sector = aggregate_group_contributions(
        positions,
        "sector",
        starting_value,
        ending_value,
        total_pnl,
    )
    currency = aggregate_group_contributions(
        positions,
        "currency",
        starting_value,
        ending_value,
        total_pnl,
    )
    winners, losers = top_winners_losers(positions)
    return {
        "trade_effects": trade_effects,
        "fixed_income_effects": fixed_income_effects,
        "options_effects": options_effects,
        "fx_pnl": fx_pnl,
        "fx_effects": fx_effects,
        "asset_class_contributions": asset_class,
        "sector_contributions": sector,
        "currency_contributions": currency,
        "top_winners": winners,
        "top_losers": losers,
        "warnings": rates_warnings + options_warnings + fx_warnings + trade_effects.warnings,
    }


def portfolio_totals(
    positions: list[PositionPnlContribution],
    cash: float,
    fees_and_costs: float,
    fx_pnl: float,
) -> dict[str, float]:
    starting_value = sum(position.starting_value for position in positions) + cash
    raw_ending_value = sum(position.ending_value for position in positions) + cash
    income = sum(position.income_pnl for position in positions)
    price = sum(position.price_pnl for position in positions)
    ending_value = raw_ending_value + income - fees_and_costs + fx_pnl
    total_pnl = calculate_total_pnl(ending_value, starting_value)
    return {
        "starting_value": starting_value,
        "ending_value": ending_value,
        "total_pnl": total_pnl,
        "total_pnl_percent": calculate_total_pnl_percent(total_pnl, starting_value),
        "income_pnl": income,
        "price_pnl": price,
        "realized_pnl": sum(position.realized_pnl for position in positions),
        "unrealized_pnl": price - sum(position.realized_pnl for position in positions),
        "fees_and_costs": fees_and_costs,
    }


def _as_float(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
