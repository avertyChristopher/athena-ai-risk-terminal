# 01 — Python Data Stack

**Project:** Athena AI Risk Terminal  
**Recommended file path:** `docs/libraries/01-python-data-stack.md`  
**Purpose:** learn the core Python data libraries needed to manipulate market data, calculate returns, analyze volatility, clean datasets, build notebooks, prototype quantitative methods and later move clean logic into Athena's backend.  
**Scope:** this document focuses on the foundational Python data stack: Python environment basics, Jupyter notebooks, NumPy, pandas, matplotlib and SciPy. More specialized quant finance libraries are documented separately.

---

## Table of Contents

1. What is the Python data stack?
2. Why Python is used in finance and risk analytics
3. Role of the data stack in Athena
4. Python environment basics
5. Virtual environments
6. Requirements files
7. Jupyter notebooks
8. Python scripts vs notebooks
9. NumPy overview
10. NumPy arrays
11. Vectorized calculations
12. Basic mathematical operations with NumPy
13. Random numbers and simulations
14. NumPy for returns
15. NumPy for volatility
16. NumPy for covariance and correlation
17. NumPy common beginner mistakes
18. pandas overview
19. Series and DataFrames
20. Reading CSV files
21. Reading Excel files
22. Reading parquet files
23. DataFrame indexing
24. Selecting columns
25. Filtering rows
26. Sorting data
27. Handling dates
28. Datetime index
29. Resampling time series
30. Missing data
31. Filling missing values
32. Dropping missing values
33. Duplicates
34. Outliers
35. Data cleaning workflow
36. Market price data with pandas
37. OHLCV data structure
38. Adjusted close
39. Calculating simple returns
40. Calculating log returns
41. Rolling windows
42. Rolling volatility
43. Rolling correlation
44. Cumulative returns
45. Drawdown calculation
46. GroupBy operations
47. Aggregation
48. Pivot tables
49. Merging datasets
50. Joining market data with portfolio data
51. Exporting cleaned data
52. matplotlib overview
53. Line charts
54. Histograms
55. Scatter plots
56. Drawdown charts
57. Return distribution charts
58. Yield curve charts
59. Plotting best practices
60. SciPy overview
61. SciPy stats module
62. Normal distribution
63. Percentiles and quantiles
64. Optimization basics
65. Root finding
66. Interpolation basics
67. SciPy for VaR and CVaR
68. SciPy for Black-Scholes
69. SciPy for yield curves
70. Python data validation
71. Type hints
72. Dataclasses
73. Pydantic preview
74. Data quality checks
75. Reproducible notebooks
76. From notebook to backend service
77. Folder structure for notebooks
78. Common Athena datasets
79. Suggested notebook exercises
80. Suggested backend functions
81. Suggested tests
82. Common beginner mistakes
83. Key formulas implemented with Python
84. How Athena uses the Python data stack
85. Summary

---

## 1. What is the Python data stack?

The Python data stack is the set of core Python libraries used to load, clean, transform, analyze and visualize data.

For Athena AI Risk Terminal, the Python data stack is the foundation of the quantitative engine.

It helps transform raw financial data into useful analytics.

Example raw input:

```text
Date
Open
High
Low
Close
Adjusted Close
Volume
```

Example output:

```text
Daily returns
Annualized volatility
Rolling volatility
Correlation matrix
Loss distribution
VaR
CVaR
Drawdown
P&L attribution
```

The core libraries are:

```text
NumPy
pandas
matplotlib
SciPy
Jupyter
```

Simple roles:

```text
NumPy      = numerical calculations
pandas     = tabular and time series data
matplotlib = charts and visual exploration
SciPy      = statistics, distributions, optimization and numerical methods
Jupyter    = notebooks for exploration and learning
```

### Athena intuition

Athena will have:

```text
docs/      = theory and methodology
notebooks/ = experimentation and learning
backend/   = clean reusable services and APIs
frontend/  = user interface
```

The Python data stack is used mainly in:

```text
notebooks/
backend/
tests/
```

---

## 2. Why Python is used in finance and risk analytics

Python is widely used in finance because it is flexible, readable and has a strong ecosystem for data analysis.

Python is useful for:

```text
Market data analysis
Portfolio analytics
Risk metrics
VaR and CVaR
Stress testing
Option pricing
Backtesting
P&L attribution
Reporting automation
Machine learning
```

Python is also useful because the same language can be used for:

```text
Research notebooks
Backend services
Data pipelines
Testing
Automation scripts
```

### Example finance workflow

```text
1. Load market prices with pandas.
2. Calculate returns with pandas and NumPy.
3. Estimate volatility with NumPy.
4. Calculate VaR with NumPy or SciPy.
5. Plot loss distribution with matplotlib.
6. Move the final logic into FastAPI backend services.
```

### Why this matters for Athena

Athena is a finance/risk terminal, so it needs to calculate things correctly.

The frontend can look beautiful, but the backend must be mathematically reliable.

The Python data stack is where the quantitative reliability starts.

---

## 3. Role of the data stack in Athena

In Athena, the Python data stack supports almost every finance module.

### Market Finance & Volatility

Used for:

```text
Loading prices
Calculating returns
Calculating volatility
Rolling windows
Correlation
Data quality checks
```

### Fixed Income, Yield Curves & Bonds

Used for:

```text
Discount factors
Bond cash flows
Yield curve tables
Interpolation
Duration approximations
```

### Portfolio Management

Used for:

```text
Position weights
Portfolio returns
Covariance matrix
Correlation matrix
Drawdowns
Benchmark comparison
```

### Risk Management

Used for:

```text
Loss distributions
Historical VaR
Historical CVaR
Stress test calculations
Risk contribution tables
```

### Options, Black-Scholes & Greeks

Used for:

```text
Black-Scholes formulas
Normal distribution functions
Greeks
Sensitivity analysis
Payoff tables
```

### P&L Attribution

Used for:

```text
Position-level P&L
Portfolio-level P&L
FX effects
Top contributors
Worst contributors
Explained vs unexplained P&L
```

---

## 4. Python environment basics

A Python environment is the setup used to run Python code and install libraries.

Important components:

```text
Python version
Virtual environment
Installed packages
Requirements file
Notebook kernel
Environment variables
```

### Recommended Python version

For Athena, use a modern Python version such as:

```text
Python 3.11 or Python 3.12
```

A stable version is usually better than the newest experimental version.

### Check Python version

```bash
python --version
```

or:

```bash
py --version
```

On Windows, `py` is often available when `python` is not correctly mapped.

### Project principle

Each project should have its own environment.

Do not install everything globally.

---

## 5. Virtual environments

A virtual environment isolates project dependencies.

Without a virtual environment, packages from different projects can conflict.

### Create a virtual environment

From the project root:

```bash
python -m venv .venv
```

or on Windows:

```powershell
py -m venv .venv
```

### Activate on Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Activate on macOS/Linux

```bash
source .venv/bin/activate
```

### Install packages

```bash
pip install pandas numpy matplotlib scipy jupyter
```

### Deactivate

```bash
deactivate
```

### Athena recommendation

For Athena, keep the virtual environment out of Git.

Add this to `.gitignore`:

```text
.venv/
venv/
```

---

## 6. Requirements files

A requirements file records Python dependencies.

Common file:

```text
requirements.txt
```

Example:

```text
numpy
pandas
matplotlib
scipy
jupyter
```

