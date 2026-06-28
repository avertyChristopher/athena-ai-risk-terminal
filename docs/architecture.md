# Athena Architecture

Athena AI Risk Terminal uses a module-first architecture for product features
and keeps shared infrastructure centralized.

## Backend

```text
backend/app/
|-- main.py
|-- api/dependencies.py
|-- core/
|-- database/
|-- models/
`-- modules/
    |-- market_data/
    |-- equity_analysis/
    |-- portfolio_builder/
    |-- trade_simulator/
    |-- trade_blotter/
    |-- risk_monitor/
    |-- volatility_lab/
    |-- options_pricing_lab/
    |-- rates_lab/
    |-- stress_testing/
    |-- limit_center/
    |-- pnl_attribution/
    |-- reconciliation/
    |-- reports_center/
    |-- ai_anomaly_center/
    |-- athena_intelligence/
    |-- demo_workflow/
    `-- risk_analytics/
```

Module pattern:

```text
routes.py      API boundary, request validation, dependency injection
schemas.py     Pydantic request and response models
service.py     business workflow and orchestration
repository.py  database or demo store access
domain/        pure financial calculations and deterministic helpers
```

`risk_analytics` is an internal shared analytics utility, not a standalone
frontend workstation.

## Frontend

```text
frontend/src/
|-- app/
|-- components/
|-- context/
|-- features/
|-- services/
|-- types/
|-- i18n/
`-- styles.css
```

Frontend pages are routed by feature. Heavy workstations are lazy-loaded through
React Suspense. The dashboard, architecture map and demo workflow use shared
services and typed API clients.

## Current Demo Workflow

```text
Dashboard
  -> POST /api/demo/run-athena-demo
  -> Portfolio Builder
  -> Market Data
  -> Risk Monitor
  -> P&L Attribution
  -> Reconciliation Center
  -> Limit Center
  -> AI Anomaly Center
  -> Reports Center
```

The demo workflow is intentionally an orchestrator. It does not duplicate the
logic of the underlying modules.

## Persistence

SQLite is the current local demo persistence layer. The UI labels persistence
status explicitly:

- persistent history for trades, P&L, reconciliation, limits, stress and
  anomalies;
- SQLite demo snapshots for reports and Athena commentary;
- deterministic fallback when data or AI providers are unavailable.

## API Paths

Existing feature API paths remain stable. The demo workflow adds:

```text
GET  /api/demo/status
POST /api/demo/run-athena-demo
GET  /api/demo/history
```

## Architecture Rules

- Keep routes thin.
- Keep business orchestration in `service.py`.
- Keep pure calculations in `domain/`.
- Keep schemas inside the module.
- Keep shared config, database sessions and core files centralized.
- Migrate modules progressively; do not mass-move unrelated modules.
- Add tests for public routes and important financial calculations.
