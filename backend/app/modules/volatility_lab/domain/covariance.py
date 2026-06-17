from app.modules.volatility_lab.domain.returns import arithmetic_mean


def covariance(first: list[float], second: list[float]) -> float:
    length = min(len(first), len(second))
    if length < 2:
        return 0.0
    left = first[-length:]
    right = second[-length:]
    left_mean = arithmetic_mean(left)
    right_mean = arithmetic_mean(right)
    return sum(
        (left[index] - left_mean) * (right[index] - right_mean)
        for index in range(length)
    ) / (length - 1)


def covariance_matrix(aligned_returns: dict[str, list[float]]) -> list[list[float]]:
    symbols = list(aligned_returns)
    return [
        [
            covariance(aligned_returns[left_symbol], aligned_returns[right_symbol])
            for right_symbol in symbols
        ]
        for left_symbol in symbols
    ]
