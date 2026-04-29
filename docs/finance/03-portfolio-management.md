# 03 — Portfolio Management

**Project:** Athena AI Risk Terminal  
**Recommended file path:** `docs/finance/03-portfolio-management.md`  
**Purpose:** build a strong foundation in portfolio management, portfolio construction, risk-return analysis, diversification, benchmarks, performance ratios, rebalancing, optimization and portfolio monitoring before implementing the Portfolio Builder and Performance Analytics modules in Athena.  
**Scope:** this document focuses only on portfolio management. Market data, fixed income, risk management, front-office workflows, RiskDNA and P&L attribution are documented separately.

---

## Table of Contents

1. What is portfolio management?
2. Why portfolio management matters
3. Portfolio vs individual asset
4. Investment objectives
5. Risk tolerance
6. Investment constraints
7. Investment policy statement
8. Strategic asset allocation
9. Tactical asset allocation
10. Asset allocation vs security selection
11. Portfolio holdings
12. Positions
13. Market value
14. Portfolio weights
15. Long positions
16. Short positions
17. Cash position
18. Portfolio return
19. Weighted average return
20. Portfolio volatility
21. Diversification
22. Correlation and diversification
23. Systematic risk
24. Unsystematic risk
25. Beta
26. Alpha
27. Benchmark selection
28. Active vs passive management
29. Tracking error
30. Information ratio
31. Sharpe ratio
32. Sortino ratio
33. Treynor ratio
34. Maximum drawdown
35. Rebalancing
36. Rebalancing frequency
37. Threshold-based rebalancing
38. Transaction costs
39. Turnover
40. Concentration risk
41. Sector exposure
42. Geographic exposure
43. Currency exposure
44. Factor exposure
45. Style exposure
46. Growth vs value
47. Large cap vs small cap
48. Defensive vs cyclical sectors
49. Portfolio constraints
50. Long-only portfolios
51. Leverage
52. Margin
53. Portfolio optimization
54. Mean-variance optimization
55. Efficient frontier
56. Minimum variance portfolio
57. Maximum Sharpe portfolio
58. Target return portfolio
59. Target volatility portfolio
60. Risk parity
61. Equal-weight portfolio
62. Capital allocation line
63. Capital market line
64. Capital asset pricing model
65. Expected return
66. Risk-free rate
67. Market risk premium
68. Portfolio performance attribution
69. Asset allocation effect
70. Security selection effect
71. Interaction effect
72. Benchmark-relative performance
73. Portfolio monitoring
74. Portfolio drift
75. Portfolio reporting
76. Data required for portfolio management
77. Common beginner mistakes
78. Key formulas
79. Possible API endpoints
80. Possible frontend components
81. Suggested tests
82. How Athena uses portfolio management
83. Summary

---

## 1. What is portfolio management?

Portfolio management is the process of selecting, combining, monitoring and adjusting investments to meet specific objectives.

A portfolio is not just a list of assets. It is a structured combination of holdings designed to achieve a goal.

A portfolio manager must decide:

- what assets to hold;
- how much capital to allocate to each asset;
- how much risk to accept;
- what benchmark to compare against;
- when to rebalance;
- how to monitor performance;
- how to control exposures.

Simple intuition:

```text
Asset analysis = understanding one investment
Portfolio management = understanding how investments work together
```

In Athena AI Risk Terminal, portfolio management supports the **Portfolio Builder**, **Performance Analytics**, **Trade Simulator**, and later the **Risk Monitor**.

---

## 2. Why portfolio management matters

Portfolio management matters because investment decisions are not made in isolation.

Owning one asset is different from owning a group of assets.

A good portfolio can:

- diversify risk;
- improve risk-adjusted return;
- control concentration;
- align investments with objectives;
- monitor exposures;
- support decision-making;
- compare performance against a benchmark.

### Example

Suppose an investor owns only one technology stock.

```text
Portfolio:
100% NVDA
```

This portfolio may perform well, but it is highly concentrated.

A more diversified portfolio may include:

```text
40% US equity ETF
20% Canadian equity ETF
20% bonds
10% cash
10% international equity ETF
```

The second portfolio may have lower concentration risk.

### Athena link

Athena should not only show positions. It should help answer:

```text
What does this portfolio own?
How much is allocated to each asset?
How risky is the allocation?
How does it compare with a benchmark?
What changed after a proposed trade?
```

---

## 3. Portfolio vs individual asset

An individual asset is one investment.

Examples:

```text
AAPL stock
SPY ETF
Government bond
Gold ETF
Cash
```

A portfolio is a collection of assets.

Example:

```text
Portfolio:
- 30% SPY
- 20% QQQ
- 20% AAPL
- 20% bonds
- 10% cash
```

### Key difference

An asset has its own return and risk.

A portfolio has return and risk that depend on:

- asset weights;
- asset returns;
- asset volatilities;
- correlations between assets.

Two assets can be risky individually, but if they do not move together, combining them can reduce portfolio risk.

This is the central idea of diversification.

---

## 4. Investment objectives

Investment objectives define what the portfolio is trying to achieve.

Common objectives:

```text
Capital preservation
Income generation
Capital growth
Balanced growth and income
Inflation protection
Liability matching
Liquidity reserve
```

### Examples

A young investor may prioritize growth.

```text
Objective: long-term capital appreciation
```

A retired investor may prioritize income and capital preservation.

```text
Objective: stable income with moderate risk
```

A pension fund may prioritize liability matching.

```text
Objective: meet future pension payments
```

### Athena link

Athena can later allow the user to define a portfolio objective.

Example field:

```text
objective = "Growth"
objective = "Income"
objective = "Balanced"
```

This can influence constraints, reporting and portfolio analytics.

---

## 5. Risk tolerance

Risk tolerance describes how much risk an investor is willing and able to accept.

It has two dimensions:

```text
Willingness to take risk
Ability to take risk
```

### Willingness

Willingness is psychological.

Example:

```text
The investor becomes uncomfortable when the portfolio falls by 5%.
```

### Ability

Ability is financial.

Example:

```text
The investor has a long time horizon and stable income, so they can tolerate more volatility.
```

### Conservative, moderate and aggressive

A simplified classification:

```text
Conservative = low risk tolerance
Moderate = balanced risk tolerance
Aggressive = high risk tolerance
```

