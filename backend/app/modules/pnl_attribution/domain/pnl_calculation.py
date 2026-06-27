from __future__ import annotations


def calculate_total_pnl(ending_value: float, starting_value: float) -> float:
    return ending_value - starting_value


def calculate_total_pnl_percent(total_pnl: float, starting_value: float) -> float:
    if starting_value == 0:
        return 0.0
    return total_pnl / starting_value


def calculate_position_price_pnl(
    starting_price: float,
    ending_price: float,
    quantity: float,
) -> float:
    return (ending_price - starting_price) * quantity


def calculate_position_pnl_percent(total_pnl: float, starting_value: float) -> float:
    if starting_value == 0:
        return 0.0
    return total_pnl / starting_value


def calculate_contribution_to_portfolio_return(
    position_pnl: float,
    portfolio_starting_value: float,
) -> float:
    if portfolio_starting_value == 0:
        return 0.0
    return position_pnl / portfolio_starting_value


def calculate_contribution_to_total_pnl(position_pnl: float, total_pnl: float) -> float:
    if total_pnl == 0:
        return 0.0
    return position_pnl / total_pnl
