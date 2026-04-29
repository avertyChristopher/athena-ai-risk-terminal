# 06 — Front Office, Middle Office and Risk Workflow

**Project:** Athena AI Risk Terminal  
**Recommended file path:** `docs/finance/06-front-office-middle-office-risk-workflow.md`  
**Purpose:** understand how investment decisions, trades, risk controls, operational checks, governance, reporting and audit workflows interact inside an institutional finance environment.  
**Scope:** this document focuses on the professional workflow connecting front office decisions to middle office controls and back office operations. It does not repeat the detailed mathematical content covered in previous finance documents.

---

## Table of Contents

1. What is the front office?
2. What is the middle office?
3. What is the back office?
4. Why the separation of roles matters
5. Investment decision lifecycle
6. Trade idea generation
7. Portfolio manager role
8. Trader role
9. Analyst role
10. Risk manager role
11. Operations role
12. Compliance role
13. Front office objectives
14. Middle office objectives
15. Back office objectives
16. From investment idea to trade
17. Trade ticket
18. Order creation
19. Pre-trade checks
20. Pre-trade risk analysis
21. Pre-trade compliance checks
22. Liquidity check
23. Concentration check
24. Limit check
25. Trade approval workflow
26. Order execution
27. Execution quality
28. Slippage
29. Transaction costs
30. Post-trade processing
31. Trade confirmation
32. Trade settlement
33. Position update
34. Cash update
35. Portfolio update
36. Market data update
37. Position reconciliation
38. Cash reconciliation
39. Trade reconciliation
40. Exception management
41. Breaks and mismatches
42. Middle office control workflow
43. Daily risk calculation
44. Daily P&L calculation
45. Daily exposure calculation
46. Limit monitoring
47. Breach detection
48. Breach escalation
49. Risk appetite framework
50. Risk limits framework
51. Front office vs risk management tension
52. Independent risk control
53. First line of defense
54. Second line of defense
55. Third line of defense
56. Governance and accountability
57. Audit trail
58. Model validation
59. Data validation
60. Report validation
61. Risk dashboard workflow
62. Portfolio dashboard workflow
63. Trade simulator workflow
64. Stress testing workflow
65. Scenario approval workflow
66. Performance monitoring workflow
67. Benchmark monitoring workflow
68. Client reporting workflow
69. Management reporting workflow
70. Regulatory reporting intuition
71. Communication between teams
72. Key daily processes
73. Key weekly processes
74. Key monthly processes
75. Common front office tools
76. Common middle office tools
77. Common back office tools
78. Common workflow failures
79. Operational risk in workflows
80. Controls and checks
81. Maker-checker principle
82. Segregation of duties
83. Data required for workflow management
84. Common beginner mistakes
85. Key workflow concepts
86. Possible API endpoints
87. Possible frontend components
88. Suggested tests
89. How Athena uses front office and middle office workflows
90. Summary

---

## 1. What is the front office?

The front office is the part of a financial institution that is directly involved in investment decisions, trading decisions, client-facing activity and revenue generation.

Typical front office functions include:

```text
Portfolio management
Trading
Sales
Investment research
Client advisory
Structuring
Origination
```

Simple definition:

```text
Front office = decision-making, trading, revenue generation and client-facing activity.
```

Examples:

```text
A portfolio manager decides to increase exposure to technology stocks.
A trader executes a buy order.
A private banker advises a client on portfolio allocation.
A structurer designs a financial product for a client.
```

The front office is not only about taking risk. It is about taking intentional risk to achieve an investment or business objective.

### Athena link

In Athena AI Risk Terminal, the front office side appears through:

```text
Portfolio Builder
Trade Simulator
Investment idea input
Scenario impact preview
Before/after trade analysis
```

Athena should help simulate what happens when the front office proposes a decision.

---

## 2. What is the middle office?

The middle office supports, controls and monitors the risk and performance of front office activity.

Typical middle office functions include:

```text
Risk management
Performance analysis
P&L control
Limit monitoring
Trade validation
Exposure monitoring
Stress testing
Reporting
Data quality controls
Model oversight
```

Simple definition:

```text
Middle office = risk control, performance control, limit monitoring and reporting.
```

Example:

```text
The front office proposes a trade.
The middle office checks whether the trade increases VaR beyond the approved limit.
```

The middle office is not supposed to block every risk. Its role is to make risk visible, controlled and aligned with risk appetite.

### Athena link

In Athena, the middle office side appears through:

```text
Risk Monitor
VaR / CVaR
Stress testing
Limit Center
Risk contribution
P&L controls
Reports Center
RiskDNA explanations
```

Athena should connect front office decisions to middle office controls.

---

## 3. What is the back office?

The back office handles operational processing, settlement, confirmation and recordkeeping after trades are executed.

Typical back office functions include:

```text
Trade confirmation
Trade settlement
Cash settlement
Position records
Custody
Accounting support
Reconciliation
Corporate actions processing
Operational records
```

Simple definition:

```text
Back office = settlement, confirmation, records and operational processing.
```

Example:

```text
A trade is executed by the front office.
The back office confirms the trade details, ensures cash and securities settle correctly, and updates records.
```

The back office is essential because a trade is not complete just because it was decided or executed. It must also be correctly settled and recorded.

### Athena link

Athena is mainly a front office / middle office learning terminal, but it can simulate some back office ideas through:

```text
Trade status
Position update
Cash update
Reconciliation checks
Audit trail
```

---

## 4. Why the separation of roles matters

The separation between front office, middle office and back office exists to reduce conflicts of interest and operational risk.

Simple separation:

```text
Front office = proposes and executes risk
Middle office = measures and controls risk
Back office = confirms and records transactions
```

If the same person or team controls everything, problems can happen:

```text
A trader could hide losses.
A portfolio manager could ignore risk limits.
A trade could be incorrectly recorded.
A report could be manipulated.
An error could go undetected.
```

Separation creates checks and balances.

### Example

```text
Front office wants to buy 10,000 shares.
Middle office checks concentration and risk limits.
Back office confirms the trade and updates records.
```

Each function protects the institution in a different way.

### Athena link

Athena should reflect this separation conceptually:

```text
Trade Simulator = front office decision simulation
Risk Monitor = middle office control
Reports / audit trail = governance and documentation
```

---

## 5. Investment decision lifecycle

An investment decision usually follows a lifecycle.

Simplified lifecycle:

```text
1. Investment idea
2. Research and analysis
3. Portfolio fit assessment
4. Trade simulation
5. Pre-trade risk check
6. Compliance check
7. Approval if required
8. Execution
9. Confirmation
10. Settlement
11. Position update
12. Monitoring
13. Reporting
```

