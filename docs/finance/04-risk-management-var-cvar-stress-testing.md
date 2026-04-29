# 04 — Risk Management, VaR, CVaR and Stress Testing

**Project:** Athena AI Risk Terminal  
**Recommended file path:** `docs/finance/04-risk-management-var-cvar-stress-testing.md`  
**Purpose:** build a clear and practical foundation in financial risk management, loss measurement, VaR, CVaR / Expected Shortfall, stress testing, risk limits and risk reporting before implementing the Risk Monitor in Athena.  
**Scope:** this document focuses only on market risk management, VaR, CVaR and stress testing. Portfolio management, options Greeks, front-office workflows, RiskDNA and P&L attribution are documented separately.

---

## Table of Contents

1. What is risk management?
2. Why risk management matters
3. Risk vs uncertainty
4. Return, volatility and loss
5. Why volatility is not enough
6. Main types of financial risk
7. Market risk
8. Credit risk
9. Liquidity risk
10. Operational risk
11. Model risk
12. Concentration risk
13. Currency risk
14. Interest rate risk
15. Risk measurement workflow
16. Portfolio value and profit/loss
17. Profit and loss distribution
18. Losses vs returns
19. Confidence level
20. Time horizon
21. Tail risk
22. Value at Risk overview
23. VaR intuition
24. VaR as a loss threshold
25. VaR confidence level
26. VaR time horizon
27. Historical VaR
28. Historical VaR example
29. Parametric VaR
30. Parametric VaR example
31. Monte Carlo VaR
32. Monte Carlo VaR intuition
33. VaR interpretation
34. What VaR does not tell you
35. VaR limitations
36. Backtesting VaR
37. VaR exceptions
38. Conditional VaR overview
39. Expected Shortfall overview
40. CVaR intuition
41. CVaR as average tail loss
42. Historical CVaR
43. Historical CVaR example
44. VaR vs CVaR
45. Why CVaR is more conservative
46. Loss distribution
47. Normal distribution assumption
48. Fat tails and extreme events
49. Downside risk
50. Drawdown risk
51. Risk contribution
52. Marginal contribution to risk
53. Component VaR
54. Portfolio risk decomposition
55. Stress testing overview
56. Why stress testing matters
57. Scenario analysis
58. Historical scenarios
59. Hypothetical scenarios
60. Sensitivity analysis
61. Equity market crash scenario
62. Interest rate shock scenario
63. FX shock scenario
64. Volatility shock scenario
65. Liquidity stress scenario
66. Correlation breakdown scenario
67. Stress loss calculation
68. Risk limits
69. Limit usage
70. Warning, breach and critical levels
71. Risk appetite
72. Risk dashboard
73. Risk reporting
74. Risk governance
75. Model assumptions
76. Data required for risk management
77. Common beginner mistakes
78. Key formulas
79. Possible API endpoints
80. Possible frontend components
81. Suggested tests
82. How Athena uses risk management
83. Summary

---

## 1. What is risk management?

Risk management is the process of identifying, measuring, monitoring and controlling risks.

In finance, risk management does not mean eliminating all risk. Risk is necessary because return usually requires taking risk.

The goal is to make risk:

- visible;
- measurable;
- controlled;
- explainable;
- aligned with objectives and limits.

Simple intuition:

```text
Investing = taking risk intentionally.
Risk management = making sure the risk is understood and controlled.
```

A portfolio manager may want to take risk to generate return.  
A risk manager wants to understand whether that risk is acceptable.

### Athena link

In Athena AI Risk Terminal, risk management supports:

- Risk Monitor;
- VaR engine;
- CVaR engine;
- Stress Testing;
- Limit Center;
- Risk Dashboard;
- RiskDNA inputs.

---

## 2. Why risk management matters

Risk management matters because financial losses can happen quickly.

A portfolio may look profitable during calm periods but suffer large losses during stress.

Risk management helps answer questions such as:

- How much can the portfolio lose?
- What happens if markets fall sharply?
- Which positions create the most risk?
- Are risk limits being breached?
- Is the portfolio too concentrated?
- Is the model relying on unrealistic assumptions?
- What scenarios could hurt the portfolio most?

### Example

A portfolio worth 100,000 may have:

```text
Expected daily return: +0.05%
Daily volatility: 1.5%
95% one-day VaR: 2,500
95% one-day CVaR: 4,000
```

The average return looks small and positive, but the tail risk can be much larger.

### Key lesson

```text
Return tells you what you earned.
Risk tells you what you could lose.
```

---

## 3. Risk vs uncertainty

Risk and uncertainty are related but not identical.

### Risk

Risk can be measured or estimated with a model.

Example:

```text
Estimated one-day 95% VaR = 10,000
```

### Uncertainty

Uncertainty refers to what is unknown, difficult to model or impossible to measure precisely.

Example:

```text
A sudden geopolitical event affects markets.
```

### Practical distinction

```text
Risk = measurable uncertainty
Uncertainty = unknown or hard-to-measure outcomes
```

In real markets, both exist. Risk models help, but they never remove uncertainty.

### Athena note

Athena should present risk metrics as estimates, not absolute truths.

---

## 4. Return, volatility and loss

A return measures how much value changes.

A loss is a negative outcome.

Volatility measures how much returns fluctuate.

### Example

```text
Portfolio value yesterday = 100,000
Portfolio value today = 98,000

Return = 98,000 / 100,000 - 1
Return = -2%

Loss = 2,000
```

### Volatility

If portfolio returns move strongly up and down, volatility is high.

### Important distinction

```text
Volatility measures movement.
Loss measures downside outcome.
```

A highly volatile asset can move up or down.  
Risk management is especially concerned with downside movements.

---

## 5. Why volatility is not enough

Volatility is useful, but it is not enough.

Volatility treats upside and downside movements similarly.

Example:

```text
Portfolio A:
+5%, -5%, +5%, -5%

Portfolio B:
0%, 0%, 0%, -20%
```

Volatility may not fully communicate the severity of a rare large loss.

### Problems with relying only on volatility

Volatility does not directly answer:

- How much can I lose?
- How bad are extreme losses?
- What happens in a crisis?
- Which position creates the loss?
- Are limits being breached?

