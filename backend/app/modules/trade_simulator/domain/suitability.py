from typing import Any


def determine_suitability_status(
    warnings: list[dict[str, Any]],
    *,
    risk_increase: float,
    concentration_increase: float,
    cash_after: float,
) -> str:
    high_severity = any(warning["severity"] == "high" for warning in warnings)
    if cash_after < 0 or any(warning["name"] == "Sell quantity" for warning in warnings):
        return "Not Suitable"
    if high_severity or risk_increase > 0.02 or concentration_increase > 0.05:
        return "Requires Review"
    if warnings:
        return "Requires Review"

    return "Suitable"


def build_suitability_commentary(
    *,
    action: str,
    symbol: str,
    suitability_status: str,
    warnings: list[dict[str, Any]],
    expected_return_change: float,
    volatility_change: float,
    concentration_change: float,
) -> str:
    direction = "increases" if action == "BUY" else "reduces"
    risk_phrase = "risk increases" if volatility_change > 0 else "risk does not increase materially"
    return_phrase = (
        "expected return improves"
        if expected_return_change > 0
        else "expected return does not improve"
    )
    concentration_phrase = (
        "concentration rises"
        if concentration_change > 0
        else "concentration declines or remains stable"
    )

    if suitability_status == "Suitable":
        return (
            f"This {action.lower()} trade {direction} exposure to {symbol.upper()}. "
            f"{return_phrase.capitalize()}, {risk_phrase}, and {concentration_phrase}. "
            "No major IPS breach is flagged by the demo suitability engine."
        )

    warning_text = warnings[0]["message"] if warnings else "Policy review required."
    return (
        f"This {action.lower()} trade {direction} exposure to {symbol.upper()}. "
        f"{return_phrase.capitalize()}, {risk_phrase}, and {concentration_phrase}. "
        f"{warning_text} The trade should be reviewed before execution."
    )


def build_athena_commentary(
    *,
    action: str,
    symbol: str,
    expected_return_change: float,
    volatility_change: float,
    concentration_change: float,
    suitability_status: str,
    warnings: list[dict[str, Any]],
) -> str:
    return_direction = "improves" if expected_return_change > 0 else "does not improve"
    risk_direction = "increases" if volatility_change > 0 else "does not materially increase"
    concentration_direction = "increases" if concentration_change > 0 else "does not increase"
    breach_phrase = (
        "IPS constraints are breached or require review"
        if warnings
        else "no major IPS constraint breach is detected"
    )

    return (
        f"This proposed {action.lower()} in {symbol.upper()} {return_direction} "
        f"expected return, {risk_direction} risk, and {concentration_direction} "
        f"concentration. Based on the deterministic demo checks, {breach_phrase}. "
        f"Suitability result: {suitability_status}."
    )
