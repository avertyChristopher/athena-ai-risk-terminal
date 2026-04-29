# Athena AI Risk Terminal — Complete GitHub Issues Roadmap  
# Roadmap complète des issues GitHub — Athena AI Risk Terminal

**Recommended file path / Emplacement recommandé :** `docs/github-issues.md`  
**Project / Projet :** Athena AI Risk Terminal  
**Purpose / Objectif :** provide a complete, ordered list of GitHub issues to create and implement.  
**Objectif :** fournir une liste complète et ordonnée des issues GitHub à créer et implémenter.

---

## 1. How to use this document / Comment utiliser ce document

### English

This file is the operational roadmap for Athena AI Risk Terminal.  
It transforms the project plan into concrete GitHub issues.

Use it like this:

1. Create the labels and milestones first.
2. Create the issues phase by phase.
3. Work on one issue at a time.
4. Use a dedicated branch for each feature or issue.
5. Ask Codex to implement only one issue at a time.
6. Run tests before merging.
7. Update documentation when the implementation changes.

### Français

Ce fichier est la roadmap opérationnelle du projet Athena AI Risk Terminal.  
Il transforme le plan du projet en issues GitHub concrètes.

Utilisation recommandée :

1. Créer les labels et milestones d’abord.
2. Créer les issues phase par phase.
3. Travailler sur une issue à la fois.
4. Utiliser une branche dédiée pour chaque feature ou issue.
5. Demander à Codex d’implémenter une seule issue à la fois.
6. Lancer les tests avant de merger.
7. Mettre à jour la documentation quand l’implémentation change.

---

## 2. Global Rule / Règle globale

### English

Do not ask Codex to build the full application in one request.  
Each issue must be implemented, tested and reviewed independently.

### Français

Ne demande pas à Codex de construire toute l’application en une seule demande.  
Chaque issue doit être implémentée, testée et révisée indépendamment.

---

## 3. Recommended GitHub Labels / Labels GitHub recommandés

Create these labels first:

```text
documentation
architecture
backend
frontend
database
devops
quant
risk
ai
portfolio
market-data
pricing
rates
pnl
reports
testing
security
project-management
good first issue
priority-high
priority-medium
priority-low
```

---

## 4. Recommended Milestones / Milestones recommandés

```text
M0 — Documentation and repository foundation
M1 — Technical foundation
M2 — Market data and portfolio
M3 — Performance, volatility and risk
M4 — Trade simulation and RiskDNA
M5 — Options and rates
M6 — Middle office workflows
M7 — AI and reports
M8 — Testing, CI/CD and final polish
```

---

# Phase 0 — Documentation and Repository Foundation  
# Phase 0 — Documentation et base du repository

---

## Issue 1 — Add project README

**Labels:** `documentation`, `priority-high`  
**Milestone:** `M0 — Documentation and repository foundation`  
**Suggested branch:** `docs/readme`

### Goal / Objectif

Create a professional README that explains Athena AI Risk Terminal clearly.

Créer un README professionnel qui explique clairement Athena AI Risk Terminal.

### Tasks / Tâches

- Add `README.md` at repository root.
- Add project name.
- Add short English description.
- Add short French description.
- Add project vision.
- Add planned features.
- Add tech stack.
- Add documentation links.
- Add project status.
- Add author name.

### Acceptance criteria / Critères d’acceptation

- `README.md` exists.
- README explains the project in English and French.
- README links to:
  - `docs/project-plan.md`
  - `docs/architecture.md`
  - `docs/product-spec.md`
  - `docs/athena_detailed_plan.md`
- README gives a professional first impression.

### Suggested commit

```text
docs: add project README
```

---

## Issue 2 — Add simple project plan

**Labels:** `documentation`, `priority-high`  
**Milestone:** `M0 — Documentation and repository foundation`  
**Suggested branch:** `docs/project-plan`

### Goal / Objectif

Add a simple roadmap to understand where the project is and what comes next.

Ajouter une roadmap simple pour comprendre où en est le projet et quoi faire ensuite.

### Tasks

- Add `docs/project-plan.md`.
- Summarize the project vision.
- Explain the current phase.
- List the main phases.
- Include English and French.
- Keep this file simpler than the detailed plan.

### Acceptance criteria

- `docs/project-plan.md` exists.
- The file makes the project easier to follow.
- It clearly shows the next steps.

### Suggested commit

```text
docs: add simple project plan
```

---

## Issue 3 — Add detailed project plan

**Labels:** `documentation`, `priority-high`  
**Milestone:** `M0 — Documentation and repository foundation`  
**Suggested branch:** `docs/detailed-plan`

### Goal / Objectif

Add the complete detailed plan for Athena AI Risk Terminal.

Ajouter le plan détaillé complet du projet Athena AI Risk Terminal.

### Tasks

- Add `docs/athena_detailed_plan.md`.
- Include the main project plan.
- Include the Quant, Derivatives and Rates extension.
- Include the 4-month roadmap.
- Include Codex prompts.
- Include CV and LinkedIn material.

### Acceptance criteria

- `docs/athena_detailed_plan.md` exists.
- The plan includes front office, middle office, quant, AI and reports.
- The plan includes VaR, CVaR, volatility, Black-Scholes, Greeks, yield curves, spot rates and bond pricing.

### Suggested commit

```text
docs: add merged detailed plan for Athena AI Risk Terminal
```

---

## Issue 4 — Add architecture documentation

**Labels:** `documentation`, `architecture`, `priority-high`  
**Milestone:** `M0 — Documentation and repository foundation`  
**Suggested branch:** `docs/architecture`

### Goal / Objectif

Define a stable technical architecture before writing code.

Définir une architecture technique stable avant de coder.

### Tasks

- Add `docs/architecture.md`.
- Define backend architecture.
- Define frontend architecture.
- Define domain/service/repository separation.
- Define testing strategy.
- Define API architecture.
- Define Codex usage rules.

### Acceptance criteria

- `docs/architecture.md` exists.
- Backend structure is documented.
- Frontend structure is documented.
- Routes are documented as thin controllers.
- Business logic is documented as service/domain responsibility.
- Quant calculations are documented as domain modules.

### Suggested commit

```text
docs: add architecture documentation
```

---

## Issue 5 — Add product specification

**Labels:** `documentation`, `priority-high`  
**Milestone:** `M0 — Documentation and repository foundation`  
**Suggested branch:** `docs/product-spec`

### Goal / Objectif

Define what the product must do and who it is for.

Définir ce que le produit doit faire et pour qui il est conçu.

### Tasks

