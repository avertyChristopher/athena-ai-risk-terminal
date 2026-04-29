# 03 — Backend Stack

**Project:** Athena AI Risk Terminal  
**Recommended file path:** `docs/libraries/03-backend-stack.md`  
**Purpose:** understand the backend technologies and architecture patterns used to transform Athena from notebooks and finance formulas into a reliable API-driven application.  
**Scope:** this document focuses on the backend stack: FastAPI, Pydantic, SQLAlchemy, PostgreSQL, Alembic, Redis, background jobs, service architecture, validation, testing, security basics and deployment readiness.

---

## Table of Contents

1. What is a backend?
2. Why Athena needs a backend
3. Backend role in Athena
4. Backend vs notebooks
5. Backend vs frontend
6. Recommended backend stack
7. FastAPI overview
8. Why FastAPI for Athena
9. FastAPI project structure
10. FastAPI application entrypoint
11. API routes
12. Request and response cycle
13. Path parameters
14. Query parameters
15. Request bodies
16. Response models
17. HTTP methods
18. HTTP status codes
19. API versioning
20. OpenAPI documentation
21. Pydantic overview
22. Pydantic models
23. Input validation
24. Output validation
25. Field constraints
26. Optional fields and defaults
27. Nested schemas
28. Error messages
29. Pydantic in Athena
30. SQLAlchemy overview
31. ORM intuition
32. Database models
33. Database sessions
34. Repositories
35. SQLAlchemy relationships
36. PostgreSQL overview
37. Why PostgreSQL for Athena
38. Core database entities
39. Portfolio table
40. Asset table
41. Position table
42. Trade table
43. Market data table
44. Risk metrics table
45. P&L table
46. Report table
47. Alembic overview
48. Database migrations
49. Why migrations matter
50. Redis overview
51. Redis caching
52. Redis for background jobs
53. Celery vs RQ
54. Background jobs in Athena
55. Long-running calculations
56. Backend clean architecture
57. API layer
58. Schema layer
59. Service layer
60. Repository layer
61. Domain layer
62. Core layer
63. Database layer
64. Dependency injection
65. Configuration management
66. Environment variables
67. Logging
68. Error handling
69. Custom exceptions
70. Security basics
71. Authentication overview
72. Authorization overview
73. Password hashing
74. JWT overview
75. CORS
76. Data validation and financial safety
77. Idempotency
78. Pagination
79. Filtering and sorting
80. File exports
81. Report generation
82. Testing backend code
83. Unit tests
84. Integration tests
85. API tests
86. Database tests
87. Test database strategy
88. Mocking external data
89. Code quality tools
90. Ruff and Black
91. Type checking
92. Backend folder structure
93. Example Athena backend structure
94. Suggested API modules
95. Suggested backend services
96. Suggested database models
97. Suggested tests
98. Common beginner mistakes
99. Development workflow
100. Summary

---

## 1. What is a backend?

A backend is the server-side part of an application.

It handles:

```text
Business logic
Data storage
API endpoints
Validation
Authentication
Authorization
Calculations
Background jobs
Reports
Database access
```

In a web application, the backend usually receives requests from the frontend, processes them, interacts with the database, and returns structured responses.

Simple flow:

```text
Frontend sends request
      ↓
Backend validates request
      ↓
Backend runs business logic
      ↓
Backend reads/writes database
      ↓
Backend returns response
```

### Athena example

The frontend asks:

```text
Calculate 1-day 95% VaR for portfolio pf_001.
```

The backend:

```text
Loads portfolio positions
Loads market data
Calculates returns and losses
Computes VaR
Stores or returns result
```

---

## 2. Why Athena needs a backend

Athena needs a backend because it is not only a static website.

Athena must:

```text
Store portfolios
Store trades
Store positions
Load market data
Calculate risk metrics
Run stress tests
Calculate Black-Scholes prices
Generate reports
Track RiskDNA scores
Validate inputs
Expose APIs to the frontend
```

If all calculations stay in notebooks, Athena remains an experiment.

If the calculations are moved into backend services, Athena becomes an application.

### Core idea

```text
Notebooks prove the methodology.
Backend services make it reusable.
Frontend makes it usable.
```

---

## 3. Backend role in Athena

The backend is the engine room of Athena.

It should own:

```text
Financial calculations
Risk calculations
Portfolio valuation
Data validation
Database access
API logic
Report generation
RiskDNA scoring
Workflow events
Limit checks
```

The backend should not be only a thin wrapper around the frontend.

It should protect the system from invalid data and inconsistent calculations.

### Example

Bad design:

```text
Frontend calculates VaR directly.
```

Better design:

```text
Frontend asks backend for VaR.
Backend calculates VaR using tested service.
Frontend displays result.
```

This keeps finance logic centralized and testable.

---

## 4. Backend vs notebooks

Notebooks are for exploration.

Backend is for production logic.

### Notebooks

Good for:

```text
Learning
Experimentation
Charts
Formula exploration
Prototypes
```

### Backend

Good for:

```text
Reusable functions
API endpoints
Testing
Validation
Database persistence
Application logic
```

### Athena workflow

```text
1. Learn concept in docs.
2. Prototype in notebook.
3. Extract clean function.
4. Add to backend service.
5. Write tests.
6. Expose via API.
7. Display in frontend.
```

Example:

```text
Notebook: calculate VaR once for one dataset.
Backend: calculate VaR for any portfolio through an API.
```

---

## 5. Backend vs frontend

The frontend is the user interface.  
The backend is the application logic and data engine.

### Frontend responsibilities

```text
Display dashboards
Collect user inputs
Show charts
Show tables
Call APIs
Handle UI state
```

### Backend responsibilities

```text
Validate inputs
Run calculations
Read/write database
Apply business rules
Check limits
Generate reports
Return structured data
```

### Example

Frontend:

```text
User enters option inputs in a form.
```

Backend:

```text
Validates inputs and calculates Black-Scholes price and Greeks.
```

Frontend:

```text
Displays call price, put price and Greeks table.
```

---

## 6. Recommended backend stack

Recommended Athena backend stack:

```text
Python
FastAPI
Pydantic
SQLAlchemy
PostgreSQL
Alembic
Redis
Celery or RQ
pytest
httpx
Ruff
Black
mypy optional
Docker
```

### Main roles

```text
FastAPI     = API framework
Pydantic    = validation and schemas
SQLAlchemy  = database ORM
PostgreSQL  = relational database
Alembic     = database migrations
Redis       = cache / background job support
Celery/RQ   = background jobs
pytest      = tests
httpx       = API testing client
Ruff/Black  = code quality and formatting
Docker      = local infrastructure
```

### Athena recommendation

Start with:

