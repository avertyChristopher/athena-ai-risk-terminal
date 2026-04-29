# 06 — Testing and DevOps

**Project:** Athena AI Risk Terminal  
**Recommended file path:** `docs/libraries/06-testing-and-devops.md`  
**Purpose:** understand how to make Athena reliable, testable, maintainable and ready for professional development using automated tests, code quality tools, Docker, CI/CD and clean development workflows.  
**Scope:** this document focuses on testing and DevOps practices for Athena: backend tests, frontend tests, integration tests, end-to-end tests, GitHub Actions, Docker, docker-compose, environment variables, linting, formatting, coverage, pre-commit and deployment basics.

---

## Table of Contents

1. What is testing?
2. Why testing matters for Athena
3. What is DevOps?
4. Why DevOps matters for Athena
5. Testing pyramid
6. Unit tests
7. Integration tests
8. API tests
9. End-to-end tests
10. Regression tests
11. Smoke tests
12. Backend testing overview
13. pytest overview
14. Backend unit tests
15. Testing finance formulas
16. Testing VaR and CVaR
17. Testing Black-Scholes
18. Testing Greeks
19. Testing portfolio calculations
20. Testing P&L attribution
21. Testing RiskDNA scoring
22. Testing data validation
23. Testing FastAPI routes
24. FastAPI TestClient
25. Testing database repositories
26. Test database strategy
27. Test fixtures
28. Mocking external services
29. Mocking market data
30. Mocking AI services
31. Frontend testing overview
32. Vitest overview
33. React Testing Library overview
34. Testing utility functions
35. Testing formatters
36. Testing components
37. Testing forms
38. Testing tables
39. Testing charts
40. Testing loading states
41. Testing error states
42. Testing empty states
43. API mocking in frontend tests
44. End-to-end testing overview
45. Playwright overview
46. Cypress overview
47. Recommended E2E strategy
48. Critical Athena E2E workflows
49. Test data management
50. Code coverage
51. Coverage limits
52. Linting overview
53. Ruff for Python
54. Black for Python
55. ESLint for frontend
56. Prettier for frontend
57. Type checking
58. mypy overview
59. TypeScript checking
60. Pre-commit hooks
61. Git workflow
62. Branching strategy
63. Commit messages
64. Pull requests
65. Code review checklist
66. GitHub Actions overview
67. CI pipeline overview
68. Backend CI job
69. Frontend CI job
70. Documentation CI job
71. Security checks
72. Dependency management
73. Environment variables
74. `.env` files
75. Secrets management
76. Docker overview
77. Dockerfile for backend
78. Dockerfile for frontend
79. docker-compose overview
80. docker-compose for Athena
81. PostgreSQL in Docker
82. Redis in Docker
83. Local development workflow
84. Database migrations in DevOps
85. Alembic in CI/CD
86. Build artifacts
87. Deployment basics
88. Staging vs production
89. Observability basics
90. Logging
91. Error tracking
92. Monitoring
93. Backup basics
94. Data safety
95. Common beginner mistakes
96. Suggested scripts
97. Suggested folder structure
98. Suggested GitHub Actions workflow
99. Athena quality checklist
100. Summary

---

## 1. What is testing?

Testing means checking that software behaves as expected.

A test defines:

```text
Given some input
When an action happens
Then the output should match expectations
```

Example:

```text
Given prices 100 and 105
When simple return is calculated
Then the return should be 5%
```

Testing is especially important in finance because small mistakes can produce misleading results.

A wrong formula can affect:

```text
portfolio value
VaR
CVaR
option prices
Greeks
P&L
RiskDNA
reports
```

Testing helps protect Athena from hidden errors.

---

## 2. Why testing matters for Athena

Athena is not a simple static website.

It is a finance/risk platform.

It calculates:

```text
returns
volatility
VaR
CVaR
stress losses
Black-Scholes prices
Greeks
portfolio weights
P&L attribution
RiskDNA scores
reports
```

If those calculations are wrong, the whole product loses credibility.

Testing matters because it gives confidence that:

```text
formulas are correct
APIs behave correctly
forms validate inputs
charts receive correct data
reports include required sections
risk warnings are not hidden
changes do not break old features
```

### Core Athena principle

```text
A finance project without tests is not reliable.
```

---

## 3. What is DevOps?

DevOps is the set of practices that connect development, testing, deployment and operations.

It includes:

```text
automation
CI/CD
Docker
environment configuration
testing pipelines
code quality checks
deployment workflows
monitoring
logging
```

Simple idea:

```text
DevOps makes the project easier to run, test, ship and maintain.
```

For Athena, DevOps helps ensure that the project works not only on your machine but also in a repeatable environment.

---

## 4. Why DevOps matters for Athena

Athena has several moving parts:

```text
frontend
backend
database
Redis later
notebooks
docs
tests
Docker
GitHub Actions
```

Without DevOps, setup becomes confusing.

Good DevOps gives:

```text
repeatable local environment
automated tests
clean builds
consistent formatting
safe environment variables
database migrations
deployment readiness
```

### Athena example

With Docker Compose:

```text
one command starts backend, PostgreSQL and Redis
```

With GitHub Actions:

```text
each push runs tests and lint checks automatically
```

This makes Athena more professional.

---

## 5. Testing pyramid

The testing pyramid describes the balance between test types.

```text
Many unit tests
Some integration tests
Few end-to-end tests
```

### Unit tests

Fast, small, focused.

Example:

```text
test annualized volatility formula
```

### Integration tests

Check multiple parts together.

Example:

```text
API route + service + database
```

### End-to-end tests

Simulate real user workflows.

Example:

```text
user creates portfolio, adds position, runs risk calculation
```

### Athena recommendation

Use many backend formula tests, many component tests, some API/database tests and a small number of critical E2E tests.

---

## 6. Unit tests

Unit tests test one small piece of logic.

Example:

```python
def test_simple_return():
    result = calculate_simple_return(100, 105)
    assert result == 0.05
```

Unit tests should be:

```text
fast
deterministic
focused
easy to understand
```

### Athena unit test examples

```text
simple return calculation
annualized volatility
historical VaR
historical CVaR
Black-Scholes call price
Delta calculation
P&L calculation
RiskDNA score mapping
```

Unit tests are the foundation of quality.

---

## 7. Integration tests

Integration tests check whether multiple parts work together.

Example:

```text
FastAPI route
    ↓
Service
    ↓
Repository
    ↓
Database
```

Integration test example:

```text
Create a portfolio through API.
Retrieve it through API.
Check it exists in database.
```

### Athena integration test examples

```text
Create portfolio and add positions
Calculate risk using stored market data
Generate report from stored risk metrics
Simulate trade with real portfolio data
```

Integration tests are slower than unit tests but catch important system issues.

---

## 8. API tests

API tests check backend endpoints.

Example:

```text
GET /api/health returns 200
POST /api/options/black-scholes/price returns call and put prices
POST /api/trades/simulate returns before/after impact
```

API tests verify:

```text
status code
response body
validation errors
error messages
data shape
```

### Athena rule

Every important endpoint should have at least one success test and one invalid-input test.

---

## 9. End-to-end tests

End-to-end tests simulate real user behavior in the browser.

Example:

```text
Open Athena
Create portfolio
Add AAPL position
Run risk calculation
See VaR result
Generate report
```

E2E tests are valuable because they test the full system.

But they are also:

```text
slower
more fragile
more expensive to maintain
```

### Athena recommendation

Use E2E tests for critical workflows only.

Do not test every small detail with E2E tests.

---

## 10. Regression tests

Regression tests make sure old features keep working after changes.

Example:

```text
A bug once caused CVaR to be lower than VaR.
Add a regression test so it never happens again.
```

Regression test principle:

```text
Every important bug fix should add a test.
```

### Athena examples

```text
Trade simulation should not mutate original portfolio.
CVaR should be greater than or equal to VaR for loss distributions.
RiskDNA critical breach should not be downgraded by average score.
```

Regression tests are extremely valuable for long-term stability.

---

## 11. Smoke tests

Smoke tests are quick checks that the system basically runs.

Examples:

```text
Backend starts
Health endpoint returns OK
Frontend builds
Database connection works
```

Smoke tests do not test everything.

They answer:

```text
Is the application basically alive?
```

### Athena smoke tests

```text
GET /api/health
npm run build
pytest simple health test
docker compose starts services
```

Smoke tests are useful in CI and deployment.

---

## 12. Backend testing overview

Backend testing should cover:

```text
domain formulas
service logic
repositories
API endpoints
database integration
error handling
validation
background jobs later
```

Recommended tools:

```text
pytest
FastAPI TestClient
httpx
pytest-cov
factory_boy optional
freezegun optional
```

### Athena backend test folders

```text
backend/app/tests/
├── unit/
├── integration/
├── api/
└── fixtures/
```

### Rule

The backend is where official calculations live, so backend tests are critical.

---

## 13. pytest overview

pytest is the main Python testing framework.

Install:

```bash
pip install pytest
```

Run tests:

```bash
pytest
```

Example:

```python
def add(a: int, b: int) -> int:
    return a + b

def test_add():
    assert add(2, 3) == 5
```

### Why pytest is good

```text
simple syntax
fixtures
parametrized tests
good error messages
large ecosystem
```

### Athena use

Use pytest for all backend tests.

---

## 14. Backend unit tests

Backend unit tests should focus on pure logic.

Example:

```python
def annualized_volatility(daily_volatility: float, periods_per_year: int = 252) -> float:
    return daily_volatility * periods_per_year ** 0.5

def test_annualized_volatility():
    result = annualized_volatility(0.01)
    assert round(result, 6) == round(0.01 * 252 ** 0.5, 6)
```

### Athena unit test targets

```text
market data functions
return functions
risk functions
option pricing functions
portfolio functions
P&L functions
RiskDNA functions
```

Unit tests should not require a database.

---

## 15. Testing finance formulas

Finance formulas need known test cases.

Good test case structure:

```text
Given known input
Expected output calculated manually or from trusted reference
Compare with tolerance
```

Use tolerances for floating point.

Example:

```python
assert abs(result - expected) < 1e-6
```

### Athena rule

Never compare complex floating values with exact equality unless they are integers or controlled decimals.

Use:

```python
pytest.approx()
```

Example:

```python
assert result == pytest.approx(expected, rel=1e-6)
```

---

## 16. Testing VaR and CVaR

Historical VaR test:

```python
import pandas as pd
import pytest

def historical_var(losses: pd.Series, confidence_level: float) -> float:
    return float(losses.quantile(confidence_level))

def test_historical_var():
    losses = pd.Series([1, 2, 3, 4, 5])
    result = historical_var(losses, 0.8)
    assert result == pytest.approx(4.2)
```

CVaR test:

```python
def historical_cvar(losses: pd.Series, confidence_level: float) -> float:
    var = losses.quantile(confidence_level)
    return float(losses[losses >= var].mean())

def test_cvar_is_at_least_var():
    losses = pd.Series([1, 2, 3, 4, 5])
    var = historical_var(losses, 0.8)
    cvar = historical_cvar(losses, 0.8)
    assert cvar >= var
```

### Athena rule

For positive loss distributions:

```text
CVaR should usually be >= VaR.
```

---

## 17. Testing Black-Scholes

Black-Scholes should be tested with known values.

Example common case:

```text
S = 100
K = 100
T = 1
r = 0.05
sigma = 0.20
q = 0
```

Expected approximate call price:

```text
10.45
```

Test:

```python
def test_black_scholes_call_price():
    result = black_scholes_call(
        spot=100,
        strike=100,
        time_to_maturity=1,
        risk_free_rate=0.05,
        volatility=0.20,
        dividend_yield=0.0,
    )

    assert result == pytest.approx(10.45, rel=1e-2)
```

