# Athena Backend

This backend follows the architecture in `docs/architecture.md`:

- FastAPI routes stay thin.
- Services orchestrate use cases.
- Repositories isolate persistence concerns.
- Domain packages are reserved for pure quant logic that will be added incrementally.
- Feature modules are progressively consolidated under `app/modules/<module_name>/`.

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
- Market Data, Equity Analysis and Portfolio Builder are migrated into `app/modules/`.
- Some remaining features still use the older global route/schema/service/repository layout and should be migrated progressively.
- PostgreSQL and Redis are supported through environment variables, while the default database URL uses local SQLite so the app can boot without extra setup.

## Module layout

Migrated backend modules follow this structure:

```text
app/modules/<module_name>/
├── routes.py
├── schemas.py
├── service.py
├── repository.py
└── domain/
```

Current migrated modules:

```text
app/modules/market_data/
app/modules/equity_analysis/
app/modules/portfolio_builder/
```

Shared files stay centralized:

```text
app/core/
app/database/
app/models/
app/api/dependencies.py
```
