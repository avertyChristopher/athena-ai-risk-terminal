# 07 — RiskDNA and AI Methodology

**Project:** Athena AI Risk Terminal  
**Recommended file path:** `docs/finance/07-riskdna-ai-methodology.md`  
**Purpose:** define Athena's internal methodology for summarizing portfolio risk into a clear, explainable and auditable risk profile, while using AI only as an explanation and reporting assistant.  
**Scope:** this document focuses on RiskDNA scoring, explainability, AI methodology, model governance, auditability and Athena implementation. It does not repeat the detailed calculations from previous finance documents.

---

## Table of Contents

1. What is RiskDNA?
2. Why RiskDNA exists
3. RiskDNA vs traditional risk metrics
4. RiskDNA as a risk scoring methodology
5. Quantitative engine vs AI layer
6. Deterministic calculations vs AI explanations
7. RiskDNA design principles
8. Explainability first
9. Reproducibility
10. Transparency
11. Auditability
12. Human-in-the-loop principle
13. RiskDNA input categories
14. Market risk inputs
15. Portfolio risk inputs
16. Fixed income risk inputs
17. Options risk inputs
18. Stress testing inputs
19. Liquidity inputs
20. Concentration inputs
21. Limit breach inputs
22. Data quality inputs
23. Governance inputs
24. RiskDNA score overview
25. Risk score scale
26. Low risk profile
27. Medium risk profile
28. High risk profile
29. Critical risk profile
30. Weighted scoring approach
31. Rule-based scoring approach
32. Hybrid scoring approach
33. Why start with deterministic scoring
34. Example RiskDNA scoring model
35. VaR contribution to RiskDNA
36. CVaR contribution to RiskDNA
37. Stress loss contribution to RiskDNA
38. Volatility contribution to RiskDNA
39. Concentration contribution to RiskDNA
40. Liquidity contribution to RiskDNA
41. Limit breach contribution to RiskDNA
42. Data quality contribution to RiskDNA
43. Risk driver identification
44. Top risk drivers
45. Positive risk drivers
46. Negative risk drivers
47. RiskDNA explanation structure
48. RiskDNA summary sentence
49. RiskDNA detailed explanation
50. RiskDNA recommendation logic
51. RiskDNA confidence level
52. RiskDNA limitations
53. AI layer overview
54. Why use AI in Athena?
55. What AI should do
56. What AI should not do
57. AI as explanation assistant
58. AI as report assistant
59. AI as anomaly explanation assistant
60. AI as natural language interface
61. AI and deterministic boundaries
62. Prompt design for financial explanations
63. Risk explanation prompt structure
64. Report generation prompt structure
65. Trade explanation prompt structure
66. Anomaly explanation prompt structure
67. AI output validation
68. Hallucination risk
69. Model risk in AI
70. Data privacy and confidentiality
71. Human review requirement
72. AI governance principles
73. Explainable AI principles
74. RiskDNA audit trail
75. Versioning the scoring model
76. Versioning prompts
77. Storing AI explanations
78. Reproducibility of AI-assisted reports
79. RiskDNA dashboard
80. RiskDNA card
81. RiskDNA driver table
82. RiskDNA timeline
83. RiskDNA before/after trade view
84. RiskDNA stress scenario view
85. RiskDNA alerting
86. RiskDNA in the trade simulator
87. RiskDNA in the risk dashboard
88. RiskDNA in reports
89. RiskDNA in portfolio monitoring
90. Data required for RiskDNA
91. Common beginner mistakes
92. Key formulas and scoring logic
93. Possible API endpoints
94. Possible frontend components
95. Suggested tests
96. How Athena uses RiskDNA
97. Future improvements
98. Ethical considerations
99. Final methodology summary
100. Summary

---

## 1. What is RiskDNA?

RiskDNA is Athena's internal methodology for summarizing a portfolio's risk profile into a clear, explainable and auditable score.

It is not a replacement for detailed risk metrics.

It is a layer that takes existing risk outputs and organizes them into a readable risk profile.

Simple idea:

```text
Risk metrics are calculated by the quantitative engine.
RiskDNA summarizes and explains those metrics.
```

Example:

```text
RiskDNA Score: 78 / 100
Risk Level: High

Main drivers:
1. CVaR usage is near the limit.
2. Technology exposure is high.
3. Equity crash stress loss is significant.
4. Largest single-name position is above warning threshold.
```

RiskDNA should help users understand not only **how risky** the portfolio is, but also **why**.

---

## 2. Why RiskDNA exists

A financial risk terminal can quickly become difficult to read.

A user may see:

```text
VaR = 2.4%
CVaR = 3.8%
Volatility = 19%
Stress loss = 14%
Largest position = 18%
Technology exposure = 42%
Limit usage = 93%
```

These metrics are useful, but they may be hard to interpret together.

RiskDNA exists to answer:

```text
What is the overall risk profile?
What are the main risk drivers?
Is the risk acceptable?
What should the user pay attention to first?
```

RiskDNA turns many risk signals into a structured risk interpretation.

### Athena goal

RiskDNA should make Athena feel like a professional risk terminal, not just a collection of disconnected calculators.

---

## 3. RiskDNA vs traditional risk metrics

Traditional risk metrics measure specific dimensions of risk.

Examples:

```text
VaR measures a loss threshold.
CVaR measures average tail loss.
Stress testing measures scenario loss.
Volatility measures uncertainty.
Concentration measures exposure dependency.
Limit usage measures how close risk is to a threshold.
```

RiskDNA does not replace these metrics.

Instead, it combines them into:

```text
Score
Risk level
Top drivers
Explanation
Actionable warnings
```

### Example

Traditional metrics:

```text
VaR usage = 88%
CVaR usage = 95%
Stress loss = 16%
Largest position = 19%
```

RiskDNA output:

```text
Risk Level: High
Main reason: tail risk and concentration are elevated.
```

---

## 4. RiskDNA as a risk scoring methodology

RiskDNA is a scoring methodology.

A scoring methodology defines:

```text
Inputs
Rules
Weights
Thresholds
Risk levels
Driver ranking
Explanation structure
Versioning
```

It should be deterministic first.

That means the same inputs should produce the same RiskDNA score.

Example:

```text
Same VaR usage
Same CVaR usage
Same stress loss
Same concentration
Same limit status
        ↓
Same RiskDNA score
```

This makes the model testable and auditable.

---

## 5. Quantitative engine vs AI layer

Athena should separate the quantitative engine from the AI layer.

### Quantitative engine

The quantitative engine calculates deterministic financial metrics.

Examples:

```text
VaR
CVaR
Stress loss
Volatility
Portfolio weights
Concentration
Limit usage
Option Greeks
Duration
P&L
```

### AI layer

The AI layer explains, summarizes and formats the results.

Examples:

```text
Plain-English risk summary
Draft risk report
Trade impact explanation
Anomaly explanation
Question-answering over provided metrics
```

