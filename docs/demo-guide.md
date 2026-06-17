# Athena Demo Guide

This guide describes the current end-to-end demo flow for Athena AI Risk
Terminal.

## Goal

Show a recruiter or reviewer that Athena is not only a collection of isolated
pages. The core demo is a connected portfolio workflow:

```text
Portfolio Builder -> Market Data -> Equity Analysis -> Trade Simulator -> Risk Monitor
```

## Recommended Demo Flow

1. Open Portfolio Builder.
2. Select Athena Demo Portfolio.
3. Edit or add a position to show that portfolio data is persisted.
4. Use a row action to open Market Data for the selected symbol.
5. Review Market Data coverage for all portfolio symbols.
6. Import CSV prices if a symbol is missing from Market Data.
7. Return to Portfolio Builder and open Equity Analysis for an equity holding.
8. Review the analyst scorecard and valuation/profitability/growth diagnostics.
9. Open Trade Simulator from a position row and review pre-trade impact.
10. Open Risk Monitor and adjust limits or stress shocks.

## Current Demo Data

The demo portfolio is persisted in SQLite and seeded from the original demo
data when the local database is empty.

Current important datasets:

- `portfolio_builder_portfolios`
- `portfolio_builder_positions`
- `market_data_custom_assets`
- `market_data_custom_prices`
- bundled demo assets and prices under `data/demo/`

## Market Data CSV Format

The Market Data import workflow expects these required headers:

```csv
date,symbol,open,high,low,close,volume
```

Optional headers:

```csv
name,asset_type,currency,sector,country,exchange,industry
```

## Validation Commands

Backend:

```bash
cd backend
python -m pytest
```

Frontend:

```bash
cd frontend
npm run build
```

## Known Demo Limits

- Data is local/demo-oriented, not a live institutional market data feed.
- SQLite persistence is appropriate for local demo usage, not production scale.
- Equity Analysis currently supports the configured demo equity universe best.
- Risk Monitor realized metrics depend on available Market Data return history.
- AI reporting and full production authentication remain future work.
