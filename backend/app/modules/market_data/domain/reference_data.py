def get_demo_fx_rate(base_currency: str, quote_currency: str) -> float:
    base = base_currency.upper()
    quote = quote_currency.upper()
    if base == quote:
        return 1.0

    rates = {
        ("USD", "CAD"): 1.37,
        ("CAD", "USD"): 0.73,
        ("EUR", "USD"): 1.08,
        ("GBP", "USD"): 1.27,
        ("USD", "EUR"): 0.93,
        ("USD", "GBP"): 0.79,
    }
    return rates.get((base, quote), 1.0)


def get_risk_free_rate_proxy(currency: str = "USD", tenor: str = "3M") -> float:
    rates = {
        ("USD", "3M"): 0.04,
        ("USD", "10Y"): 0.046,
        ("CAD", "3M"): 0.038,
        ("EUR", "3M"): 0.032,
    }
    return rates.get((currency.upper(), tenor.upper()), 0.04)


def convert_market_value(value: float, fx_rate: float) -> float:
    return value * fx_rate