### Athena link

Athena can later classify portfolio risk compared to a target risk profile.

Example:

```text
Risk profile: Moderate
Current annualized volatility: 28%
Warning: portfolio risk may be above target profile
```

---

## 6. Investment constraints

Investment constraints define what the portfolio can or cannot do.

Common constraints:

```text
Liquidity needs
Time horizon
Tax considerations
Legal and regulatory constraints
Unique circumstances
Risk limits
Asset class restrictions
Currency restrictions
Maximum position size
Maximum sector exposure
```

### Example constraints

```text
Maximum single asset weight = 10%
Maximum technology exposure = 35%
Minimum cash weight = 5%
Long-only portfolio
No leverage
```

### Why constraints matter

A portfolio can be theoretically optimal but practically unacceptable if it violates constraints.

Example:

```text
An optimizer suggests 80% in one stock.
```

This may be mathematically attractive but unacceptable from a risk control perspective.

### Athena link

Constraints are essential for the future Portfolio Optimizer and Limit Center.

---

## 7. Investment policy statement

An Investment Policy Statement, or IPS, defines the rules and objectives for managing a portfolio.

It usually includes:

- investment objectives;
- risk tolerance;
- constraints;
- benchmark;
- eligible assets;
- rebalancing rules;
- reporting frequency;
- roles and responsibilities.

### Simple example

```text
Objective: long-term growth
Risk tolerance: moderate
Benchmark: 60% equity / 40% bond index
Maximum single position: 10%
Maximum sector exposure: 35%
Minimum cash: 3%
Rebalancing: quarterly or when weights drift by more than 5%
```

### Why it matters

The IPS creates discipline.

Without an IPS, investment decisions can become emotional or inconsistent.

### Athena link

Athena can later include a simplified IPS configuration page.

---

## 8. Strategic asset allocation

Strategic asset allocation is the long-term target allocation of a portfolio.

Example:

```text
60% equities
30% bonds
10% cash
```

It reflects long-term objectives and risk tolerance.

### Why it matters

Strategic allocation is usually the biggest driver of long-term portfolio behavior.

Security selection matters, but the broad allocation to asset classes is often more important.

### Example

A conservative investor may choose:

```text
30% equities
60% bonds
10% cash
```

An aggressive investor may choose:

```text
85% equities
10% bonds
5% cash
```

### Athena link

Athena can store target weights and compare current weights against strategic allocation.

---

## 9. Tactical asset allocation

Tactical asset allocation is a short-term adjustment around the strategic allocation.

Example:

Strategic allocation:

```text
60% equities
30% bonds
10% cash
```

Tactical view:

```text
65% equities
25% bonds
10% cash
```

The investor temporarily increases equity exposure because they expect stronger equity performance.

### Strategic vs tactical

```text
Strategic allocation = long-term policy
Tactical allocation = short-term adjustment
```

### Risk

Tactical allocation can improve performance if correct, but it can also increase risk and turnover.

### Athena link

The Trade Simulator can show how a tactical trade changes allocation relative to target weights.

---

## 10. Asset allocation vs security selection

Asset allocation decides how much capital goes into broad categories.

Security selection decides which specific assets to buy inside those categories.

### Asset allocation example

```text
60% equities
30% bonds
10% cash
```

### Security selection example

Within equities:

```text
AAPL
MSFT
NVDA
SPY
QQQ
```

### Why the distinction matters

A portfolio can outperform because of:

- good asset allocation;
- good security selection;
- both;
- luck.

Performance attribution tries to separate these effects.

### Athena link

Athena can later distinguish between:

```text
allocation decisions
security selection decisions
```

This becomes useful for reporting.

---

## 11. Portfolio holdings

Holdings are the assets owned by a portfolio.

Example:

```text
AAPL
MSFT
SPY
BND
Cash
```

A holding record should usually include:

```text
asset symbol
quantity
current price
market value
weight
currency
sector
country
```

### Athena data idea

A holding can be displayed in a position table.

Example:

```text
Symbol | Quantity | Price | Market Value | Weight | Sector
AAPL   | 20       | 200   | 4,000        | 20%    | Technology
```

Holdings are the raw material for portfolio analysis.

---

## 12. Positions

A position is the amount of an asset held by the portfolio.

A position can be measured by:

- quantity;
- market value;
- portfolio weight;
- exposure.

Example:

```text
Quantity = 50 shares
Current price = 100
Market value = 5,000
```

### Position value

Formula:

```text
Position market value = Quantity × Current price
```

Example:

```text
Quantity = 50
Price = 100

Market value = 5,000
```

### Athena link

The Portfolio Builder should allow users to add, edit and remove positions.

---

## 13. Market value

Market value is the current value of a position or portfolio.

For a position:

```text
Market value = Quantity × Current price
```

For a portfolio:

```text
Portfolio market value = Sum of all position market values + cash
```

### Example

```text
AAPL market value = 4,000
MSFT market value = 3,000
Cash = 1,000

Portfolio value = 8,000
```

### Why market value matters

Market value is used to calculate:

- weights;
- exposures;
- performance;
- risk metrics;
- portfolio changes after trades.

Athena should always recalculate market value when prices or positions change.

---

## 14. Portfolio weights

A portfolio weight is the percentage of the portfolio invested in a position.

Formula:

```text
Weight_i = Position market value_i / Total portfolio value
```

Example:

```text
AAPL market value = 4,000
Portfolio value = 10,000

AAPL weight = 4,000 / 10,000
AAPL weight = 40%
```

### Weight sum

For a fully invested long-only portfolio:

```text
Sum of weights = 100%
```

If cash is included, cash also has a weight.

### Athena test

A basic test should verify:

```text
All position weights + cash weight = 100%
```

---

## 15. Long positions

A long position means the investor owns the asset and benefits if the price rises.

Example:

```text
Buy 100 shares of AAPL
```

If the price increases, the position gains value.

### Long position payoff intuition

```text
Price up → gain
Price down → loss
```

Long-only portfolios only hold long positions and cash.

### Athena first version

Athena should start with long-only portfolios because they are simpler and safer to model.

---

## 16. Short positions

A short position means the investor sells an asset they do not own, expecting the price to fall.

If the price falls, the short position gains.  
If the price rises, the short position loses.

### Example

