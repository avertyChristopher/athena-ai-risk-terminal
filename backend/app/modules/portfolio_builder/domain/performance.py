from collections.abc import Sequence


def calculate_holding_period_return(
    beginning_value: float,
    ending_value: float,
    external_cash_flows: float = 0.0,
) -> float:
    if beginning_value <= 0:
        raise ValueError("Beginning value must be positive.")

    return (ending_value - beginning_value - external_cash_flows) / beginning_value


def calculate_subperiod_return(beginning_value: float, ending_value: float) -> float:
    return calculate_holding_period_return(beginning_value, ending_value)


def calculate_time_weighted_return(subperiod_returns: Sequence[float]) -> float:
    compounded = 1.0
    for subperiod_return in subperiod_returns:
        compounded *= 1.0 + subperiod_return

    return compounded - 1.0


def calculate_money_weighted_return_placeholder() -> None:
    return None


def calculate_return_contribution(weight: float, asset_return: float) -> float:
    return weight * asset_return


def calculate_cash_flow_adjusted_return_placeholder() -> None:
    return None
