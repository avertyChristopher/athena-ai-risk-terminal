# 01 — Market Finance and Volatility

**Project:** Athena AI Risk Terminal  
**Recommended file path:** `docs/finance/01-market-finance-volatility.md`  
**Purpose:** build a strong foundation in market finance, asset classes, market data, returns, volatility, distributions, liquidity, benchmarks and data quality.  
**Scope:** this document focuses only on market finance and volatility. Other finance areas are documented separately.

---

## Table of Contents

1. What is market finance?
2. Main asset classes
3. Stocks
4. ETFs
5. Market indices
6. Currencies
7. Commodities
8. Market data
9. OHLCV data
10. Adjusted close and corporate actions
11. Volume
12. Price vs return
13. Holding Period Return
14. Simple returns
15. Log returns
16. Arithmetic vs geometric returns
17. Total return
18. Compounding and annualization
19. Volatility
20. Daily volatility
21. Annualized volatility
22. Rolling volatility
23. Realized volatility
24. Implied volatility
25. Variance and standard deviation
26. Return distributions
27. Skewness and kurtosis
28. Normal distribution and fat tails
29. Correlation
30. Covariance
31. Liquidity
32. Bid, ask and bid-ask spread
33. Order types and market microstructure
34. Benchmark
35. Index construction basics
36. Market efficiency basics
37. Nominal vs real returns
38. Data quality
39. Missing data
40. Outliers
41. Currency consistency
42. Data frequency
43. Key formulas
44. Possible API endpoints
45. Possible frontend components
46. Suggested tests
47. Common beginner mistakes
48. Summary

---

## 1. What is market finance?

Market finance studies financial instruments traded on financial markets and how their prices evolve over time.

It focuses on questions such as:

- What is the current price of an asset?
- What makes the asset price move?
- How much return did the asset generate?
- How volatile is the asset?
- How liquid is the asset?
- How does the asset behave compared with other assets?
- How reliable is the market data used for analysis?

In a financial platform such as Athena AI Risk Terminal, market finance is the base layer. Before calculating anything more advanced, the system needs clean asset data, clean price data and a correct understanding of returns.

A simple view of the logic is:

```text
Assets
  ↓
Market prices
  ↓
Returns
  ↓
Volatility, correlation and liquidity
  ↓
Market analysis
```

Market finance is therefore not just about reading stock prices. It is about transforming raw market observations into useful financial information.

---

## 2. Main asset classes

An asset class is a category of financial instruments with similar economic characteristics.

The main asset classes are:

```text
Equities
Fixed income
Currencies
Commodities
Derivatives
Cash and money market instruments
Alternative investments
```

This document introduces them from a market data perspective.

### Equities

Equities represent ownership in companies. A stock is an equity instrument.

Example:

```text
AAPL = Apple Inc.
MSFT = Microsoft Corporation
```

### Fixed income

Fixed income instruments are debt instruments. A bond is the most common example.

Example:

```text
Government bond
Corporate bond
Treasury bill
```

### Currencies

Currencies are traded through exchange rates.

Example:

```text
EUR/USD
USD/CAD
```

### Commodities

Commodities are physical goods traded on markets.

Example:

```text
Oil
Gold
Copper
Wheat
```

### Derivatives

Derivatives are financial contracts whose value depends on an underlying asset.

Example:

```text
Options
Futures
Swaps
```

### Cash and money market instruments

These are short-term, highly liquid instruments.

Example:

```text
Cash
Treasury bills
Commercial paper
```

### Alternative investments

Alternative investments include assets outside traditional public stocks and bonds.

Example:

```text
Private equity
Real estate
Hedge funds
Infrastructure
```

In Athena AI Risk Terminal, the first version can focus on equities and ETFs, then progressively support other asset types.

---

## 3. Stocks

A stock represents ownership in a company.

When someone buys a stock, they own a small part of the company. The stock price reflects the market's changing expectations about the company and its future.

A stock price can move because of:

- earnings results;
- revenue growth;
- interest rates;
- economic news;
- sector trends;
- company-specific news;
- investor sentiment;
- market liquidity;
- geopolitical events.

Example stock record:

```text
symbol: AAPL
name: Apple Inc.
asset_type: equity
currency: USD
exchange: NASDAQ
sector: Technology
country: United States
```

### Common stock metrics

Important stock-related fields include:

```text
Market price
Market capitalization
Volume
Dividend yield
Sector
Country
Currency
Exchange
```

### Price vs value

A stock price is what the market currently pays.  
A stock value is an estimate of what the asset is worth.

