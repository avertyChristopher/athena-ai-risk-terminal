# 08 — P&L Attribution and Reporting

**Project:** Athena AI Risk Terminal  
**Recommended file path:** `docs/finance/08-pnl-attribution-reporting.md`  
**Purpose:** understand profit and loss, P&L attribution, P&L explain, reconciliation, reporting workflows and how Athena communicates portfolio performance and risk in a professional way.  
**Scope:** this document focuses on P&L attribution and reporting. It uses concepts from portfolio management, risk management, fixed income and options, but does not repeat their full methodology.

---

## Table of Contents

1. What is P&L?
2. Why P&L matters
3. P&L vs return
4. Realized P&L
5. Unrealized P&L
6. Daily P&L
7. Cumulative P&L
8. P&L attribution overview
9. Why attribution matters
10. Portfolio value change
11. Beginning value and ending value
12. Position-level P&L
13. Portfolio-level P&L
14. Price effect
15. Quantity effect
16. Trade effect
17. Cash effect
18. FX effect
19. Fee and transaction cost effect
20. Dividend and income effect
21. Interest income effect
22. Coupon income effect
23. Carry effect
24. Roll-down effect
25. Spread effect
26. Rate effect
27. Equity price effect
28. Sector contribution
29. Asset contribution
30. Currency contribution
31. Country contribution
32. Factor contribution
33. Benchmark-relative P&L
34. Active return
35. Allocation effect
36. Selection effect
37. Interaction effect
38. P&L explain
39. Explained P&L
40. Unexplained P&L
41. Residual P&L
42. Why unexplained P&L matters
43. P&L breaks
44. P&L reconciliation
45. Position reconciliation and P&L
46. Cash reconciliation and P&L
47. Market data impact on P&L
48. Clean price vs dirty price impact
49. Corporate actions and P&L
50. P&L for equities
51. P&L for ETFs
52. P&L for bonds
53. P&L for options
54. Delta P&L
55. Gamma P&L
56. Vega P&L
57. Theta P&L
58. Rho P&L
59. P&L explain for options
60. P&L and risk relationship
61. P&L vs VaR
62. P&L vs stress testing
63. P&L backtesting intuition
64. P&L attribution workflow
65. Daily P&L workflow
66. Front office P&L view
67. Middle office P&L control view
68. Management reporting view
69. Client reporting view
70. Report structure
71. Executive summary
72. Portfolio performance summary
73. Risk summary
74. P&L attribution table
75. Top contributors
76. Worst contributors
77. Benchmark comparison
78. RiskDNA summary in reports
79. Limit breach section
80. Stress testing section
81. Data quality section
82. Methodology section
83. Report validation
84. Report audit trail
85. Report versioning
86. Common beginner mistakes
87. Key formulas
88. Possible API endpoints
89. Possible frontend components
90. Suggested tests
91. How Athena uses P&L attribution
92. Summary

---

## 1. What is P&L?

P&L means **profit and loss**.

It measures how much money a position, portfolio or strategy gained or lost over a period.

Simple formula:

```text
P&L = Ending value - Beginning value
```

Example:

```text
Beginning value = 100,000
Ending value = 103,000

P&L = 103,000 - 100,000
P&L = +3,000
```

If the ending value is lower than the beginning value, P&L is negative.

Example:

```text
Beginning value = 100,000
Ending value = 97,500

P&L = -2,500
```

Simple interpretation:

```text
Positive P&L = profit
Negative P&L = loss
```

### Athena link

In Athena, P&L should be shown at multiple levels:

```text
Portfolio-level P&L
Position-level P&L
Asset-level P&L
Sector-level P&L
Currency-level P&L
Risk-driver P&L
```

---

## 2. Why P&L matters

P&L matters because it tells what actually happened financially.

Risk metrics estimate what could happen.  
P&L shows what did happen.

Important distinction:

```text
Risk = possible future loss
P&L = realized or current gain/loss
```

P&L helps answer:

```text
Did the portfolio make money?
Where did the profit come from?
Where did the loss come from?
Which positions helped?
Which positions hurt?
Was the loss expected by risk models?
Is there unexplained P&L?
```

### Example

```text
Portfolio P&L today = -3,200 CAD

Main contributors:
1. NVDA: -1,400 CAD
2. AAPL: -800 CAD
3. USD/CAD: -400 CAD
4. Fees: -50 CAD
5. Residual unexplained P&L: -550 CAD
```

This is more useful than only saying:

```text
Portfolio lost 3,200 CAD.
```

---

## 3. P&L vs return

P&L is expressed in money.

Return is expressed as a percentage.

Formula:

```text
Return = P&L / Beginning value
```

Example:

```text
Beginning value = 100,000
P&L = 3,000

Return = 3,000 / 100,000
Return = 3%
```

### Why both matter

P&L answers:

```text
How much money was gained or lost?
```

Return answers:

```text
How large was the gain or loss relative to capital?
```

Example:

```text
P&L = 1,000
```

This means different things for:

```text
Portfolio A value = 10,000 → return = 10%
Portfolio B value = 1,000,000 → return = 0.1%
```

Athena should display both money and percentage when possible.

---

## 4. Realized P&L

Realized P&L is profit or loss from positions that have been closed or partially closed.

Example:

```text
Buy 100 shares at 50
Sell 100 shares at 60
```

Realized P&L:

```text
(60 - 50) × 100 = 1,000
```

The gain is realized because the position was sold.

### Why realized P&L matters

Realized P&L is important for:

```text
Performance reporting
Tax reporting
Trade review
Strategy evaluation
```

### Athena link

Athena can start with simple realized P&L logic when trades are tracked.

---

## 5. Unrealized P&L

Unrealized P&L is profit or loss on positions still held.

Example:

```text
Buy 100 shares at 50
Current price = 60
Position still open
```

Unrealized P&L:

