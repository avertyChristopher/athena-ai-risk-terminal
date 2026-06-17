# Athena AI Risk Terminal — Simple Project Plan  
# Terminal Athena AI Risk — Plan simple du projet

**Recommended file name / Nom de fichier recommandé:** `docs/project-plan.md`  
**Purpose / Objectif:** simple roadmap to understand where the project is, what has been done, and what comes next.  
**Objectif:** feuille de route simple pour comprendre où en est le projet, ce qui est déjà fait et les prochaines étapes.

---

# 1. Project Vision / Vision du projet

## Français

Athena AI Risk Terminal est une plateforme finance quantitative bilingue qui mélange :

- **Front office** : construction de portefeuille, simulation de trade, pricing d’options.
- **Middle office** : contrôle du risque, limites, P&L, rapports.
- **Quant** : VaR, CVaR, volatilité, Black-Scholes, Greeks, obligations, taux.
- **IA** : explication du risque, détection d’anomalies, génération de rapports.

Le but est de créer un projet GitHub sérieux que tu peux montrer sur ton CV, LinkedIn ou en entrevue.

## English

Athena AI Risk Terminal is a bilingual quantitative finance platform combining:

- **Front office**: portfolio construction, trade simulation, option pricing.
- **Middle office**: risk control, limits, P&L, reports.
- **Quant**: VaR, CVaR, volatility, Black-Scholes, Greeks, bonds, rates.
- **AI**: risk explanations, anomaly detection, report generation.

The goal is to build a serious GitHub project that can be shown on a resume, LinkedIn profile or during interviews.

---

# 2. Current Status / État actuel

## Current implementation snapshot / Snapshot actuel

The project has moved beyond the original repository-initialization phase. The
current working foundation includes:

- FastAPI backend with module-based architecture for Market Data, Equity
  Analysis, Portfolio Builder, Risk Monitor and Trade Simulator.
- React/TypeScript/Vite frontend with pages for `/market-data`,
  `/equity-analysis`, `/portfolio-builder`, `/risk-monitor` and
  `/trade-simulator`.
- SQLite persistence through SQLAlchemy for portfolios, positions and imported
  Market Data rows.
- Editable Athena Demo Portfolio positions.
- Shared frontend portfolio context with selected portfolio/symbol persisted in
  localStorage.
- Cross-module workflow actions from portfolio positions into Market Data,
  Equity Analysis and Trade Simulator.
- Market Data portfolio coverage checks and CSV price import workflow.
- Risk Monitor connected to the selected portfolio with configurable limits and
  stress shocks.
- Equity Analysis analyst scorecard derived from existing valuation,
  profitability, growth, quality and risk metrics.
- Backend pytest and frontend production build currently used as validation
  gates.

Immediate project phase:

```text
Phase: integrated demo platform hardening
```

The historical phase plan below remains useful as a roadmap reference, but the
implementation is now ahead of the initial Phase 0/Phase 1 text.

## Français

Tu es actuellement au début du projet.

### Déjà fait

- Le repository GitHub est créé.
- Le push GitHub fonctionne.
- Le dossier `docs/` existe.
- Le plan détaillé existe.
- Le projet est prêt à recevoir une structure propre.

### Où tu es exactement

```text
Phase 0 — Initialisation du repository
```

Tu n’es pas encore dans le vrai développement backend/frontend.  
La priorité est maintenant de rendre le repo clair, propre et facile à comprendre.

## English

You are currently at the beginning of the project.

### Already done

- The GitHub repository has been created.
- GitHub push works.
- The `docs/` folder exists.
- The detailed plan exists.
- The project is ready to receive a clean structure.

### Current phase

```text
Phase 0 — Repository initialization
```

You are not yet in the real backend/frontend development phase.  
The priority now is to make the repository clean, clear and easy to understand.

---

# 3. Simple Repository Structure / Structure simple du repository

## Français

Structure recommandée :

```text
athena-ai-risk-terminal/
├── backend/
├── frontend/
├── docs/
│   ├── project-plan.md
│   └── athena_detailed_plan.md
├── notebooks/
├── README.md
└── .gitignore
```

## English

Recommended structure:

```text
athena-ai-risk-terminal/
├── backend/
├── frontend/
├── docs/
│   ├── project-plan.md
│   └── athena_detailed_plan.md
├── notebooks/
├── README.md
└── .gitignore
```

---

# 4. Phase 1 — Clean GitHub Foundation  
# Phase 1 — Base GitHub propre

## Goal / Objectif

## Français

Avoir un repository GitHub propre avant de coder.

## English

Have a clean GitHub repository before starting the code.

## Tasks / Tâches