These two are not always equal.

```text
Price = observable market quote
Value = analytical estimate
```

Athena should store market prices but should also make it possible to calculate returns, volatility and other market behavior metrics from those prices.

---

## 4. ETFs

An ETF, or exchange-traded fund, is a fund traded on an exchange like a stock.

An ETF usually tracks a basket of assets.

Examples:

```text
SPY = tracks the S&P 500
QQQ = tracks the Nasdaq-100
XIU = tracks Canadian large-cap equities
```

ETFs are useful because they provide diversified exposure through one tradable instrument.

### Why ETFs matter

ETFs are important because they can represent:

- equity market exposure;
- sector exposure;
- country exposure;
- bond exposure;
- commodity exposure;
- currency exposure;
- factor exposure.

Example:

```text
Buying SPY gives broad exposure to large US companies.
Buying QQQ gives exposure to large Nasdaq-listed companies.
```

### ETF analysis

For Athena, ETFs can be treated similarly to stocks from a market data perspective:

```text
symbol
name
price
adjusted close
volume
returns
volatility
correlation
```

However, ETFs also have an underlying composition. A more advanced version could analyze the holdings inside an ETF, but this is not required for the first version.

---

## 5. Market indices

A market index measures the performance of a group of securities.

Examples:

```text
S&P 500
Nasdaq-100
Dow Jones Industrial Average
TSX Composite
CAC 40
FTSE 100
Nikkei 225
```

An index is not always directly tradable, but ETFs and futures can track it.

### Why indices matter

Indices are used for:

- measuring market performance;
- comparing portfolios;
- building benchmarks;
- understanding sectors or regions;
- tracking economic sentiment.

### Index return

An index return measures the percentage change in the index level.

Example:

```text
Index level yesterday = 5000
Index level today     = 5050

Return = 5050 / 5000 - 1 = 1%
```

### Price return vs total return index

A price return index tracks price changes only.

A total return index includes price changes plus income such as dividends.

This distinction matters because long-term performance can look very different depending on whether income is included.

```text
Price return index = price movement only
Total return index = price movement + reinvested income
```

---

## 6. Currencies

Currencies are traded through exchange rates.

Examples:

```text
EUR/USD
USD/CAD
GBP/USD
USD/JPY
```

An exchange rate expresses the value of one currency in terms of another.

Example:

```text
USD/CAD = 1.35
```

This means:

```text
1 USD = 1.35 CAD
```

### Base currency and quote currency

In a currency pair:

```text
EUR/USD
```

EUR is the base currency.  
USD is the quote currency.

If EUR/USD = 1.10, then:

```text
1 EUR = 1.10 USD
```

### Why currencies matter

Currencies matter when:

- assets are priced in different currencies;
- a portfolio reports values in one base currency;
- investors face foreign exchange risk;
- returns must be converted into a common currency.

Example:

```text
A Canadian investor buys a US stock.
The stock return depends on the stock price movement and the USD/CAD exchange rate.
```

In Athena, every asset should have an explicit currency field.

---

## 7. Commodities

Commodities are physical goods traded on markets.

Examples:

```text
Oil
Gold
Natural gas
Copper
Wheat
Corn
Silver
```

Commodity prices are often influenced by supply and demand dynamics.

### Main drivers of commodity prices

Commodity prices can move because of:

- production levels;
- storage levels;
- geopolitical events;
- weather;
- transportation costs;
- global demand;
- currency movements;
- interest rates;
- speculation.

### Spot and futures prices

Commodities are often traded through futures contracts.

A spot price is the current price for immediate delivery.  
A futures price is the price agreed today for delivery at a future date.

For a first version of Athena, commodities can be represented using ETFs or simple price series.

---

## 8. Market data

Market data is information about financial instruments observed in the market.

Common market data includes:

```text
Date
Open price
High price
Low price
Close price
Adjusted close
Volume
Bid
Ask
Currency
Exchange
```

Good market data is essential. If the data is wrong, every calculation built on it can become wrong.

### Raw data vs cleaned data

Raw data is data as collected from a provider.

Cleaned data is data after validation and correction.

Examples of cleaning steps:

- remove duplicate rows;
- handle missing prices;
- adjust for corporate actions;
- validate currencies;
- detect suspicious outliers;
- align dates across assets.

### Market data in Athena

Athena should treat market data as a core input.

Possible data entities:

```text
Asset
MarketPrice
MarketMetric
DataQualityWarning
```

The system should not blindly trust input data. It should validate it before using it.

---

## 9. OHLCV data

