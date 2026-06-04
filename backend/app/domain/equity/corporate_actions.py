from typing import Any


def summarize_dividend_profile(
    dividend_per_share: float | None,
    dividend_yield: float | None,
    payout_ratio: float | None,
) -> str:
    if not dividend_per_share or dividend_yield is None:
        return "No meaningful dividend profile in the demo data."
    payout_text = "payout not available"
    if payout_ratio is not None:
        payout_text = f"{payout_ratio:.1%} payout"
    return (
        f"Dividend per share is {dividend_per_share:.2f}, yield is "
        f"{dividend_yield:.2%}, with {payout_text}."
    )


def summarize_stock_split_placeholder(split_history: list[str] | None = None) -> str:
    if split_history:
        return "Recent demo split events: " + ", ".join(split_history)
    return "No stock split event is modeled in the current demo data."


def summarize_share_repurchases_placeholder(
    buyback_yield: float | None = None,
) -> str:
    if buyback_yield is None:
        return "Share repurchase data is a planned demo extension."
    return f"Estimated buyback yield is {buyback_yield:.2%}."


def calculate_buyback_yield(
    net_share_repurchases: float | None,
    market_cap: float | None,
) -> float | None:
    if net_share_repurchases is None or not market_cap:
        return None
    return net_share_repurchases / market_cap


def calculate_total_shareholder_yield(
    dividend_yield: float | None,
    buyback_yield: float | None,
) -> float | None:
    if dividend_yield is None and buyback_yield is None:
        return None
    return (dividend_yield or 0.0) + (buyback_yield or 0.0)


def summarize_corporate_actions_profile(
    *,
    dividend_profile: str,
    stock_split_summary: str,
    repurchase_summary: str,
    total_shareholder_yield: float | None,
) -> dict[str, Any]:
    return {
        "dividend_profile": dividend_profile,
        "stock_split_summary": stock_split_summary,
        "repurchase_summary": repurchase_summary,
        "total_shareholder_yield": total_shareholder_yield,
    }
