# Athena AI Risk Terminal — Product Specification  
# Spécification produit — Athena AI Risk Terminal

**Recommended file path / Emplacement recommandé :** `docs/product-spec.md`  
**Project / Projet :** Athena AI Risk Terminal  
**Document purpose / Objectif du document :** define what the product must do, for whom, and how each feature should behave.  
**Objectif :** définir ce que le produit doit faire, pour qui, et comment chaque fonctionnalité doit se comporter.

---

# 1. Product Summary / Résumé produit

## English

Athena AI Risk Terminal is a bilingual AI-powered quantitative finance platform that connects front-office portfolio decisions with middle-office risk controls.

The product allows users to:

- build portfolios;
- simulate trades;
- analyze performance;
- calculate VaR and CVaR;
- analyze volatility;
- price European call and put options;
- calculate Black-Scholes Greeks;
- analyze yield curves and spot rates;
- price bonds;
- run stress tests;
- monitor limits;
- attribute P&L;
- detect anomalies;
- generate AI-assisted risk reports;
- explain risk through the RiskDNA engine.

## Français

Athena AI Risk Terminal est une plateforme financière quantitative bilingue propulsée par l’IA qui relie les décisions de portefeuille front office aux contrôles de risque middle office.

Le produit permet à l’utilisateur de :

- construire des portefeuilles ;
- simuler des transactions ;
- analyser la performance ;
- calculer la VaR et la CVaR ;
- analyser la volatilité ;
- pricer des options européennes call et put ;
- calculer les Greeks Black-Scholes ;
- analyser les yield curves et les spot rates ;
- pricer des obligations ;
- lancer des stress tests ;
- surveiller les limites ;
- attribuer le P&L ;
- détecter des anomalies ;
- générer des rapports de risque assistés par IA ;
- expliquer le risque avec le moteur RiskDNA.

---

# 2. Product Vision / Vision produit

## English

The vision is to build a serious portfolio project that looks and behaves like a simplified institutional risk terminal.

A front-office user should be able to propose a trade or portfolio allocation, and the platform should immediately show the impact on:

- portfolio value;
- risk metrics;
- volatility;
- VaR and CVaR;
- concentration;
- limits;
- stress losses;
- option Greeks;
- rate exposure;
- P&L;
- RiskDNA score;
- AI-generated explanation.

## Français

La vision est de construire un projet portfolio sérieux qui ressemble à un terminal de risque institutionnel simplifié.

Un utilisateur front office doit pouvoir proposer une transaction ou une allocation de portefeuille, et la plateforme doit immédiatement afficher l’impact sur :

- la valeur du portefeuille ;
- les métriques de risque ;
- la volatilité ;
- la VaR et la CVaR ;
- la concentration ;
- les limites ;
- les pertes en stress test ;
- les Greeks d’options ;
- l’exposition aux taux ;
- le P&L ;
- le score RiskDNA ;
- une explication générée par IA.

---

# 3. Product Goals / Objectifs produit

## 3.1 Business goals / Objectifs métier

- Demonstrate understanding of front-office and middle-office workflows.
- Show strong quantitative finance knowledge.
- Build a credible GitHub project for CV, LinkedIn and interviews.
- Create a bilingual product with professional UX.
- Connect software engineering with financial risk management.

## 3.2 Technical goals / Objectifs techniques

- Use a clean full-stack architecture.
- Keep backend routes thin.
- Put business logic in services.
- Put pure calculations in domain modules.
- Use strong typing in backend and frontend.
- Make calculations testable.
- Support future deployment with Docker.
- Prepare the app for CI/CD.

## 3.3 Learning goals / Objectifs d’apprentissage

- FastAPI backend architecture.
- React TypeScript frontend architecture.
- Portfolio analytics.
- VaR and CVaR.
- Volatility.
- Black-Scholes.
- Greeks.
- Yield curves and spot rates.
- Bond pricing.
- Stress testing.
- AI-assisted reporting.
- Professional GitHub workflow.

---

# 4. Target Users / Utilisateurs cibles

## 4.1 Portfolio Manager / Gestionnaire de portefeuille

### Needs / Besoins

- Build and monitor portfolios.
- Simulate trades before execution.
- Compare current and optimized allocation.
- Understand performance and risk quickly.