OHLCV means:

```text
Open
High
Low
Close
Volume
```

These are the most common daily market data fields.

### Open

The first traded price of the session.

### High

The highest traded price during the session.

### Low

The lowest traded price during the session.

### Close

The last traded price of the session.

### Volume

The number of shares or contracts traded during the session.

Example:

```text
Date:   2026-04-29
Open:   100.00
High:   104.50
Low:     98.80
Close:  102.30
Volume: 5,000,000
```

### Why OHLCV matters

OHLCV data helps analyze:

- daily price movement;
- volatility;
- trading activity;
- liquidity;
- possible gaps;
- abnormal market behavior.

Close or adjusted close prices are often used to calculate daily returns.

---

## 10. Adjusted close and corporate actions

The adjusted close corrects historical prices for corporate actions.

Corporate actions include:

```text
Dividends
Stock splits
Reverse splits
Special dividends
Spin-offs
Rights issues
Distributions
```

### Why adjusted close matters

If a company pays a dividend, the stock price may drop mechanically after the dividend date. This drop does not necessarily mean the investor lost value, because the investor also received the dividend.

The adjusted close tries to reflect the economic return more accurately.

### Stock split example

Suppose a stock trades at 200 and then has a 2-for-1 split.

After the split, the price may become 100, but the investor owns twice as many shares.

Without adjustment, the price series would show a false -50% move.

### Practical rule

```text
Use adjusted close for return calculations when available.
Use raw close only when there is a specific reason.
Document the chosen price field.
```

In Athena, market data processing should identify whether returns are based on close or adjusted close.

---

## 11. Volume

Volume is the number of shares or contracts traded during a period.

Example:

```text
Volume = 5,000,000 shares
```

This means 5 million shares were traded during the session.

### Why volume matters

Volume helps evaluate:

- liquidity;
- trading activity;
- market interest;
- possible abnormal events;
- reliability of price movements.

A price move with high volume may be more meaningful than a price move with very low volume.

### Volume and liquidity

High volume often means the asset is easier to trade.

Low volume can mean:

- wider bid-ask spreads;
- higher transaction costs;
- difficulty entering or exiting positions;
- higher slippage.

In Athena, volume can be used as a simple liquidity indicator.

---

## 12. Price vs return

A price is the value of an asset at a specific point in time.

A return measures the percentage change in value between two points in time.

For analysis, returns are often more useful than prices because returns are comparable across assets.

### Example

```text
Asset A moves from 100 to 105.
Asset B moves from 20 to 21.
```

Both assets generated a 5% return.

Even though the price levels are different, the economic movement is the same in percentage terms.

### Why returns matter

Returns are used to calculate:

- performance;
- volatility;
- correlation;
- distributions;
- risk metrics;
- benchmark comparison.

In Athena, most market analytics should be built from returns rather than raw price levels.

---

## 13. Holding Period Return

Holding Period Return, or HPR, measures the total return earned over a specific holding period.

Formula:

```text
HPR = (Ending Value - Beginning Value + Income) / Beginning Value
```

Where income can include:

```text
Dividends
Coupons
Distributions
```

### Example

```text
Beginning price = 100
Ending price    = 105
Dividend        = 2

HPR = (105 - 100 + 2) / 100
HPR = 7 / 100
HPR = 7%
```

### Why HPR matters

Holding Period Return is important because it includes both:

- capital gain or loss;
- income received during the holding period.

A price return may ignore income. HPR gives a more complete view of return.

---

## 14. Simple returns

A simple return measures the percentage change between two prices.

Formula:

```text
Return_t = (Price_t - Price_{t-1}) / Price_{t-1}
```

Equivalent formula:

```text
Return_t = Price_t / Price_{t-1} - 1
```

### Positive return example

```text
Initial price = 100
Final price   = 105

Return = 105 / 100 - 1
Return = 0.05
Return = 5%
```

### Negative return example

```text
Initial price = 100
Final price   = 92

Return = 92 / 100 - 1
Return = -0.08
Return = -8%
```

### Advantages

Simple returns are:

- intuitive;
- easy to explain;
- useful for reporting;
- useful for dashboards.

### Limitation

Simple returns do not add cleanly over time.

Example:

```text
Return day 1 = +10%
Return day 2 = -10%
```

The total return is not exactly 0%.

---

## 15. Log returns

Log returns use the natural logarithm.

Formula:

```text
LogReturn_t = ln(Price_t / Price_{t-1})
```

### Example