This lifecycle turns an idea into a controlled portfolio action.

### Example

```text
Idea: Increase exposure to AAPL.
Analysis: AAPL has strong earnings momentum.
Simulation: Buying AAPL increases technology exposure from 28% to 34%.
Risk check: VaR increases by 3%.
Limit check: Technology exposure remains below 35% limit.
Decision: Trade approved.
```

### Athena link

Athena should make this lifecycle visible, especially the transition from:

```text
trade idea → simulated impact → risk check → decision support
```

---

## 6. Trade idea generation

Trade idea generation is the process of identifying a potential investment action.

Sources of trade ideas:

```text
Fundamental analysis
Quantitative signals
Macroeconomic views
Client needs
Portfolio rebalancing
Risk reduction
Benchmark alignment
Valuation opportunity
Technical indicators
News and events
```

Examples:

```text
Buy an undervalued stock.
Reduce exposure to a sector.
Hedge currency exposure.
Increase cash before a risky event.
Rebalance back to target allocation.
```

A trade idea is not yet a trade. It must be checked.

### Athena link

Athena can represent a trade idea as a draft trade ticket.

Example:

```text
Buy 50 shares of MSFT
Estimated price = 420
Portfolio = Growth Portfolio
Reason = increase high-quality technology exposure
```

---

## 7. Portfolio manager role

A portfolio manager is responsible for managing a portfolio according to its objectives and constraints.

Responsibilities include:

```text
Asset allocation
Security selection
Risk budgeting
Portfolio construction
Rebalancing
Performance review
Client or mandate alignment
Investment decision-making
```

The portfolio manager asks:

```text
What should the portfolio own?
How much should it own?
What risk is acceptable?
How does this decision affect the portfolio?
```

### Example

A portfolio manager may decide:

```text
Reduce technology exposure from 40% to 32%.
Increase healthcare exposure from 10% to 15%.
Keep cash above 5%.
```

### Athena link

The Portfolio Builder and Trade Simulator should support the portfolio manager's decision process.

---

## 8. Trader role

A trader is responsible for executing orders in the market.

The trader focuses on:

```text
Execution price
Market liquidity
Timing
Order type
Transaction cost
Slippage
Market impact
Execution quality
```

The trader asks:

```text
How should this order be executed?
Can the market absorb the trade?
What is the expected cost?
What order type should be used?
```

### Example

A portfolio manager wants to buy 20,000 shares.

The trader may decide not to send one large market order immediately because it could move the price.

Instead, the trader may split the order.

### Athena link

Athena does not need full execution algorithms in the first version, but it should understand:

```text
estimated price
order type
slippage assumption
transaction cost assumption
```

---

## 9. Analyst role

An analyst supports investment decisions through research and analysis.

Analysts can be:

```text
Equity analysts
Credit analysts
Quant analysts
Risk analysts
Macro analysts
Fund analysts
```

They may analyze:

```text
Company fundamentals
Valuation
Earnings
Macroeconomic trends
Risk factors
Quantitative signals
Credit quality
Sector trends
```

### Example

An analyst writes:

```text
The company has strong revenue growth, but valuation is high and downside risk has increased.
```

### Athena link

Athena can later include an AI explanation panel that summarizes risk and portfolio impact, but deterministic calculations should remain separate from AI summaries.

---

## 10. Risk manager role

A risk manager monitors and controls portfolio risk.

Responsibilities include:

```text
Measuring VaR and CVaR
Running stress tests
Monitoring limits
Investigating breaches
Reviewing concentration
Validating assumptions
Producing risk reports
Escalating issues
```

The risk manager asks:

```text
Is this risk acceptable?
Which positions create the risk?
Are limits being breached?
What happens under stress?
Are model assumptions reasonable?
```

### Example

A risk manager may say:

```text
This trade increases technology concentration above the approved limit. It should be reviewed before execution.
```

### Athena link

Athena's Risk Monitor and Limit Center represent the risk manager's perspective.

---

## 11. Operations role

Operations teams make sure trades, positions and cash movements are processed correctly.

Responsibilities include:

```text
Trade confirmation
Settlement support
Cash processing
Position records
Reconciliation
Corporate actions
Exception management
Operational controls
```

Operations asks:

```text
Did the trade settle?
Are positions correct?
Does cash match expected records?
Are there any breaks?
```

### Example

Expected position:

```text
100 shares
```

Actual custodian position:

```text
95 shares
```

This creates a reconciliation break.

### Athena link

Athena can simulate operational quality using reconciliation checks and audit trail events.

---

## 12. Compliance role

Compliance ensures that activity follows laws, regulations, internal policies and client mandates.

Compliance checks can include:

```text
Restricted securities
Client suitability
Regulatory rules
Mandate constraints
Insider trading policies
Concentration restrictions
ESG restrictions if applicable
Personal trading rules
```

### Example

A portfolio mandate may say:

```text
No single equity position above 10%.
No investment in restricted securities.
```

If a proposed trade violates those rules, it should be blocked or escalated.

### Athena link

Athena can include simplified pre-trade compliance checks:

```text
max position weight
max sector exposure
allowed asset types
restricted symbols
```

---

## 13. Front office objectives

Front office objectives usually include:

```text
Generating return
Serving clients
Executing investment strategy
Finding opportunities
Managing portfolio positioning
Implementing tactical views
Improving performance
```

The front office is judged by:

```text
Performance
Client satisfaction
Execution quality
Revenue generation
Strategy implementation
```

### Important

Front office objectives are not bad or reckless. They are necessary.

The issue is that return-seeking activity must be controlled.

### Athena link

Athena should help the front office understand the risk impact of its decisions before they become real trades.

---

## 14. Middle office objectives

Middle office objectives usually include:

```text
Measuring risk
Monitoring limits
Explaining P&L
Validating exposures
Supporting reporting
Escalating breaches
Ensuring data consistency
Supporting governance
```

The middle office is judged by:

```text
Accuracy
Timeliness
Independence
Control quality
Clear reporting
Escalation discipline
```

### Example

The middle office may not decide whether a portfolio should own AAPL. But it can say:

```text
After this trade, AAPL becomes 18% of the portfolio, above the 10% single-name limit.
```

### Athena link

Athena should display risk and limit results in a clear, decision-ready way.

---

## 15. Back office objectives

Back office objectives usually include:

```text
Correct settlement
Accurate records
Cash processing
Trade confirmation
Operational reliability
Reconciliation
Exception resolution
Audit support
```

The back office is judged by:

```text
Accuracy
Completeness
Timeliness
Low error rate
Operational control
```

### Example

If a trade is executed but not settled properly, the portfolio records may be wrong.

This can affect:

```text
Portfolio value
Cash balance
Risk calculations
P&L
Client reporting
```

### Athena link

Athena's first version can keep back office simple, but it should include the idea that records and positions must be consistent.

---

## 16. From investment idea to trade

A trade starts as an idea.

Example:

```text
Increase exposure to MSFT by buying 25 shares.
```

Before execution, the idea should become a structured trade ticket.

Workflow:

```text
Investment idea
      ↓
Trade ticket
      ↓
Pre-trade checks
      ↓
Approval if needed
      ↓
Execution
      ↓
Post-trade update
```

### Why structure matters

A structured trade ticket avoids ambiguity.

Bad:

```text
Buy some Microsoft.
```

Better:

```text
Buy 25 shares of MSFT at estimated price 420 USD for Growth Portfolio.
```

### Athena link

Athena should force trade ideas into structured data.

---

## 17. Trade ticket

A trade ticket is a structured record of a proposed or executed trade.

Typical fields:

```text
Portfolio
Asset
Side
Quantity
Order type
Estimated price
Estimated notional
Currency
Trade reason
Created by
Status
Timestamp
```

Example:

```text
Portfolio: Growth Portfolio
Asset: MSFT
Side: Buy
Quantity: 25
Estimated price: 420
Estimated notional: 10,500
Currency: USD
Status: Draft
```

### Trade status

Possible statuses:

```text
Draft
Simulated
Pending approval
Approved
Rejected
Executed
Cancelled
Settled
```

### Athena link

The Trade Simulator should create simulated trade tickets before any portfolio mutation.

---

## 18. Order creation

An order is an instruction to buy or sell an asset.

Common order fields:

```text
Symbol
Side
Quantity
Order type
Limit price if any
Time in force
Portfolio
Account
```

Order types can include:

```text
Market order
Limit order
Stop order
Stop-limit order
```

### Example

```text
Buy 100 AAPL market order
```

or:

```text
Buy 100 AAPL limit 195
```

### Athena first version

Athena does not need full order routing. It can model order creation conceptually through trade tickets.

---

## 19. Pre-trade checks

Pre-trade checks happen before a trade is executed.

They help determine whether the proposed trade is acceptable.

Pre-trade checks can include:

```text
Position limit check
Sector exposure check
Cash availability check
Liquidity check
Concentration check
Risk limit check
Compliance restriction check
Currency exposure check
```

### Example

Proposed trade:

```text
Buy 100 shares of NVDA
```

Pre-trade checks:

```text
Does cash allow this trade?
Will NVDA exceed single-name limit?
Will technology exposure exceed sector limit?
Will VaR exceed approved limit?
```

### Athena link

Pre-trade checks are one of the most important workflows in Athena.

---

## 20. Pre-trade risk analysis

Pre-trade risk analysis estimates how the portfolio risk changes if a proposed trade is executed.

It compares:

```text
Before trade
After simulated trade
```

Metrics can include:

```text
Portfolio value
Weights
Volatility
VaR
CVaR
Stress loss
Concentration
Sector exposure
Currency exposure
Limit usage
```

### Example

```text
Before trade VaR = 10,000
After trade VaR = 12,500
Change = +2,500
```

This tells the user that the trade increases downside risk.

### Athena link

The Trade Simulator should show before/after risk impact.

---

## 21. Pre-trade compliance checks

Pre-trade compliance checks verify whether the proposed trade respects rules and restrictions.

Examples:

```text
Restricted security list
Maximum single-name exposure
Maximum sector exposure
Minimum cash requirement
Allowed asset types
Client mandate constraints
No short selling rule
```

### Example

Rule:

```text
Maximum single asset weight = 10%
```

Trade result:

```text
AAPL after trade weight = 13%
```

Status:

```text
Breach
```

### Athena link

Athena can start with simple rules:

```text
max asset weight
max sector exposure
min cash
allowed asset types
```

---

## 22. Liquidity check

A liquidity check estimates whether the trade can be executed without excessive cost or market impact.

Inputs:

```text
Trade size
Average volume
Bid-ask spread
Asset liquidity category
Position size
```

### Simple rule example

```text
Trade notional should not exceed 10% of average daily volume.
```

Example:

```text
Trade notional = 500,000
Average daily volume notional = 2,000,000

Trade / ADV = 25%
Status = Warning
```

### Athena first version

Athena can use simplified liquidity warnings based on volume and trade size.

---

## 23. Concentration check

A concentration check verifies whether the trade creates excessive exposure to one asset, sector, country, currency or factor.

Examples:

```text
Single asset exposure
Top 5 holdings exposure
Sector exposure
Currency exposure
Country exposure
```

### Example

Before trade:

```text
Technology exposure = 32%
```

After trade:

```text
Technology exposure = 41%
```

Limit:

```text
Maximum technology exposure = 35%
```

Status:

```text
Breach
```

### Athena link

This should be part of the pre-trade check panel.

---

## 24. Limit check

A limit check compares a risk or exposure metric to an approved limit.

Formula:

```text
Limit usage = Current value / Limit value
```

Example:

```text
Current VaR = 48,000
VaR limit = 50,000

Limit usage = 96%
Status = Warning
```

Possible statuses:

```text
OK
Warning
Breach
Critical
```

### Athena link

Limit checks should be standardized so many controls use the same logic.

---

## 25. Trade approval workflow

Some trades require approval before execution.

Approval may be required when:

```text
Risk limit is near breach
Trade size is large
Asset is restricted
Portfolio mandate is affected
Liquidity warning appears
Stress loss increases too much
```

Workflow:

```text
Draft trade
      ↓
Pre-trade checks
      ↓
Pending approval
      ↓
Approved or rejected
      ↓
Execution or cancellation
```

### Athena link

Athena can model approval status even if it does not implement real user permissions at first.

---

## 26. Order execution

Order execution is the process of sending an order to the market and completing the trade.

Execution details include:

```text
Executed price
Executed quantity
Execution time
Broker or venue
Fees
Slippage
Partial fills
```

### Example

Order:

```text
Buy 100 shares at estimated price 50
```

Execution:

```text
Executed 100 shares at 50.20
```

The difference creates slippage.

### Athena first version

Athena can simulate execution using estimated price and optional slippage.

---

## 27. Execution quality

Execution quality measures how well a trade was executed.

Factors:

```text
Price improvement
Slippage
Market impact
Speed
Fill rate
Transaction costs
Benchmark price comparison
```