```text
(60 - 50) × 100 = 1,000
```

The gain exists on paper, but it is not realized until the position is sold.

### Important

Unrealized P&L can change quickly because market prices change.

### Athena link

Athena should calculate unrealized P&L for open positions.

---

## 6. Daily P&L

Daily P&L measures profit or loss over one day.

Formula:

```text
Daily P&L = Today's portfolio value - Yesterday's portfolio value
```

Example:

```text
Yesterday value = 100,000
Today value = 98,750

Daily P&L = -1,250
```

Daily P&L is central for middle office monitoring.

It helps detect:

```text
Large losses
Unexpected gains
Data issues
Trading errors
Risk model exceptions
```

### Athena link

Athena should show Daily P&L in the dashboard and reports.

---

## 7. Cumulative P&L

Cumulative P&L measures total profit or loss over a longer period.

Formula:

```text
Cumulative P&L = Current value - Initial value
```

Example:

```text
Initial value = 100,000
Current value = 112,000

Cumulative P&L = 12,000
```

Cumulative P&L can be tracked over:

```text
Week
Month
Quarter
Year
Since inception
```

### Athena link

A cumulative P&L chart helps the user see performance over time.

Possible component:

```text
CumulativePnLChart
```

---

## 8. P&L attribution overview

P&L attribution explains why P&L happened.

It decomposes total P&L into sources.

Simple idea:

```text
P&L tells what happened.
P&L attribution explains why it happened.
```

Example:

```text
Total P&L = 2,000

Price effect = 1,300
FX effect = 400
Dividend income = 200
Fees = -50
Residual = 150
```

Attribution makes performance explainable.

### Athena link

Athena should not only show total P&L. It should identify the main drivers.

---

## 9. Why attribution matters

Attribution matters because raw P&L is not enough.

A portfolio can make money for good or bad reasons.

Example:

```text
Portfolio P&L = +5,000
```

This could come from:

```text
Good stock selection
Currency movement
One concentrated position
Unexpected dividend
Data error
```

Attribution helps answer:

```text
Was the P&L expected?
Was it aligned with the strategy?
Was it caused by market risk?
Was it caused by trading activity?
Was it caused by data problems?
```

### Middle office view

The middle office wants to explain P&L clearly and detect unexplained results.

---

## 10. Portfolio value change

Portfolio value changes because of:

```text
Market price movements
Trades
Income
Fees
FX movements
Corporate actions
Cash flows
Interest
Data corrections
```

Basic formula:

```text
Ending value = Beginning value + P&L + External cash flows
```

If there are no external cash flows:

```text
P&L = Ending value - Beginning value
```

### Important

If the user adds or withdraws cash, simple P&L must separate investment performance from external flows.

Athena should eventually distinguish:

```text
Investment P&L
External contributions or withdrawals
```

---

## 11. Beginning value and ending value

P&L depends on a beginning value and an ending value.

Example:

```text
Beginning value at 2026-04-28 close = 100,000
Ending value at 2026-04-29 close = 101,500
```

Daily P&L:

```text
1,500
```

### Why dates matter

A P&L number without dates is incomplete.

Bad:

```text
P&L = 1,500
```

Better:

```text
Daily P&L on 2026-04-29 = 1,500 CAD
```

### Athena rule

Every P&L record should include:

```text
portfolio_id
valuation_date
beginning_value
ending_value
currency
```

---

## 12. Position-level P&L

Position-level P&L measures the gain or loss for one position.

Simple formula:

```text
Position P&L = (Ending price - Beginning price) × Quantity
```

Example:

```text
Quantity = 50
Beginning price = 100
Ending price = 108

Position P&L = (108 - 100) × 50
Position P&L = 400
```

Position-level P&L helps identify which holdings drove total portfolio P&L.

### Athena link

A `PositionPnLTable` should show:

```text
Symbol
Quantity
Beginning price
Ending price
P&L
P&L %
Contribution
```

---

## 13. Portfolio-level P&L

Portfolio-level P&L is the sum of all position-level P&L plus other effects.

Formula:

```text
Portfolio P&L =
Sum(position P&L)
+ cash effect
+ income
- fees
+ FX effect
+ residual
```

Example:

```text
Position P&L = 2,300
FX effect = -400
Fees = -50
Dividend income = 200
Residual = -30

Portfolio P&L = 2,020
```

Portfolio-level P&L should reconcile with:

```text
Ending portfolio value - Beginning portfolio value
```

If it does not, there is unexplained P&L.

---

## 14. Price effect

Price effect measures P&L caused by price changes.

Formula:

```text
Price P&L = Quantity × (Ending price - Beginning price)
```

Example:

```text
Quantity = 100
Beginning price = 50
Ending price = 53

Price P&L = 100 × 3
Price P&L = 300
```

Price effect is usually the main P&L driver for equities and ETFs.

### Athena link

Athena should calculate price effect separately from fees, income and FX when possible.

---

## 15. Quantity effect

Quantity effect captures the impact of changing position size.

If the portfolio trades during the day, P&L becomes more complex because quantity is not constant.

Example:

```text
Morning quantity = 100
Buy 50 more shares during the day
Ending quantity = 150
```

P&L should account for:

```text
Existing position price movement
New trade impact
Transaction cost
Execution price
```

### Simple first version

Athena can start with end-of-day position P&L.

Advanced version can separate intraday trade effects.

---

## 16. Trade effect

Trade effect measures the impact of trades on portfolio value and P&L.

Examples:

```text
Buying at a favorable price
Selling at a loss
Paying transaction costs
Changing exposure before a market move
```

Example:

```text
Buy 100 shares at 50
End price = 52

Trade-related unrealized P&L = (52 - 50) × 100 = 200
```

Trade effect is important because it connects decisions to outcomes.

### Athena link

Trade Simulator can later compare expected trade impact to realized P&L after execution.

---

## 17. Cash effect