```text
Short 100 shares at 50
Price falls to 40
Gain = 10 per share
```

### Risk

Short positions can have theoretically unlimited losses because the asset price can rise significantly.

### Athena note

Short positions are advanced. The first version can ignore shorts or support them later with strict validation.

---

## 17. Cash position

Cash is part of a portfolio.

It can be held for:

- liquidity;
- future investment;
- risk reduction;
- transaction needs;
- reserve allocation.

### Cash weight

Formula:

```text
Cash weight = Cash / Total portfolio value
```

Example:

```text
Cash = 1,000
Portfolio value = 10,000

Cash weight = 10%
```

### Why cash matters

A portfolio with 20% cash is not equivalent to a fully invested portfolio.

Cash reduces market exposure and can reduce volatility.

Athena should treat cash as a position or as a separate portfolio component.

---

## 18. Portfolio return

Portfolio return is the return generated by the full portfolio.

If no cash flows are added or removed during the period, a simple portfolio return can be calculated as:

```text
Portfolio return = Ending portfolio value / Beginning portfolio value - 1
```

Example:

```text
Beginning value = 100,000
Ending value = 103,000

Portfolio return = 103,000 / 100,000 - 1
Portfolio return = 3%
```

### With external cash flows

If the investor adds or withdraws money, return calculation becomes more complex.

Possible methods include:

```text
Time-weighted return
Money-weighted return
```

Athena can start with simple return calculations and later support more advanced return methods.

---

## 19. Weighted average return

If asset returns and portfolio weights are known, portfolio return can be calculated as a weighted average.

Formula:

```text
Portfolio return = w1R1 + w2R2 + ... + wnRn
```

Where:

```text
w_i = weight of asset i
R_i = return of asset i
```

### Example

```text
Asset A weight = 60%
Asset A return = 10%

Asset B weight = 40%
Asset B return = 2%

Portfolio return = 0.60 × 10% + 0.40 × 2%
Portfolio return = 6% + 0.8%
Portfolio return = 6.8%
```

### Important

Weights must correspond to the beginning of the return period for clean attribution.

---

## 20. Portfolio volatility

Portfolio volatility measures the variability of portfolio returns.

It depends on:

- asset weights;
- asset volatilities;
- correlations or covariances.

For a two-asset portfolio:

```text
Portfolio variance =
w1²σ1² + w2²σ2² + 2w1w2σ1σ2ρ12
```

Where:

```text
w1, w2 = weights
σ1, σ2 = asset volatilities
ρ12 = correlation between assets
```

### Key lesson

Portfolio volatility is not just the weighted average of individual volatilities.

Correlation matters.

If assets do not move together, diversification can reduce volatility.

---

## 21. Diversification

Diversification means spreading investments across different assets to reduce risk.

Simple intuition:

```text
Do not put all your eggs in one basket.
```

Diversification can be across:

- assets;
- sectors;
- countries;
- currencies;
- asset classes;
- factors;
- maturities.

### Good diversification

A diversified portfolio holds assets that do not all move in the same direction at the same time.

### Bad diversification

Owning many assets from the same sector may not provide strong diversification.

Example:

```text
AAPL
MSFT
NVDA
AMD
```

Many tickers, but similar technology exposure.

---

## 22. Correlation and diversification

Correlation measures how assets move together.

```text
+1 = move perfectly together
 0 = no clear linear relationship
-1 = move perfectly opposite
```

### Why correlation matters

The lower the correlation between assets, the greater the potential diversification benefit.

Example:

```text
Two assets with correlation 0.20 may diversify better than two assets with correlation 0.95.
```

### Diversification is not guaranteed

Correlations can increase during market stress.

This means assets that appear diversified in calm periods may fall together during crises.

### Athena link

Athena can display a correlation matrix to help users understand portfolio diversification.

---

## 23. Systematic risk

Systematic risk is market-wide risk that cannot be fully diversified away.

Examples:

- recessions;
- interest rate shocks;
- inflation shocks;
- geopolitical crises;
- broad market crashes.

### Market risk

Systematic risk is often called market risk.

Even a well-diversified portfolio is exposed to systematic risk.

### Beta link

Beta measures sensitivity to market risk.

Athena can later estimate portfolio beta relative to a benchmark.

---

## 24. Unsystematic risk

Unsystematic risk is asset-specific or company-specific risk.

Examples:

- company earnings disappointment;
- product failure;
- management scandal;
- sector-specific event;
- legal issue.

### Diversification effect

Unsystematic risk can be reduced through diversification.

Example:

If one company has bad news, a diversified portfolio may be less affected than a portfolio concentrated in that company.

### Key distinction

```text
Systematic risk = market-wide, hard to diversify away
Unsystematic risk = asset-specific, can be reduced by diversification
```

---

## 25. Beta

Beta measures how sensitive an asset or portfolio is to market movements.

Formula idea:

```text
Beta = Covariance(asset return, market return) / Variance(market return)
```

### Interpretation

```text
Beta = 1.0  → moves like the market
Beta > 1.0  → more sensitive than the market
Beta < 1.0  → less sensitive than the market
Beta < 0    → tends to move opposite the market
```

### Example

```text
Portfolio beta = 1.2
Market return = +10%

Expected portfolio movement ≈ +12%
```

If the market falls by 10%, the portfolio may fall by about 12%, under a simplified beta interpretation.

### Athena link

Beta can be included in Performance Analytics.

---

## 26. Alpha

Alpha measures performance beyond what would be expected based on market exposure.

Simplified idea:

```text
Alpha = Portfolio return - Expected return based on beta
```

A positive alpha means the portfolio outperformed after accounting for market risk.

A negative alpha means it underperformed.

### Example

```text
Expected return based on beta = 8%
Portfolio return = 10%

Alpha = 2%
```

### Important

Alpha depends heavily on the chosen benchmark and model assumptions.

A wrong benchmark can produce misleading alpha.

---

## 27. Benchmark selection

A benchmark is a reference used to evaluate portfolio performance.

Examples:

```text
S&P 500
Nasdaq-100
TSX Composite
60/40 equity-bond benchmark
Custom benchmark
```

### Good benchmark characteristics

A good benchmark should be:

- relevant;
- investable or representative;
- transparent;
- measurable;
- appropriate for the portfolio strategy;
- specified in advance.