### Key screens / Écrans clés

- Dashboard
- Portfolio Builder
- Trade Simulator
- Performance Analytics
- RiskDNA Panel

---

## 4.2 Risk Analyst / Analyste risque

### Needs / Besoins

- Monitor VaR and CVaR.
- Check limit breaches.
- Run stress tests.
- Understand main risk drivers.
- Generate daily risk reports.

### Key screens / Écrans clés

- Risk Monitor
- Limit Center
- Stress Testing
- Reports Center
- AI Anomaly Center

---

## 4.3 Middle Office Analyst / Analyste middle office

### Needs / Besoins

- Reconcile trades and positions.
- Attribute P&L.
- Detect operational anomalies.
- Track audit events.
- Produce reports.

### Key screens / Écrans clés

- P&L Attribution
- Reconciliation
- Reports Center
- Audit History

---

## 4.4 Recruiter / Interviewer / Mentor

### Needs / Besoins

- Quickly understand the project.
- See a clean architecture.
- See screenshots and demo flow.
- Understand what was implemented.
- Evaluate technical and financial maturity.

### Key documents / Documents clés

- README.md
- docs/project-plan.md
- docs/architecture.md
- docs/product-spec.md
- docs/athena_detailed_plan.md

---

# 5. Product Scope / Périmètre produit

## 5.1 In scope / Inclus

The project includes:

- bilingual UI;
- portfolio construction;
- trade simulation;
- market data module;
- performance analytics;
- volatility analytics;
- risk engine;
- VaR and CVaR;
- options pricing;
- Black-Scholes;
- Greeks;
- rates analytics;
- yield curves;
- spot rates;
- bond pricing;
- stress testing;
- limit monitoring;
- P&L attribution;
- AI explanations;
- RiskDNA;
- reports;
- GitHub documentation;
- tests;
- Docker foundation.

## 5.2 Out of scope for first version / Hors périmètre première version

Not required in the first version:

- real trading execution;
- broker integration;
- real-time professional market data feed;
- user payment system;
- production-grade authentication;
- full regulatory compliance;
- high-frequency trading;
- advanced exotic derivatives;
- live order management system.

---

# 6. Product Modules / Modules produit

---

## 6.1 Dashboard

### Purpose / Objectif

Give a global overview of the portfolio and risk state.

### Main information

- Portfolio value.
- Daily P&L.
- VaR 95%.
- CVaR / Expected Shortfall.
- RiskDNA score.
- Limit usage.
- Top risk contributors.
- Latest alerts.

### User story

```text
As a portfolio manager,
I want to see the main portfolio and risk indicators in one screen,
so that I can quickly understand the current risk state.
```

### Acceptance criteria

- User sees portfolio value.
- User sees VaR and CVaR.
- User sees RiskDNA score.
- User sees latest alerts.
- UI supports English and French.

---

## 6.2 Market Data

### Purpose / Objectif

Provide asset prices and returns used by all calculations.

### Features

- Search asset by symbol.
- Display historical prices.
- Calculate daily returns.
- Show missing data warnings.
- Store price data.

### User story

```text
As a user,
I want to view historical asset prices,
so that I can understand the data used by the platform.
```

### Acceptance criteria

- User can select an asset.
- User sees a price chart.
- Backend can return prices and returns.
- Missing data is handled safely.

---

## 6.3 Portfolio Builder

### Purpose / Objectif

Allow the user to create and manage portfolios.

### Features

- Create portfolio.
- Add positions.
- Edit quantities.
- Remove positions.
- Calculate portfolio value.
- Calculate weights.
- Show sector exposure.
- Show currency exposure.

### User story

```text
As a portfolio manager,
I want to build a portfolio with several positions,
so that I can analyze its performance and risk.
```

### Acceptance criteria

- User can create a portfolio.
- User can add positions.
- User can see portfolio value.
- User can see allocation by asset and sector.

---

## 6.4 Performance Analytics

### Purpose / Objectif

Measure portfolio performance.

### Metrics

- Total return.
- Annualized return.
- Annualized volatility.
- Sharpe ratio.
- Sortino ratio.
- Max drawdown.
- Beta.
- Alpha.
- Tracking error.

### User story

