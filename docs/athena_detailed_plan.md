# Athena AI Risk Terminal — Detailed Project Plan  
# Plan détaillé du projet Athena AI Risk Terminal

**File name / Nom du fichier :** `athena_detailed_plan.md`  
**Repository target / Emplacement recommandé :** `docs/athena_detailed_plan.md`  
**Project / Projet :** Athena AI Risk Terminal  
**Status / Statut :** Complete merged plan with mandatory Quant, Derivatives and Rates extension.  
**Generated / Généré :** 2026-04-29

---

## How to use this document / Comment utiliser ce document

### English

This file is the single reference document for the Athena AI Risk Terminal project. It merges:

1. The original detailed 4-month project plan.
2. The mandatory Quant, Derivatives and Rates extension.

This document should be placed in the repository under:

```text
docs/athena_detailed_plan.md
```

It can be used to create GitHub issues, plan sprints, guide Codex prompts, structure the frontend/backend architecture, and prepare the project for CV, LinkedIn and interviews.

### Français

Ce fichier est le document de référence unique pour le projet Athena AI Risk Terminal. Il fusionne :

1. Le plan détaillé original sur 4 mois.
2. L’extension obligatoire Quant, Options et Taux.

Ce document doit être placé dans le dépôt à l’emplacement suivant :

```text
docs/athena_detailed_plan.md
```

Il peut servir à créer les issues GitHub, organiser les sprints, guider les prompts Codex, structurer l’architecture frontend/backend et préparer le projet pour le CV, LinkedIn et les entrevues.

---

# Part 1 — Main Project Plan  
# Partie 1 — Plan principal du projet

# Athena AI Risk Terminal — Detailed 4-Month Project Plan  
# Terminal de risque Athena AI — Plan de projet détaillé sur 4 mois

**Repository name / Nom du dépôt :** `athena-ai-risk-terminal`  
**Project type / Type de projet :** Bilingual quantitative finance platform mixing front office, middle office, risk management and AI.  
**Main goal / Objectif principal :** Build a serious portfolio project that shows software engineering, quantitative finance, risk control, AI-assisted analysis and professional UI/UX.

---

## 1. Executive Summary / Résumé exécutif

### English

Athena AI Risk Terminal is a bilingual web platform designed to connect front-office investment decisions with middle-office risk controls. The application allows a user to build portfolios, simulate trades, optimize allocations, measure risk, monitor limits, attribute P&L, run stress tests, detect anomalies and generate AI-assisted risk reports.

The project is intentionally ambitious. It is not just a finance dashboard. It is a complete workflow:

1. A front-office user proposes a trade or portfolio allocation.
2. The quant engine calculates performance, risk and portfolio impact.
3. The middle-office layer checks limits, stress losses, anomalies and P&L consistency.
4. The AI layer explains the result in clear French and English.
5. The reporting layer generates professional risk reports.

The signature feature is the **RiskDNA Engine**, a custom module that gives every portfolio and trade an explainable risk fingerprint.

### Français

Athena AI Risk Terminal est une plateforme web bilingue conçue pour relier les décisions d’investissement front office aux contrôles de risque middle office. L’application permet de construire des portefeuilles, simuler des transactions, optimiser des allocations, mesurer le risque, surveiller les limites, attribuer le P&L, lancer des stress tests, détecter des anomalies et générer des rapports de risque assistés par IA.

Le projet est volontairement ambitieux. Ce n’est pas seulement un tableau de bord financier. C’est un workflow complet :

1. Un utilisateur front office propose un trade ou une allocation.
2. Le moteur quantitatif calcule la performance, le risque et l’impact portefeuille.
3. La couche middle office vérifie les limites, les pertes en stress, les anomalies et la cohérence du P&L.
4. La couche IA explique le résultat en français et en anglais.
5. La couche reporting génère des rapports de risque professionnels.

La fonctionnalité signature est le **RiskDNA Engine**, un module personnalisé qui donne à chaque portefeuille et à chaque trade une empreinte de risque explicable.

---

## 2. Project Positioning / Positionnement du projet

### What this project demonstrates / Ce que le projet démontre

| Area | English | Français |
|---|---|---|
| Software engineering | Clean architecture, APIs, database, tests, CI/CD, Docker | Architecture propre, API, base de données, tests, CI/CD, Docker |
| Quant finance | Returns, volatility, VaR, Expected Shortfall, optimization, backtesting | Rendements, volatilité, VaR, Expected Shortfall, optimisation, backtesting |
| Front office | Portfolio construction, trade ideas, strategy testing | Construction de portefeuille, idées de trades, test de stratégies |
| Middle office | Limit monitoring, P&L attribution, reconciliation, audit trail | Suivi des limites, attribution de P&L, réconciliation, audit |
| AI | Risk explanations, anomaly detection, report generation, trade interpretation | Explications de risque, détection d’anomalies, génération de rapports, interprétation de trades |
| UI/UX | Professional bilingual terminal-style interface | Interface professionnelle bilingue style terminal financier |

---

## 3. Target Users / Utilisateurs cibles

### 3.1 Portfolio Manager / Gestionnaire de portefeuille

Needs:
- See portfolio performance.
- Understand exposures.
- Simulate trades.
- Compare current vs optimized allocation.
- Understand risk before executing a decision.

Besoins :
- Voir la performance du portefeuille.
- Comprendre les expositions.
- Simuler des trades.
- Comparer l’allocation actuelle et optimisée.
- Comprendre le risque avant une décision.

### 3.2 Risk Analyst / Analyste risque

Needs:
- Monitor VaR and Expected Shortfall.
- Detect limit breaches.
- Run stress tests.
- Explain risk movements.
- Generate risk reports.

Besoins :
- Suivre la VaR et l’Expected Shortfall.
- Détecter les dépassements de limites.
- Lancer des stress tests.
- Expliquer les variations de risque.
- Générer des rapports de risque.

### 3.3 Middle Office Analyst / Analyste middle office

Needs:
- Reconcile trades and positions.
- Attribute P&L.
- Identify unexplained P&L.
- Maintain an audit trail.
- Produce daily reports.

Besoins :
- Réconcilier trades et positions.
- Attribuer le P&L.
- Identifier le P&L inexpliqué.
- Garder une piste d’audit.
- Produire des rapports journaliers.

### 3.4 Recruiter / Mentor / Interviewer

Needs:
- Quickly understand the business value.
- See screenshots and demo video.
- Read clean documentation.
- See tests and architecture.
- Understand what you personally implemented.

Besoins :
- Comprendre rapidement la valeur métier.
- Voir des captures d’écran et une vidéo démo.
- Lire une documentation claire.
- Voir les tests et l’architecture.
- Comprendre ce que tu as personnellement implémenté.

---

## 4. Core Product Vision / Vision produit centrale

### English one-liner

> A bilingual AI-powered quantitative risk terminal that transforms front-office trade decisions into middle-office risk, P&L and compliance insights.

### Phrase française

> Un terminal quantitatif bilingue propulsé par l’IA qui transforme les décisions de trading front office en analyses de risque, de P&L et de contrôle middle office.

---

## 5. Signature Feature: RiskDNA Engine / Fonctionnalité signature : RiskDNA Engine

### 5.1 Concept

The RiskDNA Engine gives a portfolio or a proposed trade a risk fingerprint.

Le RiskDNA Engine donne à un portefeuille ou à une transaction proposée une empreinte de risque.

### 5.2 Inputs

- Portfolio positions
- Historical returns
- Asset sectors
- Asset currencies
- Benchmark
- Proposed trades
- Risk limits
- Stress scenarios
- Market volatility
- Correlation matrix

### 5.3 Outputs

- RiskDNA score: Low, Medium, High, Critical
- VaR before / after
- Expected Shortfall before / after
- Sector concentration impact
- Single-name concentration impact
- Beta impact
- Drawdown impact
- Stress test loss
- Limit usage
- AI explanation in English and French
- Recommended action

### 5.4 Example output

English:

```text
RiskDNA: High
The proposed trade increases technology exposure from 31% to 47%, exceeding the internal sector limit of 35%. Portfolio VaR increases from 2.1% to 3.4%, mainly driven by NVDA and MSFT concentration. The trade should be reduced or hedged before approval.
```

Français :

```text
RiskDNA : Élevé
La transaction proposée augmente l’exposition au secteur technologique de 31 % à 47 %, ce qui dépasse la limite sectorielle interne de 35 %. La VaR du portefeuille augmente de 2,1 % à 3,4 %, principalement en raison de la concentration sur NVDA et MSFT. La transaction devrait être réduite ou couverte avant validation.
```

### 5.5 RiskDNA formula idea / Idée de formule

RiskDNA can be a weighted score:

```text
RiskDNA Score =
  25% VaR usage
+ 20% Expected Shortfall usage
+ 20% concentration risk
+ 15% stress test loss
+ 10% drawdown risk
+ 10% anomaly score
```

The score must be explainable. Do not make it a black box.

Le score doit être explicable. Il ne doit pas être une boîte noire.

---

## 6. Main Modules / Modules principaux

## 6.1 Authentication and User Profiles / Authentification et profils utilisateurs

### Goal

Create a clean foundation for user roles.

### Roles

- Admin
- Portfolio Manager
- Risk Analyst
- Viewer

### Features

- Login page
- User profile
- Role-based access
- Language preference
- Default currency
- Saved portfolios

### Optional advanced version

- OAuth login
- JWT authentication
- Refresh tokens
- Audit log for user actions

---

## 6.2 Market Data Module / Module données de marché

### Goal

Import, clean, store and serve financial market data.

### Features

- Search assets by ticker.
- Download historical prices.
- Store price history.
- Calculate daily returns.
- Calculate rolling volatility.
- Calculate correlations.
- Display missing data warnings.

### Data fields

```text
Asset:
- id
- symbol
- name
- asset_type
- sector
- currency
- exchange
- country

MarketPrice:
- id
- asset_id
- date
- open
- high
- low
- close
- adjusted_close
- volume
```

### API endpoints

```text
GET /api/assets
GET /api/assets/{symbol}
GET /api/market-data/prices/{symbol}
GET /api/market-data/returns/{symbol}
GET /api/market-data/correlation-matrix
POST /api/market-data/import
```

### UI

Page name:
- English: Market Data
- French: Données de marché

Components:
- Search bar
- Asset table
- Price chart
- Return distribution chart
- Volatility card
- Missing data alert

---

## 6.3 Portfolio Builder / Constructeur de portefeuille

### Goal

Allow the user to create and manage portfolios.

### Features