### Athena rule

Test both call and put prices.

Also test put-call parity.

---

## 18. Testing Greeks

Greeks should be tested for reasonable values.

For a standard call option:

```text
Delta should be between 0 and 1
Gamma should be positive
Vega should usually be positive
Theta may be negative for long calls
```

Example:

```python
def test_call_delta_between_zero_and_one():
    delta = calculate_call_delta(...)
    assert 0 <= delta <= 1
```

### Better tests

Compare with known reference values or finite difference approximations.

Example finite difference:

```text
Delta ≈ price(S + h) - price(S - h) / (2h)
```

### Athena use

Greeks are important, so they deserve dedicated tests.

---

## 19. Testing portfolio calculations

Portfolio calculations include:

```text
market value
weights
total value
exposures
returns
```

Example:

```python
def test_position_market_value():
    quantity = 10
    price = 200
    result = quantity * price
    assert result == 2000
```

Portfolio weights:

```python
def test_weights_sum_to_one():
    market_values = pd.Series([2000, 3000, 5000])
    weights = market_values / market_values.sum()
    assert weights.sum() == pytest.approx(1.0)
```

### Athena rule

Weights should sum to 1 unless cash or leverage is handled separately.

---

## 20. Testing P&L attribution

P&L attribution tests should verify:

```text
daily P&L
position P&L
explained P&L
unexplained P&L
top contributors
fees
FX effect
```

Example:

```python
def test_position_pnl():
    quantity = 50
    beginning_price = 100
    ending_price = 108

    pnl = quantity * (ending_price - beginning_price)

    assert pnl == 400
```

Explained/unexplained:

```python
def test_explained_plus_unexplained_equals_total():
    total = -2400
    explained = -2050
    unexplained = total - explained

    assert explained + unexplained == total
```

---

## 21. Testing RiskDNA scoring

RiskDNA tests should verify score logic.

Examples:

```text
score is between 0 and 100
risk level matches score range
high VaR usage increases score
limit breach increases score
critical breach applies override
top drivers are ranked correctly
```

Example:

```python
def test_risk_level_mapping():
    assert map_score_to_level(20) == "Low"
    assert map_score_to_level(45) == "Medium"
    assert map_score_to_level(70) == "High"
    assert map_score_to_level(90) == "Critical"
```

### Athena rule

RiskDNA should be deterministic and testable.

AI should not determine official RiskDNA score.

---

## 22. Testing data validation

Data validation tests protect calculations.

Examples:

```text
negative price is rejected
missing adjusted close creates warning
duplicate symbol-date rows are detected
confidence level outside 0-1 is rejected
volatility <= 0 is rejected
quantity <= 0 is rejected
```

Example:

```python
def test_negative_price_is_invalid():
    with pytest.raises(ValueError):
        validate_price(negative_price=-100)
```

### Athena rule

Invalid data should fail early and clearly.

---

## 23. Testing FastAPI routes

FastAPI routes should be tested with a test client.

Example:

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

### Athena route tests

```text
GET /api/health
POST /api/options/black-scholes/price
POST /api/risk/{portfolio_id}/historical-var
POST /api/trades/simulate
GET /api/reports/{portfolio_id}
```

---

## 24. FastAPI TestClient

FastAPI TestClient simulates HTTP requests.

Example:

```python
def test_invalid_option_request_returns_422():
    response = client.post("/api/options/black-scholes/price", json={
        "spot_price": -100,
        "strike_price": 100,
        "time_to_maturity": 1,
        "risk_free_rate": 0.05,
        "volatility": 0.2
    })

    assert response.status_code == 422
```

### Why this matters

It confirms that Pydantic validation works at the API boundary.

### Athena rule

Every endpoint should test invalid input.

---

## 25. Testing database repositories

Repository tests check database access.

Example repository behavior:

```text
save portfolio
get portfolio by id
list portfolios
delete portfolio
filter trades by status
retrieve latest risk metric
```

Test example concept:

```python
def test_save_and_get_portfolio(db_session):
    repo = PortfolioRepository(db_session)
    portfolio = Portfolio(id="pf_001", name="Growth", base_currency="CAD")

    repo.save(portfolio)
    result = repo.get_by_id("pf_001")

    assert result.name == "Growth"
```

### Athena rule

Repository tests should use a test database.

---

## 26. Test database strategy

Use a separate database for tests.

Do not use development or production data.

Options:

```text
SQLite in-memory for simple tests
PostgreSQL test database for realistic tests
Dockerized PostgreSQL for CI
```

### Athena recommendation

For early development:

```text
SQLite may be acceptable for simple repository tests.
```

For more realistic tests:

```text
Use PostgreSQL test database.
```

Since Athena uses PostgreSQL, test with PostgreSQL when possible.

---

## 27. Test fixtures

Fixtures provide reusable test data.

pytest fixture example:

```python
import pytest

@pytest.fixture
def sample_returns():
    return pd.Series([0.01, -0.02, 0.015, 0.005])
```

Use:

```python
def test_volatility(sample_returns):
    result = annualized_volatility(sample_returns)
    assert result > 0
```

### Athena useful fixtures

```text
sample_prices
sample_returns
sample_portfolio
sample_positions
sample_trades
sample_risk_metrics
sample_option_inputs
```

Fixtures reduce repetition.

---

## 28. Mocking external services

Mocking replaces external dependencies with controlled fake behavior.

External services:

```text
market data APIs
AI APIs
email services
file storage
payment systems if any
```

Why mock?

```text
tests are faster
tests are deterministic
tests do not need internet
tests do not spend API credits
tests avoid provider failures
```

### Athena use

Mock:

```text
yfinance
OpenAI API
external data providers
report storage
```

---

## 29. Mocking market data

Market data should be mocked in tests.

Example fake data:

```python
@pytest.fixture
def sample_market_prices():
    return pd.DataFrame({
        "date": ["2026-04-27", "2026-04-28", "2026-04-29"],
        "symbol": ["AAPL", "AAPL", "AAPL"],
        "adjusted_close": [100, 102, 101],
    })
```

### Why

Real market data changes and may not be available.

Tests should not depend on external downloads.

### Athena rule

Use fixed sample data for tests.

---

## 30. Mocking AI services

AI services should be mocked in tests.

Example fake AI response:

```python
class FakeAIService:
    def generate(self, prompt: str) -> str:
        return '{"summary": "Risk is high.", "warnings": []}'
```

### Why

AI output can vary.

API calls can cost money.

Tests should be deterministic.

### Athena tests

```text
AI explanation service validates structured output
AI output is stored as draft
AI provider failure returns fallback explanation
AI output with invented numbers is rejected
```

---

## 31. Frontend testing overview

Frontend testing checks UI behavior.

Tools:

```text
Vitest
React Testing Library
Mock Service Worker
Playwright or Cypress
```

Test targets:

```text
utility functions
formatters
components
forms
tables
loading states
error states
empty states
API interactions
critical workflows
```

### Athena rule

Test the UI behavior that matters to users.

Do not test implementation details too much.

---

## 32. Vitest overview

Vitest is a fast testing framework for Vite projects.

Install:

```bash
npm install -D vitest
```

Example:

```ts
import { describe, expect, it } from "vitest";

describe("basic math", () => {
  it("adds numbers", () => {
    expect(2 + 2).toBe(4);
  });
});
```

Run:

```bash
npm run test
```

Script:

```json
{
  "scripts": {
    "test": "vitest"
  }
}
```

### Athena use

Use Vitest for frontend unit and component tests.

---

## 33. React Testing Library overview

React Testing Library helps test React components as users see them.

Install:

```bash
npm install -D @testing-library/react @testing-library/jest-dom
```

Example:

```tsx
import { render, screen } from "@testing-library/react";
import { MetricCard } from "./MetricCard";

it("renders metric title and value", () => {
  render(<MetricCard title="VaR" value="12,500 CAD" />);

  expect(screen.getByText("VaR")).toBeInTheDocument();
  expect(screen.getByText("12,500 CAD")).toBeInTheDocument();
});
```

### Athena use

Test cards, forms, tables and panels.

---

## 34. Testing utility functions

Utility functions are easy to test.

Examples:

```text
formatCurrency
formatPercent
formatDate
mapRiskLevelToLabel
calculateDisplayStatus
```

Example:

```ts
import { expect, it } from "vitest";
import { formatPercent } from "@/lib/formatters";

it("formats percent", () => {
  expect(formatPercent(0.1234)).toBe("12.34%");
});
```

### Athena rule

Shared formatters should be tested because financial display matters.

---

## 35. Testing formatters

Formatters are important for:

```text
currencies
percentages
dates
large numbers
basis points
```

Example tests:

```ts
it("formats CAD currency", () => {
  expect(formatCurrency(12500, "CAD")).toContain("12,500");
});

it("formats percentage", () => {
  expect(formatPercent(0.05)).toBe("5.00%");
});
```

### Athena caution

Formatting depends on locale.

Tests may need stable locale configuration.

---

## 36. Testing components

Component tests verify rendering.

Example Athena components:

```text
MetricCard
RiskLevelBadge
StatusBadge
GreeksTable
RiskDriverTable
ErrorState
EmptyState
```

Example:

```tsx
it("renders critical risk badge", () => {
  render(<RiskLevelBadge level="Critical" />);
  expect(screen.getByText("Critical")).toBeInTheDocument();
});
```

### Rule

Test visible behavior, not internal component state.

---

## 37. Testing forms

Forms should be tested for:

```text
required fields
validation messages
submit behavior
disabled states
API mutation call
```

Example:

```text
Option form rejects negative volatility.
Trade form rejects quantity <= 0.
Portfolio form requires name.
```

### Athena form tests

```text
TradeTicketForm validates quantity
OptionPricingForm validates volatility
RiskScenarioForm validates numeric shocks
ReportGenerationForm submits selected report type
```

Forms are important because they protect backend from bad inputs and improve UX.

---

## 38. Testing tables

Tables should be tested for:

```text
rows render correctly
empty state appears
status badges appear
sorting works if implemented
filtering works if implemented
pagination controls appear
```

Example:

```tsx
expect(screen.getByText("AAPL")).toBeInTheDocument();
expect(screen.getByText("MSFT")).toBeInTheDocument();
```

### Athena table tests

```text
PositionTable renders positions
RiskDriverTable renders top drivers
PnlContributorTable ranks contributors
ReportsTable shows statuses
```

---

## 39. Testing charts

Charts are harder to test visually.

Do not test exact SVG internals unless necessary.

Test:

```text
chart renders title
chart receives data
empty state appears with no data
important labels appear
```

Example:

```tsx
render(<PnLChart data={sampleData} />);
expect(screen.getByText("Daily P&L")).toBeInTheDocument();
```

### Athena rule

Test data transformation separately from chart rendering.

---

## 40. Testing loading states

Loading states should appear when data is loading.

Example:

```tsx
expect(screen.getByText("Loading risk metrics...")).toBeInTheDocument();
```

Athena loading states:

```text
Loading portfolio
Loading risk metrics
Generating report
Calculating option price
Simulating trade
```

### Why

Users need feedback when calculations or API requests take time.

---

## 41. Testing error states

Error states should appear when API calls fail.

Examples:

```text
Unable to load portfolio.
Unable to calculate risk.
Report generation failed.
```

Test:

```tsx
expect(screen.getByText("Unable to load risk metrics.")).toBeInTheDocument();
```

### Athena rule

Do not let errors fail silently.

---

## 42. Testing empty states

Empty states should guide the user.

Examples:

```text
No portfolios yet.
No reports generated.
No market data available.
No trades found.
```