```text
FastAPI
Pydantic
SQLAlchemy
PostgreSQL
pytest
```

Add Redis and background jobs later.

---

## 7. FastAPI overview

FastAPI is a modern Python web framework for building APIs.

It is built around:

```text
Python type hints
Pydantic validation
Automatic OpenAPI documentation
Async support
High performance
Clean route definitions
```

Basic example:

```python
from fastapi import FastAPI

app = FastAPI(title="Athena AI Risk Terminal API")

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
```

Run with:

```bash
uvicorn app.main:app --reload
```

### Athena use

FastAPI will expose endpoints like:

```text
GET /api/portfolios
POST /api/risk/{portfolio_id}/historical-var
POST /api/options/black-scholes/price
POST /api/trades/simulate
```

---

## 8. Why FastAPI for Athena

FastAPI is a strong choice for Athena because:

```text
It works naturally with Python finance code.
It supports Pydantic validation.
It generates API documentation automatically.
It is easy to test.
It is modern and widely used.
It integrates well with async tasks and background jobs.
```

Athena needs APIs for many modules:

```text
Market data
Portfolios
Trades
Risk
Stress testing
Options
RiskDNA
P&L
Reports
```

FastAPI makes this structure clean.

### Example

An option pricing endpoint can validate input, call a service, and return typed output.

```python
@app.post("/api/options/black-scholes/price")
def price_option(request: OptionPricingRequest) -> OptionPricingResponse:
    return option_service.price(request)
```

---

## 9. FastAPI project structure

A clean FastAPI project should be organized by responsibility.

Example:

```text
backend/app/
├── main.py
├── api/
├── core/
├── database/
├── domain/
├── repositories/
├── schemas/
├── services/
└── tests/
```

### Why structure matters

Without structure, the backend quickly becomes messy.

Bad:

```text
All routes, database logic and calculations in main.py.
```

Better:

```text
Routes call services.
Services call repositories.
Repositories access database.
Schemas validate inputs and outputs.
```

This makes the project easier to test and extend.

---

## 10. FastAPI application entrypoint

The application entrypoint creates the FastAPI app.

Example:

```python
from fastapi import FastAPI
from app.api.routes import portfolio_routes, risk_routes

app = FastAPI(
    title="Athena AI Risk Terminal API",
    version="0.1.0",
)

app.include_router(portfolio_routes.router, prefix="/api/portfolios", tags=["Portfolios"])
app.include_router(risk_routes.router, prefix="/api/risk", tags=["Risk"])

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
```

Recommended file:

```text
backend/app/main.py
```

### Athena rule

`main.py` should stay small.

It should wire the application together, not contain all business logic.

---

## 11. API routes

API routes define endpoints.

Example:

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_portfolios():
    return []
```

Recommended file:

```text
backend/app/api/routes/portfolio_routes.py
```

### Route responsibility

Routes should:

```text
Receive request
Validate input through schemas
Call service layer
Return response
```

Routes should not:

```text
Contain complex financial formulas
Directly manipulate database in messy ways
Contain large business logic
```

### Athena example

```python
@router.post("/{portfolio_id}/historical-var")
def calculate_historical_var(portfolio_id: str, request: VaRRequest):
    return risk_service.calculate_historical_var(portfolio_id, request)
```

---

## 12. Request and response cycle

A backend request follows a cycle.

```text
1. Frontend sends HTTP request.
2. FastAPI receives request.
3. Pydantic validates data.
4. Route calls service.
5. Service runs business logic.
6. Repository loads or saves database data.
7. Service returns result.
8. FastAPI serializes response.
9. Frontend receives JSON.
```

### Example

Request:

```text
POST /api/options/black-scholes/price
```

Body:

```json
{
  "spot_price": 100,
  "strike_price": 100,
  "time_to_maturity": 1,
  "risk_free_rate": 0.05,
  "volatility": 0.20,
  "dividend_yield": 0.0
}
```

Response:

```json
{
  "call_price": 10.45,
  "put_price": 5.57
}
```

---

## 13. Path parameters

Path parameters are values inside the URL.

Example:

```text
/api/portfolios/{portfolio_id}
```

FastAPI code:

```python
@router.get("/{portfolio_id}")
def get_portfolio(portfolio_id: str):
    return {"portfolio_id": portfolio_id}
```

### Athena examples

```text
GET /api/portfolios/pf_001
GET /api/risk/pf_001/summary
GET /api/reports/pf_001/rpt_001
```

Path parameters are useful for identifying resources.

---

## 14. Query parameters

Query parameters are optional values after `?`.

Example:

```text
/api/market-data/prices?symbol=AAPL&start=2025-01-01
```

FastAPI code:

```python
from datetime import date

@router.get("/prices")
def get_prices(symbol: str, start: date | None = None, end: date | None = None):
    return {"symbol": symbol, "start": start, "end": end}
```

### Athena examples

```text
GET /api/market-data/prices?symbol=AAPL
GET /api/trades?portfolio_id=pf_001&status=approved
GET /api/riskdna/pf_001/timeline?start=2026-01-01
```

Query parameters are useful for filtering and date ranges.

---

## 15. Request bodies

Request bodies send structured data, usually JSON.

Example:

```python
from pydantic import BaseModel

class TradeSimulationRequest(BaseModel):
    symbol: str
    side: str
    quantity: float
    estimated_price: float

@router.post("/simulate")
def simulate_trade(request: TradeSimulationRequest):
    return request
```

Request body:

```json
{
  "symbol": "AAPL",
  "side": "buy",
  "quantity": 50,
  "estimated_price": 200
}
```

### Athena use

Request bodies are needed for:

```text
Trade simulation
Option pricing
Portfolio creation
Risk calculations
Stress scenarios
Report generation
```

---

## 16. Response models

Response models define the shape of API responses.

Example:

```python
from pydantic import BaseModel

class OptionPricingResponse(BaseModel):
    call_price: float
    put_price: float
    d1: float
    d2: float
```

Route:

```python
@router.post("/black-scholes/price", response_model=OptionPricingResponse)
def price_option(request: OptionPricingRequest):
    return option_service.price(request)