Cash affects portfolio P&L through:

```text
Cash balance changes
Interest income
External deposits
Withdrawals
Trade settlements
Fees
```

Example:

```text
Cash earns interest = 20
```

Cash effect:

```text
+20
```

External cash flows must be separated from investment P&L.

Example:

```text
User deposits 10,000
Portfolio value rises by 10,000
This is not investment profit.
```

Athena should eventually distinguish external flows from P&L.

---

## 18. FX effect

FX effect measures the impact of currency movements.

Example:

```text
Portfolio base currency = CAD
Asset currency = USD
USD asset value = 10,000 USD
USD/CAD moves from 1.35 to 1.38
```

CAD value before:

```text
10,000 × 1.35 = 13,500 CAD
```

CAD value after:

```text
10,000 × 1.38 = 13,800 CAD
```

FX P&L:

```text
+300 CAD
```

FX effect is important for portfolios holding assets in multiple currencies.

---

## 19. Fee and transaction cost effect

Fees and transaction costs reduce P&L.

Examples:

```text
Commissions
Bid-ask spread
Slippage
Exchange fees
Management fees
Custody fees
Taxes
```

Formula:

```text
Net P&L = Gross P&L - Fees and costs
```

Example:

```text
Gross P&L = 1,000
Fees = 50

Net P&L = 950
```

### Athena link

Trade simulation and reporting should include estimated or actual costs when available.

---

## 20. Dividend and income effect

Dividend income contributes to P&L.

Example:

```text
Shares held = 100
Dividend per share = 2

Dividend income = 200
```

For total return, dividends matter.

If a stock price falls after paying a dividend, the investor may still be economically better off because they received cash.

### Athena link

Dividend and income effects can be added after basic price P&L.

---

## 21. Interest income effect

Interest income comes from cash or interest-bearing instruments.

Example:

```text
Cash balance = 50,000
Annual interest rate = 3%
Daily interest ≈ 50,000 × 3% / 365
Daily interest ≈ 4.11
```

Interest income may be small daily but meaningful over time.

### Athena link

Interest income can be included in advanced reporting, especially for portfolios with large cash balances.

---

## 22. Coupon income effect

Coupon income comes from bonds.

Example:

```text
Face value = 100,000
Coupon rate = 5%
Annual coupon = 5,000
```

If coupons are paid semiannually:

```text
Semiannual coupon = 2,500
```

Coupon income contributes to bond P&L.

### Athena link

The Fixed Income module should generate bond cash flows, and the P&L module should include coupon income when relevant.

---

## 23. Carry effect

Carry is the return earned from holding an asset, assuming market conditions do not change.

In fixed income, carry often includes coupon income and financing effects.

Example:

```text
A bond earns coupon income while being held.
```

Carry can be positive or negative.

### Simple intuition

```text
Carry = P&L from holding the position over time, before major market movements.
```

Carry is especially relevant for bonds, currencies and derivatives.

---

## 24. Roll-down effect

Roll-down effect occurs when a bond moves along the yield curve as time passes.

Example:

```text
A 5-year bond becomes a 4-year bond after one year.
```

If the yield curve is upward sloping, the bond may move to a lower yield point, increasing its price.

### Simple intuition

```text
Roll-down = price effect from aging along the yield curve.
```

Roll-down is a fixed income attribution concept.

Athena can document it first and implement later.

---

## 25. Spread effect

Spread effect measures P&L caused by credit spread changes.

For corporate bonds:

```text
Corporate yield = government yield + credit spread
```

If credit spreads widen, corporate bond prices usually fall.

Example:

```text
Spread widens by 50 bps
Bond price falls
Spread P&L is negative
```

### Athena link

Spread effect can be part of advanced fixed income P&L attribution.

---

## 26. Rate effect

Rate effect measures P&L caused by interest rate changes.

For bonds, duration can approximate rate P&L.

Formula:

```text
Approximate price change ≈ -Modified Duration × Change in Yield
```

Example:

```text
Modified duration = 6
Yield increases by 1%

Approximate price change = -6%
```

### Athena link

Rate effect connects Fixed Income and P&L Attribution.

---

## 27. Equity price effect

Equity price effect is P&L caused by stock price movements.

Formula:

```text
Equity price P&L = Quantity × (Ending price - Beginning price)
```

Example:

```text
Quantity = 20
Beginning price = 200
Ending price = 190

P&L = 20 × (190 - 200)
P&L = -200
```

Equity price effect is usually straightforward and should be implemented early.

---

## 28. Sector contribution

Sector contribution shows how much each sector contributed to portfolio P&L.

Example:

```text
Technology P&L = -1,800
Healthcare P&L = +600
Financials P&L = +300
Cash = +20
```

Sector contribution helps understand whether P&L came from a broad sector exposure or individual names.

### Athena component

```text
SectorPnLContributionChart
```

---

## 29. Asset contribution

Asset contribution shows how much each asset contributed to P&L.

Example:

```text
AAPL = -800
NVDA = -1,400
MSFT = +300
SPY = +500
```

This helps identify top and worst contributors.

### Athena link

Athena should rank assets by P&L contribution.

Possible tables:

```text
TopContributorsTable
WorstContributorsTable
```

---

## 30. Currency contribution

Currency contribution shows how much P&L came from FX movements.

Example:

```text
USD assets gained 1,000 USD from price movement.
USD/CAD movement added 300 CAD.
```

Currency contribution is important when portfolio base currency differs from asset currency.

### Athena link

Athena should store:

```text
asset currency
portfolio base currency
FX rate at beginning
FX rate at end
```

---

## 31. Country contribution

Country contribution shows P&L by country or region.

Example:

```text
United States = +1,200
Canada = -300
Europe = +150
Japan = -50
```

This is useful for globally diversified portfolios.

Country contribution can also reveal hidden macro exposure.

### Athena link

