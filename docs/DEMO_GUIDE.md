# Athena Demo Guide

Use this path when presenting Athena in a GitHub, LinkedIn or interview context.

## Fast Demo

1. Start the backend and frontend.
2. Open the dashboard.
3. Click `Run Athena Demo Portfolio`.
4. Read the generated demo summary.
5. Open the generated report in Reports Center.
6. Visit `/architecture` to show the system map.

## Recommended Walkthrough

```text
Dashboard
  -> Portfolio Builder
  -> Market Data
  -> Risk Monitor
  -> P&L Attribution
  -> Reconciliation
  -> Limit Center
  -> AI Anomaly Center
  -> Reports Center
  -> Architecture
```

## What To Highlight

- The modules are connected, not isolated screens.
- Demo portfolio values are editable and flow into downstream analytics.
- Market Data powers portfolio coverage and risk inputs.
- Risk Monitor, limits, stress, P&L and reconciliation produce control outputs.
- Reports Center creates snapshot-based outputs.
- AI Anomaly Center scans persisted history with explicit limitations.
- The architecture page explains backend modules and persistence clearly.

## Demo API

```text
GET  /api/demo/status
POST /api/demo/run-athena-demo
GET  /api/demo/history
```

## Validation Before Demo

```bash
cd backend
python -m pytest
```

```bash
cd frontend
npm run build
```

## Demo Limits To Mention

- Local/demo data, not a live production feed.
- No broker execution.
- No real custodian integration.
- SQLite local persistence.
- Deterministic fallback for AI commentary when no provider is configured.