Core principle:

```text
The quantitative engine calculates.
The AI layer explains.
```

---

## 6. Deterministic calculations vs AI explanations

Deterministic calculations are predictable and testable.

Example:

```text
Limit usage = current value / limit value
```

AI explanations are language outputs based on provided inputs.

They are useful but less deterministic.

This is why Athena should never rely on AI to invent or calculate official risk numbers.

Correct approach:

```text
1. Calculate risk using deterministic code.
2. Pass calculated values to the AI layer.
3. Ask AI to explain only those values.
4. Store the explanation with input snapshot and prompt version.
```

Wrong approach:

```text
Ask AI to estimate VaR without controlled inputs.
```

---

## 7. RiskDNA design principles

RiskDNA should follow strong design principles:

```text
Explainability
Reproducibility
Transparency
Auditability
Human review
Deterministic scoring
Clear limitations
Version control
```

These principles make the methodology credible.

RiskDNA should not be a mysterious black box.

The user should understand:

```text
What inputs were used?
How the score was calculated?
Why the risk level was assigned?
Which drivers matter most?
What assumptions were applied?
```

---

## 8. Explainability first

RiskDNA should always explain the score.

A score alone is not enough.

Bad output:

```text
RiskDNA Score: 82
```

Better output:

```text
RiskDNA Score: 82 / 100
Risk Level: Critical

Main drivers:
- CVaR usage is above the critical threshold.
- Stress loss under equity crash scenario is high.
- Technology concentration exceeds the approved limit.
```

The goal is not only to rate the portfolio.

The goal is to explain the risk profile clearly.

---

## 9. Reproducibility

Reproducibility means that the same inputs should produce the same output.

For RiskDNA, reproducibility requires storing:

```text
Input metrics
Scoring version
Thresholds
Weights
Valuation date
Portfolio ID
Calculation timestamp
```

Example:

```text
riskdna_methodology_version = "riskdna-v1.0"
input_snapshot_id = "risk_run_2026_04_29_001"
```

If someone recalculates the same snapshot with the same methodology version, the score should match.

This is essential for trust.

---

## 10. Transparency

Transparency means users can understand what the system is doing.

RiskDNA should show:

```text
Score
Risk level
Input values
Weights
Thresholds
Top drivers
Warnings
Limit breaches
Methodology version
```

Example:

```text
VaR usage contributed 18 points to the RiskDNA score.
CVaR usage contributed 22 points.
Stress loss contributed 15 points.
```

Transparency is what prevents RiskDNA from feeling like a black-box rating.

---

## 11. Auditability

Auditability means the system can be reviewed after the fact.

An auditor, reviewer or user should be able to answer:

```text
What was the portfolio?
What were the inputs?
What model version was used?
What score was produced?
What explanation was generated?
Who reviewed it?
Was a trade approved after this score?
```

RiskDNA should create records, not just temporary UI values.

### Athena link

Important RiskDNA outputs should be stored with:

```text
timestamp
portfolio_id
input_snapshot_id
methodology_version
score
risk_level
drivers
```

---

## 12. Human-in-the-loop principle

Human-in-the-loop means the system supports human judgment but does not fully replace it.

RiskDNA can:

```text
Highlight risk
Explain drivers
Suggest attention areas
Draft a report
```

RiskDNA should not:

```text
Approve trades alone
Override risk limits alone
Make final investment decisions alone
Hide uncertainty
```

The user remains responsible for interpretation and decisions.

Simple principle:

```text
Athena assists.
The human decides.
```

---

## 13. RiskDNA input categories

RiskDNA uses outputs from other Athena modules.

Input categories can include:

```text
Market risk inputs
Portfolio risk inputs
Fixed income risk inputs
Options risk inputs
Stress testing inputs
Liquidity inputs
Concentration inputs
Limit breach inputs
Data quality inputs
Governance inputs
```

RiskDNA does not recalculate everything from scratch.

It receives already-calculated metrics and transforms them into a risk profile.

This prevents duplication and keeps the architecture clean.

---

## 14. Market risk inputs

Market risk inputs describe exposure to market movements.

Examples:

```text
Portfolio volatility
Volatility regime
Beta
Market drawdown
Return distribution indicators
```

Example:

```text
Annualized volatility = 28%
Volatility regime = High
```

RiskDNA can interpret this as:

```text
The portfolio is exposed to elevated market uncertainty.
```

The detailed market finance concepts are covered in the Market Finance and Volatility document.

---

## 15. Portfolio risk inputs

Portfolio risk inputs describe the structure and behavior of the portfolio.

Examples:

```text
Portfolio value
Position weights
Top holding weight
Sector exposure
Currency exposure
Geographic exposure
Benchmark active return
Tracking error
Drawdown
```

Example:

```text
Largest holding = 18%
Top 5 holdings = 62%
Technology exposure = 42%
```

RiskDNA can use these values to detect concentration and diversification issues.

---

## 16. Fixed income risk inputs

Fixed income risk inputs describe exposure to rates and bond risk.

Examples:

```text
Duration
Convexity
Rate shock loss
Yield curve exposure
Credit spread exposure
Maturity bucket exposure
```

Example:

```text
Modified duration = 7.2
+100 bps rate shock loss = 6.8%
```

RiskDNA can interpret this as:

```text
The portfolio has meaningful sensitivity to interest rate increases.
```

The detailed fixed income calculations belong in the Fixed Income document.

---

## 17. Options risk inputs

Options risk inputs describe option sensitivities.

Examples:

```text
Delta exposure
Gamma exposure
Vega exposure
Theta exposure
Rho exposure
Option scenario P&L
```

Example:

```text
Total Vega = 850
Total Theta = -120 per day
```

RiskDNA can interpret this as:

```text
The portfolio has significant volatility sensitivity and time decay exposure.
```

The detailed option and Greeks methodology belongs in the Options, Black-Scholes and Greeks document.

---

## 18. Stress testing inputs

Stress testing inputs describe losses under specific scenarios.

Examples:

```text
Equity crash stress loss
Rate shock stress loss
FX shock stress loss
Liquidity stress loss
Correlation breakdown scenario
Worst scenario loss
```

Example:

```text
Equity crash scenario loss = 16%
```

RiskDNA can treat high stress losses as major risk drivers.

Stress testing is essential because it shows scenario-based vulnerability beyond statistical metrics.

---

## 19. Liquidity inputs

Liquidity inputs describe the ability to trade or exit positions.

Examples:

```text
Average volume
Bid-ask spread
Liquidity category
Position size vs volume
Liquidity haircut
Stale price indicator
```

Example:

```text
Position equals 28% of average daily volume.
Liquidity status = Warning.
```

RiskDNA can interpret this as:

```text
The position may be difficult to exit quickly under stress.
```

Liquidity risk can increase the final score even if market VaR is moderate.

---

## 20. Concentration inputs

Concentration inputs measure dependency on a small number of exposures.

