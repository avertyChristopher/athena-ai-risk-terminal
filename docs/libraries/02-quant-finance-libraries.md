# 02 — Quant Finance Libraries

**Project:** Athena AI Risk Terminal  
**Recommended file path:** `docs/libraries/02-quant-finance-libraries.md`  
**Purpose:** understand the specialized Python libraries that can support Athena's quantitative finance modules: portfolio analytics, optimization, risk modeling, time series, volatility modeling, option pricing, fixed income and market data experimentation.  
**Scope:** this document focuses on quant finance libraries that sit above the basic Python data stack. It assumes familiarity with NumPy, pandas, matplotlib and SciPy.

---

## Table of Contents

1. What are quant finance libraries?
2. Why Athena needs quant finance libraries
3. Core principle: learn the model before the library
4. Library categories
5. statsmodels overview
6. statsmodels for regression
7. statsmodels for alpha and beta
8. statsmodels for time series
9. statsmodels for diagnostic tests
10. statsmodels Athena use cases
11. scikit-learn overview
12. scikit-learn for preprocessing
13. scikit-learn for regression
14. scikit-learn for classification
15. scikit-learn for clustering
16. scikit-learn for anomaly detection
17. scikit-learn pipelines
18. scikit-learn model evaluation
19. scikit-learn Athena use cases
20. cvxpy overview
21. Convex optimization intuition
22. cvxpy for portfolio optimization
23. Minimum variance portfolio with cvxpy
24. Target return optimization with cvxpy
25. Long-only constraints
26. Sector and weight constraints
27. cvxpy Athena use cases
28. PyPortfolioOpt overview
29. PyPortfolioOpt for efficient frontier
30. PyPortfolioOpt for expected returns
31. PyPortfolioOpt for covariance estimation
32. PyPortfolioOpt for discrete allocation
33. PyPortfolioOpt Athena use cases
34. arch overview
35. Why volatility modeling matters
36. ARCH and GARCH intuition
37. arch for volatility forecasting
38. arch for risk modeling
39. arch Athena use cases
40. QuantLib overview
41. QuantLib for fixed income
42. QuantLib for yield curves
43. QuantLib for bond pricing
44. QuantLib for option pricing
45. QuantLib limitations for beginners
46. QuantLib Athena use cases
47. yfinance overview
48. yfinance for market data experimentation
49. yfinance limitations
50. yfinance Athena use cases
51. pandas-datareader overview
52. pandas-datareader use cases
53. OpenBB overview
54. OpenBB use cases
55. Riskfolio-Lib overview
56. Riskfolio-Lib use cases
57. vectorbt overview
58. vectorbt for backtesting
59. backtrader overview
60. backtesting libraries caution
61. Library selection strategy
62. Build vs use a library
63. When to code formulas manually
64. When to use a specialized library
65. How to document library assumptions
66. How to validate library outputs
67. How to avoid black-box usage
68. Suggested learning order
69. Athena module mapping
70. Suggested notebooks
71. Suggested backend services
72. Suggested tests
73. Common beginner mistakes
74. Example architecture
75. Summary

---

## 1. What are quant finance libraries?

Quant finance libraries are Python libraries that help implement financial models, statistical analysis, optimization, risk analytics, volatility modeling, portfolio construction and market data workflows.

They sit above the basic data stack.

Basic stack:

```text
NumPy
pandas
matplotlib
SciPy
```

Quant finance stack:

```text
statsmodels
scikit-learn
cvxpy
PyPortfolioOpt
arch
QuantLib
yfinance
pandas-datareader
OpenBB
Riskfolio-Lib
vectorbt
backtrader
```

Simple idea:

```text
The basic data stack helps manipulate data.
Quant finance libraries help build financial models.
```

### Athena link

Athena should not depend on advanced libraries too early.  
First, build a strong understanding of the formulas.  
Then use libraries where they add reliability, speed or professional depth.

---

## 2. Why Athena needs quant finance libraries

Athena AI Risk Terminal is not only a web application.

It is a quantitative finance platform.

It needs tools for:

```text
Portfolio optimization
Regression analysis
Beta and alpha estimation
Volatility modeling
Stress testing support
Risk scoring
Anomaly detection
Yield curve modeling
Bond pricing
Option pricing
Market data experimentation
Backtesting prototypes
```

Quant finance libraries can help Athena move from simple formulas to more professional analytics.

However, there is a risk:

```text
Using a library without understanding the model creates a black box.
```

Athena should use libraries carefully.

The rule is:

```text
Understand first.
Prototype second.
Integrate third.
Test always.
```

---

## 3. Core principle: learn the model before the library

A quant finance library should not replace understanding.

Bad approach:

```text
Use a function because it gives a number.
```

Good approach:

```text
Understand the concept.
Implement a simple version manually.
Compare with the library.
Use the library when it is reliable and tested.
```

Example with portfolio optimization:

```text
1. Understand portfolio return and volatility.
2. Understand covariance matrix.
3. Build a simple minimum variance optimization manually.
4. Use cvxpy or PyPortfolioOpt for cleaner constrained optimization.
5. Test output against known cases.
```

### Athena principle

Every library-based calculation should include:

```text
Methodology note
Input validation
Unit tests
Assumption documentation
Fallback or simplified implementation when possible
```

---

## 4. Library categories

Quant finance libraries can be grouped by role.

### Statistics and econometrics

```text
statsmodels
```

### Machine learning

```text
scikit-learn
```

### Optimization

```text
cvxpy
PyPortfolioOpt
Riskfolio-Lib
```

### Volatility modeling

```text
arch
```

### Pricing and fixed income

```text
QuantLib
```

### Market data

```text
yfinance
pandas-datareader
OpenBB
```

### Backtesting

```text
vectorbt
backtrader
```

