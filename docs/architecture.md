# Athena AI Risk Terminal — Architecture Documentation  
# Documentation d’architecture — Athena AI Risk Terminal

**Recommended file path / Emplacement recommandé :** `docs/architecture.md`  
**Project / Projet :** Athena AI Risk Terminal  
**Purpose / Objectif :** define a stable full-stack architecture before implementation.  
**Objectif :** définir une architecture full-stack stable avant le développement.

---

# 1. Architecture Goal / Objectif de l’architecture

## English

Athena AI Risk Terminal must be built as a clean, modular and scalable financial platform.  
The architecture must support:

- front-office workflows;
- middle-office controls;
- quantitative risk calculations;
- option pricing;
- rates and bond analytics;
- AI-assisted explanations;
- bilingual user interface;
- auditability;
- testing;
- future deployment.

The goal is not only to make the application work, but to make it look like a serious software engineering and quantitative finance project.

## Français

Athena AI Risk Terminal doit être construit comme une plateforme financière propre, modulaire et évolutive.  
L’architecture doit supporter :

- les workflows front office ;
- les contrôles middle office ;
- les calculs de risque quantitatif ;
- le pricing d’options ;
- l’analyse des taux et des obligations ;
- les explications assistées par IA ;
- l’interface bilingue ;
- l’auditabilité ;
- les tests ;
- le déploiement futur.

Le but n’est pas seulement de faire fonctionner l’application, mais de montrer un vrai niveau de génie logiciel et de finance quantitative.

---

# 2. High-Level Architecture / Architecture globale

## English

The application follows a classic full-stack architecture:

```text
Frontend React/TypeScript
        ↓
REST API FastAPI
        ↓
Services layer
        ↓
Domain logic / Quant engines
        ↓
Repositories
        ↓
PostgreSQL database
```

Additional components:

```text
Redis
Celery or RQ workers
AI provider
Market data provider
PDF/CSV report generator
```

## Français

L’application suit une architecture full-stack classique :

```text
Frontend React/TypeScript
        ↓
API REST FastAPI
        ↓
Couche services
        ↓
Logique métier / moteurs quantitatifs
        ↓
Repositories
        ↓
Base PostgreSQL
```

Composants additionnels :

```text
Redis
Workers Celery ou RQ
Fournisseur IA
Fournisseur de données de marché
Générateur de rapports PDF/CSV
```

---

# 3. Main Architectural Principles / Principes d’architecture

## 3.1 Separation of concerns / Séparation des responsabilités

Each layer must have a clear role.

Chaque couche doit avoir un rôle clair.

```text
API routes      = receive HTTP requests and return responses
Schemas         = validate input/output data
Services        = orchestrate business logic
Domain          = contain pure business and quant logic
Repositories    = access the database
Models          = represent database tables
Frontend pages  = display features
Frontend hooks  = connect UI to API
```

---

## 3.2 Business logic must not live in routes  
## La logique métier ne doit pas être dans les routes

Bad / Mauvais :

```python
@router.post("/risk/var")
def calculate_var(request):
    # long VaR calculation directly here
    ...
```

Good / Bon :

```python
@router.post("/risk/var")
def calculate_var(request: VarRequest):
    return risk_service.calculate_var(request)
```

Routes should stay thin.

Les routes doivent rester légères.

---

## 3.3 Quant calculations should be testable  
## Les calculs quantitatifs doivent être testables

VaR, CVaR, volatility, Black-Scholes, Greeks, duration and bond pricing must be implemented as pure functions when possible.

La VaR, la CVaR, la volatilité, Black-Scholes, les Greeks, la duration et le pricing obligataire doivent être implémentés sous forme de fonctions pures quand c’est possible.

Example / Exemple :

```python
def historical_var(returns: list[float], confidence_level: float) -> float:
    ...
```

This makes testing easier and avoids hidden database dependencies.

Cela facilite les tests et évite les dépendances cachées à la base de données.

---

## 3.4 AI must explain, not replace calculations  
## L’IA doit expliquer, pas remplacer les calculs

The AI layer must never be the source of truth for financial calculations.

La couche IA ne doit jamais être la source de vérité pour les calculs financiers.

Correct structure / Bonne structure :

```text
Quant engine calculates the numbers.
Risk engine checks the limits.
AI engine explains the results.
Frontend displays the workflow.
```