```text
As a portfolio manager,
I want to analyze portfolio performance,
so that I can evaluate whether the strategy is efficient.
```

### Acceptance criteria

- Backend calculates performance metrics.
- Frontend displays performance cards.
- Drawdown chart is available.
- Benchmark comparison is available later.

---

## 6.5 Volatility Lab

### Purpose / Objectif

Analyze realized and rolling volatility.

### Features

- Daily volatility.
- Annualized volatility.
- Rolling 20D volatility.
- Rolling 60D volatility.
- Rolling 252D volatility.
- Volatility regime badge.
- Volatility comparison between assets.

### User story

```text
As a risk analyst,
I want to monitor volatility,
so that I can understand when portfolio risk is increasing.
```

### Acceptance criteria

- User can see historical volatility.
- User can see rolling volatility.
- User can compare volatility across assets.
- Volatility is reusable in VaR and option pricing.

---

## 6.6 Risk Engine

### Purpose / Objectif

Calculate portfolio risk metrics.

### Features

- Historical VaR.
- Parametric VaR.
- CVaR / Expected Shortfall.
- Loss distribution.
- Risk contribution.
- Rolling risk.

### User story

```text
As a risk analyst,
I want to calculate VaR and CVaR,
so that I can understand the downside risk of the portfolio.
```

### Acceptance criteria

- Historical VaR works with portfolio returns.
- CVaR is calculated from tail losses.
- Outputs are positive loss values.
- Unit tests cover deterministic examples.
- Results can be displayed in Risk Monitor.

---

## 6.7 Trade Simulator

### Purpose / Objectif

Simulate a trade before execution.

### Features

- Buy asset.
- Sell asset.
- Rebalance position.
- Compare before/after portfolio.
- Show impact on:
  - value;
  - weights;
  - exposure;
  - VaR;
  - CVaR;
  - volatility;
  - RiskDNA score.

### User story

```text
As a front-office user,
I want to simulate a trade before executing it,
so that I can understand its impact on portfolio risk.
```

### Acceptance criteria

- User can enter a trade.
- System returns before/after comparison.
- Risk metrics update after simulation.
- RiskDNA explains the impact.

---

## 6.8 Options Pricing Lab

### Purpose / Objectif

Price European call and put options.

### Features

- Black-Scholes call price.
- Black-Scholes put price.
- d1 and d2.
- Delta.
- Gamma.
- Vega.
- Theta.
- Rho.
- Payoff chart.
- Put-call parity check.

### User story

```text
As a quant user,
I want to price call and put options,
so that I can understand option value and Greeks exposure.
```

### Acceptance criteria

- User enters spot, strike, maturity, rate and volatility.
- System returns call and put price.
- System returns Greeks.
- Put-call parity test is implemented.
- UI displays results clearly.

---

## 6.9 Rates Lab

### Purpose / Objectif

Analyze interest rates and bonds.

### Features

- Yield curve display.
- Spot rates table.
- Discount factors table.
- Bond cash flow schedule.
- Bond pricing.
- Duration.
- Rate shock stress test.

### User story

```text
As a risk analyst,
I want to analyze bonds and rate sensitivity,
so that I can measure fixed-income risk.
```

### Acceptance criteria

- User can view a yield curve.
- User can calculate discount factors.
- User can price a bond.
- User can run a +100 bps rate shock.
- Duration is displayed.

---

## 6.10 Stress Testing

### Purpose / Objectif

Estimate portfolio loss under crisis scenarios.

### Scenarios

- Equity market crash.
- Technology selloff.
- Rate shock.
- FX shock.
- COVID-like shock.
- 2008-like shock.
- Custom scenario.

### User story

```text
As a risk analyst,
I want to run stress tests,
so that I can evaluate portfolio resilience under extreme scenarios.
```

### Acceptance criteria

- User can choose a scenario.
- System calculates estimated loss.
- Loss is broken down by asset or sector.
- Results can feed RiskDNA.

---

## 6.11 Limit Center

### Purpose / Objectif

Monitor risk limits and breaches.

### Limit examples

- Max VaR.
- Max CVaR.
- Max sector exposure.
- Max single-name exposure.
- Max drawdown.
- Max option delta exposure.
- Max option vega exposure.
- Max duration exposure.

### User story