Test:

```tsx
expect(screen.getByText("No portfolios yet.")).toBeInTheDocument();
```

### Athena rule

Every page that depends on data should have an empty state.

---

## 43. API mocking in frontend tests

Mock APIs so frontend tests do not require backend.

Options:

```text
Mock Service Worker
manual mocks
Vitest fetch mocks
```

Example concept:

```text
Mock GET /api/portfolios to return sample portfolios.
Render PortfolioPage.
Check portfolio names appear.
```

### Athena use

Mock:

```text
portfolios
risk metrics
reports
trade simulation results
AI explanations
```

---

## 44. End-to-end testing overview

E2E testing checks the full application in a browser.

Tools:

```text
Playwright
Cypress
```

E2E tests simulate real user workflows.

Example:

```text
User opens app
User creates portfolio
User adds position
User views risk dashboard
```

### Athena recommendation

Use E2E tests only for critical workflows.

Keep them stable and not too numerous.

---

## 45. Playwright overview

Playwright is an E2E testing framework.

Install:

```bash
npm init playwright@latest
```

Example:

```ts
import { test, expect } from "@playwright/test";

test("home page loads", async ({ page }) => {
  await page.goto("http://localhost:5173");
  await expect(page.getByText("Athena")).toBeVisible();
});
```

### Athena use

Playwright is a strong option for:

```text
critical user workflows
cross-browser tests
CI E2E tests later
```

---

## 46. Cypress overview

Cypress is another popular E2E testing framework.

It is good for:

```text
interactive test runner
frontend workflows
component testing options
```

Example:

```ts
describe("Athena dashboard", () => {
  it("loads dashboard", () => {
    cy.visit("/");
    cy.contains("Athena");
  });
});
```

### Athena choice

Either Playwright or Cypress is fine.

Recommendation:

```text
Use Playwright if you want modern cross-browser E2E.
Use Cypress if your course/team already uses it.
```

Do not use both at the beginning.

---

## 47. Recommended E2E strategy

Start with a few high-value E2E tests.

Recommended E2E workflows:

```text
Application loads
Create portfolio
View portfolio dashboard
Run option pricing
Simulate trade
Generate report draft
Switch language
```

Do not test every button with E2E.

Use component and unit tests for smaller behavior.

### Athena rule

E2E tests should be stable and meaningful.

---

## 48. Critical Athena E2E workflows

Critical workflows:

### Workflow 1 — Health

```text
Open app
Dashboard loads
Navigation works
```

### Workflow 2 — Portfolio

```text
Create portfolio
Add position
View total value
```

### Workflow 3 — Risk

```text
Select portfolio
Run risk calculation
See VaR/CVaR cards
```

### Workflow 4 — Options

```text
Open options page
Enter valid inputs
See call price, put price and Greeks
```

### Workflow 5 — Reports

```text
Generate report
Preview report
See draft status
```

---

## 49. Test data management

Good tests need controlled data.

Test data should be:

```text
small
clear
deterministic
realistic enough
easy to reset
```

Examples:

```text
sample portfolio with AAPL and MSFT
sample returns series
sample option input
sample risk metrics
sample P&L data
```

### Athena folder

```text
backend/app/tests/fixtures/
frontend/src/test/fixtures/
```

### Rule

Tests should not depend on personal or external data.

---

## 50. Code coverage

Code coverage measures how much code is executed by tests.

Python:

```bash
pytest --cov=app
```

Frontend:

```bash
vitest --coverage
```

Coverage can help find untested areas.

### Important

High coverage does not guarantee good tests.

Bad tests can cover code without checking meaningful behavior.

### Athena goal

Focus coverage on:

```text
finance formulas
risk services
validation
critical API routes
core frontend components
```

---

## 51. Coverage limits

Coverage targets can be useful but should be realistic.

Example targets:

```text
backend domain functions: high coverage
backend routes: medium coverage
frontend utilities: high coverage
frontend visual pages: moderate coverage
E2E: only critical workflows
```

### Athena recommendation

Start with:

```text
meaningful tests first
coverage target later
```

Do not chase 100% coverage if tests become useless.

---

## 52. Linting overview

Linting checks code for style and potential errors.

Backend linting:

```text
Ruff
```

Frontend linting:

```text
ESLint
```

Linting helps catch:

```text
unused imports
bad patterns
formatting issues
possible bugs
inconsistent style
```

### Athena use

Run linting before commits and in CI.

---

## 53. Ruff for Python

Ruff is a fast Python linter and formatter tool.

Install:

```bash
pip install ruff
```

Run:

```bash
ruff check backend/
```

Fix:

```bash
ruff check backend/ --fix
```

### Athena use

Ruff helps keep backend code clean.

It can catch:

```text
unused imports
unused variables
style problems
simple bugs
```

---

## 54. Black for Python

Black formats Python code automatically.

Install:

```bash
pip install black
```

Run:

```bash
black backend/
```

Check without formatting:

```bash
black --check backend/
```

### Athena use

Black makes formatting consistent.

Use Black with Ruff.

### Rule

Do not waste time manually formatting Python code.

Let tools do it.

---

## 55. ESLint for frontend

ESLint checks TypeScript/React code.

Run:

```bash
npm run lint
```

It can catch:

```text
unused variables
bad React hooks usage
syntax issues
style problems
```

### Athena use

ESLint helps keep the frontend maintainable.

It should run in CI.

---

## 56. Prettier for frontend

Prettier formats frontend code.

Install:

```bash
npm install -D prettier
```

Run:

```bash
npx prettier . --write
```

Check:

```bash
npx prettier . --check
```

### Athena use

Prettier keeps formatting consistent for:

```text
TypeScript
TSX
JSON
Markdown
CSS
```

---

## 57. Type checking

Type checking catches type-related mistakes.

Backend:

```text
mypy optional
```

Frontend:

```text
TypeScript compiler
```