Examples:

```text
Largest position weight
Top 5 holdings weight
Sector concentration
Currency concentration
Country concentration
Factor concentration
Issuer concentration
```

Example:

```text
Largest position = 22%
Technology sector = 47%
```

RiskDNA can identify concentration as a major risk driver.

Concentration is important because a portfolio may appear diversified by number of holdings but still be exposed to the same underlying risk.

---

## 21. Limit breach inputs

Limit breach inputs show whether approved thresholds are exceeded.

Examples:

```text
VaR breach
CVaR breach
Sector exposure breach
Single-name breach
Stress loss breach
Liquidity breach
Drawdown breach
```

Possible statuses:

```text
OK
Warning
Breach
Critical
```

Example:

```text
Technology sector exposure = 42%
Limit = 35%
Status = Breach
```

Limit breaches should strongly affect the RiskDNA score.

---

## 22. Data quality inputs

Data quality inputs show whether the calculations can be trusted.

Examples:

```text
Missing prices
Stale prices
Duplicated dates
Missing currency
Invalid position quantity
Invalid volatility input
Missing benchmark
Unresolved reconciliation break
```

Example:

```text
Data quality status = Warning
Reason = stale price for one illiquid asset
```

RiskDNA should penalize poor data quality because unreliable inputs reduce confidence in the risk profile.

---

## 23. Governance inputs

Governance inputs describe control and review status.

Examples:

```text
Unreviewed model change
Unapproved scenario
Unresolved breach
Unreviewed AI report
Missing audit trail
Outdated methodology version
```

Example:

```text
Risk methodology version = outdated
Review status = pending
```

Governance inputs can increase the risk profile even if market metrics look acceptable.

A financial system is not only about numbers. It is also about controls.

---

## 24. RiskDNA score overview

The RiskDNA score is a single number summarizing overall risk.

Example scale:

```text
0 to 100
```

Where:

```text
0 = very low risk
100 = extremely high risk
```

Example output:

```text
RiskDNA Score: 74 / 100
Risk Level: High
```

The score should be:

```text
Deterministic
Explainable
Versioned
Auditable
Driven by measurable inputs
```

The score should never be generated freely by AI.

---

## 25. Risk score scale

A practical score scale could be:

```text
0–30   = Low
31–60  = Medium
61–80  = High
81–100 = Critical
```

Example:

```text
Score = 45 → Medium
Score = 72 → High
Score = 88 → Critical
```

The exact thresholds should be configurable.

Athena should store the score scale in the methodology version.

Example:

```text
riskdna_methodology_version = "v1.0"
score_scale = "0-30 low, 31-60 medium, 61-80 high, 81-100 critical"
```

---

## 26. Low risk profile

A low risk profile indicates that the portfolio is within comfortable limits.

Typical characteristics:

```text
Low VaR usage
Low CVaR usage
Moderate or low stress losses
No major concentration
No limit breach
Clean data quality
Good liquidity
```

Example:

```text
RiskDNA Score: 22 / 100
Risk Level: Low
```

Explanation:

```text
The portfolio has moderate exposures, no limit breaches, clean data quality and limited downside under the selected stress scenarios.
```

Low risk does not mean no risk.

It means risk appears controlled under the current methodology.

---

## 27. Medium risk profile

A medium risk profile indicates that risk is acceptable but should be monitored.

Typical characteristics:

```text
Moderate VaR usage
Some concentration
Manageable stress losses
No critical breaches
Minor warnings
```

Example:

```text
RiskDNA Score: 48 / 100
Risk Level: Medium
```

Explanation:

```text
The portfolio remains within limits, but sector concentration and stress loss are approaching warning levels.
```

Medium risk often means no immediate action is required, but monitoring is important.

---

## 28. High risk profile

A high risk profile indicates that risk is elevated.

Typical characteristics:

```text
High VaR or CVaR usage
Large stress losses
High concentration
Liquidity warning
Near-breach or breach conditions
```

Example:

```text
RiskDNA Score: 74 / 100
Risk Level: High
```

Explanation:

```text
The portfolio shows elevated downside risk mainly due to high tail loss, sector concentration and stress scenario vulnerability.
```

High risk should trigger review or risk reduction consideration.

---

## 29. Critical risk profile

A critical risk profile indicates that risk is severe or outside acceptable boundaries.

Typical characteristics:

```text
Limit breach
Critical CVaR usage
Severe stress loss
Major concentration
Poor data quality
Unresolved governance issue
```

Example:

```text
RiskDNA Score: 91 / 100
Risk Level: Critical
```

Explanation:

```text
The portfolio breaches approved risk limits and shows severe downside exposure under stress scenarios.
```

Critical risk should trigger escalation.

---

## 30. Weighted scoring approach

A weighted scoring approach assigns weights to different risk components.

Example weights:

```text
VaR usage:             20%
CVaR usage:            20%
Stress loss:           20%
Concentration:         15%
Volatility regime:     10%
Liquidity:              5%
Limit breaches:         5%
Data quality warnings:  5%
```

Formula:

```text
RiskDNA Score =
0.20 × VaRScore
+ 0.20 × CVaRScore
+ 0.20 × StressScore
+ 0.15 × ConcentrationScore
+ 0.10 × VolatilityScore
+ 0.05 × LiquidityScore
+ 0.05 × BreachScore
+ 0.05 × DataQualityScore
```

This approach is transparent and easy to test.

---

## 31. Rule-based scoring approach

A rule-based approach uses conditions and thresholds.

Example rules:

```text
If VaR usage > 100%, add 25 points.
If CVaR usage > 100%, add 25 points.
If stress loss > 15%, add 20 points.
If largest position > 20%, add 10 points.
If data quality status = Critical, add 20 points.
```

Rule-based scoring is useful because it is easy to explain.

Example:

```text
Score increased because CVaR exceeded its limit.
```

The downside is that rule boundaries can be too rigid if not designed carefully.

---

## 32. Hybrid scoring approach

A hybrid approach combines weighted scoring and rule-based overrides.

Example:

```text
Base score = weighted model
Override = if any critical breach exists, risk level cannot be below High
```

This is practical because some conditions are too important to average away.

Example:

```text
Weighted score = 52
But CVaR breach = Critical
Final risk level = High or Critical
```

### Athena recommendation

Athena should use a hybrid approach:

```text
Weighted score for general risk
Rule-based overrides for breaches and critical warnings
```

---

## 33. Why start with deterministic scoring

Athena should start with deterministic RiskDNA scoring.

Reasons:

```text
Testable
Explainable
Auditable
Stable
Easy to debug
Professional
Safe
```

AI-generated scoring would be risky because it may be inconsistent or hallucinate.

Correct design:

```text
Deterministic model calculates score.
AI explains the score.
```

This architecture is stronger and more credible.

---

## 34. Example RiskDNA scoring model

Example normalized component scores:

```text
VaRScore = 85
CVaRScore = 92
StressScore = 78
ConcentrationScore = 70
VolatilityScore = 60
LiquidityScore = 40
BreachScore = 50
DataQualityScore = 0
```

Weights:

```text
VaR = 20%
CVaR = 20%
Stress = 20%
Concentration = 15%
Volatility = 10%
Liquidity = 5%
Breach = 5%
Data quality = 5%
```

Calculation:

```text
Score =
0.20×85 + 0.20×92 + 0.20×78 + 0.15×70
+ 0.10×60 + 0.05×40 + 0.05×50 + 0.05×0

Score = 72.0
```

Risk level:

```text
72 = High
```

---

## 35. VaR contribution to RiskDNA

VaR contribution measures how close VaR is to its limit.

Example:

```text
Current VaR = 42,000
VaR limit = 50,000
VaR usage = 84%
```

A simple scoring rule:

```text
VaR usage < 50%     → low score
50% to 80%          → medium score
80% to 100%         → high score
above 100%          → critical score
```

Example:

```text
VaR usage = 84%
VaRScore = High
```

RiskDNA explanation:

```text
VaR usage is elevated and approaching the approved limit.
```

---

## 36. CVaR contribution to RiskDNA

CVaR contribution measures average tail loss relative to a limit.

Example:

```text
Current CVaR = 68,000
CVaR limit = 75,000
CVaR usage = 90.7%
```

CVaR should often receive strong weight because it captures severity beyond the VaR threshold.

Example explanation:

```text
CVaR is close to the limit, indicating that losses beyond the VaR threshold could be materially severe.
```

If CVaR is much larger than VaR, this can be a warning about fat-tail exposure.

---

## 37. Stress loss contribution to RiskDNA

Stress loss contribution measures vulnerability under defined scenarios.

Example:

```text
Equity crash stress loss = 16%
Stress loss warning threshold = 10%
Stress loss breach threshold = 15%
```

Status:

```text
Breach
```

RiskDNA explanation:

```text
The equity crash scenario produces a loss above the breach threshold, making stress testing a major risk driver.
```

Stress loss is important because it captures scenario-based risk that statistical metrics may miss.

---

## 38. Volatility contribution to RiskDNA

Volatility contribution measures the level of uncertainty in portfolio returns.

Example:

```text
Annualized volatility = 28%
Volatility regime = High
```

RiskDNA scoring can map regimes to scores:

```text
Low volatility = low score
Normal volatility = medium score
High volatility = high score
Crisis volatility = critical score
```

Explanation:

```text
The portfolio is currently in a high volatility regime, increasing uncertainty around short-term outcomes.
```

Volatility should not dominate the score alone, but it is a useful signal.

---

## 39. Concentration contribution to RiskDNA

Concentration contribution measures dependency on a small number of exposures.

Examples:

```text
Largest holding = 22%
Top 5 holdings = 68%
Technology exposure = 47%
USD exposure = 82%
```

RiskDNA should flag:

```text
Single-name concentration
Sector concentration
Currency concentration
Issuer concentration
Factor concentration
```

Example explanation:

```text
The portfolio is highly concentrated in technology, making it vulnerable to sector-specific shocks.
```

Concentration is often one of the clearest risk drivers for users.

---

## 40. Liquidity contribution to RiskDNA

Liquidity contribution measures how difficult it may be to trade or exit positions.

Examples:

```text
Low volume
Wide bid-ask spread
Large position relative to average volume
Stale price warning
Illiquid asset category
```

Example:

```text
Position size = 30% of average daily volume
Liquidity status = Warning
```

RiskDNA explanation:

```text
The position may be difficult to exit quickly without price impact.
```

Liquidity should receive higher importance during stress scenarios.

---

## 41. Limit breach contribution to RiskDNA

Limit breaches are strong risk signals.

Possible statuses:

```text
OK
Warning
Breach
Critical
```

Example:

```text
Single-name limit = 10%
Current largest position = 13%
Status = Breach
```

RiskDNA should strongly penalize breaches.

A breach can trigger a rule-based override:

```text
If any critical breach exists, Risk Level cannot be below High.
```

This prevents serious issues from being averaged away.

---

## 42. Data quality contribution to RiskDNA

Data quality affects trust in all calculations.

Examples of data quality problems:

```text
Missing prices
Stale market data
Invalid currency
Missing benchmark
Unresolved reconciliation break
Invalid volatility input
```

Example:

```text
Risk Score = Medium
Data quality = Critical
```

RiskDNA should warn:

```text
Risk metrics may be unreliable because critical input data is missing or stale.
```

Poor data quality may increase the score or reduce confidence in the score.

---

## 43. Risk driver identification

Risk driver identification explains which inputs caused the score.

A driver should include:

```text
Name
Category
Value
Threshold
Severity
Contribution
Explanation
Rank
```

Example:

```text
Driver: CVaR usage
Value: 94%
Threshold: 80% warning, 100% breach
Severity: High
Explanation: CVaR is close to the approved limit.
```

RiskDNA should identify drivers automatically from the scoring components.

---

## 44. Top risk drivers

Top risk drivers are the most important causes of the risk score.

Example:

```text
Top drivers:
1. CVaR usage = 94%
2. Technology exposure = 42%
3. Equity crash stress loss = 16%
4. Largest position = 18%
```

Top drivers help the user focus.

Without driver ranking, the user may not know what matters most.

### Athena UI

Use a table:

```text
Rank | Driver | Value | Threshold | Severity | Explanation
```

---

## 45. Positive risk drivers

Positive risk drivers reduce risk or support risk quality.

Examples:

```text
Good diversification
Strong liquidity
No limit breaches
Low stress loss
Clean data quality
Moderate volatility
High cash buffer
```

Example explanation:

```text
Liquidity is strong across major positions, reducing execution risk under normal market conditions.
```

Positive drivers are useful because risk reporting should not only be negative.

They explain why the score is not higher.

---

## 46. Negative risk drivers

Negative risk drivers increase risk.

Examples:

```text
High CVaR usage
Stress loss breach
High concentration
Liquidity warning
Data quality issue
Large drawdown
Limit breach
High volatility regime
```

Example explanation:

```text
The portfolio's downside risk is elevated because CVaR usage is near the limit and stress losses are above warning thresholds.
```

Negative drivers should be prioritized in the UI.

---

## 47. RiskDNA explanation structure

A good RiskDNA explanation should have a consistent structure.

Recommended structure:

```text
1. Overall risk level
2. Main reason for the score
3. Top risk drivers
4. Limit status
5. Data quality status
6. Suggested areas to review
```

Example:

```text
The portfolio is classified as High risk. The score is mainly driven by elevated CVaR usage, high technology concentration and a large equity crash stress loss. No critical data quality issues were detected, but risk limits are close to breach levels.
```

Consistency makes reports easier to read.

---

## 48. RiskDNA summary sentence

The summary sentence should be short and clear.

