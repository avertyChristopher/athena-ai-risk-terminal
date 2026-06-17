from app.modules.volatility_lab.domain.covariance import covariance
from app.modules.volatility_lab.domain.volatility import standard_deviation


def correlation(first: list[float], second: list[float]) -> float:
    length = min(len(first), len(second))
    if length < 2:
        return 0.0
    left = first[-length:]
    right = second[-length:]
    denominator = standard_deviation(left) * standard_deviation(right)
    if denominator == 0:
        return 0.0
    return covariance(left, right) / denominator


def correlation_matrix(aligned_returns: dict[str, list[float]]) -> list[list[float]]:
    symbols = list(aligned_returns)
    return [
        [
            correlation(aligned_returns[left_symbol], aligned_returns[right_symbol])
            for right_symbol in symbols
        ]
        for left_symbol in symbols
    ]