Structure correcte :

```text
Le moteur quant calcule les chiffres.
Le moteur de risque vérifie les limites.
Le moteur IA explique les résultats.
Le frontend affiche le workflow.
```

---

## 3.5 Bilingual by design / Bilingue par conception

All visible UI text must come from translation files.

Tout texte visible dans l’interface doit venir des fichiers de traduction.

```text
frontend/src/i18n/en.json
frontend/src/i18n/fr.json
```

Bad / Mauvais :

```tsx
<h1>Risk Dashboard</h1>
```

Good / Bon :

```tsx
<h1>{t("dashboard.title")}</h1>
```

---

# 4. Recommended Tech Stack / Stack technique recommandée

## 4.1 Frontend

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

### Responsibilities / Responsabilités

- display dashboards;
- provide bilingual UI;
- handle user interactions;
- call backend APIs;
- validate forms with Zod;
- render charts and tables;
- display alerts and reports.

---

## 4.2 Backend

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

### Responsibilities / Responsabilités

- expose REST API;
- validate requests;
- run business services;
- calculate financial metrics;
- manage portfolios, trades, risk and reports;
- persist data in PostgreSQL;
- run long calculations asynchronously if needed.

---

## 4.3 Quant / AI

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

### Responsibilities / Responsabilités

- returns and volatility;
- VaR and CVaR;
- portfolio optimization;
- backtesting;
- Black-Scholes pricing;
- Greeks;
- yield curve and bond analytics;
- anomaly detection;
- AI explanations and reports.

---

## 4.4 DevOps

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

### Responsibilities / Responsabilités

- local development environment;
- automated tests;
- code formatting;
- linting;
- build checks;
- future deployment readiness.

---

# 5. Backend Architecture / Architecture backend

## 5.1 Backend folder structure / Structure des dossiers backend

```text
backend/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── health_routes.py
│   │   │   ├── auth_routes.py
│   │   │   ├── asset_routes.py
│   │   │   ├── market_data_routes.py
│   │   │   ├── portfolio_routes.py
│   │   │   ├── trade_routes.py
│   │   │   ├── analytics_routes.py
│   │   │   ├── risk_routes.py
│   │   │   ├── volatility_routes.py
│   │   │   ├── pricing_routes.py
│   │   │   ├── rates_routes.py
│   │   │   ├── stress_routes.py
│   │   │   ├── limits_routes.py
│   │   │   ├── pnl_routes.py
│   │   │   ├── reconciliation_routes.py
│   │   │   ├── ai_routes.py
│   │   │   └── report_routes.py
│   │   └── dependencies.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── logging.py
│   │   └── exceptions.py
│   │
│   ├── database/
│   │   ├── session.py
│   │   ├── base.py
│   │   └── migrations/
│   │
│   ├── models/
│   │   ├── user_model.py
│   │   ├── asset_model.py
│   │   ├── market_price_model.py
│   │   ├── portfolio_model.py
│   │   ├── position_model.py
│   │   ├── trade_model.py
│   │   ├── risk_metric_model.py
│   │   ├── risk_limit_model.py
│   │   ├── stress_scenario_model.py
│   │   ├── pnl_model.py
│   │   ├── report_model.py
│   │   └── audit_event_model.py
│   │
│   ├── schemas/
│   │   ├── auth_schema.py
│   │   ├── asset_schema.py
│   │   ├── market_data_schema.py
│   │   ├── portfolio_schema.py
│   │   ├── trade_schema.py
│   │   ├── analytics_schema.py
│   │   ├── risk_schema.py
│   │   ├── volatility_schema.py
│   │   ├── pricing_schema.py
│   │   ├── rates_schema.py
│   │   ├── stress_schema.py
│   │   ├── limits_schema.py
│   │   ├── pnl_schema.py
│   │   └── report_schema.py
│   │
│   ├── repositories/
│   │   ├── user_repository.py
│   │   ├── asset_repository.py
│   │   ├── market_data_repository.py
│   │   ├── portfolio_repository.py
│   │   ├── trade_repository.py
│   │   ├── risk_repository.py
│   │   ├── limits_repository.py
│   │   ├── pnl_repository.py
│   │   └── report_repository.py
│   │
│   ├── services/
│   │   ├── market_data_service.py
│   │   ├── portfolio_service.py
│   │   ├── trade_service.py
│   │   ├── analytics_service.py
│   │   ├── risk_service.py
│   │   ├── volatility_service.py
│   │   ├── pricing_service.py
│   │   ├── rates_service.py
│   │   ├── stress_service.py
│   │   ├── limit_service.py
│   │   ├── pnl_service.py
│   │   ├── reconciliation_service.py
│   │   ├── riskdna_service.py
│   │   ├── ai_service.py
│   │   └── report_service.py
│   │
│   ├── domain/
│   │   ├── portfolios/
│   │   ├── trades/
│   │   ├── analytics/
│   │   ├── risk/
│   │   ├── volatility/
│   │   ├── pricing/
│   │   ├── rates/
│   │   ├── stress/
│   │   ├── limits/
│   │   ├── pnl/
│   │   └── reports/
│   │
│   ├── jobs/
│   │   ├── worker.py
│   │   ├── market_data_jobs.py
│   │   ├── risk_jobs.py
│   │   └── report_jobs.py
│   │
│   ├── main.py
│   └── __init__.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── api/
│
├── pyproject.toml
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 5.2 Backend layers / Couches backend

## API routes

### Role

Receive HTTP requests and call services.

### Rules

- no complex logic;
- no direct database queries;
- no financial formulas;
- input/output through schemas;
- use dependency injection.

---

## Schemas

### Role

Validate API inputs and outputs.

### Tools

```text
Pydantic
```

### Example

```python
class BlackScholesRequest(BaseModel):
    spot: float
    strike: float
    time_to_maturity: float
    risk_free_rate: float
    volatility: float
