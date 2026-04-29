# 05 — Options, Black-Scholes and Greeks

**Project:** Athena AI Risk Terminal  
**Recommended file path:** `docs/finance/05-options-black-scholes-greeks.md`  
**Purpose:** build a clear foundation in options, option payoff, option pricing, Black-Scholes, Greeks, option sensitivities and option P&L intuition before implementing the Options Pricing Lab in Athena.  
**Scope:** this document focuses only on options, Black-Scholes and Greeks. General market volatility, fixed income rates, portfolio management, VaR/CVaR and P&L attribution are documented separately.

---

## Table of Contents

1. What is a derivative?
2. What is an option?
3. Why options matter
4. Underlying asset
5. Option contract basics
6. Option buyer vs option seller
7. Rights vs obligations
8. Call option
9. Put option
10. Strike price
11. Expiration date
12. Maturity and time to maturity
13. Option premium
14. Contract size
15. European options
16. American options
17. Intrinsic value
18. Time value
19. Moneyness
20. In the money
21. At the money
22. Out of the money
23. Option payoff
24. Call payoff
25. Put payoff
26. Long call
27. Short call
28. Long put
29. Short put
30. Profit vs payoff
31. Breakeven price
32. Maximum profit
33. Maximum loss
34. Option payoff tables
35. Option payoff diagrams
36. Option pricing intuition
37. Factors affecting option prices
38. Spot price impact
39. Strike price impact
40. Time to maturity impact
41. Volatility impact
42. Risk-free rate impact
43. Dividend impact
44. Cost of carry intuition
45. Put-call parity
46. Put-call parity intuition
47. Arbitrage intuition
48. Synthetic positions
49. Black-Scholes overview
50. Black-Scholes purpose
51. Black-Scholes assumptions
52. Black-Scholes inputs
53. Spot price input
54. Strike price input
55. Time to maturity input
56. Risk-free rate input
57. Volatility input
58. Dividend yield input
59. d1 intuition
60. d2 intuition
61. Black-Scholes call formula
62. Black-Scholes put formula
63. Standard normal distribution role
64. Black-Scholes call example
65. Black-Scholes put example
66. Put-call parity check
67. Black-Scholes limitations
68. What are the Greeks?
69. Why Greeks matter
70. Delta
71. Call Delta
72. Put Delta
73. Delta interpretation
74. Delta as hedge ratio
75. Gamma
76. Gamma interpretation
77. Delta-Gamma relationship
78. Vega
79. Vega interpretation
80. Volatility risk
81. Theta
82. Theta interpretation
83. Time decay
84. Rho
85. Rho interpretation
86. Interest rate sensitivity
87. Greeks summary table
88. Greeks by moneyness
89. Greeks by time to maturity
90. Greeks by volatility
91. Option P&L intuition
92. Delta approximation of P&L
93. Delta-Gamma approximation of P&L
94. Vega impact on P&L
95. Theta impact on P&L
96. Basic option strategies
97. Option risk management
98. Possible API endpoints
99. Possible frontend components and tests
100. How Athena uses options and Greeks

---

## 1. What is a derivative?

A derivative is a financial contract whose value depends on another asset.

That asset is called the **underlying asset**.

Examples of derivatives:

```text
Options
Futures
Forwards
Swaps
```

Simple intuition:

```text
A derivative does not have value independently.
Its value is derived from something else.
```

Example:

```text
A call option on Apple depends on the price of Apple stock.
A futures contract on oil depends on the price of oil.
```

This document focuses only on options.

---

## 2. What is an option?

An option is a contract that gives one party a right linked to an underlying asset.

There are two main types:

```text
Call option
Put option
```

An option usually has:

```text
Underlying asset
Strike price
Expiration date
Premium
Contract size
Exercise style
Currency
```

Simple idea:

```text
A call gives the right to buy.
A put gives the right to sell.
```

The option buyer pays a premium.  
The option seller receives the premium.

---

## 3. Why options matter

Options matter because they can be used for:

```text
Hedging
Speculation
Income generation
Risk transfer
Volatility exposure
Portfolio protection
Structured strategies
```

Examples:

```text
An investor buys a put to protect a stock position.
A trader buys a call to benefit from upside.
A portfolio manager sells covered calls to generate income.
```

Options are important because they are **nonlinear instruments**.

This means their value does not move one-for-one with the underlying asset.

For Athena, options are important because they add a more advanced layer of market risk and sensitivity analysis.

---

## 4. Underlying asset

The underlying asset is the asset on which the option is based.

Examples:

```text
Stock
ETF
Index
Currency
Commodity
Bond
Future
```

For Athena's first version, the simplest underlying is:

```text
Stock or ETF
```

Example:

```text
Underlying = AAPL
Option type = Call
Strike = 200
Expiration = 3 months
```

The option value depends mainly on the behavior of AAPL.

---

## 5. Option contract basics

An option contract usually includes:

```text
Underlying symbol
Option type
Strike price
Expiration date
Premium
Contract size
Exercise style
Currency
```

Example:

```text
Underlying: AAPL
Type: Call
Strike: 200
Expiration: 2026-09-18
Premium: 12.50
Contract size: 100 shares
Style: American
Currency: USD
```

For one contract, the total premium paid is usually:

```text
Premium × Contract size
```

Example:

```text
12.50 × 100 = 1,250
```

Athena should clearly distinguish between:

```text
Option price per unit
Total contract value
```

---

## 6. Option buyer vs option seller

An option has two sides:

```text
Buyer / holder
Seller / writer
```

The buyer pays the premium and receives the right.

The seller receives the premium and takes the potential obligation.

Example with a call:

```text
Call buyer = has the right to buy
Call seller = may have the obligation to sell
```

Example with a put:

