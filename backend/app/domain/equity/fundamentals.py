def calculate_book_value_per_share(total_equity: float, shares_outstanding: float) -> float:
    _validate_positive(shares_outstanding, "shares_outstanding")
    return total_equity / shares_outstanding


def calculate_market_cap(price: float, shares_outstanding: float) -> float:
    _validate_positive(price, "price")
    _validate_positive(shares_outstanding, "shares_outstanding")
    return price * shares_outstanding


def calculate_enterprise_value(
    market_cap: float,
    total_debt: float,
    cash_and_equivalents: float,
) -> float:
    _validate_positive(market_cap, "market_cap")
    return market_cap + total_debt - cash_and_equivalents


def _validate_positive(value: float, field_name: str) -> None:
    if value <= 0:
        raise ValueError(f"{field_name} must be positive.")