- Create portfolio.
- Add positions.
- Edit quantities.
- Set benchmark.
- Set base currency.
- View allocation by asset.
- View allocation by sector.
- View allocation by currency.
- Compare current allocation to target allocation.

### Data fields

```text
Portfolio:
- id
- name
- description
- base_currency
- benchmark_symbol
- created_at
- updated_at

Position:
- id
- portfolio_id
- asset_id
- quantity
- average_price
- market_value
- weight
```

### API endpoints

```text
GET /api/portfolios
POST /api/portfolios
GET /api/portfolios/{portfolio_id}
PUT /api/portfolios/{portfolio_id}
DELETE /api/portfolios/{portfolio_id}
POST /api/portfolios/{portfolio_id}/positions
PUT /api/portfolios/{portfolio_id}/positions/{position_id}
DELETE /api/portfolios/{portfolio_id}/positions/{position_id}
```

### UI

Page name:
- English: Portfolio Builder
- French: Construction de portefeuille

Components:
- Portfolio selector
- Position table
- Add position modal
- Allocation pie chart
- Sector exposure heatmap
- Currency exposure card
- Risk summary sidebar

---

## 6.4 Performance Analytics / Analyse de performance

### Goal

Show professional performance metrics.

### Metrics

- Total return
- Annualized return
- Daily volatility
- Annualized volatility
- Sharpe ratio
- Sortino ratio
- Max drawdown
- Calmar ratio
- Beta vs benchmark
- Alpha vs benchmark
- Tracking error
- Information ratio

### API endpoints

```text
GET /api/analytics/performance/{portfolio_id}
GET /api/analytics/drawdown/{portfolio_id}
GET /api/analytics/benchmark-comparison/{portfolio_id}
```

### UI

Page name:
- English: Performance Analytics
- French: Analyse de performance

Components:
- Performance cards
- Portfolio value chart
- Benchmark comparison chart
- Drawdown chart
- Monthly returns heatmap
- Risk-adjusted performance section

---

## 6.5 Portfolio Optimizer / Optimiseur de portefeuille

### Goal

Allow the user to optimize portfolio weights.

### Optimization methods

- Max Sharpe ratio
- Minimum variance
- Risk parity
- Target return
- Target volatility
- Constrained optimization

### Constraints

- Minimum weight per asset
- Maximum weight per asset
- Maximum sector exposure
- Long-only mode
- Cash allocation
- Excluded assets

### API endpoints

```text
POST /api/optimizer/max-sharpe
POST /api/optimizer/min-variance
POST /api/optimizer/risk-parity
POST /api/optimizer/target-return
```

### UI

Page name:
- English: Portfolio Optimizer
- French: Optimiseur de portefeuille

Components:
- Current allocation chart
- Optimized allocation chart
- Constraint panel
- Efficient frontier chart
- Optimization result table
- Apply allocation button

### Advanced idea

Add a “Risk-aware AI explanation”:

English:
```text
The optimizer reduced the concentration in technology and increased exposure to defensive sectors, lowering portfolio volatility from 18.2% to 13.7%.
```

Français :
```text
L’optimiseur a réduit la concentration technologique et augmenté l’exposition aux secteurs défensifs, ce qui diminue la volatilité du portefeuille de 18,2 % à 13,7 %.
```

---

## 6.6 Trade Simulator / Simulateur de transactions

### Goal

Let users simulate trades before execution.

### Trade types

- Buy equity
- Sell equity
- Rebalance weight
- Add ETF
- Reduce sector exposure
- Increase cash

### Input examples

Structured input:

```text
Action: Buy
Symbol: NVDA
Quantity: 50
```

Natural language input:

```text
Increase exposure to US technology by 10% while keeping VaR below 3%.
```

### Outputs

- Portfolio before trade
- Portfolio after trade
- Risk before / after
- Exposure before / after
- Limit impact
- RiskDNA score
- AI explanation
- Approval recommendation

### API endpoints

```text
POST /api/trades/simulate
POST /api/trades/parse-intent
POST /api/trades/approve
GET /api/trades/history
```

### UI

Page name:
- English: Trade Simulator
- French: Simulateur de transactions

Components:
- Trade ticket form
- Natural language trade input
- Before/after risk cards
- Allocation delta table
- RiskDNA panel
- Approval status badge
- Save simulation button

---

## 6.7 Risk Engine / Moteur de risque

### Goal

Calculate portfolio risk metrics.

### Methods

- Historical VaR
- Parametric VaR
- Monte Carlo VaR
- Expected Shortfall
- Rolling volatility
- Correlation matrix
- Beta
- Contribution to risk
- Component VaR
- Marginal VaR

### API endpoints

```text
GET /api/risk/var/{portfolio_id}
GET /api/risk/expected-shortfall/{portfolio_id}
GET /api/risk/contribution/{portfolio_id}
GET /api/risk/correlation/{portfolio_id}
POST /api/risk/recalculate/{portfolio_id}
```

### UI

Page name:
- English: Risk Monitor
- French: Moniteur de risque

Components:
- VaR card
- Expected Shortfall card
- Risk contribution table
- Correlation heatmap
- Loss distribution chart
- Rolling risk chart
- Risk explanation panel

---

## 6.8 Stress Testing / Stress tests

### Goal

Show how the portfolio reacts to crisis scenarios.

### Scenarios

- 2008 Financial Crisis
- COVID selloff
- Tech crash
- Interest rate shock
- Oil shock
- CAD/USD shock
- Custom scenario

### Scenario fields

```text
StressScenario:
- id
- name
- description
- equity_shock
- rate_shock
- fx_shock
- sector_shocks
- created_at
```

### Outputs

- Estimated portfolio loss
- Loss by asset
- Loss by sector
- Limit breach under stress
- Worst contributors
- AI scenario explanation

### API endpoints

```text
GET /api/stress/scenarios
POST /api/stress/run/{portfolio_id}
POST /api/stress/custom-scenario
```

### UI

Page name:
- English: Stress Testing
- French: Tests de résistance

Components:
- Scenario selector
- Shock configuration form
- Stress loss chart
- Sector loss table
- Worst contributors panel
- AI explanation panel

---

## 6.9 Limit Monitoring / Suivi des limites

### Goal

Create a middle-office control center.

### Limits

- Maximum VaR
- Maximum Expected Shortfall
- Maximum single-name exposure
- Maximum sector exposure
- Maximum currency exposure
- Maximum drawdown
- Minimum liquidity score
- Maximum leverage

### Limit states

- OK
- Warning
- Breach
- Critical breach

### API endpoints

```text
GET /api/limits/{portfolio_id}
POST /api/limits
PUT /api/limits/{limit_id}
GET /api/limits/breaches/{portfolio_id}
POST /api/limits/check/{portfolio_id}
```

### UI

Page name:
- English: Limit Center
- French: Centre des limites

Components:
- Limit usage bars
- Breach table
- Alert cards
- Rule editor
- Breach history
- Approval workflow

---

## 6.10 P&L Attribution / Attribution du P&L

### Goal

Explain where profit and loss comes from.

### P&L components

- Market movement
- Asset selection
- Sector allocation
- Currency effect
- Fees
- Slippage
- Residual / unexplained P&L

### API endpoints

```text
GET /api/pnl/daily/{portfolio_id}
GET /api/pnl/attribution/{portfolio_id}
GET /api/pnl/unexplained/{portfolio_id}
```

### UI

Page name:
- English: P&L Attribution
- French: Attribution du P&L

Components:
- Daily P&L card
- P&L waterfall chart
- Asset contribution table
- Sector contribution table
- Unexplained P&L alert
- AI summary

### Example AI explanation

English:
```text
Most of today’s P&L came from semiconductor exposure. NVDA contributed 42% of the daily gain. The residual P&L is low, suggesting that the movement is well explained by market factors.
```

Français :
```text
La majorité du P&L du jour provient de l’exposition aux semi-conducteurs. NVDA représente 42 % du gain quotidien. Le P&L résiduel est faible, ce qui indique que le mouvement est bien expliqué par les facteurs de marché.
```

---

## 6.11 Reconciliation / Réconciliation

### Goal

Simulate middle-office reconciliation between trades, positions and P&L.

### Features

- Import trade file.
- Import position file.
- Compare expected positions vs actual positions.
- Detect missing trades.
- Detect quantity mismatch.
- Detect price mismatch.
- Generate reconciliation report.

### API endpoints

```text
POST /api/reconciliation/import-trades
POST /api/reconciliation/import-positions
POST /api/reconciliation/run
GET /api/reconciliation/exceptions
```

### UI

Page name:
- English: Reconciliation
- French: Réconciliation

Components:
- File upload
- Reconciliation status
- Exception table
- Difference by asset
- Export report button

---

## 6.12 AI Anomaly Detection / Détection d’anomalies par IA

### Goal

Detect unusual trades, risk movements or P&L movements.

### Models

- Z-score baseline
- Isolation Forest
- One-Class SVM
- Simple autoencoder later if time allows

### Inputs

- Trade size
- Historical trade size
- Daily P&L
- Risk metric changes
- Exposure changes
- Limit usage changes

### Outputs

- Anomaly score
- Alert level
- Explanation
- Suggested investigation

### API endpoints

```text
POST /api/ai/anomaly-detection/trades
POST /api/ai/anomaly-detection/pnl
POST /api/ai/anomaly-detection/risk
GET /api/ai/anomaly-detection/history
```

### UI

Page name:
- English: AI Anomaly Center
- French: Centre d’anomalies IA

Components:
- Anomaly timeline
- Anomaly cards
- Investigation panel
- Model confidence indicator
- False positive feedback button

---

## 6.13 AI Risk Report Generator / Générateur de rapports de risque IA

### Goal

Generate clear risk reports in French and English.

### Report types

- Daily risk report
- Weekly portfolio report
- Trade impact report
- Limit breach report
- Stress test report
- P&L attribution report

### Report sections

- Executive summary
- Portfolio overview
- Performance
- Risk metrics
- Limit status
- Stress results
- Main risk drivers
- AI commentary
- Recommended actions

### API endpoints

```text
POST /api/reports/daily-risk
POST /api/reports/trade-impact
POST /api/reports/stress-test
GET /api/reports/history
GET /api/reports/{report_id}/download
```

### UI

Page name:
- English: Reports Center
- French: Centre de rapports

Components:
- Report type selector
- Language selector
- Generate button
- Report preview
- Download PDF
- Download Excel
- Download CSV

---

## 6.14 Bilingual System / Système bilingue

### Goal

Make the application fully bilingual.

### Languages

- English
- French

### Files

```text
frontend/src/i18n/en.json
frontend/src/i18n/fr.json
```

