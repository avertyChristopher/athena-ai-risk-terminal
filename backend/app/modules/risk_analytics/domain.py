from collections.abc import Mapping, Sequence
from math import sqrt
from statistics import mean

TRADING_DAYS_PER_YEAR = 252


def align_return_series_by_symbol(
    rows: Sequence[Mapping[str, float | str]],
    symbols: Sequence[str],
) -> tuple[list[str], dict[str, list[float]]]:
    normalized_symbols = [symbol.upper() for symbol in symbols]
    dates: list[str] = []
    returns_by_symbol = {symbol: [] for symbol in normalized_symbols}

    for row in rows:
        if not all(symbol in row for symbol in normalized_symbols):
            continue
        dates.append(str(row["date"]))
        for symbol in normalized_symbols:
            returns_by_symbol[symbol].append(float(row[symbol]))

    return dates, returns_by_symbol


def calculate_weighted_portfolio_returns(
    returns_by_symbol: Mapping[str, Sequence[float]],
    weights_by_symbol: Mapping[str, float],
) -> list[float]:
    symbols = [
        symbol
        for symbol in weights_by_symbol
        if symbol in returns_by_symbol and returns_by_symbol[symbol]
    ]
    if not symbols:
        return []

    aligned_length = min(len(returns_by_symbol[symbol]) for symbol in symbols)
    if aligned_length == 0:
        return []

    return [
        sum(
            float(weights_by_symbol[symbol])
            * float(returns_by_symbol[symbol][-aligned_length + index])
            for symbol in symbols
        )
        for index in range(aligned_length)
    ]


def calculate_annualized_volatility(
    returns: Sequence[float],
    trading_days: int = TRADING_DAYS_PER_YEAR,
) -> float:
    return calculate_standard_deviation(returns) * sqrt(trading_days)


def calculate_covariance_matrix(
    returns_by_symbol: Mapping[str, Sequence[float]],
    symbols: Sequence[str],
    trading_days: int = TRADING_DAYS_PER_YEAR,
) -> list[list[float]]:
    matrix: list[list[float]] = []
    for row_symbol in symbols:
        row = []
        for column_symbol in symbols:
            row.append(
                calculate_covariance(
                    returns_by_symbol[row_symbol],
                    returns_by_symbol[column_symbol],
                )
                * trading_days,
            )
        matrix.append(row)
    return matrix


def calculate_portfolio_variance_from_covariance(
    weights: Sequence[float],
    covariance_matrix: Sequence[Sequence[float]],
) -> float:
    variance = 0.0
    for row_index, row_weight in enumerate(weights):
        for column_index, column_weight in enumerate(weights):
            variance += (
                row_weight
                * column_weight
                * float(covariance_matrix[row_index][column_index])
            )
    return variance


def calculate_historical_var(
    returns: Sequence[float],
    confidence_level: float = 0.95,
) -> float:
    _validate_returns(returns)
    percentile = _percentile(returns, (1.0 - confidence_level) * 100)
    return max(0.0, -percentile)


def calculate_historical_cvar(
    returns: Sequence[float],
    confidence_level: float = 0.95,
) -> float:
    _validate_returns(returns)
    percentile = _percentile(returns, (1.0 - confidence_level) * 100)
    tail_losses = [period_return for period_return in returns if period_return <= percentile]
    if not tail_losses:
        return calculate_historical_var(returns, confidence_level)
    return max(0.0, -mean(tail_losses))


def calculate_tracking_error(
    portfolio_returns: Sequence[float],
    benchmark_returns: Sequence[float],
    trading_days: int = TRADING_DAYS_PER_YEAR,
) -> float:
    portfolio, benchmark = _align_sequences(portfolio_returns, benchmark_returns)
    active_returns = [
        portfolio_return - benchmark_return
        for portfolio_return, benchmark_return in zip(portfolio, benchmark)
    ]
    return calculate_standard_deviation(active_returns) * sqrt(trading_days)


def calculate_sharpe_ratio(
    returns: Sequence[float],
    annual_risk_free_rate: float = 0.02,
    trading_days: int = TRADING_DAYS_PER_YEAR,
) -> float:
    annualized_volatility = calculate_annualized_volatility(returns, trading_days)
    if annualized_volatility == 0:
        return 0.0
    return (
        calculate_annualized_return(returns, trading_days) - annual_risk_free_rate
    ) / annualized_volatility


def calculate_annualized_return(
    returns: Sequence[float],
    trading_days: int = TRADING_DAYS_PER_YEAR,
) -> float:
    _validate_returns(returns)
    compounded_growth = 1.0
    for period_return in returns:
        compounded_growth *= 1.0 + period_return
    return compounded_growth ** (trading_days / len(returns)) - 1.0


def calculate_max_drawdown_from_returns(returns: Sequence[float]) -> float:
    _validate_returns(returns)
    cumulative_value = 1.0
    running_peak = 1.0
    max_drawdown = 0.0
    for period_return in returns:
        cumulative_value *= 1.0 + period_return
        running_peak = max(running_peak, cumulative_value)
        max_drawdown = min(max_drawdown, (cumulative_value / running_peak) - 1.0)
    return max_drawdown


def calculate_standard_deviation(returns: Sequence[float]) -> float:
    _validate_returns(returns, minimum_length=2)
    average = mean(returns)
    variance = sum((period_return - average) ** 2 for period_return in returns) / (
        len(returns) - 1
    )
    return sqrt(variance)


def calculate_covariance(
    first_returns: Sequence[float],
    second_returns: Sequence[float],
) -> float:
    first, second = _align_sequences(first_returns, second_returns)
    first_average = mean(first)
    second_average = mean(second)
    return sum(
        (first_return - first_average) * (second_return - second_average)
        for first_return, second_return in zip(first, second)
    ) / (len(first) - 1)


def _align_sequences(
    first_returns: Sequence[float],
    second_returns: Sequence[float],
) -> tuple[list[float], list[float]]:
    length = min(len(first_returns), len(second_returns))
    if length < 2:
        raise ValueError("At least two aligned returns are required.")
    return list(first_returns[-length:]), list(second_returns[-length:])


def _percentile(values: Sequence[float], percentile: float) -> float:
    sorted_values = sorted(values)
    rank = (percentile / 100.0) * (len(sorted_values) - 1)
    lower_index = int(rank)
    upper_index = min(lower_index + 1, len(sorted_values) - 1)
    weight = rank - lower_index
    return sorted_values[lower_index] * (1.0 - weight) + sorted_values[upper_index] * weight


def _validate_returns(
    returns: Sequence[float],
    minimum_length: int = 1,
) -> None:
    if len(returns) < minimum_length:
        raise ValueError(f"At least {minimum_length} returns are required.")