Install from requirements:

```bash
pip install -r requirements.txt
```

Generate current environment:

```bash
pip freeze > requirements.txt
```

### Important caution

`pip freeze` can include too many dependencies.

For a clean learning project, it is often better to manually maintain a simple requirements file at first.

### Athena possible structure

```text
requirements.txt              # general local notebooks
backend/requirements.txt       # backend dependencies
```

Example root requirements for notebooks:

```text
numpy
pandas
matplotlib
scipy
jupyter
ipykernel
```

Example backend requirements:

```text
fastapi
uvicorn
pydantic
sqlalchemy
psycopg2-binary
pytest
numpy
pandas
scipy
```

---

## 7. Jupyter notebooks

Jupyter notebooks are interactive documents containing code, text, formulas and charts.

They are excellent for learning and experimentation.

Notebook files use:

```text
.ipynb
```

Example:

```text
notebooks/01_market_data_returns.ipynb
```

### What notebooks are good for

Notebooks are useful for:

```text
Exploring data
Testing formulas
Building charts
Trying VaR/CVaR calculations
Prototyping Black-Scholes
Explaining methodology
Creating educational demos
```

### What notebooks are not good for

Notebooks are not ideal for:

```text
Production backend code
Large application architecture
Reusable service logic
API endpoints
Complex testing
```

### Athena rule

Use notebooks to learn and prototype.

Move stable logic into backend services.

---

## 8. Python scripts vs notebooks

Python scripts and notebooks have different roles.

### Notebooks

Good for:

```text
Exploration
Learning
Visual explanation
Step-by-step analysis
Charts
```

Example:

```text
notebooks/04_var_cvar_exploration.ipynb
```

### Scripts

Good for:

```text
Reusable code
Backend services
Tests
Command-line tools
Automation
```

Example:

```text
backend/app/services/risk_service.py
```

### Athena workflow

```text
1. Prototype in notebook.
2. Validate logic with examples.
3. Move formulas into backend service.
4. Add unit tests.
5. Expose through FastAPI endpoint.
6. Display in frontend.
```

### Example

Notebook prototype:

```python
var_95 = losses.quantile(0.95)
```

Backend service:

```python
def historical_var(losses: pd.Series, confidence_level: float = 0.95) -> float:
    return float(losses.quantile(confidence_level))
```

Test:

```python
def test_historical_var_returns_expected_percentile():
    ...
```

---

## 9. NumPy overview

NumPy is the core Python library for numerical computing.

It provides:

```text
Arrays
Vectorized operations
Mathematical functions
Linear algebra
Random numbers
Statistics
```

Import convention:

```python
import numpy as np
```

### Why NumPy matters in finance

Finance calculations often involve arrays of numbers:

```text
Prices
Returns
Weights
Volatilities
Covariances
Simulated scenarios
Loss distributions
```

NumPy makes these calculations fast and concise.

### Example

```python
import numpy as np

returns = np.array([0.01, -0.02, 0.015, 0.005])
average_return = np.mean(returns)
volatility = np.std(returns)

print(average_return)
print(volatility)
```

---

## 10. NumPy arrays

A NumPy array stores numerical data efficiently.

Example:

```python
import numpy as np

prices = np.array([100, 102, 101, 105])
print(prices)
```

Output:

```text
[100 102 101 105]
```

### Array vs list

Python list:

```python
prices_list = [100, 102, 101, 105]
```

NumPy array:

```python
prices_array = np.array([100, 102, 101, 105])
```

NumPy arrays support vectorized math.

Example:

```python
prices_array * 2
```

Output:

```text
array([200, 204, 202, 210])
```

With a Python list, `prices_list * 2` repeats the list instead of multiplying values.

### Athena use

Use arrays for:

```text
Return vectors
Portfolio weights
Monte Carlo simulations
Covariance matrices
```

---

## 11. Vectorized calculations

Vectorization means applying operations to entire arrays at once instead of using loops.

Example:

```python
import numpy as np

prices = np.array([100, 102, 101, 105])
returns = prices[1:] / prices[:-1] - 1

print(returns)
```

Output:

```text
[ 0.02       -0.00980392  0.03960396]
```

### Why vectorization matters

Vectorization is:

```text
Faster
Cleaner
Less error-prone
Closer to mathematical notation
```

### Loop version

```python
returns = []

for i in range(1, len(prices)):
    returns.append(prices[i] / prices[i - 1] - 1)
```

### Vectorized version

```python
returns = prices[1:] / prices[:-1] - 1
```

The vectorized version is better for quantitative work.

---

## 12. Basic mathematical operations with NumPy

NumPy provides many mathematical functions.

Common functions:

```python
np.mean()
np.std()
np.var()
np.sum()
np.min()
np.max()
np.sqrt()
np.log()
np.exp()
np.percentile()
np.quantile()
```

### Example

```python
import numpy as np

returns = np.array([0.01, -0.02, 0.015, 0.005])

mean_return = np.mean(returns)
volatility = np.std(returns, ddof=1)
variance = np.var(returns, ddof=1)
minimum = np.min(returns)
maximum = np.max(returns)

print(mean_return)
print(volatility)
print(variance)
print(minimum)
print(maximum)
```

### Note on `ddof`

For sample standard deviation, use:

```python
np.std(returns, ddof=1)
```

For population standard deviation, use:

```python
np.std(returns, ddof=0)
```

In finance, sample standard deviation is often used for historical data.

---

## 13. Random numbers and simulations

NumPy can generate random numbers for simulations.

Example:

```python
import numpy as np

rng = np.random.default_rng(seed=42)
simulated_returns = rng.normal(loc=0.001, scale=0.02, size=1000)
```

Where:

```text
loc = mean
scale = standard deviation
size = number of simulations
```

### Why seed matters

A seed makes simulations reproducible.

```python
rng = np.random.default_rng(seed=42)
```

Without a seed, results change every time.

### Athena use

Random simulations can be used for:

```text
Monte Carlo VaR
Scenario simulation
Option price simulation later
Portfolio return simulation
```

### Important

Simulations depend on assumptions.

Do not treat simulated results as guaranteed predictions.

---

## 14. NumPy for returns

Simple returns can be calculated with NumPy.

Formula:

```text
Return_t = Price_t / Price_{t-1} - 1
```

Example:

```python
import numpy as np

prices = np.array([100, 102, 101, 105], dtype=float)
returns = prices[1:] / prices[:-1] - 1

print(returns)
```

Output:

```text
[ 0.02       -0.00980392  0.03960396]
```

### Log returns

Formula:

```text
Log return = ln(Price_t / Price_{t-1})
```

Code:

```python
log_returns = np.log(prices[1:] / prices[:-1])
```

### Athena use

Returns are used for:

```text
Volatility
Correlation
VaR
CVaR
Drawdown
Portfolio analytics
```

---

## 15. NumPy for volatility

Volatility measures the dispersion of returns.

Daily volatility:

```python
daily_volatility = np.std(returns, ddof=1)
```

Annualized volatility:

```python
annualized_volatility = daily_volatility * np.sqrt(252)
```

Why 252?

```text
There are approximately 252 trading days in a year.
```

Example:

```python
import numpy as np

returns = np.array([0.01, -0.02, 0.015, 0.005])
daily_vol = np.std(returns, ddof=1)
annualized_vol = daily_vol * np.sqrt(252)

print(daily_vol)
print(annualized_vol)
```