```text
Put buyer = has the right to sell
Put seller = may have the obligation to buy
```

This distinction is critical because the risk profile is very different.

---

## 7. Rights vs obligations

The option buyer has a **right**.

The option seller has a potential **obligation**.

For a call:

```text
Call buyer has the right to buy the underlying at the strike.
Call seller may be obligated to sell the underlying at the strike.
```

For a put:

```text
Put buyer has the right to sell the underlying at the strike.
Put seller may be obligated to buy the underlying at the strike.
```

Simple rule:

```text
Buyer = right
Seller = obligation
```

This is one of the most important ideas in options.

---

## 8. Call option

A call option gives the buyer the right to buy the underlying asset at the strike price.

Simple rule:

```text
Call = right to buy
```

A call becomes more valuable when the underlying price increases.

Example:

```text
Stock price = 120
Call strike = 100
```

The call has value because it gives the right to buy at 100 when the market price is 120.

A call buyer is generally bullish on the underlying.

---

## 9. Put option

A put option gives the buyer the right to sell the underlying asset at the strike price.

Simple rule:

```text
Put = right to sell
```

A put becomes more valuable when the underlying price decreases.

Example:

```text
Stock price = 80
Put strike = 100
```

The put has value because it gives the right to sell at 100 when the market price is 80.

A put buyer is generally bearish or protective.

---

## 10. Strike price

The strike price is the price at which the option can be exercised.

Example:

```text
Call strike = 100
```

This means the call buyer has the right to buy the underlying at 100.

Example:

```text
Put strike = 100
```

This means the put buyer has the right to sell the underlying at 100.

The strike is central to:

```text
Moneyness
Intrinsic value
Payoff
Profit
Black-Scholes pricing
Greeks
```

---

## 11. Expiration date

The expiration date is the date when the option contract ends.

After expiration, the option no longer exists.

Example:

```text
Expiration date = 2026-09-18
```

Time matters because an option with more time usually has more opportunity to become valuable.

An option close to expiration can behave very differently from an option with one year remaining.

---

## 12. Maturity and time to maturity

Time to maturity is the amount of time remaining until expiration.

It is often expressed in years for pricing models.

Examples:

```text
1 year = 1.0
6 months = 0.5
3 months = 0.25
30 days ≈ 30 / 365 = 0.0822
```

In Black-Scholes, time to maturity is usually written as:

```text
T
```

Athena should convert dates into time to maturity automatically when possible.

---

## 13. Option premium

The option premium is the price paid by the buyer to the seller.

Example:

```text
Option premium = 5
Contract size = 100
Total cost = 500
```

The premium is paid upfront.

For a long call or long put, the premium is the maximum possible loss.

For the seller, the premium is income received, but the seller may face large losses.

Simple rule:

```text
Buyer pays premium.
Seller receives premium.
```

---

## 14. Contract size

Contract size defines how many units of the underlying one option contract represents.

For many listed equity options:

```text
Contract size = 100 shares
```

Example:

```text
Premium = 4
Contract size = 100

Total premium = 400
```

Athena should be clear whether it displays:

```text
Price per option unit
```

or:

```text
Total contract value
```

This avoids confusion between a premium of 4 and a total cost of 400.

---

## 15. European options

A European option can be exercised only at expiration.

Simple rule:

```text
European option = exercise only at expiration
```

This is the option type used in the basic Black-Scholes model.

For Athena's first Options Pricing Lab, European options are the best starting point because the pricing formulas are clear and standard.

---

## 16. American options

An American option can be exercised at any time before or at expiration.

Simple rule:

```text
American option = exercise any time before expiration
```

American options are more complex to price because early exercise may matter.

Basic Black-Scholes is designed for European options.

Athena should start with European options and clearly state that American exercise is outside the first version.

---

## 17. Intrinsic value

Intrinsic value is the value the option would have if exercised immediately.

For a call:

```text
Call intrinsic value = max(Spot - Strike, 0)
```

For a put:

```text
Put intrinsic value = max(Strike - Spot, 0)
```

Example call:

```text
Spot = 120
Strike = 100

Intrinsic value = max(120 - 100, 0)
Intrinsic value = 20
```

Example put:

```text
Spot = 80
Strike = 100

Intrinsic value = max(100 - 80, 0)
Intrinsic value = 20
```

Intrinsic value cannot be negative.

---

## 18. Time value

Time value is the part of the option premium above intrinsic value.

Formula:

```text
Time value = Option premium - Intrinsic value
```

Example:

```text
Option premium = 25
Intrinsic value = 20

Time value = 5
```

Time value exists because the option still has time to become more valuable before expiration.

General intuition:

```text
More time to expiration → more opportunity → more time value
```

Time value disappears at expiration.

---

## 19. Moneyness

Moneyness describes the relationship between the spot price and the strike price.

Main categories:

```text
In the money
At the money
Out of the money
```

Moneyness helps explain whether an option currently has intrinsic value.

For calls and puts, the interpretation is different.

Athena should include a `MoneynessBadge` in the Options Pricing Lab.

---

## 20. In the money

An option is in the money when it has positive intrinsic value.

For a call:

```text
Spot > Strike
```

For a put:

```text
Spot < Strike
```

Example call:

```text
Spot = 120
Strike = 100
Call is in the money
```

Example put:

```text
Spot = 80
Strike = 100
Put is in the money
```

In-the-money options usually have higher intrinsic value.

---

## 21. At the money

An option is at the money when the spot price is close to the strike price.

Example:

```text
Spot = 100
Strike = 100
```

At-the-money options usually have important sensitivity behavior.

They often have:

```text
High time value
Important Gamma behavior
Delta around 0.5 for calls
Delta around -0.5 for puts
```

At-the-money options are central for understanding Greeks.

---