Country attribution can be implemented if assets have country metadata.

---

## 32. Factor contribution

Factor contribution explains P&L by style or risk factor.

Possible factors:

```text
Growth
Value
Momentum
Quality
Size
Low volatility
Dividend yield
```

Example:

```text
Growth factor contributed +1.2%
Value factor contributed -0.4%
```

This is advanced and can be added later.

### Athena note

Factor contribution should be documented but not required in the first version.

---

## 33. Benchmark-relative P&L

Benchmark-relative P&L compares portfolio performance to a benchmark.

Example:

```text
Portfolio return = 8%
Benchmark return = 6%
Active return = 2%
```

Benchmark-relative performance answers:

```text
Did the portfolio outperform or underperform its benchmark?
```

Absolute P&L is useful, but relative performance provides context.

### Athena link

Each portfolio should have an optional benchmark.

---

## 34. Active return

Active return is the difference between portfolio return and benchmark return.

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

If active return is positive, the portfolio outperformed.

If active return is negative, the portfolio underperformed.

### Athena link

Active return belongs in performance and reporting.

---

## 35. Allocation effect

Allocation effect measures whether overweighting or underweighting segments helped performance.

Example:

```text
Portfolio overweight technology.
Technology outperformed benchmark.
Allocation effect is positive.
```

If the portfolio is overweight a sector that underperforms, allocation effect is negative.

### Simple intuition

```text
Allocation effect = impact of choosing how much to allocate to each segment.
```

Detailed performance attribution can be implemented later, but the concept belongs in reporting.

---

## 36. Selection effect

Selection effect measures whether the selected securities within a segment outperformed.

Example:

```text
Portfolio held better technology stocks than the benchmark technology sector.
Selection effect is positive.
```

### Simple intuition

```text
Allocation = choosing the bucket.
Selection = choosing assets inside the bucket.
```

Selection effect helps separate portfolio construction skill from security selection skill.

---

## 37. Interaction effect

Interaction effect captures the combined effect of allocation and selection.

In detailed attribution, allocation and selection are not always independent.

For a first version, Athena can simplify and focus on:

```text
Portfolio return
Benchmark return
Active return
Top contributors
Sector contribution
```

Detailed Brinson-style attribution can be added later.

---

## 38. P&L explain

P&L explain is the process of explaining total P&L through known drivers.

Goal:

```text
Total P&L = Explained P&L + Unexplained P&L
```

Example:

```text
Total P&L = -5,000
Explained P&L = -4,700
Unexplained P&L = -300
```

P&L explain is a key middle office process.

It helps detect whether losses are understood or whether something is missing.

---

## 39. Explained P&L

Explained P&L is the part of total P&L attributed to known drivers.

Known drivers can include:

```text
Price movement
FX movement
Fees
Income
Rates
Spreads
Option Greeks
Trades
Cash effects
```

Example:

```text
Total P&L = 2,000

Explained:
Price effect = 1,300
FX effect = 400
Income = 200
Fees = -50

Explained P&L = 1,850
```

The remaining 150 is residual or unexplained.

---

## 40. Unexplained P&L

Unexplained P&L is the part of P&L not explained by the attribution model.

Formula:

```text
Unexplained P&L = Total P&L - Explained P&L
```

Example:

```text
Total P&L = 2,000
Explained P&L = 1,850

Unexplained P&L = 150
```

Small unexplained P&L may be acceptable depending on tolerance.

Large unexplained P&L requires investigation.

---

## 41. Residual P&L

Residual P&L is another name for unexplained P&L.

It may come from:

```text
Rounding
Missing fees
Timing differences
Incorrect prices
Missing FX effect
Corporate actions
Incorrect positions
Model approximation error
```

Example:

```text
Residual P&L = -700
```

A large residual should trigger a warning.

### Athena link

Athena should show an `ExplainedUnexplainedPnLCard`.

---

## 42. Why unexplained P&L matters

Unexplained P&L matters because it may indicate a problem.

Possible causes:

```text
Data issue
Pricing issue
Incorrect trade
Missing fee
Wrong FX rate
Corporate action
Position mismatch
Model issue
Operational break
```

Example:

```text
Total P&L = -10,000
Explained P&L = -6,000
Unexplained P&L = -4,000
```

This is significant and should be investigated.

### Athena link

Large unexplained P&L should create a warning or exception.

---

## 43. P&L breaks

A P&L break is a mismatch or unexplained difference in P&L.

Examples:

```text
System A P&L = 10,000
System B P&L = 9,400
Break = 600
```

or:

```text
Total P&L = -5,000
Explained P&L = -3,500
Unexplained P&L = -1,500
```

Breaks require investigation.

### Athena link

Athena can create a P&L break record when residual exceeds a tolerance.

---

## 44. P&L reconciliation

P&L reconciliation checks whether P&L is consistent across sources and calculations.

Reconciliation checks:

```text
Portfolio P&L equals sum of position P&L plus cash effects.
Ending value equals beginning value plus P&L plus flows.
Explained P&L plus unexplained P&L equals total P&L.
System values match report values.
```

### Example

```text
Portfolio total P&L = 1,000
Sum of position P&L = 950
Cash effect = 50

Reconciled = yes
```

Athena should include reconciliation tests.

---

## 45. Position reconciliation and P&L

Position reconciliation affects P&L because incorrect positions produce incorrect gains and losses.

Example:

```text
Internal quantity = 100
Actual quantity = 90
Price change = 5
```

P&L difference:

```text
(100 - 90) × 5 = 50
```

A position mismatch can explain part of unexplained P&L.

### Athena link

If reconciliation breaks exist, reports should show a data quality warning.

---

## 46. Cash reconciliation and P&L

Cash reconciliation affects P&L and portfolio value.

Example:

```text
Internal cash = 50,000
Actual cash = 49,800
Difference = -200
```

Possible explanations:

