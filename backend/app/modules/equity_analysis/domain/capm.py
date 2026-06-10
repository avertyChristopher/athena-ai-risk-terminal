def calculate_market_risk_premium(
    expected_market_return: float | None,
    risk_free_rate: float | None,
) -> float | None:
    if expected_market_return is None or risk_free_rate is None:
        return None
    return expected_market_return - risk_free_rate


def calculate_equity_risk_premium(
    expected_equity_return: float | None,
    risk_free_rate: float | None,
) -> float | None:
    if expected_equity_return is None or risk_free_rate is None:
        return None
    return expected_equity_return - risk_free_rate


def calculate_capm_required_return(
    risk_free_rate: float | None,
    beta: float | None,
    market_risk_premium: float | None,
) -> float | None:
    if risk_free_rate is None or beta is None or market_risk_premium is None:
        return None
    return risk_free_rate + beta * market_risk_premium


def compare_expected_return_to_required_return(
    expected_return: float | None,
    required_return: float | None,
) -> float | None:
    if expected_return is None or required_return is None:
        return None
    return expected_return - required_return


def classify_required_return_signal(
    expected_return_vs_required_return: float | None,
) -> str:
    if expected_return_vs_required_return is None:
        return "Insufficient CAPM inputs"
    if expected_return_vs_required_return > 0.02:
        return "Expected return exceeds required return"
    if expected_return_vs_required_return < -0.02:
        return "Expected return below required return"
    return "Expected return near required return"


def create_capm_warnings(
    beta: float | None,
    risk_free_rate: float | None,
    market_risk_premium: float | None,
) -> list[str]:
    warnings = []
    if beta is None:
        warnings.append("Beta is missing; CAPM required return cannot be calculated.")
    elif beta < 0:
        warnings.append("Beta is negative; interpret CAPM output carefully.")
    if risk_free_rate is None:
        warnings.append("Risk-free rate is missing; CAPM uses fallback inputs.")
    if market_risk_premium is None:
        warnings.append("Market risk premium is missing.")
    return warnings