```text
As a middle-office analyst,
I want to detect limit breaches,
so that I can flag risky portfolios before approval.
```

### Acceptance criteria

- System checks limits automatically.
- Limits return OK / Warning / Breach / Critical.
- Breach history is stored.
- User sees limit usage bars.

---

## 6.12 P&L Attribution

### Purpose / Objectif

Explain profit and loss.

### Features

- Daily P&L.
- P&L by asset.
- P&L by sector.
- Fees.
- Slippage.
- Residual unexplained P&L.
- Later: Greeks-based option P&L.

### User story

```text
As a middle-office analyst,
I want to understand where P&L comes from,
so that I can explain performance and detect anomalies.
```

### Acceptance criteria

- User sees P&L by asset.
- User sees P&L by sector.
- Residual P&L is identified.
- AI summary explains main drivers.

---

## 6.13 Reconciliation

### Purpose / Objectif

Compare expected positions with imported positions or trades.

### Features

- Import trades.
- Import positions.
- Detect missing trades.
- Detect quantity mismatch.
- Detect price mismatch.
- Generate exception report.

### User story

```text
As a middle-office analyst,
I want to reconcile positions and trades,
so that I can detect operational errors.
```

### Acceptance criteria

- User can upload trade/position files later.
- System detects mismatches.
- Exceptions are displayed in a table.
- Report can be generated.

---

## 6.14 AI Anomaly Center

### Purpose / Objectif

Detect abnormal trades, risk changes or P&L movements.

### Features

- Z-score baseline.
- Isolation Forest later.
- Trade size anomaly.
- P&L anomaly.
- Risk metric anomaly.
- AI explanation.

### User story

```text
As a risk analyst,
I want to detect unusual activity,
so that I can investigate abnormal risk or P&L movements.
```

### Acceptance criteria

- System assigns anomaly score.
- User sees alert level.
- AI provides a short explanation.
- User can mark false positives later.

---

## 6.15 RiskDNA Engine

### Purpose / Objectif

Provide one explainable risk fingerprint for a portfolio or trade.

### Inputs

- VaR.
- CVaR.
- Volatility.
- Drawdown.
- Concentration.
- Stress losses.
- Option Greeks.
- Rate duration.
- Limit breaches.
- Anomaly score.

### Outputs

- Low / Medium / High / Critical.
- Numeric score.
- Main drivers.
- Recommendation.
- AI explanation in English and French.

### User story

```text
As a user,
I want one clear risk score and explanation,
so that I can quickly understand whether a trade or portfolio is acceptable.
```

### Acceptance criteria

- RiskDNA score is explainable.
- Score changes after risky trade simulation.
- Main drivers are visible.
- AI explanation is bilingual.
- AI does not replace the numerical calculations.

---

## 6.16 Reports Center

### Purpose / Objectif

Generate professional bilingual reports.

### Report types

- Daily risk report.
- Portfolio summary.
- Trade impact report.
- Options pricing report.
- Rates report.
- P&L report.
- Limit breach report.

### User story

```text
As a user,
I want to generate reports,
so that I can document risk, performance and trade decisions.
```

### Acceptance criteria

- User can select report type.
- User can select English or French.
- Report preview is available.
- PDF/CSV export later.
- AI commentary can be included.

---

# 7. MVP Definition / Définition du MVP

## MVP must include / Le MVP doit inclure

The first strong version should include:

```text
1. README and documentation
2. Backend health endpoint
3. Frontend shell
4. Bilingual UI foundation
5. Market Data page
6. Portfolio Builder
7. Performance Analytics
8. Volatility Lab
9. VaR and CVaR Risk Engine
10. Trade Simulator
11. RiskDNA v1
```

## Not required in MVP / Pas obligatoire dans le MVP

Can be added after MVP:

```text
Options Pricing Lab
Rates Lab
P&L Attribution
Reconciliation
AI Anomaly Center
PDF reports
Advanced authentication
Deployment
```

---

# 8. Product Roadmap / Roadmap produit

## Phase 0 — Repository foundation

- README.md.
- docs/project-plan.md.
- docs/architecture.md.
- docs/product-spec.md.
- docs/athena_detailed_plan.md.
- .gitignore.
- docker-compose.yml.

## Phase 1 — Technical foundation