```text
Fees
Failed settlement
Interest
Withdrawal
Incorrect trade cost
FX conversion
```

Cash breaks can create unexplained P&L or incorrect portfolio value.

Athena should track cash effects separately when possible.

---

## 47. Market data impact on P&L

Market data errors can create false P&L.

Examples:

```text
Wrong closing price
Stale price
Missing price
Incorrect FX rate
Incorrect adjusted close
Wrong bond price
Wrong option volatility input
```

Example:

```text
Correct price = 100
Bad price = 110
Quantity = 1,000

False P&L impact = 10,000
```

### Athena link

DataQualityWarnings should be included in P&L reports.

---

## 48. Clean price vs dirty price impact

For bonds, clean price excludes accrued interest.  
Dirty price includes accrued interest.

Formula:

```text
Dirty price = Clean price + Accrued interest
```

If P&L uses inconsistent pricing, results can be wrong.

Example:

```text
Yesterday value uses dirty price.
Today value uses clean price.
```

This creates artificial P&L.

### Athena link

Fixed income P&L should specify pricing convention.

---

## 49. Corporate actions and P&L

Corporate actions can affect prices, quantities and cash.

Examples:

```text
Dividends
Stock splits
Reverse splits
Spin-offs
Rights issues
Special dividends
```

Example stock split:

```text
Before split:
100 shares at 200

After 2-for-1 split:
200 shares at 100
```

Economic value is unchanged, but raw price changed.

If Athena does not handle corporate actions correctly, P&L may be wrong.

---

## 50. P&L for equities

Equity P&L usually comes from:

```text
Price movement
Dividends
FX effect if foreign currency
Transaction costs
Corporate actions
```

Simple equity P&L:

```text
P&L = Quantity × (Ending price - Beginning price)
```

Example:

```text
Quantity = 100
Beginning price = 50
Ending price = 54

Price P&L = 400
```

Equity P&L is the best starting point for Athena.

---

## 51. P&L for ETFs

ETF P&L is similar to equity P&L.

Sources:

```text
Price movement
Distributions
FX effect
Fees
Tracking difference
Underlying exposure
```

Example:

```text
ETF beginning price = 100
ETF ending price = 103
Quantity = 50

P&L = 150
```

ETFs can represent broad exposures, so attribution may also be done by asset class or region if holdings data is available.

Athena first version can treat ETFs like equities.

---

## 52. P&L for bonds

Bond P&L can come from:

```text
Coupon income
Rate effect
Spread effect
Carry
Roll-down
Accrued interest
FX effect
Transaction costs
```

Example:

```text
Bond price P&L = -1,500
Coupon income = +500
Total bond P&L = -1,000
```

Bond P&L is more complex than equity P&L because yield and cash flow effects matter.

Athena can start with simple bond price P&L and later add rate/spread decomposition.

---

## 53. P&L for options

Option P&L can come from:

```text
Underlying price movement
Volatility change
Time decay
Interest rate change
Dividends
Gamma curvature
```

Greeks help explain option P&L.

Simplified formula:

```text
Option P&L ≈ Delta effect + Gamma effect + Vega effect + Theta effect + Rho effect
```

The detailed Greeks are covered in the Options document. Here, they are used only to explain P&L.

---

## 54. Delta P&L

Delta P&L estimates P&L from underlying price movement.

Formula:

```text
Delta P&L ≈ Delta × Change in underlying price
```

Example:

```text
Delta = 0.60
Underlying change = +3

Delta P&L ≈ 0.60 × 3
Delta P&L ≈ +1.80
```

For option contracts, multiply by contract size and number of contracts.

### Athena link

Option P&L explain should include Delta effect.

---

## 55. Gamma P&L

Gamma P&L estimates the curvature effect from underlying price movement.

Formula:

```text
Gamma P&L ≈ 0.5 × Gamma × (Change in underlying price)^2
```

Example:

```text
Gamma = 0.04
Underlying change = +3

Gamma P&L ≈ 0.5 × 0.04 × 3²
Gamma P&L ≈ 0.18
```

Gamma becomes more important for larger underlying moves.

---

## 56. Vega P&L

Vega P&L estimates P&L from volatility changes.

Formula:

```text
Vega P&L ≈ Vega × Change in volatility
```

Example:

```text
Vega = 0.25
Volatility increases by 2 percentage points

Vega P&L ≈ 0.25 × 2
Vega P&L ≈ 0.50
```

Vega convention must be documented.

Athena should specify whether Vega is per 1 volatility point.

---

## 57. Theta P&L

Theta P&L estimates P&L from time decay.

Formula:

```text
Theta P&L ≈ Theta × Days passed
```

Example:

```text
Theta = -0.04 per day
Days passed = 5

Theta P&L ≈ -0.20
```

Theta is usually negative for long options.

This means time passing reduces option value, all else equal.

---

## 58. Rho P&L

Rho P&L estimates P&L from changes in interest rates.

Formula:

```text
Rho P&L ≈ Rho × Change in interest rate
```

Example:

```text
Rho = 0.10
Rate increases by 1 percentage point

Rho P&L ≈ 0.10
```

Rho is often less important for short-dated equity options but can matter for longer maturities.

---

## 59. P&L explain for options

Option P&L explain combines multiple Greek effects.

Example:

```text
Total option P&L = 2.20

Delta P&L = 1.80
Gamma P&L = 0.18
Vega P&L = 0.50
Theta P&L = -0.20
Rho P&L = 0.02
Residual = -0.10
```

The residual may come from approximation error or other effects.

### Athena link

Option P&L explain can be a future advanced feature after Options Pricing Lab.

---

## 60. P&L and risk relationship

P&L and risk are connected.

Risk estimates potential losses before they happen.  
P&L shows actual gain or loss after market movements occur.

Questions:

```text
Was the loss consistent with risk estimates?
Did P&L exceed VaR?
Which risk driver caused the loss?
Did a stress scenario predict this vulnerability?
```