Example low risk:

```text
The portfolio currently shows a low risk profile with no major limit breaches and controlled stress losses.
```

Example medium risk:

```text
The portfolio shows moderate risk, mainly due to rising volatility and sector concentration.
```

Example high risk:

```text
The portfolio shows elevated downside risk driven by high CVaR usage and significant stress scenario losses.
```

Example critical risk:

```text
The portfolio is in a critical risk state because approved limits are breached and stress losses are severe.
```

---

## 49. RiskDNA detailed explanation

The detailed explanation expands the summary.

It should include:

```text
Risk level
Score
Quantitative drivers
Limit interpretation
Stress interpretation
Concentration interpretation
Data quality caveat
```

Example:

```text
The RiskDNA score is 74 / 100, classified as High. The main contributors are CVaR usage at 94% of limit, technology exposure at 42%, and a 16% loss under the equity crash scenario. These results indicate that the portfolio is particularly vulnerable to equity market stress and sector-specific shocks.
```

The explanation must use only available inputs.

---

## 50. RiskDNA recommendation logic

RiskDNA can suggest areas to review, but it should not make unsupported investment recommendations.

Allowed:

```text
Review concentration exposure.
Review CVaR limit usage.
Consider whether the stress loss is acceptable.
Investigate data quality warning.
Escalate critical breach according to governance process.
```

Avoid:

```text
Buy this stock.
Sell this asset immediately.
This trade is guaranteed to reduce risk.
```

RiskDNA recommendations should be framed as risk review prompts.

Example:

```text
Recommended review: assess whether technology concentration remains consistent with the portfolio's risk appetite.
```

---

## 51. RiskDNA confidence level

RiskDNA confidence should describe how reliable the score is based on input quality.

Possible confidence levels:

```text
High
Medium
Low
```

Example:

```text
RiskDNA Score: 68
Risk Level: High
Confidence: Low
Reason: Missing prices for two positions.
```

Confidence is different from risk level.

A portfolio can have:

```text
Low risk score but low confidence
```

if data quality is poor.

---

## 52. RiskDNA limitations

RiskDNA has limitations.

It depends on:

```text
Input data quality
Risk model assumptions
Chosen weights
Chosen thresholds
Available scenarios
Historical window
Portfolio coverage
```

RiskDNA does not predict the future with certainty.

It summarizes known and modeled risk signals.

Important statement:

```text
RiskDNA is a decision-support methodology, not a guarantee of future losses or outcomes.
```

This should be visible in methodology documentation.

---

## 53. AI layer overview

The AI layer helps explain and communicate risk results.

It should not calculate official risk metrics.

AI can help with:

```text
Plain-language explanations
Report drafting
Trade impact summaries
Anomaly explanations
Natural language Q&A over provided metrics
```

AI should receive structured inputs from deterministic engines.

Example:

```text
RiskDNA score
Top drivers
VaR
CVaR
Stress loss
Limit status
Data quality warnings
```

Then it can generate a clear explanation.

---

## 54. Why use AI in Athena?

AI is useful because risk outputs can be technical.

A user may not immediately understand:

```text
CVaR usage = 94%
Stress loss = 16%
Technology exposure = 42%
Limit status = Warning
```

AI can convert this into:

```text
The portfolio has elevated downside risk because tail losses are close to the approved limit and the portfolio is heavily exposed to technology.
```

AI improves usability and learning.

But the underlying numbers must come from deterministic calculations.

---

## 55. What AI should do

AI should:

```text
Explain calculated results
Summarize risk drivers
Draft reports
Translate technical metrics into clear language
Compare before/after trade impact using provided values
Identify which provided warnings matter most
Generate educational explanations
```

Example:

```text
Explain why CVaR is higher than VaR using the provided risk metrics.
```

AI can improve clarity, especially for users learning finance.

---

## 56. What AI should not do

AI should not:

```text
Invent risk numbers
Replace VaR calculation
Replace CVaR calculation
Override risk limits
Approve trades alone
Hide assumptions
Make unsupported recommendations
Use unavailable data
Pretend uncertainty does not exist
```

Wrong:

```text
The AI estimates the portfolio VaR is 10,000 without using the VaR engine.
```

Correct:

```text
The VaR engine calculates VaR = 10,000, and AI explains what that means.
```

---

## 57. AI as explanation assistant

AI can act as a risk explanation assistant.

Input:

```text
RiskDNA Score: 74
Risk Level: High
Top drivers:
- CVaR usage: 94%
- Technology exposure: 42%
- Stress loss: 16%
```

Output:

```text
The portfolio is classified as High risk mainly because tail risk is close to its limit and technology exposure is elevated. The equity crash scenario also indicates meaningful downside vulnerability.
```

The explanation should be concise and based only on provided metrics.

---

## 58. AI as report assistant

AI can draft reports from structured metrics.

Example report sections:

```text
Executive summary
Portfolio risk profile
Top risk drivers
Limit status
Stress testing results
Data quality notes
Recommended review points
```

The AI should not create numbers.

It should format and explain numbers already calculated by Athena.

### Athena workflow

```text
Risk engine calculates metrics
RiskDNA calculates score
AI drafts report
Human reviews report
Report is stored
```

---

## 59. AI as anomaly explanation assistant

An anomaly is an unusual change or result.

Examples:

```text
VaR increased by 40%
CVaR doubled
Stress loss suddenly increased
Data quality warning appeared
Technology exposure jumped
```

AI can help explain possible reasons based on provided data.

Example:

```text
VaR increased mainly because portfolio volatility rose and the NVDA position increased after the latest trade.
```

AI should avoid speculation beyond the provided inputs.

---

## 60. AI as natural language interface

AI can allow the user to ask questions in natural language.

Examples:

```text
Why is the portfolio high risk?
What changed after this trade?
Which position contributes most to stress loss?
Why did RiskDNA increase today?
```

The AI should answer using Athena's calculated data.

It should not browse, guess or invent portfolio values.

### Athena rule

Natural language answers should be grounded in structured portfolio and risk data.

---

## 61. AI and deterministic boundaries

Deterministic boundaries define what AI is allowed to do.

Allowed:

```text
Explain
Summarize
Compare provided values
Draft text
Identify provided drivers
```

Not allowed:

```text
Calculate official metrics
Invent missing data
Approve trades
Modify limits
Override deterministic checks
```

This boundary protects Athena from unreliable AI behavior.

Core rule:

```text
AI explains deterministic outputs. It does not replace them.
```

---

## 62. Prompt design for financial explanations

Prompts should be structured and restrictive.

A good prompt includes:

```text
Role
Inputs
Task
Constraints
Output format
Warnings
```

Example instruction:

```text
Use only the provided metrics.
Do not invent values.
Mention the top three risk drivers.
Mention any limit breach.
Use professional and concise language.
```

Prompt design is part of model governance.

Bad prompts create vague or unreliable outputs.

---