### Example

A US large-cap equity portfolio can be compared to the S&P 500.

A global multi-asset portfolio should not be compared only to the Nasdaq-100.

### Athena link

Each portfolio should have a benchmark field.

Example:

```text
benchmark_symbol = "SPY"
```

---

## 28. Active vs passive management

### Passive management

Passive management tries to track a benchmark.

Example:

```text
Buy an ETF tracking the S&P 500.
```

Goal:

```text
Match benchmark performance before fees.
```

### Active management

Active management tries to outperform a benchmark.

Active managers use:

- security selection;
- tactical allocation;
- factor tilts;
- macro views;
- risk management.

### Key comparison

```text
Passive = track the benchmark
Active = try to beat the benchmark
```

### Risk

Active management can underperform.

Performance must be evaluated relative to benchmark risk.

---

## 29. Tracking error

Tracking error measures how much portfolio returns differ from benchmark returns.

Formula idea:

```text
Tracking error = standard deviation of active returns
```

Where:

```text
Active return = Portfolio return - Benchmark return
```

### Example

```text
Portfolio return = 1.2%
Benchmark return = 1.0%

Active return = 0.2%
```

Tracking error measures the volatility of those active returns over time.

### Interpretation

```text
Low tracking error = portfolio closely follows benchmark
High tracking error = portfolio deviates more from benchmark
```

Tracking error is especially important for active managers.

---

## 30. Information ratio

The information ratio measures active return per unit of active risk.

Formula:

```text
Information Ratio = Average active return / Tracking error
```

### Interpretation

A higher information ratio means the portfolio generated more excess return per unit of benchmark-relative risk.

### Example

```text
Average active return = 2%
Tracking error = 4%

Information ratio = 0.50
```

### Athena link

Information ratio can be included in Performance Analytics for benchmark-relative evaluation.

---

## 31. Sharpe ratio

The Sharpe ratio measures excess return per unit of total risk.

Formula:

```text
Sharpe Ratio = (Portfolio return - Risk-free rate) / Portfolio volatility
```

### Example

```text
Portfolio return = 10%
Risk-free rate = 3%
Portfolio volatility = 14%

Sharpe ratio = (10% - 3%) / 14%
Sharpe ratio = 0.50
```

### Interpretation

Higher Sharpe ratio generally means better risk-adjusted performance.

### Important caution

Sharpe ratio uses volatility as the risk measure. It treats upside and downside volatility similarly.

---

## 32. Sortino ratio

The Sortino ratio is similar to the Sharpe ratio but focuses on downside risk.

Formula:

```text
Sortino Ratio = (Portfolio return - Target return) / Downside deviation
```

### Difference from Sharpe

Sharpe uses total volatility.  
Sortino uses downside volatility.

### Why it matters

Investors usually care more about downside movements than upside movements.

### Example

If two portfolios have the same return and same total volatility, the one with less downside volatility may have a higher Sortino ratio.

---

## 33. Treynor ratio

The Treynor ratio measures excess return per unit of systematic risk.

Formula:

```text
Treynor Ratio = (Portfolio return - Risk-free rate) / Beta
```

### Sharpe vs Treynor

```text
Sharpe uses total risk.
Treynor uses systematic risk.
```

Treynor ratio is more relevant when the portfolio is well diversified.

### Example

```text
Portfolio return = 9%
Risk-free rate = 3%
Beta = 1.2

Treynor ratio = (9% - 3%) / 1.2
Treynor ratio = 5%
```

---

## 34. Maximum drawdown

Maximum drawdown measures the largest peak-to-trough decline.

Formula idea:

```text
Drawdown = Current value / Previous peak - 1
```

Maximum drawdown is the worst drawdown over the period.

### Example

```text
Portfolio peak = 120,000
Portfolio trough = 90,000

Drawdown = 90,000 / 120,000 - 1
Drawdown = -25%
```

### Why drawdown matters

Investors experience losses through drawdowns.

A portfolio can have attractive average returns but painful drawdowns.

Athena should display drawdown charts in Performance Analytics.

---

## 35. Rebalancing

Rebalancing means adjusting portfolio weights back toward target weights.

Example target allocation:

```text
60% equities
40% bonds
```

After market movements:

```text
70% equities
30% bonds
```

Rebalancing sells some equities and buys bonds to return to target.

### Why rebalancing matters

Rebalancing helps:

- control risk;
- maintain target allocation;
- avoid unintended concentration;
- enforce discipline.

### Trade-off

Rebalancing can create transaction costs and taxes.

---

## 36. Rebalancing frequency

Rebalancing can be done at fixed intervals.

Common frequencies:

```text
Monthly
Quarterly
Semiannual
Annual
```

### Frequent rebalancing

Advantages:

- keeps weights close to target;
- controls drift.

Disadvantages:

- higher transaction costs;
- more turnover.

### Less frequent rebalancing

Advantages:

- lower costs;
- fewer trades.

Disadvantages:

- more drift;
- risk can deviate from target.

---

## 37. Threshold-based rebalancing

Threshold-based rebalancing triggers when weights move too far from target.

Example:

```text
Target equity weight = 60%
Allowed drift = ±5%
```

Rebalance if equity weight goes below 55% or above 65%.

### Advantages

Threshold-based rebalancing reacts to actual portfolio drift instead of calendar dates.

### Athena link

Athena can show:

```text
Current weight
Target weight
Drift
Rebalance signal
```

Example:

```text
Technology target = 25%
Current technology weight = 38%
Status = Rebalance warning
```

---

## 38. Transaction costs

Transaction costs reduce portfolio returns.

Examples:

- commissions;
- bid-ask spread;
- slippage;
- market impact;
- taxes.

### Simple formula

```text
Net return = Gross return - Transaction costs
```

### Example

```text
Gross return = 8%
Transaction costs = 0.5%

Net return = 7.5%
```

### Why costs matter

A strategy that trades frequently must overcome higher transaction costs.

In Athena, trade simulation should eventually include transaction cost assumptions.

---

## 39. Turnover

Turnover measures how much of the portfolio is traded over a period.

High turnover means frequent trading.

### Formula idea

```text
Turnover = Value traded / Average portfolio value
```

### Interpretation

```text
Low turnover = stable portfolio
High turnover = active trading
```

### Why turnover matters

