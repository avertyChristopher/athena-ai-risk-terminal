# Athena Current Limitations

Athena is intentionally transparent about its current limits.

## Data

- Market data is local/demo-oriented by default.
- No live vendor feed is connected by default.
- Fundamental data is demo data, not a live filing or data provider feed.
- Some calculations use deterministic fallback assumptions when source data is
  incomplete.

## Persistence

- SQLite is used for local development and demo persistence.
- PostgreSQL is a future deployment-hardening path.
- Some generated analytics are snapshots rather than continuously refreshed
  live state.

## Trading And Operations

- No broker execution.
- No real order management system.
- No custodian integration.
- Reconciliation uses deterministic demo reference data.

## Quant And Risk

- Models are educational and analytical.
- Options pricing is useful for demonstration, but not execution quoting.
- Stress scenarios are deterministic demo scenarios unless extended.
- AI Anomaly Center is rule-based monitoring, not production fraud detection.

## AI

- Athena Intelligence uses deterministic fallback when no AI provider is
  configured.
- Outputs must not be interpreted as investment advice.
- AI commentary is generated from structured payloads only.

## Security And Deployment

- Authentication is not yet the central focus.
- Production authorization, secrets management and deployment hardening remain
  future work.
