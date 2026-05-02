# Athena AI Risk Terminal

Athena AI Risk Terminal is a bilingual quantitative finance and risk management platform designed around a clean full-stack architecture. This repository now contains the initial technical foundation described in `docs/architecture.md`: a FastAPI backend with thin routes and service boundaries, plus a React TypeScript frontend with an app shell, routing, and i18n.

## Architecture Summary

- Frontend: React + TypeScript + Vite application shell with routed feature placeholders.
- Backend: FastAPI API with thin routes, service orchestration, repository placeholders, and domain packages reserved for pure quant logic.
- Data services: PostgreSQL and Redis are provisioned through `docker-compose.yml` for future persistence and worker flows.
- i18n: visible frontend labels live in `frontend/src/i18n/en.json` and `frontend/src/i18n/fr.json`.

## Project Structure

```text
athena-ai-risk-terminal/
├── backend/
├── frontend/
├── docs/
├── notebooks/
└── docker-compose.yml
```

## Local Development

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Optional local services

```bash
docker compose up -d postgres redis
```

## Local URLs

- Backend URL: `http://localhost:8000`
- Backend health: `http://localhost:8000/api/health`
- Backend API docs: `http://localhost:8000/docs`
- Frontend URL: `http://localhost:5173`

## Current Scope

- Implemented: backend health endpoint, placeholder module routes, service/repository/domain scaffolding, frontend shell, sidebar navigation, reusable finance display components, and English/French translations.
- Deferred intentionally: authentication, advanced database migrations, VaR/CVaR engines, Black-Scholes, rates analytics, RiskDNA scoring, report generation, and other finance-heavy logic beyond placeholders.

## Documentation

- Architecture: [docs/architecture.md](docs/architecture.md)
- Detailed plan: [docs/athena_detailed_plan.md](docs/athena_detailed_plan.md)
- Product specification: [docs/product-spec.md](docs/product-spec.md)
