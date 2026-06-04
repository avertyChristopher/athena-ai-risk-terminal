from typing import Any


def classify_equity_security_type(
    security_type: str | None = None,
    *,
    has_voting_rights: bool | None = None,
    dividend_priority: str | None = None,
) -> str:
    normalized_type = (security_type or "").strip().lower()
    normalized_priority = (dividend_priority or "").strip().lower()

    if "preferred" in normalized_type or normalized_priority == "preferred":
        return "Preferred equity"
    if "adr" in normalized_type:
        return "Depositary receipt"
    if has_voting_rights is False:
        return "Non-voting common equity"
    return "Common equity"


def calculate_market_cap(price: float, shares_outstanding: float) -> float:
    _validate_positive(price, "price")
    _validate_positive(shares_outstanding, "shares_outstanding")
    return price * shares_outstanding


def calculate_free_float_market_cap(
    price: float,
    shares_outstanding: float,
    free_float_percent: float | None,
) -> float | None:
    if free_float_percent is None:
        return None
    if free_float_percent < 0 or free_float_percent > 1:
        raise ValueError("free_float_percent must be between 0 and 1.")
    return calculate_market_cap(price, shares_outstanding) * free_float_percent


def calculate_book_value_per_share(
    total_equity: float | None,
    shares_outstanding: float | None,
) -> float | None:
    if total_equity is None or shares_outstanding is None:
        return None
    _validate_positive(shares_outstanding, "shares_outstanding")
    return total_equity / shares_outstanding


def calculate_market_to_book_value(
    market_price: float,
    book_value_per_share: float | None,
) -> float | None:
    _validate_positive(market_price, "market_price")
    if not book_value_per_share or book_value_per_share <= 0:
        return None
    return market_price / book_value_per_share


def summarize_equity_security_profile(
    *,
    security_type: str,
    exchange: str,
    currency: str,
    voting_rights: str,
    dividend_profile: str,
    liquidity_note: str,
) -> dict[str, Any]:
    return {
        "security_type": security_type,
        "exchange": exchange,
        "currency": currency,
        "voting_rights": voting_rights,
        "dividend_profile": dividend_profile,
        "liquidity_note": liquidity_note,
    }


def _validate_positive(value: float, field_name: str) -> None:
    if value <= 0:
        raise ValueError(f"{field_name} must be positive.")