### Athena recommendation

Start with:

```text
statsmodels
scikit-learn
cvxpy
yfinance
```

Then later learn:

```text
PyPortfolioOpt
arch
QuantLib
Riskfolio-Lib
vectorbt
```

---

## 5. statsmodels overview

`statsmodels` is a Python library for statistical modeling and econometrics.

It is useful for:

```text
Regression
Time series analysis
Hypothesis testing
Statistical diagnostics
Econometric modeling
```

Import convention:

```python
import statsmodels.api as sm
```

### Why it matters in finance

Finance often asks statistical questions:

```text
What is the beta of this asset?
Does this strategy have alpha?
Is this factor significant?
Are returns autocorrelated?
Is volatility persistent?
```

`statsmodels` helps answer those questions.

### Athena use

Use `statsmodels` for:

```text
Beta estimation
Alpha estimation
Factor regression
Benchmark sensitivity
Time series diagnostics
Risk model validation
```

---

## 6. statsmodels for regression

Regression estimates the relationship between variables.

Simple model:

```text
Asset return = alpha + beta × Market return + error
```

Python example:

```python
import statsmodels.api as sm

y = asset_returns
X = market_returns

X = sm.add_constant(X)
model = sm.OLS(y, X).fit()

print(model.summary())
```

### Output interpretation

Important outputs:

```text
coef
p-value
R-squared
standard error
t-statistic
```

### Athena link

Regression can support:

```text
Beta calculation
Benchmark analysis
Factor exposure
Risk diagnostics
```

---

## 7. statsmodels for alpha and beta

Beta measures sensitivity to the market.

Alpha measures return beyond what the market exposure explains.

Regression:

```text
R_asset = alpha + beta × R_market + error
```

Example interpretation:

```text
beta = 1.20
```

Meaning:

```text
The asset tends to move 1.2 times the market, approximately.
```

Example:

```text
alpha = 0.001 daily
```

Meaning:

```text
The asset produced an average daily return above the model expectation.
```

### Athena use

Athena can calculate:

```text
Portfolio beta
Asset beta
Regression alpha
Benchmark sensitivity
```

---

## 8. statsmodels for time series

Time series data is ordered by time.

Financial examples:

```text
Daily returns
Yield curves over time
Volatility series
RiskDNA score history
P&L series
```

`statsmodels` supports time series models such as:

```text
AR
MA
ARMA
ARIMA
Seasonality models
Autocorrelation tests
```

### Athena caution

Do not overcomplicate early.

Athena does not need advanced ARIMA models at the beginning.

Start with:

```text
rolling averages
rolling volatility
autocorrelation checks
simple regression
```

Then add time series models later.

---

## 9. statsmodels for diagnostic tests

Diagnostics help check whether a model is reasonable.

Examples:

```text
Residual analysis
Autocorrelation tests
Heteroskedasticity checks
Normality tests
```

Why this matters:

```text
A model can produce numbers but still be unreliable.
```

Example:

```text
Regression residuals are autocorrelated.
```

This may mean the model misses time-series structure.

### Athena use

Diagnostics can support:

```text
Model validation
Risk methodology notes
Backtesting reports
AI methodology governance
```

---

## 10. statsmodels Athena use cases

Possible Athena use cases:

```text
Estimate beta of portfolio vs benchmark
Estimate alpha of portfolio vs benchmark
Run factor regression
Analyze rolling beta
Validate regression residuals
Support performance attribution
Support risk model validation
```

Possible notebook:

```text
notebooks/03_beta_alpha_regression.ipynb
```

Possible backend service:

```text
backend/app/services/regression_service.py
```

Possible endpoint:

```text
GET /api/analytics/{portfolio_id}/beta
```

Suggested tests:

```text
Beta calculation returns expected value for known data.
Regression handles missing returns safely.
Alpha and beta outputs include methodology metadata.
```

---

## 11. scikit-learn overview

`scikit-learn` is a Python library for machine learning.

It supports:

```text
Regression
Classification
Clustering
Dimensionality reduction
Preprocessing
Model selection
Anomaly detection
Pipelines
```

Import examples:

```python
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
```

### Athena use

Athena can use scikit-learn for:

```text
RiskDNA anomaly detection
Portfolio clustering
Market regime classification
Feature preprocessing
Risk score experimentation
AI-adjacent non-LLM models
```

### Important

Do not use machine learning before deterministic metrics are solid.

---

## 12. scikit-learn for preprocessing

Preprocessing prepares data for machine learning.

Common tools:

```text
StandardScaler
MinMaxScaler
OneHotEncoder
SimpleImputer
Pipeline
ColumnTransformer
```

Example:

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

### Why scaling matters

Some models are sensitive to feature scale.

Example:

```text
Feature 1: VaR usage from 0 to 1
Feature 2: Portfolio value from 0 to 1,000,000
```

Without scaling, large numeric values can dominate.

### Athena use

Preprocessing can support RiskDNA machine learning experiments later.

---

## 13. scikit-learn for regression

Regression predicts continuous values.

Examples:

```text
Predict volatility
Predict risk score
Estimate expected return
Forecast drawdown proxy
```

Simple example:

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)
```

### Athena caution

Expected return prediction is very difficult.

Do not claim predictive power without evidence.

Better early use:

```text
Educational experiments
Model comparison
Feature importance exploration
Anomaly support
```

---

## 14. scikit-learn for classification

Classification predicts categories.

Examples:

```text
Risk level: Low / Medium / High / Critical
Market regime: Calm / Volatile / Stress
Data quality status: Clean / Warning / Critical
```

Example:

```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)
```

### Athena use

Classification can support future RiskDNA experiments.

But the first RiskDNA version should be deterministic and rule-based.

ML classification can be added later as:

```text
experimental model
not official risk engine
```

---

## 15. scikit-learn for clustering

Clustering groups similar observations.

Examples:

```text
Cluster assets by return behavior
Cluster portfolios by risk profile
Cluster market days into regimes
Cluster stress scenarios
```

Example:

```python
from sklearn.cluster import KMeans

