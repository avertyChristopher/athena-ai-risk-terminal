def calculate_position_market_value(quantity: float, current_price: float) -> float:
    validate_position_input(
        symbol="POSITION",
        asset_type="asset",
        currency="USD",
        quantity=quantity,
        current_price=current_price,
    )

    return quantity * current_price


def calculate_position_cost_basis(quantity: float, average_price: float) -> float:
    if quantity <= 0:
        raise ValueError("Position quantity must be positive.")

    if average_price <= 0:
        raise ValueError("Average price must be positive.")

    return quantity * average_price


def calculate_position_unrealized_pnl(
    quantity: float,
    average_price: float,
    current_price: float,
) -> float:
    return calculate_position_market_value(
        quantity,
        current_price,
    ) - calculate_position_cost_basis(quantity, average_price)


def calculate_position_unrealized_pnl_percent(
    quantity: float,
    average_price: float,
    current_price: float,
) -> float:
    cost_basis = calculate_position_cost_basis(quantity, average_price)
    return calculate_position_unrealized_pnl(
        quantity,
        average_price,
        current_price,
    ) / cost_basis


def calculate_portfolio_weight(market_value: float, total_market_value: float) -> float:
    if market_value < 0:
        raise ValueError("Market value cannot be negative.")

    if total_market_value <= 0:
        return 0.0

    return market_value / total_market_value


def calculate_invested_weight(market_value: float, invested_value: float) -> float:
    if market_value < 0:
        raise ValueError("Market value cannot be negative.")

    if invested_value <= 0:
        return 0.0

    return market_value / invested_value


def validate_position_input(
    *,
    symbol: str,
    asset_type: str,
    currency: str,
    quantity: float,
    current_price: float,
    average_price: float | None = None,
) -> None:
    if not symbol.strip():
        raise ValueError("Position symbol is required.")

    if not asset_type.strip():
        raise ValueError("Asset type is required.")

    if not currency.strip():
        raise ValueError("Currency is required.")

    if quantity <= 0:
        raise ValueError("Position quantity must be positive.")

    if current_price <= 0:
        raise ValueError("Current price must be positive.")

    if average_price is not None and average_price <= 0:
        raise ValueError("Average price must be positive.")