### Example

Expected price:

```text
100.00
```

Executed price:

```text
100.30
```

For a buy order, this is worse than expected.

### Athena link

Athena can later compare estimated price vs simulated executed price.

---

## 28. Slippage

Slippage is the difference between expected execution price and actual execution price.

For a buy order:

```text
Slippage = Executed price - Expected price
```

Example:

```text
Expected price = 100
Executed price = 100.50

Slippage = 0.50
```

For 1,000 shares:

```text
Total slippage cost = 0.50 × 1,000 = 500
```

### Why slippage matters

Slippage reduces realized performance.

High slippage can make a strategy look good in theory but poor in practice.

---

## 29. Transaction costs

Transaction costs are costs associated with trading.

Examples:

```text
Commissions
Bid-ask spread
Slippage
Market impact
Taxes
Exchange fees
Borrow costs for shorts
```

Simple formula:

```text
Net result = Gross result - Transaction costs
```

### Example

```text
Gross expected gain = 2,000
Transaction costs = 300

Net expected gain = 1,700
```

### Athena link

Trade simulation should eventually include transaction cost assumptions.

---

## 30. Post-trade processing

Post-trade processing starts after execution.

It includes:

```text
Trade capture
Trade confirmation
Settlement instruction
Cash update
Position update
Accounting records
Reconciliation
Exception management
```

The goal is to make sure the executed trade is correctly recorded and settled.

### Example

Executed trade:

```text
Buy 100 shares of AAPL at 200
```

Post-trade updates:

```text
AAPL position increases by 100 shares
Cash decreases by 20,000 plus costs
Trade record is created
```

---

## 31. Trade confirmation

Trade confirmation verifies trade details between parties.

Details include:

```text
Asset
Side
Quantity
Price
Trade date
Settlement date
Currency
Counterparty
Fees
```

### Example

Front office record:

```text
Buy 100 AAPL at 200
```

Broker confirmation:

```text
Buy 100 AAPL at 200
```

Status:

```text
Matched
```

If details differ, an exception is created.

---

## 32. Trade settlement

Settlement is the exchange of cash and securities.

For a buy trade:

```text
Buyer receives securities
Buyer pays cash
```

For a sell trade:

```text
Seller delivers securities
Seller receives cash
```

### Settlement risk

Settlement risk is the risk that one side fails to deliver.

### Athena link

Athena can model simplified settlement status:

```text
Pending settlement
Settled
Failed
Cancelled
```

---

## 33. Position update

After a trade, positions must be updated.

Buy trade:

```text
Position quantity increases
Cash decreases
```

Sell trade:

```text
Position quantity decreases
Cash increases
```

Example:

Before:

```text
AAPL quantity = 50
```

Trade:

```text
Buy 20 AAPL
```

After:

```text
AAPL quantity = 70
```

### Athena rule

Trade simulation should not mutate actual positions. Execution or explicit application should update positions.

---

## 34. Cash update

Trades affect cash.

Buy trade:

```text
Cash decreases by notional + costs
```

Sell trade:

```text
Cash increases by proceeds - costs
```

Example buy:

```text
Buy 100 shares at 50
Costs = 20

Cash impact = -5,020
```

### Why cash matters

If cash is wrong, portfolio value and risk metrics become wrong.

Athena should treat cash as part of portfolio value.

---

## 35. Portfolio update

After positions and cash are updated, the portfolio must be recalculated.

Updated metrics include:

```text
Total value
Position weights
Sector exposures
Currency exposures
Performance
Risk metrics
Limit usage
```

### Example

A new trade increases technology exposure.

Athena should update:

```text
Technology sector weight
Top holding weight
Portfolio VaR
Stress loss
Limit status
```

Portfolio update is the bridge between operations and risk monitoring.

---

## 36. Market data update

Market data must be updated regularly for accurate portfolio valuation and risk metrics.

Market data includes:

```text
Prices
FX rates
Rates
Volatility inputs
Benchmark levels
Corporate actions
```

### Example

If yesterday's price is used by mistake, risk and P&L may be wrong.

### Athena link

Athena should display market data timestamps and data quality warnings.

Example:

```text
AAPL price timestamp: 2026-04-29 16:00
Status: current
```

---

## 37. Position reconciliation

Position reconciliation compares internal position records with external or expected records.

Example:

```text
Internal position: 100 shares
Custodian position: 95 shares
Break: -5 shares
```

A break must be investigated.

### Why reconciliation matters

If positions are wrong, all downstream analytics are wrong:

```text
Portfolio value
Risk
P&L
Reporting
Limit checks
```

### Athena link

Athena can simulate reconciliation with expected vs actual position tables.

---

## 38. Cash reconciliation

Cash reconciliation compares internal cash records with bank or custodian records.

Example:

```text
Internal cash = 50,000
Custodian cash = 49,850
Difference = -150
```

Possible causes:

```text
Fees
Failed settlement
FX conversion
Incorrect trade record
Dividend payment
Timing difference
```

Cash breaks affect portfolio value and available trading capacity.

---

## 39. Trade reconciliation

Trade reconciliation compares trade records across systems.

Sources may include:

```text
Order management system
Execution system
Broker confirmation
Accounting system
Custodian record
```

### Example mismatch

Internal trade:

```text
Buy 100 MSFT at 420
```

Broker confirmation:

```text
Buy 100 MSFT at 421
```

This creates a price mismatch.

### Athena link

A ReconciliationBreak entity can represent such mismatches.

---

## 40. Exception management

Exception management is the process of investigating and resolving problems.

Examples of exceptions:

```text
Position mismatch
Cash mismatch
Trade price mismatch
Missing market data
Limit breach
Failed settlement
Invalid report
Data quality warning
```

Workflow:

```text
Detect exception
Classify severity
Assign owner
Investigate
Resolve
Document
Close
```

### Athena link

Athena can use statuses:

```text
Open
In review
Resolved
Closed
```

---

## 41. Breaks and mismatches

A break is a mismatch between expected and actual values.

Examples:

```text
Position break
Cash break
Trade break
Market data break
P&L break
```

### Example

Expected:

```text
Portfolio value = 100,000
```

Actual:

```text
Portfolio value = 99,500
```

Difference:

```text
-500
```

This requires explanation.

### Why breaks matter

Breaks reduce trust in reports and risk calculations.

---

## 42. Middle office control workflow

The middle office control workflow is the daily process of validating risk, P&L, exposures and limits.

Simplified workflow:

```text
1. Load positions
2. Load market data
3. Validate data
4. Calculate portfolio value
5. Calculate P&L
6. Calculate exposures
7. Calculate risk metrics
8. Check limits
9. Investigate breaches
10. Generate reports
```

### Athena link

Athena should model this workflow through a Risk Control Dashboard.

---

## 43. Daily risk calculation

Daily risk calculation updates risk metrics using current positions and market data.

Metrics may include:

```text
VaR
CVaR
Volatility
Stress loss
Concentration
Drawdown
Risk contribution
Limit usage
```

### Example

```text
Portfolio VaR yesterday = 10,000
Portfolio VaR today = 12,500
Change = +2,500
```

The middle office should understand why risk changed.

Possible reasons:

```text
New trade
Price movement
Volatility increase
Correlation change
Position size change
```

---

## 44. Daily P&L calculation

Daily P&L calculation explains how much the portfolio gained or lost during the day.

Basic formula:

```text
Daily P&L = Ending value - Beginning value
```

P&L may be decomposed by:

```text
Asset
Sector
Currency
Trade
Market movement
Fees
Residual
```

### Example

```text
Portfolio P&L = -2,000
AAPL contribution = -800
MSFT contribution = -500
FX contribution = -200
Fees = -50
Residual = -450
```

Detailed P&L attribution is covered in the P&L document, but this workflow document explains where it fits operationally.

---

## 45. Daily exposure calculation

Exposure calculation measures what the portfolio is exposed to.

Common exposures:

```text
Asset exposure
Sector exposure
Country exposure
Currency exposure
Factor exposure
Duration exposure
Delta exposure for options
```

### Example

```text
Technology exposure = 42%
USD exposure = 68%
Top holding exposure = 15%
```

Exposure is important because risk often comes from hidden concentration.

### Athena link

Exposure calculations support both the Portfolio Dashboard and Risk Monitor.

---

## 46. Limit monitoring

Limit monitoring checks whether portfolio metrics are within approved thresholds.

Examples:

```text
Max VaR
Max CVaR
Max single-name weight
Max sector weight
Max currency exposure
Max stress loss
Max drawdown
Minimum cash
```

### Example

```text
Max sector exposure = 35%
Current technology exposure = 38%
Status = Breach
```

Limit monitoring transforms analytics into control.

---

## 47. Breach detection

A breach occurs when a limit is exceeded.

Example:

```text
VaR limit = 50,000
Current VaR = 55,000
Breach = yes
```

Breach detection should record:

```text
Metric
Current value
Limit value
Severity
Timestamp
Portfolio
Status
```

### Athena link

Athena should create a breach record when a limit is exceeded.

Possible statuses:

```text
Open
Acknowledged
In remediation
Resolved
Closed
```

---

## 48. Breach escalation

Breach escalation defines what happens after a breach is detected.

Workflow:

```text
Breach detected
      ↓
Alert generated
      ↓
Owner notified
      ↓
Investigation performed
      ↓
Decision documented
      ↓
Action taken
      ↓
Breach closed
```

Possible actions:

```text
Reduce position
Hedge exposure
Approve temporary exception
Block new trades
Raise limit after approval
Escalate to committee
```

### Athena link

Athena can simulate breach escalation through status changes and workflow events.

---

## 49. Risk appetite framework

Risk appetite defines how much risk an institution or portfolio is willing to accept.

It can be expressed through:

```text
Target volatility
VaR limit
Stress loss tolerance
Concentration limits
Drawdown tolerance
Liquidity requirements
Credit quality requirements
```

### Example

```text
Maximum 1-day 95% VaR = 2.5% of portfolio value
Maximum single-name exposure = 10%
Maximum sector exposure = 35%
Minimum cash = 3%
```

Risk appetite guides risk limits.

---

## 50. Risk limits framework

A risk limits framework translates risk appetite into measurable limits.

Example:

```text
Risk appetite: moderate
VaR limit: 50,000
CVaR limit: 75,000
Technology exposure limit: 35%
Single-name limit: 10%
```

### Limit levels

Limits may include:

```text
Warning level
Breach level
Critical level
```

Example:

```text
Warning at 80%
Breach at 100%
Critical at 120%
```

### Athena link

The Limit Center should centralize this logic.

---

## 51. Front office vs risk management tension

There is often natural tension between front office and risk management.

Front office may want to take risk to generate return.

Risk management may restrict or challenge that risk.

This tension is healthy if handled correctly.

### Example

Front office:

```text
This trade has strong return potential.
```

Risk manager:

```text
It pushes the portfolio above the sector concentration limit.
```

The goal is not to stop all trades. The goal is to make informed decisions.

---

## 52. Independent risk control

Independent risk control means risk measurement should not depend only on the team taking the risk.

Why?

Because the front office may be optimistic or incentivized to focus on return.

Independent risk control provides:

```text
Objectivity
Challenge
Consistency
Governance
Credibility
```

### Athena link

Athena can represent independent control by separating:

```text
Trade simulation
Risk calculation
Limit check
Audit event
```

Even if the same user interacts with all modules, the system architecture should keep logic separated.

---

## 53. First line of defense

The first line of defense is the business itself.

In finance, this usually includes:

```text
Front office
Portfolio managers
Traders
Business managers
```

Responsibilities:

```text
Own the risk
Follow policies
Respect limits
Use controls
Escalate issues
```

### Example

A portfolio manager should not knowingly submit trades that violate the mandate.

The first line takes and manages risk day to day.

---

## 54. Second line of defense

The second line of defense provides independent oversight.

It includes:

```text
Risk management
Compliance
Model risk oversight
Control functions
```

Responsibilities:

```text
Set policies
Monitor limits
Challenge assumptions
Review breaches
Escalate risk issues
Validate controls
```

### Example

Risk management reviews whether a portfolio's VaR remains within approved limits.

Compliance reviews whether trades respect regulations and mandates.

---

## 55. Third line of defense

The third line of defense is internal audit.

It provides independent assurance that governance and controls are working.

Responsibilities:

```text
Audit processes
Review control effectiveness
Check policy compliance
Identify weaknesses
Recommend improvements
```

### Example

Internal audit may review whether risk breaches were properly escalated and documented.

### Athena note

Athena does not need to implement internal audit, but it should include audit trail concepts.

---

## 56. Governance and accountability

Governance defines who is responsible for decisions, controls and escalation.

A strong governance process defines:

```text
Who can create trades
Who can approve trades
Who can override limits
Who receives breach alerts
Who validates reports
Who owns data quality
Who signs off models
```

### Accountability

Every important action should have:

```text
User
Timestamp
Action
Reason
Result
```

### Athena link