```

### Why response models matter

They ensure:

```text
Consistent responses
Automatic documentation
Validation
Frontend predictability
Cleaner contracts
```

### Athena rule

Every major endpoint should have response schemas.

---

## 17. HTTP methods

Common HTTP methods:

```text
GET     = read data
POST    = create or calculate
PUT     = replace/update
PATCH   = partial update
DELETE  = delete
```

### Athena examples

```text
GET  /api/portfolios
POST /api/portfolios
GET  /api/portfolios/{portfolio_id}
POST /api/trades/simulate
POST /api/risk/{portfolio_id}/historical-var
DELETE /api/portfolios/{portfolio_id}
```

### Calculation endpoints

For calculations that need a request body, use `POST`.

Example:

```text
POST /api/options/black-scholes/price
```

Even if it does not create a database record, it performs a calculation.

---

## 18. HTTP status codes

Important status codes:

```text
200 OK
201 Created
204 No Content
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
422 Validation Error
500 Internal Server Error
```

### Athena examples

```text
200 = risk metric calculated successfully
201 = portfolio created
404 = portfolio not found
422 = invalid request input
409 = trade cannot be approved because status is rejected
```

### Good practice

Use meaningful status codes.

Do not return `200 OK` for everything.

---

## 19. API versioning

API versioning helps manage changes over time.

Example:

```text
/api/v1/portfolios
/api/v1/risk
```

Possible structure:

```text
backend/app/api/v1/routes/
```

### Why versioning matters

If the frontend depends on an API contract, changing it can break the application.

Versioning allows future changes without breaking existing clients.

### Athena recommendation

For early development, either use:

```text
/api/...
```

or:

```text
/api/v1/...
```

If you want a more professional structure, use `/api/v1`.

---

## 20. OpenAPI documentation

FastAPI automatically generates OpenAPI documentation.

Default docs:

```text
/docs
```

Alternative docs:

```text
/redoc
```

Example local URLs:

```text
http://localhost:8000/docs
http://localhost:8000/redoc
```

### Why it matters

OpenAPI docs help you:

```text
Test endpoints manually
Understand request schemas
Understand response schemas
Share API structure
Debug backend/frontend integration
```

### Athena use

Your GitHub README can mention:

```text
Run backend and open /docs to explore the API.
```

---

## 21. Pydantic overview

Pydantic validates data using Python type hints.

It is deeply integrated with FastAPI.

Example:

```python
from pydantic import BaseModel

class PortfolioCreateRequest(BaseModel):
    name: str
    base_currency: str
```

If the frontend sends invalid data, FastAPI returns a validation error automatically.

### Athena use

Pydantic schemas should define:

```text
Portfolio requests
Trade requests
Risk calculation requests
Option pricing requests
Report requests
API responses
```

Pydantic protects the backend from bad inputs.

---

## 22. Pydantic models

A Pydantic model defines structured data.

Example:

```python
from pydantic import BaseModel

class OptionPricingRequest(BaseModel):
    spot_price: float
    strike_price: float
    time_to_maturity: float
    risk_free_rate: float
    volatility: float
    dividend_yield: float = 0.0
```

Use:

```python
request = OptionPricingRequest(
    spot_price=100,
    strike_price=100,
    time_to_maturity=1,
    risk_free_rate=0.05,
    volatility=0.20,
)
```

### Athena rule

Use Pydantic schemas for API boundaries.

Do not pass raw dictionaries everywhere.

---

## 23. Input validation

Input validation ensures data makes sense before calculations.

Example:

```python
from pydantic import BaseModel, Field

class OptionPricingRequest(BaseModel):
    spot_price: float = Field(gt=0)
    strike_price: float = Field(gt=0)
    time_to_maturity: float = Field(gt=0)
    volatility: float = Field(gt=0)
    risk_free_rate: float
    dividend_yield: float = 0.0
```

This rejects:

```text
negative spot price
zero strike price
negative volatility
zero time to maturity
```

### Athena importance

Financial calculations can produce nonsense if inputs are invalid.

Validation is risk control.

---

## 24. Output validation

Output validation ensures API responses match the expected schema.

Example:

```python
class VaRResponse(BaseModel):
    portfolio_id: str
    confidence_level: float
    time_horizon: str
    var_amount: float
    currency: str
```

If a service returns missing or wrong fields, FastAPI can detect it.

### Athena use

Output validation helps keep the frontend stable.

The frontend should know exactly what fields to expect.

---

## 25. Field constraints

Pydantic field constraints make schemas safer.

Examples:

```python
from pydantic import BaseModel, Field

class VaRRequest(BaseModel):
    confidence_level: float = Field(gt=0, lt=1)
    lookback_days: int = Field(ge=30, le=5000)
```

This ensures:

```text
confidence_level between 0 and 1
lookback_days between 30 and 5000
```

### Athena examples

```text
quantity > 0
portfolio_value > 0
volatility > 0
confidence_level between 0 and 1
weight between 0 and 1
```

---

## 26. Optional fields and defaults

Some fields can be optional.

Example:

```python
from pydantic import BaseModel

class PortfolioCreateRequest(BaseModel):
    name: str
    description: str | None = None
    base_currency: str = "CAD"
```

This means:

```text
name is required
description is optional
base_currency defaults to CAD
```

### Athena use

Defaults are useful for:

```text
base currency
confidence level
time horizon
lookback window
dividend yield
risk-free rate source
```

### Caution

Defaults should be documented.

A hidden default can affect financial results.

---

## 27. Nested schemas

Nested schemas represent complex data.

Example:

```python
class PositionInput(BaseModel):
    symbol: str
    quantity: float
    price: float

class PortfolioInput(BaseModel):
    name: str
    positions: list[PositionInput]
```

Request:

```json
{
  "name": "Growth Portfolio",
  "positions": [
    {"symbol": "AAPL", "quantity": 10, "price": 200},
    {"symbol": "MSFT", "quantity": 5, "price": 420}
  ]
}
```

### Athena use

Nested schemas are useful for:

```text
portfolio creation
stress scenarios
report sections
trade simulations
batch pricing
```

---

## 28. Error messages

Good error messages help users and developers fix problems.

Bad:

```text
Invalid input.
```

Better:

```text
volatility must be greater than 0.
```

Pydantic automatically returns detailed validation errors.

Example:

```json
{
  "detail": [
    {
      "loc": ["body", "volatility"],
      "msg": "Input should be greater than 0",
      "type": "greater_than"
    }
  ]
}
```

### Athena rule

For financial logic errors, create clear domain-specific messages.

Example:

```text
Cannot calculate VaR because the portfolio has no historical returns.
```

---

## 29. Pydantic in Athena

Pydantic should be used for:

```text
API request schemas
API response schemas
Calculation input schemas
Configuration validation
Report generation requests
Trade simulation requests
Risk metric responses
```

Recommended folder:

```text
backend/app/schemas/
```

Example files:

```text
portfolio_schema.py
trade_schema.py
risk_schema.py
option_schema.py
report_schema.py
riskdna_schema.py
```

### Athena principle

Schemas define the contract between frontend and backend.

---

## 30. SQLAlchemy overview

SQLAlchemy is a Python library for working with relational databases.

It can be used as:

```text
SQL toolkit
ORM
```

ORM means Object-Relational Mapping.

Simple idea:

```text
Python class ↔ database table
Python object ↔ database row
```

Example:

```python
class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
```

### Athena use

SQLAlchemy will manage database models for:

```text
Portfolios
Assets
Positions
Trades
Market data
Risk metrics
Reports
RiskDNA scores
```

---

## 31. ORM intuition

ORM lets you work with Python objects instead of writing raw SQL everywhere.

Without ORM:

```sql
SELECT * FROM portfolios WHERE id = 'pf_001';
```

With ORM:

```python
portfolio = session.get(Portfolio, "pf_001")
```

### Benefits

```text
Cleaner Python code
Reusable models
Relationships
Less repetitive SQL
Integration with migrations
```

### Caution

You should still understand SQL basics.

ORM does not remove the need to understand database design.

---

## 32. Database models

Database models define tables.

Example:

```python
from sqlalchemy import Column, String, DateTime
from app.database.base import Base