```text
Initial price = 100
Final price   = 105

LogReturn = ln(105 / 100)
LogReturn ≈ 0.0488
LogReturn ≈ 4.88%
```

### Why log returns are useful

Log returns are useful because they are additive over time.

If:

```text
Day 1 log return = 1%
Day 2 log return = 2%
```

Then the two-day log return is approximately:

```text
3%
```

### Practical rule

```text
Simple returns are better for interpretation.
Log returns are often useful for modeling.
```

In Athena, the chosen return type should always be clear in the code and documentation.

---

## 16. Arithmetic vs geometric returns

Returns can be averaged in different ways.

The two most important methods are:

```text
Arithmetic mean return
Geometric mean return
```

### Arithmetic mean return

The arithmetic mean is the simple average of periodic returns.

Formula:

```text
Arithmetic mean = (R1 + R2 + ... + Rn) / n
```

Example:

```text
Year 1 return = +10%
Year 2 return = -5%

Arithmetic mean = (10% - 5%) / 2
Arithmetic mean = 2.5%
```

### Geometric mean return

The geometric mean measures the compounded average return.

Formula:

```text
Geometric mean = [(1 + R1)(1 + R2)...(1 + Rn)]^(1/n) - 1
```

Example:

```text
Year 1 return = +10%
Year 2 return = -5%

Geometric mean = [(1.10)(0.95)]^(1/2) - 1
Geometric mean ≈ 2.23%
```

### Key difference

The arithmetic mean is usually higher than the geometric mean when returns are volatile.

```text
Arithmetic mean = average periodic return
Geometric mean  = compounded average return
```

The geometric mean is more relevant for long-term realized performance.

---

## 17. Total return

Total return includes both price change and income.

Formula:

```text
Total return = price return + income return
```

More explicitly:

```text
Total return = (Ending price - Beginning price + Income) / Beginning price
```

Income can include:

```text
Dividends
Coupons
Distributions
```

### Price return

Price return only considers the change in price.

```text
Price return = (Ending price - Beginning price) / Beginning price
```

### Income return

Income return measures income received relative to the beginning value.

```text
Income return = Income / Beginning price
```

### Example

```text
Beginning price = 100
Ending price    = 104
Dividend        = 3

Price return = 4 / 100 = 4%
Income return = 3 / 100 = 3%
Total return = 7%
```

For market analysis, total return is often more complete than price return.

---

## 18. Compounding and annualization

Compounding means that returns accumulate over time by reinvesting gains.

If an investment grows by 10%, then loses 10%, it does not return exactly to the original value.

Example:

```text
Initial value = 100
After +10%    = 110
After -10%    = 99
```

The total return is:

```text
-1%
```

not 0%.

### Annualized return

Annualized return expresses a multi-period return as a yearly rate.

Formula:

```text
Annualized return = (Ending value / Beginning value)^(1 / years) - 1
```

### Example

```text
Beginning value = 100
Ending value    = 121
Time            = 2 years

Annualized return = (121 / 100)^(1/2) - 1
Annualized return = 10%
```

### Annualizing volatility

Volatility is annualized differently from returns.

For daily volatility:

```text
Annualized volatility = Daily volatility * sqrt(252)
```

This square-root rule comes from the way variance scales with time under simplifying assumptions.

---

## 19. Volatility

Volatility measures how much returns move around their average.

If returns move a lot, volatility is high.  
If returns are stable, volatility is low.

Volatility is one of the most important concepts in market finance because it measures uncertainty.

### Important distinction

```text
Volatility measures movement.
Volatility does not only mean loss.
```

An asset can be volatile because it moves strongly upward and downward.

### Low volatility example

```text
Day 1: +0.1%
Day 2: -0.2%
Day 3: +0.1%
Day 4: +0.0%
```

### High volatility example

```text
Day 1: +5%
Day 2: -6%
Day 3: +4%
Day 4: -7%
```

The second asset is more unstable and uncertain.

---

## 20. Daily volatility

Daily volatility is usually calculated as the standard deviation of daily returns.

Formula:

```text
Daily volatility = standard_deviation(daily_returns)
```

If daily returns are very close to their average, daily volatility is low.  
If daily returns are far from their average, daily volatility is high.

### Example interpretation

```text
Daily volatility = 1%
```

This means daily returns typically move around their average by about 1%, under a simplified interpretation.

Daily volatility is useful as a building block, but it is often converted into annualized volatility for comparison.

---

## 21. Annualized volatility

Annualized volatility converts daily volatility into a yearly measure.

Formula:

```text
Annualized volatility = Daily volatility * sqrt(252)
```

Why 252?