### Why it matters

Athena has many structured objects:

```text
Portfolio
Position
Trade
RiskMetric
Report
AIExplanation
```

Type checking helps keep these consistent.

---

## 58. mypy overview

mypy checks Python type hints.

Install:

```bash
pip install mypy
```

Run:

```bash
mypy backend/
```

### Athena recommendation

Use type hints from the beginning.

Add mypy when backend structure stabilizes.

mypy can be strict, so do not let it slow early prototyping too much.

---

## 59. TypeScript checking

TypeScript checking runs during frontend build.

Command:

```bash
npm run build
```

Usually includes:

```bash
tsc && vite build
```

### Athena use

This catches:

```text
missing fields
wrong types
invalid props
bad API response assumptions
```

### Rule

The frontend should build successfully before pushing.

---

## 60. Pre-commit hooks

Pre-commit hooks run checks before commits.

Possible checks:

```text
format Python
lint Python
format frontend
lint frontend
run selected tests
prevent secrets
```

Tool:

```text
pre-commit
```

Install:

```bash
pip install pre-commit
```

Run:

```bash
pre-commit install
```

### Athena recommendation

Add pre-commit later after the team workflow is stable.

For now, manually run tests/lint before commits.

---

## 61. Git workflow

Git workflow defines how code changes are managed.

Basic workflow:

```text
pull latest changes
create branch
make changes
run tests
commit
push
open pull request if working with team
merge
```

For solo Athena work, main branch can be acceptable early.

But as the project grows, feature branches are cleaner.

---

## 62. Branching strategy

Recommended branch names:

```text
docs/add-testing-devops-notes
feature/backend-risk-service
feature/frontend-risk-dashboard
fix/var-calculation-edge-case
chore/setup-github-actions
```

### Athena recommendation

For documentation:

```text
docs/...
```

For new features:

```text
feature/...
```

For fixes:

```text
fix/...
```

For tooling:

```text
chore/...
```

### Main branch

Keep `main` stable when possible.

---

## 63. Commit messages

Good commit messages explain what changed.

Examples:

```text
docs: add testing and devops notes
feat: add portfolio risk endpoint
fix: correct cvar tail calculation
test: add black scholes pricing tests
chore: setup backend linting
```

Recommended prefixes:

```text
docs
feat
fix
test
chore
refactor
style
ci
```

### Athena use

Commit messages make the GitHub history professional.

---

## 64. Pull requests

Pull requests are useful even for solo projects.

They help document:

```text
What changed
Why it changed
How it was tested
Screenshots if UI changed
```

PR checklist:

```text
Tests pass
Lint passes
Docs updated
Screenshots included if UI
No secrets committed
```

### Athena use

For a polished GitHub project, PRs show professional workflow.

---

## 65. Code review checklist

Before merging or pushing important work, check:

```text
Does the code solve the right problem?
Are finance formulas tested?
Are inputs validated?
Are errors handled?
Is the API response typed?
Does frontend handle loading/error/empty states?
Are docs updated?
Are secrets excluded?
Does the app still build?
```

### Athena finance-specific checklist

```text
Does the calculation use correct units?
Are currencies clear?
Are dates clear?
Are assumptions documented?
Are edge cases tested?
```

---

## 66. GitHub Actions overview

GitHub Actions runs automated workflows on GitHub.

It can run when you:

```text
push code
open pull request
merge to main
schedule a workflow
```

Common CI tasks:

```text
run backend tests
run frontend tests
lint code
build frontend
check formatting
```

### Athena use

GitHub Actions makes the project look serious and prevents broken code from being merged.

---

## 67. CI pipeline overview

CI means Continuous Integration.

A CI pipeline automatically checks code.

Athena CI should include:

```text
backend lint
backend tests
frontend lint
frontend tests
frontend build
documentation checks optional
```

Basic pipeline:

```text
push to GitHub
      ↓
GitHub Actions starts
      ↓
install dependencies
      ↓
run checks
      ↓
pass or fail
```

### Rule

If CI fails, fix it before continuing.

---

## 68. Backend CI job

Backend CI job can run:

```text
install Python
install dependencies
run ruff
run black check
run pytest
```

Example steps:

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: "3.11"

- run: pip install -r backend/requirements.txt
- run: ruff check backend/
- run: black --check backend/
- run: pytest backend/
```

### Athena use

Backend CI protects finance calculations and API behavior.

---

## 69. Frontend CI job

Frontend CI job can run:

```text
install Node
npm ci
npm run lint
npm run test
npm run build
```

Example:

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: "20"

- run: cd frontend && npm ci
- run: cd frontend && npm run lint
- run: cd frontend && npm run test -- --run
- run: cd frontend && npm run build
```

### Athena use

Frontend CI prevents broken UI builds.

---

## 70. Documentation CI job

Documentation CI is optional but useful.

Possible checks:

```text
Markdown formatting
Broken links
No forbidden TODO markers
Spell check optional
```

Simple start:

```text
Ensure docs folder exists
Ensure required files exist
```

### Athena docs check

Required files:

```text
docs/finance/
docs/libraries/
docs/architecture.md
docs/product-spec.md
```

This is optional but can make the project more professional.

---

## 71. Security checks

Security checks help prevent common risks.

Possible checks:

```text
detect secrets
dependency vulnerability scan
no .env committed
no API keys in code
```

Tools:

```text
GitHub secret scanning
gitleaks
pip-audit
npm audit
```

### Athena rule

Never commit:

```text
API keys
database passwords
OpenAI keys
private credentials
.env with secrets
```

---

## 72. Dependency management

Dependencies should be managed carefully.

Backend:

```text
requirements.txt
pyproject.toml later
```

Frontend:

```text
package.json
package-lock.json
```

### Athena rule

Commit lock files for reproducibility.

For npm:

```text
package-lock.json
```

For Python, you can start with `requirements.txt`.

Later, consider:

```text
Poetry
uv
pip-tools
```