### Example

English:

```json
{
  "dashboard.title": "Risk Dashboard",
  "risk.var": "Value at Risk",
  "trade.simulator": "Trade Simulator"
}
```

French:

```json
{
  "dashboard.title": "Tableau de bord du risque",
  "risk.var": "Valeur à risque",
  "trade.simulator": "Simulateur de transactions"
}
```

### Requirement

No hardcoded UI text in React components. Every visible string must come from the translation system.

---

## 7. UI/UX Vision / Vision interface

## 7.1 General Style

### English

The interface should feel like a modern institutional risk terminal:
- dark mode by default;
- clean sidebar;
- dense but readable data tables;
- professional charts;
- risk badges;
- bilingual switch;
- dashboard cards;
- command/search bar;
- clear alert system.

### Français

L’interface doit ressembler à un terminal de risque institutionnel moderne :
- dark mode par défaut ;
- sidebar propre ;
- tableaux denses mais lisibles ;
- graphiques professionnels ;
- badges de risque ;
- bouton FR/EN ;
- cartes de dashboard ;
- barre de commande/recherche ;
- système d’alertes clair.

---

## 7.2 Main Layout

### Sidebar pages

```text
Dashboard
Market Data
Portfolio Builder
Trade Simulator
Risk Monitor
Stress Testing
Limit Center
P&L Attribution
Reconciliation
AI Anomaly Center
Reports Center
Settings
```

### Top bar

- Portfolio selector
- Date selector
- Language switch
- Theme switch
- Search / command bar
- User profile

### Dashboard cards

- Portfolio Value
- Daily P&L
- VaR 95%
- Expected Shortfall
- RiskDNA Score
- Limit Usage
- Top Risk Contributor
- Unexplained P&L

---

## 8. Technical Architecture / Architecture technique

## 8.1 Recommended Stack

### Frontend

```text
React
TypeScript
Vite
Tailwind CSS
shadcn/ui
Recharts or Plotly
react-i18next
TanStack Query
Zod
```

### Backend

```text
Python
FastAPI
Pydantic
SQLAlchemy
PostgreSQL
Redis
Celery or RQ
Pytest
```

### Quant / AI

```text
pandas
numpy
scipy
scikit-learn
statsmodels
cvxpy
QuantLib optional
OpenAI API optional
```

### DevOps

```text
Docker
docker-compose
GitHub Actions
Ruff
Black
Prettier
ESLint
Pytest coverage
```

---

## 8.2 Backend Clean Architecture

Current backend direction: Athena is migrating progressively from a global
layered backend to feature-owned backend modules. Migrated modules own their
routes, schemas, services, repositories and pure domain calculations under
`backend/app/modules/<module_name>/`.

Current migrated modules:

```text
backend/app/modules/
├── market_data/
│   ├── routes.py
│   ├── schemas.py
│   ├── service.py
│   ├── repository.py
│   └── domain/
├── equity_analysis/
│   ├── routes.py
│   ├── schemas.py
│   ├── service.py
│   ├── repository.py
│   └── domain/
└── portfolio_builder/
    ├── routes.py
    ├── schemas.py
    ├── service.py
    ├── repository.py
    └── domain/
```

Shared backend infrastructure remains centralized:

```text
backend/app/core/
backend/app/database/
backend/app/models/
backend/app/api/dependencies.py
```

The older global folders `api/routes`, `schemas`, `services`, `repositories`
and `domain` are transitional for non-migrated features only. New work on
Market Data, Equity Analysis or Portfolio Builder should use the module folders
above and should not recreate old global files.

Historical/global layout reference:

```text
backend/app/
├── api/
│   ├── routes/
│   └── dependencies.py
├── core/
│   ├── config.py
│   ├── security.py
│   └── logging.py
├── database/
│   ├── session.py
│   └── migrations/
├── domain/
│   ├── portfolios/
│   ├── trades/
│   ├── risk/
│   ├── pnl/
│   └── reports/
├── services/
│   ├── market_data_service.py
│   ├── portfolio_service.py
│   ├── risk_service.py
│   ├── optimizer_service.py
│   ├── pnl_service.py
│   ├── ai_service.py
│   └── report_service.py
├── repositories/
│   ├── portfolio_repository.py
│   ├── asset_repository.py
│   └── trade_repository.py
├── schemas/
│   ├── portfolio_schema.py
│   ├── trade_schema.py
│   ├── risk_schema.py
│   └── report_schema.py
└── tests/
```

---

## 8.3 Frontend Architecture

```text
frontend/src/
├── app/
│   ├── router.tsx
│   └── providers.tsx
├── components/
│   ├── layout/
│   ├── charts/
│   ├── tables/
│   ├── forms/
│   └── ui/
├── features/
│   ├── dashboard/
│   ├── market-data/
│   ├── portfolio/
│   ├── trade-simulator/
│   ├── risk-monitor/
│   ├── stress-testing/
│   ├── limits/
│   ├── pnl/
│   ├── reconciliation/
│   ├── ai-anomalies/
│   └── reports/
├── i18n/
│   ├── en.json
│   └── fr.json
├── lib/
│   ├── api-client.ts
│   ├── formatters.ts
│   └── validators.ts
└── types/
```

---

## 9. Data Model / Modèle de données

## 9.1 Main tables

```text
users
assets
market_prices
portfolios
positions
trades
risk_metrics
risk_limits
limit_breaches
stress_scenarios
stress_results
pnl_records
reconciliation_runs
reconciliation_exceptions
ai_anomalies
reports
audit_events
```

## 9.2 Important relationships

```text
User 1 --- N Portfolio
Portfolio 1 --- N Position
Asset 1 --- N Position
Portfolio 1 --- N Trade
Portfolio 1 --- N RiskMetric
Portfolio 1 --- N PnLRecord
Portfolio 1 --- N LimitBreach
Portfolio 1 --- N Report
```

---

## 10. API Design / Conception API

## 10.1 API groups

```text
/api/health
/api/auth
/api/assets
/api/market-data
/api/portfolios
/api/trades
/api/analytics
/api/risk
/api/stress
/api/limits
/api/pnl
/api/reconciliation
/api/ai
/api/reports
/api/audit
```

## 10.2 Example API response

```json
{
  "portfolio_id": "pf_001",
  "risk_date": "2026-04-28",
  "var_95": 0.023,
  "expected_shortfall_95": 0.041,
  "riskdna_score": "Medium",
  "limit_status": "Warning",
  "main_driver": "Technology concentration"
}
```

---

## 11. Testing Strategy / Stratégie de tests

## 11.1 Backend tests

- Unit tests for risk calculations.
- Unit tests for portfolio calculations.
- Unit tests for optimizer constraints.
- API tests for endpoints.
- Database repository tests.
- Service tests with mocked repositories.
- AI service tests with mocked model responses.

## 11.2 Frontend tests

- Component rendering tests.
- Form validation tests.
- Language switch tests.
- Dashboard display tests.
- API error state tests.

## 11.3 Quant tests

Important calculations must be tested with known small examples:

- daily returns;
- portfolio weights;
- VaR;
- Expected Shortfall;
- drawdown;
- Sharpe ratio;
- P&L attribution.

## 11.4 CI pipeline

```text
Backend:
- install dependencies
- run ruff
- run black check
- run pytest
- generate coverage

Frontend:
- install dependencies
- run eslint
- run typecheck
- run tests
- build app
```

---

## 12. GitHub Strategy / Stratégie GitHub

## 12.1 Branches

```text
main
dev
feature/backend-foundation
feature/frontend-foundation
feature/market-data
feature/portfolio-builder
feature/risk-engine
feature/trade-simulator
feature/riskdna-engine
feature/reports-center
docs/project-plan
```

## 12.2 Commit format

```text
feat: add portfolio risk summary endpoint
fix: correct historical var calculation
docs: add risk methodology documentation
test: add unit tests for expected shortfall
chore: configure docker compose
refactor: split risk service into calculators
```

## 12.3 Pull request template

```md
## Summary
Describe what this PR changes.

## Type of change
- [ ] Feature
- [ ] Fix
- [ ] Refactor
- [ ] Documentation
- [ ] Test

## Screenshots
Add screenshots if UI changed.

## Tests
Explain what was tested.

## Risk
Mention any known limitations.
```

---

# 13. Four-Month Roadmap / Roadmap sur 4 mois

---

## Month 1 — Foundation and First Visual Demo  
## Mois 1 — Fondation et première démo visuelle

### Week 1 — Repository, architecture and project setup

#### Goals

- Create GitHub repository.
- Add bilingual README.
- Add Docker setup.
- Create FastAPI backend.
- Create React frontend.
- Add project documentation.
- Add initial GitHub issues.

#### Tasks

- Create repo `athena-ai-risk-terminal`.
- Add `README.md`.
- Add `docs/project-plan.md`.
- Add `docs/architecture.md`.
- Add `docs/product-spec.md`.
- Initialize backend.
- Initialize frontend.
- Add `.gitignore`.
- Add `docker-compose.yml`.
- Add GitHub Actions skeleton.
- Create issue labels:
  - `frontend`
  - `backend`
  - `quant`
  - `risk`
  - `ai`
  - `documentation`
  - `good first issue`
  - `priority-high`

#### Deliverable

A clean repository that starts locally.

#### Codex prompt

```text
Create the initial monorepo structure for a project called Athena AI Risk Terminal. Use a backend folder with FastAPI and a frontend folder with React TypeScript Vite. Add a docker-compose.yml for backend, frontend, PostgreSQL and Redis. Add a professional bilingual README skeleton in English and French.
```

---

### Week 2 — Market data foundation

#### Goals

- Create asset model.
- Create price model.
- Import historical prices.
- Display first price chart.

#### Tasks

- Add SQLAlchemy models for Asset and MarketPrice.
- Add market data service.
- Add endpoint to retrieve historical prices.
- Add endpoint to calculate returns.
- Add frontend page `Market Data`.
- Add line chart for price history.
- Add basic error handling.

#### Deliverable

The app can show historical prices for selected symbols.

#### Codex prompt

```text
Implement a Market Data module in the FastAPI backend. Add SQLAlchemy models for Asset and MarketPrice, Pydantic schemas, repository functions, and API routes to list assets and retrieve historical prices by symbol. Include pytest unit tests for the service layer.
```

---

### Week 3 — Portfolio builder

#### Goals

- Create portfolios.
- Add positions.
- Calculate portfolio value and weights.

#### Tasks

- Add Portfolio model.
- Add Position model.
- Add CRUD endpoints.
- Add portfolio calculation service.
- Add frontend Portfolio Builder page.
- Add Add Position modal.
- Add allocation chart.
- Add position table.