High turnover can increase:

- transaction costs;
- taxes;
- operational complexity;
- slippage.

A portfolio optimizer should not recommend constant large reallocations without considering turnover.

---

## 40. Concentration risk

Concentration risk occurs when too much of the portfolio is exposed to one asset, sector, country or factor.

Example:

```text
50% of portfolio in one stock
70% of portfolio in one sector
90% of portfolio in one currency
```

### Why concentration matters

Concentration can increase portfolio risk.

A concentrated portfolio may perform very well if the concentrated position rises, but it can also suffer large losses.

### Athena link

Athena should show concentration metrics such as:

```text
Top holding weight
Top 5 holdings weight
Largest sector weight
Largest currency weight
```

---

## 41. Sector exposure

Sector exposure measures how much of the portfolio is invested in each economic sector.

Examples:

```text
Technology
Financials
Healthcare
Energy
Consumer Staples
Industrials
Utilities
Materials
Real Estate
Communication Services
```

### Example

```text
Technology = 45%
Healthcare = 15%
Financials = 10%
Cash = 5%
Other = 25%
```

### Why it matters

Sector exposure helps identify hidden concentration.

A portfolio can have many assets but still be concentrated in one sector.

Athena should include a Sector Exposure Chart.

---

## 42. Geographic exposure

Geographic exposure measures how much of the portfolio is invested in different countries or regions.

Examples:

```text
United States
Canada
Europe
Japan
Emerging Markets
Global
```

### Why it matters

Geographic exposure affects:

- economic risk;
- currency risk;
- political risk;
- regulatory risk;
- diversification.

### Example

```text
US exposure = 80%
Canada exposure = 10%
Europe exposure = 10%
```

This portfolio is heavily exposed to the US market.

---

## 43. Currency exposure

Currency exposure measures how much of the portfolio is exposed to each currency.

Examples:

```text
USD
CAD
EUR
GBP
JPY
CHF
```

### Why it matters

If the investor's base currency is CAD but the portfolio holds many USD assets, portfolio value in CAD will be affected by USD/CAD movements.

### Example

```text
Portfolio base currency = CAD
USD exposure = 70%
CAD exposure = 20%
EUR exposure = 10%
```

This portfolio has significant foreign exchange exposure.

Athena should store both asset currency and portfolio base currency.

---

## 44. Factor exposure

Factor exposure describes sensitivity to broad drivers of return.

Common equity factors:

```text
Value
Growth
Momentum
Quality
Size
Low volatility
Dividend yield
```

### Why factors matter

Two portfolios may have different tickers but similar factor exposures.

Example:

```text
Portfolio A and Portfolio B both have high growth exposure.
```

They may behave similarly in certain market environments.

### Athena first version

Factor exposure can be a placeholder or optional advanced module.

---

## 45. Style exposure

Style exposure refers to investment style characteristics.

Common styles:

```text
Growth
Value
Blend
Quality
Momentum
Low volatility
Dividend income
```

### Growth style

Growth portfolios focus on companies expected to grow earnings or revenue faster than the market.

### Value style

Value portfolios focus on companies trading at lower valuation multiples.

### Why style matters

Growth and value can perform differently depending on interest rates, economic cycles and investor sentiment.

---

## 46. Growth vs value

Growth and value are two major investment styles.

### Growth

Growth companies usually have:

- high expected earnings growth;
- high valuation multiples;
- reinvestment in expansion;
- higher sensitivity to expectations.

### Value

Value companies usually have:

- lower valuation multiples;
- more mature business models;
- potential mispricing;
- often higher dividend yields.

### Simple comparison

```text
Growth = paying for future expansion
Value = buying relatively cheap current fundamentals
```

A portfolio may tilt toward growth or value.

---

## 47. Large cap vs small cap

Market capitalization measures the market value of a company.

Formula:

```text
Market capitalization = Share price × Shares outstanding
```

### Large-cap stocks

Usually:

- larger companies;
- more liquid;
- more established;
- often lower business risk.

### Small-cap stocks

Usually:

- smaller companies;
- less liquid;
- higher growth potential;
- higher risk.

### Portfolio implication

A small-cap-heavy portfolio may have higher expected return but also higher volatility.

---

## 48. Defensive vs cyclical sectors

Sectors can behave differently across economic cycles.

### Defensive sectors

Defensive sectors tend to be more stable during economic downturns.

Examples:

```text
Utilities
Consumer Staples
Healthcare
```

### Cyclical sectors

Cyclical sectors tend to be more sensitive to economic growth.

Examples:

```text
Industrials
Consumer Discretionary
Materials
Energy
Financials
```

### Why it matters

Sector mix affects how a portfolio behaves during different economic environments.

---

## 49. Portfolio constraints

Portfolio constraints limit what the portfolio can hold or how much it can allocate.

Examples:

```text
Maximum single asset weight = 10%
Maximum sector exposure = 35%
Minimum cash weight = 3%
No short selling
No leverage
Only listed equities and ETFs
Base currency must be CAD
```

### Why constraints matter

Constraints make the portfolio realistic.

An unconstrained optimizer might produce allocations that are not practical.

### Athena link

Constraints should be used in:

- Portfolio Builder;
- Portfolio Optimizer;
- Trade Simulator;
- Risk Monitor.

---

## 50. Long-only portfolios

A long-only portfolio only holds positive positions and cash.

It does not use short selling.

### Advantages

Long-only portfolios are:

- easier to understand;
- easier to implement;
- more common for beginner investment platforms;
- less risky than portfolios with short positions.

### Constraint

```text
Weight_i >= 0 for all assets
```

### Athena first version

Athena should start with long-only portfolios.

This makes portfolio construction, weights and risk easier to validate.

---

## 51. Leverage

Leverage means using borrowed money or derivatives to increase exposure.

Example:

```text
Portfolio value = 100,000
Market exposure = 150,000

Leverage = 1.5x
```

### Why leverage matters

Leverage magnifies gains and losses.

If exposure increases by 10%, a leveraged portfolio may gain more.  
If exposure falls by 10%, losses are also magnified.

### Athena note

Leverage should be treated as advanced. First version can use no leverage.

---

## 52. Margin

Margin is borrowed capital used to finance positions.

A margin account allows investors to buy more assets than their cash balance would allow.