### Example

```text
VaR was low, but actual P&L loss was large.
```

This may indicate model weakness or unusual market conditions.

---

## 61. P&L vs VaR

VaR estimates a loss threshold.

Actual P&L can be compared to VaR.

Example:

```text
1-day 95% VaR = 10,000
Actual P&L = -15,000
```

This is a VaR exception.

Why?

Because actual loss exceeded the VaR threshold.

### Athena link

Athena can later include VaR backtesting:

```text
Date
VaR
Actual P&L
Exception yes/no
```

---

## 62. P&L vs stress testing

Stress testing estimates what could happen under a scenario.

P&L shows what actually happened.

Example:

```text
Equity crash stress scenario loss = -20,000
Actual market shock loss = -18,000
```

This suggests the stress scenario was directionally useful.

If actual loss is much worse than stress loss, scenarios may need review.

### Athena link

Reports can compare actual losses to stress scenario expectations.

---

## 63. P&L backtesting intuition

P&L backtesting compares realized P&L to risk model predictions.

Questions:

```text
How often did losses exceed VaR?
Were stress scenarios realistic?
Did the model underestimate tail losses?
Did risk metrics react quickly enough?
```

Example:

```text
Expected 95% VaR exceptions over 100 days ≈ 5
Actual exceptions = 12
```

This suggests the model may underestimate risk.

Athena can implement simple VaR exception tracking later.

---

## 64. P&L attribution workflow

A P&L attribution workflow turns raw portfolio value changes into explained drivers.

Workflow:

```text
1. Load beginning positions
2. Load ending positions
3. Load market prices
4. Load FX rates
5. Load trades
6. Load income and fees
7. Calculate position P&L
8. Calculate portfolio P&L
9. Decompose P&L by drivers
10. Calculate unexplained P&L
11. Validate and reconcile
12. Generate report
```

### Athena link

This workflow can power P&L Analytics and Reports Center.

---

## 65. Daily P&L workflow

Daily P&L workflow:

```text
1. Start with prior close portfolio state
2. Update today's market data
3. Apply trades and cash movements
4. Revalue positions
5. Calculate daily P&L
6. Attribute P&L by driver
7. Reconcile totals
8. Flag breaks
9. Publish dashboard
```

### Example daily output

```text
Daily P&L: -2,400 CAD
Top loss: NVDA -1,100 CAD
Main driver: equity price effect
Residual: -50 CAD
```

---

## 66. Front office P&L view

The front office P&L view focuses on investment decision outcomes.

It asks:

```text
Which trades made money?
Which positions contributed most?
Did the investment thesis work?
How did the portfolio perform vs benchmark?
```

Front office users want:

```text
Top contributors
Worst contributors
Trade impact
Benchmark comparison
Performance trend
```

### Athena link

Athena can show a performance view useful for portfolio managers.

---

## 67. Middle office P&L control view

The middle office P&L view focuses on accuracy, explanation and control.

It asks:

```text
Is P&L correct?
Is it reconciled?
Is there unexplained P&L?
Are market data inputs valid?
Do positions match records?
Are reports consistent?
```

Middle office users want:

```text
Explained vs unexplained P&L
Breaks
Reconciliation status
Data quality warnings
Audit trail
Report validation status
```

### Athena link

This supports a professional control-oriented interface.

---

## 68. Management reporting view

Management reporting focuses on oversight.

It asks:

```text
What happened today?
What are the biggest gains and losses?
Are risks increasing?
Were limits breached?
Are there unresolved issues?
```

Management reports should be concise and decision-oriented.

Example sections:

```text
P&L summary
Risk summary
Top drivers
Breaches
Stress losses
Data issues
Actions required
```

---

## 69. Client reporting view

Client reporting focuses on clarity.

It should explain performance without unnecessary technical complexity.

Client reports may include:

```text
Portfolio value
Performance
Benchmark comparison
Asset allocation
Top contributors
Risk summary
Commentary
```

Client reports should avoid overly technical internal control language unless required.

### Athena note

Athena reports can start as internal reports, then later support client-style reports.

---

## 70. Report structure

A professional report should be structured.

Recommended structure:

```text
1. Executive summary
2. Portfolio performance summary
3. P&L attribution
4. Top contributors
5. Worst contributors
6. Benchmark comparison
7. Risk summary
8. RiskDNA summary
9. Limit breaches
10. Stress testing results
11. Data quality notes
12. Methodology notes
13. Audit trail
```

The report should answer:

```text
What happened?
Why did it happen?
Is risk acceptable?
Are there issues to review?
```

---

## 71. Executive summary

The executive summary is the first section of the report.

It should be short and clear.

Example:

```text
The portfolio lost 2,400 CAD on 2026-04-29, mainly due to negative equity price movements in technology holdings. RiskDNA remains High because CVaR usage and technology concentration are elevated. No critical data quality issues were detected.
```

A good executive summary includes:

```text
P&L result
Main driver
Risk status
Important warnings
```

---

## 72. Portfolio performance summary

The performance summary provides key metrics.

Possible metrics:

```text
Beginning value
Ending value
Daily P&L
Daily return
Month-to-date return
Year-to-date return
Cumulative P&L
Benchmark return
Active return
```

Example:

```text
Beginning value: 100,000 CAD
Ending value: 97,600 CAD
Daily P&L: -2,400 CAD
Daily return: -2.4%
Benchmark return: -1.8%
Active return: -0.6%
```

---

## 73. Risk summary

The risk summary connects P&L to risk.

Possible metrics:

```text
VaR
CVaR
Stress loss
Volatility
Max drawdown
Limit usage
RiskDNA score
```

Example:

```text
1-day 95% VaR = 2,000 CAD
Actual P&L = -2,400 CAD
VaR exception = yes
```

This connects realized loss to expected risk.

