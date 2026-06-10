from collections.abc import Sequence
from math import sqrt


def calculate_weighted_expected_return(
    expected_returns: Sequence[float],
    weights: Sequence[float],
) -> float:
    _validate_same_length(expected_returns, weights)
    return sum(expected_return * weight for expected_return, weight in zip(expected_returns, weights))


def calculate_portfolio_variance_two_asset(
    weight_a: float,
    weight_b: float,
    variance_a: float,
    variance_b: float,
    covariance_ab: float,
) -> float:
    return (
        (weight_a**2) * variance_a
        + (weight_b**2) * variance_b
        + 2 * weight_a * weight_b * covariance_ab
    )


def calculate_portfolio_variance_from_covariance_matrix(
    weights: Sequence[float],
    covariance_matrix: Sequence[Sequence[float]],
) -> float:
    if len(weights) != len(covariance_matrix):
        raise ValueError("Weights and covariance matrix must have matching dimensions.")

    variance = 0.0
    for row_index, weight_i in enumerate(weights):
        if len(covariance_matrix[row_index]) != len(weights):
            raise ValueError("Covariance matrix must be square.")
        for column_index, weight_j in enumerate(weights):
            variance += weight_i * weight_j * covariance_matrix[row_index][column_index]

    return variance


def calculate_portfolio_standard_deviation(variance: float) -> float:
    if variance < 0:
        raise ValueError("Variance cannot be negative.")

    return sqrt(variance)


def calculate_diversification_benefit(
    weighted_average_volatility: float,
    portfolio_volatility: float,
) -> float:
    if weighted_average_volatility <= 0:
        return 0.0

    return max(0.0, weighted_average_volatility - portfolio_volatility)


def calculate_asset_contribution_to_return(weight: float, expected_return: float) -> float:
    return weight * expected_return


def calculate_asset_contribution_to_risk_placeholder(weight: float) -> float:
    return weight


def _validate_same_length(first: Sequence[float], second: Sequence[float]) -> None:
    if len(first) != len(second):
        raise ValueError("Inputs must have the same length.")