### Athena use

Volatility is used in:

```text
Market Finance
Risk Management
Black-Scholes
RiskDNA
Portfolio monitoring
```

---

## 16. NumPy for covariance and correlation

Covariance and correlation measure how assets move together.

### Example returns matrix

Rows are observations.  
Columns are assets.

```python
import numpy as np

returns = np.array([
    [0.01, 0.02],
    [-0.01, -0.005],
    [0.015, 0.01],
    [0.00, -0.002],
])
```

### Covariance matrix

```python
cov_matrix = np.cov(returns, rowvar=False)
print(cov_matrix)
```

### Correlation matrix

```python
corr_matrix = np.corrcoef(returns, rowvar=False)
print(corr_matrix)
```

### Athena use

Covariance and correlation are used for:

```text
Portfolio volatility
Diversification analysis
Risk contribution
Portfolio optimization later
```

---

## 17. NumPy common beginner mistakes

### Mistake 1 — Using Python lists like arrays

Bad:

```python
prices = [100, 102, 101]
prices * 2
```

This repeats the list.

Better:

```python
prices = np.array([100, 102, 101])
prices * 2
```

### Mistake 2 — Forgetting `dtype=float`

If calculations involve division, use float arrays.

```python
prices = np.array([100, 102, 101], dtype=float)
```

### Mistake 3 — Confusing variance and volatility

```text
Variance = squared volatility
Volatility = standard deviation
```

### Mistake 4 — Forgetting annualization

Daily volatility and annualized volatility are not the same.

### Mistake 5 — Not setting a random seed

Simulations without seeds are harder to reproduce.

---

## 18. pandas overview

pandas is the core library for working with tabular and time series data.

Import convention:

```python
import pandas as pd
```

pandas provides:

```text
Series
DataFrames
Date handling
CSV and Excel reading
Missing data handling
GroupBy
Merging
Resampling
Rolling windows
Time series analysis
```

### Why pandas matters in finance

Financial data is usually tabular and time-indexed.

Examples:

```text
Daily prices
Portfolio positions
Trades
P&L records
Risk metrics
Yield curve points
Option inputs
```

pandas is the main tool to manipulate these datasets.

---

## 19. Series and DataFrames

A pandas Series is one column of data.

A DataFrame is a table.

### Series example

```python
import pandas as pd

returns = pd.Series([0.01, -0.02, 0.015])
print(returns)
```

### DataFrame example

```python
import pandas as pd

data = {
    "date": ["2026-04-27", "2026-04-28", "2026-04-29"],
    "close": [100, 102, 101],
}

prices = pd.DataFrame(data)
print(prices)
```

Output:

```text
         date  close
0  2026-04-27    100
1  2026-04-28    102
2  2026-04-29    101
```

### Athena use

Use DataFrames for:

```text
Market prices
Portfolio positions
Trades
Risk metrics
P&L attribution
```

---

## 20. Reading CSV files

CSV files are common for market data and exports.

Example:

```python
import pandas as pd

prices = pd.read_csv("data/raw/aapl_prices.csv")
```

### Parse dates

```python
prices = pd.read_csv("data/raw/aapl_prices.csv", parse_dates=["date"])
```

### Inspect data

```python
print(prices.head())
print(prices.info())
print(prices.describe())
```

### Common CSV columns

```text
date
open
high
low
close
adjusted_close
volume
```

### Athena rule

Always inspect imported data before calculating.

---

## 21. Reading Excel files

Excel files are common in finance.

Read Excel:

```python
import pandas as pd

positions = pd.read_excel("data/raw/positions.xlsx")
```

Read a specific sheet:

```python
positions = pd.read_excel("data/raw/positions.xlsx", sheet_name="Positions")
```

### Common use cases

```text
Portfolio positions
Manual trade files
Reports
Risk limits
Benchmark mappings
```

### Athena caution

Excel files are flexible but risky.

They may contain:

```text
Hidden formulas
Merged cells
Manual errors
Wrong formats
Multiple sheets
```

Validate Excel inputs carefully.

---

## 22. Reading parquet files

Parquet is a columnar file format useful for larger datasets.

Read parquet:

```python
import pandas as pd

prices = pd.read_parquet("data/processed/prices.parquet")
```

Write parquet:

```python
prices.to_parquet("data/processed/prices_clean.parquet", index=False)
```

### Why parquet is useful

Parquet is:

```text
Efficient
Compressed
Fast to read
Good for large tables
Preserves column types better than CSV
```

### Athena use

Use parquet for processed market data and large datasets.

---

## 23. DataFrame indexing

Indexing means selecting rows or columns from a DataFrame.

Example:

```python
import pandas as pd

df = pd.DataFrame({
    "symbol": ["AAPL", "MSFT", "NVDA"],
    "price": [200, 420, 900],
})
```

Select a column:

```python
df["price"]
```

Select multiple columns:

```python
df[["symbol", "price"]]
```

Select by row label with `.loc`:

```python
df.loc[0]
```

Select by row position with `.iloc`:

```python
df.iloc[0]
```

### Common rule

```text
Use .loc for labels.
Use .iloc for positions.
```

---

## 24. Selecting columns

Selecting columns is a basic pandas operation.

Single column:

```python
prices["adjusted_close"]
```

Multiple columns:

```python
prices[["date", "adjusted_close", "volume"]]
```

Create a smaller DataFrame:

```python
market_data = prices[["date", "symbol", "adjusted_close"]]
```

### Athena use

In Athena, select only needed columns before calculations.

Example:

```python
returns_input = prices[["date", "symbol", "adjusted_close"]]
```

This makes code clearer and reduces mistakes.

---

## 25. Filtering rows

Filtering rows means keeping only rows that match a condition.

Example:

```python
aapl = prices[prices["symbol"] == "AAPL"]
```

Filter by date:

```python
recent = prices[prices["date"] >= "2026-01-01"]
```

Filter multiple conditions:

```python
filtered = prices[
    (prices["symbol"] == "AAPL") &
    (prices["volume"] > 1_000_000)
]
```

### Athena use

Filtering is used for:

```text
Selecting one asset
Selecting date ranges
Removing invalid rows
Filtering portfolios
Selecting risk windows
```

---

## 26. Sorting data

Sorting is important for time series calculations.

Example:

```python
prices = prices.sort_values(["symbol", "date"])
```

Why?

Returns require prices in chronological order.

Bad:

```text
2026-04-29
2026-04-27
2026-04-28
```

Good:

```text
2026-04-27
2026-04-28
2026-04-29
```

### Athena rule

Always sort by date before calculating returns.

For multiple assets:

```python
prices = prices.sort_values(["symbol", "date"])
```

---

## 27. Handling dates

Dates are critical in finance.

Convert a column to datetime:

```python
prices["date"] = pd.to_datetime(prices["date"])
```

Extract year:

```python
prices["year"] = prices["date"].dt.year
```

Extract month:

```python
prices["month"] = prices["date"].dt.month
```

### Common date problems

```text
Dates stored as strings
Mixed date formats
Time zones
Missing dates
Non-trading days
Duplicate dates
```

### Athena rule

Dates should be parsed and validated before analysis.

---

## 28. Datetime index

A datetime index makes time series operations easier.

Example:

```python
prices = prices.set_index("date")
```