This is why VaR, CVaR and stress testing are useful.

### Key distinction

```text
Volatility = uncertainty of returns
VaR = loss threshold
CVaR = average loss beyond the threshold
Stress testing = scenario loss
```

---

## 6. Main types of financial risk

Financial risk has many forms.

Main types include:

```text
Market risk
Credit risk
Liquidity risk
Operational risk
Model risk
Concentration risk
Currency risk
Interest rate risk
```

Each risk type answers a different question.

### Market risk

What happens if market prices move?

### Credit risk

What happens if a borrower or issuer cannot pay?

### Liquidity risk

What happens if an asset cannot be sold quickly at a fair price?

### Operational risk

What happens if systems, processes or people fail?

### Model risk

What happens if the model is wrong?

### Concentration risk

What happens if the portfolio depends too much on one asset, sector or factor?

### Currency risk

What happens if exchange rates move?

### Interest rate risk

What happens if rates change?

---

## 7. Market risk

Market risk is the risk of loss due to movements in market prices.

Examples of market risk drivers:

```text
Equity prices
Interest rates
Credit spreads
Foreign exchange rates
Commodity prices
Volatility
```

### Example

A portfolio holds technology stocks.

If the technology sector falls by 15%, the portfolio may suffer a large loss.

### Market risk measures

Market risk can be measured with:

- volatility;
- VaR;
- CVaR;
- stress testing;
- sensitivity analysis;
- beta;
- drawdown;
- risk contribution.

### Athena link

Athena's first risk engine should focus primarily on market risk.

---

## 8. Credit risk

Credit risk is the risk that a borrower or issuer fails to meet obligations.

Examples:

- bond issuer default;
- counterparty default;
- credit downgrade;
- spread widening.

### Default risk

Default risk is the risk that the borrower does not pay interest or principal.

### Spread risk

Spread risk is the risk that credit spreads widen, reducing bond prices.

### Example

A corporate bond yield increases from 5% to 7% because investors become worried about the issuer.

The bond price falls.

### Athena note

Credit risk can be added later in a more advanced fixed income module.

---

## 9. Liquidity risk

Liquidity risk is the risk of not being able to trade quickly without a large price impact.

A portfolio may have assets that look valuable on paper but are difficult to sell in a stressed market.

### Indicators of liquidity risk

```text
Low trading volume
Wide bid-ask spread
Few buyers and sellers
Large market impact
Stale prices
```

### Example

An asset has a market value of 100,000, but during stress, selling it quickly may only generate 92,000.

The liquidity loss is:

```text
100,000 - 92,000 = 8,000
```

### Athena link

Athena can include liquidity warnings based on volume, bid-ask spread or data quality.

---

## 10. Operational risk

Operational risk is the risk of loss due to failures in systems, processes, people or external events.

Examples:

- wrong trade entry;
- system outage;
- data error;
- failed reconciliation;
- cyber incident;
- incorrect report;
- process failure.

### Why operational risk matters

A portfolio can lose money even if the investment idea is correct, because execution or operations failed.

### Athena link

Operational risk can be indirectly supported through:

- audit trail;
- data validation;
- reconciliation;
- clear error handling;
- report generation logs.

---

## 11. Model risk

Model risk is the risk that a model is wrong, misused or based on bad assumptions.

Examples:

- assuming returns are normal when they have fat tails;
- using stale volatility estimates;
- using the wrong benchmark;
- ignoring correlations;
- using a model outside its valid scope.

### Model risk lesson

A model is a simplification of reality.

```text
A model can be useful and still be wrong.
```

### Athena rule

Athena should clearly show model assumptions.

Example:

```text
Parametric VaR assumes normally distributed returns.
Historical VaR uses past returns directly.
Stress testing uses scenario assumptions.
```

---

## 12. Concentration risk

Concentration risk occurs when too much exposure is concentrated in one asset, sector, country, currency or factor.

Examples:

```text
50% in one stock
70% in one sector
90% in one currency
```

### Why concentration matters

A concentrated portfolio can suffer large losses if the concentrated exposure declines.

### Example

A portfolio has:

```text
NVDA weight = 35%
Technology sector = 70%
```

Even if the portfolio has many positions, it is still highly exposed to technology risk.

### Athena link

Athena should calculate:

- top holding weight;
- top 5 holdings weight;
- sector exposure;
- currency exposure;
- concentration warnings.

---

## 13. Currency risk

Currency risk is the risk that exchange rates affect portfolio value.

Example:

```text
Portfolio base currency = CAD
Asset currency = USD
```

If USD/CAD moves, the CAD value of USD assets changes.

### Example

A Canadian investor holds a US asset.

```text
US asset return = 5%
USD/CAD change = -3%
Approximate CAD return = 2%
```

Currency can increase or reduce the investor's realized return.

### Athena link

Every asset should have a currency field, and every portfolio should have a base currency.

---

## 14. Interest rate risk

Interest rate risk is the risk that changes in rates affect asset values.

This is especially important for bonds.

Main rule:

```text
Yields rise → bond prices fall
Yields fall → bond prices rise
```

### Example

A bond with modified duration of 6 faces a +1% rate shock.

Approximate price change:

```text
-6 × 1% = -6%
```

### Athena note

Interest rate risk is developed in the Fixed Income file, but risk dashboards may still display rate shock losses.

---

## 15. Risk measurement workflow

A practical risk measurement workflow follows several steps.

```text
1. Load portfolio positions
2. Load market data
3. Calculate returns
4. Calculate portfolio value
5. Calculate portfolio P&L
6. Build loss distribution
7. Calculate risk metrics
8. Run stress scenarios
9. Check limits
10. Generate report
```

### Why workflow matters

Risk is not just one formula.

It is a process that depends on:

- clean data;
- correct positions;
- consistent prices;
- clear assumptions;
- validated calculations.

### Athena link

Athena should structure risk calculations as services, not as random formulas inside API routes.

---

## 16. Portfolio value and profit/loss

Portfolio value is the market value of all positions plus cash.

Formula:

```text
Portfolio value = Sum(position market values) + Cash
```