#### Deliverable

A user can build a portfolio manually.

#### Codex prompt

```text
Build the Portfolio Builder module. Implement backend models, schemas, repositories, services and FastAPI routes for portfolios and positions. On the frontend, create a Portfolio Builder page with a position table, add-position modal and allocation chart. Use TypeScript types and keep all visible text ready for i18n.
```

---

### Week 4 — Dashboard and bilingual UI

#### Goals

- Make the app look serious.
- Add language switch.
- Add dashboard cards.
- Add sidebar layout.

#### Tasks

- Add dark terminal-style layout.
- Add sidebar navigation.
- Add top bar.
- Add FR/EN translation files.
- Add dashboard cards:
  - Portfolio Value
  - Daily P&L
  - VaR 95%
  - Expected Shortfall
  - RiskDNA Score
  - Limit Usage
- Add placeholder charts.

#### Deliverable

A visually impressive first demo.

#### Codex prompt

```text
Create a professional dark-mode financial terminal UI in React TypeScript. Add sidebar navigation, top bar, dashboard cards, bilingual i18n support with English and French JSON files, and placeholder charts using Recharts. Do not hardcode visible text inside components.
```

---

## Month 2 — Front Office Quant Features  
## Mois 2 — Fonctionnalités quant front office

### Week 5 — Performance analytics

#### Goals

- Calculate performance metrics.
- Show benchmark comparison.

#### Tasks

- Implement returns calculation.
- Implement volatility.
- Implement Sharpe ratio.
- Implement Sortino ratio.
- Implement max drawdown.
- Implement beta vs benchmark.
- Add performance API endpoints.
- Add Performance Analytics page.

#### Deliverable

The portfolio has professional performance analytics.

#### Codex prompt

```text
Implement performance analytics for a portfolio. Add functions for total return, annualized return, annualized volatility, Sharpe ratio, Sortino ratio, max drawdown and beta versus benchmark. Add API endpoints and tests with small deterministic datasets.
```

---

### Week 6 — Portfolio optimizer

#### Goals

- Add optimization methods.
- Compare current vs optimized allocation.

#### Tasks

- Add max Sharpe optimizer.
- Add minimum variance optimizer.
- Add simple risk parity.
- Add constraints:
  - max asset weight;
  - max sector weight;
  - long-only.
- Add optimizer page.
- Add efficient frontier chart if possible.

#### Deliverable

The app can suggest optimized allocations.

#### Codex prompt

```text
Build a portfolio optimization service using scipy or cvxpy. Implement max Sharpe, minimum variance and simple risk parity optimization with long-only constraints and maximum weight constraints. Return optimized weights, expected return, volatility and Sharpe ratio. Add tests.
```

---

### Week 7 — Strategy Lab and backtesting

#### Goals

- Add basic strategy backtesting.
- Show strategy vs benchmark.

#### Tasks

- Add Strategy model.
- Implement momentum strategy.
- Implement moving average crossover.
- Add transaction costs.
- Add backtest results.
- Add Strategy Lab page.
- Add equity curve chart.
- Add drawdown chart.

#### Deliverable

The user can backtest a strategy.

#### Codex prompt

```text
Create a Strategy Lab module. Implement a simple momentum strategy and a moving average crossover strategy. Add a backtesting engine that calculates equity curve, drawdown, total return, volatility, Sharpe ratio and transaction costs. Add API routes and frontend charts.
```

---

### Week 8 — Trade simulator

#### Goals

- Simulate trades before execution.
- Show before/after impact.

#### Tasks

- Create Trade model.
- Add structured trade input.
- Add before/after portfolio calculation.
- Add before/after exposures.
- Add before/after risk placeholders.
- Add Trade Simulator page.
- Add save simulation feature.

#### Deliverable

The user can simulate trades and see portfolio impact.

#### Codex prompt

```text
Implement a Trade Simulator module. Add a backend endpoint that receives a proposed trade, applies it to a copy of the portfolio, and returns before/after positions, weights, sector exposures and portfolio value. Add a React page with a trade ticket form and before/after comparison cards.
```

---

## Month 3 — Middle Office, Risk and AI  
## Mois 3 — Middle office, risque et IA

### Week 9 — VaR and Expected Shortfall

#### Goals

- Implement core risk metrics.
- Make risk calculations reliable.

#### Tasks

- Historical VaR.
- Parametric VaR.
- Expected Shortfall.
- Loss distribution.
- Rolling VaR.
- Tests for risk calculations.
- Risk Monitor page.

#### Deliverable

The project has a serious risk engine.

#### Codex prompt

```text
Implement a Risk Engine for portfolio VaR and Expected Shortfall. Add historical VaR, parametric VaR and Expected Shortfall using portfolio returns. Add risk contribution by asset if possible. Include unit tests with deterministic return series and document the methodology.
```

---

### Week 10 — Stress testing

#### Goals

- Add crisis scenarios.
- Show estimated stress losses.

#### Tasks

- Create StressScenario model.
- Add standard scenarios:
  - 2008 crisis;
  - COVID selloff;
  - technology crash;
  - interest rate shock;
  - FX shock.
- Add custom scenario input.
- Add stress result table.
- Add stress loss chart.

#### Deliverable

The user can run stress scenarios.

#### Codex prompt

```text
Create a Stress Testing module. Add predefined scenarios with shocks by sector, asset class and currency. Implement a service that applies scenario shocks to portfolio positions and returns estimated losses by asset and sector. Add API routes, tests and a frontend scenario page.
```

---

### Week 11 — Limit monitoring

#### Goals

- Create middle-office limit controls.
- Detect breaches automatically.

#### Tasks

- Create RiskLimit model.
- Create LimitBreach model.
- Add limit rules:
  - max single asset exposure;
  - max sector exposure;
  - max VaR;
  - max Expected Shortfall;
  - max drawdown.
- Add limit check service.
- Add Limit Center page.
- Add breach history.

#### Deliverable

The system flags risk breaches like a middle-office tool.

#### Codex prompt

```text
Build a Limit Monitoring module. Create risk limit and breach models, implement a service that checks a portfolio against limits, and return OK, Warning, Breach or Critical status. Add a frontend Limit Center with usage bars, breach table and history.
```

---

### Week 12 — RiskDNA Engine and AI explanations

#### Goals

- Build the signature feature.
- Add AI-generated explanations in both languages.

#### Tasks

- Implement RiskDNA scoring.
- Combine:
  - VaR usage;
  - Expected Shortfall usage;
  - concentration risk;
  - stress loss;
  - drawdown;
  - anomaly score.
- Add AI explanation service.
- Add English/French output.
- Add RiskDNA panel in dashboard and trade simulator.

#### Deliverable

The project now has a unique, memorable feature.

#### Codex prompt

```text
Implement the RiskDNA Engine. Create a service that combines risk metrics, concentration metrics, stress test results and limit usage into an explainable score: Low, Medium, High or Critical. Return the score, numerical drivers, and a plain-language explanation in English and French. Add tests for scoring rules.
```

---

## Month 4 — Professional Finish  
## Mois 4 — Finition professionnelle

### Week 13 — P&L attribution

#### Goals

- Explain daily P&L.
- Add middle-office credibility.

#### Tasks

- Add PnLRecord model.
- Calculate daily P&L by position.
- Calculate P&L by sector.
- Add fees/slippage field.
- Add unexplained P&L.
- Add P&L Attribution page.
- Add waterfall chart.

#### Deliverable

The project can explain profit and loss.

#### Codex prompt

```text
Implement a P&L Attribution module. Calculate portfolio P&L by asset and sector using position quantities and price changes. Include fees, slippage and residual unexplained P&L. Add API routes, tests and a frontend waterfall chart.
```

---

### Week 14 — Reconciliation and Reports Center

#### Goals

- Add real middle-office workflow.
- Generate professional reports.

#### Tasks

- Add file upload for trades and positions.
- Compare expected vs actual positions.
- Detect mismatches.
- Add Reports Center.
- Generate PDF risk report.
- Generate CSV/Excel exports.
- Add bilingual report templates.

#### Deliverable

The app can produce real-looking operational reports.

#### Codex prompt

```text
Create a Reports Center module. Generate bilingual daily risk reports and trade impact reports from portfolio, risk, limit and P&L data. Add PDF export and CSV export. Include a report preview page in React.
```

---

### Week 15 — Testing, CI/CD and code quality

#### Goals

- Make the project credible.
- Add automated checks.

#### Tasks

- Increase backend test coverage.
- Add frontend tests.
- Add GitHub Actions.
- Add linting.
- Add formatting.
- Add type checks.
- Add Docker build check.
- Add coverage badge.
- Fix technical debt.

#### Deliverable

A professional repository with reliable CI.

#### Codex prompt

```text
Improve code quality across the repository. Add GitHub Actions for backend tests, frontend tests, linting, formatting and build checks. Add missing unit tests for risk, portfolio, optimizer and API modules. Fix failing tests and update the README with CI instructions.
```

---

### Week 16 — Final demo and portfolio packaging

#### Goals

- Prepare the project for LinkedIn, CV and interviews.

#### Tasks

- Add screenshots.
- Add demo video script.
- Add final README.
- Add architecture diagram.
- Add methodology documentation.
- Add “What I learned” section.
- Add “Business relevance” section.
- Add “Limitations and next steps” section.
- Create LinkedIn post.
- Create CV bullet points.

#### Deliverable

The project is ready to show publicly.

#### Codex prompt

```text
Polish the repository for a portfolio presentation. Improve the README, add a project overview, architecture section, screenshots placeholders, demo script, setup instructions, feature list, business relevance section, limitations and next steps. Keep the tone professional and bilingual.
```

---

# 14. What I can help with in Codex / Comment je peux t’aider avec Codex

## 14.1 What Codex can help with

Based on OpenAI’s current product information, Codex can help with software engineering tasks such as writing features, answering questions about a codebase, fixing bugs and proposing pull requests. ChatGPT can also connect to GitHub repositories to analyze live repository content. Codex can also be used for GitHub code reviews and suggested fixes when configured.

## 14.2 How I can help you use Codex effectively

I can help you in five main ways:

### 1. Turn the project plan into GitHub issues

Example issues:

```text
Issue 1: Set up FastAPI backend foundation
Issue 2: Set up React TypeScript frontend foundation
Issue 3: Implement Market Data module
Issue 4: Implement Portfolio Builder
Issue 5: Implement Historical VaR and Expected Shortfall
Issue 6: Implement Trade Simulator
Issue 7: Implement RiskDNA Engine
Issue 8: Implement Reports Center
```