Now you can filter by date:

```python
prices.loc["2026-01-01":"2026-03-31"]
```

### Resample with datetime index

```python
monthly_prices = prices["adjusted_close"].resample("ME").last()
```

### Athena use

Use datetime index in notebooks for time series analysis.

In backend services, be careful: explicit date columns can be easier to validate and serialize through APIs.

---

## 29. Resampling time series

Resampling changes data frequency.

Examples:

```text
Daily to monthly
Daily to weekly
Intraday to daily
```

Example monthly last price:

```python
monthly = prices["adjusted_close"].resample("ME").last()
```

Example weekly last price:

```python
weekly = prices["adjusted_close"].resample("W").last()
```

Example monthly returns:

```python
monthly_returns = monthly.pct_change()
```

### Athena use

Resampling is useful for:

```text
Monthly reports
Weekly dashboards
Long-term performance charts
Risk summaries by period
```

---

## 30. Missing data

Missing data appears often in financial datasets.

Examples:

```text
Missing price
Missing volume
Missing FX rate
Missing benchmark return
Missing sector
```

Check missing values:

```python
prices.isna().sum()
```

Rows with missing adjusted close:

```python
missing_prices = prices[prices["adjusted_close"].isna()]
```

### Why missing data matters

Missing prices can break:

```text
Returns
Volatility
VaR
CVaR
P&L
Charts
```

### Athena rule

Never ignore missing data silently.

---

## 31. Filling missing values

Filling missing values can be useful but dangerous.

Forward fill:

```python
prices["adjusted_close"] = prices["adjusted_close"].ffill()
```

Backward fill:

```python
prices["adjusted_close"] = prices["adjusted_close"].bfill()
```

Fill with zero:

```python
df["volume"] = df["volume"].fillna(0)
```

### Finance caution

Forward filling prices can be acceptable in some contexts, but it can also hide stale prices.

If a price is missing because the asset did not trade, forward filling may understate risk.

### Athena recommendation

If you fill data, also create a warning flag.

Example:

```python
prices["price_was_missing"] = prices["adjusted_close"].isna()
prices["adjusted_close"] = prices["adjusted_close"].ffill()
```

---

## 32. Dropping missing values

Dropping missing values removes rows with missing data.

Example:

```python
clean_prices = prices.dropna(subset=["adjusted_close"])
```

Drop rows missing any value:

```python
clean = prices.dropna()
```

### When dropping is acceptable

Dropping can be acceptable when:

```text
Only a few rows are missing
Rows are not important
Missing data would break calculation
```

### When dropping is dangerous

Dropping is dangerous when it:

```text
Removes many observations
Creates biased results
Deletes important stress periods
Misaligns assets
```

### Athena rule

Log or report how many rows were dropped.

---

## 33. Duplicates

Duplicate rows can distort calculations.

Check duplicates:

```python
duplicates = prices.duplicated(subset=["symbol", "date"])
print(duplicates.sum())
```

Remove duplicates:

```python
prices = prices.drop_duplicates(subset=["symbol", "date"], keep="last")
```

### Why duplicates matter

Duplicates can create:

```text
Wrong returns
Wrong volume
Double-counted P&L
Incorrect charts
Bad joins
```

### Athena rule

Market data should have one row per symbol per date.

Validation check:

```python
assert not prices.duplicated(subset=["symbol", "date"]).any()
```

---

## 34. Outliers

Outliers are extreme values that may be real or erroneous.

Examples:

```text
Price jumps from 100 to 1000
Return = +900%
Volume = 0 for a liquid stock
Negative close price
```

Detect large returns:

```python
prices["return"] = prices["adjusted_close"].pct_change()
outliers = prices[prices["return"].abs() > 0.20]
```

### Important

Do not automatically delete outliers.

Some outliers are real market events.

### Athena workflow

```text
Detect outlier
Flag it
Investigate it
Decide whether to keep, adjust or exclude
Document decision
```

---

## 35. Data cleaning workflow

A clean data workflow is essential.

Recommended workflow:

```text
1. Load raw data
2. Parse dates
3. Standardize column names
4. Sort by symbol and date
5. Check missing values
6. Check duplicates
7. Check invalid values
8. Check outliers
9. Create warnings
10. Save cleaned data
```

Example code:

```python
import pandas as pd

prices = pd.read_csv("data/raw/prices.csv", parse_dates=["date"])

prices.columns = prices.columns.str.lower().str.replace(" ", "_")
prices = prices.sort_values(["symbol", "date"])
prices = prices.drop_duplicates(subset=["symbol", "date"], keep="last")

invalid_prices = prices[prices["adjusted_close"] <= 0]
missing_prices = prices[prices["adjusted_close"].isna()]

prices.to_parquet("data/processed/prices_clean.parquet", index=False)
```

### Athena rule

Clean data should be saved separately from raw data.

Never overwrite raw data.

---

## 36. Market price data with pandas

Market price data usually contains one row per asset per date.

Example:

```text
date        symbol  open  high  low  close  adjusted_close  volume
2026-04-27  AAPL    198   202   197  200    200             50000000
2026-04-28  AAPL    200   203   199  201    201             48000000
```

Load and prepare:

```python
import pandas as pd

prices = pd.read_csv("data/raw/prices.csv", parse_dates=["date"])
prices = prices.sort_values(["symbol", "date"])
```

### Typical Athena market data columns

```text
date
symbol
open
high
low
close
adjusted_close
volume
currency
source
```

### Important

Use `adjusted_close` for return calculations when available.

---

## 37. OHLCV data structure

OHLCV means:

```text
Open
High
Low
Close
Volume
```

Full common structure:

```text
Date
Open
High
Low
Close
Adjusted Close
Volume
```

### Meaning

```text
Open   = first traded price of the period
High   = highest traded price of the period
Low    = lowest traded price of the period
Close  = last traded price of the period
Volume = number of shares/contracts traded
```

### Athena use

OHLCV supports:

```text
Price charts
Return calculations
Volatility analysis
Liquidity analysis
Data quality checks
```

### Basic validation

```python
invalid = prices[
    (prices["high"] < prices["low"]) |
    (prices["close"] <= 0) |
    (prices["volume"] < 0)
]
```

---

## 38. Adjusted close

Adjusted close accounts for corporate actions such as:

```text
Dividends
Stock splits
Certain distributions
```

For return calculations, adjusted close is usually better than raw close.

Example:

```python
prices["return"] = prices.groupby("symbol")["adjusted_close"].pct_change()
```

### Why adjusted close matters

A stock split can make the raw price appear to fall sharply even though economic value did not change.

Example:

```text
Before split: 1 share at 200
After 2-for-1 split: 2 shares at 100
Economic value unchanged
```

Without adjusted close, returns may be wrong.

### Athena rule

Use adjusted close for historical returns when available.

---

## 39. Calculating simple returns

Simple return formula:

```text
Return_t = Price_t / Price_{t-1} - 1
```

pandas code for one asset:

```python
prices["simple_return"] = prices["adjusted_close"].pct_change()
```

For multiple assets:

```python
prices["simple_return"] = (
    prices
    .sort_values(["symbol", "date"])
    .groupby("symbol")["adjusted_close"]
    .pct_change()
)
```

### Example

```text
Yesterday price = 100
Today price = 105

Return = 105 / 100 - 1 = 5%
```

### Athena use

Simple returns are used for:

```text
Performance
Volatility
VaR
CVaR
Drawdown
Portfolio returns
```

---

## 40. Calculating log returns

Log return formula:

```text
Log return = ln(Price_t / Price_{t-1})
```

pandas and NumPy code:

```python
import numpy as np

prices["log_return"] = (
    prices
    .sort_values(["symbol", "date"])
    .groupby("symbol")["adjusted_close"]
    .transform(lambda s: np.log(s / s.shift(1)))
)
```

### Simple vs log returns

Simple returns are easier to interpret.

Log returns are useful because they are additive over time.

Example:

```text
Daily log returns can be summed to get multi-day log return.
```

### Athena recommendation

Use simple returns for user-facing performance.  
Use log returns where mathematically useful.

---

## 41. Rolling windows

A rolling window calculates metrics over a moving period.

Example:

```python
prices["rolling_20d_vol"] = (
    prices
    .groupby("symbol")["simple_return"]
    .transform(lambda s: s.rolling(window=20).std())
)
```

### Meaning

A 20-day rolling volatility uses the most recent 20 returns for each date.

Rolling windows are useful for:

```text
Rolling volatility
Rolling correlation
Moving averages
Rolling VaR
Rolling drawdown
```

### Athena use

Rolling metrics help show risk changing over time.

---

## 42. Rolling volatility

Rolling volatility measures how volatility changes through time.

Example:

```python
import numpy as np

prices["rolling_20d_vol"] = (
    prices
    .groupby("symbol")["simple_return"]
    .transform(lambda s: s.rolling(20).std() * np.sqrt(252))
)
```

This calculates annualized 20-day rolling volatility.

### Interpretation

```text
Higher rolling volatility = more unstable recent returns
Lower rolling volatility = more stable recent returns
```

### Athena chart

Possible chart:

```text
RollingVolatilityChart
```

---

## 43. Rolling correlation

Rolling correlation measures how correlation changes over time.

Example with two return series:

```python
rolling_corr = returns["AAPL"].rolling(60).corr(returns["MSFT"])
```

### Why it matters

Correlations can change during stress.

Assets that normally diversify may become highly correlated during crises.

### Athena use

Rolling correlation can support:

```text
Diversification analysis
Stress testing assumptions
RiskDNA risk drivers
```

### Caution

Rolling correlation needs enough data.

A 60-day window requires at least 60 observations.

---

## 44. Cumulative returns

Cumulative returns show growth over time.

Formula:

```text
Cumulative return = (1 + r1)(1 + r2)...(1 + rn) - 1
```

pandas code:

```python
prices["cumulative_return"] = (
    prices
    .groupby("symbol")["simple_return"]
    .transform(lambda s: (1 + s.fillna(0)).cumprod() - 1)
)
```

### Example

Returns:

```text
+10%, -5%
```

Cumulative return:

```text
(1.10 × 0.95) - 1 = 4.5%
```

### Athena use

Cumulative returns support:

```text
Performance charts
Benchmark comparison
Portfolio reporting
```

---

## 45. Drawdown calculation

Drawdown measures decline from a previous peak.

Steps:

```text
1. Calculate wealth index
2. Calculate rolling peak
3. Calculate drawdown
```

Code:

```python
returns = prices["simple_return"].fillna(0)

wealth = (1 + returns).cumprod()
peak = wealth.cummax()
drawdown = wealth / peak - 1
```

### Example

```text
Peak value = 120
Current value = 90

Drawdown = 90 / 120 - 1 = -25%
```

### Athena use

Drawdown is used in:

```text
Portfolio Management
Risk Management
P&L Reporting
RiskDNA
```

Possible chart:

```text
DrawdownChart
```

---

## 46. GroupBy operations

`groupby` allows calculations by category.

Example:

```python
prices.groupby("symbol")["simple_return"].mean()
```

Calculate volatility by symbol:

```python
vol_by_symbol = prices.groupby("symbol")["simple_return"].std() * np.sqrt(252)
```

Calculate market value by sector:

```python
sector_exposure = positions.groupby("sector")["market_value"].sum()
```

### Athena use

GroupBy is essential for:

```text
Returns by asset
P&L by asset
Exposure by sector
Exposure by currency
Risk by portfolio
```

### Beginner rule

If you have multiple assets, use `groupby("symbol")` before calculating asset-specific returns.

---

## 47. Aggregation

Aggregation summarizes data.

Common aggregations:

```python
.sum()
.mean()
.std()
.min()
.max()
.count()
```

Example:

```python
positions.groupby("sector").agg(
    market_value=("market_value", "sum"),
    number_of_positions=("symbol", "count"),
)
```

### Named aggregation

Named aggregation makes output clearer.

Example:

```python
summary = positions.groupby("sector").agg(
    total_value=("market_value", "sum"),
    average_weight=("weight", "mean"),
)
```

### Athena use

Aggregation supports dashboards and reports.

---

## 48. Pivot tables

Pivot tables reshape data into a matrix.

Example price data:

```text
date | symbol | adjusted_close
```

Create wide format:

```python
price_matrix = prices.pivot(
    index="date",
    columns="symbol",
    values="adjusted_close"
)
```

Now columns are symbols:

```text
date        AAPL   MSFT   NVDA
2026-04-27  200    420    900
```

### Why this is useful

Wide matrices are useful for:

```text
Correlation
Covariance
Portfolio return calculations
Vectorized risk calculations
```

### Athena use

Use pivot tables to build return matrices.

---

## 49. Merging datasets

Merging combines datasets.

Example:

```python
positions_with_prices = positions.merge(
    latest_prices,
    on="symbol",
    how="left"
)
```

### Join types

```text
left  = keep all rows from left table
inner = keep only matching rows
outer = keep all rows from both
```

### Athena example

Positions:

```text
symbol | quantity
```

Prices:

```text
symbol | price
```

Merged:

```text
symbol | quantity | price
```

Then calculate market value:

```python
positions_with_prices["market_value"] = (
    positions_with_prices["quantity"] * positions_with_prices["price"]
)
```

---

## 50. Joining market data with portfolio data

Athena often needs to combine market data with portfolio data.

Example:

```python
positions = pd.DataFrame({
    "symbol": ["AAPL", "MSFT"],
    "quantity": [10, 5],
})

prices = pd.DataFrame({
    "symbol": ["AAPL", "MSFT"],
    "price": [200, 420],
})

portfolio = positions.merge(prices, on="symbol", how="left")
portfolio["market_value"] = portfolio["quantity"] * portfolio["price"]
```

Output:

```text
AAPL market value = 10 × 200 = 2,000
MSFT market value = 5 × 420 = 2,100
```

### Athena use

This logic supports:

```text
Portfolio valuation
Weights
Exposure
P&L
Risk metrics
```

---

## 51. Exporting cleaned data

After cleaning data, export it.

CSV:

```python
prices.to_csv("data/processed/prices_clean.csv", index=False)
```

Parquet:

```python
prices.to_parquet("data/processed/prices_clean.parquet", index=False)
```

Excel:

```python
prices.to_excel("data/processed/prices_clean.xlsx", index=False)
```

### Recommendation

Use:

```text
CSV for simple readability
Parquet for larger processed datasets
Excel for manual review/reporting
```

### Athena rule

Keep raw and processed data separate.

Example:

```text
data/raw/
data/processed/
```

---

## 52. matplotlib overview