Profit and loss, or P&L, measures how value changes.

Formula:

```text
P&L = Ending portfolio value - Beginning portfolio value
```

Return:

```text
Return = Ending value / Beginning value - 1
```

### Example

```text
Beginning value = 100,000
Ending value = 97,500

P&L = 97,500 - 100,000
P&L = -2,500

Return = -2.5%
```

Risk management usually focuses on losses, meaning negative P&L.

---

## 17. Profit and loss distribution

A P&L distribution shows possible or historical gains and losses.

Example historical daily P&L:

```text
+500
-800
+200
-1,200
+700
-3,000
+100
```

From this distribution, the risk engine can estimate:

- typical gains/losses;
- volatility;
- worst historical losses;
- VaR;
- CVaR;
- stress behavior.

### Loss convention

It is often useful to define losses as positive numbers.

Example:

```text
P&L = -3,000
Loss = 3,000
```

This makes VaR and CVaR easier to interpret.

---

## 18. Losses vs returns

Risk metrics can be calculated using returns or money losses.

### Return-based risk

Example:

```text
95% VaR = 2%
```

This means a 2% loss threshold.

### Money-based risk

Example:

```text
Portfolio value = 100,000
95% VaR = 2%

Money VaR = 2,000
```

### Conversion

```text
Money VaR = Portfolio value × Return VaR
```

### Athena link

Athena should display both percentage and money values when possible.

Example:

```text
VaR 95% = 2.4% = 2,400 CAD
```

---

## 19. Confidence level

A confidence level defines how much of the distribution is covered.

Common levels:

```text
90%
95%
99%
```

### Example

A 95% VaR focuses on the loss threshold exceeded in the worst 5% of cases.

```text
95% confidence → 5% tail
99% confidence → 1% tail
```

### Intuition

Higher confidence levels look deeper into the tail.

A 99% VaR is usually larger than a 95% VaR.

### Athena setting

Confidence level should be configurable.

Example:

```text
confidence_level = 0.95
```

---

## 20. Time horizon

Time horizon defines the period over which risk is measured.

Common horizons:

```text
1 day
10 days
1 month
1 year
```

### Example

```text
1-day 95% VaR = 10,000
10-day 95% VaR = 30,000
```

Longer horizons usually imply larger potential losses.

### Important

Risk does not always scale perfectly with time.

A simple square-root-of-time rule may be used for approximate scaling, but it relies on assumptions.

### Athena first version

Start with:

```text
1-day VaR
1-day CVaR
```

Then extend later.

---

## 21. Tail risk

Tail risk is the risk of extreme outcomes in the tail of the distribution.

In a loss distribution, the right tail contains large losses if losses are represented as positive values.

### Example

Most daily losses may be below:

```text
1,000
```

But occasionally, losses may be:

```text
10,000
20,000
50,000
```

These extreme losses are tail events.

### Why tail risk matters

Tail events can dominate long-term outcomes.

A strategy can look safe most of the time but fail badly in rare scenarios.

---

## 22. Value at Risk overview

Value at Risk, or VaR, estimates a loss threshold for a given confidence level and time horizon.

It answers:

```text
How much could I lose over a given time horizon at a given confidence level?
```

Example:

```text
1-day 95% VaR = 10,000
```

Interpretation:

```text
With 95% confidence, the portfolio is not expected to lose more than 10,000 over one day under the model assumptions.
```

### Important

VaR is not the maximum possible loss.

It is a threshold.

Losses worse than VaR can still happen.

---

## 23. VaR intuition

Imagine sorting daily losses from smallest to largest.

Example:

```text
100
200
300
500
800
1,000
1,500
2,000
5,000
10,000
```

A VaR estimate chooses a percentile from this distribution.

At a high confidence level, VaR focuses on the large-loss region.

### Intuition

```text
VaR is the line between normal losses and tail losses.
```

It tells you where the danger zone begins, not how bad the danger zone can become.

---

## 24. VaR as a loss threshold

VaR should be understood as a threshold.

Example:

```text
95% VaR = 10,000
```

This does not mean the worst possible loss is 10,000.

It means losses worse than 10,000 are expected to occur in the tail beyond the confidence level.

### Simple interpretation

```text
VaR tells us: losses should usually not exceed this amount.
```

### But

```text
VaR does not tell us how large losses are when they do exceed this amount.
```

This is why CVaR is useful.

---

## 25. VaR confidence level

The confidence level controls how far into the loss distribution VaR looks.

### 95% VaR

Looks at the worst 5% tail.

### 99% VaR

Looks at the worst 1% tail.

### Example

```text
95% VaR = 10,000
99% VaR = 20,000
```

The 99% VaR is usually larger because it focuses on more extreme events.

### Athena link

The UI should clearly show:

```text
confidence level
time horizon
VaR value
method used
```

---

## 26. VaR time horizon

VaR must always include a time horizon.

Examples:

```text
1-day 95% VaR
10-day 95% VaR
1-month 99% VaR
```

A VaR number without a time horizon is incomplete.

### Example

```text
95% VaR = 10,000
```

This is unclear.

Better:

```text
1-day 95% VaR = 10,000
```

### Athena rule

Every risk metric should store:

```text
confidence_level
time_horizon
method
valuation_date
```

---

## 27. Historical VaR

Historical VaR uses past returns or losses directly.

It does not assume a normal distribution.

Steps:

```text
1. Collect historical returns
2. Convert returns into losses
3. Sort losses
4. Select the percentile corresponding to the confidence level
```

### Advantages

Historical VaR is:

- intuitive;
- easy to explain;
- based on observed data;
- useful for dashboards.

### Limitations

Historical VaR assumes the past is relevant for the future.

It may miss new risks not present in the historical window.

---

## 28. Historical VaR example

Suppose we have 20 daily losses in dollars:

```text
100
150
200
250
300
350
400
500
600
700
800
900
1,000
1,200
1,400
1,600
1,900
2,500
3,500
5,000
```

For 95% VaR, we look near the worst 5%.

With 20 observations:

```text
5% of 20 = 1 observation
```

The 95% VaR is close to the second-worst or worst loss depending on percentile convention.

