from collections.abc import Sequence


def calculate_fcff(
    ebit: float,
    tax_rate: float,
    depreciation: float,
    capital_expenditures: float,
    change_in_working_capital: float,
) -> float:
    return ebit * (1.0 - tax_rate) + depreciation - capital_expenditures - change_in_working_capital


def calculate_fcfe(
    net_income: float,
    depreciation: float,
    capital_expenditures: float,
    change_in_working_capital: float,
    net_borrowing: float,
) -> float:
    return net_income + depreciation - capital_expenditures - change_in_working_capital + net_borrowing


def discount_cash_flows(cash_flows: Sequence[float], discount_rate: float) -> list[float]:
    if discount_rate <= -1:
        raise ValueError("Discount rate must be greater than -100%.")
    return [
        cash_flow / ((1.0 + discount_rate) ** period)
        for period, cash_flow in enumerate(cash_flows, start=1)
    ]


def calculate_terminal_value_gordon(
    final_cash_flow: float,
    discount_rate: float,
    terminal_growth_rate: float,
) -> float:
    if discount_rate <= terminal_growth_rate:
        raise ValueError("Discount rate must be greater than terminal growth rate.")
    return final_cash_flow * (1.0 + terminal_growth_rate) / (discount_rate - terminal_growth_rate)


def calculate_enterprise_value_from_fcff(
    projected_fcff: Sequence[float],
    wacc: float,
    terminal_growth_rate: float,
) -> float:
    terminal_value = calculate_terminal_value_gordon(projected_fcff[-1], wacc, terminal_growth_rate)
    present_values = discount_cash_flows(projected_fcff, wacc)
    terminal_present_value = terminal_value / ((1.0 + wacc) ** len(projected_fcff))
    return sum(present_values) + terminal_present_value


def calculate_equity_value_from_enterprise_value(
    enterprise_value: float,
    debt: float,
    cash: float,
) -> float:
    return enterprise_value - debt + cash


def calculate_intrinsic_value_per_share(
    equity_value: float,
    shares_outstanding: float,
) -> float:
    if shares_outstanding <= 0:
        raise ValueError("Shares outstanding must be positive.")
    return equity_value / shares_outstanding


def calculate_dcf_sensitivity_table(
    base_cash_flow: float,
    discount_rates: Sequence[float],
    terminal_growth_rates: Sequence[float],
) -> list[dict[str, float | None]]:
    rows = []
    for discount_rate in discount_rates:
        for growth_rate in terminal_growth_rates:
            intrinsic_value = None
            if discount_rate > growth_rate:
                intrinsic_value = calculate_terminal_value_gordon(base_cash_flow, discount_rate, growth_rate)
            rows.append(
                {
                    "discount_rate": discount_rate,
                    "terminal_growth_rate": growth_rate,
                    "terminal_value": intrinsic_value,
                },
            )
    return rows