model = KMeans(n_clusters=3, random_state=42)
clusters = model.fit_predict(features)
```

### Athena use

Possible uses:

```text
Market regime exploration
Asset similarity analysis
Portfolio similarity
Risk scenario grouping
```

### Caution

Clusters are not always economically meaningful.

Always interpret them carefully.

---

## 16. scikit-learn for anomaly detection

Anomaly detection identifies unusual observations.

Examples:

```text
Unusual P&L
Unexpected VaR jump
Abnormal volume
Sudden volatility spike
Data quality anomaly
RiskDNA score jump
```

Possible models:

```text
IsolationForest
LocalOutlierFactor
OneClassSVM
```

Example:

```python
from sklearn.ensemble import IsolationForest

model = IsolationForest(random_state=42)
labels = model.fit_predict(X)
```

Output:

```text
1 = normal
-1 = anomaly
```

### Athena use

Anomaly detection can support:

```text
RiskDNA alerts
P&L anomaly explanation
Data quality monitoring
```

---

## 17. scikit-learn pipelines

Pipelines combine preprocessing and modeling.

Example:

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression()),
])

pipeline.fit(X_train, y_train)
```

### Why pipelines matter

Pipelines reduce mistakes.

They ensure preprocessing is applied consistently to training and test data.

### Athena use

Use pipelines for ML experiments and future RiskDNA models.

Do not scatter preprocessing logic across notebooks.

---

## 18. scikit-learn model evaluation

Models must be evaluated.

Regression metrics:

```text
MAE
MSE
RMSE
R-squared
```

Classification metrics:

```text
Accuracy
Precision
Recall
F1-score
Confusion matrix
ROC AUC
```

Example:

```python
from sklearn.metrics import classification_report

print(classification_report(y_test, y_pred))
```

### Athena caution

Financial models can overfit easily.

Always separate:

```text
training data
validation data
test data
```

Do not evaluate a model only on the data used to train it.

---

## 19. scikit-learn Athena use cases

Possible Athena use cases:

```text
RiskDNA anomaly detection
Risk regime classification
Data quality anomaly detection
P&L anomaly detection
Asset clustering
Scenario clustering
Feature importance exploration
```

Possible notebook:

```text
notebooks/07_riskdna_anomaly_detection.ipynb
```

Possible backend service later:

```text
backend/app/services/anomaly_service.py
```

Suggested tests:

```text
Pipeline produces deterministic results with fixed seed.
Anomaly model handles missing values after preprocessing.
Model output is not used as official risk metric without validation.
```

---

## 20. cvxpy overview

`cvxpy` is a Python library for convex optimization.

It helps solve problems like:

```text
Minimize portfolio variance
Maximize expected return under constraints
Find optimal weights
Control exposure limits
```

Import convention:

```python
import cvxpy as cp
```

### Why cvxpy matters

Portfolio optimization is naturally expressed with variables, objectives and constraints.

Example:

```text
Choose weights that minimize risk.
Weights must sum to 1.
Weights must be non-negative.
No asset can exceed 20%.
```

cvxpy makes this kind of problem readable.

---

## 21. Convex optimization intuition

Optimization means finding the best solution.

A portfolio optimization problem usually has:

```text
Decision variables
Objective
Constraints
```

Example:

```text
Decision variables = portfolio weights
Objective = minimize volatility
Constraints = weights sum to 1, weights >= 0
```

Simple structure:

```text
minimize risk
subject to constraints
```

### Why convex matters

Convex optimization problems are easier and more reliable to solve than many non-convex problems.

Many useful portfolio problems can be expressed as convex problems.

---

## 22. cvxpy for portfolio optimization

Basic portfolio optimization structure:

```python
import cvxpy as cp
import numpy as np

n_assets = 3
weights = cp.Variable(n_assets)

cov_matrix = np.array([
    [0.04, 0.01, 0.02],
    [0.01, 0.09, 0.03],
    [0.02, 0.03, 0.16],
])

portfolio_variance = cp.quad_form(weights, cov_matrix)

constraints = [
    cp.sum(weights) == 1,
    weights >= 0,
]

problem = cp.Problem(cp.Minimize(portfolio_variance), constraints)
problem.solve()

print(weights.value)
```

### Athena use

This can power:

```text
Minimum variance portfolio
Target return portfolio
Constraint-aware allocation
```

---

## 23. Minimum variance portfolio with cvxpy

Minimum variance portfolio minimizes portfolio variance.

Objective:

```text
Minimize wᵀΣw
```

Where:

```text
w = portfolio weights
Σ = covariance matrix
```

cvxpy code:

```python
weights = cp.Variable(n_assets)
risk = cp.quad_form(weights, cov_matrix)

constraints = [
    cp.sum(weights) == 1,
    weights >= 0,
]

problem = cp.Problem(cp.Minimize(risk), constraints)
problem.solve()
```

### Athena use

This can support:

```text
Portfolio Optimizer
Efficient Frontier Lab
Risk reduction recommendations
```

### Important

Optimization results depend heavily on inputs.

---

## 24. Target return optimization with cvxpy

Target return optimization minimizes risk while requiring expected return above a threshold.

Example:

```python
expected_returns = np.array([0.08, 0.10, 0.12])
target_return = 0.10

weights = cp.Variable(n_assets)
risk = cp.quad_form(weights, cov_matrix)
portfolio_return = expected_returns @ weights

constraints = [
    cp.sum(weights) == 1,
    weights >= 0,
    portfolio_return >= target_return,
]

problem = cp.Problem(cp.Minimize(risk), constraints)
problem.solve()
```

