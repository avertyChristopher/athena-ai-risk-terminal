def calculate_position_market_value(quantity: float, current_price: float) -> float:
    if quantity < 0:
        raise ValueError("Position quantity cannot be negative.")

    if current_price < 0:
        raise ValueError("Position price cannot be negative.")

    return quantity * current_price