## 22. Out of the money

An option is out of the money when it has no intrinsic value.

For a call:

```text
Spot < Strike
```

For a put:

```text
Spot > Strike
```

Example call:

```text
Spot = 90
Strike = 100
Call is out of the money
```

Example put:

```text
Spot = 110
Strike = 100
Put is out of the money
```

Out-of-the-money options can still have time value before expiration.

---

## 23. Option payoff

Payoff is the option value at expiration before considering the premium paid.

Important distinction:

```text
Payoff ignores premium.
Profit includes premium.
```

At expiration, time value is gone.

Only intrinsic value remains.

Payoff is useful because it shows the contract's mechanical outcome at expiration.

Profit is more realistic because it includes the cost of entering the position.

---

## 24. Call payoff

A call option payoff at expiration is:

```text
Call payoff = max(Spot at expiration - Strike, 0)
```

Example:

```text
Strike = 100
Spot at expiration = 120

Call payoff = max(120 - 100, 0)
Call payoff = 20
```

If spot is below strike:

```text
Strike = 100
Spot at expiration = 90

Call payoff = max(90 - 100, 0)
Call payoff = 0
```

A call payoff cannot be negative for the buyer.

---

## 25. Put payoff

A put option payoff at expiration is:

```text
Put payoff = max(Strike - Spot at expiration, 0)
```

Example:

```text
Strike = 100
Spot at expiration = 80

Put payoff = max(100 - 80, 0)
Put payoff = 20
```

If spot is above strike:

```text
Strike = 100
Spot at expiration = 120

Put payoff = max(100 - 120, 0)
Put payoff = 0
```

A put payoff cannot be negative for the buyer.

---

## 26. Long call

A long call means buying a call option.

The buyer benefits if the underlying price rises.

Payoff:

```text
max(S_T - K, 0)
```

Profit:

```text
max(S_T - K, 0) - premium
```

Example:

```text
Strike = 100
Premium = 5
Spot at expiration = 120

Payoff = 20
Profit = 20 - 5 = 15
```

Maximum loss:

```text
Premium paid
```

Upside potential:

```text
Theoretically large
```

A long call is a bullish option position.

---

## 27. Short call

A short call means selling a call option.

The seller receives the premium but may lose if the underlying rises.

Profit:

```text
Premium - max(S_T - K, 0)
```

Example:

```text
Strike = 100
Premium = 5
Spot at expiration = 120

Profit = 5 - 20 = -15
```

Maximum profit:

```text
Premium received
```

Potential loss:

```text
Theoretically unlimited
```

This is why naked short calls are risky.

---

## 28. Long put

A long put means buying a put option.

The buyer benefits if the underlying price falls.

Profit:

```text
max(K - S_T, 0) - premium
```

Example:

```text
Strike = 100
Premium = 4
Spot at expiration = 80

Payoff = 20
Profit = 20 - 4 = 16
```

Maximum loss:

```text
Premium paid
```

A long put can be used for downside protection.

---

## 29. Short put

A short put means selling a put option.

The seller receives the premium but may lose if the underlying falls.

Profit:

```text
Premium - max(K - S_T, 0)
```

Example:

```text
Strike = 100
Premium = 4
Spot at expiration = 80

Profit = 4 - 20 = -16
```

Maximum profit:

```text
Premium received
```

Large loss occurs if the underlying falls sharply.

A short put can be risky because the seller may be forced to buy the asset at a strike above market value.

---

## 30. Profit vs payoff

Payoff is the value at expiration before considering premium.

Profit includes the premium paid or received.

Example long call:

```text
Strike = 100
Premium = 5
Spot at expiration = 110

Payoff = 10
Profit = 10 - 5 = 5
```

If you only look at payoff, you may think the trade made 10.  
But after paying premium, the profit is only 5.

Simple rule for buyers:

```text
Profit = Payoff - Premium paid
```

Simple rule for sellers:

```text
Profit = Premium received - Payoff owed
```

---

## 31. Breakeven price

The breakeven price is the underlying price at expiration where profit is zero.

Long call breakeven:

```text
Breakeven = Strike + Premium
```

Long put breakeven:

```text
Breakeven = Strike - Premium
```

Example long call:

```text
Strike = 100
Premium = 5

Breakeven = 105
```

Example long put:

```text
Strike = 100
Premium = 4

Breakeven = 96
```

Breakeven is essential for understanding whether a trade is profitable at expiration.

---

## 32. Maximum profit

Maximum profit depends on the option position.

Long call:

```text
Potential profit is theoretically unlimited.
```

Short call:

```text
Maximum profit = premium received.
```

Long put:

```text
Maximum profit is large but limited because the underlying cannot fall below zero.
```

Short put:

```text
Maximum profit = premium received.
```

Example long put:

```text
Strike = 100
Premium = 4
Underlying falls to 0

Maximum profit = 100 - 4 = 96
```

---

## 33. Maximum loss

Maximum loss also depends on the position.

Long call:

```text
Maximum loss = premium paid
```

Long put:

```text
Maximum loss = premium paid
```

Short call:

```text
Potential loss is theoretically unlimited
```

Short put:

```text
Large but limited loss if underlying falls to zero
```

Example short put:

```text
Strike = 100
Premium = 4
Underlying falls to 0

Loss = 100 - 4 = 96
```

Athena should display maximum profit and maximum loss when showing payoff charts.

---

## 34. Option payoff tables

A payoff table shows payoff or profit at different underlying prices.

Example long call:

```text
Strike = 100
Premium = 5
```

```text
Spot at expiration | Payoff | Profit
80                 | 0      | -5
90                 | 0      | -5
100                | 0      | -5
105                | 5      | 0
110                | 10     | 5
120                | 20     | 15
```

