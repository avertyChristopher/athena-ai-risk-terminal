from math import inf


def single_option_risk_summary(
    option_type: str,
    side: str,
    strike_price: float,
    premium: float,
    contract_size: int,
    quantity: int,
) -> dict[str, float | str | None]:
    multiplier = contract_size * quantity
    if option_type == "call" and side == "long":
        return {
            "max_profit": None,
            "max_profit_label": "Unlimited",
            "max_loss": premium * multiplier,
            "risk_note": "Long call can expire worthless but has leveraged upside.",
        }
    if option_type == "call" and side == "short":
        return {
            "max_profit": premium * multiplier,
            "max_profit_label": f"{premium * multiplier:.2f}",
            "max_loss": None,
            "risk_note": "Short call has theoretically unlimited loss.",
        }
    if option_type == "put" and side == "long":
        return {
            "max_profit": max(strike_price - premium, 0.0) * multiplier,
            "max_profit_label": f"{max(strike_price - premium, 0.0) * multiplier:.2f}",
            "max_loss": premium * multiplier,
            "risk_note": "Long put benefits from downside moves and can expire worthless.",
        }
    return {
        "max_profit": premium * multiplier,
        "max_profit_label": f"{premium * multiplier:.2f}",
        "max_loss": max(strike_price - premium, 0.0) * multiplier,
        "risk_note": "Short put has large downside obligation if the underlying falls.",
    }


def finite_or_none(value: float) -> float | None:
    if value in {inf, -inf}:
        return None
    return value