### 2. Write precise Codex prompts

Bad prompt:

```text
Make my app better.
```

Good prompt:

```text
Implement a FastAPI service for historical VaR calculation. The function should accept a list of portfolio returns and a confidence level, return the VaR as a positive loss number, include input validation, and include pytest tests with deterministic data.
```

### 3. Review Codex outputs

When Codex generates code, I can help you check:

- Is the architecture clean?
- Are services separated from routes?
- Are there tests?
- Are calculations correct?
- Is the code too complicated?
- Is the UI clean?
- Is the naming professional?
- Is the bilingual system respected?

### 4. Debug errors

You can send me:

- terminal errors;
- failing tests;
- screenshots;
- code snippets;
- PR diffs.

I can help you understand and correct them.

### 5. Prepare PR review instructions

Example:

```text
Review this PR like a senior software engineer. Focus on architecture, test quality, separation of concerns, type safety, security and maintainability. Suggest concrete improvements without rewriting unrelated code.
```

---

# 15. Codex Workflow / Workflow avec Codex

## Recommended workflow

```text
1. Create one GitHub issue.
2. Ask Codex to implement only that issue.
3. Let Codex create a branch or propose changes.
4. Run tests.
5. Ask Codex to fix failures.
6. Ask me to review the code or PR.
7. Merge only when clean.
8. Move to the next issue.
```

## Rule

Do not ask Codex to build the entire project in one prompt.  
Ask Codex to build one module at a time.

Ne demande pas à Codex de construire tout le projet en une seule demande.  
Demande-lui de construire un module à la fois.

---

# 16. First 10 GitHub Issues / 10 premières issues GitHub

## Issue 1 — Project setup

```md
## Goal
Initialize the monorepo with backend, frontend, Docker and documentation.

## Tasks
- Create backend folder with FastAPI.
- Create frontend folder with React TypeScript Vite.
- Add docker-compose.
- Add README skeleton.
- Add docs folder.
- Add health check endpoint.
- Add basic frontend landing page.

## Acceptance criteria
- `docker compose up` starts the project.
- Backend health endpoint returns OK.
- Frontend loads successfully.
```

## Issue 2 — Bilingual UI foundation

```md
## Goal
Add English/French internationalization.

## Tasks
- Add i18n library.
- Create en.json and fr.json.
- Add language switch.
- Replace hardcoded visible strings.

## Acceptance criteria
- User can switch between English and French.
- Dashboard title changes language.
```

## Issue 3 — Market data module

```md
## Goal
Create market data backend and first frontend page.

## Tasks
- Add Asset model.
- Add MarketPrice model.
- Add routes for assets and prices.
- Add Market Data page.
- Add price chart.

## Acceptance criteria
- User can select an asset and see a price chart.
```

## Issue 4 — Portfolio Builder

```md
## Goal
Allow users to create portfolios and positions.

## Tasks
- Add Portfolio and Position models.
- Add CRUD endpoints.
- Add portfolio value calculation.
- Add Portfolio Builder UI.

## Acceptance criteria
- User can create a portfolio and add positions.
```

## Issue 5 — Performance Analytics

```md
## Goal
Calculate portfolio performance metrics.

## Tasks
- Add return calculation.
- Add volatility.
- Add Sharpe ratio.
- Add max drawdown.
- Add performance page.

## Acceptance criteria
- User can see performance metrics for a portfolio.
```

## Issue 6 — Risk Engine

```md
## Goal
Implement VaR and Expected Shortfall.

## Tasks
- Historical VaR.
- Parametric VaR.
- Expected Shortfall.
- Risk endpoint.
- Tests.

## Acceptance criteria
- Risk calculations are tested with deterministic examples.
```

## Issue 7 — Trade Simulator

```md
## Goal
Simulate trades and show before/after impact.

## Tasks
- Add Trade model.
- Add simulate trade endpoint.
- Add before/after portfolio calculation.
- Add Trade Simulator UI.

## Acceptance criteria
- User can simulate a buy or sell order and see portfolio impact.
```

## Issue 8 — Limit Center

```md
## Goal
Monitor risk limits and breaches.

## Tasks
- Add RiskLimit model.
- Add LimitBreach model.
- Add limit checking service.
- Add Limit Center UI.

## Acceptance criteria
- System detects a sector exposure breach.
```

## Issue 9 — RiskDNA Engine

```md
## Goal
Create the signature explainable risk score.

## Tasks
- Combine VaR, ES, concentration, stress loss and limit usage.
- Return Low, Medium, High or Critical score.
- Add explanation.
- Add dashboard widget.

## Acceptance criteria
- RiskDNA score changes after a risky trade simulation.
```

## Issue 10 — Reports Center

```md
## Goal
Generate bilingual risk reports.

## Tasks
- Add report templates.
- Add PDF export.
- Add report preview UI.
- Add daily risk report.

## Acceptance criteria
- User can generate an English or French PDF report.
```

---

# 17. Learning Roadmap / Plan d’apprentissage

## Month 1 learning

- FastAPI basics
- React TypeScript basics
- Docker basics
- PostgreSQL basics
- Clean architecture
- GitHub project management

## Month 2 learning

- Portfolio theory
- Returns and volatility
- Sharpe ratio
- Optimization
- Backtesting
- Front-office workflow

## Month 3 learning

- VaR
- Expected Shortfall
- Stress testing
- Limit monitoring
- AI anomaly detection
- Explainable risk scoring

## Month 4 learning

- P&L attribution
- Reconciliation
- Report generation
- Testing
- CI/CD
- Portfolio presentation

---

# 18. README Structure / Structure du README final

```md
# Athena AI Risk Terminal

## Overview
## Résumé en français
## Demo
## Screenshots
## Features
## Business Context
## Architecture
## Tech Stack
## Quant Methodology
## AI Features
## Installation
## Usage
## Testing
## Roadmap
## What I Learned
## Limitations
## License
```

---

# 19. CV Bullets / Points CV

## English

```text
Developed Athena AI Risk Terminal, a bilingual quantitative finance platform combining front-office portfolio construction, trade simulation, VaR, Expected Shortfall, stress testing, limit monitoring, P&L attribution and AI-generated risk explanations.
```

```text
Built a custom RiskDNA Engine to evaluate the risk impact of proposed trades by combining VaR usage, Expected Shortfall, concentration risk, stress losses and anomaly detection into an explainable risk score.
```

```text
Designed a full-stack architecture using React, TypeScript, FastAPI, PostgreSQL, Docker and automated tests to simulate institutional risk and portfolio management workflows.
```

## Français

```text
Développement d’Athena AI Risk Terminal, une plateforme financière quantitative bilingue combinant construction de portefeuille, simulation de transactions, VaR, Expected Shortfall, stress tests, suivi des limites, attribution du P&L et explications de risque générées par IA.
```

```text
Création d’un moteur RiskDNA évaluant l’impact risque des transactions proposées à partir de la VaR, de l’Expected Shortfall, de la concentration, des stress losses et de la détection d’anomalies.
```

```text
Conception d’une architecture full-stack avec React, TypeScript, FastAPI, PostgreSQL, Docker et tests automatisés pour simuler des workflows institutionnels de gestion de portefeuille et de risque.
```

---

# 20. LinkedIn Post / Publication LinkedIn

## English

```text
I am building Athena AI Risk Terminal, a bilingual quantitative finance platform designed to connect front-office portfolio decisions with middle-office risk controls.

The platform includes portfolio construction, trade simulation, VaR, Expected Shortfall, stress testing, limit monitoring, P&L attribution, anomaly detection and AI-generated risk explanations.

The goal is to combine software engineering, quantitative finance and risk management into one professional full-stack project.
```

## Français

```text
Je développe Athena AI Risk Terminal, une plateforme financière quantitative bilingue conçue pour relier les décisions de portefeuille front office aux contrôles de risque middle office.

La plateforme inclut la construction de portefeuille, la simulation de transactions, la VaR, l’Expected Shortfall, les stress tests, le suivi des limites, l’attribution du P&L, la détection d’anomalies et des explications de risque générées par IA.

L’objectif est de combiner génie logiciel, finance quantitative et gestion du risque dans un projet full-stack professionnel.
```

---

# 21. Minimum Viable Version / Version minimale viable

If the full project is too heavy, the minimum version should include:

Si le projet complet est trop lourd, la version minimale doit contenir :

```text
1. Bilingual dashboard
2. Portfolio Builder
3. Market Data page
4. Performance metrics
5. Historical VaR
6. Expected Shortfall
7. Trade Simulator
8. RiskDNA score
9. AI explanation
10. PDF report
```

This is already strong enough for interviews.

Cette version est déjà assez forte pour des entrevues.

---

# 22. Advanced Version / Version avancée

If time allows:

Si le temps le permet :

```text
1. Monte Carlo VaR
2. Options pricing
3. Fixed income duration risk
4. FX risk
5. Risk parity optimizer
6. Reconciliation engine
7. Anomaly detection with Isolation Forest
8. AI natural language trade parser
9. GitHub PR review automation with Codex
10. Deployed public demo
```

---

# 23. Important Rule / Règle importante

This project must not become a random AI chatbot.

Ce projet ne doit pas devenir un simple chatbot IA.

The correct structure is:

```text
Quant engine = calculates
Middle office engine = controls
AI layer = explains, detects, summarizes
Frontend = makes everything usable and impressive
```

La bonne structure est :

```text
Moteur quantitatif = calcule
Moteur middle office = contrôle
Couche IA = explique, détecte, résume
Frontend = rend le tout utilisable et impressionnant
```

---

# 24. Official References / Références officielles

- OpenAI Codex overview: https://openai.com/index/introducing-codex/
- Connecting GitHub to ChatGPT: https://help.openai.com/en/articles/11145903-connecting-github-to-chatgpt
- ChatGPT release notes mentioning Codex GitHub code reviews: https://help.openai.com/en/articles/6825453-chatgpt-release-notes
- FastAPI documentation: https://fastapi.tiangolo.com/
- React TypeScript documentation: https://react.dev/learn/typescript
- QuantLib project: https://www.quantlib.org/
- OpenBB documentation: https://docs.openbb.co/

---

# Part 2 — Mandatory Quant, Derivatives and Rates Extension  
# Partie 2 — Extension obligatoire Quant, Options et Taux

# Athena AI Risk Terminal — Quant, Derivatives and Rates Extension  
# Extension Quant, Options et Taux pour Athena AI Risk Terminal

**Status / Statut :** Mandatory extension to the existing Athena AI Risk Terminal project.  
**Important / Important :** This document does not replace the original project. It extends it.