- Add `docs/product-spec.md`.
- Define target users.
- Define product modules.
- Add user stories.
- Add acceptance criteria.
- Define MVP.
- Define non-functional requirements.

### Acceptance criteria

- `docs/product-spec.md` exists.
- Each major module has a purpose.
- Each major module has acceptance criteria.
- MVP is clearly defined.

### Suggested commit

```text
docs: add product specification
```

---

## Issue 6 — Add GitHub issues roadmap

**Labels:** `documentation`, `project-management`, `priority-high`  
**Milestone:** `M0 — Documentation and repository foundation`  
**Suggested branch:** `docs/github-issues`

### Goal / Objectif

Add this roadmap as a permanent project management reference.

Ajouter cette roadmap comme référence permanente de gestion du projet.

### Tasks

- Add `docs/github-issues.md`.
- Organize issues by phase.
- Add labels and milestones.
- Add tasks and acceptance criteria.
- Add suggested commits and branches.

### Acceptance criteria

- `docs/github-issues.md` exists.
- The file lists all issues in a logical order.
- The file can guide development from start to finish.

### Suggested commit

```text
docs: add github issues roadmap
```

---

## Issue 7 — Add `.gitignore`

**Labels:** `devops`, `security`, `priority-high`  
**Milestone:** `M0 — Documentation and repository foundation`  
**Suggested branch:** `chore/gitignore`

### Goal / Objectif

Prevent useless, generated or sensitive files from being committed.

Empêcher les fichiers inutiles, générés ou sensibles d’être commités.

### Tasks

- Ignore `.env`.
- Ignore `.env.*` except `.env.example`.
- Ignore Python cache.
- Ignore virtual environments.
- Ignore Node modules.
- Ignore build folders.
- Ignore local databases.
- Ignore generated reports.
- Ignore raw data folders if needed.

### Acceptance criteria

- `.gitignore` exists at repository root.
- `.env` is ignored.
- `node_modules/` is ignored.
- `venv/` and `.venv/` are ignored.
- Generated outputs are ignored.

### Suggested commit

```text
chore: add gitignore
```

---

## Issue 8 — Add Docker Compose foundation

**Labels:** `devops`, `backend`, `frontend`, `priority-medium`  
**Milestone:** `M0 — Documentation and repository foundation`  
**Suggested branch:** `chore/docker-compose`

### Goal / Objectif

Prepare the project to run locally with Docker Compose.

Préparer le projet à fonctionner localement avec Docker Compose.

### Tasks

- Add `docker-compose.yml`.
- Add services:
  - backend;
  - frontend;
  - PostgreSQL;
  - Redis.
- Add PostgreSQL named volume.
- Add placeholder environment variables.
- Keep it ready for future Dockerfiles.

### Acceptance criteria

- `docker-compose.yml` exists.
- Backend, frontend, postgres and redis services are defined.
- PostgreSQL volume exists.
- The file is ready for later implementation.

### Suggested commit

```text
chore: add docker compose foundation
```

---

## Issue 9 — Add `.env.example`

**Labels:** `devops`, `security`, `priority-high`  
**Milestone:** `M0 — Documentation and repository foundation`  
**Suggested branch:** `chore/env-example`

### Goal / Objectif

Document environment variables without exposing secrets.

Documenter les variables d’environnement sans exposer de secrets.

### Tasks

- Add `.env.example`.
- Include `DATABASE_URL`.
- Include `REDIS_URL`.
- Include `OPENAI_API_KEY`.
- Include `MARKET_DATA_API_KEY`.
- Include `VITE_API_BASE_URL`.
- Add safe placeholder values.

### Acceptance criteria

- `.env.example` exists.
- No real secret is committed.
- The file is safe to publish on GitHub.

### Suggested commit

```text
chore: add environment example file
```

---

## Issue 10 — Create GitHub labels and milestones

**Labels:** `project-management`, `documentation`, `priority-medium`  
**Milestone:** `M0 — Documentation and repository foundation`

### Goal / Objectif

Organize the GitHub repository before coding.

Organiser le repository GitHub avant de coder.

### Tasks

- Create recommended labels.
- Create recommended milestones.
- Assign issues to milestones.
- Use priorities consistently.

### Acceptance criteria

- Labels exist.
- Milestones exist.
- Issues are organized.
- The repository looks professional.

### Suggested commit

```text
No commit required.
```

---

# Phase 1 — Technical Foundation  
# Phase 1 — Fondation technique

---

## Issue 11 — Initialize backend FastAPI foundation

**Labels:** `backend`, `priority-high`  
**Milestone:** `M1 — Technical foundation`  
**Suggested branch:** `feature/backend-foundation`

### Goal / Objectif

Create the first working backend.

Créer le premier backend fonctionnel.

### Tasks

- Create `backend/`.
- Add FastAPI.
- Add `backend/app/main.py`.
- Add `backend/app/api/routes/health_routes.py`.
- Add `backend/app/core/config.py`.
- Add `requirements.txt` or `pyproject.toml`.
- Add backend README.

### Acceptance criteria

- Backend starts locally.
- `GET /api/health` returns status OK.
- Backend follows `docs/architecture.md`.
- Routes stay thin.

### Codex prompt

```text
Read docs/architecture.md and initialize the FastAPI backend foundation for Athena AI Risk Terminal. Add app/main.py, app/api/routes/health_routes.py, app/core/config.py and a health endpoint at GET /api/health. Keep routes thin and add a basic test.
```

### Suggested commit

```text
chore: initialize backend foundation
```

---

## Issue 12 — Add backend health endpoint tests

**Labels:** `backend`, `testing`, `priority-high`  
**Milestone:** `M1 — Technical foundation`  
**Suggested branch:** `test/backend-health`

### Goal / Objectif

Test the first backend endpoint.

Tester le premier endpoint backend.

### Tasks

- Add pytest.
- Add FastAPI test client.
- Add `backend/tests/api/test_health_routes.py`.
- Test status code.
- Test response body.

### Acceptance criteria

- `pytest` passes.
- Health endpoint test passes.
- Test is simple and deterministic.

### Suggested commit

```text
test: add backend health endpoint tests
```

---

## Issue 13 — Initialize frontend React TypeScript foundation

**Labels:** `frontend`, `priority-high`  
**Milestone:** `M1 — Technical foundation`  
**Suggested branch:** `feature/frontend-foundation`

### Goal / Objectif

Create the first working frontend.

Créer le premier frontend fonctionnel.

### Tasks

- Create `frontend/`.
- Initialize React + TypeScript + Vite.
- Add a basic homepage.
- Add folder structure:
  - `app/`
  - `components/`
  - `features/`
  - `i18n/`
  - `lib/`
  - `types/`