Approximate result:

```text
95% VaR ≈ 3,500 or 5,000 depending on method
```

### Important

Different percentile interpolation methods can produce slightly different VaR values.

Athena should document the percentile method used.

---

## 29. Parametric VaR

Parametric VaR uses a statistical model.

The common simple version assumes returns are normally distributed.

Formula idea for return VaR:

```text
VaR = -(mean return + z-score × volatility)
```

For losses, the result is expressed as a positive number.

### Common z-scores

Approximate one-tail z-scores:

```text
95% confidence → 1.65
99% confidence → 2.33
```

### Advantages

Parametric VaR is:

- fast;
- easy to calculate;
- useful for simple models.

### Limitations

It depends heavily on distribution assumptions.

If returns have fat tails, normal VaR may underestimate risk.

---

## 30. Parametric VaR example

Assume:

```text
Portfolio value = 100,000
Mean daily return = 0%
Daily volatility = 1.5%
Confidence level = 95%
z-score = 1.65
```

Return VaR:

```text
VaR return ≈ 1.65 × 1.5%
VaR return ≈ 2.475%
```

Money VaR:

```text
Money VaR = 100,000 × 2.475%
Money VaR = 2,475
```

Interpretation:

```text
1-day 95% parametric VaR ≈ 2,475
```

### Important

This result depends on the normal distribution assumption.

---

## 31. Monte Carlo VaR

Monte Carlo VaR uses simulation.

Instead of relying only on historical observations or a simple formula, it generates many possible future scenarios.

Steps:

```text
1. Choose model assumptions
2. Simulate many return paths
3. Calculate portfolio value under each scenario
4. Build simulated loss distribution
5. Calculate VaR from simulated losses
```

### Example

```text
Simulate 10,000 one-day portfolio returns.
Calculate 10,000 possible losses.
Take the 95th percentile loss.
```

### Advantages

Monte Carlo can handle more complex assumptions.

### Limitations

It depends on the simulation model.

Bad assumptions produce bad simulations.

---

## 32. Monte Carlo VaR intuition

Monte Carlo VaR asks:

```text
If the market could evolve thousands of possible ways, what loss threshold appears in the simulated tail?
```

### Simple analogy

Instead of looking only at historical days, Monte Carlo creates artificial possible days.

Example:

```text
Scenario 1: portfolio return = +0.4%
Scenario 2: portfolio return = -1.2%
Scenario 3: portfolio return = -3.8%
...
Scenario 10,000
```

Then the losses are sorted, and VaR is calculated.

### Athena note

Monte Carlo VaR can be added after historical and parametric VaR.

---

## 33. VaR interpretation

A correct VaR statement must include:

```text
portfolio
method
confidence level
time horizon
currency or percentage
valuation date
```

Good statement:

```text
The portfolio has a 1-day 95% historical VaR of 12,000 CAD as of 2026-04-29.
```

Bad statement:

```text
The VaR is 12,000.
```

### Why the full statement matters

VaR changes depending on:

- method;
- confidence level;
- time horizon;
- portfolio value;
- historical window;
- market volatility.

Athena should never display VaR without context.

---

## 34. What VaR does not tell you

VaR does not tell you:

- the maximum possible loss;
- the average loss beyond VaR;
- how bad the worst case can be;
- whether the model assumptions are correct;
- what caused the risk;
- how risk changes under specific scenarios.

Example:

```text
95% VaR = 10,000
```

This does not say whether tail losses are:

```text
11,000
```

or:

```text
100,000
```

This is the main weakness of VaR.

---

## 35. VaR limitations

Main VaR limitations:

```text
VaR can underestimate extreme losses.
VaR depends on historical data or assumptions.
VaR does not describe tail severity.
VaR can be unstable with small samples.
VaR can be misleading under non-normal distributions.
VaR may ignore liquidity problems.
VaR may not capture sudden regime changes.
```

### Practical lesson

VaR should not be used alone.

It should be combined with:

- CVaR;
- stress testing;
- scenario analysis;
- risk limits;
- risk contribution;
- qualitative judgment.

---

## 36. Backtesting VaR

Backtesting checks whether VaR predictions are consistent with actual outcomes.

If a 95% one-day VaR model is accurate, actual losses should exceed VaR about 5% of the time.

### Example

Over 100 trading days:

```text
Expected exceptions ≈ 5
```

If there are 20 exceptions, the model may underestimate risk.

### Athena link

Athena can later include VaR backtesting:

```text
number of exceptions
exception dates
exception loss amount
exception rate
```

---

## 37. VaR exceptions

A VaR exception occurs when actual loss exceeds VaR.

Example:

```text
1-day 95% VaR = 10,000
Actual daily loss = 14,000

Exception = yes
```

### Why exceptions matter

Too many exceptions may indicate:

- volatility increased;
- model assumptions are wrong;
- historical window is outdated;
- portfolio changed;
- tail risk is underestimated.

### Athena UI idea

Display:

```text
VaR exceptions over last 250 days
Expected exceptions
Actual exceptions
Model status
```

---

## 38. Conditional VaR overview

Conditional VaR, or CVaR, measures the average loss beyond the VaR threshold.

It is also commonly called Expected Shortfall.

It answers:

```text
If losses exceed VaR, how large is the average tail loss?
```

### Example

```text
95% VaR = 10,000
95% CVaR = 16,000
```

Interpretation:

```text
The VaR threshold is 10,000, but when losses are worse than that threshold, the average loss is 16,000.
```

### Key idea

```text
VaR tells where the tail begins.
CVaR tells how bad the tail is on average.
```

---

## 39. Expected Shortfall overview

Expected Shortfall is another name for CVaR in many contexts.

The two terms are often used interchangeably.

```text
Expected Shortfall ≈ Conditional VaR
```

It focuses on the expected loss conditional on being in the tail.

### Why Expected Shortfall matters

Expected Shortfall is more informative for extreme risk because it considers losses beyond the VaR cutoff.

### Simple intuition

```text
VaR = threshold
Expected Shortfall = average beyond threshold
```

---

## 40. CVaR intuition

Suppose a portfolio has the following worst tail losses:

```text
10,000
12,000
15,000
20,000
```

If these are losses beyond the VaR threshold, CVaR is the average:

```text
CVaR = (10,000 + 12,000 + 15,000 + 20,000) / 4
CVaR = 14,250
```

CVaR tells us the average loss when things are already bad.

### Why this is useful

Investors and risk managers often care more about the severity of bad outcomes than the cutoff point alone.

---

## 41. CVaR as average tail loss

CVaR is a tail average.

If losses are represented as positive numbers:

```text
CVaR = average(losses greater than or equal to VaR threshold)
```

### Example

```text
VaR threshold = 10,000
Tail losses = 10,000, 14,000, 18,000

CVaR = 14,000
```

### Interpretation

When the portfolio enters the worst tail, the average loss is 14,000.

### Athena display

Athena should display both:

```text
VaR
CVaR
```

because they answer different questions.

---

## 42. Historical CVaR

Historical CVaR uses historical losses directly.

Steps:

```text
1. Calculate historical portfolio returns
2. Convert returns into losses
3. Sort losses
4. Calculate VaR threshold
5. Average the losses beyond the VaR threshold
```

### Advantages

Historical CVaR is:

- intuitive;
- based on observed historical losses;
- easy to explain;
- consistent with historical VaR.

### Limitations

It depends on the historical sample.

If the historical window does not include a crisis, CVaR may underestimate tail risk.

---

## 43. Historical CVaR example

Suppose sorted losses are:

```text
100
200
300
400
500
700
900
1,200
2,000
5,000
```

Assume the VaR threshold is:

```text
2,000
```

Tail losses beyond or equal to VaR:

```text
2,000
5,000
```

CVaR:

```text
CVaR = (2,000 + 5,000) / 2
CVaR = 3,500
```

Interpretation:

```text
The VaR threshold is 2,000, but the average tail loss is 3,500.
```

---

## 44. VaR vs CVaR

VaR and CVaR measure different aspects of downside risk.

### VaR

```text
Threshold loss at a confidence level
```

### CVaR

```text
Average loss beyond the threshold
```

### Example

```text
95% VaR = 10,000
95% CVaR = 18,000
```

Interpretation:

```text
Losses usually should not exceed 10,000 at the 95% level, but when they do, the average tail loss is 18,000.
```

### Simple comparison

```text
VaR = where the danger zone starts
CVaR = average damage inside the danger zone
```

---

## 45. Why CVaR is more conservative

CVaR is usually more conservative than VaR because it looks beyond the threshold.

If the tail contains extreme losses, CVaR captures them.

### Example

Two portfolios have the same VaR:

```text
Portfolio A VaR = 10,000
Portfolio B VaR = 10,000
```

But tail losses differ:

```text
Portfolio A tail losses: 10,000, 11,000, 12,000
Portfolio B tail losses: 10,000, 30,000, 80,000
```

CVaR will reveal that Portfolio B is much more dangerous.

### Key lesson

```text
Same VaR does not mean same tail risk.
```

---

## 46. Loss distribution

A loss distribution shows the range of possible or historical losses.

Example:

```text
Losses:
0
100
250
500
1,000
2,000
5,000
10,000
```

The distribution helps calculate:

- VaR;
- CVaR;
- worst loss;
- percentiles;
- tail behavior.

### Visualization

Athena can display:

```text
LossDistributionChart
VaR threshold line
CVaR tail area
```

### Why visualization matters

A chart can make risk easier to understand than a number alone.

---

## 47. Normal distribution assumption

Some models assume returns are normally distributed.

A normal distribution is symmetric and described by:

```text
mean
standard deviation
```

Parametric VaR often uses this assumption.

### Problem

Financial returns are often not perfectly normal.

They may have:

- fat tails;
- skewness;
- volatility clustering;
- sudden jumps.

### Athena note

When Athena uses parametric VaR, it should explain the normality assumption.

---

## 48. Fat tails and extreme events

Fat tails mean extreme events happen more often than a normal distribution would suggest.

### Example

A normal model may treat a -8% daily move as extremely rare.

In real markets, large moves can happen more often than expected.

### Why it matters

If a model underestimates fat tails, it may underestimate VaR and CVaR.

### Risk management lesson

```text
Do not rely only on normal models.
Use historical data and stress testing too.
```

---

## 49. Downside risk

Downside risk focuses only on negative outcomes.

Volatility measures both upside and downside movement.

Downside risk asks:

```text
How bad can losses be?
```

Examples of downside risk measures:

- downside deviation;
- VaR;
- CVaR;
- drawdown;
- semi-variance;
- stress loss.

### Why it matters

Investors usually care more about losing money than about unexpectedly high gains.

---

## 50. Drawdown risk

A drawdown measures decline from a previous peak.

Formula:

```text
Drawdown = Current value / Previous peak - 1
```

Maximum drawdown is the worst peak-to-trough decline.

### Example

```text
Portfolio peak = 120,000
Portfolio trough = 90,000

Drawdown = 90,000 / 120,000 - 1
Drawdown = -25%
```

### Why drawdown matters

Drawdowns represent the investor's lived experience of loss.

A strategy with strong average return can still be hard to tolerate if drawdowns are severe.

---

## 51. Risk contribution

Risk contribution identifies which positions contribute most to portfolio risk.

A portfolio-level risk number is useful, but it is not enough.

Risk managers also need to know:

```text
Which assets create the risk?
Which sectors create the risk?
Which exposures should be reduced?
```

### Example

```text
Portfolio VaR = 50,000
NVDA contribution = 18,000
AAPL contribution = 10,000
QQQ contribution = 8,000
Other = 14,000
```

### Athena link

Athena should include a RiskContributionTable.

---

## 52. Marginal contribution to risk

Marginal contribution to risk measures how portfolio risk changes when a position is slightly increased.

Conceptually:

```text
Marginal contribution = change in portfolio risk for a small change in weight
```

### Intuition

If increasing a position slightly increases total risk a lot, that position has high marginal risk.

### Use

Marginal risk helps answer:

```text
What happens if I add more of this asset?
```

This is useful for trade simulation.

---