### Athena use

This can support:

```text
Target return portfolio
Efficient frontier
Scenario-based allocation
```

### Caution

Expected returns are uncertain.

Small changes can produce very different weights.

---

## 25. Long-only constraints

A long-only portfolio has no short positions.

Constraint:

```python
weights >= 0
```

Also:

```python
cp.sum(weights) == 1
```

This means:

```text
Each asset weight is positive or zero.
Total capital is fully allocated.
```

### Athena recommendation

Start with long-only optimization.

Why?

```text
Easier to understand
Safer for beginner users
More intuitive
Less risk of extreme solutions
```

Shorting and leverage can be added later.

---

## 26. Sector and weight constraints

Real portfolios need constraints.

Examples:

```text
No asset above 20%
Technology sector below 35%
Cash above 5%
No shorting
Weights sum to 100%
```

Asset maximum constraint:

```python
weights <= 0.20
```

Sector constraint example:

```python
technology_indices = [0, 2]
cp.sum(weights[technology_indices]) <= 0.35
```

### Athena use

Constraints make optimization more realistic.

Without constraints, optimizers can produce extreme allocations.

---

## 27. cvxpy Athena use cases

Possible Athena use cases:

```text
Minimum variance optimization
Target return optimization
Target volatility optimization
Long-only portfolio allocation
Sector-constrained optimization
Risk budget experiments
Trade impact optimization
```

Possible notebook:

```text
notebooks/03_portfolio_optimization_cvxpy.ipynb
```

Possible backend service:

```text
backend/app/services/optimizer_service.py
```

Suggested tests:

```text
Optimized weights sum to 1.
Long-only weights are non-negative.
Max weight constraint is respected.
Sector constraint is respected.
Minimum variance solution has lower variance than equal weight in known case.
```

---

## 28. PyPortfolioOpt overview

`PyPortfolioOpt` is a library focused on portfolio optimization.

It can help with:

```text
Expected return estimation
Risk model estimation
Efficient frontier
Maximum Sharpe portfolio
Minimum volatility portfolio
Discrete allocation
```

Typical imports:

```python
from pypfopt import EfficientFrontier
from pypfopt import expected_returns
from pypfopt import risk_models
```

### Athena use

PyPortfolioOpt can speed up portfolio optimization prototypes.

But it should not replace understanding of:

```text
Expected returns
Covariance matrix
Constraints
Efficient frontier
Optimization sensitivity
```

---

## 29. PyPortfolioOpt for efficient frontier

Example:

```python
from pypfopt import EfficientFrontier

mu = expected_returns.mean_historical_return(price_data)
S = risk_models.sample_cov(price_data)

ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe()
cleaned_weights = ef.clean_weights()

print(cleaned_weights)
```

### Athena use

This can support:

```text
Maximum Sharpe portfolio
Minimum volatility portfolio
Efficient frontier visualizations
```

### Caution

The output depends on expected return and covariance assumptions.

Always document inputs.

---

## 30. PyPortfolioOpt for expected returns

PyPortfolioOpt includes expected return estimators.

Examples:

```text
Mean historical return
Exponentially weighted mean return
CAPM return
```

Expected returns are one of the weakest parts of optimization.

Why?

```text
Future returns are hard to estimate.
Small changes in expected returns can create large changes in optimal weights.
```

### Athena recommendation

Start with simple assumptions:

```text
Historical mean return
User-defined expected return
Equal expected return for risk-only optimization
```

---

## 31. PyPortfolioOpt for covariance estimation

PyPortfolioOpt includes risk models.

Examples:

```text
Sample covariance
Semi-covariance
Exponentially weighted covariance
Shrinkage methods
```

Covariance estimation matters because portfolio risk depends on correlations and volatilities.

### Athena use

Risk model choices can be exposed later.

Example:

```text
Covariance method: sample covariance
Covariance method: exponentially weighted
```

### Important

Different covariance methods can produce different optimized portfolios.

---

## 32. PyPortfolioOpt for discrete allocation

Optimized weights are percentages.

But real portfolios buy integer quantities.

Example:

```text
AAPL weight = 12.3%
MSFT weight = 8.7%
```

Discrete allocation converts weights into shares.

Example:

```text
Buy 4 AAPL
Buy 2 MSFT
Hold remaining cash
```

PyPortfolioOpt can help with this.

### Athena use

This can support:

```text
Portfolio Optimizer
Trade proposal generator
Rebalancing assistant
```

---

## 33. PyPortfolioOpt Athena use cases

Possible Athena use cases:

```text
Efficient frontier demo
Maximum Sharpe portfolio
Minimum volatility portfolio
Discrete allocation
Portfolio optimizer prototype
Educational notebook
```

Suggested notebook:

```text
notebooks/03_pyportfolioopt_efficient_frontier.ipynb
```

Possible backend use:

```text
Optional, later
```

Recommendation:

```text
Use cvxpy for transparent custom optimization.
Use PyPortfolioOpt for quick portfolio optimization prototypes.
```

---

## 34. arch overview

`arch` is a Python library for autoregressive conditional heteroskedasticity models.

In simpler words, it helps model time-varying volatility.

Common models:

```text
ARCH
GARCH
EGARCH
GJR-GARCH
```

### Why this matters

Financial volatility changes over time.

Markets often show volatility clustering:

```text
Large moves tend to be followed by large moves.
Calm periods tend to be followed by calm periods.
```

### Athena use

`arch` can support advanced volatility modeling later.

---

## 35. Why volatility modeling matters

Volatility is central to:

```text
Risk management
VaR
CVaR
Option pricing
Stress testing
RiskDNA
Portfolio monitoring
```