## 63. Risk explanation prompt structure

Recommended structure:

```text
System role:
You are a financial risk explanation assistant.

Inputs:
- Portfolio name
- RiskDNA score
- Risk level
- VaR and CVaR values
- Stress test results
- Limit status
- Top risk drivers
- Data quality warnings

Task:
Explain the portfolio risk profile clearly.

Constraints:
Use only provided inputs.
Do not invent metrics.
Do not give investment advice.
```

This keeps the AI explanation grounded.

---

## 64. Report generation prompt structure

Recommended structure:

```text
System role:
You draft professional risk reports from structured risk metrics.

Inputs:
- Portfolio summary
- RiskDNA score
- Risk metrics
- Stress scenarios
- Limit breaches
- Data quality status
- Methodology notes

Task:
Generate a structured report draft.

Constraints:
Do not create new calculations.
Mark output as draft.
Use only provided values.
```

AI-generated reports should require human review before final use.

---

## 65. Trade explanation prompt structure

Recommended structure:

```text
System role:
You explain pre-trade risk impact.

Inputs:
- Proposed trade
- Before metrics
- After metrics
- Limit checks
- Exposure changes
- Top changes

Task:
Explain how the trade changes portfolio risk.

Constraints:
Use only before/after values.
Do not approve or reject the trade by yourself.
Highlight warnings and breaches.
```

Example AI output:

```text
The proposed trade increases technology exposure from 32% to 38%, breaching the 35% sector limit. It also increases 1-day VaR by 1,200 CAD.
```

---

## 66. Anomaly explanation prompt structure

Recommended structure:

```text
System role:
You explain unusual changes in risk metrics.

Inputs:
- Previous metrics
- Current metrics
- Changes
- Portfolio trades
- Market changes
- Data quality warnings

Task:
Explain possible reasons for the anomaly based only on provided data.

Constraints:
Do not speculate beyond inputs.
Mention if data is insufficient.
```

Example:

```text
RiskDNA increased mainly because CVaR usage rose from 70% to 92% and the equity crash stress loss increased from 9% to 15%.
```

---

## 67. AI output validation

AI output validation checks whether the generated text is safe and grounded.

Validation checks:

```text
Does the output use only provided metrics?
Does it invent numbers?
Does it contradict deterministic results?
Does it hide limit breaches?
Does it make unsupported recommendations?
Does it mention required warnings?
```

If validation fails, Athena should:

```text
Reject output
Regenerate with stricter prompt
Ask for human review
Display fallback deterministic explanation
```

AI output should not be trusted blindly.

---

## 68. Hallucination risk

Hallucination risk is the risk that AI produces false or unsupported information.

Examples:

```text
Inventing a VaR value
Inventing a trade
Inventing a benchmark
Claiming a limit was approved
Saying risk is low despite a breach
```

Mitigation:

```text
Use structured inputs
Restrict prompts
Validate outputs
Store input snapshots
Require human review
Use deterministic fallback explanations
```

Athena should explicitly design against hallucination.

---

## 69. Model risk in AI

AI model risk is the risk that AI outputs are wrong, misleading, biased or used outside intended scope.

Examples:

```text
Overconfident explanation
Incorrect interpretation
Unsupported recommendation
Failure to mention data quality issue
Inconsistent tone
Poor handling of edge cases
```

AI should be treated as another model requiring governance.

Model risk principles apply to both quantitative models and AI models.

---

## 70. Data privacy and confidentiality

Risk explanations may involve sensitive portfolio data.

Data can include:

```text
Positions
Portfolio values
Trade ideas
Risk limits
Client information
Performance data
Reports
```

Athena should follow privacy principles:

```text
Use only necessary data
Avoid exposing confidential data
Control storage
Avoid unnecessary prompts with sensitive details
Respect access permissions
```

For a personal project, the principle still matters because it shows professional maturity.

---

## 71. Human review requirement

AI-generated explanations and reports should be reviewed before official use.

Possible review statuses:

```text
Draft
Reviewed
Approved
Rejected
Archived
```

Example:

```text
AI report draft generated
Human reviews
Human edits
Human approves
Report stored
```

This is especially important for:

```text
Reports
Limit breach explanations
Trade impact summaries
Client-facing text
```

Athena should label AI outputs as drafts unless reviewed.

---

## 72. AI governance principles

AI governance defines how AI is used safely.

Principles:

```text
Clear scope
Human oversight
Prompt versioning
Output validation
Audit trail
Data protection
Model version tracking
Fallback behavior
No unsupported advice
```

Example governance rule:

```text
AI may explain calculated risk metrics but may not approve trades or change risk limits.
```

Governance makes the AI layer credible.

---

## 73. Explainable AI principles

Explainable AI means users can understand why the AI produced an explanation.

For Athena, explainability should come from structured inputs.

AI explanations should reference:

```text
RiskDNA score
Top drivers
Limit status
Stress results
Data quality status
Methodology notes
```

Example:

```text
The explanation identifies CVaR usage and sector concentration because these were the two highest-ranked RiskDNA drivers.
```

The AI should not produce vague statements without evidence.

---

## 74. RiskDNA audit trail

RiskDNA should create audit trail events.

Examples:

```text
RiskDNA score calculated
RiskDNA methodology version changed
AI explanation generated
AI explanation reviewed
Risk report generated
Risk driver overridden
Prompt version updated
```

Audit event fields:

```text
event_id
event_type
entity_id
performed_by
timestamp
details
```

Audit trail supports governance and reproducibility.

---

## 75. Versioning the scoring model

The RiskDNA scoring model should be versioned.

Example:

```text
riskdna_methodology_version = "v1.0"
```

If weights or thresholds change, create a new version.

Example:

```text
v1.0 = initial scoring
v1.1 = adjusted concentration thresholds
v2.0 = added liquidity score
```

Why versioning matters:

```text
A score of 70 under v1.0 may not mean the same thing as 70 under v2.0.
```

---

## 76. Versioning prompts

Prompt templates should be versioned.

Example:

```text
risk-summary-prompt-v1
trade-impact-prompt-v1
report-draft-prompt-v2
```

Prompt version should be stored with each AI explanation.

Example:

```text
prompt_version = "risk-summary-v1"
model_version = "ai-risk-explainer-v1"
```

This helps explain why two outputs may differ.

---

## 77. Storing AI explanations

AI explanations should be stored when they are used in reports, decisions or reviews.

Fields:

```text
explanation_id
portfolio_id
riskdna_score_id
input_snapshot_id
prompt_version
model_version
content
review_status
created_at
reviewed_by
```

Storing explanations supports:

```text
Traceability
Review
Audit
Reproducibility
Report history
```

Temporary UI explanations may not need long-term storage, but official reports should be stored.

---

## 78. Reproducibility of AI-assisted reports

AI-assisted reports are harder to reproduce than deterministic calculations.

To improve reproducibility, store:

```text
Input snapshot
Prompt version
Model version
Generated output
Review status
Final edited report
```

If exact reproduction is not possible, Athena should still preserve the exact generated output.

Important distinction:

```text
Deterministic score should be reproducible.
AI text should be stored and traceable.
```

This is a professional design choice.

---

## 79. RiskDNA dashboard

The RiskDNA dashboard is the main interface for understanding the portfolio risk profile.

It should show:

```text
RiskDNA score
Risk level
Top drivers
Trend over time
Limit status
Data quality status
AI explanation
Recommended review areas
```

The dashboard should answer:

```text
How risky is the portfolio?
Why?
What changed?
What should be reviewed?
```

Athena's dashboard should be clear and not overloaded.

---

## 80. RiskDNA card

A RiskDNA card is a compact summary component.

Example:

```text
RiskDNA Score: 74 / 100
Risk Level: High
Confidence: Medium
Top Driver: CVaR usage
Status: Warning
```

Card elements:

```text
Score
Badge
Short explanation
Trend arrow
Confidence indicator
```

The card should be visible on the main dashboard.

---

## 81. RiskDNA driver table

The driver table explains the score.

Columns:

```text
Rank
Driver
Category
Value
Threshold
Severity
Contribution
Explanation
```

Example row:

```text
1 | CVaR usage | Tail risk | 94% | 80% warning | High | 22 pts | CVaR is close to limit
```

This table is one of the most important components because it turns the score into a transparent explanation.

---

## 82. RiskDNA timeline

The RiskDNA timeline shows how the score changes over time.

Example:

```text
2026-04-01: Score 42, Medium
2026-04-08: Score 51, Medium
2026-04-15: Score 68, High
2026-04-29: Score 74, High
```

Useful questions:

```text
Why did the score increase?
Which driver changed?
Was it due to a trade or market movement?
```

Timeline view helps detect risk deterioration.

---

## 83. RiskDNA before/after trade view

Before/after trade view shows how a proposed trade changes RiskDNA.

Example:

```text
Before trade:
RiskDNA Score = 58
Risk Level = Medium

After trade:
RiskDNA Score = 72
Risk Level = High
```

Driver changes:

```text
Technology exposure +6%
VaR usage +8%
Stress loss +4%
```

This view helps the front office understand risk impact before execution.

---

## 84. RiskDNA stress scenario view

RiskDNA should connect to stress testing.

Example:

```text
Scenario: Equity crash
Stress loss: 16%
RiskDNA contribution: High
```

The stress scenario view can show:

```text
Scenario loss
Worst contributors
Limit status
Driver contribution
AI explanation
```

This makes stress testing easier to interpret.

---

## 85. RiskDNA alerting

RiskDNA alerts notify the user when risk changes materially.

Example alert triggers:

```text
RiskDNA score increases by more than 10 points
Risk level changes from Medium to High
Critical limit breach appears
Data quality becomes Critical
Stress loss exceeds threshold
```

Example alert:

```text
RiskDNA increased from 59 to 74 after the proposed trade. Main driver: technology concentration.
```

Alerts should be actionable, not noisy.

---

## 86. RiskDNA in the trade simulator

The Trade Simulator should use RiskDNA to show risk impact.

Workflow:

```text
1. User enters proposed trade.
2. Athena simulates portfolio after trade.
3. Risk metrics are recalculated.
4. RiskDNA is recalculated before and after.
5. Driver changes are identified.
6. AI explains the trade impact.
```

Example:

```text
This trade increases the RiskDNA score from 61 to 78, mainly due to higher sector concentration and increased CVaR usage.
```

This is a strong Athena feature.

---

## 87. RiskDNA in the risk dashboard

The Risk Dashboard should use RiskDNA as the summary layer.

Dashboard structure:

```text
Top: RiskDNA score and risk level
Middle: VaR, CVaR, stress loss, volatility
Bottom: top drivers, limit status, explanations
```

RiskDNA should not hide detailed metrics.

It should summarize them and link to them.

Example:

```text
Click CVaR driver → open CVaR details
Click stress loss driver → open stress scenario
```

---

## 88. RiskDNA in reports

RiskDNA should appear in reports as a clear summary.

Report section example:

```text
RiskDNA Summary
Score: 74 / 100
Risk Level: High
Top Drivers:
1. CVaR usage
2. Technology concentration
3. Equity crash stress loss
```

AI can draft the narrative:

```text
The portfolio's risk profile is classified as High, mainly due to elevated tail risk and sector concentration.
```

The report should include methodology version.

---

## 89. RiskDNA in portfolio monitoring

RiskDNA can support ongoing portfolio monitoring.

Monitoring questions:

```text
Is risk increasing?
Which driver is changing?
Did a trade cause the increase?
Did market volatility cause the increase?
Are limits near breach?
Is data quality reliable?
```

Example:

```text
RiskDNA has increased for three consecutive weeks due to rising volatility and concentration.
```

This helps identify risk trends before a crisis.

---

## 90. Data required for RiskDNA

RiskDNA requires structured data.

### RiskDNAScore

```text
id
portfolio_id
valuation_date
score
risk_level
confidence_level
methodology_version
created_at
```

### RiskDNADriver

```text
id
riskdna_score_id
driver_name
driver_category
value
threshold
severity
contribution
explanation
rank
```

### RiskDNAInputSnapshot

```text
id
portfolio_id
valuation_date
var_value
cvar_value
stress_loss
volatility_regime
concentration_metrics
liquidity_status
limit_status
data_quality_status
created_at
```

### AIExplanation

```text
id
portfolio_id
riskdna_score_id
explanation_type
input_snapshot_id
prompt_version
model_version
content
review_status
created_at
```

### PromptTemplate

```text
id
name
version
template_text
created_at
is_active
```

---

## 91. Common beginner mistakes

### Mistake 1 — Letting AI calculate risk numbers

Risk numbers should come from deterministic models.

### Mistake 2 — Creating a score without explaining it

A score without drivers is not useful.

### Mistake 3 — Ignoring model versioning

Scores are hard to compare if methodology changes without version tracking.

### Mistake 4 — Ignoring data quality

Poor input data makes risk scores unreliable.

### Mistake 5 — Overweighting one metric

A score based only on VaR misses other dimensions of risk.

### Mistake 6 — Hiding limit breaches in an average score

Critical breaches should not be averaged away.

### Mistake 7 — Treating AI text as final without review

AI-generated reports should be reviewed.

### Mistake 8 — Forgetting audit trail

Risk explanations and scores should be traceable.

### Mistake 9 — Making recommendations too strong

RiskDNA should suggest review areas, not unsupported trades.

### Mistake 10 — Making the methodology too complex too early

Start simple, deterministic and explainable.

---

## 92. Key formulas and scoring logic

### Limit usage

```text
Limit usage = Current value / Limit value
```

### Weighted RiskDNA score