Payoff tables are useful because they make option behavior concrete.

Athena should include payoff tables or charts for learning and validation.

---

## 35. Option payoff diagrams

A payoff diagram shows profit or payoff across possible underlying prices at expiration.

Typical x-axis:

```text
Underlying price at expiration
```

Typical y-axis:

```text
Profit or payoff
```

A long call diagram has limited downside and increasing upside.

A long put diagram has limited downside and benefits when the underlying falls.

Athena component ideas:

```text
PayoffChart
ProfitLossChart
```

These visuals make options much easier to understand.

---

## 36. Option pricing intuition

Option pricing before expiration is more complex than payoff at expiration.

Before expiration, an option price depends on:

```text
Intrinsic value
Time value
Uncertainty
Interest rates
Dividends
```

A call option may have value even if it is currently out of the money because it might become in the money before expiration.

Example:

```text
Spot = 95
Strike = 100
Call intrinsic value = 0
Call premium may still be positive
```

Why?

Because there is still time and uncertainty.

---

## 37. Factors affecting option prices

Main factors:

```text
Spot price
Strike price
Time to maturity
Volatility
Risk-free rate
Dividends
```

General effects for a call:

```text
Higher spot price → higher call value
Higher strike → lower call value
More time → usually higher call value
Higher volatility → higher call value
Higher risk-free rate → usually higher call value
Higher dividends → lower call value
```

General effects for a put:

```text
Higher spot price → lower put value
Higher strike → higher put value
More time → usually higher put value
Higher volatility → higher put value
Higher risk-free rate → usually lower put value
Higher dividends → higher put value
```

These are general rules and may have exceptions in more advanced contexts.

---

## 38. Spot price impact

The spot price is the current price of the underlying asset.

For calls:

```text
Spot up → call value up
```

For puts:

```text
Spot up → put value down
```

Example:

```text
Call strike = 100
Spot rises from 100 to 110
```

The call becomes more valuable because the right to buy at 100 is more attractive.

For a put, the opposite happens.

This is the intuition behind Delta.

---

## 39. Strike price impact

The strike price determines the exercise price.

For calls:

```text
Higher strike → lower call value
```

For puts:

```text
Higher strike → higher put value
```

Example call:

```text
Spot = 100
Call strike 90 is more valuable than call strike 110
```

Example put:

```text
Spot = 100
Put strike 110 is more valuable than put strike 90
```

Strike price is central to moneyness.

---

## 40. Time to maturity impact

More time usually increases option value.

Why?

Because more time gives the option more opportunity to become valuable.

Example:

```text
A 1-year call is usually worth more than a 1-month call with the same strike.
```

However, time effects can be more complex for certain American options and dividend-paying assets.

In the basic European Black-Scholes framework, more time usually increases option value.

Theta measures sensitivity to time passing.

---

## 41. Volatility impact

Volatility is one of the most important inputs in option pricing.

Higher volatility usually increases both call and put values.

Why?

Because options benefit from uncertainty.

A long option has limited downside but can benefit from large favorable moves.

Example:

```text
Same spot, same strike, same maturity.
Volatility increases from 20% to 40%.
Option premium usually increases.
```

The general concept of volatility is covered in the Market Finance and Volatility document. Here, volatility is treated specifically as an option pricing input.

---

## 42. Risk-free rate impact

The risk-free rate is an input in Black-Scholes.

For calls:

```text
Higher risk-free rate usually increases call value.
```

For puts:

```text
Higher risk-free rate usually decreases put value.
```

Intuition:

A call delays paying the strike until expiration. If rates are higher, delaying payment can be more valuable.

Interest rates and yield curves are covered in the Fixed Income document. Here, the risk-free rate is used only as an option pricing input.

---

## 43. Dividend impact

Dividends affect option prices because they reduce the expected future stock price when paid.

For calls:

```text
Higher dividends usually reduce call value.
```

For puts:

```text
Higher dividends usually increase put value.
```

Why?

If the underlying is expected to drop because of dividends, calls become less attractive and puts become more attractive.

Black-Scholes can include continuous dividend yield as:

```text
q
```

---

## 44. Cost of carry intuition

Cost of carry refers to the net cost or benefit of holding the underlying asset.

It can include:

```text
Financing cost
Dividend yield
Storage cost
Convenience yield
```

For stocks, dividends are often the most relevant carry component.

For commodities, storage and convenience yield may matter.

Athena's first option pricing module can keep this simple:

```text
Risk-free rate
Dividend yield
```

---

## 45. Put-call parity

Put-call parity links the prices of European calls and puts with the same:

```text
Underlying
Strike
Expiration
```

Basic formula without dividends:

```text
Call - Put = Spot - Strike × e^(-rT)
```

With continuous dividend yield:

```text
Call - Put = Spot × e^(-qT) - Strike × e^(-rT)
```

Where:

```text
C = call price
P = put price
S = spot price
K = strike
r = risk-free rate
q = dividend yield
T = time to maturity
```

Put-call parity is useful for checking pricing consistency.

---

## 46. Put-call parity intuition

Put-call parity says that certain combinations of calls, puts, stock and cash should produce equivalent payoffs.

If two portfolios have the same payoff at expiration, they should have the same price today.

Otherwise, arbitrage may exist.

Simple intuition:

```text
Same future payoff → same current value
```

If not, traders could buy the cheaper portfolio and sell the more expensive one.

Athena can use put-call parity as a model consistency check.

---

## 47. Arbitrage intuition

Arbitrage is a riskless profit opportunity created by price inconsistency.

In efficient markets, arbitrage opportunities should disappear quickly.

Example idea:

```text
Portfolio A and Portfolio B have identical future payoffs.
Portfolio A costs 100.
Portfolio B costs 105.
```

A trader could buy A and sell B.