- Add frontend README.

### Acceptance criteria

- Frontend starts locally.
- Homepage displays Athena AI Risk Terminal.
- Structure follows `docs/architecture.md`.

### Codex prompt

```text
Initialize the React TypeScript Vite frontend for Athena AI Risk Terminal. Create a clean folder structure with app, components, features, i18n, lib and types. Add a basic homepage and prepare the structure for future bilingual UI.
```

### Suggested commit

```text
chore: initialize frontend foundation
```

---

## Issue 14 — Add AppShell layout

**Labels:** `frontend`, `priority-high`  
**Milestone:** `M1 — Technical foundation`  
**Suggested branch:** `feature/app-shell`

### Goal / Objectif

Create the main visual layout of the application.

Créer la structure visuelle principale de l’application.

### Tasks

- Add `AppShell`.
- Add `Sidebar`.
- Add `Topbar`.
- Add `PageHeader`.
- Add placeholder navigation.
- Add basic responsive layout.

### Acceptance criteria

- App has a reusable layout.
- Sidebar exists.
- Topbar exists.
- Page header exists.
- Layout is ready for future pages.

### Suggested commit

```text
feat: add application shell layout
```

---

## Issue 15 — Add bilingual UI foundation

**Labels:** `frontend`, `priority-high`  
**Milestone:** `M1 — Technical foundation`  
**Suggested branch:** `feature/i18n-foundation`

### Goal / Objectif

Add English/French support.

Ajouter le support français/anglais.

### Tasks

- Add `react-i18next`.
- Add `frontend/src/i18n/en.json`.
- Add `frontend/src/i18n/fr.json`.
- Add `frontend/src/i18n/i18n.ts`.
- Add language switch.
- Replace hardcoded visible strings.

### Acceptance criteria

- User can switch between English and French.
- Main title changes language.
- Visible UI text comes from translation files.

### Codex prompt

```text
Add bilingual support to the React frontend using react-i18next. Create en.json and fr.json, add a language switch, and make sure visible UI strings come from the translation files.
```

### Suggested commit

```text
feat: add bilingual ui foundation
```

---

## Issue 16 — Add shared frontend components

**Labels:** `frontend`, `priority-medium`  
**Milestone:** `M1 — Technical foundation`  
**Suggested branch:** `feature/shared-components`

### Goal / Objectif

Create reusable UI components for the financial terminal.

Créer des composants UI réutilisables pour le terminal financier.

### Tasks

- Add `MetricCard`.
- Add `RiskBadge`.
- Add `DataTable`.
- Add `MoneyValue`.
- Add `PercentValue`.
- Add chart wrapper components.
- Add loading and error components.

### Acceptance criteria

- Components are typed.
- Components are reusable.
- Components are visually consistent.
- Components support future i18n.

### Suggested commit

```text
feat: add shared frontend components
```

---

## Issue 17 — Add backend database foundation

**Labels:** `backend`, `database`, `priority-high`  
**Milestone:** `M1 — Technical foundation`  
**Suggested branch:** `feature/database-foundation`

### Goal / Objectif

Prepare PostgreSQL access.

Préparer l’accès à PostgreSQL.

### Tasks

- Add SQLAlchemy.
- Add `database/session.py`.
- Add `database/base.py`.
- Add database URL config.
- Add connection helper.
- Add repository base pattern.

### Acceptance criteria

- Database config is centralized.
- Database session is reusable.
- Routes do not access database directly.

### Suggested commit

```text
chore: add database foundation
```

---

# Phase 2 — Market Data and Portfolio  
# Phase 2 — Données de marché et portefeuille

---

## Issue 18 — Add Asset and MarketPrice models

**Labels:** `backend`, `database`, `market-data`, `priority-high`  
**Milestone:** `M2 — Market data and portfolio`  
**Suggested branch:** `feature/asset-marketprice-models`

### Goal / Objectif

Model assets and historical prices.

Modéliser les actifs et les prix historiques.

### Tasks

- Add `Asset` model.
- Add `MarketPrice` model.
- Add relationship between assets and prices.
- Add Pydantic schemas.
- Add repository skeleton.

### Acceptance criteria

- Asset model exists.
- MarketPrice model exists.
- One asset can have many prices.
- Schemas exist.

### Suggested commit

```text
feat: add asset and market price models
```

---

## Issue 19 — Add Market Data service and routes

**Labels:** `backend`, `market-data`, `priority-high`  
**Milestone:** `M2 — Market data and portfolio`  
**Suggested branch:** `feature/market-data-api`

### Goal / Objectif

Expose market data through the API.

Exposer les données de marché via l’API.

### Tasks

- Add `market_data_service.py`.
- Add route `GET /api/assets`.
- Add route `GET /api/assets/{symbol}`.
- Add route `GET /api/market-data/prices/{symbol}`.
- Add route `GET /api/market-data/returns/{symbol}`.
- Add tests.

### Acceptance criteria

- Asset list endpoint works.
- Price endpoint works.
- Returns endpoint works.
- Tests pass.

### Codex prompt

```text
Implement the Market Data module in the FastAPI backend. Add Asset and MarketPrice schemas, repository methods, service functions and routes for listing assets, retrieving prices and calculating returns. Add tests.
```

### Suggested commit

```text
feat: add market data api
```

---

## Issue 20 — Add Market Data frontend page

**Labels:** `frontend`, `market-data`, `priority-high`  
**Milestone:** `M2 — Market data and portfolio`  
**Suggested branch:** `feature/market-data-page`

### Goal / Objectif

Display assets and historical prices.

Afficher les actifs et les prix historiques.

### Tasks

- Add Market Data route.
- Add asset search.
- Add asset table.
- Add price chart.
- Add return distribution placeholder.
- Add loading and error states.

### Acceptance criteria

- User can open the Market Data page.
- User can see assets.
- User can see a price chart.
- UI is bilingual.

### Suggested commit

```text
feat: add market data page
```

---

## Issue 21 — Add Portfolio and Position models

**Labels:** `backend`, `database`, `portfolio`, `priority-high`  
**Milestone:** `M2 — Market data and portfolio`  
**Suggested branch:** `feature/portfolio-position-models`

### Goal / Objectif

Model portfolios and positions.

Modéliser les portefeuilles et positions.

### Tasks

- Add `Portfolio` model.
- Add `Position` model.
- Add relationships.
- Add schemas.
- Add repository skeleton.

### Acceptance criteria

- Portfolio model exists.
- Position model exists.
- A portfolio can contain many positions.
- Position references an asset.

### Suggested commit

```text
feat: add portfolio and position models
```

---

## Issue 22 — Add Portfolio Builder backend