matplotlib is a Python library for creating charts.

Import convention:

```python
import matplotlib.pyplot as plt
```

Example:

```python
import matplotlib.pyplot as plt

plt.plot(prices["date"], prices["adjusted_close"])
plt.title("Adjusted Close Price")
plt.xlabel("Date")
plt.ylabel("Price")
plt.show()
```

### Why matplotlib matters

In Athena notebooks, matplotlib is useful for:

```text
Price charts
Return charts
Volatility charts
Loss distributions
Drawdowns
Yield curves
```

The production frontend may use Recharts or another JS library, but notebooks can use matplotlib.

---

## 53. Line charts

Line charts show time series.

Example:

```python
plt.plot(prices["date"], prices["adjusted_close"])
plt.title("AAPL Adjusted Close")
plt.xlabel("Date")
plt.ylabel("Price")
plt.show()
```

### Athena use

Line charts are useful for:

```text
Prices
Portfolio value
Cumulative returns
Rolling volatility
Drawdown
RiskDNA timeline
```

### Best practice

Use clear titles and axis labels.

Bad:

```text
Chart
```

Better:

```text
AAPL Adjusted Close Price Over Time
```

---

## 54. Histograms

Histograms show distributions.

Example:

```python
plt.hist(prices["simple_return"].dropna(), bins=50)
plt.title("Return Distribution")
plt.xlabel("Daily return")
plt.ylabel("Frequency")
plt.show()
```

### Athena use

Histograms are useful for:

```text
Return distributions
Loss distributions
VaR visualization
CVaR tail visualization
```

### Risk intuition

A histogram helps users see:

```text
Most common returns
Extreme losses
Fat tails
Skewness
```

---

## 55. Scatter plots

Scatter plots show relationships between two variables.

Example:

```python
plt.scatter(returns["AAPL"], returns["MSFT"])
plt.title("AAPL vs MSFT Daily Returns")
plt.xlabel("AAPL return")
plt.ylabel("MSFT return")
plt.show()
```

### Athena use

Scatter plots can help explore:

```text
Correlation
Beta
Benchmark relationship
Asset co-movement
```

### Example

If points slope upward, the two assets tend to move together.

---

## 56. Drawdown charts

Drawdown charts show portfolio declines from previous peaks.

Example:

```python
wealth = (1 + returns.fillna(0)).cumprod()
peak = wealth.cummax()
drawdown = wealth / peak - 1

plt.plot(drawdown.index, drawdown)
plt.title("Portfolio Drawdown")
plt.xlabel("Date")
plt.ylabel("Drawdown")
plt.show()
```

### Why drawdown charts matter

Drawdowns show the investor's experience of loss.

A portfolio can have good average returns but painful drawdowns.

### Athena use

Drawdown belongs in:

```text
Portfolio Management
Risk Management
P&L Reporting
```

---

## 57. Return distribution charts

A return distribution chart shows how returns are distributed.

Example:

```python
daily_returns = prices["simple_return"].dropna()

plt.hist(daily_returns, bins=50)
plt.title("Daily Return Distribution")
plt.xlabel("Daily return")
plt.ylabel("Frequency")
plt.show()
```

### Add VaR line

```python
var_95 = -daily_returns.quantile(0.05)

plt.hist(daily_returns, bins=50)
plt.axvline(daily_returns.quantile(0.05))
plt.title("Daily Returns with 5% Quantile")
plt.show()
```

### Athena use

This supports VaR/CVaR learning and visualization.

---

## 58. Yield curve charts

A yield curve chart plots yields by maturity.

Example:

```python
maturities = [1, 2, 5, 10, 30]
yields = [0.035, 0.037, 0.040, 0.042, 0.045]

plt.plot(maturities, yields, marker="o")
plt.title("Yield Curve")
plt.xlabel("Maturity in years")
plt.ylabel("Yield")
plt.show()
```

### Athena use

Yield curve charts support:

```text
Fixed Income
Rates Lab
Bond pricing
Rate shock visualization
```

### Note

In the frontend, yield curve charts can later be built with Recharts.

---

## 59. Plotting best practices

Good charts should be clear.

Best practices:

```text
Use clear titles
Label axes
Use appropriate units
Avoid overcrowding
Keep charts focused
Use date formatting for time series
Explain what the chart means
```

### Bad chart

```text
No title
No labels
Too many lines
Unclear units
```

### Good chart

```text
Title: 20-Day Rolling Annualized Volatility
X-axis: Date
Y-axis: Volatility
```

### Athena rule

A chart should answer a question.

Example:

```text
Question: Is portfolio volatility increasing?
Chart: Rolling volatility over time.
```

---

## 60. SciPy overview

SciPy is a scientific computing library built on NumPy.

Import examples:

```python
from scipy import stats
from scipy import optimize
from scipy import interpolate
```

SciPy provides tools for:

```text
Statistics
Distributions
Optimization
Root finding
Interpolation
Linear algebra
Numerical methods
```

### Why SciPy matters for Athena

SciPy is useful for:

```text
Normal distribution in Black-Scholes
Parametric VaR
Optimization
Yield curve interpolation
Solving yield to maturity
Finding roots
```

SciPy is the bridge between basic data analysis and more advanced quantitative methods.

---

## 61. SciPy stats module

The `scipy.stats` module provides statistical distributions and functions.

Import:

```python
from scipy import stats
```

Example normal distribution:

```python
from scipy import stats

z_95 = stats.norm.ppf(0.95)
print(z_95)
```

Output:

```text
Approximately 1.64485
```

### Athena use

Used for:

```text
Parametric VaR
Black-Scholes N(d1), N(d2)
Confidence levels
Distribution analysis
```

---

## 62. Normal distribution

The normal distribution is used in many financial models.

Example:

```python
from scipy import stats

probability = stats.norm.cdf(1.0)
z_value = stats.norm.ppf(0.95)
```

Where:

```text
cdf = cumulative distribution function
ppf = inverse cumulative distribution function
```

### Black-Scholes use

Black-Scholes uses:

```text
N(d1)
N(d2)
```

In Python:

```python
stats.norm.cdf(d1)
stats.norm.cdf(d2)
```

### Risk caution

Financial returns are not always normal.

Normal models can underestimate tail risk.

---

## 63. Percentiles and quantiles

Percentiles and quantiles are used for historical VaR.

With NumPy:

```python
var_threshold = np.quantile(losses, 0.95)
```

With pandas:

```python
var_threshold = losses.quantile(0.95)
```

### Example

```python
import pandas as pd

losses = pd.Series([100, 200, 300, 500, 1000])
var_95 = losses.quantile(0.95)

print(var_95)
```

### Athena use

Quantiles are used for:

```text
Historical VaR
Loss distribution analysis
Tail risk
Outlier detection
```

---

## 64. Optimization basics

Optimization means finding the best value according to an objective.

Examples:

```text
Minimize portfolio volatility
Maximize Sharpe ratio
Find yield to maturity
Fit curve parameters
```

SciPy optimization:

```python
from scipy import optimize
```

Example:

```python
from scipy import optimize

def objective(x):
    return (x - 3) ** 2

result = optimize.minimize(objective, x0=0)
print(result.x)
```

Output is close to:

```text
3
```

### Athena use

Optimization is useful for portfolio optimization and numerical solving.

---

## 65. Root finding

Root finding solves equations of the form:

```text
f(x) = 0
```

Example:

```python
from scipy import optimize

def f(x):
    return x**2 - 4

root = optimize.brentq(f, 0, 3)
print(root)
```

Output:

```text
2
```

### Finance use

Root finding can solve:

```text
Yield to maturity
Implied volatility
Break-even rate
Equation-based calibration
```

### Athena use

Examples:

```text
Solve YTM from bond price
Solve implied volatility from market option price
```

---

## 66. Interpolation basics

Interpolation estimates values between known points.

Example yield curve:

```text
1Y = 3.5%
2Y = 3.7%
5Y = 4.0%
```

What is the 3-year rate?

Interpolation can estimate it.

Python example:

```python
from scipy.interpolate import interp1d

maturities = [1, 2, 5, 10]
rates = [0.035, 0.037, 0.040, 0.042]

curve = interp1d(maturities, rates, kind="linear")
rate_3y = float(curve(3))

print(rate_3y)
```

### Athena use

Interpolation supports:

```text
Yield curves
Discount factors
Stress curves
Missing curve points
```

---

## 67. SciPy for VaR and CVaR

SciPy can support parametric VaR.

Example:

```python
from scipy import stats

portfolio_value = 100_000
daily_volatility = 0.015
confidence_level = 0.95

z = stats.norm.ppf(confidence_level)
var_amount = z * daily_volatility * portfolio_value

print(var_amount)
```

### Historical CVaR with pandas

```python
losses = -returns * portfolio_value
var_95 = losses.quantile(0.95)
cvar_95 = losses[losses >= var_95].mean()
```

### Athena use

Use SciPy for distribution functions and pandas for historical loss calculations.

---

## 68. SciPy for Black-Scholes

Black-Scholes uses the normal cumulative distribution function.

Example:

```python
import numpy as np
from scipy import stats

S = 100
K = 100
T = 1
r = 0.05
sigma = 0.20
q = 0.0

d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

call = S * np.exp(-q * T) * stats.norm.cdf(d1) - K * np.exp(-r * T) * stats.norm.cdf(d2)

print(call)
```

This should be close to:

```text
10.45
```

### Athena use

The Options Pricing Lab can use SciPy for `N(d1)` and `N(d2)`.

---

## 69. SciPy for yield curves

SciPy can support yield curve interpolation.

Example:

```python
from scipy.interpolate import interp1d

maturities = [1, 2, 5, 10, 30]
rates = [0.035, 0.037, 0.040, 0.042, 0.045]

curve = interp1d(maturities, rates, kind="linear", fill_value="extrapolate")
rate_7y = float(curve(7))

print(rate_7y)
```

### Use cases

```text
Estimate missing curve points
Build discount factor curve
Interpolate spot rates
Stress curve points
```

### Caution

Interpolation method matters.

Linear interpolation is simple but not always the most accurate for professional fixed income.

Start simple, document assumptions.

---

## 70. Python data validation

Data validation checks whether inputs are acceptable before calculations.

Examples:

```text
Price must be positive
Volume cannot be negative
Date cannot be missing
Quantity cannot be null
Portfolio weights should sum to 1
Volatility must be positive
Confidence level must be between 0 and 1
```

Simple validation:

```python
if (prices["adjusted_close"] <= 0).any():
    raise ValueError("Adjusted close must be positive.")
```

### Athena rule

Validate before calculating.

Bad inputs produce bad outputs.

---

## 71. Type hints

Type hints make Python code clearer.

Example:

```python
def calculate_return(beginning_price: float, ending_price: float) -> float:
    return ending_price / beginning_price - 1
```

### Why type hints matter

They improve:

```text
Readability
Maintainability
Editor support
Static checking
Team collaboration
```

### Athena use

Backend services should use type hints.

Example:

```python
def annualized_volatility(returns: pd.Series, periods_per_year: int = 252) -> float:
    return float(returns.std(ddof=1) * np.sqrt(periods_per_year))
```

---

## 72. Dataclasses

Dataclasses help define simple structured data.

Example:

```python
from dataclasses import dataclass

@dataclass
class BondInput:
    face_value: float
    coupon_rate: float
    yield_to_maturity: float
    maturity_years: int
```

Use:

```python
bond = BondInput(
    face_value=1000,
    coupon_rate=0.05,
    yield_to_maturity=0.04,
    maturity_years=3,
)
```

### Athena use

Dataclasses can be useful in notebooks and internal services.

For API input validation, Pydantic is usually better.

---

## 73. Pydantic preview

Pydantic validates data using Python type hints.

Example:

```python
from pydantic import BaseModel, Field

class VaRRequest(BaseModel):
    confidence_level: float = Field(gt=0, lt=1)
    portfolio_value: float = Field(gt=0)
```

Use:

```python
request = VaRRequest(confidence_level=0.95, portfolio_value=100000)
```

Invalid values raise validation errors.

### Athena use

Pydantic is essential for FastAPI request and response models.

This file only previews Pydantic.  
The backend stack document should cover it in detail.

---

## 74. Data quality checks

Data quality checks protect analytics.

Example checks:

```text
No missing prices
No duplicate symbol-date rows
No negative prices
No negative volume
Dates are sorted
Returns are not extreme without warning
Currency is defined
FX rate exists when needed
```

Example code:

```python
def validate_price_data(prices: pd.DataFrame) -> list[str]:
    warnings = []

    if prices["adjusted_close"].isna().any():
        warnings.append("Missing adjusted close values detected.")

    if (prices["adjusted_close"] <= 0).any():
        warnings.append("Non-positive adjusted close values detected.")

    if prices.duplicated(subset=["symbol", "date"]).any():
        warnings.append("Duplicate symbol-date rows detected.")

    return warnings
```

### Athena use

Data quality warnings should appear in dashboards and reports.

---

## 75. Reproducible notebooks

A reproducible notebook can be rerun and produce the same results.

Best practices:

```text
Use fixed random seeds
Keep data paths relative
Run cells from top to bottom
Avoid hidden manual state
Document assumptions
Save output datasets
Use clear section headings
```

### Good notebook structure

```text
1. Objective
2. Imports
3. Configuration
4. Load data
5. Validate data
6. Clean data
7. Calculate metrics
8. Visualize
9. Conclusion
10. Next step to backend
```

### Athena rule

Every notebook should explain what it proves or explores.

---

## 76. From notebook to backend service

Moving from notebook to backend means turning exploratory code into clean reusable functions.

Notebook code:

```python
returns = prices["adjusted_close"].pct_change()
vol = returns.std() * np.sqrt(252)
```

Backend function:

```python
def calculate_annualized_volatility(
    prices: pd.Series,
    periods_per_year: int = 252,
) -> float:
    returns = prices.pct_change().dropna()
    return float(returns.std(ddof=1) * np.sqrt(periods_per_year))
```

### Steps

```text
1. Identify stable calculation
2. Create pure function
3. Add type hints
4. Validate inputs
5. Add unit tests
6. Use in service
7. Expose through API if needed
```

### Athena principle

Notebooks teach and prototype.  
Backend services productionize.

---

## 77. Folder structure for notebooks

Recommended Athena notebook structure:

```text
notebooks/
├── README.md
├── 01_market_data_returns.ipynb
├── 02_yield_curve_bond_pricing.ipynb
├── 03_portfolio_analytics.ipynb
├── 04_var_cvar_stress_testing.ipynb
├── 05_black_scholes_greeks.ipynb
├── 06_riskdna_scoring_demo.ipynb
└── 08_pnl_attribution_demo.ipynb
```

