# Athena Modules

This document describes the current active module set.

## Active Workstations And Services

| Module | Current Role | Status |
| --- | --- | --- |
| Market Data | Prices, returns, volatility, coverage and data quality | Functional |
| Equity Analysis | Fundamentals, ratios, valuation and analyst diagnostics | Functional |
| Portfolio Builder | Portfolio construction, positions, allocation and policy context | Functional |
| Trade Simulator | Portfolio-aware pre-trade simulation | Functional |
| Trade Blotter | Persistent simulated trade register and review workflow | Functional |
| Risk Monitor | VaR/CVaR, drawdown, concentration, risk score and alerts | Functional |
| Volatility Lab | Realized/EWMA volatility, beta, correlation and VaR source analytics | Functional |
| Options Pricing Lab | Black-Scholes, Greeks, parity, payoff and strategy analytics | Functional |
| Rates Lab | Bond pricing, yield, duration, convexity, DV01 and curve scenarios | Functional |
| Stress Testing | Multi-asset scenario losses and limit-ready payloads | Functional |
| Limit Center | Governance rules, breach detection and exception workflow | Functional |
| P&L Attribution | Performance and P&L decomposition by position/group/drivers | Functional |
| Reconciliation Center | Position, cash, price, trade and P&L breaks | Functional |
| Reports Center | Snapshot-based JSON, Markdown and CSV reports | Functional |
| AI Anomaly Center | Rule-based anomaly scans across persisted history | Functional |
| Athena Intelligence | Structured commentary with deterministic fallback | Functional |

## Utility Modules

| Module | Role |
| --- | --- |
| demo_workflow | Orchestrates the recruiter-ready demo run without duplicating business logic |
| risk_analytics | Shared risk calculations reused by portfolio, trade and risk modules |

## Current Integration Shape

```text
Market Data -> Equity Analysis -> Portfolio Builder
Portfolio Builder -> Trade Simulator -> Trade Blotter
Portfolio Builder + Market Data -> Risk Monitor
Volatility/Rates/Options/Stress -> Risk Monitor -> Limit Center
Portfolio + Market Data + Trades -> P&L Attribution -> Reconciliation
Risk/P&L/Reconciliation/Limits/Stress/Anomalies -> Reports Center
Persisted history -> AI Anomaly Center -> Athena Intelligence
```

## Next Module Candidates

The best next work is not necessarily a new module. The strongest next step is
to harden the existing modules with tests, persistence clarity, richer demo
data and better reports.

If adding a module, the most logical candidates are:

- Benchmark & Performance Analytics.
- Factor Risk / Exposure Attribution.
- Scenario Library Manager.
- Data Import Center.