**Labels:** `backend`, `portfolio`, `priority-high`  
**Milestone:** `M2 — Market data and portfolio`  
**Suggested branch:** `feature/portfolio-builder-api`

### Goal / Objectif

Create portfolio CRUD and portfolio calculations.

Créer le CRUD portefeuille et les calculs de portefeuille.

### Tasks

- Add portfolio service.
- Add CRUD routes.
- Add add-position route.
- Add update-position route.
- Add delete-position route.
- Calculate portfolio value.
- Calculate position weights.
- Add tests.

### Acceptance criteria

- API can create a portfolio.
- API can add positions.
- API returns portfolio value.
- API returns weights by asset.
- Tests pass.

### Codex prompt

```text
Build the Portfolio Builder backend module. Add models, schemas, repositories, services and FastAPI routes for portfolios and positions. Include portfolio value and position weight calculations. Add unit and API tests.
```

### Suggested commit

```text
feat: add portfolio builder api
```

---

## Issue 23 — Add Portfolio Builder frontend

**Labels:** `frontend`, `portfolio`, `priority-high`  
**Milestone:** `M2 — Market data and portfolio`  
**Suggested branch:** `feature/portfolio-builder-page`

### Goal / Objectif

Create the portfolio management UI.

Créer l’interface de gestion de portefeuille.

### Tasks

- Add Portfolio Builder page.
- Add portfolio selector.
- Add positions table.
- Add add-position form.
- Add allocation chart.
- Add sector exposure placeholder.
- Add currency exposure placeholder.

### Acceptance criteria

- User can view Portfolio Builder page.
- User can see positions.
- User can add a position later through API integration.
- UI is bilingual.

### Suggested commit

```text
feat: add portfolio builder page
```

---

# Phase 3 — Performance, Volatility and Risk  
# Phase 3 — Performance, volatilité et risque

---

## Issue 24 — Add performance analytics backend

**Labels:** `backend`, `quant`, `portfolio`, `priority-high`  
**Milestone:** `M3 — Performance, volatility and risk`  
**Suggested branch:** `feature/performance-analytics-backend`

### Goal / Objectif

Calculate portfolio performance metrics.

Calculer les métriques de performance du portefeuille.

### Tasks

- Total return.
- Annualized return.
- Annualized volatility.
- Sharpe ratio.
- Sortino ratio.
- Max drawdown.
- Beta placeholder.
- Add deterministic tests.

### Acceptance criteria

- Performance service exists.
- Metrics are calculated correctly.
- Tests use deterministic datasets.
- API endpoint returns metrics.

### Codex prompt

```text
Implement performance analytics for Athena AI Risk Terminal. Add total return, annualized return, annualized volatility, Sharpe ratio, Sortino ratio and max drawdown. Keep calculations in domain modules and add deterministic tests.
```

### Suggested commit

```text
feat: add performance analytics backend
```

---

## Issue 25 — Add Performance Analytics frontend

**Labels:** `frontend`, `quant`, `priority-medium`  
**Milestone:** `M3 — Performance, volatility and risk`  
**Suggested branch:** `feature/performance-analytics-page`

### Goal / Objectif

Display portfolio performance.

Afficher la performance du portefeuille.

### Tasks

- Add Performance Analytics page.
- Add metric cards.
- Add portfolio value chart placeholder.
- Add drawdown chart placeholder.
- Add benchmark comparison placeholder.

### Acceptance criteria

- Page exists.
- Metrics display clearly.
- UI is bilingual.
- Loading and error states exist.

### Suggested commit

```text
feat: add performance analytics page
```

---

## Issue 26 — Add volatility analytics backend

**Labels:** `backend`, `quant`, `risk`, `priority-high`  
**Milestone:** `M3 — Performance, volatility and risk`  
**Suggested branch:** `feature/volatility-backend`

### Goal / Objectif

Add volatility calculations.

Ajouter les calculs de volatilité.

### Tasks

- Daily volatility.
- Annualized volatility.
- Rolling volatility.
- Volatility regime classification.
- Tests.

### Acceptance criteria

- Volatility calculations are pure functions.
- Rolling volatility works for configurable windows.
- Tests pass.

### Suggested commit

```text
feat: add volatility analytics backend
```

---

## Issue 27 — Add Volatility Lab frontend

**Labels:** `frontend`, `quant`, `risk`, `priority-medium`  
**Milestone:** `M3 — Performance, volatility and risk`  
**Suggested branch:** `feature/volatility-lab-page`

### Goal / Objectif

Create the Volatility Lab page.

Créer la page Laboratoire de volatilité.

### Tasks

- Add Volatility Lab route.
- Add historical volatility card.
- Add annualized volatility card.
- Add rolling volatility chart.
- Add volatility comparison placeholder.
- Add volatility regime badge.

### Acceptance criteria

- Page exists.
- User can see volatility metrics.
- UI is bilingual.

### Suggested commit

```text
feat: add volatility lab page
```

---

## Issue 28 — Add VaR and CVaR backend

**Labels:** `backend`, `quant`, `risk`, `priority-high`  
**Milestone:** `M3 — Performance, volatility and risk`  
**Suggested branch:** `feature/var-cvar-backend`

### Goal / Objectif

Implement the first real risk engine.

Implémenter le premier vrai moteur de risque.

### Tasks

- Historical VaR.
- Parametric VaR.
- CVaR / Expected Shortfall.
- Loss distribution.
- Tests with deterministic data.
- Ensure outputs are positive loss values.

### Acceptance criteria

- VaR returns positive loss values.
- CVaR returns average tail loss.
- Parametric VaR works.
- Tests pass.

### Codex prompt

```text
Implement a Risk Engine for VaR and CVaR in Athena AI Risk Terminal. Add historical VaR, parametric VaR and Expected Shortfall. Return positive loss values and add deterministic tests.
```

### Suggested commit

```text
feat: add var and cvar risk engine
```

---

## Issue 29 — Add Risk Monitor frontend

**Labels:** `frontend`, `risk`, `priority-high`  
**Milestone:** `M3 — Performance, volatility and risk`  
**Suggested branch:** `feature/risk-monitor-page`

### Goal / Objectif

Display VaR, CVaR and risk information.

Afficher la VaR, la CVaR et les informations de risque.

### Tasks

- Add Risk Monitor page.
- Add VaR card.
- Add CVaR card.
- Add loss distribution chart placeholder.
- Add risk contribution table placeholder.
- Add rolling risk chart placeholder.

### Acceptance criteria

- User can see VaR and CVaR.
- Risk metrics display clearly.
- UI is bilingual.

### Suggested commit

```text
feat: add risk monitor page
```