This supports the WorkflowEvent and AuditTrail concepts.

---

## 57. Audit trail

An audit trail is a chronological record of important actions.

Examples:

```text
Trade created
Trade simulated
Limit breach detected
Trade approved
Trade rejected
Report generated
Breach resolved
Assumption changed
```

Audit trail fields:

```text
event_id
entity_type
entity_id
event_type
performed_by
timestamp
details
```

### Why audit trails matter

They support:

```text
Transparency
Governance
Investigation
Compliance
Reproducibility
Trust
```

Athena should log major workflow events.

---

## 58. Model validation

Model validation checks whether models are appropriate, correctly implemented and used properly.

Examples of models:

```text
VaR model
CVaR model
Stress testing model
Black-Scholes model
Optimization model
RiskDNA scoring model
```

Validation questions:

```text
Is the formula correct?
Are assumptions documented?
Are inputs valid?
Are outputs reasonable?
Are tests passing?
Is the model used within scope?
```

### Athena link

Athena should include tests and methodology notes for every model.

---

## 59. Data validation

Data validation checks whether inputs are complete, consistent and reasonable.

Examples:

```text
Prices are positive
Dates are not duplicated
Currency is defined
Portfolio weights are valid
Maturity dates are in the future
Volatility is positive
Trade quantity is positive
```

Bad data can break the workflow.

### Example

If price is missing, portfolio value cannot be trusted.

### Athena link

DataQualityWarnings should appear in relevant pages.

---

## 60. Report validation

Report validation checks whether reports are accurate and consistent before distribution.

Checks can include:

```text
Numbers tie to source data
Dates are correct
Portfolio name is correct
Currency is correct
Risk metrics match dashboard
No unresolved critical breaks
No missing sections
```

### Example

If VaR in the dashboard is 12,000 but VaR in the report is 10,000, the report must be investigated.

### Athena link

Reports Center should generate reproducible reports from the same calculation source.

---

## 61. Risk dashboard workflow

A risk dashboard summarizes key risk indicators.

Workflow:

```text
1. Load portfolio
2. Load latest market data
3. Validate inputs
4. Calculate risk metrics
5. Check limits
6. Identify top contributors
7. Display status
8. Generate explanation
```

Dashboard elements:

```text
VaR
CVaR
Stress loss
Limit usage
Risk status
Top contributors
Data warnings
```

### Athena link

The Risk Monitor should implement this workflow.

---

## 62. Portfolio dashboard workflow

A portfolio dashboard summarizes holdings and performance.

Workflow:

```text
1. Load positions
2. Update prices
3. Calculate market values
4. Calculate weights
5. Calculate exposures
6. Calculate performance
7. Compare benchmark
8. Display summary
```

Dashboard elements:

```text
Total value
Daily return
Top holdings
Sector allocation
Currency exposure
Benchmark comparison
Drawdown
```

### Athena link

This supports the main dashboard and Portfolio Builder.

---

## 63. Trade simulator workflow

The Trade Simulator is one of Athena's most important front-office / middle-office bridges.

Workflow:

```text
1. User enters proposed trade.
2. Athena validates the trade ticket.
3. Athena calculates current portfolio state.
4. Athena applies the trade to a simulated copy.
5. Athena recalculates weights and exposures.
6. Athena recalculates risk metrics.
7. Athena checks limits.
8. Athena compares before vs after.
9. Athena displays warnings and explanation.
```

### Important rule

```text
Simulation must not mutate the real portfolio.
```

The simulated portfolio is temporary.

---

## 64. Stress testing workflow

Stress testing workflow:

```text
1. Select portfolio
2. Select scenario
3. Load positions and exposures
4. Apply scenario shocks
5. Calculate stressed values
6. Calculate stress loss
7. Identify worst contributors
8. Compare stress loss to limits
9. Display results
```

Example scenario:

```text
Equity market -20%
Technology -30%
USD/CAD -5%
Volatility +50%
```

### Athena link

Stress testing should connect to the Risk Monitor and Reports Center.

---

## 65. Scenario approval workflow

In professional environments, stress scenarios may need approval before official use.

Workflow:

```text
Scenario drafted
      ↓
Assumptions reviewed
      ↓
Scenario approved
      ↓
Scenario used in reports
      ↓
Scenario reviewed periodically
```

Scenario metadata:

```text
name
description
assumptions
created_by
approved_by
status
version
```

### Athena first version

Athena can start with predefined scenarios and later support custom scenario approval.

---

## 66. Performance monitoring workflow

Performance monitoring tracks returns and compares them to objectives or benchmarks.

Workflow:

```text
1. Calculate portfolio return
2. Calculate benchmark return
3. Calculate active return
4. Calculate risk-adjusted metrics
5. Identify contributors
6. Report results
```

Metrics:

```text
Total return
Benchmark return
Active return
Sharpe ratio
Drawdown
Tracking error
```

### Athena link

Performance Analytics should connect to portfolio data and benchmark data.

---

## 67. Benchmark monitoring workflow

Benchmark monitoring checks how the portfolio behaves relative to its benchmark.

Workflow:

```text
1. Load portfolio returns
2. Load benchmark returns
3. Calculate active return
4. Calculate tracking error
5. Identify deviations
6. Report underperformance or outperformance
```

Example:

```text
Portfolio return = 8%
Benchmark return = 10%
Active return = -2%
```

### Athena link

Each portfolio should have a benchmark symbol or benchmark definition.

---

## 68. Client reporting workflow

Client reporting communicates portfolio status to a client or stakeholder.

A client report may include:

```text
Portfolio value
Performance
Benchmark comparison
Holdings
Allocation
Risk summary
Key changes
Commentary
```

### Good client reporting

It should be:

```text
Clear
Accurate
Understandable
Consistent
Not overly technical
```

### Athena link

Reports Center can eventually generate clean portfolio and risk reports.

---

## 69. Management reporting workflow

Management reporting gives decision-makers an overview of portfolios, risks and issues.

It may include:

```text
Aggregate exposures
Limit breaches
Top risks
Stress losses
Performance summary
Operational breaks
Data quality issues
Trend analysis
```

### Difference from client reporting

Client reporting explains portfolio outcomes.

Management reporting focuses on oversight and control.

### Athena link

Athena can include a management-style dashboard later.

---

## 70. Regulatory reporting intuition

Regulatory reporting is the process of providing required information to regulators.

This depends on jurisdiction and institution type.

Examples of regulatory themes:

```text
Risk exposure
Capital adequacy
Liquidity
Client suitability
Transaction reporting
Best execution
Market abuse prevention
```

### Athena note