```

---

## Services

### Role

Orchestrate use cases.

Example:

```text
TradeSimulationService
```

Responsibilities:

- load portfolio;
- apply proposed trade;
- calculate before/after positions;
- call risk service;
- call RiskDNA service;
- return simulation result.

---

## Domain

### Role

Contain pure business and quant logic.

Examples:

```text
historical_var.py
expected_shortfall.py
black_scholes.py
greeks.py
bond_pricing.py
duration.py
riskdna_score.py
```

The domain layer should be the easiest layer to test.

---

## Repositories

### Role

Access database tables.

Rules:

- only database logic;
- no risk formulas;
- no business decisions;
- no API-specific objects.

---

## Models

### Role

Represent database tables.

Tool:

```text
SQLAlchemy
```

---

# 6. Domain Modules / Modules domaine

## 6.1 Portfolio domain

```text
domain/portfolios/
├── portfolio_calculator.py
├── allocation_calculator.py
├── exposure_calculator.py
└── portfolio_rules.py
```

Responsibilities:

- portfolio value;
- position weights;
- sector exposure;
- currency exposure;
- benchmark comparison.

---

## 6.2 Risk domain

```text
domain/risk/
├── historical_var.py
├── parametric_var.py
├── expected_shortfall.py
├── monte_carlo_var.py
├── risk_contribution.py
└── loss_distribution.py
```

Responsibilities:

- VaR;
- CVaR / Expected Shortfall;
- loss distribution;
- risk contribution;
- rolling risk.

---

## 6.3 Volatility domain

```text
domain/volatility/
├── realized_volatility.py
├── rolling_volatility.py
├── annualized_volatility.py
└── volatility_regime.py
```

Responsibilities:

- daily volatility;
- annualized volatility;
- rolling volatility;
- volatility regime classification.

---

## 6.4 Pricing domain

```text
domain/pricing/
├── black_scholes.py
├── black_scholes_greeks.py
├── put_call_parity.py
├── payoff.py
└── implied_volatility.py
```

Responsibilities:

- European call price;
- European put price;
- d1 and d2;
- Greeks;
- payoff diagrams;
- put-call parity;
- implied volatility later.

---

## 6.5 Rates domain

```text
domain/rates/
├── yield_curve.py
├── spot_rates.py
├── discount_factors.py
├── bond_pricing.py
├── duration.py
├── convexity.py
└── rate_shock.py
```

Responsibilities:

- yield curve;
- spot rates;
- discount factors;
- bond pricing;
- duration;
- convexity later;
- rate stress tests.

---

## 6.6 RiskDNA domain

```text
domain/riskdna/
├── riskdna_score.py
├── riskdna_drivers.py
├── riskdna_thresholds.py
└── riskdna_explanation_context.py
```

Responsibilities:

- aggregate risk indicators;
- produce Low / Medium / High / Critical score;
- return explainable drivers;
- prepare data for AI explanation.

---

# 7. Frontend Architecture / Architecture frontend

## 7.1 Frontend folder structure / Structure frontend

```text
frontend/
├── src/
│   ├── app/
│   │   ├── router.tsx
│   │   ├── providers.tsx
│   │   ├── routes.tsx
│   │   └── App.tsx
│   │
│   ├── components/
│   │   ├── layout/
│   │   │   ├── AppShell.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Topbar.tsx
│   │   │   └── PageHeader.tsx
│   │   ├── charts/
│   │   │   ├── LineChartCard.tsx
│   │   │   ├── BarChartCard.tsx
│   │   │   ├── HeatmapCard.tsx
│   │   │   └── WaterfallChart.tsx
│   │   ├── tables/
│   │   │   ├── DataTable.tsx
│   │   │   └── MetricTable.tsx
│   │   ├── forms/
│   │   │   ├── FormField.tsx
│   │   │   └── NumberInput.tsx
│   │   ├── finance/
│   │   │   ├── RiskBadge.tsx
│   │   │   ├── MetricCard.tsx
│   │   │   ├── MoneyValue.tsx
│   │   │   └── PercentValue.tsx
│   │   └── ui/
│   │
│   ├── features/
│   │   ├── dashboard/
│   │   ├── market-data/
│   │   ├── portfolio/
│   │   ├── trade-simulator/
│   │   ├── performance/
│   │   ├── risk-monitor/
│   │   ├── volatility-lab/
│   │   ├── options-pricing/
│   │   ├── rates-lab/
│   │   ├── stress-testing/
│   │   ├── limits/
│   │   ├── pnl/
│   │   ├── reconciliation/
│   │   ├── ai-anomalies/
│   │   ├── reports/
│   │   └── settings/
│   │
│   ├── hooks/
│   │   ├── usePortfolio.ts
│   │   ├── useMarketData.ts
│   │   ├── useRiskMetrics.ts
│   │   └── useTranslation.ts
│   │
│   ├── i18n/
│   │   ├── en.json
│   │   ├── fr.json
│   │   └── i18n.ts
│   │
│   ├── lib/
│   │   ├── api-client.ts
│   │   ├── endpoints.ts
│   │   ├── formatters.ts
│   │   ├── validators.ts
│   │   └── constants.ts
│   │
│   ├── types/
│   │   ├── asset.ts
│   │   ├── portfolio.ts
│   │   ├── trade.ts
│   │   ├── risk.ts
│   │   ├── pricing.ts
│   │   ├── rates.ts
│   │   └── report.ts
│   │
│   └── main.tsx
│
├── package.json
├── vite.config.ts
├── tsconfig.json
└── README.md
```

---

## 7.2 Feature folder pattern / Modèle de dossier feature

Each feature should follow the same structure.

Chaque feature devrait suivre la même structure.

Example:

```text
features/risk-monitor/
├── pages/
│   └── RiskMonitorPage.tsx
├── components/
│   ├── VarCard.tsx
│   ├── ExpectedShortfallCard.tsx
│   ├── LossDistributionChart.tsx
│   └── RiskContributionTable.tsx
├── hooks/
│   └── useRiskMonitor.ts
├── api/
│   └── riskMonitorApi.ts
├── schemas/
│   └── riskMonitorSchema.ts
└── index.ts
```

Rules:

- pages assemble components;
- components stay reusable;
- hooks call APIs;
- schemas validate forms;
- API files isolate backend calls.

---

# 8. Frontend Pages / Pages frontend

## Main navigation

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
AI Anomaly Center
Reports Center
Settings
```

