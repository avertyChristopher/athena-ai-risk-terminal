# Athena Roadmap

This roadmap reflects the current state after the module migration and workflow
connection work.

## Completed Foundation

- Module-based backend for Market Data, Equity Analysis, Portfolio Builder, Risk
  Monitor and Trade Simulator.
- SQLite-backed persistence for portfolios and positions.
- Editable Athena Demo Portfolio.
- Market Data coverage and CSV import workflow.
- Portfolio row actions that connect to Market Data, Equity Analysis and Trade
  Simulator.
- Risk Monitor connected to selected portfolio, with configurable limits and
  stress shocks.
- Equity Analysis analyst scorecard.
- Frontend styling improved toward a modern financial terminal.

## Next Engineering Priorities

1. Add GitHub Actions CI for backend tests and frontend build.
2. Add Alembic migrations for persistent tables.
3. Add API-level tests for the major cross-module workflows.
4. Add frontend tests for portfolio context and workflow navigation.
5. Add a real database profile for PostgreSQL while keeping SQLite local dev.
6. Add authentication only after the demo workflow is stable.

## Next Finance/Product Priorities

1. Expand Market Data import to support provider adapters and larger CSV files.
2. Add benchmark constituent weights for active risk.
3. Add richer Risk Monitor scenario libraries and saved scenario sets.
4. Add portfolio-level reports that combine Market Data, Equity Analysis and
   Risk Monitor output.
5. Expand Equity Analysis coverage beyond the demo equity universe.

## Portfolio Presentation Priorities

1. Add screenshots and a short video demo.
2. Update README with the demo flow.
3. Add architecture diagram image.
4. Add "Known limitations" and "Next steps" sections clearly.
5. Keep commits grouped by major feature area.