---

# Phase 4 — Trade Simulation and RiskDNA  
# Phase 4 — Simulation de transactions et RiskDNA

---

## Issue 30 — Add Trade model and schemas

**Labels:** `backend`, `portfolio`, `priority-high`  
**Milestone:** `M4 — Trade simulation and RiskDNA`  
**Suggested branch:** `feature/trade-model`

### Goal / Objectif

Prepare trade data structures.

Préparer les structures de données pour les trades.

### Tasks

- Add Trade model.
- Add Trade schemas.
- Add trade action enum:
  - BUY;
  - SELL.
- Add validation rules.

### Acceptance criteria

- Trade model exists.
- Trade schemas exist.
- Buy and sell actions are supported.
- Invalid trade input is rejected.

### Suggested commit

```text
feat: add trade model and schemas
```

---

## Issue 31 — Add Trade Simulator backend

**Labels:** `backend`, `portfolio`, `risk`, `priority-high`  
**Milestone:** `M4 — Trade simulation and RiskDNA`  
**Suggested branch:** `feature/trade-simulator-backend`

### Goal / Objectif

Simulate a trade and return before/after portfolio impact.

Simuler une transaction et retourner l’impact avant/après sur le portefeuille.

### Tasks

- Add trade simulation service.
- Apply trade to a copy of portfolio.
- Calculate before/after value.
- Calculate before/after weights.
- Calculate before/after exposure.
- Prepare connection to risk service.
- Add tests.

### Acceptance criteria

- API can simulate buy order.
- API can simulate sell order.
- API returns before/after comparison.
- Tests pass.

### Codex prompt

```text
Implement the Trade Simulator backend. Add a service that receives a proposed trade, applies it to a copy of the portfolio, and returns before/after portfolio value, positions, weights and exposure. Keep business logic in services and add tests.
```

### Suggested commit

```text
feat: add trade simulator backend
```

---

## Issue 32 — Add Trade Simulator frontend

**Labels:** `frontend`, `portfolio`, `risk`, `priority-high`  
**Milestone:** `M4 — Trade simulation and RiskDNA`  
**Suggested branch:** `feature/trade-simulator-page`

### Goal / Objectif

Create the trade simulation UI.

Créer l’interface de simulation de transactions.

### Tasks

- Add Trade Simulator page.
- Add trade ticket form.
- Add before/after cards.
- Add allocation delta table.
- Add placeholder RiskDNA panel.
- Add loading/error states.

### Acceptance criteria

- User can open Trade Simulator.
- User can fill trade form.
- Before/after section exists.
- UI is bilingual.

### Suggested commit

```text
feat: add trade simulator page
```

---

## Issue 33 — Add RiskDNA v1 backend

**Labels:** `backend`, `risk`, `ai`, `priority-high`  
**Milestone:** `M4 — Trade simulation and RiskDNA`  
**Suggested branch:** `feature/riskdna-v1-backend`

### Goal / Objectif

Create the first explainable risk score.

Créer le premier score de risque explicable.

### Tasks

- Add RiskDNA service.
- Use VaR usage.
- Use CVaR usage.
- Use concentration risk.
- Use volatility regime.
- Return:
  - Low;
  - Medium;
  - High;
  - Critical.
- Add main drivers.
- Add tests.

### Acceptance criteria

- RiskDNA returns a score.
- Score is explainable.
- Tests cover Low, Medium, High and Critical cases.
- The output includes main risk drivers.

### Codex prompt

```text
Implement RiskDNA v1. Create an explainable scoring service that combines VaR usage, CVaR usage, volatility regime and concentration risk into Low, Medium, High or Critical. Return main drivers and add unit tests.
```

### Suggested commit

```text
feat: add riskdna v1 backend
```

---

## Issue 34 — Add RiskDNA frontend panel

**Labels:** `frontend`, `risk`, `ai`, `priority-high`  
**Milestone:** `M4 — Trade simulation and RiskDNA`  
**Suggested branch:** `feature/riskdna-panel`

### Goal / Objectif

Display RiskDNA clearly in the UI.

Afficher RiskDNA clairement dans l’interface.

### Tasks

- Add RiskDNA card.
- Add score badge.
- Add main drivers list.
- Add recommendation area.
- Add RiskDNA to Dashboard.
- Add RiskDNA to Trade Simulator.

### Acceptance criteria

- RiskDNA appears on Dashboard.
- RiskDNA appears after trade simulation.
- UI is bilingual.
- Score is visually clear.

### Suggested commit

```text
feat: add riskdna panel
```

---

# Phase 5 — Options and Rates  
# Phase 5 — Options et taux

---

## Issue 35 — Add Black-Scholes pricing backend

**Labels:** `backend`, `quant`, `pricing`, `priority-high`  
**Milestone:** `M5 — Options and rates`  
**Suggested branch:** `feature/black-scholes-pricing`

### Goal / Objectif

Price European call and put options.

Pricer les options européennes call et put.

### Tasks

- Add Black-Scholes input schema.
- Add call price.
- Add put price.
- Add d1.
- Add d2.
- Add input validation.
- Add put-call parity test.

### Acceptance criteria

- API returns call and put price.
- Put-call parity test passes.
- Invalid inputs are rejected.

### Codex prompt

```text
Implement Black-Scholes pricing for European call and put options without dividends. Return call price, put price, d1 and d2. Add input validation and tests, including put-call parity.
```

### Suggested commit

```text
feat: add black scholes pricing backend
```

---

## Issue 36 — Add Black-Scholes Greeks backend

**Labels:** `backend`, `quant`, `pricing`, `priority-high`  
**Milestone:** `M5 — Options and rates`  
**Suggested branch:** `feature/black-scholes-greeks`

### Goal / Objectif

Calculate option Greeks.

Calculer les Greeks d’options.

### Tasks

- Add call delta.
- Add put delta.
- Add gamma.
- Add vega.
- Add theta.
- Add rho.
- Add tests.

### Acceptance criteria

- Greeks are returned by service/API.
- Tests cover basic sanity checks.
- Greeks are documented.

### Suggested commit

```text
feat: add black scholes greeks
```

---

## Issue 37 — Add Options Pricing Lab frontend

**Labels:** `frontend`, `quant`, `pricing`, `priority-high`  
**Milestone:** `M5 — Options and rates`  
**Suggested branch:** `feature/options-pricing-lab`

### Goal / Objectif

Create option pricing UI.

Créer l’interface de pricing d’options.

### Tasks

- Add Options Pricing Lab page.
- Add Black-Scholes form.
- Add call price card.
- Add put price card.
- Add Greeks table.
- Add payoff chart placeholder.
- Add put-call parity status.

