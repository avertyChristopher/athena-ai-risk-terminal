def build_risk_alerts(
    breaches: list[dict[str, object]],
    stress_tests: list[dict[str, object]],
) -> list[dict[str, object]]:
    alerts: list[dict[str, object]] = []
    for breach in breaches:
        if str(breach["severity"]) in {"high", "critical"}:
            alerts.append(
                {
                    "title": str(breach["rule_name"]),
                    "severity": str(breach["severity"]),
                    "message": str(breach["explanation"]),
                    "suggested_action": str(breach["suggested_action"]),
                },
            )

    for scenario in stress_tests:
        if str(scenario["severity"]) in {"high", "critical"}:
            alerts.append(
                {
                    "title": str(scenario["name"]),
                    "severity": str(scenario["severity"]),
                    "message": (
                        f"Estimated stress impact is "
                        f"{float(scenario['estimated_impact_percent']):.1%}."
                    ),
                    "suggested_action": "Review stress vulnerability and hedge or rebalance exposed holdings.",
                },
            )

    if not alerts:
        alerts.append(
            {
                "title": "No high-severity risk alert",
                "severity": "low",
                "message": "Current surveillance checks do not flag a high-severity breach.",
                "suggested_action": "Continue monitoring realized risk and concentration.",
            },
        )
    return alerts[:8]
