from collections.abc import Mapping, Sequence


def detect_home_bias_placeholder(
    positions: Sequence[Mapping[str, object]],
    home_country: str,
) -> str:
    if not positions:
        return "No holdings available for home-bias review."

    home_weight = sum(
        float(position.get("invested_weight", 0.0))
        for position in positions
        if str(position.get("country", "")).lower() == home_country.lower()
    )
    if home_weight >= 0.75:
        return "Potential home bias: domestic exposure dominates the portfolio."
    return "No home-bias warning from the demo country exposure check."


def detect_concentration_overconfidence_warning(
    largest_position_weight: float,
) -> str | None:
    if largest_position_weight >= 0.30:
        return "Large single-position weight may indicate overconfidence or insufficient diversification."
    return None


def detect_loss_aversion_placeholder(unrealized_pnl_percent: float) -> str | None:
    if unrealized_pnl_percent < -0.15:
        return "Material unrealized loss: review whether loss aversion is delaying a decision."
    return None


def create_behavioral_bias_summary(warnings: Sequence[str | None]) -> str:
    active_warnings = [warning for warning in warnings if warning]
    if not active_warnings:
        return "No behavioral-bias warning was triggered by the demo heuristics."
    return " ".join(active_warnings)