class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    base_currency = Column(String, nullable=False, default="CAD")
```

### Athena model examples

```text
Portfolio
Asset
Position
Trade
MarketPrice
RiskMetric
StressScenario
RiskDNAScore
PnlRecord
Report
```

### Rule

Database models should represent persisted data, not API requests.

Use Pydantic schemas for API requests.

---

## 33. Database sessions

A database session manages communication with the database.

Example dependency:

```python
from sqlalchemy.orm import Session
from app.database.session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Route:

```python
from fastapi import Depends

@router.get("/{portfolio_id}")
def get_portfolio(portfolio_id: str, db: Session = Depends(get_db)):
    ...
```

### Athena use

Sessions should be injected into repositories or services.

Avoid creating database connections randomly inside functions.

---

## 34. Repositories

Repositories isolate database access.

Example:

```python
class PortfolioRepository:
    def __init__(self, db):
        self.db = db

    def get_by_id(self, portfolio_id: str):
        return self.db.get(Portfolio, portfolio_id)

    def save(self, portfolio: Portfolio):
        self.db.add(portfolio)
        self.db.commit()
        self.db.refresh(portfolio)
        return portfolio
```

### Why repositories matter

They keep database logic out of:

```text
API routes
financial services
frontend
```

### Athena use

Recommended repositories:

```text
portfolio_repository.py
asset_repository.py
position_repository.py
trade_repository.py
risk_metric_repository.py
report_repository.py
```

---

## 35. SQLAlchemy relationships

Relationships connect tables.

Example:

```text
Portfolio has many Positions.
Asset has many Positions.
Portfolio has many Trades.
```

SQLAlchemy example:

```python
class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(String, primary_key=True)
    positions = relationship("Position", back_populates="portfolio")
```

```python
class Position(Base):
    __tablename__ = "positions"

    id = Column(String, primary_key=True)
    portfolio_id = Column(String, ForeignKey("portfolios.id"))
    portfolio = relationship("Portfolio", back_populates="positions")
```

### Athena use

Relationships help load related data, but be careful with performance and lazy loading.

---

## 36. PostgreSQL overview

PostgreSQL is a powerful open-source relational database.

It is a strong choice for Athena because it supports:

```text
Structured data
Relationships
Transactions
Constraints
Indexes
JSON fields if needed
Reliable persistence
```

### Why not only CSV?

CSV files are useful for learning, but a real application needs a database.

A database supports:

```text
Multiple portfolios
Persistent trades
Historical risk metrics
Reports
Users later
Audit trail
```

### Athena use

PostgreSQL should store the official application data.

---

## 37. Why PostgreSQL for Athena

PostgreSQL fits Athena because Athena has relational data.

Examples:

```text
A portfolio has positions.
A position references an asset.
A trade belongs to a portfolio.
A risk metric belongs to a portfolio and date.
A report belongs to a portfolio.
```

PostgreSQL helps enforce consistency.

### Important database concepts

```text
Primary key
Foreign key
Unique constraints
Indexes
Transactions
Migrations
```

### Athena recommendation

Use PostgreSQL with Docker Compose for local development.

---

## 38. Core database entities

Core Athena entities:

```text
Portfolio
Asset
Position
Trade
MarketPrice
RiskMetric
StressScenario
StressResult
RiskLimit
RiskDNAScore
RiskDNADriver
PnlRecord
Report
WorkflowEvent
```

These entities support the whole platform.

### Entity principle

An entity should represent a real concept in Athena.

Example:

```text
Portfolio = set of positions and cash
Trade = proposed or executed transaction
RiskMetric = calculated risk result
Report = generated document/report record
```

---

## 39. Portfolio table

Possible fields:

```text
id
name
description
base_currency
created_at
updated_at
```

Example:

```python
class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    base_currency = Column(String, nullable=False, default="CAD")
```

### Athena use

Portfolios are central.

Most modules reference `portfolio_id`.

---

## 40. Asset table

Possible fields:

```text
id
symbol
name
asset_type
currency
sector
country
exchange
created_at
updated_at
```

Asset types:

```text
equity
ETF
bond
option
cash
index
currency
commodity
```

### Athena use

Assets allow positions, trades and market data to reference the same instrument.

Example:

```text
AAPL = Apple Inc., equity, USD, technology, United States
```

---

## 41. Position table

Possible fields:

```text
id
portfolio_id
asset_id
quantity
average_price
market_price
market_value
currency
valuation_date
created_at
updated_at
```

### Position example

```text
Portfolio: pf_001
Asset: AAPL
Quantity: 10
Average price: 180
Market price: 200
Market value: 2,000
```

### Athena use

Positions drive:

```text
Portfolio value
Weights
Exposures
Risk
P&L
Trade simulation
```

---

## 42. Trade table

Possible fields:

```text
id
portfolio_id
asset_id
side
quantity
order_type
estimated_price
executed_price
fees
currency
status
trade_date
settlement_date
created_at
updated_at
```

Trade statuses:

```text
draft
simulated
pending_approval
approved
rejected
executed
cancelled
settled
```

### Athena use

Trades support:

```text
Trade Simulator
Workflow
P&L
Audit trail
Portfolio updates
```

---

## 43. Market data table

Possible fields:

```text
id
asset_id
date
open
high
low
close
adjusted_close
volume
currency
source
created_at
```

Unique constraint:

```text
asset_id + date + source
```

### Athena use

Market data supports:

```text
Returns
Volatility
VaR
CVaR
P&L
Charts
Portfolio valuation
```

### Data quality rule

Market data should be validated before official calculations.

---

## 44. Risk metrics table

Possible fields:

```text
id
portfolio_id
valuation_date
confidence_level
time_horizon
var_amount
cvar_amount
volatility
max_drawdown
stress_loss
methodology_version
currency
created_at
```