Because there are approximately 252 trading days in a year.

### Example

```text
Daily volatility = 1%

Annualized volatility = 1% * sqrt(252)
Annualized volatility ≈ 15.87%
```

### Why annualized volatility matters

Annualized volatility makes it easier to compare assets over a common horizon.

Example:

```text
Asset A annualized volatility = 12%
Asset B annualized volatility = 35%
```

Asset B is more volatile.

---

## 22. Rolling volatility

Rolling volatility is calculated over a moving window.

Common windows:

```text
20 days
60 days
252 days
```

### Example

A 20-day rolling volatility uses the most recent 20 daily returns.

Then the window moves forward one day, and the calculation is repeated.

### Why rolling volatility matters

Volatility changes over time.

A calm asset can become volatile during market stress.  
A volatile asset can become calmer after uncertainty decreases.

Rolling volatility helps detect changing market conditions.

### Practical interpretation

```text
20-day volatility = short-term behavior
60-day volatility = medium-term behavior
252-day volatility = one-year behavior
```

---

## 23. Realized volatility

Realized volatility is calculated from historical returns.

It answers:

```text
How volatile was the asset in the past?
```

It is backward-looking.

Realized volatility can be calculated over different windows:

```text
20-day realized volatility
60-day realized volatility
252-day realized volatility
```

### Use case

Realized volatility is useful when the system needs a volatility estimate based only on observed price behavior.

It is simple, transparent and easy to test.

---

## 24. Implied volatility

Implied volatility is extracted from market prices of options.

It reflects the volatility that the market appears to expect in the future.

### Realized vs implied volatility

```text
Realized volatility = based on historical returns
Implied volatility  = implied by option prices
```

Realized volatility looks backward.  
Implied volatility looks forward through market expectations.

### Why implied volatility matters

Implied volatility can rise even if realized volatility has not yet increased.

This can happen when investors expect future uncertainty.

In Athena, implied volatility can be added later. The first version can start with realized volatility.

---

## 25. Variance and standard deviation

Variance and standard deviation are basic measures of dispersion.

### Variance

Variance measures the average squared deviation from the mean.

Conceptually:

```text
Variance = average squared distance from the mean return
```

### Standard deviation

Standard deviation is the square root of variance.

```text
Standard deviation = sqrt(variance)
```

In finance, standard deviation of returns is commonly called volatility.

### Why standard deviation is easier to interpret

Variance is expressed in squared units.  
Standard deviation is expressed in the same unit as returns.

Example:

```text
Standard deviation = 2%
```

This is easier to interpret than a variance of:

```text
0.0004
```

---

## 26. Return distributions

A return distribution shows how returns are spread across possible outcomes.

It can show:

- average return;
- volatility;
- extreme losses;
- extreme gains;
- asymmetry;
- tail behavior.

### Example

A return distribution may show that most daily returns are between:

```text
-1% and +1%
```

but occasionally returns may be:

```text
-5% or +6%
```

### Why distributions matter

Looking only at average return is not enough.

Two assets can have the same average return but very different risk profiles.

Example:

```text
Asset A average return = 5%, stable
Asset B average return = 5%, very volatile
```

The average is the same, but the experience is very different.

---

## 27. Skewness and kurtosis

Skewness and kurtosis describe the shape of a return distribution.

### Skewness

Skewness measures asymmetry.

```text
Positive skewness = more extreme positive outcomes
Negative skewness = more extreme negative outcomes
```

Negative skewness is important because it may indicate large downside events.

### Kurtosis

Kurtosis measures the weight of the tails of a distribution.

High kurtosis means extreme events occur more often than expected under a normal distribution.

### Why they matter

Financial returns often show:

```text
fat tails
asymmetry
large extreme events
```

This means that average return and volatility do not tell the full story.

---

## 28. Normal distribution and fat tails

The normal distribution is a common statistical model.

It is symmetric and described by:

```text
mean
standard deviation
```

However, financial returns are often not perfectly normal.

### Normal distribution limitation

A normal distribution can underestimate extreme events.

In markets, large losses and large gains can happen more often than a normal model suggests.

This phenomenon is often called:

```text
fat tails
```

### Practical implication

Models based only on normal assumptions should be used carefully.

In Athena, market analytics should make it clear when a calculation assumes normality and when it uses historical data directly.

---

## 29. Correlation

Correlation measures how two assets move together.

It ranges from -1 to +1.

```text
+1  = assets move perfectly together
 0  = no clear linear relationship
-1  = assets move perfectly in opposite directions
```

### Example