---

## 1. Purpose of this Extension / Objectif de cette extension

### English

This extension adds a deeper quantitative finance layer to Athena AI Risk Terminal. The project already includes portfolio construction, VaR, Expected Shortfall, trade simulation, P&L attribution, stress testing and RiskDNA. This document makes the project stronger by adding:

1. A clearer Value at Risk and Conditional VaR methodology.
2. A full volatility learning and analytics module.
3. A derivatives pricing module for European call and put options.
4. A first Black-Scholes pricer with Greeks.
5. A rates and fixed-income module covering yield curves, spot rates, discount factors and bond pricing.
6. New UI pages, backend services, API endpoints, tests and Codex prompts.

### Français

Cette extension ajoute une couche de finance quantitative plus profonde à Athena AI Risk Terminal. Le projet existant inclut déjà la construction de portefeuille, la VaR, l’Expected Shortfall, la simulation de transactions, l’attribution du P&L, les stress tests et RiskDNA. Ce document renforce le projet en ajoutant :

1. Une méthodologie plus claire sur la Value at Risk et la Conditional VaR.
2. Un module complet sur la volatilité.
3. Un module de pricing de produits dérivés pour les options européennes call et put.
4. Un premier pricer Black-Scholes avec Greeks.
5. Un module taux/fixed income avec yield curves, spot rates, discount factors et pricing obligataire.
6. De nouvelles pages UI, services backend, endpoints API, tests et prompts Codex.

---

# 2. Mini Course — Value at Risk and Conditional VaR  
# Mini cours — Value at Risk et Conditional VaR

## 2.1 What is Value at Risk? / C’est quoi la Value at Risk ?

### English

Value at Risk, usually written VaR, answers this question:

> What is the maximum loss I should expect not to exceed over a given horizon, with a given confidence level?

Example:

```text
1-day VaR 95% = $100,000
```

Meaning:

```text
With 95% confidence, the portfolio should not lose more than $100,000 in one day.
```

Equivalently:

```text
There is a 5% probability that the loss will be worse than $100,000.
```

### Français

La Value at Risk, souvent appelée VaR, répond à cette question :

> Quelle est la perte maximale que je ne devrais pas dépasser sur un horizon donné, avec un niveau de confiance donné ?

Exemple :

```text
VaR 1 jour à 95 % = 100 000 $
```

Cela veut dire :

```text
Avec 95 % de confiance, le portefeuille ne devrait pas perdre plus de 100 000 $ en une journée.
```

Autrement dit :

```text
Il existe 5 % de probabilité que la perte soit pire que 100 000 $.
```

---

## 2.2 Historical VaR / VaR historique

### Idea

Use historical portfolio returns and take the loss percentile.

### Steps

1. Compute daily portfolio returns.
2. Convert returns into losses.
3. Sort losses.
4. Pick the 95% or 99% quantile.

### Formula idea

If portfolio return is:

```text
r_t
```

Then loss is:

```text
L_t = -r_t
```

The 95% VaR is:

```text
VaR_95 = quantile(L, 0.95)
```

### In the project

Backend service:

```text
backend/app/risk/historical_var.py
```

Function:

```python
def historical_var(returns: list[float], confidence_level: float = 0.95) -> float:
    losses = [-r for r in returns]
    return quantile(losses, confidence_level)
```

UI card:

```text
Historical VaR 95%
VaR historique 95 %
```

---

## 2.3 Parametric VaR / VaR paramétrique

### Idea

Assume returns are normally distributed.

### Formula

```text
VaR = -(mu - z_alpha * sigma)
```

Where:

```text
mu = average return
sigma = volatility
z_alpha = normal distribution quantile
```

At 95%, the one-sided z-score is approximately:

```text
1.645
```

### In the project

Use this as a second method to compare with historical VaR.

UI:

```text
VaR Method:
- Historical
- Parametric
- Monte Carlo later
```

---

## 2.4 Conditional VaR / CVaR / Expected Shortfall

### English

Conditional VaR, also called Expected Shortfall, answers:

> If the loss is worse than VaR, what is the average loss in that bad tail?

Example:

```text
VaR 95% = $100,000
CVaR 95% = $160,000
```

Meaning:

```text
In the worst 5% of cases, the average loss is $160,000.
```

### Français

La Conditional VaR, aussi appelée Expected Shortfall, répond à cette question :

> Si la perte dépasse la VaR, quelle est la perte moyenne dans cette mauvaise zone ?

Exemple :

```text
VaR 95 % = 100 000 $
CVaR 95 % = 160 000 $
```

Cela veut dire :

```text
Dans les 5 % des pires scénarios, la perte moyenne est de 160 000 $.
```

### Formula

```text
CVaR_alpha = E[L | L >= VaR_alpha]
```

### In the project

Backend service:

```text
backend/app/risk/expected_shortfall.py
```

Function:

```python
def expected_shortfall(returns: list[float], confidence_level: float = 0.95) -> float:
    losses = sorted([-r for r in returns])
    var = historical_var(returns, confidence_level)
    tail_losses = [loss for loss in losses if loss >= var]
    return sum(tail_losses) / len(tail_losses)
```

---

## 2.5 Why VaR is not enough / Pourquoi la VaR ne suffit pas

### Weakness of VaR

VaR tells where the danger zone begins, but not how bad the losses are inside the danger zone.

### Example

Portfolio A:

```text
VaR 95% = $100,000
CVaR 95% = $120,000
```

Portfolio B:

```text
VaR 95% = $100,000
CVaR 95% = $400,000
```

Both have the same VaR, but Portfolio B is much more dangerous.

### Project use

RiskDNA must use both VaR and CVaR:

```text
RiskDNA should penalize portfolios where CVaR is much larger than VaR.
```

---

# 3. Mini Course — Volatility  
# Mini cours — Volatilité

## 3.1 What is volatility? / C’est quoi la volatilité ?

### English

Volatility measures how much returns move around their average. In finance, volatility is often used as a proxy for risk.

A stock that moves from +5% to -6% to +4% is more volatile than a bond that moves from +0.1% to -0.2% to +0.1%.

### Français

La volatilité mesure à quel point les rendements bougent autour de leur moyenne. En finance, elle est souvent utilisée comme approximation du risque.

Une action qui fait +5 %, -6 %, +4 % est plus volatile qu’une obligation qui fait +0,1 %, -0,2 %, +0,1 %.

---

## 3.2 Daily volatility / Volatilité journalière

Formula:

```text
sigma_daily = standard_deviation(daily_returns)
```

---

## 3.3 Annualized volatility / Volatilité annualisée

For daily returns, annualized volatility is usually:

```text
sigma_annual = sigma_daily * sqrt(252)
```

Because there are approximately 252 trading days in a year.

---

## 3.4 Rolling volatility / Volatilité roulante

Rolling volatility calculates volatility over a moving window.

Example:

```text
20-day rolling volatility
60-day rolling volatility
252-day rolling volatility
```

Project UI:

```text
Volatility Lab
- 20D volatility
- 60D volatility
- 252D volatility
- Rolling chart
```

---

## 3.5 Realized vs implied volatility / Volatilité réalisée vs implicite

### Realized volatility

Calculated from historical market returns.

### Implied volatility

Extracted from option prices. It is the volatility input that makes Black-Scholes output the observed market option price.

### Project use

In the first version:

```text
Use realized volatility as input for Black-Scholes.
```

Later advanced version:

```text
Add implied volatility solver.
```

---

# 4. Mini Course — Option Pricing: Call and Put  
# Mini cours — Pricing d’options : call et put

## 4.1 What is an option? / C’est quoi une option ?

An option is a derivative contract. Its value depends on an underlying asset such as a stock or ETF.

Une option est un produit dérivé. Sa valeur dépend d’un actif sous-jacent comme une action ou un ETF.

---

## 4.2 Call option

### English

A call option gives the buyer the right, but not the obligation, to buy the underlying asset at a fixed strike price before or at maturity.

### Français

Une option call donne à l’acheteur le droit, mais pas l’obligation, d’acheter l’actif sous-jacent à un prix d’exercice fixé avant ou à l’échéance.

### Payoff at maturity

```text
Call payoff = max(S_T - K, 0)
```

Where:

```text
S_T = underlying price at maturity
K = strike price
```

Example:

```text
S_T = 120
K = 100
Call payoff = max(120 - 100, 0) = 20
```

---

## 4.3 Put option

### English

A put option gives the buyer the right, but not the obligation, to sell the underlying asset at a fixed strike price before or at maturity.

### Français

Une option put donne à l’acheteur le droit, mais pas l’obligation, de vendre l’actif sous-jacent à un prix d’exercice fixé avant ou à l’échéance.

### Payoff at maturity

```text
Put payoff = max(K - S_T, 0)
```

Example:

```text
S_T = 80
K = 100
Put payoff = max(100 - 80, 0) = 20
```

---

## 4.4 Option value components

An option price has two main components:

```text
Option price = intrinsic value + time value
```

### Intrinsic value

For a call:

```text
max(S - K, 0)
```

For a put:

```text
max(K - S, 0)
```

### Time value

The extra value coming from uncertainty and remaining time.

More time and more volatility usually mean a more expensive option.

---

# 5. Mini Course — Black-Scholes  
# Mini cours — Black-Scholes

## 5.1 Purpose

Black-Scholes is a model used to price European call and put options.

A European option can only be exercised at maturity.

---

## 5.2 Inputs

```text
S = current underlying price
K = strike price
T = time to maturity in years
r = risk-free rate
sigma = volatility
q = dividend yield, optional
```

---

## 5.3 Black-Scholes formulas without dividends

```text
d1 = [ln(S/K) + (r + 0.5*sigma^2)T] / [sigma*sqrt(T)]
d2 = d1 - sigma*sqrt(T)
```

Call price:

```text
C = S*N(d1) - K*exp(-rT)*N(d2)
```

Put price:

```text
P = K*exp(-rT)*N(-d2) - S*N(-d1)
```

Where:

```text
N(x) = standard normal cumulative distribution function
```

---

## 5.4 Put-call parity

For European options without dividends:

```text
C - P = S - K*exp(-rT)
```

This is very useful for testing your implementation.

---

## 5.5 First Black-Scholes pricer to include in the project

File:

```text
backend/app/pricing/black_scholes.py
```

Starter code:

```python
from dataclasses import dataclass
from math import erf, exp, log, sqrt


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))


@dataclass(frozen=True)
class BlackScholesInput:
    spot: float
    strike: float
    time_to_maturity: float
    risk_free_rate: float
    volatility: float


@dataclass(frozen=True)
class BlackScholesOutput:
    call_price: float
    put_price: float
    d1: float
    d2: float


def black_scholes_price(params: BlackScholesInput) -> BlackScholesOutput:
    S = params.spot
    K = params.strike
    T = params.time_to_maturity
    r = params.risk_free_rate
    sigma = params.volatility

    if S <= 0:
        raise ValueError("spot must be positive")
    if K <= 0:
        raise ValueError("strike must be positive")
    if T <= 0:
        raise ValueError("time_to_maturity must be positive")
    if sigma <= 0:
        raise ValueError("volatility must be positive")

    d1 = (log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)

    call_price = S * normal_cdf(d1) - K * exp(-r * T) * normal_cdf(d2)
    put_price = K * exp(-r * T) * normal_cdf(-d2) - S * normal_cdf(-d1)

    return BlackScholesOutput(
        call_price=call_price,
        put_price=put_price,
        d1=d1,
        d2=d2,
    )
```

---

# 6. Mini Course — Black-Scholes Greeks  
# Mini cours — Greeks Black-Scholes

Greeks measure how sensitive the option price is to inputs.

Les Greeks mesurent la sensibilité du prix d’une option à ses paramètres.

---

## 6.1 Delta

Delta measures sensitivity to the underlying price.

Call delta:

```text
Delta_call = N(d1)
```

Put delta:

```text
Delta_put = N(d1) - 1
```

Interpretation:

```text
If call delta = 0.60, then a $1 increase in the stock increases the call price by about $0.60.
```

---

## 6.2 Gamma

Gamma measures how fast Delta changes when the underlying price changes.

```text
Gamma = N'(d1) / (S*sigma*sqrt(T))
```

Where:

```text
N'(x) = standard normal density
```

High Gamma means Delta changes quickly.

---

## 6.3 Vega

Vega measures sensitivity to volatility.

```text
Vega = S*N'(d1)*sqrt(T)
```

If Vega is high, the option price is very sensitive to changes in volatility.

---

## 6.4 Theta

Theta measures sensitivity to time passing.

Usually, long options have negative theta because time value decays.

---

## 6.5 Rho

Rho measures sensitivity to the risk-free rate.

---

## 6.6 Greeks module in the project

File:

```text
backend/app/pricing/black_scholes_greeks.py
```

Functions:

```text
calculate_delta
calculate_gamma
calculate_vega
calculate_theta
calculate_rho
```

UI:

```text
Options Pricing Lab
- Inputs: S, K, T, r, sigma
- Output: Call price, Put price
- Greeks: Delta, Gamma, Vega, Theta, Rho
- Payoff chart
- Sensitivity charts
```

---

# 7. Mini Course — Bonds, Yield Curves and Spot Rates  
# Mini cours — Obligations, yield curves et spot rates

## 7.1 What is a bond? / C’est quoi une obligation ?

A bond is a debt instrument. The investor lends money and receives coupons plus the face value at maturity.

Une obligation est un instrument de dette. L’investisseur prête de l’argent et reçoit des coupons plus la valeur nominale à l’échéance.

---

## 7.2 Bond price

A bond price is the present value of future cash flows.

```text
Bond price = sum(CF_t / (1 + y)^t)
```

Where:

```text
CF_t = cash flow at time t
y = yield to maturity
```

For a coupon bond:

```text
Price = C/(1+y)^1 + C/(1+y)^2 + ... + (C+Face)/(1+y)^n
```

---

## 7.3 Yield curve

A yield curve shows interest rates by maturity.

Example:

```text
1Y rate = 3.5%
2Y rate = 3.7%
5Y rate = 4.0%
10Y rate = 4.2%
```

Typical shapes:

```text
Normal curve: long rates > short rates
Inverted curve: short rates > long rates
Flat curve: similar rates across maturities
```

Project UI:

```text
Rates Lab
- Yield curve chart
- Maturity selector
- Spot rate table
- Discount factor table
```

---

## 7.4 Spot rates

A spot rate is the zero-coupon rate for a specific maturity.

Example:

```text
2-year spot rate = rate used to discount a cash flow paid exactly in 2 years.
```

If the 2-year spot rate is 4%:

```text
Discount factor = 1 / (1 + 0.04)^2
```

---

## 7.5 Discount factors

Discount factors convert future cash flows into present value.

```text
DF(t) = 1 / (1 + s_t)^t
```

Where:

```text
s_t = spot rate for maturity t
```

Then:

```text
Present Value = Future Cash Flow * DF(t)
```

---

## 7.6 Bootstrapping idea

Bootstrapping means building spot rates from market bond prices.

Simple logic:

1. Use the 1-year zero-coupon bond to get the 1-year spot rate.
2. Use the 2-year coupon bond and the 1-year spot rate to solve the 2-year spot rate.
3. Continue maturity by maturity.

This is advanced, but perfect for a serious project.

---

## 7.7 Duration

Duration measures bond price sensitivity to interest rates.

Simplified intuition:

```text
Longer duration = more sensitive to rate changes.
```

If rates go up, bond prices usually go down.

Project use:

```text
Rate shock stress test:
+100 bps parallel shift
Estimated bond portfolio loss
```

---

# 8. New Modules to Add to Athena  
# Nouveaux modules à ajouter à Athena

## 8.1 Volatility Lab

### Page name

```text
Volatility Lab / Laboratoire de volatilité
```

### Features

- Historical volatility.
- Annualized volatility.
- Rolling volatility.
- Volatility comparison between assets.
- Volatility used in VaR.
- Volatility used in Black-Scholes.
- Volatility regime detection:
  - Low volatility;
  - Normal volatility;
  - High volatility;
  - Crisis volatility.

### Backend folder

```text
backend/app/volatility/
```

### Frontend folder

```text
frontend/src/features/volatility-lab/
```

### API endpoints

```text
GET /api/volatility/{symbol}/historical
GET /api/volatility/{symbol}/rolling
GET /api/volatility/{symbol}/annualized
GET /api/volatility/portfolio/{portfolio_id}
```

---

## 8.2 Options Pricing Lab

### Page name

```text
Options Pricing Lab / Laboratoire de pricing d’options
```

### Features

- European call price.
- European put price.
- Black-Scholes d1 and d2.
- Delta, Gamma, Vega, Theta, Rho.
- Payoff diagram.
- Option value vs volatility chart.
- Option value vs time to maturity chart.
- Put-call parity check.
- Export pricing report.

### Backend folder

```text
backend/app/pricing/
```

### Frontend folder

```text
frontend/src/features/options-pricing/
```

### API endpoints

```text
POST /api/pricing/black-scholes
POST /api/pricing/black-scholes/greeks
POST /api/pricing/put-call-parity-check
```

### Example request

```json
{
  "spot": 100,
  "strike": 105,
  "time_to_maturity": 0.5,
  "risk_free_rate": 0.04,
  "volatility": 0.25
}
```

### Example response

```json
{
  "call_price": 5.17,
  "put_price": 8.10,
  "d1": 0.02,
  "d2": -0.16,
  "delta_call": 0.51,
  "delta_put": -0.49,
  "gamma": 0.022,
  "vega": 28.1,
  "theta_call": -8.4,
  "rho_call": 23.7
}
```

---

## 8.3 Rates Lab

### Page name

```text
Rates Lab / Laboratoire des taux
```

### Features

- Yield curve display.
- Spot rate table.
- Discount factor table.
- Bond cash flow schedule.
- Bond pricing.
- Yield to maturity estimate.
- Duration.
- Convexity later.
- Rate shock stress test.

### Backend folder

```text
backend/app/rates/
```

### Frontend folder

```text
frontend/src/features/rates-lab/
```

### API endpoints

```text
GET /api/rates/yield-curve
POST /api/rates/discount-factors
POST /api/rates/bond-price
POST /api/rates/duration
POST /api/rates/rate-shock
```

### Example bond request

```json
{
  "face_value": 1000,
  "coupon_rate": 0.05,
  "maturity_years": 5,
  "payments_per_year": 2,
  "yield_to_maturity": 0.04
}
```

---

# 9. Updated Repository Structure / Structure du repo mise à jour

```text
athena-risk-terminal/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── data/
│   │   ├── models/
│   │   ├── portfolios/
│   │   ├── trades/
│   │   ├── risk/
│   │   ├── volatility/
│   │   ├── pricing/
│   │   ├── rates/
│   │   ├── pnl/
│   │   ├── reports/
│   │   └── audit/
│   ├── tests/
│   │   ├── test_var.py
│   │   ├── test_expected_shortfall.py
│   │   ├── test_volatility.py
│   │   ├── test_black_scholes.py
│   │   ├── test_greeks.py
│   │   └── test_bond_pricing.py
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── features/
│   │   │   ├── dashboard/
│   │   │   ├── portfolio/
│   │   │   ├── trade-simulator/
│   │   │   ├── risk-monitor/
│   │   │   ├── volatility-lab/
│   │   │   ├── options-pricing/
│   │   │   ├── rates-lab/
│   │   │   ├── pnl/
│   │   │   ├── reports/
│   │   │   └── settings/
│   │   ├── i18n/
│   │   └── lib/
│   └── package.json
│
├── docs/
│   ├── architecture.md
│   ├── product-spec.md
│   ├── risk-methodology.md
│   ├── derivatives-methodology.md
│   ├── rates-methodology.md
│   ├── quant-derivatives-rates-extension.md
│   ├── screenshots/
│   └── demo-script.md
│
├── notebooks/
│   ├── 01_market_data.ipynb
│   ├── 02_portfolio_optimization.ipynb
│   ├── 03_var_expected_shortfall.ipynb
│   ├── 04_strategy_backtest.ipynb
│   ├── 05_black_scholes_options.ipynb
│   ├── 06_volatility_lab.ipynb
│   └── 07_bonds_yield_curve_spot_rates.ipynb
│
├── docker-compose.yml
├── README.md
└── LICENSE
```

---

# 10. Updated UI Navigation / Navigation UI mise à jour

```text
Dashboard
Market Data
Portfolio Builder
Trade Simulator
Performance Analytics
Risk Monitor
Volatility Lab
Options Pricing Lab
Rates Lab
Stress Testing
Limit Center
P&L Attribution
Reconciliation
Reports Center
Settings
```

---

# 11. Updated 4-Month Roadmap / Roadmap 4 mois mise à jour

## Month 1

No major change. Keep original foundation.

Add:

```text
Create placeholder pages for Volatility Lab, Options Pricing Lab and Rates Lab.
```

---

## Month 2

### Week 5 — Performance and Volatility

