# Athena AI Risk Terminal

Athena AI Risk Terminal is a bilingual quantitative finance and risk management
platform built as a portfolio-ready full-stack project. It combines market data,
equity research, portfolio construction, trade workflow, risk monitoring,
volatility/rates/options analytics, stress testing, P&L attribution,
reconciliation, reporting and AI-assisted monitoring.

The current version is designed for a recruiter or GitHub walkthrough: the
backend is module-based, the frontend exposes a connected financial dashboard,
and the demo workflow can run a full Athena portfolio risk pack from one button.

## What It Shows

- Clean FastAPI module architecture with thin routes, services, repositories and
  domain calculation boundaries.
- React / TypeScript / Vite frontend with routed financial workstations.
- SQLite demo persistence for portfolio, trades, P&L, reconciliation, limits,
  stress, anomaly and report snapshots.
- A recruiter-ready dashboard action: `Run Athena Demo Portfolio`.
- A system map page at `/architecture`.
- Bilingual UI foundation in English and French.
- Backend and frontend validation commands that run cleanly.

## Active Modules

Athena currently exposes 16 connected workstations or services:

All active modules are presented at `Functional` level in the dashboard,
architecture map and module documentation.

1. Market Data
2. Equity Analysis
3. Portfolio Builder
4. Trade Simulator
5. Trade Blotter
6. Risk Monitor
7. Volatility Lab
8. Options Pricing Lab
9. Rates Lab
10. Stress Testing
11. Limit Center
12. P&L Attribution
13. Reconciliation Center
14. Reports Center
15. AI Anomaly Center
16. Athena Intelligence / Demo Workflow support

`risk_analytics` remains an internal shared analytics utility used by several
modules.

## Architecture Summary

```text
frontend/
  React + TypeScript + Vite workstations
        |
backend/
  FastAPI app
  app/modules/<module>/
    routes.py       thin API layer
    schemas.py      request/response models
    service.py      business orchestration
    repository.py   persistence access
    domain/         pure finance calculations
        |
SQLite demo persistence
```

Shared infrastructure such as configuration, database sessions, exception
handling and dependency wiring stays centralized.

## Demo Workflow

The dashboard can run:

```text
Portfolio Builder
  -> Market Data
  -> Risk Monitor
  -> P&L Attribution
  -> Reconciliation
  -> Limit Center
  -> AI Anomaly Center
  -> Reports Center
```

Demo workflow API:

```text
GET  /api/demo/status
POST /api/demo/run-athena-demo
GET  /api/demo/history
```

## Local Development

Backend:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Windows helper:

```powershell
powershell -ExecutionPolicy Bypass -File .\start-dev.ps1
```

Local URLs:

- Frontend: `http://localhost:5173`
- Backend health: `http://localhost:8000/api/health`
- Backend API docs: `http://localhost:8000/docs`

## Validation

```bash
cd backend
python -m pytest
```

```bash
cd frontend
npm run build
```

## Documentation

- [Architecture](docs/architecture.md)
- [Demo Guide](docs/DEMO_GUIDE.md)
- [Modules](docs/MODULES.md)
- [Roadmap](docs/roadmap.md)
- [Limitations](docs/LIMITATIONS.md)
- [Screenshots Guide](docs/SCREENSHOTS.md)
- Historical planning references remain in `docs/athena_detailed_plan.md`,
  `docs/product-spec.md` and `docs/project-plan.md`.

## Current Limits

- Demo/local data only; no live market data vendor by default.
- No real broker execution or custodian integration.
- SQLite is used for local demonstration rather than production scale.
- AI commentary has deterministic fallback behavior when no provider is
  configured.
- Outputs are analytical and educational, not investment advice.
