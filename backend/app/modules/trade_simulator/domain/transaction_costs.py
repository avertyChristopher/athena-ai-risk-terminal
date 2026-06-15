def calculate_gross_trade_value(quantity: float, price: float) -> float:
    if quantity <= 0:
        raise ValueError("Trade quantity must be positive.")
    if price <= 0:
        raise ValueError("Trade price must be positive.")

    return quantity * price


def estimate_commission(gross_trade_value: float) -> float:
    return max(1.0, gross_trade_value * 0.0005)


def estimate_fees(gross_trade_value: float) -> float:
    return gross_trade_value * 0.0001


def estimate_spread_cost(
    gross_trade_value: float,
    asset_type: str,
) -> float:
    spread_bps = {
        "equity": 0.0004,
        "etf": 0.00025,
        "fixed_income": 0.0007,
        "bond": 0.0007,
    }.get(asset_type.lower(), 0.0005)
    return gross_trade_value * spread_bps


def estimate_slippage(
    gross_trade_value: float,
    order_type: str,
) -> float:
    slippage_bps = {
        "Market": 0.0008,
        "Limit": 0.0003,
        "Stop": 0.0010,
    }.get(order_type, 0.0007)
    return gross_trade_value * slippage_bps


def estimate_market_impact(
    gross_trade_value: float,
    portfolio_value: float,
) -> float:
    if portfolio_value <= 0:
        return gross_trade_value * 0.001

    participation_proxy = min(gross_trade_value / portfolio_value, 1.0)
    return gross_trade_value * min(0.0025, participation_proxy * 0.0015)


def calculate_total_implementation_cost(
    commission: float,
    fees: float,
    spread_cost: float,
    slippage: float,
    market_impact: float,
) -> float:
    return commission + fees + spread_cost + slippage + market_impact


def calculate_cost_percent(
    total_cost: float,
    gross_trade_value: float,
) -> float:
    if gross_trade_value <= 0:
        return 0.0

    return total_cost / gross_trade_value