---

## 8.1 Dashboard

Purpose:

- global overview;
- main KPIs;
- risk summary;
- latest alerts.

Components:

```text
PortfolioValueCard
DailyPnlCard
VarCard
ExpectedShortfallCard
RiskDnaCard
LimitUsageCard
TopRiskContributors
PortfolioValueChart
```

---

## 8.2 Market Data

Purpose:

- visualize assets and historical prices.

Components:

```text
AssetSearch
AssetTable
PriceChart
ReturnsDistribution
VolatilitySummary
CorrelationPreview
```

---

## 8.3 Portfolio Builder

Purpose:

- create and edit portfolios.

Components:

```text
PortfolioSelector
PositionTable
AddPositionModal
AllocationChart
SectorExposureHeatmap
CurrencyExposureCard
```

---

## 8.4 Trade Simulator

Purpose:

- simulate front-office decisions before execution.

Components:

```text
TradeTicketForm
NaturalLanguageTradeInput
BeforeAfterRiskCards
AllocationDeltaTable
RiskDnaPanel
ApprovalStatusBadge
```

---

## 8.5 Risk Monitor

Purpose:

- middle-office risk view.

Components:

```text
HistoricalVarCard
ParametricVarCard
ExpectedShortfallCard
LossDistributionChart
RiskContributionTable
CorrelationHeatmap
RollingRiskChart
```