```text
RiskDNA Score =
w1 × VaRScore
+ w2 × CVaRScore
+ w3 × StressScore
+ w4 × ConcentrationScore
+ w5 × VolatilityScore
+ w6 × LiquidityScore
+ w7 × BreachScore
+ w8 × DataQualityScore
```

### Example weights

```text
VaRScore:             20%
CVaRScore:            20%
StressScore:          20%
ConcentrationScore:   15%
VolatilityScore:      10%
LiquidityScore:        5%
BreachScore:           5%
DataQualityScore:      5%
```

### Risk level mapping

```text
0–30   = Low
31–60  = Medium
61–80  = High
81–100 = Critical
```

### Override rule example

```text
If any critical breach exists, final risk level cannot be below High.
```

---

## 93. Possible API endpoints

Possible Athena API endpoints:

```text
GET  /api/riskdna/{portfolio_id}/latest
POST /api/riskdna/{portfolio_id}/calculate
GET  /api/riskdna/{portfolio_id}/drivers
GET  /api/riskdna/{portfolio_id}/timeline
POST /api/riskdna/{portfolio_id}/before-after-trade
GET  /api/riskdna/{portfolio_id}/methodology

POST /api/ai/risk-explanation
POST /api/ai/report-draft
POST /api/ai/trade-impact-explanation
POST /api/ai/anomaly-explanation
GET  /api/ai/explanations/{explanation_id}

GET  /api/prompts
POST /api/prompts
PUT  /api/prompts/{prompt_id}
GET  /api/prompts/{prompt_id}/versions
```

### Example RiskDNA response

```json
{
  "portfolio_id": "pf_001",
  "valuation_date": "2026-04-29",
  "score": 74,
  "risk_level": "High",
  "confidence": "Medium",
  "methodology_version": "riskdna-v1.0",
  "top_drivers": [
    {
      "rank": 1,
      "name": "CVaR usage",
      "value": 0.94,
      "severity": "High",
      "explanation": "CVaR is close to the approved limit."
    }
  ]
}
```

---

## 94. Possible frontend components

Possible Athena frontend components:

```text
RiskDNACard
RiskDNAScoreGauge
RiskLevelBadge
RiskConfidenceBadge
RiskDriverTable
RiskDNAExplanationPanel
RiskDNATimeline
BeforeAfterRiskDNAPanel
RiskDNAStressScenarioView
AIReportDraftPanel
AIExplanationReviewBox
PromptVersionBadge
MethodologyVersionBadge
AIOutputValidationWarning
```

### Page ideas

```text
RiskDNA Dashboard
RiskDNA Methodology Page
AI Explanation Review Page
Before/After Trade RiskDNA View
RiskDNA Timeline Page
```

### UI goal

The user should immediately understand:

```text
How risky is the portfolio?
Why is it risky?
What changed?
Can the explanation be trusted?
Which model and prompt versions were used?
```

---

## 95. Suggested tests

### Scoring tests

```text
RiskDNA score is between 0 and 100.
Risk level matches score range.
High VaR usage increases score.
High CVaR usage increases score.
High stress loss increases score.
Limit breach increases score.
Data quality warning increases score.
Critical breach applies override rule.
```

### Driver tests

```text
Top drivers are ranked correctly.
Driver contribution sums approximately to total score.
Driver severity matches thresholds.
Positive and negative drivers are classified correctly.
```

### Reproducibility tests

```text
Same input snapshot and methodology version produce same score.
Methodology version is stored with score.
Input snapshot is stored with score.
```

### AI tests

```text
AI explanation uses only provided inputs.
AI explanation does not invent metrics.
AI explanation mentions critical breaches.
AI explanation includes top drivers.
Prompt version is stored with explanation.
Model version is stored with explanation.
Review status defaults to draft.
```

### API tests

```text
Latest RiskDNA endpoint returns most recent score.
Timeline endpoint returns ordered scores.
Before/after endpoint returns both scores and driver changes.
```

---

## 96. How Athena uses RiskDNA

Athena uses RiskDNA as the explanatory layer connecting all risk modules.

### Risk Monitor

RiskDNA summarizes the current portfolio risk state.

### Trade Simulator

RiskDNA compares before-trade and after-trade risk.

### Stress Testing

RiskDNA highlights which scenarios drive portfolio vulnerability.

### Limit Center

RiskDNA incorporates warning, breach and critical statuses.

### Reports Center

RiskDNA provides the executive risk summary.

### AI Layer

AI explains RiskDNA outputs in clear language.

### Example workflow

```text
1. Portfolio metrics are calculated.
2. Risk metrics are calculated.
3. Stress tests are run.
4. Limits are checked.
5. RiskDNA calculates score and drivers.
6. AI drafts an explanation using only structured outputs.
7. User reviews the explanation.
8. Report or dashboard displays the result.
```

---

## 97. Future improvements

Future improvements can include:

```text
Machine learning anomaly detection
RiskDNA trend prediction
Scenario clustering
Natural language portfolio Q&A
Automated driver attribution
Custom risk appetite profiles
User-defined scoring weights
Advanced liquidity risk inputs
Option portfolio Greeks aggregation
Model validation dashboard
```

Important caution:

Future improvements should preserve:

```text
Explainability
Auditability
Human control
Deterministic core calculations
```

Do not make RiskDNA more complex if it becomes less understandable.

---

## 98. Ethical considerations

Risk systems can influence decisions.

Ethical considerations include:

```text
Avoid false certainty
Avoid hiding assumptions
Avoid unsupported recommendations
Avoid biased explanations
Protect confidential data
Keep humans in control
Clearly label AI-generated content
Escalate critical risks honestly
```

Athena should not pretend to know more than the data supports.

Good risk technology should make uncertainty clearer, not hide it.

---

## 99. Final methodology summary

RiskDNA is Athena's methodology for turning calculated risk metrics into an explainable risk profile.

Core architecture:

```text
Deterministic calculations
        ↓
RiskDNA scoring
        ↓
Risk driver ranking
        ↓
AI-assisted explanation
        ↓
Human review
        ↓
Report or dashboard
```

Core rule:

```text
AI explains.
It does not calculate official risk metrics.
```

Core value:

```text
RiskDNA makes risk understandable, traceable and actionable.
```

---

## 100. Summary

RiskDNA is not a magic AI score.

It is a structured methodology for summarizing risk.

The strongest version of RiskDNA is:

```text
Deterministic
Explainable
Transparent
Auditable
Versioned
Human-reviewed
AI-assisted but not AI-controlled
```

For Athena AI Risk Terminal, RiskDNA connects:

```text
Market risk
Portfolio risk
Fixed income risk
Options risk
Stress testing
Liquidity
Concentration
Limit monitoring
Data quality
Reporting
AI explanations
```

The key lesson is:

```text
Athena does not use AI to guess risk.
Athena uses quantitative models to calculate risk, then uses AI to explain it clearly.
```

That is what makes RiskDNA credible, professional and useful.