If AAPL and MSFT often rise and fall together, their correlation is likely positive.

If one asset tends to rise when another falls, their correlation may be negative.

### Why correlation matters

Correlation helps understand diversification.

A portfolio with many assets is not necessarily diversified if all assets move together.

---

## 30. Covariance

Covariance measures the joint movement of two assets.

Basic interpretation:

```text
Positive covariance = assets tend to move in the same direction
Negative covariance = assets tend to move in opposite directions
Near zero covariance = weak joint movement
```

### Covariance vs correlation

Covariance depends on the scale of returns.  
Correlation is standardized between -1 and +1.

Because of this, correlation is usually easier to interpret.

### Use in finance

Covariance is useful in portfolio calculations because it helps measure how assets contribute to total portfolio variability.

---

## 31. Liquidity

Liquidity measures how easy it is to buy or sell an asset without strongly affecting its price.

A liquid asset usually has:

- high trading volume;
- many buyers and sellers;
- narrow bid-ask spread;
- fast execution.

An illiquid asset may have:

- low volume;
- few market participants;
- wide bid-ask spread;
- high transaction costs;
- large price impact.

### Why liquidity matters

An asset can look attractive based on price history but be difficult to trade in practice.

Liquidity is especially important during stressed market conditions.

---

## 32. Bid, ask and bid-ask spread

The bid is the price buyers are willing to pay.

The ask is the price sellers are willing to accept.

```text
Bid = price offered by buyers
Ask = price requested by sellers
```

The bid-ask spread is:

```text
Spread = Ask - Bid
```

### Example

```text
Bid = 99.95
Ask = 100.05

Spread = 0.10
```

### Interpretation

A small spread usually indicates good liquidity.  
A large spread usually indicates higher trading cost.

The spread is an implicit cost of trading.

---

## 33. Order types and market microstructure

Market microstructure studies how trading actually happens in markets.

Basic order types include:

```text
Market order
Limit order
Stop order
Stop-limit order
```

### Market order

A market order executes immediately at the best available price.

Advantage:

```text
Fast execution
```

Disadvantage:

```text
Execution price is uncertain
```

### Limit order

A limit order sets a maximum buying price or minimum selling price.

Advantage:

```text
Price control
```

Disadvantage:

```text
Execution is not guaranteed
```

### Stop order

A stop order becomes active when a specified stop price is reached.

It is often used for risk control or trade automation.

### Slippage

Slippage is the difference between expected execution price and actual execution price.

```text
Slippage = actual execution price - expected execution price
```

Slippage is more likely when liquidity is low or markets move quickly.

---

## 34. Benchmark

A benchmark is a reference used to evaluate performance.

Examples:

```text
S&P 500
Nasdaq-100
TSX Composite
CAC 40
```

### Why benchmarks matter

Performance needs context.

Example:

```text
Portfolio return = +8%
Benchmark return = +12%
```

The portfolio made money but underperformed.

Another example:

```text
Portfolio return = -3%
Benchmark return = -10%
```

The portfolio lost money but outperformed the benchmark.

### Benchmark selection

A good benchmark should be:

- relevant;
- investable or representative;
- transparent;
- consistent with the strategy;
- appropriate for the asset universe.

---

## 35. Index construction basics

Indices can be built in different ways.

The construction method affects index behavior.

### Price-weighted index

In a price-weighted index, higher-priced stocks have more influence.

Example:

```text
A stock priced at 300 has more impact than a stock priced at 50.
```

### Market-cap-weighted index

In a market-cap-weighted index, larger companies have more influence.

Market capitalization is:

```text
Market cap = share price * number of shares outstanding
```

This is the most common index construction method.

### Equal-weighted index

In an equal-weighted index, every constituent has the same weight.

Example:

```text
100 stocks
Each stock weight = 1%
```

### Price return vs total return index

A price return index includes only price changes.  
A total return index includes price changes and reinvested income.

This distinction is important for long-term analysis.

---

## 36. Market efficiency basics

Market efficiency describes how quickly and accurately market prices reflect information.

### Basic idea

If markets are efficient, prices already reflect available information.

This makes it difficult to consistently outperform the market without taking additional risk or having an informational advantage.

### Forms of market efficiency

Common forms:

```text
Weak form
Semi-strong form
Strong form
```

### Weak form

Prices reflect past market data.

If weak-form efficiency holds, historical prices alone should not reliably predict future returns.

### Semi-strong form

Prices reflect all publicly available information.

If semi-strong efficiency holds, public news is quickly incorporated into prices.

### Strong form