---

## 8.6 Volatility Lab

Purpose:

- analyze realized and rolling volatility.

Components:

```text
VolatilitySelector
HistoricalVolatilityCard
AnnualizedVolatilityCard
RollingVolatilityChart
VolatilityComparisonChart
VolatilityRegimeBadge
```

---

## 8.7 Options Pricing Lab

Purpose:

- price European options and display Greeks.

Components:

```text
BlackScholesForm
CallPriceCard
PutPriceCard
GreeksTable
PayoffChart
SensitivityChart
PutCallParityCheck
```

---

## 8.8 Rates Lab

Purpose:

- analyze rates, yield curves and bonds.

Components:

```text
YieldCurveChart
SpotRatesTable
DiscountFactorsTable
BondPricingForm
BondCashFlowTable
DurationCard
RateShockPanel
```

---

## 8.9 Reports Center

Purpose:

- generate bilingual reports.

Components:

```text
ReportTypeSelector
LanguageSelector
ReportPreview
GenerateReportButton
DownloadPdfButton
DownloadCsvButton
```

---

# 9. Data Architecture / Architecture des données

## 9.1 Main database tables / Tables principales

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

---

## 9.2 Extended quant tables / Tables quant étendues

```text
volatility_metrics
option_pricing_results
option_greeks
yield_curves
spot_rates
discount_factors
bonds
bond_valuations
rate_shock_results
riskdna_results
```

---

## 9.3 Relationships / Relations

```text
User 1 --- N Portfolio
Portfolio 1 --- N Position
Asset 1 --- N Position
Asset 1 --- N MarketPrice
Portfolio 1 --- N Trade
Portfolio 1 --- N RiskMetric
Portfolio 1 --- N PnLRecord
Portfolio 1 --- N LimitBreach
Portfolio 1 --- N Report
Portfolio 1 --- N RiskDnaResult
Asset 1 --- N OptionPricingResult
YieldCurve 1 --- N SpotRate
Bond 1 --- N BondValuation
```

---

# 10. API Architecture / Architecture API

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
/api/volatility
/api/pricing
/api/rates
/api/stress
/api/limits
/api/pnl
/api/reconciliation
/api/ai
/api/reports
/api/audit
```

---

## 10.2 API design rules / Règles de conception API

- Use nouns for resources.
- Use clear response schemas.
- Return errors consistently.
- Use status codes correctly.
- Keep route names predictable.
- Do not expose internal model names.
- Do not return unnecessary sensitive data.

---

## 10.3 Example endpoints / Exemples d’endpoints

```text
GET  /api/health
GET  /api/assets
GET  /api/assets/{symbol}
GET  /api/market-data/prices/{symbol}
POST /api/portfolios
GET  /api/portfolios/{portfolio_id}
POST /api/trades/simulate
GET  /api/risk/var/{portfolio_id}
GET  /api/risk/expected-shortfall/{portfolio_id}
GET  /api/volatility/{symbol}/rolling
POST /api/pricing/black-scholes
POST /api/rates/bond-price
POST /api/stress/run/{portfolio_id}
POST /api/reports/daily-risk
```

---

# 11. RiskDNA v2 Architecture / Architecture RiskDNA v2

## 11.1 Inputs

```text
VaR
CVaR
Volatility
Drawdown
Sector exposure
Single-name exposure
Option Delta
Option Gamma
Option Vega
Bond duration
Rate shock loss
Stress test loss
Anomaly score
Limit usage
```

---

## 11.2 Scoring structure

```text
RiskDNA Score =
  20% VaR usage