### Acceptance criteria

- User can enter option parameters.
- User can see call and put prices.
- User can see Greeks.
- UI is bilingual.

### Suggested commit

```text
feat: add options pricing lab page
```

---

## Issue 38 — Add Rates and Bond schemas

**Labels:** `backend`, `quant`, `rates`, `database`, `priority-medium`  
**Milestone:** `M5 — Options and rates`  
**Suggested branch:** `feature/rates-bond-schemas`

### Goal / Objectif

Prepare rates and bonds data structures.

Préparer les structures de données pour les taux et obligations.

### Tasks

- Add YieldCurve schema.
- Add SpotRate schema.
- Add DiscountFactor schema.
- Add Bond schema.
- Add BondValuation schema.
- Add optional database models.

### Acceptance criteria

- Rates schemas exist.
- Bond request/response schemas exist.
- Models are ready for later persistence.

### Suggested commit

```text
feat: add rates and bond schemas
```

---

## Issue 39 — Add bond pricing and rates backend

**Labels:** `backend`, `quant`, `rates`, `priority-high`  
**Milestone:** `M5 — Options and rates`  
**Suggested branch:** `feature/rates-bond-pricing-backend`

### Goal / Objectif

Add rates and bond analytics.

Ajouter l’analyse des taux et des obligations.

### Tasks

- Discount factors.
- Spot rate table.
- Bond cash flows.
- Bond price.
- Duration.
- Rate shock function.
- Tests.

### Acceptance criteria

- Bond price calculator works.
- Discount factors work.
- Duration works.
- +100 bps rate shock works.
- Tests pass.

### Codex prompt

```text
Implement a Rates Lab backend module. Add discount factors from spot rates, coupon bond pricing, cash flow schedule, duration and a +100 bps rate shock function. Keep calculations in domain modules and add deterministic tests.
```

### Suggested commit

```text
feat: add rates and bond pricing backend
```

---

## Issue 40 — Add Rates Lab frontend

**Labels:** `frontend`, `quant`, `rates`, `priority-high`  
**Milestone:** `M5 — Options and rates`  
**Suggested branch:** `feature/rates-lab-page`

### Goal / Objectif

Create UI for yield curves and bonds.

Créer l’interface pour les courbes de taux et obligations.

### Tasks

- Add Rates Lab page.
- Add yield curve chart.
- Add spot rates table.
- Add discount factors table.
- Add bond pricing form.
- Add duration card.
- Add rate shock panel.

### Acceptance criteria

- User can see yield curve.
- User can see spot rates.
- User can price a bond.
- User can run a rate shock.
- UI is bilingual.

### Suggested commit

```text
feat: add rates lab page
```

---

# Phase 6 — Middle Office Workflows  
# Phase 6 — Workflows middle office

---

## Issue 41 — Add Stress Testing backend

**Labels:** `backend`, `risk`, `priority-high`  
**Milestone:** `M6 — Middle office workflows`  
**Suggested branch:** `feature/stress-testing-backend`

### Goal / Objectif

Run stress scenarios on portfolios.

Lancer des scénarios de stress sur les portefeuilles.

### Tasks

- Add stress scenario schemas.
- Add equity crash scenario.
- Add technology selloff scenario.
- Add rate shock scenario.
- Add FX shock scenario.
- Calculate losses by asset.
- Calculate losses by sector.
- Add tests.

### Acceptance criteria

- Stress service exists.
- Standard scenarios work.
- Losses are returned by asset and sector.
- Tests pass.

### Suggested commit

```text
feat: add stress testing backend
```

---

## Issue 42 — Add Stress Testing frontend

**Labels:** `frontend`, `risk`, `priority-medium`  
**Milestone:** `M6 — Middle office workflows`  
**Suggested branch:** `feature/stress-testing-page`

### Goal / Objectif

Create the Stress Testing page.

Créer la page Stress Testing.

### Tasks

- Add Stress Testing page.
- Add scenario selector.
- Add stress loss chart.
- Add sector loss table.
- Add worst contributors table.
- Add AI explanation placeholder.

### Acceptance criteria

- User can select a scenario.
- User can see estimated losses.
- UI is bilingual.

### Suggested commit

```text
feat: add stress testing page
```

---

## Issue 43 — Add Limit Monitoring backend

**Labels:** `backend`, `risk`, `priority-high`  
**Milestone:** `M6 — Middle office workflows`  
**Suggested branch:** `feature/limit-monitoring-backend`

### Goal / Objectif

Detect risk limit breaches.

Détecter les dépassements de limites de risque.

### Tasks

- Add RiskLimit model.
- Add LimitBreach model.
- Add limit checking service.
- Check max VaR.
- Check max CVaR.
- Check max sector exposure.
- Check max single asset exposure.
- Check max option delta.
- Check max option vega.
- Check max duration.
- Add tests.

### Acceptance criteria

- System detects OK / Warning / Breach / Critical.
- Breaches are stored or returned.
- Tests pass.

### Suggested commit

```text
feat: add limit monitoring backend
```

---

## Issue 44 — Add Limit Center frontend

**Labels:** `frontend`, `risk`, `priority-medium`  
**Milestone:** `M6 — Middle office workflows`  
**Suggested branch:** `feature/limit-center-page`

### Goal / Objectif

Create the Limit Center UI.

Créer l’interface du centre des limites.

### Tasks

- Add Limit Center page.
- Add limit usage bars.
- Add breach table.
- Add status badges.
- Add breach history placeholder.

### Acceptance criteria

- User can view limits.
- User can see breaches.
- UI is bilingual.

### Suggested commit

```text
feat: add limit center page
```

---

## Issue 45 — Add P&L Attribution backend

**Labels:** `backend`, `pnl`, `priority-high`  
**Milestone:** `M6 — Middle office workflows`  
**Suggested branch:** `feature/pnl-attribution-backend`

### Goal / Objectif

Explain profit and loss.

Expliquer le P&L.

### Tasks

- Calculate daily P&L.
- Calculate P&L by asset.
- Calculate P&L by sector.
- Add fees.
- Add slippage.
- Add residual unexplained P&L.
- Add tests.

### Acceptance criteria

- P&L by asset works.
- P&L by sector works.
- Residual P&L is returned.
- Tests pass.

### Suggested commit

```text
feat: add pnl attribution backend
```

---

## Issue 46 — Add P&L Attribution frontend

**Labels:** `frontend`, `pnl`, `priority-medium`  
**Milestone:** `M6 — Middle office workflows`  
**Suggested branch:** `feature/pnl-attribution-page`

### Goal / Objectif