Prices reflect all public and private information.

This is the strongest and most unrealistic form in practice.

### Active vs passive investing

Market efficiency is one reason passive investing exists.

If it is difficult to beat the market, some investors choose to track the market instead of trying to outperform it.

---

## 37. Nominal vs real returns

A nominal return is the return before adjusting for inflation.

A real return is the return after adjusting for inflation.

Approximate formula:

```text
Real return ≈ Nominal return - Inflation
```

More exact formula:

```text
Real return = (1 + nominal return) / (1 + inflation) - 1
```

### Example

```text
Nominal return = 8%
Inflation      = 3%

Approximate real return = 8% - 3% = 5%
```

### Why real returns matter

Nominal gains do not always mean purchasing power increased.

If inflation is high, a positive nominal return can still produce a weak real return.

---

## 38. Data quality

Bad market data produces bad analysis.

Common data problems include:

- missing prices;
- duplicated dates;
- wrong currency;
- wrong ticker;
- unadjusted prices;
- stale prices;
- extreme outliers;
- inconsistent time zones;
- mixed data frequencies.

A serious financial application should validate market data before using it.

### Data quality checks

Possible checks:

```text
No negative prices
No duplicated dates
No impossible volume values
No missing adjusted close for required calculations
Currency is defined
Exchange is defined
Asset type is defined
```

In Athena, data quality warnings should be visible to the user.

---

## 39. Missing data

Missing data can break calculations or distort results.

Example:

```text
Date        Price
2026-01-01  100
2026-01-02  missing
2026-01-03  103
```

Possible treatments:

- remove missing observations;
- forward-fill carefully;
- interpolate only when justified;
- reject the asset if data quality is too poor;
- display a warning.

### Forward-fill caution

Forward-filling means using the last known value.

Example:

```text
Missing price on Jan 2 is filled with Jan 1 price.
```

This can be useful, but it can also artificially reduce volatility.

Therefore, the method must be documented.

---

## 40. Outliers

An outlier is an abnormal observation.

It can be:

- a real market event;
- a data error.

### Example of real event

```text
Daily return = -20%
```

This may be a true crash or earnings shock.

### Example of data error

```text
Price moves from 100 to 0 and then back to 101.
```

This is likely a data issue.

### Practical rule

```text
Flag outliers first.
Investigate before removing them.
Do not silently delete extreme observations.
```

---

## 41. Currency consistency

Every asset price must have a currency.

Examples:

```text
AAPL price in USD
SHOP.TO price in CAD
AIR.PA price in EUR
```

Currency consistency matters because values cannot be combined correctly without conversion.

### Example

```text
Asset A = 10,000 USD
Asset B = 10,000 CAD
```

These are not the same economic value.

### Required fields

Athena should store:

```text
asset currency
portfolio base currency
exchange rate when conversion is needed
```

Even if full currency conversion is not implemented immediately, the data model should be ready.

---

## 42. Data frequency

Market data can have different frequencies:

```text
Intraday
Daily
Weekly
Monthly
Quarterly
Annual
```

### Daily data

Daily data is common for early portfolio and risk analysis.

It is simpler, widely available and easier to test.

### Intraday data

Intraday data is more detailed but more complex.

It requires careful handling of:

- time zones;
- market hours;
- microstructure noise;
- large data volume.

### Resampling

Resampling means converting data from one frequency to another.

Example:

```text
Daily prices → monthly prices
```

### Practical rule

```text
Do not mix frequencies without clear methodology.
```

For Athena's first version, daily data is the best starting point.

---

## 43. Key formulas

### Simple return

```text
Return_t = Price_t / Price_{t-1} - 1
```

### Log return

```text
LogReturn_t = ln(Price_t / Price_{t-1})
```

### Holding Period Return

```text
HPR = (Ending Value - Beginning Value + Income) / Beginning Value
```

### Total return

```text
Total return = price return + income return
```

### Arithmetic mean return

```text
Arithmetic mean = (R1 + R2 + ... + Rn) / n
```

### Geometric mean return

```text
Geometric mean = [(1 + R1)(1 + R2)...(1 + Rn)]^(1/n) - 1
```

### Daily volatility

```text
Daily volatility = standard_deviation(daily_returns)
```

### Annualized volatility

```text
Annualized volatility = Daily volatility * sqrt(252)
```

### Variance and standard deviation

```text
Standard deviation = sqrt(variance)
```

### Bid-ask spread

```text
Spread = Ask - Bid
```

### Real return approximation

```text
Real return ≈ Nominal return - Inflation
```

