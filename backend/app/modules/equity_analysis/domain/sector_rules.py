def interpret_sector_ratios(
    sector: str,
    industry: str,
    ratios: dict[str, float | None],
) -> list[str]:
    normalized = f"{sector} {industry}".lower()
    if "bank" in normalized or "financial" in normalized:
        return [
            "For banks, P/B and ROE carry more weight than industrial leverage ratios.",
            "Debt ratios are less comparable because leverage is part of the business model.",
        ]
    if "reit" in normalized or "real estate" in normalized:
        return [
            "For REITs, FFO/AFFO would be preferred; current implementation uses placeholders.",
            "Dividend sustainability should be read with property cash-flow metrics.",
        ]
    if "technology" in normalized or "software" in normalized or "semiconductor" in normalized:
        return [
            "For technology companies, margins, reinvestment efficiency and growth durability matter more than book value.",
            "P/E and EV/Sales should be read alongside growth and free cash flow conversion.",
        ]
    return [
        "General industrial interpretation: profitability, leverage, liquidity and valuation multiples should be read together.",
    ]


def classify_sector_ratio_emphasis(sector: str, industry: str) -> list[str]:
    normalized = f"{sector} {industry}".lower()
    if "bank" in normalized:
        return ["P/B", "ROE", "Net interest margin placeholder"]
    if "reit" in normalized or "real estate" in normalized:
        return ["FFO placeholder", "AFFO placeholder", "Dividend coverage"]
    if "technology" in normalized:
        return ["Revenue growth", "Operating margin", "FCF conversion", "EV/Sales"]
    return ["ROE", "Debt-to-equity", "Operating margin", "P/E"]