Athena does not need to implement regulatory reporting.

But understanding the idea is useful:

```text
Financial institutions must document, monitor and report risk and activity.
```

---

## 71. Communication between teams

Strong workflows require good communication between teams.

Examples:

```text
Front office explains trade rationale.
Risk explains limit impact.
Operations reports settlement issues.
Compliance flags restrictions.
Management reviews breaches.
```

### Poor communication creates risk

Problems can occur when:

```text
A trade is executed without risk review.
A breach is detected but not escalated.
A data issue is known but not communicated.
A report is sent with inconsistent numbers.
```

### Athena link

Athena can make communication easier through clear statuses, explanations and workflow events.

---

## 72. Key daily processes

Daily processes may include:

```text
Load market data
Update positions
Calculate portfolio value
Calculate daily P&L
Calculate exposures
Calculate risk metrics
Run limit checks
Investigate exceptions
Produce risk dashboard
Review breaches
```

### Athena daily workflow

A simplified Athena daily workflow:

```text
1. Refresh prices
2. Revalue portfolio
3. Recalculate risk
4. Check limits
5. Display warnings
6. Generate report if needed
```

---

## 73. Key weekly processes

Weekly processes may include:

```text
Review portfolio performance
Review exposures
Review risk trends
Review unresolved breaks
Review stress testing outputs
Review benchmark deviations
Prepare management summary
```

### Example weekly question

```text
Did portfolio risk increase materially this week?
```

Athena can support this through trend charts and historical metrics.

---

## 74. Key monthly processes

Monthly processes may include:

```text
Client reporting
Management reporting
Performance attribution
Risk committee review
Model review
Limit review
Portfolio rebalancing review
Data quality review
```

### Example monthly question

```text
Did the portfolio remain aligned with its objective and risk appetite?
```

Athena's reports can eventually summarize monthly performance and risk.

---

## 75. Common front office tools

Front office tools may include:

```text
Portfolio management systems
Order management systems
Execution management systems
Market data terminals
Research platforms
Analytics dashboards
Client relationship tools
Trading platforms
```

The front office needs tools for:

```text
Decision-making
Execution
Market monitoring
Client service
Portfolio construction
```

### Athena positioning

Athena is not a full trading system. It is a learning and analytics terminal focused on portfolio and risk decisions.

---

## 76. Common middle office tools

Middle office tools may include:

```text
Risk systems
Performance systems
Limit monitoring tools
P&L systems
Stress testing platforms
Data quality tools
Reporting systems
Reconciliation tools
```

The middle office needs tools for:

```text
Control
Measurement
Validation
Reporting
Escalation
```

### Athena positioning

Athena is strongly aligned with middle office analytics:

```text
Risk Monitor
Limit Center
Stress Testing
Reports Center
RiskDNA
```

---

## 77. Common back office tools

Back office tools may include:

```text
Settlement systems
Accounting systems
Custody platforms
Reconciliation tools
Cash management tools
Corporate actions systems
Recordkeeping systems
```

The back office needs tools for:

```text
Operational processing
Settlement
Records
Reconciliation
Exception handling
```

### Athena positioning

Athena can include simplified back office concepts, but it is not designed as a settlement system.

---

## 78. Common workflow failures

Common workflow failures include:

```text
Trade entered incorrectly
Trade not approved before execution
Missing market data
Wrong price used
Wrong currency used
Position mismatch
Cash mismatch
Limit breach not escalated
Report sent with incorrect data
Model used with invalid assumptions
```

### Example

A trade is entered as:

```text
Buy 1,000 shares
```

but should have been:

```text
Buy 100 shares
```

This creates large unintended exposure.

### Athena link

Validation and confirmation steps reduce workflow failures.

---

## 79. Operational risk in workflows

Operational risk appears when processes, systems or people fail.

Examples:

```text
Manual input error
System outage
Data feed failure
Incorrect calculation
Unauthorized approval
Missed settlement
Incorrect report
Cybersecurity issue
```

### Why operational risk matters

Even a good investment decision can create losses if the workflow fails.

### Athena link

Athena should reduce operational risk through:

```text
Input validation
Clear statuses
Audit trail
Data quality warnings
Automated calculations
Deterministic tests
```

---

## 80. Controls and checks

Controls are rules or processes designed to prevent or detect problems.

Examples:

```text
Input validation
Limit checks
Approval workflow
Reconciliation
Data quality checks
Report validation
Audit trail
Access controls
```

### Preventive controls

Prevent errors before they happen.

Example:

```text
Reject negative trade quantity.
```

### Detective controls

Detect errors after they occur.

Example:

```text
Reconciliation identifies position mismatch.
```

Athena should include both types where possible.

---

## 81. Maker-checker principle

The maker-checker principle means one person creates or changes something, and another person reviews or approves it.

Example:

```text
Maker creates trade ticket.
Checker approves trade ticket.
```

This reduces error and fraud risk.

### Athena first version

Athena may not need multiple user roles at first, but it can model the concept through statuses:

```text
Draft
Pending approval
Approved
Rejected
```

---

## 82. Segregation of duties

Segregation of duties means critical tasks are separated across different roles.

Example:

```text
The person executing the trade should not be the only person validating risk and settlement.
```

This prevents conflicts of interest and reduces operational risk.

### Simple principle

```text
No single person should control every step of a risky process.
```

### Athena link

Athena can reflect this by separating modules:

```text
Trade Simulator
Risk Monitor
Limit Center
Reports Center
Audit Trail
```

---

## 83. Data required for workflow management

Athena needs structured data to manage workflows.

### TradeTicket

```text
id
portfolio_id
asset_id
side
quantity
order_type
estimated_price
estimated_notional
currency
created_by
status
created_at
```

### PreTradeCheck

```text
trade_id
portfolio_id
check_type
status
message
before_value
after_value
limit_value
usage_percent
```

### WorkflowEvent

```text
id
entity_type
entity_id
event_type
performed_by
timestamp
details
```

### ReconciliationBreak

```text
id
break_type
expected_value
actual_value
difference
status
assigned_to
created_at
resolved_at
```

### LimitBreach

```text
id
portfolio_id
metric_name
current_value
limit_value
severity
status
detected_at
resolved_at
```

---

## 84. Common beginner mistakes

### Mistake 1 — Thinking finance ends at the trade decision

A trade must be checked, executed, confirmed, settled, recorded and monitored.

### Mistake 2 — Confusing front office and middle office

Front office takes investment decisions. Middle office controls risk and reporting.

### Mistake 3 — Ignoring back office

Incorrect settlement or records can break risk and P&L calculations.