Do not overcomplicate early.

---

## 73. Environment variables

Environment variables configure the app.

Examples:

```text
DATABASE_URL
REDIS_URL
OPENAI_API_KEY
ENVIRONMENT
VITE_API_BASE_URL
SECRET_KEY
```

Backend uses:

```text
DATABASE_URL
OPENAI_API_KEY
```

Frontend uses:

```text
VITE_API_BASE_URL
```

### Athena rule

Do not hardcode environment-specific values in source code.

---

## 74. `.env` files

`.env` files store local environment variables.

Example backend `.env`:

```text
DATABASE_URL=postgresql://athena:athena@localhost:5432/athena
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=replace-me
ENVIRONMENT=development
```

Example frontend `.env`:

```text
VITE_API_BASE_URL=http://localhost:8000
```

### Git rule

Add to `.gitignore`:

```text
.env
.env.local
backend/.env
frontend/.env
```

You can commit examples:

```text
.env.example
backend/.env.example
frontend/.env.example
```

---

## 75. Secrets management

Secrets are sensitive values.

Examples:

```text
API keys
database passwords
JWT secret
cloud credentials
OpenAI key
```

Secrets should be stored in:

```text
local .env files
GitHub Actions secrets
cloud secret manager later
```

Never store secrets in:

```text
README
source code
commits
screenshots
public logs
```

### Athena rule

Use `.env.example` with fake values.

---

## 76. Docker overview

Docker packages an application into containers.

A container includes:

```text
application code
runtime
dependencies
configuration
```

Why Docker helps:

```text
consistent environment
easier setup
works across machines
supports databases locally
deployment preparation
```

### Athena use

Docker can run:

```text
backend
frontend
PostgreSQL
Redis
```

---

## 77. Dockerfile for backend

Example backend Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Athena note

This is a simple starting point.

Later improvements:

```text
non-root user
multi-stage build
health checks
separate dev/prod config
```

---

## 78. Dockerfile for frontend

Example frontend Dockerfile:

```dockerfile
FROM node:20-alpine AS build

WORKDIR /app

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
```

### Athena note

For local development, you may run frontend with:

```bash
npm run dev
```

Dockerized frontend is more useful for production-like builds.

---

## 79. docker-compose overview

Docker Compose runs multiple services together.

Example services:

```text
backend
frontend
postgres
redis
```

Command:

```bash
docker compose up
```

Stop:

```bash
docker compose down
```

### Athena use

Docker Compose can start Athena's local infrastructure.

This makes onboarding easier.

---

## 80. docker-compose for Athena

Example `docker-compose.yml`:

```yaml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: athena
      POSTGRES_PASSWORD: athena
      POSTGRES_DB: athena
    ports:
      - "5432:5432"
    volumes:
      - athena_postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

volumes:
  athena_postgres_data:
```

### Start simple

At first, Docker Compose can include only:

```text
PostgreSQL
Redis
```

Run backend and frontend locally outside Docker.

Later, add backend and frontend services.

---

## 81. PostgreSQL in Docker

PostgreSQL in Docker makes local setup easier.

Start:

```bash
docker compose up postgres
```

Connection:

```text
host = localhost
port = 5432
user = athena
password = athena
database = athena
```

Database URL:

```text
postgresql://athena:athena@localhost:5432/athena
```

### Athena use

This should be used in backend `.env`.

---

## 82. Redis in Docker

Redis in Docker supports caching and background jobs later.

Start:

```bash
docker compose up redis
```

Redis URL:

```text
redis://localhost:6379/0
```

### Athena use

Redis can be added later for:

```text
background report generation
cached risk metrics
job queues
```

Do not use Redis before there is a real need.

---

## 83. Local development workflow

Recommended local workflow:

```text
1. Start PostgreSQL with Docker Compose.
2. Activate backend virtual environment.
3. Run backend migrations.
4. Start FastAPI backend.
5. Start frontend dev server.
6. Open frontend in browser.
7. Open backend docs when needed.
```

Commands example:

```bash
docker compose up postgres redis
```

Backend:

```bash
cd backend
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm run dev
```

---

## 84. Database migrations in DevOps

Migrations update database schema.

Tool:

```text
Alembic
```

Workflow:

```text
Change SQLAlchemy model
Generate migration
Review migration
Apply migration
Commit migration file
```

Commands:

```bash
alembic revision --autogenerate -m "create portfolios table"
alembic upgrade head
```

### Athena rule

Do not manually change database schema without migrations once Alembic is in place.

---

## 85. Alembic in CI/CD

In CI, migrations can be tested.

Example:

```text
Start PostgreSQL service
Install backend dependencies
Run alembic upgrade head
Run tests
```

This confirms migrations apply correctly.

### Athena use

Later CI can include:

```text
migration check
database integration tests
```

Early CI can skip database if setup is not ready.

---

## 86. Build artifacts

Build artifacts are outputs produced by build processes.

Examples:

```text
frontend/dist/
coverage reports
test reports
Docker images
generated reports
```

### Git rule

Do not commit build artifacts unless specifically needed.

Add to `.gitignore`:

```text
frontend/dist/
coverage/
.pytest_cache/
node_modules/
```

### Athena use

CI can generate artifacts like coverage reports later.

---

## 87. Deployment basics

Deployment means running the app somewhere users can access it.

Possible deployment targets:

```text
Render
Railway
Fly.io
AWS
Azure
GCP
Vercel for frontend
Docker server
```

Athena deployment parts:

```text
frontend static app
backend API
PostgreSQL database
Redis optional
environment variables
```

### Early Athena

Focus on local development and GitHub first.

Deploy later when the app has a stable MVP.

---

## 88. Staging vs production

Staging is a test environment similar to production.

Production is the real user-facing environment.

### Staging

Used for:

```text
testing deployment
checking migrations
reviewing features
validating configuration
```

### Production

Used for:

```text
real users
real data
stable releases
```