### Athena use

Risk metrics should be persisted when used in reports or RiskDNA.

This allows:

```text
Historical risk trends
Backtesting
Reports
RiskDNA timeline
Auditability
```

---

## 45. P&L table

Possible fields:

```text
id
portfolio_id
valuation_date
beginning_value
ending_value
daily_pnl
daily_return
cumulative_pnl
explained_pnl
unexplained_pnl
currency
created_at
```

### Athena use

P&L records support:

```text
P&L dashboard
P&L attribution
Reports
VaR backtesting
RiskDNA monitoring
```

### Rule

P&L should be linked to valuation date and currency.

---

## 46. Report table

Possible fields:

```text
id
portfolio_id
report_type
report_date
title
status
version
methodology_version
generated_by
reviewed_by
approved_by
created_at
updated_at
```

Statuses:

```text
draft
validated
reviewed
approved
rejected
archived
```

### Athena use

Reports should be traceable, not just downloaded files.

---

## 47. Alembic overview

Alembic is a database migration tool for SQLAlchemy.

It manages changes to the database schema over time.

Example changes:

```text
Create portfolios table
Add base_currency column
Add risk_metrics table
Add index on market_data date
```

### Why Alembic matters

Without migrations, database schema changes become messy and manual.

Alembic makes schema evolution controlled.

---

## 48. Database migrations

A migration is a script that changes the database schema.

Example:

```bash
alembic revision --autogenerate -m "create portfolios table"
alembic upgrade head
```

Migration files are stored in:

```text
backend/app/database/migrations/
```

or:

```text
backend/alembic/versions/
```

### Athena workflow

```text
1. Modify SQLAlchemy model.
2. Generate migration.
3. Review migration.
4. Apply migration.
5. Commit migration file.
```

### Important

Always review autogenerated migrations.

---

## 49. Why migrations matter

Migrations matter because Athena's data model will evolve.

At first, you may have:

```text
Portfolio
Asset
Position
```

Later, you add:

```text
RiskMetric
RiskDNAScore
Report
WorkflowEvent
```

Migrations allow the database to evolve safely.

### Bad practice

```text
Drop database and recreate every time.
```

This destroys data and is not professional.

### Good practice

```text
Use migrations to evolve schema.
```

---

## 50. Redis overview

Redis is an in-memory data store.

It is often used for:

```text
Caching
Background job queues
Temporary data
Rate limiting
Session storage
```

### Athena use

Redis can support:

```text
Caching market data
Caching expensive risk results
Background job queue
Report generation jobs
Stress testing jobs
```

### Start later

Athena does not need Redis on day one.

Add it when calculations or reports become slow.

---

## 51. Redis caching

Caching stores frequently used results temporarily.

Example:

```text
Portfolio risk summary calculated once and cached for 5 minutes.
```

Benefits:

```text
Faster responses
Less repeated calculation
Reduced database load
```

### Athena examples

Cache:

```text
Latest portfolio summary
Latest risk metrics
Market data query results
RiskDNA latest score
```

### Caution

Caching can create stale data.

Always define expiration and invalidation rules.

---

## 52. Redis for background jobs

Redis can act as a broker for background jobs.

Example:

```text
User requests report generation.
API returns job ID.
Worker generates report in background.
Frontend polls job status.
```

Redis can queue the job.

A worker processes it.

### Athena use

Good candidates for background jobs:

```text
Monte Carlo VaR
Large stress tests
Report generation
Data ingestion
Batch market data processing
```

---

## 53. Celery vs RQ

Celery and RQ are Python background job systems.

### Celery

Pros:

```text
Powerful
Feature-rich
Supports complex workflows
Widely used
```

Cons:

```text
More complex
More configuration
```

### RQ

Pros:

```text
Simpler
Easy to start
Redis-based
Good for smaller projects
```

Cons:

```text
Less feature-rich than Celery
```

### Athena recommendation

Start without background jobs.  
Then use RQ first if you want simplicity.  
Use Celery later if workflows become complex.

---

## 54. Background jobs in Athena

Some calculations may take longer than normal API requests.

Examples:

```text
Monte Carlo simulation
Large portfolio risk calculation
Batch VaR backtest
Report generation
Market data ingestion
RiskDNA timeline rebuild
```

Background job flow:

```text
1. Frontend requests job.
2. Backend creates job record.
3. Worker runs calculation.
4. Job status updates.
5. Frontend retrieves result.
```

Statuses:

```text
queued
running
completed
failed
cancelled
```

---

## 55. Long-running calculations

Long-running calculations should not block the API.

Bad:

```text
Frontend waits 60 seconds for report generation.
```

Better:

```text
Backend returns job ID immediately.
Worker generates report.
Frontend checks status.
```

### Athena examples

```text
POST /api/reports/{portfolio_id}/generate
returns { "job_id": "job_001" }
```

Then:

```text
GET /api/jobs/job_001
```

Returns:

```text
running
```

or:

```text
completed
```

---

## 56. Backend clean architecture

Clean architecture separates responsibilities.

Recommended layers:

```text
API layer
Schema layer
Service layer
Repository layer
Domain layer
Database layer
Core layer
```

Simple flow:

```text
Route → Service → Repository → Database
```

For calculations:

```text
Route → Service → Domain/Quant functions → Response
```

### Why it matters

Clean architecture makes Athena:

```text
Easier to test
Easier to extend
Easier to debug
More professional
Less coupled to FastAPI
```

---

## 57. API layer

The API layer contains FastAPI routes.

Responsibilities:

```text
Define endpoints
Receive requests
Use schemas
Call services
Return responses
Set status codes
```

Should not contain:

```text
Long formulas
Database query details
Complex business logic
```

Recommended folder:

```text
backend/app/api/routes/
```

Example files:

```text
portfolio_routes.py
risk_routes.py
option_routes.py
trade_routes.py
report_routes.py
```

---

## 58. Schema layer

The schema layer contains Pydantic models.

Responsibilities:

```text
Validate request data
Define response shapes
Document API contracts
Constrain fields
```

Recommended folder:

```text
backend/app/schemas/
```

Example files:

```text
portfolio_schema.py
trade_schema.py
risk_schema.py
option_schema.py
report_schema.py
```

### Rule

Schemas are not database models.

They are API contracts.

---

## 59. Service layer

The service layer contains business logic and application logic.

Responsibilities:

```text
Calculate risk metrics
Simulate trades
Validate financial rules
Check limits
Generate reports
Coordinate repositories
Run workflow logic
```

Recommended folder:

```text
backend/app/services/
```

Example files:

```text
portfolio_service.py
risk_service.py
option_pricing_service.py
trade_simulation_service.py
riskdna_service.py
pnl_service.py
report_service.py
```