+ 20% CVaR usage
+ 15% volatility regime
+ 15% concentration risk
+ 10% option Greeks exposure
+ 10% rate duration exposure
+ 10% stress and anomaly score
```

---

## 11.3 Output

```json
{
  "score": "High",
  "numeric_score": 78,
  "main_drivers": [
    "Technology concentration",
    "CVaR above warning threshold",
    "High option Vega exposure"
  ],
  "recommendation": "Reduce exposure or hedge before approval."
}
```

---

## 11.4 AI explanation

The AI receives structured context, not raw database data.

L’IA reçoit un contexte structuré, pas les données brutes de la base.

Example:

```json
{
  "language": "en",
  "riskdna_score": "High",
  "var_change": "+0.8%",
  "cvar_change": "+1.3%",
  "main_driver": "Technology concentration",
  "recommendation": "Reduce or hedge the trade"
}
```

---

# 12. Testing Architecture / Architecture de tests

## 12.1 Backend tests

```text
tests/
├── unit/
│   ├── test_portfolio_calculator.py
│   ├── test_historical_var.py
│   ├── test_expected_shortfall.py
│   ├── test_volatility.py
│   ├── test_black_scholes.py
│   ├── test_greeks.py
│   ├── test_bond_pricing.py
│   ├── test_duration.py
│   └── test_riskdna_score.py
├── integration/
│   ├── test_portfolio_repository.py
│   ├── test_trade_simulation_flow.py
│   └── test_report_generation_flow.py
└── api/
    ├── test_health_routes.py
    ├── test_portfolio_routes.py
    ├── test_risk_routes.py
    ├── test_pricing_routes.py
    └── test_rates_routes.py
```

---

## 12.2 Frontend tests

```text
frontend/src/
├── features/
│   ├── dashboard/__tests__/
│   ├── portfolio/__tests__/
│   ├── risk-monitor/__tests__/
│   ├── options-pricing/__tests__/
│   └── rates-lab/__tests__/
```

Test focus:

- page rendering;
- form validation;
- language switch;
- API loading states;
- error states;
- chart data formatting.

---

## 12.3 Quant tests must be deterministic  
## Les tests quant doivent être déterministes

Use small known datasets.

Utiliser de petits jeux de données connus.

Example:

```text
returns = [-0.01, 0.02, -0.03, 0.01, -0.05]
```

Test:

```text
Historical VaR
Expected Shortfall
Volatility
Drawdown
```

---

# 13. DevOps Architecture / Architecture DevOps

## 13.1 Docker Compose

Recommended services:

```text
frontend
backend
postgres
redis
worker
```

Example:

```text
docker-compose.yml
├── frontend
├── backend
├── postgres
├── redis
└── worker
```

---

## 13.2 GitHub Actions

CI should run:

```text
Backend:
- install Python dependencies
- run Ruff
- run Black check
- run Pytest
- upload coverage

