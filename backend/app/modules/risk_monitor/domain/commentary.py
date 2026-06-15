def build_athena_risk_commentary(
    *,
    status: str,
    main_drivers: list[str],
    breaches: list[dict[str, object]],
    stress_tests: list[dict[str, object]],
    benchmark_warnings: list[str],
) -> dict[str, object]:
    high_breaches = [
        breach
        for breach in breaches
        if str(breach["severity"]) in {"high", "critical"}
    ]
    worst_stress = min(
        stress_tests,
        key=lambda scenario: float(scenario["estimated_impact_percent"]),
        default=None,
    )
    breach_text = (
        f"{len(high_breaches)} high-severity limit breach(es)"
        if high_breaches
        else "no high-severity limit breach"
    )
    stress_text = (
        f"the most severe stress scenario is {worst_stress['name']} "
        f"with {float(worst_stress['estimated_impact_percent']):.1%} estimated impact"
        if worst_stress
        else "stress testing did not identify a material vulnerability"
    )
    summary = (
        f"The portfolio is classified as {status}. Athena Risk Monitor flags "
        f"{breach_text}; {stress_text}. "
        "The result should be reviewed with concentration, active risk and liquidity constraints."
    )
    suggested_actions = [
        str(breach["suggested_action"]) for breach in high_breaches[:3]
    ]
    if benchmark_warnings:
        suggested_actions.append("Add benchmark constituent data to refine active-risk monitoring.")
    if worst_stress and float(worst_stress["estimated_impact_percent"]) <= -0.05:
        suggested_actions.append("Review stress scenario hedges or diversify the most exposed holdings.")
    if not suggested_actions:
        suggested_actions.append("Maintain monitoring and refresh realized return history regularly.")

    return {
        "summary": summary,
        "main_drivers": main_drivers[:5],
        "suggested_actions": suggested_actions,
    }
