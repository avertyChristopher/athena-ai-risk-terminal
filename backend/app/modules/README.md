Backend module map for Athena AI Risk Terminal.

This directory is the target home for product-oriented backend modules. Each
module should own its route, schema, service, repository and domain code while
shared infrastructure remains centralized.

Current migrated modules:
- `market_data`
- `equity_analysis`
- `portfolio_builder`

Migrated module pattern:

```text
app/modules/<module_name>/
├── routes.py
├── schemas.py
├── service.py
├── repository.py
└── domain/
    └── pure calculation files
```

Rules:
- Keep FastAPI routes thin.
- Put use-case orchestration in `service.py`.
- Put persistence/data access in `repository.py`.
- Put pure financial calculations in `domain/`.
- Put request/response contracts in `schemas.py`.
- Keep API paths stable during migrations.
- Do not migrate multiple modules in one refactor unless explicitly planned.

Shared infrastructure such as database sessions, configuration, logging,
exceptions and security remains centralized under `app/core` and `app/database`.
SQLAlchemy models remain centralized under `app/models` for now.