Frontend:
- install Node dependencies
- run ESLint
- run TypeScript check
- run tests
- run production build
```

---

# 14. Environment Variables / Variables d’environnement

## Backend

```text
DATABASE_URL
REDIS_URL
APP_ENV
SECRET_KEY
OPENAI_API_KEY
MARKET_DATA_PROVIDER
MARKET_DATA_API_KEY
```

## Frontend

```text
VITE_API_BASE_URL
VITE_APP_NAME
```

Rules:

- never commit `.env`;
- provide `.env.example`;
- keep secrets out of GitHub.

---

# 15. Error Handling / Gestion des erreurs

## Backend error response

```json
{
  "error": {
    "code": "PORTFOLIO_NOT_FOUND",
    "message": "Portfolio not found",
    "details": {}
  }
}
```

## Rules

- predictable errors;
- no raw stack traces in production;
- log technical details internally;
- return user-friendly messages.

---

# 16. Logging and Audit / Logs et audit

## Logs

Use logs for:

```text
API requests
calculation errors
AI provider errors
report generation
market data import
```

## Audit events

Use audit trail for:

```text
portfolio creation
position update
trade simulation
trade approval
limit breach
report generation
AI explanation generation
```

---

# 17. Security Principles / Principes de sécurité

- Use HTTPS in deployment.
- Validate all inputs.
- Never expose API keys.
- Avoid storing unnecessary personal data.
- Use role-based access later.
- Keep financial calculations traceable.
- Keep report generation auditable.

---

# 18. Naming Conventions / Conventions de nommage

## Backend

```text
snake_case for files and functions
PascalCase for classes
```

Examples:

```text
risk_service.py
BlackScholesInput
calculate_expected_shortfall
```

## Frontend

```text
PascalCase for components
camelCase for variables and functions
kebab-case for folders when useful
```

Examples:

```text
RiskMonitorPage.tsx
useRiskMetrics.ts
options-pricing/
```

## Git branches

```text
feature/project-foundation
feature/market-data
feature/portfolio-builder
feature/risk-engine
feature/options-pricing
feature/rates-lab
feature/riskdna-engine
docs/architecture
```

## Commits

```text
docs: add architecture documentation
chore: initialize backend foundation
feat: add market data module
feat: add black scholes pricing
test: add var and cvar unit tests
fix: correct expected shortfall calculation
```

---

# 19. Development Order / Ordre de développement

## Recommended order

```text
1. Documentation foundation
2. Backend health endpoint
3. Frontend shell
4. Bilingual system
5. Market data
6. Portfolio builder
7. Performance analytics
8. Volatility Lab
9. Risk Engine: VaR and CVaR
10. Trade Simulator
11. Options Pricing Lab
12. Rates Lab
13. Stress Testing
14. Limit Center
15. RiskDNA v2
16. P&L Attribution
17. Reports Center
18. AI explanations
19. Tests and CI
20. Final polish
```

---

# 20. Codex Usage Rules / Règles d’utilisation avec Codex

## Rule 1 — One issue at a time

Do not ask Codex to build the entire project at once.

Ne demande pas à Codex de construire tout le projet d’un coup.

Correct:

```text
Implement the backend health endpoint and tests.
```

Incorrect:

```text
Build the whole Athena project.
```

---

## Rule 2 — Always mention architecture

Every Codex prompt should include:

```text
Follow the architecture defined in docs/architecture.md.
Keep routes thin.
Put business logic in services.
Put pure quant calculations in domain modules.
Add tests.
```

---

## Rule 3 — Ask for tests

Every backend feature must include tests.

Chaque feature backend doit inclure des tests.

---

## Rule 4 — Protect bilingual UI

Every frontend feature must use i18n.

Chaque feature frontend doit utiliser le système bilingue.

---

# 21. First Codex Prompt / Premier prompt Codex

Use this after adding this file.

À utiliser après avoir ajouté ce fichier.

```text
Read docs/architecture.md and initialize the technical foundation of Athena AI Risk Terminal.

Create a FastAPI backend inside backend/ with:
- app/main.py
- app/api/routes/health_routes.py
- app/core/config.py
- tests/api/test_health_routes.py
- pyproject.toml or requirements.txt

Create a React TypeScript Vite frontend inside frontend/ with:
- a basic AppShell layout
- a sidebar placeholder
- a topbar placeholder
- i18n files for English and French
- a homepage titled Athena AI Risk Terminal

Follow the architecture rules:
- keep backend routes thin;
- put logic in services when needed;
- keep frontend visible text in i18n files;
- add basic tests where appropriate.
```

---

# 22. Final Architecture Summary / Résumé final de l’architecture

## English

Athena AI Risk Terminal uses a clean full-stack architecture:

```text
React TypeScript frontend
FastAPI backend
Service layer
Domain quant engines
Repository layer
PostgreSQL database
Redis workers
AI explanation layer
```

The architecture is designed to support a professional multi-asset risk platform covering equities, options, bonds, rates, portfolio analytics, risk controls and AI-assisted reporting.

## Français

Athena AI Risk Terminal utilise une architecture full-stack propre :

```text
Frontend React TypeScript
Backend FastAPI
Couche services
Moteurs quantitatifs domaine
Couche repository
Base PostgreSQL
Workers Redis
Couche d’explication IA
```

L’architecture est conçue pour supporter une plateforme de risque multi-actifs professionnelle couvrant les actions, les options, les obligations, les taux, l’analyse de portefeuille, les contrôles de risque et les rapports assistés par IA.