## 53. Component VaR

Component VaR breaks total VaR into contributions by position or factor.

It attempts to answer:

```text
How much of total VaR comes from each position?
```

Example:

```text
Total VaR = 100,000

Component VaR:
AAPL = 25,000
MSFT = 20,000
NVDA = 35,000
Other = 20,000
```

### Why it matters

Component VaR helps prioritize risk reduction.

A risk manager can focus on the largest contributors first.

### Athena note

Component VaR can be advanced. First version can use simpler contribution approximations.

---

## 54. Portfolio risk decomposition

Portfolio risk decomposition breaks total risk into drivers.

Possible decompositions:

```text
By asset
By sector
By currency
By country
By factor
By strategy
```

### Example by sector

```text
Technology = 55% of risk
Financials = 15% of risk
Healthcare = 10% of risk
Other = 20% of risk
```

### Why decomposition matters

A portfolio may appear diversified by asset count but still have concentrated risk.

Athena should show both exposure and risk contribution when possible.

---

## 55. Stress testing overview

Stress testing estimates portfolio losses under specific scenarios.

Unlike VaR, stress testing does not primarily ask:

```text
What is the statistical percentile loss?
```

It asks:

```text
What happens if this specific shock occurs?
```

### Examples

```text
Equities fall 20%
Interest rates rise 100 bps
USD/CAD moves 5%
Volatility doubles
Liquidity disappears
Correlations go to 1
```

### Key distinction

```text
VaR is statistical.
Stress testing is scenario-based.
```

---

## 56. Why stress testing matters

Stress testing matters because risk models can miss extreme scenarios.

VaR may underestimate loss if:

- the historical window is calm;
- the model assumes normal returns;
- correlations change;
- liquidity disappears;
- volatility jumps.

Stress tests force the portfolio to face specific shocks.

### Example

A portfolio may have acceptable VaR but fail under:

```text
Equity crash scenario
Rate shock scenario
Currency shock scenario
```

### Athena link

Stress Testing should be a core risk page after VaR and CVaR.

---

## 57. Scenario analysis

Scenario analysis estimates the portfolio impact of a defined scenario.

A scenario includes assumptions such as:

```text
Equity shock
Rate shock
FX shock
Volatility shock
Credit spread shock
Correlation shock
```

### Example scenario

```text
Scenario name: Equity selloff
Equity shock: -20%
Technology shock: -30%
Volatility shock: +50%
```

### Output

The risk engine calculates:

```text
Estimated loss
Loss percentage
Worst contributors
Sector losses
Asset losses
```

---

## 58. Historical scenarios

Historical scenarios are based on real past events.

Examples:

```text
2008 financial crisis
COVID-19 market shock
Dot-com crash
Inflation shock period
Rate hiking cycle
```

### Advantage

They are realistic because they happened.

### Limitation

The future may not repeat the past exactly.

### Athena note

First version can include simplified historical-style scenarios without exact historical calibration.

Example:

```text
COVID-like shock: equities -25%, volatility +80%
```

---

## 59. Hypothetical scenarios

Hypothetical scenarios are designed manually.

Examples:

```text
Equities -20%
Rates +100 bps
USD/CAD +5%
Oil -30%
Technology -35%
```

### Advantage

They can test risks that may not exist in the historical sample.

### Limitation

They depend on assumptions.

### Athena link

Athena should allow predefined and later custom hypothetical scenarios.

---

## 60. Sensitivity analysis

Sensitivity analysis changes one variable at a time to see its impact.

Examples:

```text
What if equities fall 5%?
What if rates rise 50 bps?
What if volatility rises 20%?
What if FX moves 3%?
```

### Difference from scenario analysis

Sensitivity analysis is usually simpler and one-dimensional.

Scenario analysis can combine multiple shocks.

### Athena use

A simple sensitivity panel can be useful for quick risk exploration.

---

## 61. Equity market crash scenario

An equity crash scenario applies negative shocks to equity positions.

Example:

```text
All equities: -20%
Technology equities: -30%
Defensive equities: -10%
Cash: 0%
```

### Calculation idea

For each position:

```text
Stress loss = Market value × Shock
```

Example:

```text
Technology position = 50,000
Shock = -30%

Stress loss = -15,000
```

### Athena output

```text
Total stress loss
Loss by asset
Loss by sector
Worst contributors
```

---

## 62. Interest rate shock scenario

An interest rate shock scenario estimates the impact of rate changes.

For bonds, duration can approximate price impact.

Formula:

```text
% Price Change ≈ -Modified Duration × Change in Yield
```

Example:

```text
Modified duration = 6
Rate shock = +1%

Estimated price change = -6%
```

### Athena note

This connects to the Fixed Income module.

Risk Monitor can display rate shock losses if the portfolio contains rate-sensitive assets.

---

## 63. FX shock scenario

An FX shock scenario estimates the impact of currency movements.

Example:

```text
Portfolio base currency = CAD
USD exposure = 70%
USD/CAD shock = -5%
```

Approximate impact:

```text
Portfolio impact = 70% × -5%
Portfolio impact = -3.5%
```

### Why it matters

Foreign assets expose investors to exchange rate movements.

Athena should track asset currency and portfolio base currency.

---

## 64. Volatility shock scenario

A volatility shock increases volatility assumptions.

Example:

```text
Current volatility = 20%
Shock = +50%

Stressed volatility = 30%
```

### Why it matters

Higher volatility can increase risk measures.

In option portfolios, volatility shocks are especially important.  
The detailed option sensitivity topic belongs in the Options, Black-Scholes and Greeks document.

### Athena note

For this file, volatility shock can affect risk estimates such as parametric VaR.

---

## 65. Liquidity stress scenario

A liquidity stress scenario estimates losses or costs caused by poor market liquidity.

Example assumptions:

```text
Bid-ask spreads double
Low-volume assets suffer additional 3% liquidation discount
Large positions face market impact
```

### Example

```text
Illiquid position value = 100,000
Liquidity haircut = 5%

Estimated liquidity loss = 5,000
```

### Athena first version

Liquidity stress can start as a simple haircut by asset liquidity category.

---

## 66. Correlation breakdown scenario

