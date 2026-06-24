from __future__ import annotations

from copy import deepcopy
from typing import Any


Scenario = dict[str, Any]


_SCENARIOS: list[Scenario] = [
    {
        "id": "equity_selloff",
        "name": "Equity Selloff",
        "description": "Broad equity market downturn with a modest defensive fixed-income offset.",
        "asset_class_shocks": {"equity": -0.20, "etf": -0.15, "fixed_income": 0.02},
        "sector_shocks": {"Technology": -0.25},
        "symbol_shocks": {},
        "rate_shock_bps": 0.0,
        "volatility_shock": 0.40,
        "fx_shock": 0.0,
        "credit_spread_shock_bps": 0.0,
        "liquidity_multiplier": 1.0,
    },
    {
        "id": "technology_shock",
        "name": "Technology Shock",
        "description": "Concentrated technology selloff with broad-market spillover.",
        "asset_class_shocks": {"equity": -0.12, "etf": -0.12, "fixed_income": 0.01},
        "sector_shocks": {"Technology": -0.30},
        "symbol_shocks": {},
        "rate_shock_bps": 0.0,
        "volatility_shock": 0.50,
        "fx_shock": 0.0,
        "credit_spread_shock_bps": 0.0,
        "liquidity_multiplier": 1.0,
    },
    {
        "id": "rates_shock_up",
        "name": "Rates Shock Up",
        "description": "Inflation or central-bank tightening shock with higher rates.",
        "asset_class_shocks": {"equity": -0.05, "etf": -0.05},
        "sector_shocks": {"Technology": -0.08},
        "symbol_shocks": {},
        "rate_shock_bps": 100.0,
        "volatility_shock": 0.25,
        "fx_shock": 0.0,
        "credit_spread_shock_bps": 0.0,
        "liquidity_multiplier": 1.0,
    },
    {
        "id": "rates_shock_down",
        "name": "Rates Shock Down",
        "description": "Growth slowdown and monetary easing shock with lower rates.",
        "asset_class_shocks": {"equity": 0.04, "etf": 0.03},
        "sector_shocks": {},
        "symbol_shocks": {},
        "rate_shock_bps": -100.0,
        "volatility_shock": 0.15,
        "fx_shock": 0.0,
        "credit_spread_shock_bps": 0.0,
        "liquidity_multiplier": 1.0,
    },
    {
        "id": "volatility_spike",
        "name": "Volatility Spike",
        "description": "Market volatility stress with broad equity pressure.",
        "asset_class_shocks": {"equity": -0.10, "etf": -0.10},
        "sector_shocks": {},
        "symbol_shocks": {},
        "rate_shock_bps": 0.0,
        "volatility_shock": 0.75,
        "fx_shock": 0.0,
        "credit_spread_shock_bps": 0.0,
        "liquidity_multiplier": 1.0,
    },
    {
        "id": "usd_shock",
        "name": "USD Shock",
        "description": "USD appreciation stress with translation impact on non-USD exposures.",
        "asset_class_shocks": {},
        "sector_shocks": {},
        "symbol_shocks": {},
        "rate_shock_bps": 0.0,
        "volatility_shock": 0.10,
        "fx_shock": 0.10,
        "credit_spread_shock_bps": 0.0,
        "liquidity_multiplier": 1.0,
    },
    {
        "id": "credit_spread_widening",
        "name": "Credit Spread Widening",
        "description": "Credit-risk stress with wider spreads on fixed-income holdings.",
        "asset_class_shocks": {"equity": -0.03, "etf": -0.04},
        "sector_shocks": {},
        "symbol_shocks": {},
        "rate_shock_bps": 0.0,
        "volatility_shock": 0.30,
        "fx_shock": 0.0,
        "credit_spread_shock_bps": 150.0,
        "liquidity_multiplier": 1.0,
    },
    {
        "id": "risk_off_combined",
        "name": "Risk-Off Combined Scenario",
        "description": "Severe multi-asset risk-off scenario across equities, rates, volatility and credit.",
        "asset_class_shocks": {"equity": -0.20, "etf": -0.18, "fixed_income": 0.01},
        "sector_shocks": {"Technology": -0.30},
        "symbol_shocks": {},
        "rate_shock_bps": -50.0,
        "volatility_shock": 0.80,
        "fx_shock": 0.05,
        "credit_spread_shock_bps": 200.0,
        "liquidity_multiplier": 1.25,
    },
    {
        "id": "liquidity_shock",
        "name": "Liquidity Shock",
        "description": "Market liquidity deterioration with larger haircuts on concentrated positions.",
        "asset_class_shocks": {"equity": -0.06, "etf": -0.04, "fixed_income": -0.03},
        "sector_shocks": {},
        "symbol_shocks": {},
        "rate_shock_bps": 0.0,
        "volatility_shock": 0.35,
        "fx_shock": 0.0,
        "credit_spread_shock_bps": 75.0,
        "liquidity_multiplier": 1.75,
    },
]


def list_predefined_scenarios() -> list[Scenario]:
    return deepcopy(_SCENARIOS)


def get_predefined_scenario(scenario_id: str) -> Scenario | None:
    normalized = scenario_id.strip().lower()
    for scenario in _SCENARIOS:
        if scenario["id"] == normalized:
            return deepcopy(scenario)
    return None


def build_custom_scenario(payload: dict[str, Any]) -> Scenario:
    return {
        "id": "custom_scenario",
        "name": payload.get("name") or "Custom Scenario",
        "description": payload.get("description") or "User-defined multi-asset stress scenario.",
        "asset_class_shocks": {
            "equity": float(payload.get("equity_shock", 0.0)),
            **{
                str(key): float(value)
                for key, value in dict(payload.get("asset_class_shocks") or {}).items()
            },
        },
        "sector_shocks": {
            str(key): float(value)
            for key, value in dict(payload.get("sector_shocks") or {}).items()
        },
        "symbol_shocks": {
            str(key).upper(): float(value)
            for key, value in dict(payload.get("symbol_shocks") or {}).items()
        },
        "rate_shock_bps": float(payload.get("rate_shock_bps", 0.0)),
        "volatility_shock": float(payload.get("volatility_shock", 0.0)),
        "fx_shock": float(payload.get("fx_shock", 0.0)),
        "credit_spread_shock_bps": float(payload.get("credit_spread_shock_bps", 0.0)),
        "liquidity_multiplier": float(payload.get("liquidity_multiplier", 1.0)),
    }