Put-call parity is a no-arbitrage relationship.

Athena should not present arbitrage as guaranteed in real markets because transaction costs and liquidity matter. But the concept is essential for pricing logic.

---

## 48. Synthetic positions

Options can be combined with the underlying and cash to create synthetic exposures.

Examples:

```text
Synthetic stock
Synthetic call
Synthetic put
```

One relationship from put-call parity:

```text
Long call + short put + present value of strike ≈ long stock
```

Synthetic positions are useful because they show that options can replicate other payoffs.

For Athena's first version, this can be educational rather than deeply implemented.

---

## 49. Black-Scholes overview

Black-Scholes is a model used to price European options.

It gives theoretical prices for:

```text
European call options
European put options
```

The model uses:

```text
Spot price
Strike price
Time to maturity
Risk-free rate
Volatility
Dividend yield optional
```

Black-Scholes is not perfect, but it is a foundational model.

Athena's Options Pricing Lab can start with Black-Scholes because it is clear, testable and educational.

---

## 50. Black-Scholes purpose

The purpose of Black-Scholes is to estimate a fair theoretical option price.

It answers:

```text
Given the inputs, what should the option be worth under the model?
```

It does not guarantee that the market price will equal the model price.

Market prices can differ because of:

```text
Supply and demand
Implied volatility
Transaction costs
Liquidity
Dividends
Early exercise features
Market expectations
```

Athena should label the result as a **model price**.

---

## 51. Black-Scholes assumptions

Basic Black-Scholes assumptions include:

```text
European exercise
Constant volatility
Constant risk-free rate
Lognormal underlying price dynamics
No arbitrage
Frictionless markets
Continuous trading
No transaction costs
```

With dividends, a continuous dividend yield can be added.

Important:

These assumptions are simplifications.

Real markets have:

```text
Changing volatility
Transaction costs
Liquidity limits
Discrete dividends
Jumps
Early exercise
Volatility smiles
```

Athena should explain these limitations clearly.

---

## 52. Black-Scholes inputs

Main inputs:

```text
S = spot price
K = strike price
T = time to maturity
r = risk-free rate
sigma = volatility
q = dividend yield
```

Without dividends, q can be zero.

Example input:

```text
S = 100
K = 100
T = 1
r = 5%
sigma = 20%
q = 0%
```

Athena should validate that inputs are sensible:

```text
S > 0
K > 0
T > 0
sigma > 0
```

---

## 53. Spot price input

The spot price is the current price of the underlying asset.

In Black-Scholes:

```text
S = spot price
```

Example:

```text
S = 100
```

If the spot price increases, call values generally increase and put values generally decrease.

Athena should allow the user to input spot manually or use market data from the Market Data module.

---

## 54. Strike price input

The strike price is the exercise price.

In Black-Scholes:

```text
K = strike price
```

Example:

```text
K = 105
```

Strike strongly affects moneyness.

A call with low strike is more valuable than a call with high strike, all else equal.

A put with high strike is more valuable than a put with low strike, all else equal.

---

## 55. Time to maturity input

Time to maturity is usually expressed in years.

In Black-Scholes:

```text
T = time to maturity in years
```

Examples:

```text
1 year = 1.0
6 months = 0.5
3 months = 0.25
30 days ≈ 30 / 365
```

Time should be positive.

As expiration approaches, time value usually declines.

Athena should calculate this from the expiration date when possible.

---

## 56. Risk-free rate input

The risk-free rate is written as:

```text
r
```

It is usually expressed as an annual continuously compounded rate in the model.

Example:

```text
r = 0.05
```

meaning:

```text
5%
```

Athena can start with a simple annual rate input.

Later, it can pull the rate from the Rates Lab.

---

## 57. Volatility input

Volatility is written as:

```text
sigma
```

It is usually annualized.

Example:

```text
sigma = 0.20
```

meaning:

```text
20% annualized volatility
```

The volatility input can be:

```text
Realized volatility
Implied volatility
User assumption
```

For the first Athena version, user-provided volatility and realized volatility are enough.

---

## 58. Dividend yield input

Dividend yield is written as:

```text
q
```

It represents continuous dividend yield.

Example:

```text
q = 0.02
```

meaning:

```text
2% annual dividend yield
```

If the underlying pays no dividends, use:

```text
q = 0
```

Dividend yield lowers call prices and raises put prices, all else equal.

---

## 59. d1 intuition

In Black-Scholes, d1 is an intermediate variable.

Formula with dividends:

```text
d1 = [ln(S/K) + (r - q + 0.5σ²)T] / (σ√T)
```

Intuition:

```text
d1 combines moneyness, time, interest rates, dividends and volatility.
```

It helps calculate the call Delta and option value.

Do not think of d1 as a price.

It is a standardized quantity used inside the model.

---

## 60. d2 intuition

d2 is related to d1.

Formula:

```text
d2 = d1 - σ√T
```

Intuition:

```text
d2 adjusts d1 for volatility over the option's time horizon.
```

d2 appears in the Black-Scholes pricing formulas.

Like d1, d2 is not a price.

It is a model variable.

---

## 61. Black-Scholes call formula

With continuous dividend yield, the European call formula is:

```text
C = S e^(-qT) N(d1) - K e^(-rT) N(d2)
```

Where:

```text
C = call price
S = spot price
K = strike price
T = time to maturity
r = risk-free rate
q = dividend yield
N(.) = cumulative standard normal distribution
```

Without dividends:

```text
q = 0
```

Athena should return the call price and the intermediate values d1 and d2 for transparency.

---

## 62. Black-Scholes put formula

With continuous dividend yield, the European put formula is:

```text
P = K e^(-rT) N(-d2) - S e^(-qT) N(-d1)
```

Where:

```text
P = put price
```