Simple historical volatility assumes volatility is constant over the calculation window.

But markets often move between regimes:

```text
Calm regime
Normal regime
High volatility regime
Crisis regime
```

Volatility models attempt to estimate and forecast changing volatility.

### Athena caution

Start with simple rolling volatility.

Add GARCH later when the simpler methods are understood.

---

## 36. ARCH and GARCH intuition

ARCH and GARCH models estimate conditional volatility.

Simple intuition:

```text
Today’s volatility depends on recent shocks and past volatility.
```

GARCH is often written conceptually as:

```text
Variance today = constant + recent shock effect + previous variance effect
```

This captures volatility clustering.

### Example

After a large market shock, the model may estimate higher future volatility.

### Athena use

GARCH volatility can later support:

```text
Parametric VaR
Risk regime detection
RiskDNA volatility input
```

---

## 37. arch for volatility forecasting

Example structure:

```python
from arch import arch_model

returns_pct = returns.dropna() * 100

model = arch_model(returns_pct, vol="Garch", p=1, q=1)
result = model.fit(disp="off")

forecast = result.forecast(horizon=1)
print(forecast.variance.iloc[-1])
```

### Important

The `arch` package often expects returns in percent form.

Example:

```text
0.01 return → 1.0 percent
```

### Athena caution

Document units clearly.

Volatility unit mistakes can create huge risk errors.

---

## 38. arch for risk modeling

GARCH forecasts can feed risk models.

Example:

```text
Forecast volatility
Use volatility in parametric VaR
Compare with rolling volatility
Flag volatility regime
```

Possible workflow:

```text
1. Calculate returns.
2. Fit GARCH model.
3. Forecast volatility.
4. Estimate parametric VaR.
5. Compare to historical VaR.
```

### Athena use

This is advanced.

Add only after the basic VaR/CVaR engine works.

---

## 39. arch Athena use cases

Possible Athena use cases:

```text
Volatility forecasting
Volatility regime detection
Advanced parametric VaR
RiskDNA volatility score
Stress testing calibration
```

Suggested notebook:

```text
notebooks/04_garch_volatility_forecast.ipynb
```

Suggested tests:

```text
Model handles returns without missing values.
Volatility forecast is positive.
Units are documented.
Output is not used if model fitting fails.
```

---

## 40. QuantLib overview

`QuantLib` is a powerful quantitative finance library.

It supports:

```text
Fixed income
Yield curves
Interest rate models
Option pricing
Derivatives pricing
Calendars
Day count conventions
Cash flows
Term structures
```

QuantLib is professional-level and powerful, but it can be difficult for beginners.

### Athena recommendation

Do not start with QuantLib too early.

First, implement simple versions manually:

```text
Bond pricing
Duration
Convexity
Spot rates
Black-Scholes
```

Then use QuantLib to compare and extend.

---

## 41. QuantLib for fixed income

Fixed income is one of QuantLib's strengths.

It can support:

```text
Bond pricing
Cash flow schedules
Day count conventions
Yield curves
Discounting
Duration
Convexity
```

### Why this matters

Real fixed income analytics require details:

```text
Coupon schedules
Settlement dates
Business calendars
Day count conventions
Accrued interest
Clean vs dirty price
```

These details are hard to implement perfectly from scratch.

### Athena use

Use QuantLib later for a more professional Fixed Income Lab.

---

## 42. QuantLib for yield curves

QuantLib can build yield curves from market instruments.

Examples:

```text
Deposit rates
Swap rates
Bond yields
Zero curves
Discount curves
Forward curves
```

### Athena simple version

Before QuantLib, Athena can implement:

```text
Simple spot rate table
Linear interpolation
Discount factors
Basic curve chart
```

### QuantLib version later

QuantLib can add:

```text
Calendars
Curve bootstrapping
Day count conventions
Term structures
```

This is advanced and should be added after the basic version works.

---

## 43. QuantLib for bond pricing

QuantLib can price bonds with detailed conventions.

Bond pricing needs:

```text
Face value
Coupon rate
Maturity date
Payment frequency
Day count convention
Calendar
Yield curve
Settlement date
```

### Athena simple version

Manual formula:

```text
Bond price = present value of coupons + present value of principal
```

### QuantLib version

Use QuantLib when you want:

```text
Realistic coupon schedules
Accrued interest
Clean price
Dirty price
Professional conventions
```

---

## 44. QuantLib for option pricing

QuantLib can also price options.

It supports:

```text
European options
American options
Exotic options
Black-Scholes processes
Binomial trees
Monte Carlo methods
```

### Athena first version

Use manual Black-Scholes with SciPy.

Why?

```text
Better for learning
Easier to explain
Easier to test
```

### QuantLib later

Use QuantLib to compare results or support more advanced options.

---

## 45. QuantLib limitations for beginners

QuantLib is powerful but difficult.

Challenges:

```text
Complex API
Finance conventions required
Steep learning curve
Harder debugging
Many object types
Calendar and date complexity
```

### Beginner risk

Using QuantLib too early can lead to copying code without understanding it.

### Athena recommendation

Use this order:

```text
1. Manual formulas
2. SciPy support
3. cvxpy/PyPortfolioOpt for optimization
4. QuantLib for advanced pricing
```

---

## 46. QuantLib Athena use cases

Possible Athena use cases:

```text
Advanced bond pricing
Clean and dirty price calculations
Yield curve bootstrapping
Duration and convexity with conventions
Swap pricing later
Advanced option pricing
Model comparison
```

Suggested notebook:

```text
notebooks/02_quantlib_bond_pricing_demo.ipynb
```

Possible backend service later:

```text
backend/app/services/quantlib_pricing_service.py
```

Suggested tests:

```text
Manual bond price matches QuantLib for simple bond.
Clean plus accrued interest equals dirty price.
Black-Scholes manual price approximately matches QuantLib European option price.
```

---

## 47. yfinance overview

`yfinance` is a Python library commonly used to download Yahoo Finance data.

Example:

```python
import yfinance as yf

data = yf.download("AAPL", start="2020-01-01", end="2026-01-01")
print(data.head())
```

It is useful for:

```text
Learning
Prototyping
Notebook experiments
Historical price examples
```

### Athena caution

yfinance is convenient but not ideal as a professional production data source.

Use it for prototypes and demos, not as the final institutional data source.

---

## 48. yfinance for market data experimentation

Example workflow:

```python
import yfinance as yf

symbols = ["AAPL", "MSFT", "SPY"]
prices = yf.download(symbols, start="2020-01-01")["Adj Close"]

returns = prices.pct_change().dropna()
```

This quickly gives data for:

```text
Return calculations
Volatility
Correlation
Portfolio optimization
VaR/CVaR demos
```

### Athena use

Use yfinance in notebooks like:

```text
notebooks/01_market_data_returns.ipynb
notebooks/04_var_cvar_stress_testing.ipynb
```

For backend demos, consider storing downloaded data locally instead of calling yfinance every time.

---

## 49. yfinance limitations

yfinance has limitations:

```text
Data may change
Availability can vary
Not an official market data feed
Corporate action handling should be checked
Intraday data limitations
Potential rate limits or download issues
No guarantee of institutional quality
```

### Athena recommendation

Use yfinance for:

```text
Education
Prototypes
GitHub demos
Notebook examples
```

Avoid relying on it for:

```text
Official risk reports
Production-grade finance decisions
Institutional analytics
```

### Good practice

Cache downloaded data in:

```text
data/raw/
```

Then run Athena calculations on local data.

---

## 50. yfinance Athena use cases

Possible Athena use cases:

```text
Download sample historical prices
Build demo portfolios
Calculate returns
Demonstrate VaR/CVaR
Demonstrate Black-Scholes inputs
Show rolling volatility
Build portfolio optimization examples
```

Suggested notebook:

```text
notebooks/01_yfinance_market_data_demo.ipynb
```

Suggested backend caution:

```text
Do not make core backend depend directly on yfinance in production.
```

Better pattern:

```text
Data ingestion script downloads prices.
Backend reads validated local/database prices.
```

---

## 51. pandas-datareader overview

`pandas-datareader` can fetch data from several online sources.

It is useful for:

```text
Economic data
Market data experiments
FRED data
Interest rates
Macroeconomic series
```

Example use case:

```text
Download risk-free rate proxy
Download inflation data
Download economic indicators
```

### Athena use

pandas-datareader can support:

```text
Rates Lab
Macroeconomic context
Risk-free rate assumptions
Market regime analysis
```

### Caution

Like yfinance, data source reliability and terms matter.

Use for learning and prototypes.

---

## 52. pandas-datareader use cases

Possible use cases:

```text
Fetch Treasury rates
Fetch central bank data
Fetch inflation series
Fetch market index data
Fetch macro indicators
```

Example Athena notebook:

```text
notebooks/02_rates_macro_data_demo.ipynb
```

Possible use in Athena:

```text
Risk-free rate assumptions
Yield curve references
Macro regime dashboard later
```

### Recommendation

Use it after mastering:

```text
pandas
market data cleaning
basic rate concepts
```

Do not overcomplicate early.

---

## 53. OpenBB overview

OpenBB is an open-source investment research platform and toolkit.

It can provide access to:

```text
Market data
Fundamental data
Economic data
News
Alternative datasets
Research workflows
```

### Athena use

OpenBB can be useful later for richer research workflows.

Potential use cases:

```text
Market data exploration
Equity fundamentals
Macro data
News-related research
Investment dashboard experiments
```

### Caution

OpenBB may be more than Athena needs at the beginning.

Start simple.

---

## 54. OpenBB use cases

Possible Athena use cases:

```text
Market research notebooks
Fundamental data enrichment
Macro dashboard
Sector analysis
Data source experimentation
```

Suggested approach:

```text
Do not integrate OpenBB into backend immediately.
Use it in notebooks first.
```

Why?

```text
Athena should keep backend dependencies controlled.
```

OpenBB can be explored after the core platform is stable.

---

## 55. Riskfolio-Lib overview

Riskfolio-Lib is a portfolio optimization and risk analysis library.

It supports many risk measures and optimization methods.

Possible features:

```text
Mean-risk optimization
CVaR optimization
Risk parity
Hierarchical risk parity
Multiple risk measures
```

### Athena use

Riskfolio-Lib can support advanced portfolio construction later.

It is especially interesting because Athena already focuses on VaR, CVaR and risk management.

### Caution

It is more advanced.

Use it after understanding:

```text
Portfolio volatility
Covariance matrix
VaR
CVaR
Optimization constraints
```

---

## 56. Riskfolio-Lib use cases

Possible Athena use cases:

```text
CVaR-based portfolio optimization
Risk parity
Hierarchical risk parity
Advanced efficient frontier
Risk-budgeting experiments
```

Suggested notebook:

```text
notebooks/03_riskfolio_portfolio_optimization.ipynb
```

Potential module later:

```text
Portfolio Optimizer Pro
```

### Recommendation

Do not start with Riskfolio-Lib.

Start with:

```text
Manual formulas
cvxpy
PyPortfolioOpt
```

Then explore Riskfolio-Lib.

---

## 57. vectorbt overview

`vectorbt` is a Python library for vectorized backtesting and strategy research.

It can support:

```text
Fast backtests
Portfolio simulation
Trading strategy research
Signal testing
Performance analysis
```

### Athena use

Athena is not primarily a trading strategy platform.

But vectorbt can be useful for:

```text
Educational backtests
Strategy demonstration
Risk of trading rules
Portfolio research notebooks
```

### Caution

Backtesting can be misleading if done poorly.

Common problems:

```text
Look-ahead bias
Survivorship bias
Ignoring fees
Ignoring slippage
Overfitting
```

---

## 58. vectorbt for backtesting

Example use case:

```text
Test moving average crossover strategy.
Analyze returns.
Calculate drawdown.
Compare benchmark.
```

Athena could use vectorbt in notebooks to demonstrate:

```text
How strategy returns behave
How risk metrics apply to strategies
How drawdowns emerge
How transaction costs affect results
```

### Recommendation

Use vectorbt only after core risk analytics are stable.

Athena's main identity should remain:

```text
Risk terminal
Portfolio analytics
Risk workflow
```

not a pure trading strategy platform.

---

## 59. backtrader overview

`backtrader` is another Python backtesting framework.

It is event-driven and strategy-oriented.

It can support:

```text
Strategy logic
Order simulation
Portfolio value tracking
Broker simulation
Indicators
```

### Athena use

Backtrader is optional.

It may be useful if Athena later includes:

```text
Strategy testing
Order simulation
Trading logic education
```

### Recommendation

For Athena's current roadmap, backtesting is secondary.

Focus first on:

```text
Market data
Portfolio analytics
Risk
Options
P&L
Reporting
```

---

## 60. Backtesting libraries caution

Backtesting can look impressive but be dangerous.

Common beginner mistakes:

```text
Using future data accidentally
Ignoring transaction costs
Ignoring slippage
Ignoring liquidity
Optimizing too many parameters
Testing too many strategies until one works
Not using out-of-sample data
```

### Athena principle

If Athena includes backtesting later, it must include warnings about:

```text
Look-ahead bias
Overfitting
Costs
Data quality
Survivorship bias
```

Backtesting should support learning, not fake certainty.

---

## 61. Library selection strategy

Athena should not use every library immediately.

Recommended strategy:

```text
1. Use the basic stack for core calculations.
2. Add statsmodels for regression and beta.
3. Add cvxpy for optimization.
4. Add scikit-learn for anomaly detection experiments.
5. Add yfinance for notebook data.
6. Add PyPortfolioOpt for portfolio optimization prototypes.
7. Add arch for advanced volatility.
8. Add QuantLib for advanced fixed income and pricing.
```

### Keep dependencies controlled

Too many dependencies can create:

```text
Installation problems
Version conflicts
Harder deployment
More complex debugging
```

Use libraries intentionally.

---

## 62. Build vs use a library

Sometimes Athena should build formulas manually.

Sometimes it should use a library.

### Build manually when

```text
The formula is simple.
Learning is important.
Transparency matters.
Testing is easy.
You need full control.
```

Examples:

```text
Simple returns
Volatility
Historical VaR
Historical CVaR
Basic Black-Scholes
Bond present value
```

### Use a library when

```text
The model is complex.
Conventions matter.
Optimization is non-trivial.
A trusted implementation exists.
You need advanced functionality.
```

Examples:

```text
Constrained optimization
Detailed bond conventions
Advanced volatility modeling
Advanced portfolio optimization
```

---

## 63. When to code formulas manually

Code manually for the educational core.

Manual implementation helps you understand the model.

Good manual targets:

```text
Simple returns
Log returns
Annualized volatility
Covariance
Correlation
Historical VaR
Historical CVaR
Drawdown
Portfolio weights
Basic bond pricing
Basic Black-Scholes
Basic Greeks
```

### Athena advantage

Manual formulas make your project more credible because you can explain what you built.

Then later, compare with libraries.

---

## 64. When to use a specialized library

Use specialized libraries when complexity becomes high.

Examples:

```text
cvxpy for constrained optimization
QuantLib for real fixed income conventions
arch for GARCH volatility models
PyPortfolioOpt for quick efficient frontier prototypes
Riskfolio-Lib for advanced risk-based optimization
```

### Rule

Use a library when it adds:

```text
Reliability
Professional conventions
Speed
Advanced methods
Cleaner implementation
```

Do not use a library only to make the project look advanced.

---

## 65. How to document library assumptions

Every library use should have methodology notes.

Document:

```text
Library name
Version if relevant
Function used
Inputs
Outputs
Assumptions
Limitations
Validation method
```

Example:

```text
Optimization method: cvxpy minimum variance
Constraints: long-only, weights sum to 1, max asset weight 20%
Covariance: sample covariance from daily returns
Expected returns: not used
```

### Athena use

Put methodology notes in:

```text
docs/
backend service docstrings
API response metadata
reports
```

---

## 66. How to validate library outputs

Validation is essential.

Validation methods:

```text
Compare to manual calculation
Use known test cases
Check constraints
Check output ranges
Check edge cases
Backtest where applicable
Cross-check with another library
```

Example:

```text
Manual Black-Scholes call price ≈ QuantLib European option price.
```

Example:

```text
Optimized weights sum to 1 and are non-negative.
```

### Athena rule

Never trust library output without tests.

---

## 67. How to avoid black-box usage

To avoid black-box usage:

```text
Read the documentation
Understand the inputs
Understand the outputs
Document assumptions
Write small examples
Compare with manual formulas
Add tests
Expose methodology to users
```

Bad:

```text
The library says the portfolio is optimal.
```

Better:

```text
The portfolio minimizes variance under long-only constraints using the sample covariance matrix from daily returns.
```

Athena should always prefer the second style.

---

## 68. Suggested learning order

Recommended learning order:

```text
1. statsmodels basic regression
2. scikit-learn preprocessing and pipelines
3. cvxpy basic optimization
4. yfinance for data experiments
5. PyPortfolioOpt efficient frontier
6. arch GARCH models
7. QuantLib basic bond pricing
8. Riskfolio-Lib risk-based optimization
9. vectorbt basic backtesting
10. OpenBB exploration
```