---

## 74. P&L attribution table

A P&L attribution table decomposes total P&L.

Example:

```text
Driver                 | P&L
Equity price effect    | -1,800
FX effect              | -300
Fees                   | -50
Dividend income        | +100
Residual               | -350
Total                  | -2,400
```

This table is the core of the P&L report.

Athena should make it easy to see which drivers matter most.

---

## 75. Top contributors

Top contributors are positions or drivers that added the most P&L.

Example:

```text
MSFT: +600
SPY: +350
Cash interest: +20
```

Top contributors help explain gains.

### Athena component

```text
TopContributorsTable
```

Useful columns:

```text
Rank
Asset
P&L
P&L %
Contribution
Explanation
```

---

## 76. Worst contributors

Worst contributors are positions or drivers that reduced P&L the most.

Example:

```text
NVDA: -1,400
AAPL: -800
USD/CAD: -400
```

Worst contributors help identify sources of losses.

### Athena component

```text
WorstContributorsTable
```

Worst contributors should be included in both dashboards and reports.

---

## 77. Benchmark comparison

Benchmark comparison gives context.

Example:

```text
Portfolio return = -2.4%
Benchmark return = -1.8%
Active return = -0.6%
```

Interpretation:

```text
The portfolio underperformed the benchmark by 0.6 percentage points.
```

Benchmark comparison can include:

```text
Daily comparison
Month-to-date comparison
Year-to-date comparison
Cumulative comparison
```

Athena should include benchmark comparison when a benchmark is defined.

---

## 78. RiskDNA summary in reports

RiskDNA should appear in reports as a concise risk profile.

Example:

```text
RiskDNA Score: 74 / 100
Risk Level: High
Confidence: Medium

Top drivers:
1. CVaR usage
2. Technology concentration
3. Equity crash stress loss
```

The report should explain why the risk level matters.

Example:

```text
The portfolio remains classified as High risk because tail loss and sector concentration remain elevated.
```

---

## 79. Limit breach section

Reports should include limit breaches and warnings.

Example:

```text
Metric: Technology exposure
Current value: 42%
Limit: 35%
Status: Breach
```

Possible statuses:

```text
OK
Warning
Breach
Critical
```

The report should mention:

```text
Open breaches
New breaches
Resolved breaches
Critical breaches
```

This supports governance and escalation.

---

## 80. Stress testing section

The stress testing section summarizes scenario losses.

Example:

```text
Scenario                  | Estimated loss
Equity crash              | -16%
Rate shock +100 bps       | -4%
FX shock                  | -3%
Liquidity stress          | -5%
```

The report should highlight the worst scenario.

Example:

```text
The worst selected scenario is Equity Crash, with an estimated loss of 16%.
```

Stress testing connects risk to possible future shocks.

---

## 81. Data quality section

Reports should include data quality status.

Possible warnings:

```text
Missing price
Stale price
Missing FX rate
Missing benchmark
Unresolved reconciliation break
Invalid position data
```

Example:

```text
Data quality status: Warning
Reason: One position uses a stale price from the previous day.
```

Data quality matters because it affects confidence in the report.

---

## 82. Methodology section

The methodology section explains how metrics were calculated.

It may include:

```text
P&L calculation method
Return calculation method
Benchmark source
VaR method
CVaR method
Stress scenario definitions
RiskDNA methodology version
Data source timestamp
```

Example:

```text
RiskDNA methodology version: riskdna-v1.0
P&L method: end-of-day mark-to-market
VaR method: historical 1-day 95%
```

A methodology section increases transparency.

---

## 83. Report validation

Report validation checks that report numbers are accurate and consistent.

Validation checks:

```text
P&L equals ending value minus beginning value
Portfolio P&L equals sum of component P&L
Explained plus unexplained P&L equals total P&L
Dashboard values match report values
Dates and currencies are correct
Required sections are present
Data quality warnings are included
```

If validation fails, the report should remain in draft.

### Athena link

Reports should have validation status:

```text
Draft
Validated
Reviewed
Approved
Rejected
```

---

## 84. Report audit trail

A report audit trail records important report events.

Examples:

```text
Report generated
Report validated
Report reviewed
Report approved
Report rejected
Report exported
Report modified
```

Fields:

```text
event_id
report_id
event_type
performed_by
timestamp
details
```

Audit trail supports governance and traceability.

### Athena link

Reports should not just be files. They should be traceable objects.

---

## 85. Report versioning

Reports should be versioned when changed.

Example:

```text
Report v1 generated automatically.
Report v2 edited after review.
Report v3 approved.
```

Versioning helps answer:

```text
Which version was sent?
Who changed it?
What changed?
When was it approved?
```

### Athena link

Report entity should include:

```text
version
status
created_at
updated_at
reviewed_by
approved_by
```

---

## 86. Common beginner mistakes

### Mistake 1 — Confusing P&L and return

P&L is money. Return is percentage.

### Mistake 2 — Ignoring fees

Fees reduce P&L.

### Mistake 3 — Ignoring FX

Foreign positions can gain or lose because of currency movement.

### Mistake 4 — Ignoring income

Dividends, coupons and interest matter.

### Mistake 5 — Ignoring unexplained P&L

Large unexplained P&L may indicate a problem.

### Mistake 6 — Ignoring reconciliation

Wrong positions or cash create wrong P&L.

### Mistake 7 — Comparing performance without a benchmark

Benchmark context matters.

### Mistake 8 — Forgetting corporate actions

Splits and dividends can distort raw price P&L.

### Mistake 9 — Mixing clean and dirty bond prices

This can create artificial fixed income P&L.

### Mistake 10 — Sending reports without validation

Reports should be checked before approval.

---

## 87. Key formulas

### P&L

```text
P&L = Ending value - Beginning value
```

### Return

```text
Return = P&L / Beginning value
```

### Position price P&L