The put formula uses the same inputs as the call formula.

Athena should return both call and put prices from the same input set.

---

## 63. Standard normal distribution role

Black-Scholes uses the cumulative standard normal distribution:

```text
N(d1)
N(d2)
N(-d1)
N(-d2)
```

These values convert d1 and d2 into probability-like weights under the model.

The user does not need to manually calculate N(d1).

Athena will do it.

For educational transparency, Athena can show:

```text
d1
d2
N(d1)
N(d2)
```

---

## 64. Black-Scholes call example

Example inputs:

```text
S = 100
K = 100
T = 1
r = 5%
sigma = 20%
q = 0%
```

Typical result:

```text
Call price ≈ 10.45
```

Interpretation:

```text
Under these assumptions, the theoretical European call price is about 10.45.
```

If volatility increases, the call price should increase.

If spot increases, the call price should increase.

Athena should include test cases for these relationships.

---

## 65. Black-Scholes put example

Using the same inputs:

```text
S = 100
K = 100
T = 1
r = 5%
sigma = 20%
q = 0%
```

Typical result:

```text
Put price ≈ 5.57
```

Interpretation:

```text
Under these assumptions, the theoretical European put price is about 5.57.
```

The call is more expensive than the put in this case partly because the risk-free rate is positive and there are no dividends.

---

## 66. Put-call parity check

For non-dividend European options:

```text
C - P = S - K e^(-rT)
```

Using the example:

```text
C ≈ 10.45
P ≈ 5.57
S = 100
K = 100
r = 5%
T = 1
```

Left side:

```text
C - P = 10.45 - 5.57 = 4.88
```

Right side:

```text
S - K e^(-rT) = 100 - 100e^(-0.05) ≈ 4.88
```

The parity approximately holds.

Athena should include a put-call parity check with a tolerance.

---

## 67. Black-Scholes limitations

Black-Scholes is foundational but limited.

Limitations include:

```text
Constant volatility assumption
Constant risk-free rate assumption
European exercise only
No transaction costs
Continuous trading assumption
Lognormal price assumption
Simplified dividend treatment
Does not explain volatility smile
```

Practical lesson:

```text
Black-Scholes is useful for learning and baseline pricing, but real market option prices may differ.
```

Athena should present Black-Scholes as a model, not as absolute truth.

---

## 68. What are the Greeks?

The Greeks measure sensitivities of option prices to different inputs.

Main Greeks:

```text
Delta
Gamma
Vega
Theta
Rho
```

Each Greek answers a different question.

```text
Delta = sensitivity to underlying price
Gamma = sensitivity of Delta
Vega = sensitivity to volatility
Theta = sensitivity to time passing
Rho = sensitivity to interest rates
```

Greeks are essential for option risk management.

---

## 69. Why Greeks matter

Option prices are nonlinear.

A simple price alone does not explain the risk.

Two options can have similar prices but very different sensitivities.

Greeks help answer:

```text
What happens if the underlying moves?
What happens if volatility changes?
What happens as time passes?
What happens if rates change?
```

Athena should display Greeks next to option prices.

The key idea is:

```text
Black-Scholes gives the price.
Greeks explain the risk.
```

---

## 70. Delta

Delta measures sensitivity of the option price to the underlying price.

Formula idea:

```text
Delta ≈ change in option price / change in underlying price
```

Example:

```text
Delta = 0.60
Underlying increases by 1

Option price increases by about 0.60
```

Delta is one of the most important Greeks.

It measures directional exposure.

---

## 71. Call Delta

Call Delta is usually between 0 and 1.

```text
0 < Call Delta < 1
```

Interpretation:

```text
Call Delta close to 1 = behaves almost like stock
Call Delta close to 0 = less sensitive to stock price
```

Example:

```text
Call Delta = 0.70
Stock rises by 2

Approximate call price change = 0.70 × 2 = 1.40
```

Call Delta is positive because calls benefit when the underlying rises.

---

## 72. Put Delta

Put Delta is usually between -1 and 0.

```text
-1 < Put Delta < 0
```

Interpretation:

```text
Put Delta is negative because put value usually falls when the underlying rises.
```

Example:

```text
Put Delta = -0.40
Stock rises by 2

Approximate put price change = -0.40 × 2 = -0.80
```

Put Delta is negative because puts benefit when the underlying falls.

---

## 73. Delta interpretation

Delta has multiple interpretations.

It can be viewed as:

```text
Price sensitivity
Hedge ratio
Approximate directional exposure
```

Example:

```text
A call with Delta 0.60 behaves roughly like 0.60 shares of stock for small movements.
```

But Delta changes as the underlying moves.

This is why Gamma matters.

Athena should not show Delta as a constant truth. It is local sensitivity.

---

## 74. Delta as hedge ratio

Delta can be used for hedging.

Example:

```text
Long 1 call option
Call Delta = 0.60
Contract size = 100
Position Delta = 60
```

This means the option position behaves approximately like 60 shares.

To delta hedge, one might short approximately 60 shares.

Athena can later show position Delta for option contracts.

First version can simply display Delta per option.

---

## 75. Gamma

Gamma measures how Delta changes when the underlying price changes.

Formula idea:

```text
Gamma ≈ change in Delta / change in underlying price
```

Example:

```text
Gamma = 0.05
Underlying increases by 1
Delta increases by about 0.05
```

Gamma is usually highest for options near at-the-money and close to expiration.

Gamma is a curvature measure.

---

## 76. Gamma interpretation

Gamma measures the curvature of the option price with respect to the underlying price.

Simple idea:

```text
Delta tells the slope.
Gamma tells how the slope changes.
```

High Gamma means Delta can change quickly.

This can create large nonlinear P&L effects.

Athena should display Gamma because it shows how unstable Delta is.