### For Athena right now

Highest priority:

```text
statsmodels
cvxpy
scikit-learn basics
yfinance for notebooks
```

Later:

```text
QuantLib
arch
Riskfolio-Lib
vectorbt
```

---

## 69. Athena module mapping

### Market Finance

```text
yfinance
pandas-datareader
OpenBB later
```

### Portfolio Management

```text
cvxpy
PyPortfolioOpt
Riskfolio-Lib later
```

### Risk Management

```text
statsmodels
arch
scikit-learn for anomalies
```

### Fixed Income

```text
QuantLib later
SciPy first
```

### Options

```text
SciPy first
QuantLib later
```

### RiskDNA

```text
scikit-learn
statsmodels
deterministic scoring first
```

### P&L Reporting

```text
pandas first
scikit-learn later for anomaly detection
```

---

## 70. Suggested notebooks

Recommended notebooks:

```text
notebooks/
├── 02_01_statsmodels_beta_alpha.ipynb
├── 02_02_cvxpy_minimum_variance.ipynb
├── 02_03_pyportfolioopt_efficient_frontier.ipynb
├── 02_04_sklearn_risk_anomaly_detection.ipynb
├── 02_05_arch_garch_volatility.ipynb
├── 02_06_quantlib_bond_pricing.ipynb
└── 02_07_yfinance_market_data_demo.ipynb
```

Each notebook should include:

```text
Objective
Imports
Data loading
Methodology
Calculation
Visualization
Conclusion
Next step for backend
```

---

## 71. Suggested backend services

Possible backend services:

```text
backend/app/services/regression_service.py
backend/app/services/optimizer_service.py
backend/app/services/anomaly_service.py
backend/app/services/volatility_model_service.py
backend/app/services/pricing_service.py
backend/app/services/market_data_ingestion_service.py
```

### Recommended first services

```text
regression_service.py
optimizer_service.py
```

### Later services

```text
anomaly_service.py
volatility_model_service.py
quantlib_pricing_service.py
```

Keep advanced services optional until core app works.

---

## 72. Suggested tests

### statsmodels tests

```text
Beta is correct for known linear relationship.
Regression handles missing values after cleaning.
Output includes alpha, beta and R-squared.
```

### cvxpy tests

```text
Weights sum to 1.
Weights are non-negative for long-only optimization.
Max weight constraint is respected.
Sector constraint is respected.
```

### scikit-learn tests

```text
Pipeline fits and predicts without error.
Fixed random seed produces stable output.
Anomaly labels are in expected set.
```

### PyPortfolioOpt tests

```text
Weights sum approximately to 1.
Cleaned weights are valid.
Discrete allocation does not exceed budget.
```

### QuantLib tests

```text
Simple bond price matches manual present value in simplified case.
European option price roughly matches manual Black-Scholes.
```

---

## 73. Common beginner mistakes

### Mistake 1 — Using too many libraries too early

This makes the project complex and hard to debug.

### Mistake 2 — Not understanding the model

A library output is not useful if you cannot explain it.

### Mistake 3 — Ignoring assumptions

Every library function has assumptions.

### Mistake 4 — No tests

Financial model outputs must be tested.

### Mistake 5 — Confusing prototype and production

A notebook demo is not automatically backend-ready.

### Mistake 6 — Treating predictions as certainty

ML outputs are uncertain and can fail.

### Mistake 7 — Ignoring data quality

Advanced libraries cannot fix bad data.

### Mistake 8 — Overfitting

Especially dangerous in ML and backtesting.

### Mistake 9 — Not documenting versions

Library behavior can change across versions.

### Mistake 10 — Building a black box

Athena should be explainable.

---

## 74. Example architecture

Possible structure:

```text
athena-ai-risk-terminal/
├── docs/
│   └── libraries/
│       ├── README.md
│       ├── 01-python-data-stack.md
│       ├── 02-quant-finance-libraries.md
│       ├── 03-backend-stack.md
│       ├── 04-frontend-stack.md
│       ├── 05-ai-stack.md
│       └── 06-testing-and-devops.md
├── notebooks/
│   ├── 02_01_statsmodels_beta_alpha.ipynb
│   ├── 02_02_cvxpy_minimum_variance.ipynb
│   └── 02_03_sklearn_anomaly_detection.ipynb
├── backend/
│   └── app/
│       └── services/
│           ├── regression_service.py
│           ├── optimizer_service.py
│           └── anomaly_service.py
└── frontend/
```

### Principle

Docs explain the library.  
Notebooks explore it.  
Backend services productionize it.  
Frontend displays results.

---

## 75. Summary

Quant finance libraries help Athena move beyond basic data manipulation into professional quantitative analytics.

Important libraries:

```text
statsmodels     = regression, alpha, beta, econometrics
scikit-learn    = machine learning, anomaly detection, pipelines
cvxpy           = constrained optimization
PyPortfolioOpt  = portfolio optimization prototypes
arch            = volatility modeling
QuantLib        = advanced fixed income and pricing
yfinance        = market data experiments
pandas-datareader = economic and market data
OpenBB          = broader research toolkit
Riskfolio-Lib   = advanced risk-based optimization
vectorbt/backtrader = backtesting experiments
```

Most important principle:

```text
Do not use libraries as black boxes.
```

Athena should follow this workflow:

```text
Understand the model.
Implement a simple version manually.
Prototype with a library.
Validate the output.
Document assumptions.
Move stable logic into backend services.
Add tests.
Display results clearly in the frontend.
```

The goal is not to collect libraries.

The goal is to build a credible, explainable and tested quantitative finance platform.