### Athena rule

Most finance logic should live in services or domain functions, not routes.

---

## 60. Repository layer

The repository layer handles database access.

Responsibilities:

```text
Get by ID
List records
Save records
Update records
Delete records
Query by date
Query by portfolio
```

Recommended folder:

```text
backend/app/repositories/
```

Example files:

```text
portfolio_repository.py
asset_repository.py
position_repository.py
trade_repository.py
risk_metric_repository.py
report_repository.py
```

### Benefit

Services do not need to know SQL details.

They call repositories.

---

## 61. Domain layer

The domain layer contains core business concepts and pure finance logic.

Examples:

```text
Portfolio valuation
Position weights
VaR calculation
CVaR calculation
Black-Scholes formulas
Greeks calculations
P&L formulas
RiskDNA scoring rules
```

Recommended folder:

```text
backend/app/domain/
```

Possible structure:

```text
domain/
├── portfolios/
├── risk/
├── options/
├── pnl/
├── fixed_income/
└── riskdna/
```

### Rule

Domain functions should be as pure and testable as possible.

---

## 62. Core layer

The core layer contains cross-cutting configuration.

Examples:

```text
config.py
logging.py
security.py
exceptions.py
constants.py
```

Recommended folder:

```text
backend/app/core/
```

### Example

```python
class Settings(BaseSettings):
    database_url: str
    environment: str = "development"
```

Core should not depend on business modules.

---

## 63. Database layer

The database layer contains database setup.

Examples:

```text
base.py
session.py
migrations/
```

Recommended folder:

```text
backend/app/database/
```

Example:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
```

### Athena rule

Keep database configuration centralized.

---

## 64. Dependency injection

Dependency injection provides dependencies to routes or services.

FastAPI supports it with `Depends`.

Example:

```python
from fastapi import Depends
from sqlalchemy.orm import Session

@router.get("/{portfolio_id}")
def get_portfolio(
    portfolio_id: str,
    db: Session = Depends(get_db),
):
    ...
```

### Why it matters

Dependency injection makes code:

```text
Easier to test
Less coupled
More explicit
```

### Athena use

Inject:

```text
Database session
Current user later
Settings
Repositories
Services
```

---

## 65. Configuration management

Configuration controls environment-specific settings.

Examples:

```text
Database URL
Redis URL
API environment
Secret key
CORS origins
Log level
External API keys
```

Use environment variables.

Example:

```text
DATABASE_URL=postgresql://athena:athena@localhost:5432/athena
ENVIRONMENT=development
```

### Athena rule

Do not hardcode secrets in code.

Use `.env` locally and environment variables in deployment.

---

## 66. Environment variables

Environment variables store configuration outside code.

Example `.env`:

```text
DATABASE_URL=postgresql://athena:athena@localhost:5432/athena
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=change-me
ENVIRONMENT=development
```

`.env` should not be committed if it contains secrets.

Add to `.gitignore`:

```text
.env
.env.local
```

### Athena use

Environment variables support local development and future deployment.

---

## 67. Logging

Logging records what the backend is doing.

Examples:

```text
API request received
Risk calculation started
Risk calculation completed
Report generation failed
Database connection error
Data validation warning
```

Python logging example:

```python
import logging

logger = logging.getLogger(__name__)

logger.info("Calculating VaR for portfolio %s", portfolio_id)
```

### Athena use

Logging is important for:

```text
Debugging
Monitoring
Audit support
Error investigation
Background jobs
```

Do not use `print()` everywhere in backend code.

---

## 68. Error handling

Error handling controls what happens when something fails.

Examples:

```text
Portfolio not found
Invalid confidence level
Missing market data
Database error
Report generation failure
Unauthorized request
```

Good error response:

```json
{
  "detail": "Portfolio not found."
}
```

### Athena rule

Errors should be clear and safe.

Do not expose sensitive internal stack traces to users.

---

## 69. Custom exceptions

Custom exceptions make domain errors clearer.

Example:

```python
class PortfolioNotFoundError(Exception):
    pass

class InsufficientMarketDataError(Exception):
    pass

class RiskLimitBreachedError(Exception):
    pass
```

FastAPI exception handler:

```python
from fastapi import HTTPException

try:
    result = risk_service.calculate_var(portfolio_id)
except InsufficientMarketDataError as exc:
    raise HTTPException(status_code=400, detail=str(exc))