---

## 77. Delta-Gamma relationship

Delta gives a first-order approximation of option P&L.

Gamma adds a second-order correction.

Approximation:

```text
Option P&L ≈ Delta × ΔS + 0.5 × Gamma × (ΔS)^2
```

Example:

```text
Delta = 0.60
Gamma = 0.04
Underlying move = +2

P&L ≈ 0.60 × 2 + 0.5 × 0.04 × 2²
P&L ≈ 1.20 + 0.08
P&L ≈ 1.28
```

This is more accurate than Delta alone for larger moves.

---

## 78. Vega

Vega measures sensitivity to volatility.

Formula idea:

```text
Vega ≈ change in option price / change in volatility
```

Example:

```text
Vega = 0.20
Volatility increases by 1 percentage point

Option price increases by about 0.20
```

Vega is positive for standard long calls and long puts.

Why?

Long options benefit from more uncertainty.

---

## 79. Vega interpretation

Vega tells how exposed an option is to changes in volatility.

Example:

```text
Option price = 5
Vega = 0.30
Volatility increases from 20% to 21%

New price ≈ 5.30
```

Vega is important because volatility can change even if the underlying price does not move much.

Athena should include a Vega shock scenario.

---

## 80. Volatility risk

Volatility risk is the risk that option values change because volatility changes.

Example:

```text
Long option position
Volatility falls
Option price may fall even if the underlying does not move
```

For short options:

```text
Volatility rises
Short option position may lose value
```

Volatility risk is central to options.

This is different from the general volatility discussion in the market finance file because here volatility directly changes option value.

---

## 81. Theta

Theta measures sensitivity to the passage of time.

It is often called time decay.

Formula idea:

```text
Theta ≈ change in option price as one day passes
```

For long options, Theta is often negative.

Example:

```text
Theta = -0.05
One day passes

Option price decreases by about 0.05, all else equal
```

Theta is especially important for options close to expiration.

---

## 82. Theta interpretation

Theta measures how much time value is lost as expiration approaches.

Long options usually lose time value over time.

Short option sellers often benefit from time decay, but they take other risks.

Simple idea:

```text
Time passing usually hurts long option buyers.
Time passing usually helps option sellers.
```

This is not the only risk, but it is important.

---

## 83. Time decay

Time decay accelerates as expiration approaches, especially for at-the-money options.

Example:

```text
An at-the-money option with 6 months left may lose time value slowly.
An at-the-money option with 5 days left may lose time value quickly.
```

Time decay is one reason option buyers need not only to be right about direction, but also about timing.

Athena can show:

```text
Theta per day
Estimated decay over selected days
```

---

## 84. Rho

Rho measures sensitivity to interest rates.

Formula idea:

```text
Rho ≈ change in option price / change in interest rate
```

For calls:

```text
Rho is usually positive
```

For puts:

```text
Rho is usually negative
```

Rho is often less important than Delta, Gamma, Vega and Theta for short-dated equity options, but it still matters.

---

## 85. Rho interpretation

Rho tells how option value changes when the risk-free rate changes.

Example:

```text
Rho = 0.10
Interest rate increases by 1 percentage point

Call price increases by about 0.10
```

For long-maturity options, Rho can become more important.

Athena should calculate it, but it may not be the main focus at the start.

---

## 86. Interest rate sensitivity

Interest rates affect the present value of the strike payment.

For calls, higher rates can increase value because the strike payment is delayed.

For puts, higher rates can reduce value.

This is why Rho differs between calls and puts.

The detailed fixed income logic belongs in the Fixed Income file. Here, the rate is only used as a Black-Scholes input.

---

## 87. Greeks summary table

Athena should display a Greeks table.

Example:

```text
Greek | Meaning | Typical long call sign | Typical long put sign
Delta | Underlying price sensitivity | Positive | Negative
Gamma | Delta sensitivity | Positive | Positive
Vega  | Volatility sensitivity | Positive | Positive
Theta | Time decay | Usually negative | Usually negative
Rho   | Rate sensitivity | Usually positive | Usually negative
```

This table makes option risk easier to understand.

A user should be able to read this table and understand the main risk drivers of the option.

---

## 88. Greeks by moneyness

Greeks change depending on moneyness.

### Delta

Call Delta:

```text
Deep out of the money → close to 0
At the money → around 0.5
Deep in the money → close to 1
```

Put Delta:

```text
Deep out of the money → close to 0
At the money → around -0.5
Deep in the money → close to -1
```

### Gamma

Gamma is usually highest near at-the-money.

Moneyness strongly affects option risk.

---

## 89. Greeks by time to maturity

Time to maturity affects Greeks.

### Gamma

Gamma can become very high near expiration for at-the-money options.

### Theta

Theta often accelerates near expiration.

### Vega

Vega is usually higher for longer-dated options.

Simple idea:

```text
Short-dated options can have high Gamma and high Theta.
Longer-dated options often have more Vega.
```

Athena can later show how Greeks change as expiration approaches.

---

## 90. Greeks by volatility

Volatility affects option price and Greeks.

Higher volatility can:

```text
Increase option prices
Change Delta behavior
Affect Gamma
Increase Vega exposure
Alter time value
```

Vega is especially important when volatility is uncertain.

Athena can later show sensitivity charts:

```text
Option price vs volatility
Vega by volatility level
```

This would make the Options Pricing Lab more educational.

---

## 91. Option P&L intuition

Option P&L can come from several sources:

```text
Underlying price movement
Volatility change
Time decay
Interest rate change
Dividends
```

Greeks help approximate these sources.

A simplified P&L view:

```text
Option P&L ≈ Delta effect + Gamma effect + Vega effect + Theta effect + Rho effect
```

This is not exact, but it is useful for understanding option risk.