### Margin risk

Margin can create:

- forced selling;
- margin calls;
- amplified losses;
- liquidity risk.

### Margin call

A margin call occurs when the investor must add collateral or reduce positions.

### Athena note

Margin can be documented but does not need to be implemented in the first version.

---

## 53. Portfolio optimization

Portfolio optimization tries to find portfolio weights that satisfy an objective and constraints.

Examples of objectives:

```text
Maximize expected return
Minimize volatility
Maximize Sharpe ratio
Target a specific return
Target a specific volatility
Balance risk contributions
```

Optimization requires inputs:

```text
Expected returns
Volatilities
Covariance matrix
Constraints
Risk-free rate
```

### Important caution

Optimization is sensitive to input assumptions.

Small changes in expected returns can produce very different optimal weights.

---

## 54. Mean-variance optimization

Mean-variance optimization uses expected return and variance to choose portfolio weights.

It tries to balance:

```text
Expected return
Portfolio risk
```

The classic idea is:

```text
For a given level of risk, choose the highest expected return.
For a given expected return, choose the lowest risk.
```

### Inputs

```text
Expected returns vector
Covariance matrix
Constraints
```

### Output

```text
Optimized weights
Expected portfolio return
Expected portfolio volatility
```

### Athena link

Athena can later implement mean-variance optimization using `scipy` or `cvxpy`.

---

## 55. Efficient frontier

The efficient frontier is the set of portfolios that provide the highest expected return for each level of risk.

Portfolios below the frontier are inefficient.

### Simple intuition

An inefficient portfolio can be improved by either:

- increasing expected return without increasing risk;
- reducing risk without reducing expected return.

### Visual

The efficient frontier is usually plotted with:

```text
x-axis = volatility
y-axis = expected return
```

### Athena component

Possible frontend component:

```text
EfficientFrontierChart
```

---

## 56. Minimum variance portfolio

The minimum variance portfolio is the portfolio with the lowest possible volatility, given the available assets and constraints.

Objective:

```text
Minimize portfolio variance
```

Subject to:

```text
weights sum to 1
constraints are respected
```

### Use case

This portfolio is useful for risk reduction.

### Limitation

It may have low expected return if it focuses only on minimizing volatility.

---

## 57. Maximum Sharpe portfolio

The maximum Sharpe portfolio maximizes excess return per unit of risk.

Formula:

```text
Sharpe Ratio = (Expected portfolio return - Risk-free rate) / Portfolio volatility
```

Objective:

```text
Maximize Sharpe ratio
```

### Why it matters

The maximum Sharpe portfolio is often used as a risk-adjusted optimal portfolio.

### Caution

It is sensitive to expected return estimates.

Poor inputs can produce unrealistic weights.

---

## 58. Target return portfolio

A target return portfolio is optimized to achieve a required expected return with the lowest possible risk.

Example:

```text
Target return = 8%
Objective = minimize volatility
```

This is useful when the investor has a required return objective.

### Constraint example

```text
Expected portfolio return >= 8%
Weights sum to 100%
No short selling
Maximum asset weight = 20%
```

---

## 59. Target volatility portfolio

A target volatility portfolio is designed to keep risk near a specific volatility level.

Example:

```text
Target volatility = 12%
```

The portfolio may adjust risky asset exposure to stay near that level.

### Use case

Target volatility strategies are common when risk control is more important than fixed asset weights.

### Athena link

Athena can later show whether current portfolio volatility is above or below target.

---

## 60. Risk parity

Risk parity allocates risk more evenly across assets.

Instead of equal capital weights, it tries to equalize risk contributions.

### Equal weight vs risk parity

Equal weight:

```text
Each asset receives the same capital weight.
```

Risk parity:

```text
Each asset contributes similarly to portfolio risk.
```

### Why it matters

A 50/50 stock-bond portfolio may still have most risk coming from stocks because stocks are more volatile.

Risk parity tries to correct this imbalance.

---

## 61. Equal-weight portfolio

An equal-weight portfolio gives the same weight to each asset.

Example with five assets:

```text
Each asset weight = 20%
```

### Advantages

Equal-weight portfolios are:

- simple;
- transparent;
- easy to implement;
- less dependent on forecasts.

### Limitations

Equal weighting ignores:

- asset risk;
- expected returns;
- correlations;
- liquidity;
- constraints.

### Athena use

Equal-weight can be a simple baseline allocation.

---

## 62. Capital allocation line

The Capital Allocation Line, or CAL, shows combinations of a risky portfolio and a risk-free asset.

It illustrates the trade-off between expected return and risk when combining:

```text
Risk-free asset
Risky portfolio
```

Formula idea:

```text
Expected return = Risk-free rate + slope × volatility
```

The slope is related to the Sharpe ratio of the risky portfolio.

### Intuition

A better risky portfolio has a steeper CAL because it offers more excess return per unit of risk.

---

## 63. Capital market line

The Capital Market Line, or CML, is a special case of the capital allocation line when the risky portfolio is the market portfolio.

It represents efficient combinations of:

```text
Risk-free asset
Market portfolio
```

### Interpretation

Portfolios on the CML are efficient under the assumptions of the model.

### Athena note

The CML is mainly theoretical. Athena may not need to implement it immediately, but it helps understand risk-return theory.

---

## 64. Capital asset pricing model

The Capital Asset Pricing Model, or CAPM, links expected return to systematic risk.

Formula:

```text
Expected return = Risk-free rate + Beta × Market risk premium
```

Where:

```text
Market risk premium = Expected market return - Risk-free rate
```

### Example

```text
Risk-free rate = 3%
Beta = 1.2
Market risk premium = 5%

Expected return = 3% + 1.2 × 5%
Expected return = 9%
```

### Meaning

CAPM says investors should be compensated for systematic risk, measured by beta.

---

## 65. Expected return

Expected return is the return an investor expects to earn in the future.

It can be estimated using:

- historical average returns;
- analyst forecasts;
- factor models;
- CAPM;
- scenario analysis;
- user assumptions.

### Important caution

Expected returns are uncertain.

Optimization models can become unstable if expected returns are poorly estimated.

### Athena link

Athena should allow expected returns to be explicit assumptions, not hidden magic numbers.

---

## 66. Risk-free rate

The risk-free rate is the theoretical return on an investment with no default risk and no uncertainty.

