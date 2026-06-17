from statistics import median

from app.modules.volatility_lab.domain.returns import arithmetic_mean
from app.modules.volatility_lab.domain.volatility import standard_deviation


def percentile(values: list[float], percentile_value: float) -> float:
    if not values:
        return 0.0
    sorted_values = sorted(values)
    index = (len(sorted_values) - 1) * percentile_value
    lower = int(index)
    upper = min(lower + 1, len(sorted_values) - 1)
    weight = index - lower
    return sorted_values[lower] * (1.0 - weight) + sorted_values[upper] * weight


def skewness(values: list[float]) -> float:
    if len(values) < 3:
        return 0.0
    mean_value = arithmetic_mean(values)
    deviation = standard_deviation(values)
    if deviation == 0:
        return 0.0
    return sum(((value - mean_value) / deviation) ** 3 for value in values) / len(values)


def kurtosis(values: list[float]) -> float:
    if len(values) < 4:
        return 0.0
    mean_value = arithmetic_mean(values)
    deviation = standard_deviation(values)
    if deviation == 0:
        return 0.0
    return sum(((value - mean_value) / deviation) ** 4 for value in values) / len(values) - 3.0


def histogram(values: list[float], bins: int = 8) -> list[dict[str, float | int]]:
    if not values or bins <= 0:
        return []
    minimum = min(values)
    maximum = max(values)
    if minimum == maximum:
        return [{"lower": minimum, "upper": maximum, "count": len(values)}]
    width = (maximum - minimum) / bins
    counts = [0 for _ in range(bins)]
    for value in values:
        index = min(int((value - minimum) / width), bins - 1)
        counts[index] += 1
    return [
        {
            "lower": minimum + width * index,
            "upper": minimum + width * (index + 1),
            "count": counts[index],
        }
        for index in range(bins)
    ]


def distribution_summary(values: list[float]) -> dict[str, object]:
    if not values:
        return {
            "mean": 0.0,
            "median": 0.0,
            "minimum": 0.0,
            "maximum": 0.0,
            "skewness": 0.0,
            "kurtosis": 0.0,
            "percentiles": {},
            "histogram": [],
        }
    return {
        "mean": arithmetic_mean(values),
        "median": median(values),
        "minimum": min(values),
        "maximum": max(values),
        "skewness": skewness(values),
        "kurtosis": kurtosis(values),
        "percentiles": {
            "p5": percentile(values, 0.05),
            "p25": percentile(values, 0.25),
            "p50": percentile(values, 0.50),
            "p75": percentile(values, 0.75),
            "p95": percentile(values, 0.95),
        },
        "histogram": histogram(values),
    }