- FastAPI backend.
- React TypeScript frontend.
- Health endpoint.
- App shell.
- Bilingual setup.

## Phase 2 — Market and portfolio

- Market data.
- Portfolio builder.
- Position management.
- Allocation view.

## Phase 3 — Performance and risk

- Performance analytics.
- Volatility Lab.
- VaR.
- CVaR.
- Risk Monitor.

## Phase 4 — Trade simulation and RiskDNA

- Trade Simulator.
- Before/after risk.
- RiskDNA v1.
- AI explanation later.

## Phase 5 — Derivatives and rates

- Black-Scholes.
- Greeks.
- Options Pricing Lab.
- Yield curve.
- Spot rates.
- Bond pricing.
- Rates Lab.

## Phase 6 — Middle office workflows

- Stress testing.
- Limit Center.
- P&L Attribution.
- Reconciliation.

## Phase 7 — AI and reports

- AI anomaly detection.
- AI risk explanation.
- Reports Center.
- PDF/CSV export.

## Phase 8 — Final polish

- Tests.
- CI/CD.
- Docker.
- Screenshots.
- Demo script.
- LinkedIn/CV material.

---

# 9. UI Requirements / Exigences UI

## 9.1 General UI

- Dark mode by default.
- Professional financial terminal style.
- Sidebar navigation.
- Topbar with portfolio selector.
- FR/EN language switch.
- Metric cards.
- Charts.
- Tables.
- Clear alert badges.

## 9.2 Bilingual requirement

All UI text must support:

```text
English
French
```

Translation files:

```text
frontend/src/i18n/en.json
frontend/src/i18n/fr.json
```

No hardcoded visible text in React components.

---

# 10. Non-Functional Requirements / Exigences non fonctionnelles

## Performance

- Basic pages should load quickly.
- Heavy calculations should later use workers.
- API responses should be structured and predictable.

## Reliability

- Quant calculations must have tests.
- API errors must be handled consistently.
- Missing market data must not crash the app.

## Maintainability

- Clean architecture.
- Feature-based frontend.
- Thin API routes.
- Services for orchestration.
- Domain modules for calculations.

## Security

- No secrets in GitHub.
- Use `.env.example`.
- Validate all inputs.
- Avoid exposing stack traces.
- Prepare role-based access later.

## Auditability

Important actions should be auditable later:

- portfolio creation;
- position update;
- trade simulation;
- limit breach;
- report generation;
- AI explanation generation.

---

# 11. Success Criteria / Critères de réussite

## Technical success

The project is successful technically if:

- the app starts locally;
- backend and frontend are separated;
- calculations are tested;
- architecture is documented;
- API endpoints are clean;
- frontend is bilingual;
- GitHub repository is professional.

## Product success

The product is successful if a user can:

1. create a portfolio;
2. view performance;
3. calculate volatility;
4. calculate VaR and CVaR;
5. simulate a trade;
6. understand risk impact;
7. get a RiskDNA score;
8. generate or preview a report later.

## Career success

The project is successful for your career if it clearly shows:

- software engineering skill;
- finance knowledge;
- quant curiosity;
- risk management understanding;
- bilingual product thinking;
- ability to build a serious GitHub project.

---

# 12. First Implementation Priority / Première priorité d’implémentation

## Current next step

After adding this file, the next technical task is:

```text
Create the backend and frontend foundation.
```

This means:

```text
backend/
frontend/
GET /api/health
basic React homepage
i18n foundation
```

## Recommended first Codex prompt

```text
Read docs/architecture.md and docs/product-spec.md.

Initialize the technical foundation for Athena AI Risk Terminal.

Create a FastAPI backend in backend/ with:
- app/main.py
- app/api/routes/health_routes.py
- app/core/config.py
- tests/api/test_health_routes.py

Create a React TypeScript Vite frontend in frontend/ with:
- a basic AppShell
- a Sidebar placeholder
- a Topbar placeholder
- English and French i18n files
- a homepage titled Athena AI Risk Terminal

Follow the architecture:
- keep backend routes thin;
- use schemas when needed;
- keep visible frontend text in i18n files;
- prepare the project for future modules.
```

---

# 13. Recommended Commit / Commit recommandé

```text
docs: add product specification
```