---

## 92. Delta approximation of P&L

Delta approximation:

```text
Option P&L ≈ Delta × Change in underlying price
```

Example:

```text
Delta = 0.60
Underlying change = +3

Option P&L ≈ 0.60 × 3
Option P&L ≈ +1.80
```

This works best for small underlying moves.

For larger moves, Gamma becomes important.

Athena can include this in an option scenario panel.

---

## 93. Delta-Gamma approximation of P&L

Delta-Gamma approximation:

```text
Option P&L ≈ Delta × ΔS + 0.5 × Gamma × (ΔS)^2
```

Example:

```text
Delta = 0.60
Gamma = 0.04
Underlying change = +3

P&L ≈ 0.60 × 3 + 0.5 × 0.04 × 3²
P&L ≈ 1.80 + 0.18
P&L ≈ 1.98
```

This improves the approximation by including curvature.

It is still an approximation, not a full repricing.

---

## 94. Vega impact on P&L

Vega approximation:

```text
Option P&L ≈ Vega × Change in volatility
```

Example:

```text
Vega = 0.25
Volatility increases by 2 percentage points

Vega P&L ≈ 0.25 × 2
Vega P&L ≈ 0.50
```

Important: this assumes Vega is quoted per 1 percentage point volatility change.

Athena should document the convention used.

---

## 95. Theta impact on P&L

Theta approximation:

```text
Option P&L ≈ Theta × days passed
```

Example:

```text
Theta = -0.04 per day
Days passed = 5

Theta P&L ≈ -0.04 × 5
Theta P&L ≈ -0.20
```

This means the option loses about 0.20 from time decay, all else equal.

Theta is especially important for short-dated options.

---

## 96. Basic option strategies

This section introduces basic strategies without going too deep.

Examples:

```text
Covered call
Protective put
Straddle
Strangle
Spread strategies
```

### Covered call

Own the underlying and sell a call.

Purpose:

```text
Generate income
```

Risk:

```text
Upside is capped
Underlying downside remains
```

### Protective put

Own the underlying and buy a put.

Purpose:

```text
Downside protection
```

Risk:

```text
Premium cost reduces return
```

### Straddle

Buy a call and a put with the same strike and expiration.

Purpose:

```text
Benefit from large movement in either direction
```

### Strangle

Buy an out-of-the-money call and an out-of-the-money put.

Purpose:

```text
Cheaper volatility exposure than a straddle
```

Athena's first version does not need to implement all strategies. It can start with single-option pricing.

---

## 97. Option risk management

Option risk management uses Greeks to monitor sensitivities.

Important exposures:

```text
Delta exposure
Gamma exposure
Vega exposure
Theta exposure
Rho exposure
```

Example portfolio exposure:

```text
Total Delta = +250
Total Gamma = +15
Total Vega = +800
Total Theta = -120
Total Rho = +50
```

This tells the user how the option portfolio may react to market changes.

Athena can later aggregate Greeks across option positions.

For the first version, Athena should calculate Greeks for one option at a time.

---

## 98. Possible API endpoints

Possible Athena endpoints:

```text
POST /api/options/black-scholes/price
POST /api/options/black-scholes/call
POST /api/options/black-scholes/put
POST /api/options/black-scholes/greeks
POST /api/options/payoff
POST /api/options/profit
POST /api/options/put-call-parity
POST /api/options/scenario
POST /api/options/pnl-approximation
```

Example request:

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

Example response:

```json
{
  "call_price": 10.45,
  "put_price": 5.57,
  "d1": 0.35,
  "d2": 0.15,
  "greeks": {
    "call_delta": 0.64,
    "put_delta": -0.36,
    "gamma": 0.0188,
    "vega": 37.52,
    "call_theta": -6.41,
    "put_theta": -1.66,
    "call_rho": 53.23,
    "put_rho": -41.89
  }
}
```

---

## 99. Possible frontend components and tests

Possible frontend components:

```text
OptionPricingForm
CallPriceCard
PutPriceCard
GreeksTable
PayoffChart
ProfitLossChart
MoneynessBadge
PutCallParityCheck
SensitivityChart
DeltaGammaPanel
VegaThetaPanel
ThetaDecayPanel
OptionScenarioPanel
```

Suggested tests:

```text
Call price is positive
Put price is positive
Call price increases when spot increases
Put price decreases when spot increases
Call price decreases when strike increases
Put price increases when strike increases
Option price increases when volatility increases
Call Delta is between 0 and 1
Put Delta is between -1 and 0
Gamma is positive for standard European options
Vega is positive for long standard options
Theta is usually negative for long standard options
Put-call parity holds approximately
Call payoff is correct at expiration
Put payoff is correct at expiration
Intrinsic value is never negative
Breakeven is calculated correctly
```

Athena should include deterministic tests with known Black-Scholes values.

---

## 100. How Athena uses options and Greeks

Athena AI Risk Terminal should use this document to build the **Options Pricing Lab**.

Main features:

```text
Black-Scholes pricing
Call and put prices
d1 and d2
Put-call parity check
Greeks table
Payoff chart
Profit chart
Sensitivity analysis
Option scenario panel
Basic option P&L approximation
```

Possible workflow:

```text
1. User enters option inputs.
2. Athena validates the inputs.
3. Athena calculates d1 and d2.
4. Athena calculates call and put prices.
5. Athena calculates Greeks.
6. Athena checks put-call parity.
7. Athena displays payoff and profit charts.
8. Athena shows sensitivity to spot, volatility and time.
```

Key lesson:

```text
The option price is only the starting point.
The Greeks explain the risk.
```

For Athena, this is the most important message:

```text
Black-Scholes prices the option.
Greeks explain how the option price reacts.
Athena should show both.
```