In practice, government short-term rates are often used as proxies.

Examples:

```text
Treasury bill yield
Short-term government rate
Overnight rate proxy
```

### Uses

The risk-free rate is used in:

- Sharpe ratio;
- CAPM;
- discounting;
- option pricing;
- performance analysis.

### Athena link

Athena should store or configure a risk-free rate assumption.

---

## 67. Market risk premium

The market risk premium is the excess expected return of the market over the risk-free rate.

Formula:

```text
Market risk premium = Expected market return - Risk-free rate
```

Example:

```text
Expected market return = 8%
Risk-free rate = 3%

Market risk premium = 5%
```

The market risk premium is used in CAPM.

### Athena note

This can be a configurable assumption in advanced analytics.

---

## 68. Portfolio performance attribution

Performance attribution explains why a portfolio outperformed or underperformed a benchmark.

It helps answer:

```text
Was performance due to asset allocation?
Was it due to security selection?
Was it due to sector exposure?
Was it due to currency?
```

Attribution is important because raw return does not explain the source of performance.

### Athena link

Athena can later include simplified attribution in Reports Center or Performance Analytics.

---

## 69. Asset allocation effect

Asset allocation effect measures the impact of being overweight or underweight certain segments compared with the benchmark.

Example:

```text
Portfolio overweight technology.
Technology outperformed.
Positive allocation effect.
```

If the portfolio is overweight a sector that performs poorly, allocation effect may be negative.

### Intuition

Allocation effect is about **where the portfolio was allocated**.

---

## 70. Security selection effect

Security selection effect measures the impact of choosing specific securities within a segment.

Example:

```text
Portfolio held better technology stocks than the benchmark technology sector.
Positive selection effect.
```

### Intuition

Selection effect is about **which securities were selected** inside a category.

### Allocation vs selection

```text
Allocation = choosing the bucket
Selection = choosing assets inside the bucket
```

---

## 71. Interaction effect

Interaction effect captures the combined impact of allocation and selection.

It appears because allocation and selection are not always independent.

In beginner portfolio analysis, interaction effect can be simplified or ignored.

### Athena note

First version can focus on:

```text
portfolio return
benchmark return
excess return
sector contribution
```

Detailed attribution can be added later.

---

## 72. Benchmark-relative performance

Benchmark-relative performance compares portfolio return to benchmark return.

Formula:

```text
Active return = Portfolio return - Benchmark return
```

Example:

```text
Portfolio return = 9%
Benchmark return = 7%

Active return = 2%
```

### Why it matters

Absolute return is not enough.

A portfolio can lose money and still outperform if the benchmark lost more.

Example:

```text
Portfolio return = -5%
Benchmark return = -12%

Active return = +7%
```

The portfolio outperformed despite losing money.

---

## 73. Portfolio monitoring

Portfolio monitoring is the ongoing process of checking whether the portfolio remains aligned with objectives and constraints.

Monitoring includes:

- current value;
- weights;
- performance;
- volatility;
- drawdown;
- benchmark comparison;
- sector exposure;
- currency exposure;
- concentration;
- drift;
- rebalancing signals.

### Athena link

The Dashboard should provide a portfolio monitoring view.

Possible cards:

```text
Portfolio Value
Daily Return
Annualized Volatility
Sharpe Ratio
Max Drawdown
Top Holding
Sector Concentration
Cash Weight
```

---

## 74. Portfolio drift

Portfolio drift occurs when actual portfolio weights move away from target weights due to market movements.

Example target:

```text
60% equities
40% bonds
```

After market changes:

```text
70% equities
30% bonds
```

The portfolio drifted toward equities.

### Why drift matters

Drift changes the risk profile.

A portfolio that started moderate can become aggressive if risky assets outperform.

### Athena link

Athena should calculate:

```text
Current weight - Target weight = Drift
```

---

## 75. Portfolio reporting

Portfolio reporting communicates portfolio status and performance.

A good report may include:

- portfolio value;
- return;
- benchmark comparison;
- asset allocation;
- top holdings;
- sector exposure;
- geographic exposure;
- currency exposure;
- volatility;
- drawdown;
- rebalancing notes;
- key changes.

### Reporting audience

Reports can be used by:

- portfolio managers;
- clients;
- risk analysts;
- management;
- investment committees.

### Athena link

Athena's Reports Center can later generate a portfolio report.

---

## 76. Data required for portfolio management

Athena needs structured data to manage portfolios.

### Portfolio

```text
id
name
description
base_currency
benchmark_symbol
objective
risk_profile
created_at
updated_at
```

### Position

```text
id
portfolio_id
asset_id
quantity
average_price
current_price
market_value
weight
currency
sector
country
```

### PortfolioMetric

```text
portfolio_id
valuation_date
total_value
daily_return
total_return
annualized_return
annualized_volatility
sharpe_ratio
sortino_ratio
max_drawdown
tracking_error
information_ratio
beta
alpha
```

### PortfolioExposure

```text
portfolio_id
valuation_date
sector_exposures
country_exposures
currency_exposures
factor_exposures
top_holdings
```

### TargetAllocation

```text
portfolio_id
asset_or_group
target_weight
minimum_weight
maximum_weight
```

---

## 77. Common beginner mistakes

### Mistake 1 — Looking only at returns

High return is not enough. Risk matters.

### Mistake 2 — Ignoring weights

A small position and a large position do not affect the portfolio equally.

### Mistake 3 — Confusing number of holdings with diversification

Many holdings can still be concentrated if they move together.

### Mistake 4 — Ignoring benchmark

Performance without benchmark context is incomplete.

### Mistake 5 — Ignoring costs

Transaction costs reduce returns.

### Mistake 6 — Ignoring currency exposure

Foreign assets create currency risk.

### Mistake 7 — Overtrusting optimization

Optimization results depend heavily on assumptions.

### Mistake 8 — Ignoring rebalancing

Portfolio weights change over time.

### Mistake 9 — Ignoring cash

Cash affects risk, return and exposure.

### Mistake 10 — Using the wrong benchmark

A wrong benchmark can make performance analysis misleading.

---

## 78. Key formulas

### Position market value

```text
Position market value = Quantity × Current price
```

### Portfolio market value

```text
Portfolio value = Sum of position market values + Cash
```