- Add `README.md`.
- Add `docs/project-plan.md`.
- Keep `docs/athena_detailed_plan.md` as the full detailed reference.
- Create folders:
  - `backend/`
  - `frontend/`
  - `notebooks/`
- Add `.gitignore`.

## Commit

```text
docs: add simple project plan
```

---

# 5. Phase 2 — Technical Foundation  
# Phase 2 — Fondation technique

## Goal / Objectif

## Français

Créer une application minimale qui démarre côté backend et frontend.

## English

Create a minimal application that starts on both backend and frontend.

## Backend

Technology / Technologie:

```text
Python + FastAPI
```

Tasks / Tâches:

- Create the `backend/` folder.
- Install FastAPI.
- Create a health endpoint:

```text
GET /api/health
```

Expected response / Réponse attendue:

```json
{
  "status": "ok",
  "service": "athena-api"
}
```

## Frontend

Technology / Technologie:

```text
React + TypeScript + Vite
```

Tasks / Tâches:

- Create the `frontend/` folder.
- Create a homepage.
- Create a simple layout.
- Prepare English/French translation.

## Commit

```text
chore: initialize backend and frontend foundation
```

---

# 6. Phase 3 — Market Data Module  
# Phase 3 — Module données de marché

## Goal / Objectif

## Français

Importer ou simuler les premières données financières.

## English

Import or simulate the first financial market data.

## Tasks / Tâches

Backend:

- Create `Asset`.
- Create `MarketDataService`.
- Add route for historical prices.
- Add route for daily returns.

Frontend:

- Create `Market Data` page.
- Show asset list.
- Show a simple price chart.

## Why this phase matters / Pourquoi c’est important

## Français

Tous les autres modules dépendent des données de marché : portefeuille, volatilité, VaR, pricing, risque.

## English

All other modules depend on market data: portfolio, volatility, VaR, pricing and risk.

## Commit

```text
feat: add market data module
```

---

# 7. Phase 4 — Portfolio Builder  
# Phase 4 — Construction de portefeuille

## Goal / Objectif

## Français

Permettre à l’utilisateur de créer un portefeuille.

## English

Allow the user to create a portfolio.

## Tasks / Tâches

Backend:

- Create `Portfolio`.
- Create `Position`.
- Add CRUD routes.
- Calculate portfolio value.
- Calculate portfolio weights.

Frontend:

- Create `Portfolio Builder` page.
- Add positions table.
- Add position form.
- Show allocation chart.

## Commit

```text
feat: add portfolio builder
```

---

# 8. Phase 5 — Performance and Volatility  
# Phase 5 — Performance et volatilité

## Goal / Objectif

## Français

Calculer les premières métriques quantitatives.

## English

Calculate the first quantitative metrics.

## Metrics / Métriques

- Total return / Rendement total
- Annualized return / Rendement annualisé
- Daily volatility / Volatilité journalière
- Annualized volatility / Volatilité annualisée
- Sharpe ratio
- Max drawdown
- Rolling volatility / Volatilité roulante

## Pages

```text
Performance Analytics
Volatility Lab
```

## Commit

```text
feat: add performance and volatility analytics
```

---

# 9. Phase 6 — Risk Engine: VaR and CVaR  
# Phase 6 — Moteur de risque : VaR et CVaR

## Goal / Objectif

## Français

Créer le premier vrai module de risque middle office.

## English

Create the first real middle-office risk module.

## Tasks / Tâches

- Historical VaR / VaR historique
- Parametric VaR / VaR paramétrique
- CVaR / Expected Shortfall
- Loss distribution chart / Graphique de distribution des pertes
- Unit tests / Tests unitaires

## Page

```text
Risk Monitor
```

## Commit

```text
feat: add var and cvar risk engine
```

---

# 10. Phase 7 — Trade Simulator  
# Phase 7 — Simulateur de transactions

## Goal / Objectif

## Français

Simuler un trade avant de l’exécuter.

## English

Simulate a trade before execution.

## Tasks / Tâches

- Buy an asset / Acheter un actif
- Sell an asset / Vendre un actif
- Compare before and after portfolio / Comparer portefeuille avant et après
- Show impact on:
  - weights / poids
  - exposure / exposition
  - VaR
  - CVaR
  - volatility / volatilité

## Page

```text
Trade Simulator
```

## Commit

```text
feat: add trade simulator
```

---

# 11. Phase 8 — Options Pricing Lab  
# Phase 8 — Laboratoire de pricing d’options

## Goal / Objectif

## Français

Ajouter le pricing d’options call et put.

## English

Add call and put option pricing.

## Tasks / Tâches

- European call / Call européen
- European put / Put européen
- Black-Scholes
- d1 / d2
- Delta
- Gamma
- Vega
- Theta
- Rho
- Put-call parity test