In crises, correlations often rise.

Assets that seemed diversified may fall together.

### Example

Normal correlations:

```text
Asset A vs B correlation = 0.30
```

Stress correlation:

```text
Asset A vs B correlation = 0.90
```

### Why it matters

Diversification benefits can disappear in stressed markets.

### Athena note

A simple stress scenario can assume correlations increase toward 1 for risky assets.

---

## 67. Stress loss calculation

Stress loss is calculated by applying scenario shocks to portfolio exposures.

Basic formula:

```text
Stress loss = Sum(position market value × shock)
```

Example:

```text
AAPL value = 20,000
AAPL shock = -25%

Loss = -5,000
```

For multiple positions:

```text
Total stress loss = Sum(all stressed position losses)
```

### Output

Athena should return:

```text
estimated_loss
estimated_loss_pct
asset_losses
sector_losses
worst_contributors
scenario_name
```

---

## 68. Risk limits

Risk limits define maximum acceptable risk.

Examples:

```text
Maximum VaR
Maximum CVaR
Maximum sector exposure
Maximum single asset exposure
Maximum drawdown
Maximum stress loss
Maximum currency exposure
```

### Why limits matter

Risk metrics are not useful if there is no threshold for action.

A limit tells the system whether a risk level is acceptable.

### Example

```text
VaR limit = 50,000
Current VaR = 42,000

Status = OK or Warning depending on policy
```

---

## 69. Limit usage

Limit usage measures how much of a limit is consumed.

Formula:

```text
Limit usage = Current value / Limit
```

Example:

```text
Current VaR = 40,000
VaR limit = 50,000

Limit usage = 40,000 / 50,000
Limit usage = 80%
```

### Interpretation

```text
Low usage = comfortable
High usage = warning
Above 100% = breach
```

### Athena display

A LimitUsageBar should show:

```text
current value
limit
usage percent
status
```

---

## 70. Warning, breach and critical levels

Risk limits can have different levels.

Example:

```text
Warning: 80% of limit
Breach: 100% of limit
Critical: 120% of limit
```

### Example

```text
VaR limit = 50,000
Current VaR = 60,000

Usage = 120%
Status = Critical
```

### Why multiple levels help

Multiple levels allow the system to warn before a hard breach occurs.

### Athena statuses

Possible statuses:

```text
OK
Warning
Breach
Critical
```

---

## 71. Risk appetite

Risk appetite defines how much risk an investor or organization is willing to accept.

It should guide:

- limits;
- allocation;
- stress tolerance;
- reporting thresholds;
- escalation rules.

### Example

A conservative risk appetite may set:

```text
Max VaR = 2% of portfolio value
Max sector exposure = 25%
Max single asset exposure = 8%
```

An aggressive risk appetite may allow higher limits.

### Athena link

Athena can later provide risk profile presets.

---

## 72. Risk dashboard

A risk dashboard summarizes important risk metrics in one view.

Possible dashboard elements:

```text
Portfolio value
Daily P&L
Volatility
VaR
CVaR
Stress loss
Top risk contributors
Limit usage
Risk status
Latest breaches
```

### Goal

The dashboard should answer quickly:

```text
Is the portfolio risk acceptable today?
What changed?
What should be investigated?
```

### Athena UI

The Risk Monitor page should act as the first version of the risk dashboard.

---

## 73. Risk reporting

Risk reporting communicates risk information clearly.

A risk report may include:

- risk summary;
- VaR and CVaR;
- stress test results;
- limit breaches;
- top risk contributors;
- key assumptions;
- data quality warnings;
- methodology.

### Good reporting

A good report should be:

- clear;
- consistent;
- explainable;
- reproducible;
- linked to data and assumptions.

### Athena link

Reports Center can later generate daily risk reports.

---

## 74. Risk governance

Risk governance defines how risk is controlled.

It includes:

- roles and responsibilities;
- risk limits;
- approval process;
- escalation process;
- model validation;
- reporting frequency;
- audit trail.

### Example workflow

```text
Risk calculated
Limit checked
Breach detected
Alert generated
Responsible user reviews
Decision documented
Report archived
```

### Athena note

Athena can simulate this through:

- limit status;
- audit events;
- report generation;
- risk explanation panels.

---

## 75. Model assumptions

Every risk model has assumptions.

Examples:

```text
Historical VaR assumes historical losses are relevant.
Parametric VaR may assume normal returns.
Monte Carlo VaR depends on simulation assumptions.
Stress testing depends on scenario assumptions.
```

### Why assumptions matter

A risk number without assumptions can be misleading.

### Athena rule

Each risk metric should include metadata:

```text
method
confidence_level
time_horizon
lookback_window
distribution_assumption
valuation_date
```

This makes the output more transparent.

---

## 76. Data required for risk management

Athena needs structured data for risk calculations.

### Portfolio data

```text
portfolio_id
positions
quantities
market values
weights
base currency
```

### Market data

```text
historical prices
returns
volatility
correlations
liquidity indicators
```

### Risk settings

```text
confidence_level
time_horizon
lookback_window
VaR method
CVaR method
stress scenarios
risk limits
```

### Output data

```text
VaR
CVaR
loss distribution
stress results
limit usage
risk contributors
warnings
```

---

## 77. Common beginner mistakes

### Mistake 1 — Thinking VaR is the maximum possible loss

VaR is only a threshold.

### Mistake 2 — Ignoring CVaR

VaR does not explain the average severity beyond the threshold.

### Mistake 3 — Using volatility as the only risk measure

Volatility is useful but incomplete.

### Mistake 4 — Ignoring time horizon

A VaR number without time horizon is incomplete.

### Mistake 5 — Ignoring confidence level

95% VaR and 99% VaR are not the same.

### Mistake 6 — Mixing return losses and money losses

Always specify whether the risk metric is in percentage or currency.

### Mistake 7 — Ignoring data quality

Bad prices produce bad risk metrics.

### Mistake 8 — Trusting normal distribution blindly

Financial returns often have fat tails.

### Mistake 9 — Ignoring stress testing

Statistical metrics may miss specific extreme scenarios.