```

### Athena use

Custom exceptions are useful for finance-specific errors.

---

## 70. Security basics

Backend security matters even for personal projects.

Basic principles:

```text
Validate inputs
Do not expose secrets
Use HTTPS in production
Hash passwords
Use authentication for private data
Use authorization for permissions
Avoid SQL injection
Avoid unsafe file handling
Limit CORS origins
```

### Athena first version

If Athena is local only, security can be simple.

But design as if it may become public later.

---

## 71. Authentication overview

Authentication answers:

```text
Who are you?
```

Common methods:

```text
Email/password login
JWT tokens
OAuth
Session cookies
API keys
```

Athena first version may not need authentication.

But later, authentication is required for:

```text
Private portfolios
Saved reports
User-specific dashboards
```

### Recommendation

Start without auth for local prototype.  
Add auth when persistence and user data become serious.

---

## 72. Authorization overview

Authorization answers:

```text
What are you allowed to do?
```

Examples:

```text
View portfolio
Edit portfolio
Approve trade
Generate report
Change risk limits
Admin settings
```

Possible roles:

```text
viewer
analyst
portfolio_manager
risk_manager
admin
```

### Athena use

Authorization matters later for workflow:

```text
Only risk manager can approve limit override.
Only admin can change methodology.
```

---

## 73. Password hashing

Never store plain text passwords.

Use password hashing.

Common library:

```text
passlib
bcrypt
argon2
```

Example concept:

```text
User enters password.
Backend hashes password.
Database stores hash.
Login compares hash.
```

### Athena note

This belongs to later authentication work.

Do not implement authentication poorly.

If needed, follow established patterns.

---

## 74. JWT overview

JWT means JSON Web Token.

It is often used for API authentication.

Flow:

```text
User logs in
Backend returns token
Frontend stores token carefully
Frontend sends token with requests
Backend verifies token
```

Header example:

```text
Authorization: Bearer <token>
```

### Athena use

JWT can be used later for user authentication.

Caution:

```text
Token storage and expiration must be handled carefully.
```

---

## 75. CORS

CORS controls which frontends can call the backend.

FastAPI example:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Athena use

Frontend likely runs on:

```text
http://localhost:5173
```

Backend likely runs on:

```text
http://localhost:8000
```

CORS allows the frontend to call the backend during development.

### Production caution

Do not allow all origins in production.

---

## 76. Data validation and financial safety

Financial APIs need strong validation.

Examples:

```text
Quantity must be positive
Price must be positive
Confidence level must be between 0 and 1
Volatility must be positive
Portfolio must exist
Market data must be sufficient
Weights should sum correctly
Currency must be supported
```

### Example

Do not allow:

```json
{
  "volatility": -0.2
}
```

Financial safety means preventing nonsensical calculations.

Athena should fail clearly when inputs are invalid.

---

## 77. Idempotency

Idempotency means repeating the same request does not create duplicate unintended effects.

Example problem:

```text
User clicks "Generate report" twice.
System creates two identical reports.
```

Idempotency solution:

```text
Use idempotency key
Detect duplicate request
Return existing result
```

### Athena use

Important for:

```text
Trade execution
Report generation
Background jobs
Data ingestion
```

For early prototype, this may be optional.

But it is a professional concept.

---

## 78. Pagination

Pagination splits large lists into pages.

Example:

```text
GET /api/trades?page=1&page_size=50
```

Why?

```text
A portfolio may have thousands of trades.
Returning all at once is inefficient.
```

Response:

```json
{
  "items": [],
  "page": 1,
  "page_size": 50,
  "total": 230
}
```

### Athena use

Use pagination for:

```text
Trades
Market data
Reports
Workflow events
Audit trail
```

---

## 79. Filtering and sorting

APIs should support filtering and sorting.

Examples:

```text
GET /api/trades?status=approved
GET /api/reports?report_type=risk
GET /api/market-data/prices?symbol=AAPL&start=2026-01-01
GET /api/workflows/events?entity_type=trade
```

Sorting:

```text
sort_by=date
sort_order=desc
```

### Athena use

Filtering and sorting are essential for dashboards.

The frontend should not load everything and filter all data locally.

---

## 80. File exports

Athena may export:

```text
CSV
Excel
PDF later
Markdown
JSON
```

Backend can generate files for:

```text
Reports
P&L tables
Risk summaries
Trade logs
Audit trails
```

### Example endpoint

```text
GET /api/reports/{report_id}/export?format=csv
```

### Caution

File exports must be validated.

Avoid exporting sensitive data accidentally.

---

## 81. Report generation

Report generation turns metrics into structured output.

Report workflow:

```text
1. Load portfolio
2. Load risk metrics
3. Load P&L
4. Load RiskDNA
5. Validate data
6. Build report sections
7. Store report
8. Return report ID
```

### Athena report types

```text
Risk report
P&L report
Portfolio summary
Trade impact report
Stress testing report
```

Report generation may become a background job if it is slow.

---

## 82. Testing backend code

Backend testing is essential.

Why?

```text
Finance calculations must be reliable.
APIs must return expected responses.
Database operations must work.
Invalid inputs must fail safely.
```

Testing levels:

```text
Unit tests
Integration tests
API tests
Database tests
```

Testing tool:

```text
pytest
```

Run tests:

```bash
pytest
```

### Athena rule

Every financial formula should have tests.

---

## 83. Unit tests

Unit tests test one function or service in isolation.

Example:

```python
def test_calculate_simple_return():
    result = calculate_simple_return(100, 105)
    assert result == 0.05
```

Good unit tests are:

```text
Small
Fast
Deterministic
Focused
```

### Athena unit test targets

```text
Return calculation
Volatility
VaR
CVaR
Black-Scholes
Greeks
P&L
RiskDNA scoring
Limit usage
```

---

## 84. Integration tests

Integration tests check multiple parts working together.

Example:

```text
Create portfolio
Add positions
Load prices
Calculate portfolio value
```

Integration tests may use a test database.

### Athena integration test example

```text
Given a portfolio with two positions
And current prices
When portfolio summary is requested
Then total value and weights are correct
```

Integration tests are slower than unit tests but very valuable.

---

## 85. API tests

API tests call endpoints and check responses.

FastAPI provides a test client.

Example:

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
```

### Athena API test targets

```text
Health check
Create portfolio
Get portfolio
Simulate trade
Calculate VaR
Price option
Generate report
```

---

## 86. Database tests

Database tests verify database operations.

Examples:

```text
Save portfolio
Retrieve portfolio
Update trade status
Create risk metric
Query reports by portfolio
```

### Test database

Use a separate database for tests.

Do not test against production or real user data.

Possible approaches:

```text
SQLite for simple tests
PostgreSQL test container for realistic tests
```

For Athena, PostgreSQL test database is more realistic.

---

## 87. Test database strategy

Recommended strategy:

```text
Use separate test database.
Run migrations or create tables for tests.
Clean database between tests.
Use fixtures.
```

Example test database URL:

```text
postgresql://athena_test:athena_test@localhost:5432/athena_test
```

### pytest fixtures

Fixtures can create reusable test data:

```python
@pytest.fixture
def sample_portfolio():
    ...
```

### Athena rule

Tests should not depend on existing local data.

They should create what they need.

---

## 88. Mocking external data

Mocking replaces external dependencies with fake controlled data.

Examples of external dependencies:

```text
Market data APIs
AI APIs
Email services
File storage
```

Why mock?

```text
Tests should be fast
Tests should be deterministic
Tests should not depend on the internet
Tests should not spend API credits
```

### Athena use

Mock:

```text
Market data provider
OpenAI / AI explanation service
External report storage
```

Core calculations should use deterministic sample data.

---

## 89. Code quality tools

Code quality tools keep the backend clean.

Recommended tools:

```text
Ruff
Black
mypy optional
pytest
coverage
pre-commit optional
```

### Why this matters

A finance backend must be readable and maintainable.

Messy code creates calculation risk.

### Athena use

Add code quality checks to GitHub Actions later.

---

## 90. Ruff and Black

Black formats Python code automatically.

Run:

```bash
black backend/
```

Ruff checks and fixes lint issues.

Run:

```bash
ruff check backend/
ruff check backend/ --fix
```

### Recommended

Use both:

```text
Black for formatting
Ruff for linting
```

### Athena benefit

Consistent style makes the project look professional.

---

## 91. Type checking

Type checking catches some bugs before runtime.

Tool:

```text
mypy
```

Example:

```bash
mypy backend/
```

Type hints help:

```text
Function clarity
Editor autocomplete
Bug prevention
Documentation
```

### Athena recommendation

Use type hints from the start.

Add mypy later if it becomes useful.

---

## 92. Backend folder structure

Recommended high-level structure:

```text
backend/
├── app/
│   ├── main.py
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── domain/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── tests/
├── requirements.txt
├── pyproject.toml
└── README.md
```

### Why this structure is good

It separates:

```text
API routes
Business logic
Database logic
Validation schemas
Core config
Tests
```

This supports long-term growth.

---

## 93. Example Athena backend structure

Detailed example:

```text
backend/app/
├── main.py
├── api/
│   ├── dependencies.py
│   └── routes/
│       ├── health_routes.py
│       ├── portfolio_routes.py
│       ├── market_data_routes.py
│       ├── trade_routes.py
│       ├── risk_routes.py
│       ├── option_routes.py
│       ├── riskdna_routes.py
│       ├── pnl_routes.py
│       └── report_routes.py
├── core/
│   ├── config.py
│   ├── logging.py
│   ├── security.py
│   └── exceptions.py
├── database/
│   ├── base.py
│   ├── session.py
│   └── migrations/
├── domain/
│   ├── portfolios/
│   ├── risk/
│   ├── options/
│   ├── fixed_income/
│   ├── pnl/
│   └── riskdna/
├── repositories/
│   ├── portfolio_repository.py
│   ├── asset_repository.py
│   ├── position_repository.py
│   ├── trade_repository.py
│   ├── market_data_repository.py
│   ├── risk_metric_repository.py
│   └── report_repository.py
├── schemas/
│   ├── portfolio_schema.py
│   ├── trade_schema.py
│   ├── risk_schema.py
│   ├── option_schema.py
│   ├── riskdna_schema.py
│   ├── pnl_schema.py
│   └── report_schema.py
├── services/
│   ├── portfolio_service.py
│   ├── market_data_service.py
│   ├── trade_simulation_service.py
│   ├── risk_service.py
│   ├── option_pricing_service.py
│   ├── riskdna_service.py
│   ├── pnl_service.py
│   └── report_service.py
└── tests/
```

This is a strong target architecture for Athena.

---

## 94. Suggested API modules

Suggested route modules:

```text
health_routes.py
portfolio_routes.py
asset_routes.py
market_data_routes.py
trade_routes.py
risk_routes.py
stress_testing_routes.py
option_routes.py
riskdna_routes.py
pnl_routes.py
report_routes.py
workflow_routes.py
```

### Start small

Initial routes:

```text
health_routes.py
portfolio_routes.py
risk_routes.py
option_routes.py
```

Then add:

```text
trade_routes.py
riskdna_routes.py
pnl_routes.py
report_routes.py
```

### Athena rule

Do not build every route at once.

Build module by module.

---

## 95. Suggested backend services

Suggested services:

```text
PortfolioService
MarketDataService
PortfolioValuationService
TradeSimulationService
RiskService
StressTestingService
OptionPricingService
RiskDNAService
PnLService
ReportService
LimitService
WorkflowService
```

### Service responsibility examples

`RiskService`:

```text
VaR
CVaR
Volatility
Drawdown
Risk contribution
```

`OptionPricingService`:

```text
Black-Scholes
Greeks
Payoff
Put-call parity
```

`RiskDNAService`:

```text
Score
Risk level
Drivers
Explanation inputs
```

---

## 96. Suggested database models

Suggested SQLAlchemy models:

```text
Portfolio
Asset
Position
Trade
MarketPrice
RiskMetric
StressScenario
StressResult
RiskLimit
LimitBreach
RiskDNAScore
RiskDNADriver
PnLRecord
PnLAttribution
Report
ReportSection
WorkflowEvent
```

### Start small

First models:

```text
Portfolio
Asset
Position
MarketPrice
```

Then:

```text
Trade
RiskMetric
Report
```

Then:

```text
RiskDNAScore
WorkflowEvent
LimitBreach
```

This avoids overwhelming the project early.

---

## 97. Suggested tests

Initial tests:

```text
GET /api/health returns ok
Create portfolio returns 201
Get portfolio returns saved portfolio
Invalid portfolio request returns 422
Option pricing endpoint returns expected Black-Scholes price
VaR endpoint rejects invalid confidence level
Portfolio valuation equals sum of position market values
Trade simulation does not mutate original portfolio
```

Service tests:

```text
RiskService calculates VaR correctly
OptionPricingService calculates call and put prices correctly
RiskDNAService maps score to correct risk level
PnLService calculates daily P&L correctly
```

Repository tests:

```text
PortfolioRepository saves and retrieves portfolio
TradeRepository filters by status
RiskMetricRepository retrieves latest metric
```

---

## 98. Common beginner mistakes

### Mistake 1 — Putting everything in `main.py`

This makes the backend impossible to maintain.

### Mistake 2 — Calculating finance logic in routes

Routes should call services.

### Mistake 3 — Skipping validation

Invalid financial inputs create nonsense outputs.

### Mistake 4 — No tests for formulas

Finance formulas need tests.

### Mistake 5 — Mixing database models and API schemas

Use SQLAlchemy models for database and Pydantic schemas for API.

### Mistake 6 — No migrations

Schema changes become chaotic.

### Mistake 7 — Hardcoding secrets

Use environment variables.

### Mistake 8 — Returning inconsistent JSON

Use response models.

### Mistake 9 — Adding Redis/Celery too early

Start simple. Add background jobs when needed.

### Mistake 10 — No error strategy

Clear exceptions make debugging easier.

---

## 99. Development workflow

Recommended backend development workflow:

```text
1. Define the use case.
2. Design the schema.
3. Write domain function if needed.
4. Write service method.
5. Write repository method if database is needed.
6. Create route.
7. Add tests.
8. Run formatter and linter.
9. Test with FastAPI docs.
10. Connect frontend.
```

Example for Black-Scholes:

```text
1. Define option pricing request/response schemas.
2. Implement Black-Scholes function.
3. Add OptionPricingService.
4. Add POST /api/options/black-scholes/price.
5. Add tests with known values.
6. Display in frontend.
```

This workflow keeps the project clean.

---

## 100. Summary

The backend is the engine of Athena AI Risk Terminal.

It transforms finance concepts and notebook prototypes into reliable APIs.

Recommended stack:

```text
FastAPI       = API framework
Pydantic      = validation
SQLAlchemy    = ORM/database access
PostgreSQL    = relational database
Alembic       = migrations
Redis         = cache/jobs later
Celery/RQ     = background jobs later
pytest        = tests
Ruff/Black    = code quality
Docker        = local infrastructure
```

Most important architecture principle:

```text
Routes receive requests.
Schemas validate data.
Services run business logic.
Repositories access the database.
Domain functions contain finance logic.
Tests protect correctness.
```

For Athena, the backend should be:

```text
Clean
Tested
Validated
Modular
Explainable
Ready to support finance and risk workflows
```

The key lesson:

```text
A beautiful frontend is not enough.
Athena needs a reliable backend because financial calculations must be correct, validated and reproducible.
```
