from collections.abc import Mapping, Sequence


def create_default_policy(benchmark: str) -> dict[str, object]:
    return {
        "investor_type": "Individual",
        "investment_objective": "Long-term capital growth with controlled diversification.",
        "return_objective": "Seek balanced demo portfolio growth versus benchmark.",
        "risk_objective": "Accept moderate volatility while avoiding uncompensated concentration risk.",
        "risk_tolerance": "Moderate",
        "ability_to_take_risk": "Moderate",
        "willingness_to_take_risk": "Moderate",
        "risk_aversion_coefficient": 3.0,
        "time_horizon": "Long term",
        "liability_profile": "No explicit liability schedule modeled.",
        "liquidity_needs": "Maintain a small cash reserve.",
        "tax_considerations": "Placeholder: tax constraints are not modeled.",
        "legal_regulatory_constraints": "Placeholder: legal constraints are not modeled.",
        "unique_circumstances": "Educational demo portfolio.",
        "permitted_asset_classes": ["equity", "etf", "fixed_income", "cash"],
        "prohibited_asset_classes": [],
        "benchmark": benchmark,
        "target_allocation": [
            {"name": "equity", "target_weight": 0.70, "tolerance_band": 0.10},
            {"name": "etf", "target_weight": 0.20, "tolerance_band": 0.10},
            {"name": "cash", "target_weight": 0.10, "tolerance_band": 0.05},
        ],
    }


def validate_policy_constraints(policy: Mapping[str, object]) -> list[str]:
    warnings: list[str] = []
    target_allocation = policy.get("target_allocation", [])
    if isinstance(target_allocation, list):
        total_weight = sum(float(item.get("target_weight", 0.0)) for item in target_allocation)
        if abs(total_weight - 1.0) > 0.01:
            warnings.append("Target allocation weights should sum to 100%.")
    return warnings


def compare_allocation_to_policy(
    current_allocation: Mapping[str, float],
    target_allocation: Sequence[Mapping[str, object]],
) -> list[dict[str, float | str]]:
    rows: list[dict[str, float | str]] = []
    for target in target_allocation:
        name = str(target["name"])
        target_weight = float(target["target_weight"])
        current_weight = current_allocation.get(name, 0.0)
        tolerance_band = float(target.get("tolerance_band", 0.0))
        drift = current_weight - target_weight
        status = "Within tolerance"
        if drift > tolerance_band:
            status = "Overweight"
        elif drift < -tolerance_band:
            status = "Underweight"
        rows.append(
            {
                "name": name,
                "current_weight": current_weight,
                "target_weight": target_weight,
                "drift": drift,
                "tolerance_band": tolerance_band,
                "status": status,
            }
        )
    return rows


def identify_policy_breaches(policy_comparison: Sequence[Mapping[str, object]]) -> list[str]:
    return [
        f"{item['name']} is {str(item['status']).lower()}."
        for item in policy_comparison
        if item.get("status") != "Within tolerance"
    ]


def classify_allocation_quality(number_of_asset_classes: int, breaches: Sequence[object]) -> str:
    if breaches:
        return "Needs review"
    if number_of_asset_classes >= 3:
        return "Broadly diversified"
    return "Narrow allocation"


def classify_diversification_quality(effective_number_of_holdings: float) -> str:
    if effective_number_of_holdings >= 6:
        return "Strong diversification"
    if effective_number_of_holdings >= 3:
        return "Moderate diversification"
    return "Concentrated"


def classify_cash_level(cash_weight: float) -> str:
    if cash_weight < 0.02:
        return "Low cash"
    if cash_weight > 0.20:
        return "High cash"
    return "Balanced cash"


def classify_benchmark_alignment(total_active_weight: float) -> str:
    if total_active_weight >= 0.50:
        return "Highly active"
    if total_active_weight >= 0.20:
        return "Moderately active"
    return "Benchmark-aware"


def create_portfolio_diagnostics_summary(
    *,
    allocation_quality: str,
    diversification_quality: str,
    concentration_level: str,
    cash_level: str,
    benchmark_alignment: str,
    policy_breaches: Sequence[str],
) -> str:
    breach_note = "No policy breaches flagged." if not policy_breaches else "Policy review required."
    return (
        f"{allocation_quality}; {diversification_quality}; {concentration_level}; "
        f"{cash_level}; {benchmark_alignment}. {breach_note}"
    )