### Exact real return

```text
Real return = (1 + nominal return) / (1 + inflation) - 1
```

---

## 44. Possible API endpoints

Possible endpoints for Athena's market finance and volatility module:

```text
GET /api/assets
GET /api/assets/{symbol}
GET /api/market-data/prices/{symbol}
GET /api/market-data/returns/{symbol}
GET /api/market-data/log-returns/{symbol}
GET /api/market-data/volatility/{symbol}
GET /api/market-data/rolling-volatility/{symbol}
GET /api/market-data/correlation
GET /api/market-data/data-quality/{symbol}
GET /api/market-data/liquidity/{symbol}
```

### Example response for volatility

```json
{
  "symbol": "AAPL",
  "daily_volatility": 0.012,
  "annualized_volatility": 0.190,
  "window": 252,
  "volatility_regime": "Normal"
}
```

### Example response for data quality

```json
{
  "symbol": "AAPL",
  "missing_prices": 0,
  "duplicated_dates": 0,
  "currency_defined": true,
  "adjusted_close_available": true,
  "warnings": []
}
```

---

## 45. Possible frontend components

Possible components for the Market Finance and Volatility page:

```text
AssetSearch
AssetOverviewCard
AssetPriceChart
ReturnChart
ReturnDistributionChart
VolatilityCards
RollingVolatilityChart
CorrelationMatrix
LiquiditySummary
BidAskSpreadCard
DataQualityWarnings
BenchmarkComparisonCard
```

### Page goal

The page should help the user understand the market behavior of a selected asset.

The user should be able to see:

- price history;
- return history;
- volatility;
- rolling volatility;
- liquidity indicators;
- correlation with other assets;
- data quality warnings.

The page should be educational and analytical.

---

## 46. Suggested tests

### Return tests

```text
Price 100 → 105 = +5%
Price 100 → 92  = -8%
```

### Holding Period Return test

```text
Beginning price = 100
Ending price = 105
Income = 2
HPR = 7%
```

### Log return test

```text
Price 100 → 105
Log return = ln(1.05)
```

### Volatility tests

```text
Stable returns should produce low volatility.
Highly variable returns should produce high volatility.
```

### Annualization test

```text
Daily volatility = 1%
Annualized volatility ≈ 15.87%
```

### Data quality tests

```text
Missing price should be detected.
Negative price should be rejected.
Duplicate date should be flagged.
Missing currency should be flagged.
Missing adjusted close should produce a warning.
```

### Liquidity tests

```text
High volume and low spread should indicate better liquidity.
Low volume and high spread should indicate weaker liquidity.
```

---

## 47. Common beginner mistakes

### Mistake 1 — Using prices instead of returns

Prices are not directly comparable across assets.

### Mistake 2 — Ignoring adjusted close

Unadjusted close prices can create false returns after dividends or stock splits.

### Mistake 3 — Confusing volatility and loss

Volatility measures movement, not only downside loss.

### Mistake 4 — Forgetting currency

A price without currency is incomplete.

### Mistake 5 — Removing outliers automatically

Some outliers are real market shocks.

### Mistake 6 — Mixing data frequencies

Daily and intraday data should not be mixed without clear methodology.

### Mistake 7 — Comparing returns without a benchmark

A return is more meaningful when compared with an appropriate reference.

### Mistake 8 — Ignoring inflation

A positive nominal return can still be weak after inflation.

### Mistake 9 — Ignoring liquidity

An asset can look attractive but be difficult or expensive to trade.

### Mistake 10 — Assuming normal distribution blindly

Financial returns often have fat tails and extreme events.

---

## 48. Summary

Market finance starts with assets and prices.

Prices are transformed into returns.  
Returns are used to calculate volatility, correlation and market behavior.  
Volatility measures uncertainty.  
Liquidity measures how easily an asset can be traded.  
Benchmarks provide context for performance.  
Data quality is essential because poor data leads to poor analysis.

This document supports the **Market Finance and Volatility** foundation of Athena AI Risk Terminal.

It prepares the implementation of:

- asset data;
- historical prices;
- adjusted close handling;
- returns;
- holding period return;
- total return;
- arithmetic and geometric returns;
- volatility;
- rolling volatility;
- correlation;
- liquidity indicators;
- benchmarks;
- data quality checks;
- frontend market analytics;
- backend market data endpoints.

The key lesson is simple:

```text
Clean market data is the foundation.
Returns transform prices into analysis.
Volatility measures uncertainty.
Liquidity determines tradability.
Benchmarks provide context.
```