Create the P&L Attribution page.

Créer la page d’attribution du P&L.

### Tasks

- Add P&L Attribution page.
- Add daily P&L cards.
- Add waterfall chart placeholder.
- Add asset contribution table.
- Add sector contribution table.
- Add unexplained P&L alert.

### Acceptance criteria

- User can see P&L.
- User can see contribution by asset and sector.
- UI is bilingual.

### Suggested commit

```text
feat: add pnl attribution page
```

---

## Issue 47 — Add Reconciliation backend

**Labels:** `backend`, `pnl`, `priority-medium`  
**Milestone:** `M6 — Middle office workflows`  
**Suggested branch:** `feature/reconciliation-backend`

### Goal / Objectif

Compare expected and actual trades/positions.

Comparer les trades/positions attendus et réels.

### Tasks

- Add reconciliation service.
- Add import trade file placeholder.
- Add import position file placeholder.
- Compare expected vs actual positions.
- Detect missing trades.
- Detect quantity mismatches.
- Detect price mismatches.
- Generate exception list.

### Acceptance criteria

- Reconciliation service exists.
- Mismatches can be detected.
- Exceptions are returned clearly.

### Suggested commit

```text
feat: add reconciliation backend
```

---

## Issue 48 — Add Reconciliation frontend

**Labels:** `frontend`, `pnl`, `priority-low`  
**Milestone:** `M6 — Middle office workflows`  
**Suggested branch:** `feature/reconciliation-page`

### Goal / Objectif

Create the Reconciliation page.

Créer la page Réconciliation.

### Tasks

- Add Reconciliation page.
- Add file upload placeholder.
- Add reconciliation status.
- Add exception table.
- Add export button placeholder.

### Acceptance criteria

- Page exists.
- User can see reconciliation results placeholder.
- UI is bilingual.

### Suggested commit

```text
feat: add reconciliation page
```

---

# Phase 7 — AI and Reports  
# Phase 7 — IA et rapports

---

## Issue 49 — Add AI explanation service

**Labels:** `backend`, `ai`, `priority-high`  
**Milestone:** `M7 — AI and reports`  
**Suggested branch:** `feature/ai-explanation-service`

### Goal / Objectif

Generate clear risk explanations from structured context.

Générer des explications de risque claires à partir d’un contexte structuré.

### Tasks

- Add `ai_service.py`.
- Accept structured risk context.
- Generate English explanation.
- Generate French explanation.
- Add mock mode for tests.
- Ensure AI does not replace calculations.

### Acceptance criteria

- AI service receives structured data.
- AI service returns explanation.
- Mock mode works.
- Tests do not require real API calls.

### Suggested commit

```text
feat: add ai explanation service
```

---

## Issue 50 — Add AI anomaly detection backend

**Labels:** `backend`, `ai`, `risk`, `priority-medium`  
**Milestone:** `M7 — AI and reports`  
**Suggested branch:** `feature/ai-anomaly-backend`

### Goal / Objectif

Detect unusual risk, trade or P&L movements.

Détecter les mouvements inhabituels de risque, trade ou P&L.

### Tasks

- Add Z-score anomaly baseline.
- Add anomaly score.
- Add alert level.
- Add explanation context.
- Add tests.
- Prepare Isolation Forest later.

### Acceptance criteria

- Anomaly score is returned.
- Alert level is returned.
- Tests pass.

### Suggested commit

```text
feat: add ai anomaly detection backend
```

---

## Issue 51 — Add AI Anomaly Center frontend

**Labels:** `frontend`, `ai`, `risk`, `priority-medium`  
**Milestone:** `M7 — AI and reports`  
**Suggested branch:** `feature/ai-anomaly-center`

### Goal / Objectif

Create the AI Anomaly Center page.

Créer la page Centre d’anomalies IA.

### Tasks

- Add AI Anomaly Center page.
- Add anomaly timeline.
- Add anomaly cards.
- Add investigation panel.
- Add confidence indicator.

### Acceptance criteria

- Page exists.
- User can see anomalies.
- UI is bilingual.

### Suggested commit

```text
feat: add ai anomaly center page
```

---

## Issue 52 — Add Reports Center backend

**Labels:** `backend`, `reports`, `priority-high`  
**Milestone:** `M7 — AI and reports`  
**Suggested branch:** `feature/reports-backend`

### Goal / Objectif

Generate structured reports.

Générer des rapports structurés.

### Tasks

- Add report service.
- Add daily risk report.
- Add trade impact report.
- Add options pricing report.
- Add rates report.
- Add P&L report.
- Add JSON output.
- Add CSV output.
- Prepare PDF later.

### Acceptance criteria

- Reports can be generated from structured data.
- At least one report type works.
- Report output is bilingual-ready.

### Suggested commit

```text
feat: add reports center backend
```

---

## Issue 53 — Add Reports Center frontend

**Labels:** `frontend`, `reports`, `priority-high`  
**Milestone:** `M7 — AI and reports`  
**Suggested branch:** `feature/reports-center-page`

### Goal / Objectif

Create the Reports Center UI.

Créer l’interface du centre de rapports.

### Tasks

- Add Reports Center page.
- Add report type selector.
- Add language selector.
- Add report preview.
- Add export buttons.
- Add loading/error states.

### Acceptance criteria

- User can select report type.
- User can select language.
- User can preview report.
- UI is bilingual.

### Suggested commit

```text
feat: add reports center page
```

---

# Phase 8 — Testing, CI/CD and Final Polish  
# Phase 8 — Tests, CI/CD et finition finale

---

## Issue 54 — Add backend linting and formatting

**Labels:** `backend`, `testing`, `devops`, `priority-medium`  
**Milestone:** `M8 — Testing, CI/CD and final polish`  
**Suggested branch:** `chore/backend-linting`

### Goal / Objectif

Improve backend code quality.

Améliorer la qualité du code backend.

### Tasks

- Add Ruff.
- Add Black.
- Add formatting scripts.
- Add linting scripts.
- Document commands.

### Acceptance criteria

- Backend lint command works.
- Backend format check works.
- Documentation explains commands.

### Suggested commit

```text
chore: add backend linting and formatting
```

---

## Issue 55 — Add frontend linting and formatting

**Labels:** `frontend`, `testing`, `devops`, `priority-medium`  
**Milestone:** `M8 — Testing, CI/CD and final polish`  
**Suggested branch:** `chore/frontend-linting`

### Goal / Objectif

Improve frontend code quality.

Améliorer la qualité du code frontend.

### Tasks

- Add ESLint.
- Add Prettier.
- Add TypeScript typecheck.
- Add scripts.
- Document commands.

### Acceptance criteria