## Page

```text
Options Pricing Lab
```

## Commit

```text
feat: add black scholes option pricing
```

---

# 12. Phase 9 — Rates Lab  
# Phase 9 — Laboratoire des taux

## Goal / Objectif

## Français

Ajouter les obligations et les taux.

## English

Add bonds and interest rates.

## Tasks / Tâches

- Yield curve / Courbe des taux
- Spot rates / Taux spot
- Discount factors / Facteurs d’actualisation
- Bond pricing / Pricing obligataire
- Duration
- Rate shock stress test / Stress test de taux

## Page

```text
Rates Lab
```

## Commit

```text
feat: add rates and bond pricing module
```

---

# 13. Phase 10 — RiskDNA Engine  
# Phase 10 — Moteur RiskDNA

## Goal / Objectif

## Français

Créer la fonctionnalité signature du projet.

## English

Create the project’s signature feature.

## RiskDNA combines / RiskDNA combine

- VaR
- CVaR
- Volatility / Volatilité
- Sector concentration / Concentration sectorielle
- Stress test
- Option Greeks
- Rate duration / Duration taux
- AI anomaly detection / Détection d’anomalies IA

## Output / Résultat

```text
Low / Medium / High / Critical
```

Example / Exemple:

```text
RiskDNA: High
This trade increases technology concentration and raises portfolio CVaR above the internal limit.
```

```text
RiskDNA : Élevé
Cette transaction augmente la concentration technologique et fait passer la CVaR au-dessus de la limite interne.
```

## Commit

```text
feat: add riskdna engine
```

---

# 14. Phase 11 — Reports and AI  
# Phase 11 — Rapports et IA

## Goal / Objectif

## Français

Générer des rapports professionnels en français et en anglais.

## English

Generate professional reports in French and English.

## Reports / Rapports

- Daily risk report / Rapport de risque quotidien
- Trade impact report / Rapport d’impact d’un trade
- Options pricing report / Rapport de pricing d’options
- Rates report / Rapport de taux
- P&L report / Rapport P&L

## AI role / Rôle de l’IA

The AI does not replace calculations.  
L’IA ne remplace pas les calculs.

It explains, summarizes and detects anomalies.  
Elle explique, résume et détecte les anomalies.

## Commit

```text
feat: add ai risk reports
```

---

# 15. Phase 12 — Final Polish  
# Phase 12 — Finition finale

## Goal / Objectif

## Français

Rendre le projet présentable pour GitHub, LinkedIn, CV et entrevue.

## English

Make the project ready for GitHub, LinkedIn, resume and interviews.

## Tasks / Tâches

- Final README
- Screenshots
- Demo script
- Architecture diagram
- Tests
- GitHub Actions
- Docker setup
- LinkedIn post
- CV bullets

## Commit

```text
docs: polish project documentation
```

---

# 16. Immediate Next Steps / Prochaines étapes immédiates

## Français

Ce que tu dois faire maintenant :

1. Ajouter ce fichier dans `docs/project-plan.md`.
2. Ajouter ou améliorer `README.md`.
3. Vérifier que `docs/athena_detailed_plan.md` est aussi présent.
4. Commit et push.
5. Créer une branche :

```text
feature/project-foundation
```

6. Commencer le backend FastAPI et le frontend React.

## English

What you should do now:

1. Add this file as `docs/project-plan.md`.
2. Add or improve `README.md`.
3. Make sure `docs/athena_detailed_plan.md` is also present.
4. Commit and push.
5. Create a branch:

```text
feature/project-foundation
```

6. Start the FastAPI backend and React frontend.

---

# 17. Commands / Commandes

## Add this plan / Ajouter ce plan

```powershell
git add docs/project-plan.md
git commit -m "docs: add simple project plan"
git push
```

## Create next branch / Créer la prochaine branche

```powershell
git checkout -b feature/project-foundation
git push -u origin feature/project-foundation
```

---

# 18. Simple Priority Order / Ordre de priorité simple

```text
1. README
2. Simple project plan
3. Backend health endpoint
4. Frontend homepage
5. Market data
6. Portfolio builder
7. Performance and volatility
8. VaR and CVaR
9. Trade simulator
10. Options pricing
11. Rates lab
12. RiskDNA
13. Reports and AI
14. Final polish
```

---

# 19. One-Sentence Pitch / Pitch en une phrase

## English

Athena AI Risk Terminal is a bilingual AI-powered quantitative finance platform connecting front-office trading decisions with middle-office risk controls.

## Français

Athena AI Risk Terminal est une plateforme financière quantitative bilingue propulsée par l’IA qui relie les décisions front office aux contrôles de risque middle office.