### Portfolio weight

```text
Weight_i = Position market value_i / Total portfolio value
```

### Portfolio return

```text
Portfolio return = Ending value / Beginning value - 1
```

### Weighted average return

```text
Portfolio return = w1R1 + w2R2 + ... + wnRn
```

### Two-asset portfolio variance

```text
σp² = w1²σ1² + w2²σ2² + 2w1w2σ1σ2ρ12
```

### Sharpe ratio

```text
Sharpe Ratio = (Portfolio return - Risk-free rate) / Portfolio volatility
```

### Sortino ratio

```text
Sortino Ratio = (Portfolio return - Target return) / Downside deviation
```

### Treynor ratio

```text
Treynor Ratio = (Portfolio return - Risk-free rate) / Beta
```

### Tracking error

```text
Tracking error = standard deviation of active returns
```

### Information ratio

```text
Information Ratio = Average active return / Tracking error
```

### Active return

```text
Active return = Portfolio return - Benchmark return
```

### CAPM expected return

```text
Expected return = Risk-free rate + Beta × Market risk premium
```

### Drawdown

```text
Drawdown = Current value / Previous peak - 1
```

### Turnover

```text
Turnover = Value traded / Average portfolio value
```

---

## 79. Possible API endpoints

Possible Athena endpoints for portfolio management:

```text
GET    /api/portfolios
POST   /api/portfolios
GET    /api/portfolios/{portfolio_id}
PUT    /api/portfolios/{portfolio_id}
DELETE /api/portfolios/{portfolio_id}

POST   /api/portfolios/{portfolio_id}/positions
PUT    /api/portfolios/{portfolio_id}/positions/{position_id}
DELETE /api/portfolios/{portfolio_id}/positions/{position_id}

GET    /api/portfolios/{portfolio_id}/value
GET    /api/portfolios/{portfolio_id}/weights
GET    /api/portfolios/{portfolio_id}/returns
GET    /api/portfolios/{portfolio_id}/performance
GET    /api/portfolios/{portfolio_id}/exposures
GET    /api/portfolios/{portfolio_id}/drawdown
GET    /api/portfolios/{portfolio_id}/benchmark-comparison

POST   /api/portfolios/{portfolio_id}/rebalance
POST   /api/portfolios/{portfolio_id}/optimize
```

### Example portfolio response

```json
{
  "portfolio_id": "pf_001",
  "name": "Athena Growth Portfolio",
  "base_currency": "CAD",
  "total_value": 100000,
  "benchmark_symbol": "SPY",
  "positions": [
    {
      "symbol": "AAPL",
      "quantity": 50,
      "current_price": 200,
      "market_value": 10000,
      "weight": 0.10
    }
  ]
}
```

---

## 80. Possible frontend components

Possible components for Athena's portfolio modules:

```text
PortfolioSelector
PortfolioSummaryCard
PortfolioValueCard
PositionTable
AddPositionForm
EditPositionModal
AllocationChart
SectorExposureChart
CurrencyExposureChart
CountryExposureChart
TopHoldingsTable
PerformanceMetricCards
BenchmarkComparisonChart
DrawdownChart
CorrelationMatrix
RebalancingPanel
TargetAllocationTable
PortfolioDriftCard
OptimizerPanel
EfficientFrontierChart
```

### Page ideas

```text
Portfolio Builder
Performance Analytics
Portfolio Optimizer
Dashboard Portfolio Summary
```

---

## 81. Suggested tests

### Portfolio value tests

```text
Portfolio value equals sum of position market values plus cash.
```

### Weight tests

```text
Position weight = position market value / total portfolio value.
Weights sum to 100% when cash is included.
```

### Return tests

```text
Portfolio return equals weighted average of asset returns.
```

### Volatility tests

```text
Portfolio volatility uses covariance matrix correctly.
Lower correlation reduces portfolio volatility.
```

### Benchmark tests

```text
Active return = portfolio return - benchmark return.
Tracking error is non-negative.
```

### Ratio tests

```text
Sharpe ratio handles zero volatility safely.
Sortino ratio handles no downside returns safely.
Information ratio handles zero tracking error safely.
```

### Rebalancing tests

```text
Target weights sum to 100%.
Rebalancing trades move current weights toward target weights.
Transaction costs reduce portfolio value.
```

### Exposure tests

```text
Sector exposure sums to 100%.
Currency exposure sums to 100%.
Top holding is correctly identified.
```

---

## 82. How Athena uses portfolio management

Athena AI Risk Terminal should use portfolio management concepts in several modules.

### Portfolio Builder

Allows the user to:

- create portfolios;
- add positions;
- edit positions;
- view weights;
- view total value;
- view allocation.

### Performance Analytics

Calculates:

- total return;
- annualized return;
- volatility;
- Sharpe ratio;
- Sortino ratio;
- drawdown;
- benchmark comparison.

### Trade Simulator

Shows how a proposed trade changes:

- weights;
- exposures;
- portfolio value;
- concentration;
- drift from target allocation.

### Portfolio Optimizer

Later, Athena can suggest allocations using:

- minimum variance;
- maximum Sharpe;
- target return;
- target volatility;
- risk parity;
- equal weight baseline.

### Dashboard

Displays key portfolio metrics:

```text
Portfolio value
Daily return
Top holding
Sector concentration
Cash weight
Benchmark-relative return
```

### Reports

Portfolio reports can summarize:

- holdings;
- performance;
- exposures;
- benchmark comparison;
- rebalancing notes.

---

## 83. Summary

Portfolio management is the process of building, monitoring and adjusting a collection of investments to meet objectives.

Key ideas:

```text
A portfolio is more than a list of assets.
Weights determine economic exposure.
Diversification depends on correlation.
Risk and return must be analyzed together.
Benchmarks provide context.
Performance ratios measure risk-adjusted results.
Rebalancing controls drift.
Optimization depends heavily on assumptions.
Constraints make portfolios realistic.
```

For Athena AI Risk Terminal, this document prepares the implementation of:

- Portfolio Builder;
- Performance Analytics;
- Portfolio Optimizer;
- Trade Simulator;
- portfolio dashboards;
- portfolio reporting.

The key lesson is:

```text
Portfolio management connects assets, weights, returns, risks, constraints and decisions into one coherent investment process.
```