- Frontend lint works.
- Frontend format check works.
- Typecheck works.

### Suggested commit

```text
chore: add frontend linting and formatting
```

---

## Issue 56 — Add GitHub Actions CI

**Labels:** `devops`, `testing`, `priority-high`  
**Milestone:** `M8 — Testing, CI/CD and final polish`  
**Suggested branch:** `chore/github-actions-ci`

### Goal / Objectif

Run automated checks on GitHub.

Lancer des vérifications automatiques sur GitHub.

### Tasks

- Add backend test workflow.
- Add frontend test workflow.
- Add backend lint workflow.
- Add frontend lint workflow.
- Add frontend build check.
- Add README badge.

### Acceptance criteria

- GitHub Actions run on push/PR.
- Backend tests run.
- Frontend build runs.
- CI status is visible.

### Suggested commit

```text
ci: add github actions workflow
```

---

## Issue 57 — Add Dockerfiles

**Labels:** `devops`, `backend`, `frontend`, `priority-medium`  
**Milestone:** `M8 — Testing, CI/CD and final polish`  
**Suggested branch:** `chore/dockerfiles`

### Goal / Objectif

Make Docker Compose actually runnable.

Rendre Docker Compose réellement exécutable.

### Tasks

- Add `backend/Dockerfile`.
- Add `frontend/Dockerfile`.
- Update `docker-compose.yml` if needed.
- Test `docker compose up`.

### Acceptance criteria

- Backend container builds.
- Frontend container builds.
- PostgreSQL starts.
- Redis starts.
- `docker compose up` works.

### Suggested commit

```text
chore: add dockerfiles
```

---

## Issue 58 — Add final screenshots and demo script

**Labels:** `documentation`, `priority-medium`  
**Milestone:** `M8 — Testing, CI/CD and final polish`  
**Suggested branch:** `docs/demo-script`

### Goal / Objectif

Prepare the project for presentation.

Préparer le projet pour une présentation.

### Tasks

- Add `docs/demo-script.md`.
- Add screenshots folder.
- Add demo scenario:
  - build portfolio;
  - calculate volatility;
  - calculate VaR/CVaR;
  - simulate trade;
  - view RiskDNA;
  - price option;
  - analyze rates;
  - generate report.

### Acceptance criteria

- Demo script exists.
- Screenshots folder exists.
- Demo flow is clear.

### Suggested commit

```text
docs: add demo script and screenshots guide
```

---

## Issue 59 — Polish final README

**Labels:** `documentation`, `priority-high`  
**Milestone:** `M8 — Testing, CI/CD and final polish`  
**Suggested branch:** `docs/final-readme-polish`

### Goal / Objectif

Make the README strong enough for GitHub, CV and interviews.

Rendre le README assez solide pour GitHub, le CV et les entrevues.

### Tasks

- Add screenshots.
- Add setup instructions.
- Add architecture summary.
- Add feature list.
- Add quant methodology summary.
- Add AI features summary.
- Add testing section.
- Add limitations.
- Add roadmap.
- Add author section.

### Acceptance criteria

- README is polished.
- README explains business value.
- README explains technical value.
- README is understandable by recruiters and technical reviewers.

### Suggested commit

```text
docs: polish final README
```

---

## Issue 60 — Add final project retrospective

**Labels:** `documentation`, `priority-low`  
**Milestone:** `M8 — Testing, CI/CD and final polish`  
**Suggested branch:** `docs/project-retrospective`

### Goal / Objectif

Document what was learned and what could be improved.

Documenter ce qui a été appris et ce qui pourrait être amélioré.

### Tasks

- Add `docs/retrospective.md`.
- Explain what was built.
- Explain technical challenges.
- Explain finance concepts learned.
- Explain limitations.
- Explain next steps.

### Acceptance criteria

- Retrospective exists.
- It can be used for interview preparation.
- It clearly shows learning and maturity.

### Suggested commit

```text
docs: add project retrospective
```

---

# Final Recommended Creation Order / Ordre final recommandé

## Create first / À créer en premier

```text
Issue 1 — Add project README
Issue 2 — Add simple project plan
Issue 3 — Add detailed project plan
Issue 4 — Add architecture documentation
Issue 5 — Add product specification
Issue 6 — Add GitHub issues roadmap
Issue 7 — Add .gitignore
Issue 8 — Add Docker Compose foundation
Issue 9 — Add .env.example
Issue 10 — Create GitHub labels and milestones
```

## Then start implementation / Ensuite commencer l’implémentation

```text
Issue 11 — Initialize backend FastAPI foundation
Issue 12 — Add backend health endpoint tests
Issue 13 — Initialize frontend React TypeScript foundation
Issue 14 — Add AppShell layout
Issue 15 — Add bilingual UI foundation
```

## Core MVP / MVP principal

```text
Issue 18 — Asset and MarketPrice models
Issue 19 — Market Data service and routes
Issue 20 — Market Data frontend page
Issue 21 — Portfolio and Position models
Issue 22 — Portfolio Builder backend
Issue 23 — Portfolio Builder frontend
Issue 24 — Performance analytics backend
Issue 26 — Volatility analytics backend
Issue 28 — VaR and CVaR backend
Issue 31 — Trade Simulator backend
Issue 33 — RiskDNA v1 backend
```

---

# Recommended Branch Pattern / Modèle de branches recommandé

```text
docs/readme
docs/project-plan
docs/architecture
docs/product-spec
chore/gitignore
chore/docker-compose
feature/backend-foundation
feature/frontend-foundation
feature/market-data-api
feature/portfolio-builder-api
feature/risk-engine
feature/trade-simulator
feature/riskdna-v1
feature/options-pricing
feature/rates-lab
feature/reports-center
```

---

# Recommended Commit Pattern / Modèle de commits recommandé

```text
docs: add project README
docs: add simple project plan
docs: add architecture documentation
chore: add gitignore
chore: initialize backend foundation
feat: add market data api
feat: add portfolio builder api
feat: add var and cvar risk engine
feat: add black scholes pricing backend
test: add expected shortfall tests
fix: correct portfolio weight calculation
ci: add github actions workflow
```

---

# Codex Reminder / Rappel Codex

Use this sentence in almost every Codex prompt:

```text
Follow docs/architecture.md. Keep routes thin, put business logic in services, put pure quant calculations in domain modules, add tests, and keep frontend visible text in i18n files.
```

French reminder:

```text
Suis docs/architecture.md. Garde les routes légères, mets la logique métier dans les services, mets les calculs quantitatifs purs dans les modules domain, ajoute des tests, et garde les textes visibles du frontend dans les fichiers i18n.
```
