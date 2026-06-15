def simulate_execution_price(
    *,
    action: str,
    estimated_price: float,
    order_type: str,
) -> float:
    adjustment = {
        "Market": 0.0008,
        "Limit": 0.0002,
        "Stop": 0.0012,
    }.get(order_type, 0.0008)

    if action == "BUY":
        return estimated_price * (1.0 + adjustment)

    return estimated_price * (1.0 - adjustment)


def calculate_price_shortfall(
    *,
    action: str,
    expected_price: float,
    simulated_price: float,
) -> float:
    if action == "BUY":
        return simulated_price - expected_price

    return expected_price - simulated_price


def describe_order_type_impact(order_type: str) -> str:
    return {
        "Market": "Market orders prioritize execution certainty and may increase slippage.",
        "Limit": "Limit orders control price but may reduce execution certainty.",
        "Stop": "Stop orders can protect downside but may execute through the stop level in fast markets.",
    }.get(order_type, "Order type impact is modeled with deterministic demo assumptions.")


def detect_liquidity_warning(
    *,
    gross_trade_value: float,
    portfolio_value: float,
) -> str | None:
    if portfolio_value <= 0:
        return "Portfolio value is unavailable for liquidity sizing."

    if gross_trade_value / portfolio_value >= 0.15:
        return "Trade size is large relative to portfolio value; liquidity review recommended."

    return None