### Notebook naming rules

Use:

```text
number_topic.ipynb
```

Examples:

```text
01_market_data_returns.ipynb
04_var_cvar_stress_testing.ipynb
```

### Athena recommendation

Keep notebooks clean enough that someone can open them and understand the project.

---

## 78. Common Athena datasets

Athena may use several dataset types.

### Market prices

```text
date
symbol
open
high
low
close
adjusted_close
volume
currency
```

### Portfolio positions

```text
portfolio_id
symbol
quantity
average_price
currency
sector
country
```

### Trades

```text
trade_id
portfolio_id
symbol
side
quantity
price
fees
trade_date
currency
```

### Risk metrics

```text
portfolio_id
valuation_date
var
cvar
volatility
stress_loss
riskdna_score
```

### P&L records

```text
portfolio_id
valuation_date
beginning_value
ending_value
daily_pnl
daily_return
currency
```

### Yield curve

```text
curve_date
maturity_years
rate
curve_name
currency
```

---

## 79. Suggested notebook exercises

Suggested exercises for learning:

### Exercise 1 — Load prices

```text
Load a CSV file with OHLCV data.
Parse dates.
Sort by date.
Validate adjusted_close.
```

### Exercise 2 — Calculate returns

```text
Calculate simple returns.
Calculate log returns.
Compare them.
```

### Exercise 3 — Volatility

```text
Calculate daily volatility.
Calculate annualized volatility.
Plot rolling volatility.
```

### Exercise 4 — VaR and CVaR

```text
Build loss distribution.
Calculate 95% historical VaR.
Calculate 95% historical CVaR.
Plot losses and VaR threshold.
```

### Exercise 5 — Portfolio weights

```text
Join positions with prices.
Calculate market values.
Calculate portfolio weights.
```

### Exercise 6 — P&L

```text
Calculate position-level P&L.
Calculate portfolio-level P&L.
Rank top and worst contributors.
```

---

## 80. Suggested backend functions

Functions to eventually create in Athena backend:

```python
def calculate_simple_returns(prices: pd.Series) -> pd.Series:
    ...

def calculate_log_returns(prices: pd.Series) -> pd.Series:
    ...

def annualized_volatility(returns: pd.Series, periods_per_year: int = 252) -> float:
    ...

def calculate_drawdown(returns: pd.Series) -> pd.Series:
    ...

def historical_var(losses: pd.Series, confidence_level: float) -> float:
    ...

def historical_cvar(losses: pd.Series, confidence_level: float) -> float:
    ...

def validate_price_data(prices: pd.DataFrame) -> list[str]:
    ...

def calculate_position_market_values(positions: pd.DataFrame, prices: pd.DataFrame) -> pd.DataFrame:
    ...
```

### Function design principles

```text
Keep functions small
Use clear names
Validate inputs
Return predictable outputs
Avoid hidden global variables
Write tests
```

---

## 81. Suggested tests

Suggested tests for the Python data stack.

### Return tests

```text
Simple return is calculated correctly.
Log return is calculated correctly.
Returns handle missing first value.
Prices must be positive.
```

### Volatility tests

```text
Annualized volatility equals daily volatility times sqrt(252).
Volatility is non-negative.
Empty returns are rejected.
```

### Data quality tests

```text
Missing prices generate warning.
Negative prices generate warning or error.
Duplicate symbol-date rows are detected.
Dates are parsed correctly.
```

### Portfolio tests

```text
Market value equals quantity times price.
Weights sum to 1.
Missing price creates warning.
```

### VaR/CVaR tests

```text
Historical VaR returns expected quantile.
CVaR is greater than or equal to VaR when losses are positive.
```

---

## 82. Common beginner mistakes

### Mistake 1 — Not sorting dates before returns

Returns require chronological order.

### Mistake 2 — Using close instead of adjusted close

Adjusted close is usually better for historical returns.

### Mistake 3 — Ignoring missing values

Missing values can break calculations or hide risk.

### Mistake 4 — Dropping rows without checking impact

Dropping data can remove important market events.

### Mistake 5 — Confusing daily and annualized volatility

Daily volatility is not annual volatility.

### Mistake 6 — Forgetting currency

Portfolio values need consistent currency.

### Mistake 7 — Trusting charts without checking data

Charts can look good even with bad data.

### Mistake 8 — Keeping important logic only in notebooks

Stable logic should move to backend services.

### Mistake 9 — Not writing tests

Financial calculations need tests.

### Mistake 10 — Mixing raw and processed data

Keep raw data unchanged.

---

## 83. Key formulas implemented with Python

### Simple return

```python
returns = prices.pct_change()
```

### Log return

```python
log_returns = np.log(prices / prices.shift(1))
```

### Annualized volatility

```python
annualized_vol = returns.std(ddof=1) * np.sqrt(252)
```

### Cumulative return

```python
cumulative_return = (1 + returns.fillna(0)).cumprod() - 1
```

### Drawdown

```python
wealth = (1 + returns.fillna(0)).cumprod()
peak = wealth.cummax()
drawdown = wealth / peak - 1
```

### Historical VaR

```python
losses = -returns * portfolio_value
var_95 = losses.quantile(0.95)
```

### Historical CVaR

```python
cvar_95 = losses[losses >= var_95].mean()
```

### Position market value

```python
positions["market_value"] = positions["quantity"] * positions["price"]
```

### Portfolio weights

```python
positions["weight"] = positions["market_value"] / positions["market_value"].sum()
```

---

## 84. How Athena uses the Python data stack

Athena uses the Python data stack as the foundation of its quantitative logic.

### In notebooks

Used to:

```text
Explore data
Learn formulas
Visualize results
Prototype risk calculations
Test ideas quickly
```

### In backend

Used to:

```text
Calculate metrics
Validate data
Run risk models
Generate P&L attribution
Power API responses
```

### In reports

Used to:

```text
Prepare tables
Generate metrics
Validate calculations
Support charts
```

### Complete Athena flow

```text
Raw market data
      ↓
pandas cleaning
      ↓
NumPy calculations
      ↓
SciPy statistical/numerical methods
      ↓
matplotlib notebook visualization
      ↓
backend service functions
      ↓
FastAPI endpoints
      ↓
frontend dashboards
```

The Python data stack is not optional. It is the quantitative foundation of Athena.

---

## 85. Summary

The Python data stack is the base layer for Athena's quantitative work.

Core tools:

```text
NumPy      = numerical calculations
pandas     = data manipulation and time series
matplotlib = notebook visualization
SciPy      = statistics, optimization and numerical methods
Jupyter    = exploration and learning
```

Main Athena uses:

```text
Market data cleaning
Return calculations
Volatility analysis
Correlation analysis
VaR and CVaR
Stress testing
Portfolio valuation
P&L attribution
Black-Scholes inputs
RiskDNA inputs
Reporting
```

The most important workflow is:

```text
Learn in docs.
Prototype in notebooks.
Clean logic into backend services.
Test the functions.
Expose through APIs.
Display in frontend.
```

The key lesson:

```text
Good finance analytics require clean data, reproducible calculations and tested Python code.
```

This file is the technical foundation for the rest of Athena's quantitative development.
