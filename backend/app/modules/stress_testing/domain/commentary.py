from __future__ import annotations


def generate_stress_commentary(
    scenario_name: str,
    severity: str,
    percent_loss: float,
    worst_contributor: str | None,
    fixed_income_offset: bool,
    limit_breaches: int,
) -> dict[str, object]:
    contributor_text = worst_contributor or "the largest portfolio exposures"
    summary = (
        f"The {scenario_name} scenario produces a {severity.lower()} estimated loss "
        f"of {percent_loss:.1%}, mainly driven by {contributor_text}."
    )
    key_points = [
        f"Stress severity is classified as {severity}.",
        f"Estimated portfolio loss is {percent_loss:.1%}.",
    ]
    if fixed_income_offset:
        key_points.append("Fixed-income exposure partially offsets the equity drawdown.")
    if limit_breaches:
        key_points.append(f"{limit_breaches} stress limits require review.")

    suggested_actions = [
        "Review sector and single-name concentration.",
        "Compare stress loss against the portfolio risk policy.",
        "Consider downside protection or rebalancing if the scenario is plausible.",
    ]
    return {
        "summary": summary,
        "key_points": key_points,
        "suggested_actions": suggested_actions,
        "not_investment_advice": True,
    }