```text
Position P&L = Quantity × (Ending price - Beginning price)
```

### Portfolio P&L

```text
Portfolio P&L = Sum(position P&L) + cash effects + income - fees + FX effects + residual
```

### Unexplained P&L

```text
Unexplained P&L = Total P&L - Explained P&L
```

### Active return

```text
Active return = Portfolio return - Benchmark return
```

### FX value

```text
Base currency value = Foreign currency value × FX rate
```

### Delta P&L

```text
Delta P&L ≈ Delta × ΔS
```

### Gamma P&L

```text
Gamma P&L ≈ 0.5 × Gamma × (ΔS)^2
```

### Vega P&L

```text
Vega P&L ≈ Vega × ΔVolatility
```

### Theta P&L

```text
Theta P&L ≈ Theta × Days passed
```

### Rho P&L

```text
Rho P&L ≈ Rho × ΔRate
```

---

## 88. Possible API endpoints

Possible Athena API endpoints:

```text
GET  /api/pnl/{portfolio_id}/daily
GET  /api/pnl/{portfolio_id}/cumulative
GET  /api/pnl/{portfolio_id}/positions
GET  /api/pnl/{portfolio_id}/attribution
GET  /api/pnl/{portfolio_id}/drivers
GET  /api/pnl/{portfolio_id}/reconciliation
POST /api/pnl/{portfolio_id}/calculate
POST /api/pnl/{portfolio_id}/explain

POST /api/reports/{portfolio_id}/generate
GET  /api/reports/{portfolio_id}
GET  /api/reports/{portfolio_id}/{report_id}
POST /api/reports/{report_id}/validate
POST /api/reports/{report_id}/review
POST /api/reports/{report_id}/approve
POST /api/reports/{report_id}/reject
```

### Example P&L attribution response

```json
{
  "portfolio_id": "pf_001",
  "valuation_date": "2026-04-29",
  "currency": "CAD",
  "total_pnl": -2400,
  "explained_pnl": -2050,
  "unexplained_pnl": -350,
  "drivers": [
    {
      "name": "Equity price effect",
      "value": -1800
    },
    {
      "name": "FX effect",
      "value": -300
    },
    {
      "name": "Fees",
      "value": -50
    },
    {
      "name": "Dividend income",
      "value": 100
    }
  ]
}
```

---

## 89. Possible frontend components

Possible Athena frontend components:

```text
PnLSummaryCard
DailyPnLChart
CumulativePnLChart
PositionPnLTable
PnLAttributionChart
TopContributorsTable
WorstContributorsTable
ExplainedUnexplainedPnLCard
PnLReconciliationPanel
PnlBreakWarning
BenchmarkComparisonCard
ReportBuilder
ReportPreview
ReportStatusBadge
ReportAuditTrail
ReportVersionHistory
```

### Important pages

```text
P&L Dashboard
P&L Attribution
P&L Reconciliation
Reports Center
Report Preview
```

### UI goal

The user should understand:

```text
How much did the portfolio gain or lose?
Why did it happen?
Which positions drove it?
Is there unexplained P&L?
Is the report validated?
```

---

## 90. Suggested tests

### P&L tests

```text
Daily P&L equals ending value minus beginning value.
Return equals P&L divided by beginning value.
Position P&L equals price change times quantity.
Portfolio P&L equals sum of position P&L plus cash effects.
Fees reduce P&L.
Income increases P&L.
```

### FX tests

```text
FX movement affects foreign positions.
Base currency value uses correct FX rate.
Missing FX rate creates data quality warning.
```

### Attribution tests

```text
Explained P&L plus unexplained P&L equals total P&L.
Top contributors are ranked correctly.
Worst contributors are ranked correctly.
Residual above tolerance creates warning.
```

### Report tests

```text
Report generation includes required sections.
Report validation fails if totals do not reconcile.
Report status changes from draft to reviewed to approved.
Report stores methodology version.
Report audit trail records validation and approval events.
```

### Option P&L tests

```text
Delta P&L uses Delta times underlying move.
Gamma P&L uses half Gamma times squared underlying move.
Theta P&L decreases value for negative Theta.
```

---

## 91. How Athena uses P&L attribution

Athena uses P&L attribution as the final explanation layer for what actually happened.

### Main Athena use cases

```text
P&L Dashboard
Position-level P&L
Portfolio-level P&L
Explained vs unexplained P&L
Top contributors
Worst contributors
Benchmark comparison
Report generation
Risk model backtesting
```

### Full Athena logic

```text
Market data tells what prices did.
Portfolio management tells what the portfolio holds.
Risk management tells what could be lost.
RiskDNA explains the risk profile.
P&L attribution explains what actually happened.
Reporting communicates everything clearly.
```

### Example Athena explanation

```text
The portfolio lost 2,400 CAD today. The main driver was negative equity price movement in technology holdings, especially NVDA and AAPL. FX movement also reduced portfolio value by 300 CAD. The unexplained residual is 350 CAD and should be reviewed because it exceeds the configured tolerance.
```

This is the type of professional explanation Athena should generate.

---

## 92. Summary

P&L tells what happened financially.

P&L attribution explains why it happened.

Reporting communicates the result in a structured and validated way.

Key ideas:

```text
P&L = money gained or lost
Return = P&L relative to capital
Realized P&L = closed position gain/loss
Unrealized P&L = open position gain/loss
Attribution = explanation of P&L drivers
Explained P&L = P&L linked to known drivers
Unexplained P&L = residual requiring review
Reporting = communication of performance, risk and controls
```

For Athena AI Risk Terminal, this document prepares:

```text
P&L Dashboard
P&L Attribution
P&L Explain
Top contributors
Worst contributors
Benchmark comparison
Report Center
Report validation
Report audit trail
```

The final lesson is:

```text
A serious risk terminal must not only estimate what could happen.
It must also explain what actually happened and report it clearly.
```