### Athena

For a personal project:

```text
local = development
deployed demo = staging/demo
production = later if needed
```

---

## 89. Observability basics

Observability means understanding what the application is doing.

It includes:

```text
logs
metrics
traces
alerts
error tracking
```

For Athena, observability helps detect:

```text
API errors
slow calculations
failed reports
database issues
AI provider failures
data ingestion problems
```

### Early Athena

Start with good logging.

Add monitoring later.

---

## 90. Logging

Backend logging should record important events.

Examples:

```text
risk calculation started
risk calculation completed
report generation failed
AI explanation failed validation
database connection error
```

Frontend logging should be minimal and not expose secrets.

### Athena rule

Logs should help debugging but not leak sensitive data.

Do not log:

```text
API keys
passwords
full private portfolio data unnecessarily
```

---

## 91. Error tracking

Error tracking collects application errors.

Tools:

```text
Sentry
Rollbar
Logfire
cloud provider logs
```

### Athena use

Later, use error tracking for:

```text
backend exceptions
frontend crashes
failed report generation
AI validation failures
```

Early stage:

```text
console logs and backend logs are enough
```

---

## 92. Monitoring

Monitoring tracks system health.

Examples:

```text
API response time
error rate
database availability
background job failures
memory usage
CPU usage
```

### Athena later

Monitor:

```text
risk calculation latency
report generation latency
AI request failures
database errors
```

Do not overbuild monitoring before MVP.

---

## 93. Backup basics

Backups protect data.

Important data:

```text
portfolios
positions
trades
reports
risk metrics
P&L records
RiskDNA history
```

For a local project, backups can be manual.

For production, backups should be automated.

### Athena rule

If real user data is stored, backup strategy matters.

---

## 94. Data safety

Data safety means protecting data from loss, corruption and misuse.

Practices:

```text
database backups
input validation
transaction usage
migration review
access control
no secrets in Git
safe deletion strategy
audit trail
```

### Athena finance-specific safety

Financial records should not be silently overwritten.

Use:

```text
versioning
audit events
soft delete where appropriate
```

---

## 95. Common beginner mistakes

### Mistake 1 — No tests

The project becomes fragile.

### Mistake 2 — Only E2E tests

E2E tests are slow and fragile. Use unit tests too.

### Mistake 3 — No validation

Bad data enters the system.

### Mistake 4 — Committing `.env`

Secrets leak.

### Mistake 5 — No CI

Broken code gets pushed unnoticed.

### Mistake 6 — Ignoring failed tests

Tests only matter if failures are fixed.

### Mistake 7 — Overcomplicating Docker too early

Start with database services first.

### Mistake 8 — No migrations

Database changes become chaotic.

### Mistake 9 — No formatting tools

Code becomes inconsistent.

### Mistake 10 — Testing implementation details

Test behavior and outputs, not private internals.

---

## 96. Suggested scripts

### Backend scripts

In backend context:

```bash
pytest
pytest --cov=app
ruff check .
black .
black --check .
mypy app
uvicorn app.main:app --reload
```

### Frontend scripts

In `package.json`:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint .",
    "test": "vitest",
    "test:e2e": "playwright test",
    "format": "prettier . --write",
    "format:check": "prettier . --check"
  }
}
```

### Root scripts later

You can add a Makefile or task runner later.

---

## 97. Suggested folder structure

Recommended structure:

```text
athena-ai-risk-terminal/
├── backend/
│   ├── app/
│   │   ├── tests/
│   │   │   ├── unit/
│   │   │   ├── integration/
│   │   │   ├── api/
│   │   │   └── fixtures/
│   │   └── ...
│   ├── requirements.txt
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   ├── tests/
│   ├── package.json
│   └── playwright.config.ts
├── docs/
│   └── libraries/
│       └── 06-testing-and-devops.md
├── docker-compose.yml
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
└── README.md
```

### Athena principle

Keep tests close to the code they protect, but organized clearly.

---

## 98. Suggested GitHub Actions workflow

Example `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  backend:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install backend dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r backend/requirements.txt

      - name: Lint backend
        run: ruff check backend/

      - name: Check backend formatting
        run: black --check backend/

      - name: Test backend
        run: pytest backend/

  frontend:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: "20"

      - name: Install frontend dependencies
        run: cd frontend && npm ci

      - name: Lint frontend
        run: cd frontend && npm run lint

      - name: Test frontend
        run: cd frontend && npm run test -- --run

      - name: Build frontend
        run: cd frontend && npm run build
```

### Athena note

Adjust paths when the actual project files exist.

---

## 99. Athena quality checklist

Before pushing important work, check:

```text
Backend tests pass
Frontend tests pass
Backend lint passes
Frontend lint passes
Frontend builds
No secrets committed
.env files ignored
Docs updated
API docs still work
Database migrations reviewed
Finance formulas tested
Invalid inputs tested
Loading/error/empty states handled
```

### Before LinkedIn/GitHub showcase

Check:

```text
README is clear
Screenshots included
Architecture documented
Setup instructions work
CI badge visible
Demo data available
No private data
No broken links
```

---

## 100. Summary

Testing and DevOps make Athena reliable and professional.

Testing protects:

```text
financial formulas
backend APIs
frontend behavior
database logic
AI output validation
reports
critical workflows
```

DevOps supports:

```text
repeatable setup
Docker
CI/CD
linting
formatting
environment variables
migrations
deployment readiness
observability
```

Recommended tools:

```text
pytest
FastAPI TestClient
Vitest
React Testing Library
Playwright or Cypress
Ruff
Black
ESLint
Prettier
GitHub Actions
Docker
docker-compose
PostgreSQL
Redis later
```

Most important principle:

```text
Athena should not only work once on your machine.
Athena should be testable, repeatable, documented and reliable.
```

The key lesson:

```text
In finance software, correctness is a feature.
Testing and DevOps are what make that correctness sustainable.
```
