# Athena Backend

This backend follows the architecture in `docs/architecture.md`:

- FastAPI routes stay thin.
- Services orchestrate use cases.
- Repositories isolate persistence concerns.
- Domain packages are reserved for pure quant logic that will be added incrementally.

## Run locally

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`, with docs at `http://localhost:8000/docs`.

## Test

```bash
cd backend
pytest
```

## Current foundation

- `GET /api/health` returns the backend health payload.
- Placeholder routers exist for market data, portfolios, trades, risk, pricing, rates, P&L, AI, and reports.
- PostgreSQL and Redis are supported through environment variables, while the default database URL uses local SQLite so the app can boot without extra setup.