### Mistake 4 — Ignoring pre-trade checks

A trade should be assessed before execution.

### Mistake 5 — Ignoring limits

Risk metrics need thresholds to become actionable.

### Mistake 6 — Ignoring audit trail

Important decisions should be traceable.

### Mistake 7 — Thinking a dashboard is enough

A dashboard is useful, but workflow, validation and governance matter too.

### Mistake 8 — Mixing simulation with real portfolio updates

Simulation must not mutate real portfolio data.

### Mistake 9 — Ignoring operational risk

Errors in data, trades or reports can create real losses.

### Mistake 10 — Repeating calculations without explaining decisions

Professional systems should connect numbers to interpretation and workflow status.

---

## 85. Key workflow concepts

Important concepts:

```text
Front office
Middle office
Back office
Trade ticket
Pre-trade checks
Post-trade processing
Settlement
Reconciliation
Break
Exception
Limit
Breach
Escalation
Risk appetite
Audit trail
Maker-checker
Segregation of duties
Governance
```

Simple summary:

```text
Front office = decision and execution
Middle office = control and explanation
Back office = settlement and records
```

Athena summary:

```text
Athena connects front-office decisions to middle-office risk controls.
```

---

## 86. Possible API endpoints

Possible Athena API endpoints:

```text
POST /api/trades/simulate
POST /api/trades
GET  /api/trades/{trade_id}
GET  /api/trades/{trade_id}/checks
POST /api/trades/{trade_id}/approve
POST /api/trades/{trade_id}/reject
POST /api/trades/{trade_id}/execute

GET  /api/workflows/events
GET  /api/workflows/events/{entity_type}/{entity_id}

GET  /api/controls/limits
POST /api/controls/limits/check
GET  /api/controls/breaches
POST /api/controls/breaches/{breach_id}/acknowledge
POST /api/controls/breaches/{breach_id}/resolve

GET  /api/reconciliation/breaks
POST /api/reconciliation/run
POST /api/reconciliation/breaks/{break_id}/resolve
```

### Example trade simulation request

```json
{
  "portfolio_id": "pf_001",
  "asset_symbol": "AAPL",
  "side": "buy",
  "quantity": 50,
  "estimated_price": 200,
  "order_type": "market"
}
```

### Example pre-trade check response

```json
{
  "trade_id": "tr_001",
  "checks": [
    {
      "check_type": "single_name_limit",
      "status": "OK",
      "before_value": 0.08,
      "after_value": 0.095,
      "limit_value": 0.10
    },
    {
      "check_type": "sector_limit",
      "status": "WARNING",
      "before_value": 0.32,
      "after_value": 0.345,
      "limit_value": 0.35
    }
  ]
}
```

---

## 87. Possible frontend components

Possible Athena frontend components:

```text
TradeTicketForm
TradeTicketSummary
PreTradeCheckPanel
BeforeAfterPortfolioImpact
BeforeAfterRiskImpact
LimitCheckCard
ApprovalStatusBadge
WorkflowTimeline
RiskControlDashboard
BreachTable
BreachDetailDrawer
ReconciliationBreakTable
AuditTrailPanel
MiddleOfficeControlCenter
OperationalStatusCard
DataQualityWarningPanel
```

### Important pages

```text
Trade Simulator
Risk Control Center
Limit Center
Workflow Timeline
Reconciliation Center
Audit Trail
```

### UI goal

The user should immediately understand:

```text
What trade is proposed?
What changes after the trade?
Which checks pass or fail?
Is approval needed?
What risk or operational issues exist?
```

---

## 88. Suggested tests

### Trade simulation tests

```text
Trade simulation does not mutate original portfolio.
Buying increases position quantity in simulated portfolio.
Selling decreases position quantity in simulated portfolio.
Estimated notional equals quantity × estimated price.
```

### Pre-trade check tests

```text
Pre-trade check detects single-name limit breach.
Pre-trade check detects sector limit breach.
Pre-trade check detects insufficient cash.
Limit usage is calculated correctly.
```

### Workflow status tests

```text
Draft trade can move to pending approval.
Approved trade can be executed.
Rejected trade cannot be executed.
Cancelled trade cannot be approved.
Executed trade creates workflow event.
```

### Reconciliation tests

```text
Position mismatch creates reconciliation break.
Cash mismatch creates reconciliation break.
Resolved break changes status to resolved.
```

### Audit trail tests

```text
Trade creation creates audit event.
Trade approval creates audit event.
Limit breach creates audit event.
Breach resolution creates audit event.
```

### Risk control tests

```text
Breach status becomes warning, breach or critical correctly.
Limit Center returns correct status for each metric.
```

---

## 89. How Athena uses front office and middle office workflows

Athena should use this workflow document to connect all finance modules into one coherent product.

### Main product idea

```text
Athena is not only a calculator.
Athena is a risk terminal that connects investment decisions to controls.
```

### Core Athena workflow

```text
1. User builds a portfolio.
2. User proposes a trade.
3. Athena simulates the trade.
4. Athena recalculates portfolio exposures.
5. Athena recalculates risk metrics.
6. Athena checks limits.
7. Athena identifies warnings and breaches.
8. Athena explains the result.
9. Athena creates an audit trail.
10. Athena can generate a report.
```

### Modules connected by this workflow

```text
Portfolio Builder
Trade Simulator
Risk Monitor
Stress Testing
Limit Center
RiskDNA
Reports Center
Audit Trail
```

### Example Athena explanation

```text
The proposed trade increases technology exposure from 32.0% to 34.5%, which remains below the 35.0% sector limit but triggers a warning because usage reaches 98.6%. The trade also increases 1-day 95% VaR by 1,200 CAD. Approval is recommended before execution.
```

This is the type of explanation that makes Athena look professional.

---

## 90. Summary

Front office, middle office and back office represent different responsibilities in financial institutions.

Key summary:

```text
Front office = investment decisions, trading and client-facing activity.
Middle office = risk control, performance control, limits and reporting.
Back office = settlement, confirmation, records and operations.
```

A professional financial workflow does not stop at investment ideas.

It includes:

```text
Trade ticket
Pre-trade checks
Risk analysis
Compliance checks
Approval
Execution
Confirmation
Settlement
Position update
Reconciliation
Risk monitoring
Limit monitoring
Reporting
Audit trail
```

For Athena AI Risk Terminal, this document explains the product logic:

```text
Athena connects front-office decisions to middle-office risk controls.
```

The key lesson is:

```text
A serious finance platform is not only about calculations.
It is about workflow, controls, governance, explanations and traceability.
```
