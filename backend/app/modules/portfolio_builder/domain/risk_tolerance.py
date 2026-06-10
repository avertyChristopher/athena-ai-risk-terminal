def classify_overall_risk_tolerance(
    ability_to_take_risk: str,
    willingness_to_take_risk: str,
) -> str:
    ability_score = _risk_score(ability_to_take_risk)
    willingness_score = _risk_score(willingness_to_take_risk)
    if ability_score is None or willingness_score is None:
        return "Requires review"

    score = min(ability_score, willingness_score)
    if score >= 3:
        return "High"
    if score == 2:
        return "Moderate"
    return "Low"


def detect_ability_willingness_conflict(
    ability_to_take_risk: str,
    willingness_to_take_risk: str,
) -> bool:
    ability_score = _risk_score(ability_to_take_risk)
    willingness_score = _risk_score(willingness_to_take_risk)
    if ability_score is None or willingness_score is None:
        return True
    return abs(ability_score - willingness_score) >= 2


def create_risk_tolerance_summary(
    ability_to_take_risk: str,
    willingness_to_take_risk: str,
) -> str:
    overall = classify_overall_risk_tolerance(
        ability_to_take_risk,
        willingness_to_take_risk,
    )
    if detect_ability_willingness_conflict(
        ability_to_take_risk,
        willingness_to_take_risk,
    ):
        return (
            "Ability and willingness conflict detected; CFA IPS guidance uses the "
            "more conservative constraint until reviewed."
        )
    return f"Overall risk tolerance is {overall.lower()} based on ability and willingness."


def _risk_score(value: str) -> int | None:
    normalized = value.strip().lower()
    if normalized in {"low", "conservative", "defensive"}:
        return 1
    if normalized in {"moderate", "balanced"}:
        return 2
    if normalized in {"high", "aggressive", "growth"}:
        return 3
    return None