### Mistake 10 — Ignoring limits

Risk measurement without limits does not support decision-making.

---

## 78. Key formulas

### Return

```text
Return = Ending value / Beginning value - 1
```

### P&L

```text
P&L = Ending value - Beginning value
```

### Loss as positive value

```text
Loss = -P&L when P&L is negative
```

### Money VaR

```text
Money VaR = Portfolio value × Return VaR
```

### Historical VaR

```text
Historical VaR = percentile of historical losses
```

### Historical CVaR

```text
Historical CVaR = average losses beyond VaR threshold
```

### Parametric VaR simplified

```text
VaR ≈ z-score × volatility × portfolio value
```

### Limit usage

```text
Limit usage = Current risk value / Risk limit
```

### Stress loss

```text
Stress loss = Sum(position market value × scenario shock)
```

### Drawdown

```text
Drawdown = Current value / Previous peak - 1
```

---

## 79. Possible API endpoints

Possible Athena API endpoints for risk management:

```text
GET  /api/risk/{portfolio_id}/summary
GET  /api/risk/{portfolio_id}/loss-distribution
POST /api/risk/{portfolio_id}/historical-var
POST /api/risk/{portfolio_id}/parametric-var
POST /api/risk/{portfolio_id}/monte-carlo-var
POST /api/risk/{portfolio_id}/historical-cvar
POST /api/risk/{portfolio_id}/stress-test
GET  /api/risk/{portfolio_id}/risk-contribution
GET  /api/risk/{portfolio_id}/limits
POST /api/risk/{portfolio_id}/limits/check
GET  /api/risk/{portfolio_id}/var-backtest
```

### Example VaR response

```json
{
  "portfolio_id": "pf_001",
  "method": "historical",
  "confidence_level": 0.95,
  "time_horizon": "1D",
  "var_pct": 0.024,
  "var_amount": 2400,
  "currency": "CAD",
  "valuation_date": "2026-04-29"
}
```

### Example CVaR response

```json
{
  "portfolio_id": "pf_001",
  "method": "historical",
  "confidence_level": 0.95,
  "time_horizon": "1D",
  "cvar_pct": 0.038,
  "cvar_amount": 3800,
  "currency": "CAD"
}
```

---

## 80. Possible frontend components

Possible components for Athena's Risk Monitor:

```text
RiskSummaryCards
VaRCard
CVaRCard
VolatilityCard
MaxDrawdownCard
LossDistributionChart
TailLossChart
RiskContributionTable
StressScenarioSelector
StressLossChart
StressWorstContributorsTable
LimitUsageBar
LimitStatusBadge
RiskLimitTable
VaRBacktestPanel
RiskDashboard
RiskExplanationPanel
DataQualityWarnings
```

### Page goals

The Risk Monitor should help the user understand:

- current downside risk;
- VaR and CVaR;
- stress losses;
- limit usage;
- main risk contributors;
- whether risk is acceptable.

---

## 81. Suggested tests

### Historical VaR tests

```text
Historical VaR returns the correct percentile loss.
VaR is positive when expressed as a loss.
Higher confidence level produces larger or equal VaR.
```

### Historical CVaR tests

```text
Historical CVaR returns average loss beyond VaR.
CVaR is greater than or equal to VaR.
CVaR handles small samples safely.
```

### Parametric VaR tests

```text
Parametric VaR increases when volatility increases.
Parametric VaR increases when portfolio value increases.
Parametric VaR changes with confidence level.
```

### Stress testing tests

```text
Equity shock reduces equity portfolio value.
FX shock affects foreign currency exposure.
Rate shock affects rate-sensitive assets.
Stress loss equals sum of shocked position losses.
```

### Limit tests

```text
Limit usage is calculated correctly.
Status becomes Warning when warning threshold is exceeded.
Status becomes Breach when breach threshold is exceeded.
Status becomes Critical when critical threshold is exceeded.
```

### Data validation tests

```text
Missing returns are handled safely.
Empty loss distribution is rejected.
Invalid confidence level is rejected.
Negative portfolio value is rejected.
```

---

## 82. How Athena uses risk management

Athena AI Risk Terminal should use risk management concepts in several modules.

### Risk Monitor

Displays:

- VaR;
- CVaR;
- volatility;
- max drawdown;
- loss distribution;
- stress testing results;
- limit usage.

### Trade Simulator

After a proposed trade, Athena can compare:

```text
VaR before trade vs VaR after trade
CVaR before trade vs CVaR after trade
Stress loss before vs after
Limit usage before vs after
```

### Limit Center

Checks whether risk metrics exceed defined limits.

### RiskDNA

RiskDNA can use risk metrics as inputs:

```text
VaR usage
CVaR usage
stress loss
concentration
volatility regime
limit breach status
```

### Reports Center

Generates daily or trade-specific risk reports.

### Example Athena explanation

```text
The portfolio's 1-day 95% historical VaR is 2.4%, or 2,400 CAD. The 95% CVaR is 3.8%, or 3,800 CAD, meaning that losses beyond the VaR threshold are materially larger on average. The main contributor to risk is the technology allocation.
```

---

## 83. Summary

Risk management is the process of identifying, measuring, monitoring and controlling risk.

The most important ideas in this document are:

```text
Volatility measures uncertainty.
VaR estimates a loss threshold.
CVaR estimates the average loss beyond that threshold.
Stress testing estimates losses under specific scenarios.
Risk limits define what is acceptable.
Risk contribution explains where risk comes from.
Risk reporting makes the result understandable.
```

VaR is useful, but it is not enough.

CVaR helps understand the severity of tail losses.  
Stress testing helps explore specific crisis scenarios.  
Risk limits help transform calculations into decisions.

For Athena AI Risk Terminal, this document prepares the implementation of:

- Risk Monitor;
- VaR Engine;
- CVaR Engine;
- Stress Testing;
- Limit Center;
- Risk Contribution Table;
- Risk Dashboard;
- Trade Simulator risk impact;
- RiskDNA inputs;
- Reports Center.

The key lesson is:

```text
Risk management is not just about calculating numbers.
It is about turning uncertainty into controlled, explainable and actionable decisions.
```