Add to the original performance analytics week:

```text
- historical volatility;
- annualized volatility;
- rolling volatility;
- volatility comparison;
- volatility chart.
```

Deliverable:

```text
Performance Analytics + Volatility Lab v1.
```

---

### Week 6 — Portfolio Optimizer

Keep original plan.

Add:

```text
- volatility as risk input;
- risk contribution by asset;
- optimizer comparison using volatility and CVaR.
```

---

### Week 7 — Backtesting

Keep original plan.

Add:

```text
- volatility overlay on strategy performance;
- drawdown and rolling VaR chart.
```

---

### Week 8 — Trade Simulator + Options Pricing v1

Extend original Trade Simulator.

Add:

```text
- Black-Scholes call/put pricer;
- options trade ticket;
- call/put payoff diagram;
- put-call parity check;
- first Greeks.
```

Deliverable:

```text
Trade Simulator + Options Pricing Lab v1.
```

---

## Month 3

### Week 9 — VaR, CVaR and risk engine

Keep original week 9.

Add:

```text
- explicit CVaR module;
- comparison between VaR and CVaR;
- tail loss chart;
- risk methodology documentation.
```

---

### Week 10 — Stress Testing + Rates v1

Keep original stress testing.

Add:

```text
- rate shock scenario;
- yield curve page;
- spot rate table;
- bond price calculator;
- discount factor calculator.
```

Deliverable:

```text
Stress Testing + Rates Lab v1.
```

---

### Week 11 — Limit Monitoring

Keep original plan.

Add new limits:

```text
- max option delta exposure;
- max option vega exposure;
- max rate duration exposure;
- max CVaR / VaR ratio.
```

---

### Week 12 — RiskDNA Engine v2

Extend RiskDNA.

RiskDNA must now include:

```text
- VaR score;
- CVaR score;
- volatility score;
- concentration score;
- option Greeks score;
- rate duration score;
- stress loss score.
```

---

## Month 4

### Week 13 — P&L Attribution + Greeks P&L

Keep original plan.

Add:

```text
- option P&L approximation using Greeks;
- delta effect;
- gamma effect;
- vega effect;
- theta decay.
```

---

### Week 14 — Reports Center

Keep original plan.

Add reports:

```text
- Options pricing report;
- Volatility report;
- Rates report;
- Bond valuation report.
```

---

### Week 15 — Testing and Quality

Add required tests:

```text
- Black-Scholes put-call parity test;
- Greeks sanity checks;
- VaR/CVaR deterministic tests;
- bond pricing tests;
- discount factor tests.
```

---

### Week 16 — Demo

Add demo scenario:

```text
1. Build equity portfolio.
2. Calculate volatility.
3. Simulate equity trade.
4. Calculate VaR and CVaR.
5. Price a protective put.
6. Show how the put changes downside risk.
7. Apply a rate shock to bond holdings.
8. Generate final bilingual risk report.
```

---

# 12. New GitHub Issues / Nouvelles issues GitHub

## Issue — Add Volatility Lab

```md
## Goal
Add a volatility analytics module.

## Tasks
- Implement daily volatility.
- Implement annualized volatility.
- Implement rolling volatility.
- Add API endpoints.
- Add Volatility Lab UI.
- Add tests.

## Acceptance criteria
- User can select an asset and see 20D, 60D and 252D rolling volatility.
```

---

## Issue — Add Black-Scholes Pricer

```md
## Goal
Implement Black-Scholes pricing for European call and put options.

## Tasks
- Add Black-Scholes input schema.
- Add call price.
- Add put price.
- Add d1 and d2.
- Add validation.
- Add API endpoint.
- Add tests using put-call parity.

## Acceptance criteria
- API returns call and put price.
- Put-call parity test passes.
```

---

## Issue — Add Black-Scholes Greeks

```md
## Goal
Calculate first option Greeks.

## Tasks
- Delta.
- Gamma.
- Vega.
- Theta.
- Rho.
- API endpoint.
- UI cards.
- Unit tests.

## Acceptance criteria
- Options Pricing Lab displays price and Greeks.
```

---

## Issue — Add Rates Lab

```md
## Goal
Add a fixed-income and rates module.

## Tasks
- Add yield curve model.
- Add spot rate table.
- Add discount factor calculator.
- Add bond pricing service.
- Add rate shock calculator.
- Add Rates Lab UI.

## Acceptance criteria
- User can price a coupon bond and apply a +100 bps rate shock.
```

---

## Issue — Upgrade RiskDNA v2

```md
## Goal
Extend RiskDNA to include derivatives and rates risk.

## Tasks
- Add CVaR score.
- Add volatility score.
- Add option Greeks score.
- Add duration score.
- Add rate shock score.
- Update explanation generator.

## Acceptance criteria
- RiskDNA explains equity, option and bond risks in English and French.
```

---

# 13. Codex Prompts / Prompts Codex

## 13.1 VaR and CVaR

```text
Implement a Python risk module for Athena AI Risk Terminal. Add functions for historical VaR, parametric VaR and Expected Shortfall / Conditional VaR. The functions should accept portfolio returns and a confidence level. Return positive loss values. Add pytest tests with deterministic examples and edge-case validation.
```

---

## 13.2 Volatility Lab

```text
Create a volatility analytics module. Implement daily volatility, annualized volatility using sqrt(252), and rolling volatility for configurable windows. Add FastAPI endpoints and a React TypeScript Volatility Lab page with charts for 20D, 60D and 252D rolling volatility. Keep all UI text ready for English/French i18n.
```

---

## 13.3 Black-Scholes pricer

```text
Implement a Black-Scholes pricing module for European call and put options without dividends. Add input validation for spot, strike, maturity and volatility. Return call price, put price, d1 and d2. Add a FastAPI endpoint and pytest tests, including a put-call parity test.
```

---

## 13.4 Black-Scholes Greeks

```text
Extend the Black-Scholes module with Greeks: call delta, put delta, gamma, vega, theta and rho. Add unit tests for basic sanity checks. Add a React Options Pricing Lab page that displays call price, put price, d1, d2 and Greeks in clean cards.
```

---

## 13.5 Rates Lab

```text
Create a Rates Lab module for Athena AI Risk Terminal. Implement discount factors from spot rates, coupon bond pricing, yield curve display data, duration calculation and a rate shock function. Add FastAPI endpoints, pytest tests and a React TypeScript Rates Lab page with a yield curve chart and bond pricing form.
```

---

# 14. How this makes the project stronger / Pourquoi ça rend le projet plus fort

### Before

The project was already strong because it had:

```text
Portfolio construction
Trade simulation
VaR / Expected Shortfall
Stress testing
P&L attribution
RiskDNA
Reports
```

### After

Now the project becomes much more impressive because it also has:

```text
Volatility analytics
Options pricing
Black-Scholes
Greeks
Yield curves
Spot rates
Bond pricing
Rate risk
Cross-asset risk
```

This makes Athena look less like a simple portfolio dashboard and more like a real multi-asset risk terminal.

Cela transforme Athena en vrai terminal multi-actifs : actions, options, obligations, taux, risque, P&L et reporting.

---

# 15. Interview Pitch / Pitch entretien

## English

```text
I extended Athena AI Risk Terminal with a quantitative derivatives and rates layer. The platform now includes VaR, Conditional VaR, volatility analytics, Black-Scholes option pricing, Greeks, yield curves, spot rates and bond pricing. The goal was to connect front-office trade decisions with middle-office risk controls across equities, options and fixed income.
```

## Français

```text
J’ai étendu Athena AI Risk Terminal avec une couche quantitative dédiée aux dérivés et aux taux. La plateforme inclut maintenant la VaR, la Conditional VaR, l’analyse de volatilité, le pricing d’options Black-Scholes, les Greeks, les yield curves, les spot rates et le pricing obligataire. L’objectif était de relier les décisions front office aux contrôles middle office sur plusieurs classes d’actifs : actions, options et obligations.
```

---

# 16. Final Rule / Règle finale

These modifications are now mandatory in the project plan.

Ces modifications sont maintenant obligatoires dans le plan du projet.

The project must include:

```text
1. VaR and CVaR
2. Volatility Lab
3. Black-Scholes call/put pricer
4. Greeks
5. Options Pricing Lab
6. Yield curve module
7. Spot rates
8. Bond pricing
9. Rate shock stress test
10. RiskDNA v2 including equity, options and rates risk
```

---

# Final Integrated Vision / Vision finale intégrée

## English

Athena AI Risk Terminal is now a bilingual, AI-assisted, multi-asset quantitative risk platform. It combines:

- front-office portfolio construction;
- trade simulation;
- portfolio optimization;
- performance analytics;
- VaR and Conditional VaR;
- volatility analytics;
- option pricing with Black-Scholes;
- Greeks;
- yield curves and spot rates;
- bond pricing;
- rate shock stress testing;
- limit monitoring;
- P&L attribution;
- reconciliation;
- AI anomaly detection;
- AI-generated risk reports;
- the RiskDNA v2 explainable risk engine.

The project should be positioned as a serious bridge between software engineering, quantitative finance, front office decision-making and middle office risk control.

## Français

Athena AI Risk Terminal devient maintenant une plateforme quantitative multi-actifs, bilingue et assistée par IA. Elle combine :

- construction de portefeuille front office ;
- simulation de transactions ;
- optimisation de portefeuille ;
- analyse de performance ;
- VaR et Conditional VaR ;
- analyse de volatilité ;
- pricing d’options avec Black-Scholes ;
- Greeks ;
- yield curves et spot rates ;
- pricing obligataire ;
- stress tests de taux ;
- suivi des limites ;
- attribution du P&L ;
- réconciliation ;
- détection d’anomalies par IA ;
- rapports de risque générés par IA ;
- moteur RiskDNA v2 explicable.

Le projet doit être présenté comme un pont sérieux entre génie logiciel, finance quantitative, décisions front office et contrôle du risque middle office.

---

# Recommended Commit / Commit recommandé

```text
docs: add merged detailed plan for Athena AI Risk Terminal
```

# Recommended GitHub Issue / Issue GitHub recommandée

```md
## Goal
Add the complete Athena AI Risk Terminal detailed project plan.

## Tasks
- Add `docs/athena_detailed_plan.md`.
- Include the main project roadmap.
- Include the Quant, Derivatives and Rates extension.
- Use this file as the reference for future issues and Codex prompts.

## Acceptance criteria
- The repository contains one complete detailed plan.
- The plan includes front office, middle office, AI, VaR/CVaR, volatility, options, Black-Scholes, Greeks, yield curves, spot rates and bond pricing.
```



