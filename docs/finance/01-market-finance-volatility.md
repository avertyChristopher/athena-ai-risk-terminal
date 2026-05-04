# 01 — Market Finance and Volatility

**Project:** Athena AI Risk Terminal  
**Recommended file path:** `docs/finance/01-market-finance-volatility.md`  
**Purpose:** build a strong foundation in market finance, asset classes, market data, returns, volatility, distributions, liquidity, benchmarks and data quality.  
**Scope:** this document focuses only on market finance and volatility. Other finance areas are documented separately.

---

## Table of Contents

## Part I — Market finance foundations
1. What is market finance?
2. Main asset classes
3. Stocks
4. ETFs
5. Market indices
6. Currencies
7. Commodities


## Part II — Market data and return calculations
8. Market data
9. OHLCV data
10. Adjusted close and corporate actions
11. Volume
12. Nominal vs real returns
13. Price vs return
14. Holding Period Return
15. Simple returns
16. Log returns
17. Arithmetic vs geometric returns
18. Total return
19. Compounding and annualization


## Part III — Volatility, distributions and statistical risk
20. Volatility
21. Daily volatility
22. Annualized volatility
23. Rolling volatility
24. Realized volatility
25. Implied volatility
26. Variance and standard deviation
27. Return distributions
28. Skewness and kurtosis
29. Normal distribution and fat tails
30. Correlation
31. Covariance

## Part IV — Liquidity, execution, benchmarks and market behavior
32. Liquidity
33. Bid, ask and bid-ask spread
34. Order types and market microstructure
35. Benchmark
36. Index construction basics
37. Market efficiency basics




## Part V — Data quality, Athena implementation and review
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



## Part I — Market finance foundations


## 1. What is market finance?

Market finance is the part of finance that studies financial instruments traded on markets, how their prices are formed, how they evolve over time, and how investors use market information to make decisions.

It focuses on traded assets such as:

```text
Stocks
Bonds
ETFs
Currencies
Commodities
Derivatives
Market indices
```

In simple terms, market finance tries to answer questions such as:

- What is this asset?
- What is its current market price?
- How has its price changed over time?
- What return did the asset generate?
- How risky or volatile is the asset?
- How liquid is the asset?
- How does it behave compared with a benchmark?
- How reliable is the data used for the analysis?

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

Market finance is not only about observing prices. A price is just the starting point. The real financial analysis begins when prices are transformed into returns, volatility, correlations, risk measures and performance indicators.


```text
Asset identification
        ↓
Market data collection
        ↓
Price cleaning and validation
        ↓
Return calculation
        ↓
Volatility and risk measurement
        ↓
Benchmark comparison
        ↓
Investment or risk decision

```

### Why market finance matters

Market finance matters because most investment decisions are based on market information.

For example, an investor may want to know:
- Should I buy this stock?
- Is this ETF too volatile?
- Is this portfolio more risky than the S&P 500?
- Did this asset outperform its benchmark?
- Is the recent price movement normal or extreme?
- Is the asset liquid enough to trade?

Without market finance, a financial platform would only display raw prices. With market finance, the platform can explain what those prices mean.

### Price is not enough

A beginner may look only at the price of an asset.

Example:

```text
Stock A price = 200
Stock B price = 20
```

This does not mean that Stock A is more expensive in an investment sense. It only means that one share of Stock A trades at a higher nominal price.

To compare assets, analysts usually use returns instead of prices.

Example:

```text
Stock A moves from 200 to 210.
Stock B moves from 20 to 21.
```

Both assets generated:

```text
Return = 5%
```
Even though their prices are very different, their percentage performance is the same.

This is why market finance relies heavily on returns, not only price levels.

### Market finance and risk

Market finance is closely connected to risk management.

A financial asset can generate returns, but those returns are uncertain. The future price of a stock, ETF, currency, bond or commodity is never known with certainty.

This uncertainty creates risk.

In market finance, risk is often related to the possibility that asset prices move in an unfavorable direction. However, risk does not only mean losing money. It also refers to the uncertainty of future outcomes.

For example:

```text
A stable asset may move by +0.2% or -0.2% per day.
A risky asset may move by +5% or -5% per day.
```

The second asset is more uncertain because its possible outcomes are more dispersed.

Common market-related risks include:
- Equity price risk
- Interest rate risk
- Currency risk
- Commodity price risk
- Volatility risk
- Liquidity risk
- Correlation risk


### Equity price risk

Equity price risk is the risk that stock prices decrease.

Example:

```text
An investor owns shares of Apple.
If Apple stock falls from 200 to 180, the investor loses 10% before dividends.
```
This type of risk is central for portfolios containing stocks or equity ETFs.


### Interest rate risk

Interest rate risk is the risk that changes in interest rates affect the value of financial instruments.

This is especially important for bonds.

- When interest rates rise, existing bond prices usually fall.
- When interest rates fall, existing bond prices usually rise.

This relationship is a key foundation for fixed income analysis.



### Currency risk

Currency risk appears when an investor owns assets denominated in a foreign currency.

Example:

```text
A Canadian investor buys a US stock.
The stock is priced in USD.
The investor reports wealth in CAD.
```

The final return depends on both:

```text
The return of the US stock
The movement of USD/CAD
```
Even if the stock performs well in USD, the Canadian investor may earn a weaker return if the US dollar depreciates against the Canadian dollar.


### Commodity price risk

Commodity price risk is the risk that commodity prices change.

Examples:

```text
Oil price risk
Gold price risk
Natural gas price risk
Copper price risk
Wheat price risk
```

This matters for investors, producers, consumers and companies exposed to commodity inputs.



### Volatility risk

Volatility risk is the risk that an asset becomes more unstable.

A rise in volatility can affect:

- Portfolio risk
- Option prices
- Margin requirements
- Investor confidence
- Risk limits

For a risk terminal like Athena, volatility is one of the most important market indicators.


### Liquidity risk

Liquidity risk is the risk that an investor cannot buy or sell an asset quickly at a fair price.

An asset may look attractive based on historical returns, but if it is illiquid, it may be difficult or expensive to trade.

Signs of poor liquidity include:

- Low trading volume
- Wide bid-ask spread
- Few market participants
- Large price impact when trading


### Correlation risk

Correlation risk is the risk that assets move together more than expected.

Diversification depends on assets not moving perfectly together.



Example:
```text
A portfolio owns 10 different stocks.
If all 10 stocks fall together during a crisis, diversification is weak.
```
This is why correlation is essential in portfolio risk analysis.

### Market finance and CFA Level 1

For CFA Level 1, market finance is important because it connects several major areas of the curriculum.

The concepts in this document are especially related to:

- Quantitative Methods
- Equity Investments
- Fixed Income
- Derivatives
- Portfolio Management
- Alternative Investments
- Economics

### Connection with Quantitative Methods

Market finance uses quantitative tools to transform prices into useful information.

Important CFA-related concepts include:

- Returns
- Arithmetic mean
- Geometric mean
- Variance
- Standard deviation
- Correlation
- Covariance
- Probability distributions
- Skewness
- Kurtosis

These tools help analysts measure performance and risk.


### Connection with Equity Investments

Equity analysis requires understanding stocks, indices, market data, benchmarks and market efficiency.

Important concepts include:
- Common stocks
- Market indices
- Price return indices
- Total return indices
- Market capitalization
- Benchmarks
- Market efficiency
- Liquidity


### Connection with Portfolio Management

Portfolio management is based on the relationship between risk and return.

Important concepts include:


- Portfolio return
- Portfolio risk
- Diversification
- Correlation
- Benchmark comparison
- Risk-adjusted performance
- Asset allocation


A portfolio is not evaluated only by its return. It must also be evaluated by the amount of risk taken to generate that return.

### Connection with Derivatives

Derivatives depend on underlying market assets.

Examples:


```text
A stock option depends on a stock.
An oil future depends on oil.
A currency forward depends on an exchange rate.
An interest rate swap depends on interest rates.
```

Market finance provides the underlying prices and volatility inputs needed for derivatives analysis.




















---


## 2. Main asset classes

An asset class is a group of financial instruments with similar economic characteristics.

In simple terms, an asset class answers the question:

```text
What type of investment is this?
```

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

Each asset class has its own return drivers, risks, market conventions and data requirements.

For Athena AI Risk Terminal, identifying the asset class correctly is important because the system should not analyze every instrument in the same way.

Example:

```text
- A stock is mainly analyzed through price returns, dividends and volatility.

- A bond is mainly analyzed through interest rates, coupons, yield and duration.

- A currency is analyzed through exchange rate movements.

- An option is analyzed through the price of its underlying asset and volatility.
```

The asset class is therefore one of the first fields that Athena should store for every instrument.

Example:

```text
symbol: AAPL
name: Apple Inc.
asset_class: Equity
currency: USD
exchange: NASDAQ
```

---

### Why asset classes matter

Asset classes matter because they help investors organize financial markets.

They are useful for:

- understanding what an instrument represents;
- comparing similar investments;
- building diversified portfolios;
- measuring risk correctly;
- selecting an appropriate benchmark;
- choosing the right financial model;
- designing clean market data structures.

For example, an equity portfolio should not be evaluated with the same tools as a bond portfolio.

A stock portfolio may focus on:

```text
Price returns
Dividends
Volatility
Beta
Sector exposure
Market capitalization
```

A bond portfolio may focus on:

```text
Coupon income
Yield
Maturity
Duration
Credit quality
Interest rate sensitivity
```

This is why the asset class is a basic but essential concept.

---

### Equities

Equities represent ownership in companies.

A stock is the most common equity instrument.

When an investor buys a stock, the investor owns a small part of the company.

Examples:

```text
AAPL = Apple Inc.
MSFT = Microsoft Corporation
RY.TO = Royal Bank of Canada
```

Equity investors can earn returns from:

```text
Price appreciation
Dividends
```

Example:

```text
An investor buys a stock at 100.
The stock rises to 110.
The company also pays a dividend of 2.

The investor earns both a capital gain and dividend income.
```

Equities are generally considered growth-oriented assets. They can offer high long-term returns, but they can also be volatile.

Typical equity data fields:

```text
Symbol
Company name
Exchange
Currency
Sector
Industry
Market price
Adjusted close
Volume
Dividend yield
Market capitalization
```

In Athena, equities are a natural starting point because stock price data is widely available and easy to use for return and volatility calculations.

---

### Fixed income

Fixed income instruments are debt instruments.

The most common example is a bond.

When an investor buys a bond, the investor is lending money to an issuer.

The issuer can be:

```text
A government
A corporation
A municipality
A financial institution
```

Examples:

```text
Government bond
Corporate bond
Treasury bill
Municipal bond
```

Fixed income investors can earn returns from:

```text
Coupon payments
Price changes
Return of principal at maturity
```

A bond usually has:

```text
Face value
Coupon rate
Maturity date
Yield
Issuer
Credit quality
```

Simple example:

```text
A company issues a bond.
The investor buys the bond.
The company pays coupons.
At maturity, the company repays the principal.
```

Fixed income is strongly affected by interest rates.

Basic relationship:

```text
When interest rates rise, existing bond prices usually fall.
When interest rates fall, existing bond prices usually rise.
```

In Athena, fixed income can be added after equities because bonds require more specific concepts such as yield, duration, maturity and credit risk.

---

### Currencies

Currencies are traded through exchange rates.

An exchange rate expresses the value of one currency in terms of another.

Examples:

```text
EUR/USD
USD/CAD
GBP/USD
USD/JPY
```

Example:

```text
USD/CAD = 1.35
```

This means:

```text
1 USD = 1.35 CAD
```

Currencies are important because many portfolios contain assets denominated in different currencies.

Example:

```text
A Canadian investor buys a US stock.
The stock is priced in USD.
The investor measures wealth in CAD.
```

The investor is exposed to both:

```text
The stock return
The exchange rate movement
```

Typical currency data fields:

```text
Currency pair
Base currency
Quote currency
Exchange rate
Date
Data source
```

In Athena, currency fields are important even if full foreign exchange conversion is added later.

At minimum, every asset should have a currency.

---

### Commodities

Commodities are physical goods traded in financial markets.

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

Commodities are often linked to the real economy because they are used in production, transportation, energy, food and industry.

Commodity prices are influenced by:

```text
Supply
Demand
Inventories
Weather
Geopolitical events
Transportation costs
Global economic activity
Currency movements
```

Commodity investors can get exposure through:

```text
Futures contracts
Commodity ETFs
Commodity-producing companies
Commodity indices
```

Example:

```text
An investor may buy a gold ETF instead of buying physical gold.
```

In Athena's first version, commodities can be represented through ETFs or simple historical price series.

Direct commodity futures analysis can be added later because futures require additional concepts such as contract maturity and roll yield.

---

### Derivatives

Derivatives are financial contracts whose value depends on another asset.

The asset that determines the derivative's value is called the underlying asset.

Examples of underlying assets:

```text
Stock
Bond
Currency
Commodity
Interest rate
Market index
```

Common derivatives include:

```text
Options
Futures
Forwards
Swaps
```

Example:

```text
A call option on Apple depends on the price of Apple stock.
A crude oil future depends on the price of oil.
A currency forward depends on an exchange rate.
```

Derivatives are used for:

```text
Hedging
Speculation
Risk transfer
Leverage
Portfolio protection
```

For Athena, derivatives are important because they connect directly to risk management.

However, derivatives are more complex than stocks or ETFs because they often require additional inputs.

Example for an option:

```text
Underlying price
Strike price
Time to maturity
Interest rate
Volatility
Option type
```

In Athena, derivatives can be added after the basic market data, return and volatility modules are stable.

---

### Cash and money market instruments

Cash and money market instruments are short-term and usually highly liquid.

Examples:

```text
Cash
Treasury bills
Commercial paper
Certificates of deposit
Money market funds
```

These instruments are generally used for:

```text
Liquidity management
Capital preservation
Short-term investing
Temporary cash allocation
```

They usually have lower risk and lower expected return than equities.

A Treasury bill is a common example.

Simple idea:

```text
An investor lends money to the government for a short period.
The investor receives the principal back with a small return.
```

For Athena, cash and money market instruments are useful because portfolios often hold cash positions.

Cash should not be ignored because it affects:

```text
Portfolio value
Portfolio return
Risk exposure
Liquidity
Asset allocation
```

---

### Alternative investments

Alternative investments are assets outside traditional public equities, bonds and cash.

Examples:

```text
Private equity
Real estate
Hedge funds
Infrastructure
Private debt
Venture capital
Commodities
Collectibles
```

Alternative investments often have different characteristics from traditional assets.

They may be:

```text
Less liquid
Less transparent
Harder to value
Less frequently priced
More dependent on manager skill
More complex in terms of risk
```

Example:

```text
A public stock may have a daily market price.
A private real estate fund may only report value monthly or quarterly.
```

This creates a data challenge.

In Athena, alternative investments should probably not be part of the first MVP unless they are represented through publicly traded ETFs or indices.

---

### Traditional vs alternative asset classes

A simple distinction is:

```text
Traditional asset classes:
- Equities
- Fixed income
- Cash

Alternative asset classes:
- Private equity
- Real estate
- Hedge funds
- Infrastructure
- Commodities
```

This distinction is useful for CFA Level 1 because traditional assets are usually easier to price and trade, while alternative investments often introduce liquidity, valuation and transparency challenges.

---

### Asset class comparison

A simple comparison:

```text
Equities:
Ownership in companies.
Main return sources: price appreciation and dividends.

Fixed income:
Debt issued by governments or companies.
Main return sources: coupons and price changes.

Currencies:
Exchange rates between currencies.
Main return source: currency appreciation or depreciation.

Commodities:
Physical goods traded in markets.
Main return source: commodity price changes.

Derivatives:
Contracts based on underlying assets.
Main return source: change in derivative value.

Cash and money market:
Short-term liquid instruments.
Main return source: short-term interest.

Alternative investments:
Non-traditional assets.
Main return sources depend on the specific asset type.
```

---

### CFA Level 1 takeaway

For CFA Level 1, the main point is to understand what each asset class represents.

You should be able to identify:

```text
Who owns what?
Who owes what?
What creates the return?
What creates the risk?
How liquid is the asset?
How easy is it to value?
What market data is needed?
```

A simple memory rule:

```text
Equity = ownership
Fixed income = lending
Currency = exchange rate
Commodity = physical good
Derivative = contract based on another asset
Cash = liquidity
Alternative investment = non-traditional exposure
```

---

### Athena implementation takeaway

For Athena, every asset should have a clear asset class.

Possible asset model:

```text
Asset
- symbol
- name
- asset_class
- asset_type
- currency
- exchange
- country
- sector
- data_source
```

Example:

```text
symbol: SPY
name: SPDR S&P 500 ETF Trust
asset_class: Equity
asset_type: ETF
currency: USD
exchange: NYSE Arca
country: United States
```

Another example:

```text
symbol: EUR/USD
name: Euro / US Dollar
asset_class: Currency
asset_type: FX pair
currency: USD
exchange: FX market
country: Global
```

The asset class can help Athena decide which analytics are relevant.

Example:

```text
Equity → returns, volatility, beta, drawdown
Bond → yield, duration, maturity, credit risk
Currency → exchange rate return, FX exposure
Commodity → spot price, futures price, commodity volatility
Derivative → underlying, payoff, Greeks
Cash → liquidity, short-term return
```

This keeps the system organized and avoids applying the wrong analysis to the wrong instrument.

---

### Mini revision questions

1. What is an asset class?

2. What is the difference between equities and fixed income?

3. Why are currencies important in portfolio analysis?

4. Why are derivatives different from stocks and bonds?

5. Why can alternative investments be harder to analyze?

6. Why should Athena store the asset class of each instrument?

---

### Mini answers

1. An asset class is a group of financial instruments with similar economic characteristics.

2. Equities represent ownership in a company, while fixed income represents lending money to an issuer.

3. Currencies are important because foreign assets expose investors to exchange rate movements.

4. Derivatives are different because their value depends on an underlying asset.

5. Alternative investments can be harder to analyze because they may be illiquid, less transparent and less frequently priced.

6. Athena should store the asset class because different instruments require different data, calculations and risk metrics.

---

### Section summary

Asset classes organize financial markets into major categories.

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

Each asset class has different sources of return, different risks and different data requirements.

For CFA Level 1, understanding asset classes is essential because it gives structure to the rest of investment analysis.

For Athena AI Risk Terminal, asset classification is essential because the platform must know what type of instrument it is analyzing before applying calculations.

The key lesson is:

```text
The asset class tells Athena what the instrument is,
how it behaves,
and which financial analysis is appropriate.
```
















---
## 3. Stocks

A stock represents ownership in a company.

When an investor buys a stock, the investor becomes a shareholder. This means the investor owns a small part of the company and may benefit if the company grows in value.

Stocks are also called equities because they represent an ownership interest.

Example:

```text
If a company has 1,000,000 shares outstanding
and an investor owns 10,000 shares,

the investor owns 1% of the company.
```

In practice, most investors do not buy stocks to control a company. They buy stocks to earn a return from price appreciation and, in some cases, dividends.

---

### Why companies issue stocks

Companies issue stocks to raise capital.

They can use this capital to:

- grow the business;
- invest in new projects;
- hire employees;
- repay debt;
- acquire other companies;
- fund research and development.

When a company sells shares to investors for the first time on a public exchange, this is called an IPO.

```text
IPO = Initial Public Offering
```

After the IPO, the company’s shares can trade between investors on the secondary market.

Important distinction:

```text
Primary market = the company sells new shares to investors.
Secondary market = investors trade existing shares with each other.
```

Most stock market activity happens in the secondary market.

---

### How investors make money from stocks

Stock investors can earn returns in two main ways:

```text
Capital gain
Dividend income
```

### Capital gain

A capital gain happens when the stock price increases.

Example:

```text
Purchase price = 100
Selling price  = 120

Capital gain = 20
Return = 20%
```

### Dividend income

A dividend is a cash payment distributed by a company to shareholders.

Example:

```text
Stock price = 100
Annual dividend = 3

Dividend yield = 3 / 100 = 3%
```

Not all companies pay dividends.

Growth companies often reinvest profits into the business, while mature companies are more likely to pay dividends.

---

### Common stock and preferred stock

There are two main types of stock:

```text
Common stock
Preferred stock
```

### Common stock

Common stock usually gives shareholders voting rights.

Common shareholders may vote on important company matters, such as electing the board of directors.

Common stockholders benefit if the company grows, but they also take more risk.

If the company goes bankrupt, common shareholders are paid last.

### Preferred stock

Preferred stock usually has characteristics of both equity and fixed income.

Preferred shareholders often receive fixed dividends and have priority over common shareholders for dividend payments.

However, preferred shares usually have limited or no voting rights.

Simple comparison:

```text
Common stock = more upside potential, more risk, voting rights.
Preferred stock = more stable income, less upside, priority over common stock.
```

For Athena’s first version, common stocks are the most important.

---

### What makes a stock price move?

A stock price changes because investors continuously update their expectations about the company.

Important drivers include:

```text
Earnings results
Revenue growth
Profit margins
Interest rates
Economic conditions
Industry trends
Company news
Investor sentiment
Liquidity
Geopolitical events
```

Example:

```text
If a company reports stronger earnings than expected,
investors may become more optimistic,
and the stock price may rise.
```

Another example:

```text
If interest rates rise,
future company profits may be discounted at a higher rate,
and stock prices may fall.
```

Stock prices are forward-looking. They often move because of expectations about the future, not only because of current results.

---

### Stock exchanges

Stocks are usually traded on exchanges.

Examples:

```text
NYSE
NASDAQ
Toronto Stock Exchange
London Stock Exchange
Euronext Paris
Tokyo Stock Exchange
```

An exchange provides a regulated marketplace where buyers and sellers can trade securities.

A stock record should include the exchange because the same company or similar tickers may exist in different markets.

Example:

```text
symbol: AAPL
name: Apple Inc.
exchange: NASDAQ
currency: USD
country: United States
```

---

### Ticker symbols

A ticker symbol is a short code used to identify a traded security.

Examples:

```text
AAPL = Apple Inc.
MSFT = Microsoft Corporation
RY.TO = Royal Bank of Canada on the Toronto Stock Exchange
AIR.PA = Airbus on Euronext Paris
```

Ticker symbols are useful for market data systems because they make assets easier to search and identify.

However, tickers must be handled carefully because formats can vary by exchange and data provider.

---

### Market capitalization

Market capitalization, or market cap, measures the total market value of a company’s equity.

Formula:

```text
Market capitalization = share price × shares outstanding
```

Example:

```text
Share price = 50
Shares outstanding = 1,000,000

Market cap = 50 × 1,000,000
Market cap = 50,000,000
```

Market cap is often used to classify companies.

Common categories:

```text
Large-cap
Mid-cap
Small-cap
Micro-cap
```

Large-cap companies are usually more established. Small-cap companies may have more growth potential, but they can also be riskier and less liquid.

---

### Sector and industry

Stocks are often grouped by sector and industry.

Examples of sectors:

```text
Technology
Financials
Healthcare
Energy
Consumer staples
Consumer discretionary
Industrials
Utilities
Real estate
Materials
Communication services
```

Sector classification matters because companies in the same sector are often affected by similar economic forces.

Example:

```text
Banks are strongly affected by interest rates and credit conditions.
Energy companies are strongly affected by oil and gas prices.
Technology companies are often affected by growth expectations and innovation cycles.
```

For Athena, sector information can help analyze portfolio exposure.

Example:

```text
Portfolio exposure:
Technology: 45%
Financials: 20%
Healthcare: 15%
Energy: 10%
Other: 10%
```

---

### Price vs value

A stock price is the current market quote.

A stock value is an estimate of what the stock should be worth based on analysis.

They are not always equal.

```text
Price = what the market currently pays.
Value = what an analyst estimates the stock is worth.
```

Example:

```text
Market price = 80
Analyst estimated value = 100
```

The analyst may consider the stock undervalued.

Another example:

```text
Market price = 120
Analyst estimated value = 100
```

The analyst may consider the stock overvalued.

This difference is central to active investing.

---

### Stock returns

For Athena, the most important calculation is usually the stock return.

Simple return formula:

```text
Return = Price_t / Price_{t-1} - 1
```

Example:

```text
Yesterday's price = 100
Today's price     = 103

Return = 103 / 100 - 1
Return = 3%
```

For stocks, adjusted close is often preferred for return calculations because it accounts for dividends and stock splits.

Practical rule:

```text
Use adjusted close for historical stock return calculations when available.
```

---

### Stock risk

Stocks can generate strong long-term returns, but they are risky.

Important stock risks include:

```text
Business risk
Market risk
Liquidity risk
Currency risk
Sector risk
Company-specific risk
```

### Business risk

Business risk comes from the company itself.

Example:

```text
Poor earnings
Weak management
Product failure
Higher costs
Lower demand
```

### Market risk

Market risk affects the overall market.

Example:

```text
A recession may cause many stocks to fall at the same time.
```

### Company-specific risk

Company-specific risk affects one company directly.

Example:

```text
A lawsuit, scandal, product recall or earnings miss.
```

This type of risk can often be reduced through diversification.

---

### Stock data needed in Athena

A clean stock record may include:

```text
symbol
name
asset_class
asset_type
currency
exchange
country
sector
industry
market_price
adjusted_close
volume
market_cap
dividend_yield
data_source
```

Example:

```text
symbol: AAPL
name: Apple Inc.
asset_class: Equity
asset_type: Common stock
currency: USD
exchange: NASDAQ
country: United States
sector: Technology
industry: Consumer Electronics
```

For the first version of Athena, the most important fields are:

```text
symbol
name
currency
exchange
adjusted close
volume
sector
```

These fields are enough to calculate basic stock returns, volatility, liquidity indicators and sector exposure.

---

### CFA Level 1 takeaway

For CFA Level 1, remember that a stock represents ownership.

The shareholder’s return can come from:

```text
Price appreciation
Dividends
```

Important stock concepts include:

```text
Common stock
Preferred stock
Dividends
Voting rights
Market capitalization
Sector classification
Primary market
Secondary market
Price vs value
```

A simple memory rule:

```text
Stock = ownership + uncertain future cash flows + market price risk
```

---

### Athena implementation takeaway

For Athena, stocks are a good first asset type because they are easy to represent with market data.

The stock module should support:

```text
Asset identification
Historical price loading
Adjusted close handling
Daily return calculation
Volatility calculation
Volume analysis
Sector classification
Benchmark comparison
Data quality checks
```

The goal is not only to display the stock price.

The goal is to transform stock market data into useful financial information.

---

### Mini revision questions

1. What does a stock represent?

2. What are the two main ways investors can earn returns from stocks?

3. What is the difference between common stock and preferred stock?

4. What is market capitalization?

5. Why is adjusted close useful for stock return calculations?

6. What is the difference between price and value?

7. Why does sector classification matter?

---

### Mini answers

1. A stock represents ownership in a company.

2. Investors can earn returns from price appreciation and dividends.

3. Common stock usually has voting rights and more upside potential. Preferred stock usually has priority for dividends but less upside.

4. Market capitalization is the share price multiplied by the number of shares outstanding.

5. Adjusted close is useful because it accounts for dividends and stock splits.

6. Price is the current market quote. Value is an analytical estimate of what the stock is worth.

7. Sector classification matters because companies in the same sector are often affected by similar economic forces.

---

### Section summary

A stock is an ownership claim on a company.

Stock investors can earn returns through price appreciation and dividends. Stock prices move because investors constantly update their expectations about the company’s future.

For CFA Level 1, stocks are important because they introduce ownership, dividends, voting rights, market capitalization and equity risk.

For Athena AI Risk Terminal, stocks are a key starting point because they provide clean use cases for price history, returns, volatility, liquidity and benchmark analysis.

The key lesson is:

```text
A stock is not just a price on a screen.
It is an ownership claim whose market value changes with expectations, risk and company performance.
```
















---


## 4. ETFs

An ETF, or exchange-traded fund, is an investment fund traded on an exchange.

ETF means:

```text
Exchange-Traded Fund
```

An ETF usually holds a basket of assets such as stocks, bonds, commodities or other securities.

Instead of buying each asset individually, an investor can buy one ETF and get exposure to the whole basket.

Examples:

```text
SPY = tracks the S&P 500
QQQ = tracks the Nasdaq-100
XIU = tracks Canadian large-cap equities
GLD = tracks gold exposure
TLT = tracks long-term US Treasury bonds
```

ETFs are useful because they combine two ideas:

```text
Diversification of a fund
Tradability of a stock
```

This means an ETF can be bought and sold during the trading day, like a stock, while giving exposure to many assets at once.

---

### Why ETFs exist

ETFs exist to give investors simple and efficient market exposure.

Instead of buying 500 individual stocks to follow the S&P 500, an investor can buy one ETF that tracks the index.

Example:

```text
Investor wants exposure to large US companies.
Instead of buying hundreds of stocks,
the investor buys SPY.
```

This makes ETFs useful for:

```text
Diversification
Low-cost investing
Passive investing
Portfolio construction
Sector allocation
Country exposure
Risk management
```

ETFs are often used by both individual investors and professional portfolio managers.

---

### ETF vs stock

An ETF trades like a stock, but it is not the same thing as a stock.

A stock represents ownership in one company.

An ETF represents ownership in a fund that holds multiple assets.

Simple comparison:

```text
Stock = exposure to one company
ETF = exposure to a basket of assets
```

Example:

```text
AAPL = exposure to Apple only
SPY = exposure to many large US companies
```

This distinction matters because an ETF is usually more diversified than a single stock.

However, diversification depends on what the ETF holds.

Example:

```text
A broad market ETF is diversified.
A sector ETF may still be concentrated.
A single-country ETF may carry country-specific risk.
```

---

### Types of ETFs

ETFs can provide different types of exposure.

Common ETF categories include:

```text
Equity ETFs
Bond ETFs
Sector ETFs
Commodity ETFs
Currency ETFs
International ETFs
Factor ETFs
Leveraged ETFs
Inverse ETFs
```

### Equity ETFs

Equity ETFs hold stocks.

Example:

```text
SPY = large US companies
QQQ = large Nasdaq-listed companies
XIU = large Canadian companies
```

### Bond ETFs

Bond ETFs hold fixed income instruments.

Example:

```text
Government bond ETFs
Corporate bond ETFs
High-yield bond ETFs
Short-term bond ETFs
```

### Sector ETFs

Sector ETFs focus on one sector.

Example:

```text
Technology ETF
Energy ETF
Financials ETF
Healthcare ETF
```

### Commodity ETFs

Commodity ETFs give exposure to commodities.

Example:

```text
Gold ETF
Oil ETF
Silver ETF
Natural gas ETF
```

Some commodity ETFs hold the physical commodity, while others use futures contracts.

### Factor ETFs

Factor ETFs target specific investment characteristics.

Examples:

```text
Value
Growth
Momentum
Quality
Low volatility
Dividend yield
Small size
```

Factor investing is important in portfolio management because it links portfolio returns to specific risk or style exposures.

---

### Passive ETFs and active ETFs

ETFs can be passive or active.

### Passive ETF

A passive ETF tries to track an index.

Example:

```text
SPY tracks the S&P 500.
QQQ tracks the Nasdaq-100.
```

The goal is not to beat the index.

The goal is to replicate its performance as closely as possible.

### Active ETF

An active ETF is managed by portfolio managers who make investment decisions.

The goal is usually to outperform a benchmark or achieve a specific investment objective.

Simple comparison:

```text
Passive ETF = tracks an index
Active ETF = manager makes active decisions
```

For CFA Level 1, the distinction between passive and active management is important.

---

### Net Asset Value

The Net Asset Value, or NAV, represents the value of the ETF’s underlying holdings.

Formula:

```text
NAV = value of fund assets - fund liabilities
```

On a per-share basis:

```text
NAV per share = net asset value / number of ETF shares outstanding
```

The ETF’s market price can be slightly different from its NAV.

This creates two important concepts:

```text
Premium
Discount
```

### Premium

An ETF trades at a premium when its market price is above its NAV.

```text
ETF market price > NAV
```

### Discount

An ETF trades at a discount when its market price is below its NAV.

```text
ETF market price < NAV
```

For large and liquid ETFs, the difference is usually small.

For less liquid ETFs, the difference can be more important.

---

### Tracking error

Tracking error measures how closely an ETF follows its benchmark.

If an ETF is designed to track the S&P 500, its return should be close to the S&P 500 return.

Example:

```text
Benchmark return = 10.00%
ETF return       = 9.85%
Difference       = -0.15%
```

Tracking error can come from:

```text
Management fees
Trading costs
Sampling methods
Cash holdings
Dividend timing
Liquidity issues
Currency effects
```

A low tracking error means the ETF is closely following its benchmark.

A high tracking error means the ETF is not tracking the benchmark very well.

---

### Expense ratio

The expense ratio is the annual fee charged by the ETF.

Example:

```text
Expense ratio = 0.10%
```

This means the fund charges 0.10% per year of assets under management.

Fees matter because they reduce investor returns over time.

Simple idea:

```text
Lower fees usually improve long-term net performance,
all else equal.
```

For passive ETFs, expense ratios are often an important comparison point.

---

### ETF liquidity

ETF liquidity depends on two layers:

```text
Liquidity of the ETF shares
Liquidity of the underlying holdings
```

The ETF itself may trade frequently, but the underlying assets also matter.

Example:

```text
An ETF holding large US stocks is usually liquid.
An ETF holding small emerging market bonds may be less liquid.
```

Important liquidity indicators include:

```text
Trading volume
Bid-ask spread
Assets under management
Liquidity of holdings
```

A wide bid-ask spread can make trading more expensive.

---

### Benefits of ETFs

ETFs have several advantages:

```text
Diversification
Intraday trading
Transparency
Lower cost
Easy access to markets
Benchmark exposure
Tax efficiency in some jurisdictions
```

Example:

```text
One ETF can give exposure to an entire equity market.
```

This makes ETFs useful for simple portfolio construction.

---

### Risks of ETFs

ETFs also have risks.

Important ETF risks include:

```text
Market risk
Tracking error
Liquidity risk
Currency risk
Concentration risk
Counterparty risk
Leverage risk
```

### Market risk

If the assets inside the ETF fall, the ETF price will usually fall too.

### Tracking error

The ETF may not perfectly follow its benchmark.

### Liquidity risk

Some ETFs may be expensive to trade if volume is low or spreads are wide.

### Currency risk

An international ETF may hold assets in foreign currencies.

### Concentration risk

Some ETFs look diversified but are heavily exposed to a few companies, sectors or countries.

### Leverage risk

Leveraged ETFs use financial techniques to amplify returns.

Example:

```text
2x leveraged ETF
3x leveraged ETF
```

These products are more complex and can behave very differently over time.

For Athena’s first version, leveraged ETFs should be treated carefully or excluded from the MVP.

---

### ETF data needed in Athena

A clean ETF record may include:

```text
symbol
name
asset_class
asset_type
currency
exchange
benchmark_index
expense_ratio
assets_under_management
holdings_count
issuer
distribution_yield
adjusted_close
volume
data_source
```

Example:

```text
symbol: SPY
name: SPDR S&P 500 ETF Trust
asset_class: Equity
asset_type: ETF
currency: USD
exchange: NYSE Arca
benchmark_index: S&P 500
issuer: State Street
```

For the first version of Athena, the most important ETF fields are:

```text
symbol
name
currency
exchange
benchmark_index
adjusted_close
volume
expense_ratio
```

These fields are enough to calculate returns, volatility, liquidity indicators and benchmark comparison.

---

### ETF analysis in Athena

From a market data perspective, ETFs can be analyzed similarly to stocks.

Athena can calculate:

```text
Daily returns
Cumulative returns
Annualized volatility
Rolling volatility
Maximum drawdown
Correlation with other assets
Benchmark comparison
Liquidity indicators
```

However, an ETF also has an underlying composition.

A more advanced version of Athena could analyze:

```text
Top holdings
Sector exposure
Country exposure
Currency exposure
Factor exposure
Bond duration exposure
Commodity exposure
```

This would make ETF analysis more powerful, but it is not required for the first MVP.

---

### CFA Level 1 takeaway

For CFA Level 1, remember that an ETF is a fund traded on an exchange.

The most important ETF concepts are:

```text
Diversification
Benchmark tracking
Net Asset Value
Premium and discount
Tracking error
Expense ratio
Liquidity
Passive vs active management
```

A simple memory rule:

```text
ETF = fund exposure + exchange trading
```

An ETF is useful because it gives investors access to a diversified basket through one tradable instrument.

---

### Athena implementation takeaway

For Athena, ETFs are important because they allow the platform to analyze diversified market exposure with simple price data.

The ETF module should support:

```text
ETF identification
Benchmark mapping
Historical price loading
Return calculation
Volatility calculation
Tracking comparison
Liquidity analysis
Expense ratio display
Data quality checks
```

ETFs are also useful for portfolio construction because they can represent broad market exposure.

Example:

```text
SPY = US equity exposure
QQQ = Nasdaq growth exposure
XIU = Canadian equity exposure
TLT = long-term US bond exposure
GLD = gold exposure
```

This makes ETFs practical instruments for Athena’s first portfolio and risk analysis features.

---

### Mini revision questions

1. What is an ETF?

2. How is an ETF different from a stock?

3. What is NAV?

4. What does it mean when an ETF trades at a premium?

5. What is tracking error?

6. Why does the expense ratio matter?

7. Why can ETF liquidity be different from stock liquidity?

8. Why are ETFs useful for Athena?

---

### Mini answers

1. An ETF is an exchange-traded fund that usually holds a basket of assets.

2. A stock represents ownership in one company, while an ETF represents ownership in a fund holding multiple assets.

3. NAV is the net value of the ETF’s underlying holdings after liabilities.

4. An ETF trades at a premium when its market price is above its NAV.

5. Tracking error measures how closely the ETF follows its benchmark.

6. The expense ratio matters because fees reduce investor returns over time.

7. ETF liquidity depends on both the ETF shares and the liquidity of the underlying holdings.

8. ETFs are useful for Athena because they provide diversified exposure with market data that can be analyzed like stocks.

---

### Section summary

An ETF is a fund traded on an exchange.

It gives investors exposure to a basket of assets through one tradable instrument.

ETFs can track equities, bonds, commodities, currencies, sectors, countries or investment factors.

For CFA Level 1, ETFs are important because they connect diversification, passive investing, benchmarks, NAV, tracking error and fees.

For Athena AI Risk Terminal, ETFs are important because they are practical instruments for portfolio analysis, volatility analysis and benchmark comparison.

The key lesson is:

```text
An ETF is not just one asset.
It is a tradable vehicle that represents exposure to a basket, index, sector, country or strategy.
```




















## 5. Market indices

A market index measures the performance of a group of securities.

It is designed to represent a market, a region, a sector, or a specific investment style.

Examples:

```text
S&P 500 = large US companies
Nasdaq-100 = large non-financial Nasdaq-listed companies
Dow Jones Industrial Average = 30 large US companies
TSX Composite = broad Canadian equity market
CAC 40 = large French companies
FTSE 100 = large UK companies
Nikkei 225 = large Japanese companies
```

An index is not usually a security that investors buy directly.

Instead, investors can get exposure to an index through:

```text
ETFs
Index mutual funds
Futures contracts
Options on indices
Structured products
```

Example:

```text
An investor cannot directly buy the S&P 500 index itself.
But the investor can buy an ETF that tracks the S&P 500.
```

---

### Why market indices exist

Market indices exist to summarize the performance of a group of securities.

Instead of looking at hundreds or thousands of individual stocks, investors can look at one index level.

Example:

```text
If the S&P 500 rises by 1%,
it suggests that large US stocks performed positively overall.
```

Indices are useful because they provide a simple reference point for understanding market movements.

They are commonly used for:

```text
Measuring market performance
Comparing portfolio returns
Creating benchmarks
Tracking sectors
Tracking countries
Building passive investment products
Understanding market sentiment
```

---

### Index level

An index level is the numerical value of an index.

Example:

```text
S&P 500 level = 5,000
```

The level itself is not a price of one asset. It is a calculated value based on the prices of the securities included in the index.

The index level becomes useful when it is compared over time.

Example:

```text
Index yesterday = 5,000
Index today     = 5,050
```

The index increased by:

```text
5,050 / 5,000 - 1 = 1%
```

So the index return is:

```text
1%
```

---

### Index return

An index return measures the percentage change in the index level over a period.

Formula:

```text
Index return = Index level_t / Index level_{t-1} - 1
```

Example:

```text
Index level at start = 4,000
Index level at end   = 4,400

Index return = 4,400 / 4,000 - 1
Index return = 10%
```

Index returns are useful because they show the performance of the market segment represented by the index.

---

### Price return index

A price return index includes only price changes.

It does not include dividends or other income paid by the securities in the index.

Simple idea:

```text
Price return index = capital appreciation only
```

Example:

```text
If the stocks in an index rise in price,
the price return index increases.
```

However, if those stocks pay dividends, the price return index does not fully reflect the investor’s total economic return.

---

### Total return index

A total return index includes both price changes and reinvested income.

Simple idea:

```text
Total return index = price movement + reinvested dividends
```

This is important because dividends can represent a significant part of long-term investment returns.

Example:

```text
Price return index return = 7%
Dividend contribution     = 2%

Total return index return = 9%
```

For long-term performance analysis, total return indices are usually more complete than price return indices.

---

### Price return vs total return

The difference between price return and total return matters.

Simple comparison:

```text
Price return index:
Tracks only price changes.

Total return index:
Tracks price changes and reinvested income.
```

Example:

```text
A stock index starts at 1,000.
The stock prices increase to 1,080.
The companies also pay dividends worth 20.
```

Price return:

```text
1,080 / 1,000 - 1 = 8%
```

Total return:

```text
(1,080 + 20) / 1,000 - 1 = 10%
```

The total return is higher because it includes income.

---

### Benchmark role

A market index is often used as a benchmark.

A benchmark is a reference used to evaluate investment performance.

Example:

```text
Portfolio return = 8%
S&P 500 return   = 10%
```

The portfolio made money, but it underperformed the benchmark.

Another example:

```text
Portfolio return = -4%
Benchmark return = -9%
```

The portfolio lost money, but it performed better than the benchmark.

This is why performance should not be evaluated alone. It should be compared with a relevant reference.

---

### Choosing the right index

The benchmark must match the investment strategy.

Example:

```text
A Canadian equity portfolio should not be compared only with the Nasdaq-100.
A US large-cap portfolio can be compared with the S&P 500.
A French large-cap portfolio can be compared with the CAC 40.
```

A good benchmark should be:

```text
Relevant
Transparent
Measurable
Consistent with the investment universe
Representative of the portfolio strategy
```

If the benchmark is not appropriate, the performance comparison can be misleading.

---

### Index construction

Indices can be constructed in different ways.

The construction method affects how the index behaves.

Common methods include:

```text
Price-weighted
Market-cap-weighted
Equal-weighted
Factor-weighted
```

### Price-weighted index

In a price-weighted index, stocks with higher share prices have more influence.

Example:

```text
Stock A price = 300
Stock B price = 50
```

Stock A has more impact on the index because its share price is higher.

The Dow Jones Industrial Average is a famous example of a price-weighted index.

### Market-cap-weighted index

In a market-cap-weighted index, companies with larger market capitalization have more influence.

Formula:

```text
Market capitalization = share price × shares outstanding
```

Example:

```text
Company A market cap = 2 trillion
Company B market cap = 50 billion
```

Company A has a much larger weight in the index.

The S&P 500 is a market-cap-weighted index.

### Equal-weighted index

In an equal-weighted index, every constituent has the same weight.

Example:

```text
100 companies in the index
Each company weight = 1%
```

This gives smaller companies more influence than they would have in a market-cap-weighted index.

---

### Constituents and weights

The securities inside an index are called constituents.

Example:

```text
Apple
Microsoft
Amazon
Nvidia
JPMorgan
```

Each constituent has a weight.

The weight determines how much that security affects the index.

Example:

```text
Stock A weight = 7%
Stock B weight = 0.5%
```

A price move in Stock A will affect the index more than the same percentage move in Stock B.

This is important because some indices may look diversified but still be heavily influenced by a few large companies.

---

### Rebalancing and reconstitution

Indices are updated over time.

Two important concepts are:

```text
Rebalancing
Reconstitution
```

### Rebalancing

Rebalancing adjusts the weights of existing index constituents.

Example:

```text
A stock becomes too large relative to the index rules.
The index provider adjusts the weights.
```

### Reconstitution

Reconstitution changes the list of securities included in the index.

Example:

```text
A company is removed from the index.
Another company is added.
```

This helps keep the index aligned with its objective.

---

### Index concentration

Index concentration means that a small number of securities represent a large part of the index.

Example:

```text
Top 10 stocks = 35% of the index
Remaining stocks = 65% of the index
```

A concentrated index may be more exposed to company-specific or sector-specific movements.

This matters for risk analysis.

Example:

```text
If a technology-heavy index falls,
the decline may be driven mostly by a few large technology companies.
```

In Athena, concentration can help explain why an index or ETF is moving.

---

### Market indices and ETFs

Many ETFs are designed to track indices.

Example:

```text
SPY tracks the S&P 500.
QQQ tracks the Nasdaq-100.
XIU tracks Canadian large-cap equities.
```

The index defines the target exposure.

The ETF is the tradable product.

Simple distinction:

```text
Index = calculation of market performance
ETF = tradable fund that can track the index
```

This distinction is important because the index itself is not usually directly tradable, while the ETF is.

---

### Market indices in Athena

In Athena AI Risk Terminal, indices can be used in several ways.

They can serve as:

```text
Benchmarks
Market indicators
Risk references
Portfolio comparison tools
ETF reference indices
```

Example use cases:

```text
Compare a portfolio against the S&P 500.
Compare a Canadian stock against the TSX Composite.
Compare a technology ETF against the Nasdaq-100.
Measure whether a portfolio is more volatile than its benchmark.
```

Athena should store index information separately from tradable assets.

Possible index record:

```text
index_symbol: SPX
name: S&P 500 Index
region: United States
asset_class: Equity
weighting_method: Market-cap-weighted
return_type: Price return or total return
currency: USD
```

---

### Index data needed in Athena

Important index fields may include:

```text
index_symbol
index_name
region
country
currency
asset_class
sector_focus
weighting_method
return_type
constituents_count
data_source
```

For the first version of Athena, the most important fields are:

```text
index_symbol
index_name
currency
region
return_type
historical_index_level
benchmark_mapping
```

These fields are enough to calculate index returns and compare assets or portfolios against a benchmark.

---

### CFA Level 1 takeaway

For CFA Level 1, market indices are important because they are used to measure and compare investment performance.

Important concepts include:

```text
Index level
Index return
Benchmark
Price return index
Total return index
Price-weighted index
Market-cap-weighted index
Equal-weighted index
Constituents
Weights
Rebalancing
Reconstitution
```

A simple memory rule:

```text
Index = market performance reference
Benchmark = index used for comparison
ETF = tradable product that can track an index
```

---

### Athena implementation takeaway

For Athena, market indices are useful because they provide context.

A return alone does not say enough.

Example:

```text
Portfolio return = 6%
```

This becomes more meaningful when compared with:

```text
Benchmark return = 4%
```

or:

```text
Benchmark return = 10%
```

The same portfolio return can look strong or weak depending on the benchmark.

Athena should use indices to support:

```text
Benchmark comparison
Relative performance analysis
Market context
Portfolio evaluation
ETF benchmark mapping
Risk comparison
```

---

### Mini revision questions

1. What is a market index?

2. Can investors usually buy an index directly?

3. What is the difference between a price return index and a total return index?

4. Why are indices used as benchmarks?

5. What is a market-cap-weighted index?

6. What is the difference between an index and an ETF?

7. Why can index concentration matter?

---

### Mini answers

1. A market index measures the performance of a group of securities.

2. Usually no. Investors typically get exposure through ETFs, index funds, futures or other products.

3. A price return index includes only price changes, while a total return index includes price changes and reinvested income.

4. Indices are used as benchmarks because they provide a reference for evaluating performance.

5. A market-cap-weighted index gives larger companies more influence based on their market capitalization.

6. An index is a performance calculation. An ETF is a tradable fund that may track an index.

7. Index concentration matters because a few large securities can drive much of the index’s performance and risk.

---

### Section summary

A market index measures the performance of a group of securities.

Indices help investors understand markets, compare portfolios and build benchmarks.

For CFA Level 1, indices are important because they introduce benchmark comparison, index returns, weighting methods and the difference between price return and total return.

For Athena AI Risk Terminal, indices are important because they provide context for portfolio and asset performance.

The key lesson is:

```text
An index is a reference point.
It helps explain whether performance is strong or weak relative to the market.
```
---





















## 6. Currencies

Currencies are traded through exchange rates.

An exchange rate shows how much one currency is worth compared with another currency.

Examples:

```text
EUR/USD
USD/CAD
GBP/USD
USD/JPY
```

A currency pair always contains two currencies:

```text
Base currency
Quote currency
```

Example:

```text
USD/CAD = 1.35
```

This means:

```text
1 USD = 1.35 CAD
```

The first currency is the base currency.  
The second currency is the quote currency.

---

### Base currency and quote currency

In a currency pair, the base currency is the currency being valued.

The quote currency is the currency used to express that value.

Example:

```text
EUR/USD = 1.10
```

This means:

```text
1 EUR = 1.10 USD
```

In this example:

```text
EUR = base currency
USD = quote currency
```

Another example:

```text
USD/JPY = 155
```

This means:

```text
1 USD = 155 JPY
```

Understanding the direction of the currency pair is essential.

A common beginner mistake is to read the pair backwards.

---

### Currency appreciation and depreciation

A currency appreciates when it increases in value compared with another currency.

A currency depreciates when it decreases in value compared with another currency.

Example:

```text
EUR/USD moves from 1.10 to 1.20
```

This means the euro appreciated against the US dollar.

Why?

Because:

```text
Before: 1 EUR = 1.10 USD
After:  1 EUR = 1.20 USD
```

One euro can now buy more US dollars.

Another example:

```text
USD/CAD moves from 1.35 to 1.25
```

This means the US dollar depreciated against the Canadian dollar.

Why?

Because:

```text
Before: 1 USD = 1.35 CAD
After:  1 USD = 1.25 CAD
```

One US dollar now buys fewer Canadian dollars.

---

### Why currencies matter

Currencies matter because investors often buy assets from different countries.

A portfolio may contain:

```text
US stocks priced in USD
Canadian stocks priced in CAD
European stocks priced in EUR
Japanese stocks priced in JPY
```

If all portfolio values must be reported in one base currency, foreign assets must be converted.

Example:

```text
A Canadian investor buys a US stock.
The stock is priced in USD.
The investor reports wealth in CAD.
```

The final return depends on two elements:

```text
The stock return in USD
The USD/CAD exchange rate movement
```

This is called foreign exchange exposure.

---

### Foreign exchange risk

Foreign exchange risk, or FX risk, is the risk that exchange rate movements affect the value of an investment.

Example:

```text
A Canadian investor buys a US stock for 100 USD.
Later, the stock rises to 110 USD.
```

In USD, the stock return is:

```text
110 / 100 - 1 = 10%
```

But the Canadian investor does not only care about USD.

The investor cares about CAD.

If the US dollar weakens against the Canadian dollar, part of the stock gain may disappear after conversion.

This is why international investing creates both:

```text
Asset price risk
Currency risk
```

---

### Direct and indirect currency exposure

Currency exposure can be direct or indirect.

### Direct exposure

Direct exposure happens when an investor owns an asset priced in a foreign currency.

Example:

```text
A Canadian investor owns a US stock priced in USD.
```

The investor is directly exposed to USD/CAD movements.

### Indirect exposure

Indirect exposure happens when a company earns revenues or pays costs in foreign currencies.

Example:

```text
A Canadian company sells products in the United States.
Its revenues may depend partly on USD/CAD.
```

Even if the stock trades in CAD, the company may still be affected by currency movements.

This matters for deeper equity analysis.

---

### Currency return

A currency return measures the percentage change in an exchange rate.

Formula:

```text
Currency return = FX rate_t / FX rate_{t-1} - 1
```

Example:

```text
USD/CAD yesterday = 1.35
USD/CAD today     = 1.38

Currency return = 1.38 / 1.35 - 1
Currency return = 2.22%
```

This means the US dollar appreciated against the Canadian dollar.

For an investor whose base currency is CAD, this can increase the CAD value of USD assets.

---

### Portfolio base currency

A portfolio base currency is the currency used to report portfolio value and returns.

Examples:

```text
Canadian investor → CAD base currency
US investor → USD base currency
European investor → EUR base currency
```

The base currency is important because all portfolio positions must be converted into the same currency before calculating total portfolio value.

Example:

```text
Asset A = 10,000 USD
Asset B = 10,000 CAD
```

These two values cannot simply be added without conversion.

If:

```text
USD/CAD = 1.35
```

Then:

```text
10,000 USD = 13,500 CAD
```

So the portfolio value in CAD is:

```text
13,500 CAD + 10,000 CAD = 23,500 CAD
```

---

### Currency conversion

Currency conversion transforms an amount from one currency into another.

Example:

```text
Amount in USD = 1,000
USD/CAD = 1.35
```

Value in CAD:

```text
1,000 × 1.35 = 1,350 CAD
```

If the exchange rate is quoted in the opposite direction, the calculation must be inverted.

Example:

```text
CAD/USD = 0.74
```

This means:

```text
1 CAD = 0.74 USD
```

To convert USD into CAD, the system must be careful about the direction of the pair.

This is a critical data quality issue in financial applications.

---

### Currency hedging

Currency hedging means reducing or neutralizing foreign exchange risk.

Investors may use financial instruments such as:

```text
Currency forwards
Currency futures
Currency options
Currency swaps
Hedged ETFs
```

Example:

```text
A Canadian investor owns US stocks.
The investor wants exposure to US equities,
but not to USD/CAD movements.
```

The investor may use a currency hedge to reduce USD/CAD risk.

Hedging can reduce currency risk, but it can also reduce potential gains from favorable exchange rate movements.

Simple idea:

```text
Unhedged position = asset risk + currency risk
Hedged position = mostly asset risk
```

---

### Common currency codes

Currencies are often identified by three-letter ISO codes.

Examples:

```text
USD = United States dollar
CAD = Canadian dollar
EUR = Euro
GBP = British pound
JPY = Japanese yen
CHF = Swiss franc
AUD = Australian dollar
CNY = Chinese yuan
```

Athena should use standardized currency codes to avoid ambiguity.

Example:

```text
Do not write: dollar
Write: USD or CAD
```

This is important because several countries use a currency called “dollar”.

---

### Currency data needed in Athena

A clean currency record may include:

```text
currency_pair
base_currency
quote_currency
exchange_rate
date
data_source
frequency
```

Example:

```text
currency_pair: USD/CAD
base_currency: USD
quote_currency: CAD
exchange_rate: 1.35
date: 2026-04-29
data_source: Market data provider
frequency: Daily
```

For assets, Athena should store:

```text
asset_symbol
asset_currency
portfolio_base_currency
exchange_rate_used
conversion_date
```

This allows the system to convert positions and returns correctly.

---

### Currency analysis in Athena

Athena can use currency data to support:

```text
Portfolio currency conversion
Foreign exchange exposure analysis
Multi-currency portfolio valuation
Currency-adjusted returns
FX volatility calculation
FX risk monitoring
```

Example:

```text
AAPL price return in USD = 8%
USD/CAD return = -2%
```

The Canadian investor’s CAD return will not be exactly 8%.

The currency movement changes the final result.

For a first version of Athena, the priority is simple:

```text
Store the currency of every asset.
Store the portfolio base currency.
Convert market values consistently.
Display currency clearly to the user.
```

---

### CFA Level 1 takeaway

For CFA Level 1, currencies are important because exchange rates affect international investments.

Important concepts include:

```text
Exchange rate
Currency pair
Base currency
Quote currency
Appreciation
Depreciation
Foreign exchange risk
Portfolio base currency
Currency conversion
Currency hedging
```

A simple memory rule:

```text
Currency pair = base currency priced in quote currency
```

Example:

```text
EUR/USD = 1.10
```

means:

```text
1 EUR costs 1.10 USD
```

---

### Athena implementation takeaway

For Athena, currencies must be explicit in the data model.

A price without currency is incomplete.

The currency module should support:

```text
Currency identification
Exchange rate storage
Base currency definition
Portfolio value conversion
Foreign asset conversion
Currency exposure display
FX data quality checks
```

The goal is to prevent incorrect portfolio values caused by mixing currencies.

Example problem:

```text
10,000 USD + 10,000 CAD ≠ 20,000 CAD
```

The values must first be converted into the same currency.

---

### Mini revision questions

1. What is an exchange rate?

2. In EUR/USD, which currency is the base currency?

3. What does USD/CAD = 1.35 mean?

4. What is foreign exchange risk?

5. Why does a portfolio need a base currency?

6. Why is currency conversion important in Athena?

7. What is currency hedging?

---

### Mini answers

1. An exchange rate shows the value of one currency in terms of another currency.

2. EUR is the base currency.

3. It means 1 USD equals 1.35 CAD.

4. Foreign exchange risk is the risk that currency movements affect the value of an investment.

5. A portfolio needs a base currency so all positions can be reported and compared in one currency.

6. Currency conversion is important because assets priced in different currencies cannot be added directly.

7. Currency hedging means reducing or neutralizing foreign exchange risk.

---

### Section summary

Currencies are traded through exchange rates.

A currency pair shows the value of one currency relative to another.

For international investors, currency movements can significantly affect returns.

For CFA Level 1, currencies are important because they introduce exchange rates, FX risk, base currency, quote currency and hedging.

For Athena AI Risk Terminal, currencies are essential because every asset price must be linked to a currency.

The key lesson is:

```text
A financial value is incomplete without its currency.
Currency movements can change the final return of an international investment.
```

---




















## 7. Commodities

Commodities are physical goods that are traded in financial markets.

They are real assets used in the economy for energy, production, consumption, construction, agriculture and industry.

Examples:

```text
Oil
Gold
Natural gas
Copper
Wheat
Corn
Silver
Coffee
Sugar
Soybeans
```

Commodities are different from stocks and bonds because they do not represent ownership in a company or a loan to an issuer.

A commodity is a real physical good.

Simple idea:

```text
Stock = ownership in a company
Bond = loan to an issuer
Commodity = physical good traded in the market
```

Commodities are important because they are directly linked to the real economy.

For example:

```text
Oil affects transportation and energy costs.
Wheat affects food prices.
Copper affects construction and industrial production.
Gold is often used as a store of value.
```

---

### Main categories of commodities

Commodities are usually grouped into major categories.

The main categories are:

```text
Energy commodities
Precious metals
Industrial metals
Agricultural commodities
Livestock
```

### Energy commodities

Energy commodities are used to produce power, heat and transportation fuel.

Examples:

```text
Crude oil
Natural gas
Gasoline
Heating oil
Coal
Electricity
```

Energy prices are often sensitive to:

```text
Global demand
Production levels
Geopolitical tensions
Inventories
Weather
Transportation capacity
OPEC decisions
```

Example:

```text
If oil production decreases while demand remains strong,
oil prices may rise.
```

Energy commodities can be highly volatile.

---

### Precious metals

Precious metals are rare metals often used for investment, jewelry, industry and reserves.

Examples:

```text
Gold
Silver
Platinum
Palladium
```

Gold is especially important in financial markets because it is often viewed as a store of value.

Gold prices can be affected by:

```text
Inflation expectations
Interest rates
Currency movements
Central bank reserves
Market stress
Investor demand
```

Simple idea:

```text
Gold is often treated as both a commodity and a financial asset.
```

Silver has both investment demand and industrial demand.

---

### Industrial metals

Industrial metals are used in manufacturing, construction and infrastructure.

Examples:

```text
Copper
Aluminum
Nickel
Zinc
Iron ore
Lithium
```

Industrial metals are strongly connected to economic growth.

Example:

```text
Copper is widely used in electrical wiring, construction and industrial equipment.
```

Because of this, copper is sometimes seen as a signal of global industrial activity.

If construction and manufacturing activity increase, demand for industrial metals may rise.

---

### Agricultural commodities

Agricultural commodities are crops and food-related products.

Examples:

```text
Wheat
Corn
Soybeans
Coffee
Sugar
Cotton
Cocoa
Rice
```

Agricultural prices are strongly affected by:

```text
Weather
Harvest quality
Crop yields
Storage levels
Transportation costs
Global demand
Government policies
```

Example:

```text
A drought can reduce wheat supply.
Lower supply can push wheat prices higher.
```

Agricultural commodities can be difficult to analyze because weather and seasonality matter a lot.

---

### Livestock

Livestock commodities are related to animals raised for food.

Examples:

```text
Live cattle
Feeder cattle
Lean hogs
```

Livestock prices can be influenced by:

```text
Feed costs
Disease outbreaks
Consumer demand
Weather
Processing capacity
Export demand
```

Livestock is usually less relevant for Athena’s first version, but it belongs to the broader commodity universe.

---

### Why commodities matter

Commodities matter because they affect companies, consumers, investors and governments.

They influence:

```text
Inflation
Production costs
Consumer prices
Corporate margins
Trade balances
Energy security
Economic growth
```

Example:

```text
If oil prices rise,
transportation costs may increase.
This can affect airlines, shipping companies and consumers.
```

Another example:

```text
If wheat prices rise,
food producers may face higher input costs.
```

Commodities are also important for diversification because they may behave differently from stocks and bonds.

---

### Main drivers of commodity prices

Commodity prices are mainly driven by supply and demand.

However, the details depend on the specific commodity.

Important drivers include:

```text
Production levels
Storage levels
Inventories
Geopolitical events
Weather
Transportation costs
Global demand
Currency movements
Interest rates
Speculation
Seasonality
Government regulation
Technological change
```

### Supply

Supply refers to how much of a commodity is available.

Example:

```text
Oil supply depends on production from oil-producing countries.
Wheat supply depends on harvest levels.
Copper supply depends on mining production.
```

If supply decreases while demand stays constant, prices often rise.

### Demand

Demand refers to how much buyers want or need the commodity.

Example:

```text
Oil demand increases when transportation and industrial activity increase.
Copper demand increases when construction and manufacturing activity increase.
```

If demand increases while supply stays constant, prices often rise.

### Inventories

Inventories are stored quantities of a commodity.

Example:

```text
Oil inventories
Natural gas storage
Grain inventories
Metal warehouse stocks
```

High inventories can reduce price pressure.

Low inventories can make prices more sensitive to supply shocks.

### Weather

Weather is especially important for agricultural and energy commodities.

Example:

```text
A cold winter can increase natural gas demand.
A drought can reduce crop production.
A hurricane can disrupt oil production.
```

Weather risk makes some commodity prices very volatile.

### Geopolitical events

Geopolitical events can affect supply routes, production and trade.

Example:

```text
Conflict in an oil-producing region may reduce expected oil supply.
```

This can increase oil prices even before actual supply falls, because markets react to expectations.

---

### Spot price

The spot price is the current price for immediate delivery of a commodity.

Simple idea:

```text
Spot price = price today for delivery now
```

Example:

```text
Gold spot price = current market price of gold for immediate delivery.
```

Spot prices are useful because they show the current market value of a commodity.

However, many investors do not trade the physical commodity directly.

They often use futures, ETFs or commodity-related stocks.

---

### Futures price

A futures price is the price agreed today for delivery at a future date.

Simple idea:

```text
Futures price = price today for delivery later
```

Example:

```text
Oil futures contract for delivery in 3 months = 80 USD per barrel
```

This means market participants agree today on a price for future delivery.

Futures are important in commodity markets because many commodities are expensive or difficult to store physically.

Example:

```text
It is easier for an investor to buy an oil futures contract
than to physically store barrels of oil.
```

---

### Spot price vs futures price

Spot and futures prices are related, but they are not always equal.

Simple comparison:

```text
Spot price = current delivery
Futures price = future delivery
```

Example:

```text
Gold spot price = 2,300
Gold futures price for 6 months = 2,340
```

The difference may reflect:

```text
Storage costs
Interest rates
Insurance costs
Convenience yield
Supply and demand expectations
```

This is why commodities can be more complex than simple stock price series.

---

### Contango and backwardation

Commodity futures markets often use two important terms:

```text
Contango
Backwardation
```

### Contango

Contango happens when futures prices are higher than the spot price.

Simple idea:

```text
Futures price > Spot price
```

Example:

```text
Oil spot price = 80
Oil futures price = 84
```

This may happen when storage costs, financing costs or future expectations push futures prices above spot prices.

### Backwardation

Backwardation happens when futures prices are lower than the spot price.

Simple idea:

```text
Futures price < Spot price
```

Example:

```text
Oil spot price = 80
Oil futures price = 76
```

This may happen when current demand is strong or current supply is tight.

For CFA Level 1, the key point is to understand that commodity futures returns can differ from spot commodity price changes.

---

### Commodity exposure

Investors can get commodity exposure in different ways.

Common methods include:

```text
Physical commodity ownership
Futures contracts
Commodity ETFs
Commodity mutual funds
Commodity-producing company stocks
Commodity indices
```

### Physical ownership

Physical ownership means owning the commodity directly.

Example:

```text
Buying physical gold.
```

This is possible for some commodities, but difficult for others.

Example:

```text
It is not practical for most investors to store crude oil or wheat.
```

### Futures contracts

Futures contracts are common in commodity markets.

They allow investors and companies to lock in future prices.

Example:

```text
An airline may use oil futures to hedge fuel costs.
```

### Commodity ETFs

Commodity ETFs give investors easier access to commodity exposure.

Example:

```text
A gold ETF may provide exposure to gold prices.
An oil ETF may provide exposure to oil futures.
```

ETF structure matters because some commodity ETFs hold physical commodities, while others use futures.

### Commodity-producing stocks

Investors can also buy stocks of companies linked to commodities.

Examples:

```text
Oil producers
Gold mining companies
Copper mining companies
Agricultural companies
```

However, these are still stocks. Their prices depend on both commodity prices and company-specific factors.

---

### Commodities and inflation

Commodities are closely connected to inflation.

Many commodities are inputs in the economy.

Example:

```text
Oil affects transportation costs.
Natural gas affects heating and energy costs.
Wheat affects food prices.
Copper affects construction costs.
```

When commodity prices rise broadly, production costs and consumer prices may increase.

This is why commodities are often discussed in relation to inflation.

Some investors use commodities as a potential inflation hedge.

However, this relationship is not perfect and can vary across time and commodity types.

---

### Commodities and diversification

Commodities may help diversify a portfolio because they can behave differently from stocks and bonds.

Example:

```text
Stocks may fall during an inflation shock.
Some commodities may rise if inflation is driven by higher raw material prices.
```

However, commodities are not automatically safe.

They can be very volatile and may experience large price swings.

Simple idea:

```text
Commodities can diversify risk,
but they also introduce their own risks.
```

For Athena, this makes commodities interesting for portfolio risk analysis.

---

### Commodity risks

Commodity investments have specific risks.

Important risks include:

```text
Price volatility
Supply shock risk
Demand shock risk
Geopolitical risk
Weather risk
Storage risk
Liquidity risk
Currency risk
Futures roll risk
Regulatory risk
```

### Price volatility

Commodity prices can move sharply over short periods.

Example:

```text
Oil prices can change quickly after geopolitical news.
```

### Weather risk

Weather can strongly affect agricultural and energy commodities.

Example:

```text
A drought may reduce crop supply.
A warm winter may reduce natural gas demand.
```

### Storage risk

Some commodities require storage.

Example:

```text
Oil must be stored in tanks.
Wheat must be stored in appropriate facilities.
```

Storage constraints can affect prices.

### Futures roll risk

If an investor uses futures contracts, the contracts eventually expire.

The investor may need to sell the expiring contract and buy a later contract.

This process is called rolling.

Roll returns can be positive or negative depending on the futures curve.

This is especially important for commodity ETFs that use futures.

---

### Commodity data needed in Athena

A clean commodity record may include:

```text
commodity_name
commodity_category
ticker_or_symbol
price_type
currency
unit
exchange
data_source
frequency
```

Example:

```text
commodity_name: Crude Oil
commodity_category: Energy
price_type: Futures
currency: USD
unit: barrel
exchange: NYMEX
frequency: Daily
```

Another example:

```text
commodity_name: Gold
commodity_category: Precious metal
price_type: Spot
currency: USD
unit: troy ounce
exchange: Global market
frequency: Daily
```

The unit is important because commodities are quoted in different units.

Examples:

```text
Oil = price per barrel
Gold = price per troy ounce
Natural gas = price per MMBtu
Wheat = price per bushel
Copper = price per pound or metric ton
```

A commodity price without a unit can be misleading.

---

### Commodity analysis in Athena

Athena can analyze commodities using market price series.

Possible analytics include:

```text
Price history
Daily returns
Annualized volatility
Rolling volatility
Correlation with equities
Correlation with inflation indicators
Commodity category exposure
Drawdown analysis
Liquidity indicators
```

Example use case:

```text
Analyze whether gold behaves differently from an equity index during market stress.
```

Another example:

```text
Compare oil volatility with equity market volatility.
```

For the first version of Athena, commodities can be represented through:

```text
Commodity ETFs
Simple spot price series
Simple futures price series
```

A more advanced version can add:

```text
Futures curves
Contango and backwardation analysis
Roll yield
Commodity sector exposure
Inflation sensitivity
```

---

### Commodity ETFs in Athena

Commodity ETFs are practical for the first version of Athena because they behave like tradable securities from a data perspective.

Example:

```text
Gold ETF → easier than storing gold
Oil ETF → easier than trading oil futures directly
Commodity index ETF → diversified commodity exposure
```

However, Athena should clearly display what the ETF actually tracks.

Example:

```text
Physical gold ETF
Oil futures ETF
Broad commodity index ETF
Commodity producer equity ETF
```

These are not the same type of exposure.

A gold mining ETF is not the same as physical gold exposure.

Simple distinction:

```text
Gold ETF holding physical gold = commodity exposure
Gold mining ETF = equity exposure linked to gold companies
```

This distinction is important for risk analysis.

---

### CFA Level 1 takeaway

For CFA Level 1, commodities are important because they are real assets with prices driven mainly by supply and demand.

Important concepts include:

```text
Spot price
Futures price
Supply and demand
Storage costs
Contango
Backwardation
Inflation sensitivity
Commodity exposure
Futures roll risk
Diversification
```

A simple memory rule:

```text
Commodity = physical good + supply/demand risk + often futures-based exposure
```

Unlike stocks, commodities do not produce company earnings.

Unlike bonds, commodities do not pay coupons.

Their return usually comes from price changes or futures-based exposure.

---

### Athena implementation takeaway

For Athena, commodities should be handled carefully because commodity data has specific characteristics.

The commodity module should support:

```text
Commodity category identification
Spot or futures price classification
Currency and unit storage
Historical price loading
Return calculation
Volatility calculation
Commodity ETF mapping
Futures exposure flag
Data quality checks
```

Important fields to avoid confusion:

```text
currency
unit
price_type
exchange
commodity_category
```

Example:

```text
Gold price in USD per troy ounce
Oil price in USD per barrel
Wheat price in USD per bushel
```

The goal is to prevent Athena from treating all commodity price series as if they were ordinary stock prices.

---

### Mini revision questions

1. What is a commodity?

2. What are the main categories of commodities?

3. What is the difference between a spot price and a futures price?

4. What does contango mean?

5. What does backwardation mean?

6. Why are commodities linked to inflation?

7. Why can commodity ETFs be different from direct commodity exposure?

8. Why should Athena store the unit of a commodity price?

---

### Mini answers

1. A commodity is a physical good traded in financial markets.

2. The main categories include energy, precious metals, industrial metals, agricultural commodities and livestock.

3. A spot price is the current price for immediate delivery, while a futures price is the price agreed today for delivery at a future date.

4. Contango means futures prices are higher than the spot price.

5. Backwardation means futures prices are lower than the spot price.

6. Commodities are linked to inflation because they are inputs in energy, food, transportation and production costs.

7. Commodity ETFs can differ from direct exposure because some hold physical commodities, some use futures, and some hold commodity-related stocks.

8. Athena should store the unit because commodities are quoted in different units, such as barrels, bushels or troy ounces.

---

### Section summary

Commodities are physical goods traded in markets.

They include energy products, metals, agricultural goods and livestock.

Their prices are mainly driven by supply, demand, inventories, weather, geopolitical events and global economic activity.

For CFA Level 1, commodities are important because they introduce real assets, spot prices, futures prices, contango, backwardation and inflation sensitivity.

For Athena AI Risk Terminal, commodities are useful for market analysis, diversification analysis and inflation-related risk monitoring.

The key lesson is:

```text
A commodity is a real economic input.
Its price reflects physical supply, demand, storage, delivery and market expectations.
```

---











## Part II — Market data and return calculations


## 8. Market data

Market data is information about financial instruments observed in financial markets.

It describes what happened in the market, when it happened, and under which conditions.

Common market data includes:

```text
Date
Timestamp
Open price
High price
Low price
Close price
Adjusted close
Volume
Bid price
Ask price
Currency
Exchange
Trading venue
```

Market data is the raw material of financial analysis.

Without reliable market data, calculations such as returns, volatility, correlation, liquidity and risk metrics cannot be trusted.

Simple idea:

```text
Bad data → bad calculations → bad decisions
```

For Athena AI Risk Terminal, market data must be treated as a core input, not as a secondary detail.

---

### Why market data matters

Market data matters because almost every market finance calculation depends on it.

Examples:

```text
Returns require prices.
Volatility requires returns.
Liquidity analysis requires volume, bid and ask data.
Benchmark comparison requires index data.
Portfolio valuation requires asset prices and currencies.
Risk metrics require clean historical observations.
```

If the price data is wrong, the return will be wrong.

If the return is wrong, the volatility will be wrong.

If the volatility is wrong, the risk analysis will be unreliable.

This is why a serious financial platform must validate market data before using it.

---

### Types of market data

Market data can be grouped into several categories.

Common categories include:

```text
Price data
Volume data
Quote data
Reference data
Corporate action data
Index data
Foreign exchange data
Fundamental data
```

### Price data

Price data describes traded prices.

Examples:

```text
Open price
High price
Low price
Close price
Adjusted close
Last traded price
```

Price data is used to calculate returns and price movements.

### Volume data

Volume data measures how many shares, contracts or units were traded.

Example:

```text
Volume = 5,000,000 shares
```

Volume helps analyze liquidity and market activity.

### Quote data

Quote data shows prices available from buyers and sellers.

Common quote fields:

```text
Bid price
Ask price
Bid size
Ask size
Bid-ask spread
```

Quote data is especially useful for liquidity and trading cost analysis.

### Reference data

Reference data describes the instrument itself.

Examples:

```text
Symbol
Name
Asset class
Currency
Exchange
Country
Sector
Industry
Issuer
```

Reference data helps Athena understand what the asset is before analyzing its prices.

### Corporate action data

Corporate action data describes events that affect securities.

Examples:

```text
Dividends
Stock splits
Reverse splits
Spin-offs
Rights issues
Distributions
```

Corporate actions are important because they can affect historical prices and returns.

### Index data

Index data describes market indices.

Examples:

```text
Index level
Index constituents
Index weights
Index return type
```

Index data is useful for benchmarks and relative performance analysis.

### Foreign exchange data

Foreign exchange data gives exchange rates between currencies.

Examples:

```text
USD/CAD
EUR/USD
GBP/USD
USD/JPY
```

FX data is required when Athena handles multi-currency portfolios.

### Fundamental data

Fundamental data describes company financial information.

Examples:

```text
Revenue
Earnings
Book value
Debt
Cash flow
Dividends
```

Fundamental data is not the main focus of this document, but it can be useful later for equity analysis.

---

### Raw data vs cleaned data

Raw data is data exactly as collected from a provider.

Cleaned data is data after validation, correction and standardization.

Simple comparison:

```text
Raw data = provider output
Cleaned data = validated and usable data
```

Raw data may contain problems.

Examples:

```text
Missing prices
Duplicated dates
Wrong currency
Wrong ticker
Wrong exchange
Extreme outliers
Unadjusted prices
Stale prices
Inconsistent timestamps
Mixed data frequencies
```

Cleaned data should be safer to use for financial calculations.

Cleaning steps may include:

```text
Remove duplicate rows
Detect missing values
Validate price fields
Validate volume fields
Check currency consistency
Check exchange consistency
Detect suspicious outliers
Adjust for corporate actions
Align dates across assets
Standardize column names
```

Athena should never assume that raw data is automatically correct.

---

### Example of raw data issue

Suppose Athena receives the following prices:

```text
Date         Close
2026-01-01   100
2026-01-02   102
2026-01-03   0
2026-01-04   103
```

The price of 0 is suspicious.

It may represent:

```text
A data error
A missing value incorrectly stored as zero
A failed data provider response
```

If Athena calculates returns without checking this value, the result will be wrong.

Example:

```text
Return from 102 to 0 = -100%
Return from 0 to 103 = impossible or undefined
```

The correct action is not to silently use the data.

Athena should flag the observation for review or correction.

---

### End-of-day data vs intraday data

Market data can have different frequencies.

Two common types are:

```text
End-of-day data
Intraday data
```

### End-of-day data

End-of-day data summarizes one trading day.

Common fields:

```text
Open
High
Low
Close
Adjusted close
Volume
```

This is often enough for long-term return, volatility and portfolio analysis.

For Athena’s first version, end-of-day data is the best starting point.

### Intraday data

Intraday data records market activity inside the trading day.

Examples:

```text
1-minute prices
5-minute prices
Hourly prices
Tick-by-tick data
```

Intraday data is more detailed but also more complex.

It requires careful handling of:

```text
Time zones
Market hours
Large data volume
Bid-ask bounce
Microstructure noise
Trading halts
```

For the first version of Athena, intraday data is not required.

---

### Time and timestamps

Time is critical in market data.

A price without a date or timestamp is incomplete.

Example:

```text
AAPL close price = 180
```

This is not enough.

A complete observation needs time information:

```text
AAPL close price = 180
Date = 2026-04-29
Currency = USD
Exchange = NASDAQ
```

For intraday data, Athena also needs a timestamp and time zone.

Example:

```text
Timestamp = 2026-04-29 10:35:00 America/New_York
```

Time zones matter because markets operate in different regions.

---

### Data provider

A data provider is the source of the market data.

Examples of provider types:

```text
Exchange
Broker
Market data vendor
Public API
Financial database
Internal data system
```

Different providers may report slightly different values depending on methodology, timing and adjustments.

For Athena, the data source should be stored.

Example:

```text
symbol: AAPL
date: 2026-04-29
close: 180.50
currency: USD
data_source: Market data provider
```

This helps with auditability and debugging.

Simple idea:

```text
A number is more trustworthy when its source is known.
```

---

### Data lineage

Data lineage means tracking where data came from and how it was transformed.

Example:

```text
Raw provider data
        ↓
Column standardization
        ↓
Missing value check
        ↓
Corporate action adjustment
        ↓
Return calculation
        ↓
Volatility calculation
```

Data lineage is important because users and developers need to understand how a final metric was produced.

If Athena displays annualized volatility, the system should be able to trace it back to:

```text
The price series used
The return type used
The date range used
The volatility formula used
The data cleaning rules applied
```

This makes the platform more transparent and reliable.

---

### Market data fields

A standard daily market data record may include:

```text
symbol
date
open
high
low
close
adjusted_close
volume
currency
exchange
data_source
```

Example:

```text
symbol: AAPL
date: 2026-04-29
open: 172.10
high: 175.20
low: 171.50
close: 174.60
adjusted_close: 174.60
volume: 54,000,000
currency: USD
exchange: NASDAQ
data_source: Market data provider
```

A quote data record may include:

```text
symbol
timestamp
bid
ask
bid_size
ask_size
currency
exchange
data_source
```

Example:

```text
symbol: AAPL
timestamp: 2026-04-29 10:30:00
bid: 174.55
ask: 174.60
bid_size: 200
ask_size: 300
currency: USD
exchange: NASDAQ
data_source: Market data provider
```

---

### Data validation

Data validation checks whether the data is usable.

Basic validation rules include:

```text
Price should not be negative
Volume should not be negative
Date should not be missing
Currency should be defined
Exchange should be defined
Symbol should be defined
Duplicate dates should be flagged
Missing prices should be flagged
Extreme returns should be reviewed
```

Example validation issue:

```text
Close price = -50
```

This should be rejected because a normal stock price cannot be negative.

Another issue:

```text
Volume = -1,000
```

This should also be rejected.

Athena should produce warnings when data quality is poor.

---

### Data standardization

Data standardization means converting data into a consistent format.

Different providers may use different column names.

Example:

```text
Provider A: adj_close
Provider B: adjustedClose
Provider C: adjusted_close_price
```

Athena should standardize these into one internal name:

```text
adjusted_close
```

This makes the backend easier to maintain.

Standardization can apply to:

```text
Column names
Date formats
Currency codes
Exchange names
Ticker formats
Asset class labels
```

Example:

```text
US Dollar
USD
usd
U.S. dollar
```

All should be standardized to:

```text
USD
```

---

### Data quality warnings

Athena should not hide data problems.

Instead, it should display clear warnings.

Examples:

```text
Missing adjusted close for selected period.
Duplicate price observations detected.
Currency is missing for this asset.
Large one-day return detected.
Volume is missing for several dates.
Data provider returned stale prices.
```

A warning does not always mean the data is unusable.

It means the user should be careful.

Example:

```text
A large one-day return may be a real market event,
or it may be a data error.
```

Athena should flag it, not automatically delete it.

---

### Market data and calculations

Market data feeds the calculation engine.

Examples:

```text
Close prices → price returns
Adjusted close prices → adjusted returns
Returns → volatility
Returns across assets → correlation
Bid and ask → bid-ask spread
Volume → liquidity indicator
Index levels → benchmark returns
FX rates → currency conversion
```

This is why the data layer must be stable before advanced analytics are added.

A simple pipeline:

```text
Market data
    ↓
Validation
    ↓
Cleaning
    ↓
Standardization
    ↓
Calculation
    ↓
Dashboard
```

---

### Market data in Athena

Athena should treat market data as a first-class domain object.

Possible entities:

```text
Asset
MarketPrice
MarketQuote
MarketIndex
ExchangeRate
CorporateAction
DataQualityWarning
DataSource
```

### Asset

Stores information about the instrument.

```text
symbol
name
asset_class
currency
exchange
country
sector
```

### MarketPrice

Stores historical prices.

```text
symbol
date
open
high
low
close
adjusted_close
volume
```

### MarketQuote

Stores bid and ask information.

```text
symbol
timestamp
bid
ask
bid_size
ask_size
```

### ExchangeRate

Stores currency conversion data.

```text
currency_pair
base_currency
quote_currency
rate
date
```

### DataQualityWarning

Stores data issues detected by Athena.

```text
symbol
date
warning_type
severity
message
```

This structure helps separate raw market observations from calculated metrics.

---

### Example Athena data flow

A possible Athena data flow:

```text
1. Load raw market data from provider
2. Standardize column names
3. Validate required fields
4. Detect missing values
5. Detect duplicate observations
6. Detect suspicious price movements
7. Store clean price series
8. Calculate returns
9. Calculate volatility
10. Display analytics and warnings
```

This makes the system easier to test and debug.

---

### CFA Level 1 takeaway

For CFA Level 1, market data is important because it supports investment analysis.

Important concepts include:

```text
Price data
Volume data
Bid and ask quotes
Adjusted prices
Index levels
Exchange rates
Data quality
Return calculation
Benchmark comparison
```

A simple memory rule:

```text
Market data is the evidence.
Financial analysis is the interpretation.
```

If the evidence is wrong, the interpretation may be wrong.

---

### Athena implementation takeaway

For Athena, market data must be reliable, consistent and traceable.

The market data module should support:

```text
Historical price storage
Quote data storage
Currency identification
Exchange identification
Data source tracking
Data validation
Data cleaning
Data quality warnings
Standardized field names
```

The goal is not only to collect data.

The goal is to create a trusted data foundation for every financial calculation in the platform.

---

### Mini revision questions

1. What is market data?

2. Why is market data important for financial analysis?

3. What is the difference between raw data and cleaned data?

4. Give three examples of common market data fields.

5. Why should Athena store the data source?

6. Why is a price without a date incomplete?

7. What is a data quality warning?

8. Why should Athena validate data before calculating returns?

---

### Mini answers

1. Market data is information about financial instruments observed in financial markets.

2. It is important because returns, volatility, liquidity, correlations and risk metrics depend on it.

3. Raw data is data as received from a provider. Cleaned data has been validated, corrected and standardized.

4. Examples include close price, adjusted close, volume, bid, ask, currency and exchange.

5. Athena should store the data source for traceability, auditability and debugging.

6. A price without a date is incomplete because market prices change over time.

7. A data quality warning is a message that alerts the user to a potential data problem.

8. Athena should validate data first because incorrect prices can create incorrect returns and unreliable risk metrics.

---

### Section summary

Market data is the foundation of financial analysis.

It includes prices, volumes, quotes, currencies, exchanges, index levels and other market observations.

For CFA Level 1, market data is important because it supports return calculation, benchmark comparison, liquidity analysis and risk measurement.

For Athena AI Risk Terminal, market data is one of the most important modules because every advanced calculation depends on it.

The key lesson is:

```text
Market data must be clean, consistent and traceable before it can support reliable financial analysis.
```
---












## 10. Adjusted close and corporate actions

The adjusted close is a historical price field that corrects past prices for corporate actions.

Corporate actions are events decided by a company that can affect its shares, its shareholders or its historical price series.

Common corporate actions include:

```text
Dividends
Stock splits
Reverse splits
Special dividends
Spin-offs
Rights issues
Distributions
```

The adjusted close is important because it helps analysts calculate returns that better reflect the investor’s real economic experience.

Simple idea:

```text
Close price = raw market closing price
Adjusted close = closing price adjusted for corporate actions
```

For return calculations, the adjusted close is often more useful than the raw close.

---

### Why adjusted close matters

A stock price can change because of normal market movements.

But it can also change mechanically because of a corporate action.

Example:

```text
A company pays a dividend.
The stock price may drop after the dividend date.
```

This price drop does not necessarily mean the investor lost value.

Why?

Because the investor received cash through the dividend.

If Athena uses only the raw close price, it may interpret the mechanical price drop as a real loss.

The adjusted close helps avoid this problem.

Simple idea:

```text
Adjusted close tries to measure economic return more accurately.
```

---

### Corporate actions

Corporate actions are company events that may affect shareholders.

Important examples include:

```text
Dividends
Stock splits
Reverse splits
Special dividends
Spin-offs
Rights issues
Distributions
```

These events matter because they can create artificial jumps or drops in historical price data.

If those events are ignored, return calculations may be misleading.

---

### Dividends

A dividend is a payment made by a company to its shareholders.

Example:

```text
Stock price before dividend = 100
Dividend paid = 2
```

After the dividend, the stock price may mechanically fall.

Example:

```text
Stock price after dividend = 98
```

At first glance, this looks like a 2% loss.

But the investor received 2 in cash.

The economic value is approximately:

```text
Stock value after dividend + dividend received
= 98 + 2
= 100
```

So the investor did not necessarily lose money.

This is why adjusted close is useful.

It adjusts the historical price series to reflect dividends more accurately.

---

### Stock splits

A stock split increases the number of shares and reduces the price per share.

Example:

```text
2-for-1 stock split
```

This means:

```text
Before split:
Investor owns 1 share at 200

After split:
Investor owns 2 shares at 100 each
```

The total value is the same:

```text
Before: 1 × 200 = 200
After:  2 × 100 = 200
```

Without adjustment, the raw price series would show:

```text
Price moves from 200 to 100
```

This looks like:

```text
Return = -50%
```

But economically, the investor did not lose 50%.

The number of shares doubled.

Adjusted close corrects the historical price series so the split does not create a false crash.

---

### Reverse splits

A reverse split reduces the number of shares and increases the price per share.

Example:

```text
1-for-5 reverse split
```

This means:

```text
Before reverse split:
Investor owns 5 shares at 20 each

After reverse split:
Investor owns 1 share at 100
```

The total value is the same:

```text
Before: 5 × 20 = 100
After:  1 × 100 = 100
```

Without adjustment, the price series may look like the stock jumped from 20 to 100.

This would appear to be a 400% gain.

But it is not a real investment gain.

It is a mechanical adjustment caused by the reverse split.

---

### Special dividends

A special dividend is a large non-recurring dividend.

Unlike regular dividends, special dividends are not expected to happen regularly.

Example:

```text
Stock price before special dividend = 100
Special dividend = 10
Stock price after special dividend = 90
```

The raw price falls sharply, but the shareholder receives cash.

If this is not adjusted correctly, Athena may detect a large negative return even though the investor received value through the special dividend.

Special dividends can create large distortions in return calculations.

---

### Spin-offs

A spin-off happens when a company separates part of its business into a new company.

Example:

```text
Company A creates Company B.
Shareholders of Company A receive shares of Company B.
```

After the spin-off, the price of Company A may fall because part of its value has moved into Company B.

This does not necessarily mean shareholders lost value.

They may now own:

```text
Shares of Company A
Shares of Company B
```

Spin-offs can make historical price analysis more complex.

A clean data provider should adjust price history to reflect the economic effect of the spin-off.

---

### Rights issues

A rights issue allows existing shareholders to buy new shares, often at a discounted price.

Example:

```text
A company offers shareholders the right to buy additional shares at 80
when the current market price is 100.
```

Rights issues can affect the stock price because new shares are created and existing ownership may be diluted.

They can also affect historical returns if not handled properly.

For Athena’s first version, the most important point is to detect that a corporate action happened and rely on adjusted price data when available.

---

### Close price vs adjusted close

The close price is the last traded price of the day.

The adjusted close is the close price modified to account for corporate actions.

Simple comparison:

```text
Close price:
Raw closing market price.

Adjusted close:
Closing price adjusted for dividends, splits and other corporate actions.
```

Example:

```text
Raw close may show a sharp drop after a stock split.
Adjusted close removes the artificial drop.
```

For historical return analysis, adjusted close is usually preferred.

For actual trading execution analysis, raw close may be more relevant because it reflects the actual quoted price at that time.

---

### Return calculation problem

Suppose a stock has a 2-for-1 split.

Raw close data:

```text
Date        Close
Day 1       200
Day 2       100
```

Using raw close:

```text
Return = 100 / 200 - 1
Return = -50%
```

This is wrong economically.

The investor owns twice as many shares after the split.

Adjusted close may look like:

```text
Date        Adjusted Close
Day 1       100
Day 2       100
```

Using adjusted close:

```text
Return = 100 / 100 - 1
Return = 0%
```

This better reflects the economic reality of the split.

---

### When to use adjusted close

Use adjusted close when calculating:

```text
Historical returns
Cumulative performance
Volatility
Correlation
Drawdowns
Backtests
Portfolio performance
```

Adjusted close helps avoid artificial returns caused by corporate actions.

Practical rule:

```text
Use adjusted close for historical performance analysis.
```

---

### When to use raw close

Raw close can still be useful.

Use raw close when analyzing:

```text
Actual market quotes
Trading execution
Order pricing
Intraday trading
Technical market levels
Official closing prices
```

Raw close shows what the market price actually was at the end of the trading session.

Practical rule:

```text
Use raw close when the actual observed closing price matters.
```

---

### Adjusted close and dividends

Dividends are one of the most important reasons to use adjusted close.

Example:

```text
Day 1 close = 100
Dividend = 2
Day 2 close = 98
```

Using raw close:

```text
Return = 98 / 100 - 1
Return = -2%
```

But the investor received a dividend of 2.

Economic return is closer to:

```text
(98 + 2) / 100 - 1 = 0%
```

Adjusted close helps reflect this logic automatically.

This is especially important for long-term analysis because dividends can represent a large part of total return.

---

### Adjusted close and backtesting

Backtesting means testing an investment strategy using historical data.

If a backtest uses unadjusted prices, the results may be wrong.

Example:

```text
A stock split may appear as a major crash.
A dividend may appear as a negative return.
A reverse split may appear as a huge gain.
```

This can distort:

```text
Strategy returns
Volatility
Drawdowns
Risk metrics
Buy and sell signals
```

For Athena, adjusted data is essential if the platform later supports backtesting.

---

### Data quality issues

Adjusted close depends on the data provider.

Different providers may apply adjustments differently.

Possible issues include:

```text
Missing adjusted close
Incorrect split adjustment
Incorrect dividend adjustment
Delayed corporate action update
Inconsistent adjustment methodology
```

Athena should detect and report when adjusted close is missing.

Example warning:

```text
Adjusted close is missing for this asset.
Returns may be distorted by corporate actions.
```

This warning helps the user understand that the analysis may be less reliable.

---

### Corporate action data needed in Athena

A clean corporate action record may include:

```text
symbol
corporate_action_type
ex_date
record_date
payment_date
effective_date
amount
split_ratio
currency
data_source
```

Example for a dividend:

```text
symbol: AAPL
corporate_action_type: Dividend
ex_date: 2026-02-10
amount: 0.25
currency: USD
data_source: Market data provider
```

Example for a stock split:

```text
symbol: AAPL
corporate_action_type: Stock split
effective_date: 2026-06-01
split_ratio: 2-for-1
data_source: Market data provider
```

For Athena’s first version, it is not necessary to manually calculate all adjustments.

However, Athena should know whether the price field used is adjusted or unadjusted.

---

### Adjusted close in Athena

Athena should clearly identify which price field is used for calculations.

Possible fields:

```text
close
adjusted_close
price_used_for_returns
adjustment_status
```

Example:

```text
symbol: AAPL
date: 2026-04-29
close: 180.00
adjusted_close: 179.50
price_used_for_returns: adjusted_close
adjustment_status: adjusted
```

This makes the calculation transparent.

The user should know whether performance metrics are based on raw close or adjusted close.

---

### CFA Level 1 takeaway

For CFA Level 1, adjusted close is important because return calculations must reflect the investor’s real economic return.

Important concepts include:

```text
Dividends
Stock splits
Reverse splits
Special dividends
Corporate actions
Price return
Total return
Adjusted price data
Historical performance
```

A simple memory rule:

```text
Corporate actions can change price data without changing investor wealth.
Adjusted close helps correct this problem.
```

---

### Athena implementation takeaway

For Athena, adjusted close should be the default field for historical return calculations when available.

The market data module should support:

```text
Close price storage
Adjusted close storage
Corporate action detection
Price field selection
Return calculation using adjusted close
Warning when adjusted close is missing
Documentation of the chosen price field
```

The goal is to avoid false returns caused by dividends, splits and other corporate actions.

---

### Mini revision questions

1. What is adjusted close?

2. Why can dividends distort raw price returns?

3. What happens in a 2-for-1 stock split?

4. Why can a reverse split create a false gain in raw price data?

5. When should adjusted close usually be used?

6. When can raw close still be useful?

7. Why should Athena warn users when adjusted close is missing?

---

### Mini answers

1. Adjusted close is the closing price adjusted for corporate actions such as dividends and stock splits.

2. Dividends can make the stock price drop mechanically, even though the investor receives cash.

3. In a 2-for-1 stock split, the investor owns twice as many shares and the price per share is roughly divided by two.

4. A reverse split increases the price per share mechanically, but the investor owns fewer shares, so it is not a real gain.

5. Adjusted close should usually be used for historical returns, volatility, correlation, drawdowns and backtests.

6. Raw close can be useful for actual market quotes, trading execution and official closing price analysis.

7. Athena should warn users because returns calculated without adjusted close may be distorted by corporate actions.

---

### Section summary

Adjusted close corrects historical prices for corporate actions.

Corporate actions include dividends, stock splits, reverse splits, special dividends, spin-offs and rights issues.

For CFA Level 1, this section is important because accurate return calculation requires understanding how corporate actions affect prices.

For Athena AI Risk Terminal, adjusted close is essential because return, volatility and risk metrics depend on reliable historical prices.

The key lesson is:

```text
Raw prices show what traded in the market.
Adjusted prices help measure the investor’s economic return.
```











---
## 11. Volume

Volume is the number of shares, contracts or units traded during a specific period.

For stocks and ETFs, volume usually means the number of shares traded.

For futures and options, volume usually means the number of contracts traded.

Example:

```text
Volume = 5,000,000 shares
```

This means that 5 million shares were traded during the session.

Volume does not tell us the direction of the trade by itself.  
It only tells us how much trading activity occurred.

Simple idea:

```text
Volume = trading activity
```

---

### Why volume matters

Volume matters because it shows how active the market is for an asset.

High volume usually means many buyers and sellers are participating.

Low volume usually means fewer market participants.

Volume helps analysts understand:

```text
Liquidity
Trading activity
Market interest
Strength of price movements
Abnormal market events
Execution risk
```

Example:

```text
A stock rises by 5% with very high volume.
```

This may suggest strong market interest.

Another example:

```text
A stock rises by 5% with very low volume.
```

This move may be less reliable because only a small amount of trading activity occurred.

---

### Volume and liquidity

Volume is often used as a basic liquidity indicator.

A liquid asset is easier to buy or sell without strongly affecting its price.

High volume often means:

```text
More buyers and sellers
Easier execution
Lower transaction costs
Narrower bid-ask spreads
Lower slippage
```

Low volume can mean:

```text
Fewer market participants
Wider bid-ask spreads
Higher transaction costs
Harder execution
Higher slippage
```

However, volume alone is not a perfect measure of liquidity.

A better liquidity analysis may also include:

```text
Bid-ask spread
Order book depth
Trade size
Market impact
Turnover
```

For Athena’s first version, volume can be used as a simple and useful starting liquidity indicator.

---

### Volume period

Volume must always be interpreted with a time period.

Examples:

```text
Daily volume
Weekly volume
Monthly volume
Intraday volume
```

A volume number without a time period is incomplete.

Example:

```text
Volume = 1,000,000
```

This is unclear.

A better version is:

```text
Daily volume = 1,000,000 shares
```

or:

```text
Volume between 10:00 and 11:00 = 1,000,000 shares
```

In Athena, volume should always be linked to a date or timestamp.

---

### Average daily volume

Average daily volume is the average number of shares traded per day over a selected period.

Example:

```text
20-day average daily volume
60-day average daily volume
90-day average daily volume
```

Simple formula:

```text
Average daily volume = sum of daily volume over period / number of trading days
```

Example:

```text
Total volume over 5 days = 25,000,000 shares
Number of trading days = 5

Average daily volume = 25,000,000 / 5
Average daily volume = 5,000,000 shares
```

Average daily volume is useful because one trading day can be abnormal.

Averages help smooth short-term noise.

---

### Relative volume

Relative volume compares today’s volume with normal volume.

Simple idea:

```text
Relative volume = today’s volume / average volume
```

Example:

```text
Today’s volume = 10,000,000
Average daily volume = 5,000,000

Relative volume = 10,000,000 / 5,000,000
Relative volume = 2.0
```

This means today’s volume is twice the normal level.

High relative volume may indicate unusual market attention.

Possible reasons include:

```text
Earnings announcement
Important news
Analyst upgrade or downgrade
Market stress
Large institutional trading
Index rebalancing
```

In Athena, relative volume can help detect abnormal trading activity.

---

### Dollar volume

Share volume alone can be misleading because assets have different prices.

Example:

```text
Stock A:
Price = 10
Volume = 1,000,000 shares

Stock B:
Price = 500
Volume = 1,000,000 shares
```

Both stocks have the same share volume, but Stock B has much higher traded value.

Dollar volume measures the monetary value traded.

Formula:

```text
Dollar volume = price × volume
```

Example:

```text
Price = 50
Volume = 2,000,000 shares

Dollar volume = 50 × 2,000,000
Dollar volume = 100,000,000
```

This means approximately 100 million dollars of the asset traded during the period.

Dollar volume can be more useful than share volume when comparing assets with different prices.

---

### Volume spike

A volume spike happens when volume is much higher than usual.

Example:

```text
Average daily volume = 2,000,000 shares
Today’s volume = 12,000,000 shares
```

This is a large volume spike.

Volume spikes can happen because of:

```text
Earnings releases
Major news
Mergers and acquisitions
Regulatory announcements
Market panic
Index inclusion or removal
Large institutional orders
```

A volume spike does not automatically mean the price will rise or fall.

It means market activity is unusually high.

Athena can use volume spikes as warning signals or market activity indicators.

---

### Volume and price movement

Volume can help interpret price movements.

Example:

```text
Price increases with high volume
```

This may suggest strong buying interest.

Example:

```text
Price decreases with high volume
```

This may suggest strong selling pressure.

Example:

```text
Price moves sharply with low volume
```

This may indicate a less reliable or less liquid move.

However, volume should not be interpreted alone.

It should be combined with:

```text
Price movement
Bid-ask spread
News context
Volatility
Market conditions
```

---

### Volume is not the same as return

Volume measures trading activity.

Return measures price performance.

They answer different questions.

```text
Volume answers: how much was traded?
Return answers: how much did the price change?
```

Example:

```text
High volume with 0% return:
Many shares traded, but the price ended unchanged.

Low volume with +5% return:
Price increased, but with limited trading activity.
```

For Athena, both metrics are useful, but they should not be confused.

---

### Volume and market confidence

High volume can sometimes make a price movement more meaningful.

Example:

```text
A stock rises after earnings with very high volume.
```

This may suggest that many market participants agree with the new valuation.

But this is not guaranteed.

High volume can also appear during panic selling.

Example:

```text
A stock falls sharply with very high volume.
```

This may indicate strong selling pressure or forced liquidation.

Simple idea:

```text
High volume confirms activity, not direction.
```

---

### Volume limitations

Volume is useful, but it has limits.

Important limitations include:

```text
Volume does not show whether trades were buyer-initiated or seller-initiated.
Volume does not directly measure bid-ask spread.
Volume does not guarantee low trading cost.
Volume can be temporarily distorted by news or index events.
Volume may differ across exchanges and data providers.
```

For example:

```text
A stock may have high daily volume,
but still have poor liquidity for very large orders.
```

This is because large orders can move the market even when normal trading volume looks acceptable.

---

### Volume data quality

Volume data can also have quality problems.

Possible issues include:

```text
Missing volume
Zero volume on a normal trading day
Negative volume
Duplicated volume records
Incorrect exchange volume
Unadjusted volume after stock splits
Different provider methodologies
```

Example:

```text
Volume = -5,000
```

This should be rejected because trading volume cannot be negative.

Another example:

```text
Volume = 0 for a large actively traded stock on a normal trading day
```

This should be flagged as suspicious.

Athena should validate volume before using it in liquidity analysis.

---

### Volume after stock splits

Stock splits can affect historical volume.

Example:

```text
2-for-1 stock split
```

After the split, the number of shares outstanding increases.

Trading volume may appear different because each old share became two new shares.

Some data providers adjust historical volume to make it comparable.

Athena should document whether volume data is adjusted or raw.

Simple rule:

```text
Adjusted prices and adjusted volume should be handled consistently.
```

---

### Volume data needed in Athena

A clean volume record may include:

```text
symbol
date
volume
price
dollar_volume
average_daily_volume
relative_volume
currency
exchange
data_source
```

Example:

```text
symbol: AAPL
date: 2026-04-29
close: 180.00
volume: 50,000,000
dollar_volume: 9,000,000,000
currency: USD
exchange: NASDAQ
```

For Athena’s first version, the most important fields are:

```text
symbol
date
volume
close or adjusted close
dollar_volume
average_daily_volume
data_source
```

These fields are enough to build simple liquidity indicators.

---

### Volume analysis in Athena

Athena can use volume to support:

```text
Liquidity analysis
Trading activity monitoring
Abnormal volume detection
Volume trend analysis
Dollar volume calculation
Relative volume calculation
Data quality checks
```

Possible volume indicators:

```text
Daily volume
20-day average volume
60-day average volume
Relative volume
Dollar volume
Volume spike flag
```

Example output:

```text
Symbol: AAPL
Daily volume: 50,000,000
20-day average volume: 45,000,000
Relative volume: 1.11
Dollar volume: 9,000,000,000
Liquidity signal: Strong
```

This type of information can help users understand whether an asset is actively traded.

---

### CFA Level 1 takeaway

For CFA Level 1, volume is important because it is connected to liquidity and market activity.

Important concepts include:

```text
Trading volume
Liquidity
Bid-ask spread
Transaction costs
Slippage
Market activity
Dollar volume
Average daily volume
```

A simple memory rule:

```text
Volume measures activity.
Liquidity measures ease of trading.
```

High volume often supports liquidity, but it is not the only liquidity measure.

---

### Athena implementation takeaway

For Athena, volume should be used as an early liquidity signal.

The market data module should support:

```text
Volume storage
Volume validation
Average volume calculation
Dollar volume calculation
Relative volume calculation
Volume spike detection
Liquidity warning generation
```

Possible warning examples:

```text
Volume is missing for this asset.
Volume is unusually low.
Volume is unusually high compared with recent history.
Dollar volume is too low for reliable liquidity.
```

The goal is to help users understand whether an asset is actively traded and whether the price data is supported by enough market activity.

---

### Mini revision questions

1. What does trading volume measure?

2. Why is volume useful for liquidity analysis?

3. What is average daily volume?

4. What is relative volume?

5. Why can dollar volume be more useful than share volume?

6. Does high volume always mean the price will rise?

7. Why should Athena validate volume data?

---

### Mini answers

1. Trading volume measures the number of shares, contracts or units traded during a period.

2. Volume is useful because high trading activity often makes it easier to buy or sell an asset.

3. Average daily volume is the average number of shares or contracts traded per day over a selected period.

4. Relative volume compares today’s volume with normal volume.

5. Dollar volume includes both price and volume, making it easier to compare assets with different prices.

6. No. High volume means high activity, not necessarily a price increase.

7. Athena should validate volume data because missing, negative or abnormal volume can distort liquidity analysis.

---

### Section summary

Volume measures trading activity.

It shows how many shares, contracts or units were traded during a period.

For CFA Level 1, volume is important because it helps explain liquidity, trading activity, transaction costs and market participation.

For Athena AI Risk Terminal, volume is useful as a simple liquidity and activity indicator.

The key lesson is:

```text
Volume tells us how active the market is.
It does not tell us everything about liquidity, but it is one of the first signals to check.
```
---




















## 12. Nominal vs real returns

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




## 13. Nominal vs real returns

A nominal return is the return before adjusting for inflation.

A real return is the return after adjusting for inflation.

The difference matters because money can lose purchasing power over time.

Simple idea:

```text
Nominal return = return in money terms
Real return = return in purchasing power terms
```

Inflation reduces what money can buy.

Because of this, a positive nominal return does not always mean the investor became wealthier in real economic terms.

---

### What is inflation?

Inflation is the general increase in prices in an economy over time.

When inflation rises, the purchasing power of money falls.

Example:

```text
Today: 100 CAD buys a basket of goods.
One year later: the same basket costs 105 CAD.
```

The inflation rate is:

```text
5%
```

This means the investor needs 5% more money just to buy the same goods.

Simple idea:

```text
Inflation makes money less powerful.
```

---

### Nominal return

A nominal return measures the percentage increase in the value of an investment without considering inflation.

Example:

```text
Beginning value = 1,000
Ending value    = 1,080

Nominal return = 1,080 / 1,000 - 1
Nominal return = 8%
```

The investor has more money than before.

But this does not yet tell us whether the investor can buy more goods and services.

To answer that, we need the real return.

---

### Real return

A real return measures the return after adjusting for inflation.

It shows whether purchasing power increased or decreased.

Example:

```text
Nominal return = 8%
Inflation      = 3%
```

The investor’s wealth increased by 8% in money terms.

But prices increased by 3%.

So the investor’s purchasing power increased by approximately:

```text
8% - 3% = 5%
```

This is the approximate real return.

---

### Approximate formula

The simple approximation is:

```text
Real return ≈ Nominal return - Inflation
```

Example:

```text
Nominal return = 8%
Inflation      = 3%

Approximate real return = 8% - 3%
Approximate real return = 5%
```

This approximation is easy to understand and often useful when percentages are small.

However, it is not perfectly exact because returns and inflation compound.

---

### Exact formula

The exact formula is:

```text
Real return = (1 + nominal return) / (1 + inflation) - 1
```

Example:

```text
Nominal return = 8%
Inflation      = 3%
```

Convert percentages into decimals:

```text
Nominal return = 0.08
Inflation      = 0.03
```

Apply the exact formula:

```text
Real return = (1 + 0.08) / (1 + 0.03) - 1
Real return = 1.08 / 1.03 - 1
Real return = 0.0485
Real return = 4.85%
```

So:

```text
Approximate real return = 5.00%
Exact real return       = 4.85%
```

The approximation is close, but the exact formula is more precise.

---

### Why the exact formula is different

The exact formula is different because inflation affects the whole value of money.

If prices rise by 3%, the investor needs 1.03 times more money to maintain the same purchasing power.

That is why we divide by:

```text
1 + inflation
```

Simple interpretation:

```text
Nominal wealth grew by 1.08.
Prices grew by 1.03.
Real wealth grew by 1.08 / 1.03.
```

So the real return is:

```text
1.08 / 1.03 - 1 = 4.85%
```

---

### Purchasing power

Purchasing power means the amount of goods and services that money can buy.

Example:

```text
Year 0:
Investor has 1,000 CAD.
Basket price = 100 CAD.
Investor can buy 10 baskets.

Year 1:
Investor has 1,080 CAD.
Basket price = 103 CAD.
Investor can buy 1,080 / 103 = 10.49 baskets.
```

The investor can buy more baskets than before.

So purchasing power increased.

This is the meaning of a positive real return.

---

### Positive nominal return but low real return

A positive nominal return can still be weak if inflation is high.

Example:

```text
Nominal return = 6%
Inflation      = 5%
```

Approximate real return:

```text
Real return ≈ 6% - 5%
Real return ≈ 1%
```

The investor made money in nominal terms, but purchasing power increased only slightly.

This is important because investors care about what their money can actually buy.

---

### Positive nominal return but negative real return

A nominal gain can still produce a real loss.

Example:

```text
Nominal return = 4%
Inflation      = 7%
```

Approximate real return:

```text
Real return ≈ 4% - 7%
Real return ≈ -3%
```

The investment increased in money terms, but prices increased even more.

The investor has more money, but that money buys less than before.

Simple idea:

```text
More dollars does not always mean more purchasing power.
```

---

### Negative nominal return and inflation

If the nominal return is negative and inflation is positive, the real return is even worse.

Example:

```text
Nominal return = -5%
Inflation      = 4%
```

Approximate real return:

```text
Real return ≈ -5% - 4%
Real return ≈ -9%
```

The investor lost money, and the remaining money also lost purchasing power.

This is a double effect:

```text
Investment value decreased.
Purchasing power also decreased.
```

---

### Deflation case

Deflation is the opposite of inflation.

It means the general price level decreases.

Example:

```text
Nominal return = 2%
Inflation      = -1%
```

Approximate real return:

```text
Real return ≈ 2% - (-1%)
Real return ≈ 3%
```

When inflation is negative, purchasing power increases because prices fall.

Deflation is less common than inflation, but it can happen.

---

### Fisher relationship

The relationship between nominal return, real return and inflation is often linked to the Fisher equation.

The exact relationship is:

```text
1 + nominal return = (1 + real return) × (1 + inflation)
```

This can be rearranged as:

```text
Real return = (1 + nominal return) / (1 + inflation) - 1
```

This relationship is useful because it shows that nominal returns include two components:

```text
Real return
Inflation compensation
```

Simple idea:

```text
Nominal return compensates the investor for real growth and inflation.
```

---

### Real return and investment performance

Real return is important because it tells whether an investment truly increased wealth.

Example:

```text
Investment A:
Nominal return = 10%
Inflation      = 2%
Approximate real return = 8%

Investment B:
Nominal return = 10%
Inflation      = 9%
Approximate real return = 1%
```

Both investments have the same nominal return.

But Investment A creates much more real purchasing power.

This shows why nominal returns can be misleading when inflation changes.

---

### Real return and cash

Cash can lose purchasing power when inflation is high.

Example:

```text
Cash return = 1%
Inflation   = 5%
```

Approximate real return:

```text
Real return ≈ 1% - 5%
Real return ≈ -4%
```

Even if the cash balance increases slightly, the investor loses purchasing power.

This is why inflation is important for savings, cash management and long-term investing.

---

### Real return and bonds

Nominal vs real return is especially important for fixed income.

A bond may pay a fixed coupon.

Example:

```text
Bond yield = 4%
Inflation  = 6%
```

Approximate real return:

```text
Real return ≈ 4% - 6%
Real return ≈ -2%
```

The bond pays income, but inflation is higher than the nominal yield.

The investor’s purchasing power decreases.

This is one reason inflation can be dangerous for bond investors.

---

### Real return and equities

Stocks may offer protection against inflation over the long term, but this is not guaranteed.

Companies may raise prices when inflation rises.

However, inflation can also increase costs, reduce profit margins and raise interest rates.

Example:

```text
Inflation rises.
A company increases product prices.
But wages, materials and financing costs also increase.
```

The effect on stock returns depends on the company’s pricing power, costs and market conditions.

For Athena, this means inflation can be used later as a macroeconomic context variable.

---

### Real return and long-term investing

Real returns are especially important over long horizons.

Small differences in inflation can compound significantly over time.

Example:

```text
Nominal portfolio growth over 10 years = 80%
Inflation over 10 years = 35%
```

The investor’s purchasing power did not increase by 80%.

The real gain is lower because prices also increased.

Long-term investors should focus on real wealth, not only nominal account value.

---

### Nominal wealth vs real wealth

Nominal wealth is measured in currency units.

Real wealth is measured in purchasing power.

Example:

```text
Nominal wealth = 100,000 CAD
```

This number alone is incomplete.

The real question is:

```text
What can 100,000 CAD buy?
```

If prices rise significantly, the same 100,000 CAD buys less.

Simple comparison:

```text
Nominal wealth = amount of money
Real wealth = economic purchasing power
```

---

### Inflation index

Inflation is usually measured using a price index.

A common example is the Consumer Price Index, or CPI.

The CPI tracks the price of a basket of goods and services.

Example:

```text
CPI at start = 100
CPI at end   = 103
```

Inflation is:

```text
103 / 100 - 1 = 3%
```

This inflation rate can then be used to estimate real returns.

In a more advanced version, Athena could use CPI or other inflation data to calculate real returns.

---

### Nominal return vs real return example

Suppose an investor starts with:

```text
Initial investment = 10,000
```

After one year:

```text
Ending value = 10,800
Inflation    = 3%
```

Nominal return:

```text
10,800 / 10,000 - 1 = 8%
```

Exact real return:

```text
Real return = 1.08 / 1.03 - 1
Real return = 4.85%
```

Real ending value in beginning-year purchasing power:

```text
10,800 / 1.03 = 10,485.44
```

This means the ending value has the same purchasing power as approximately:

```text
10,485.44 at the beginning of the year
```

So the investor gained about:

```text
485.44 of real purchasing power
```

---

### Common beginner mistake

A common beginner mistake is to think:

```text
If my investment went up, I became richer.
```

This is not always true.

A better question is:

```text
Did my investment grow faster than inflation?
```

Example:

```text
Investment return = 3%
Inflation         = 6%
```

The investment increased in nominal value, but the investor lost purchasing power.

---

### Nominal vs real in performance reporting

Performance reports often show nominal returns.

Example:

```text
Portfolio return = 7%
```

But for a long-term investor, the real return may be more meaningful.

Example:

```text
Portfolio return = 7%
Inflation        = 4%
Approximate real return = 3%
```

Athena can display both values to give a clearer view of performance.

This is especially useful when inflation is high.

---

### Nominal vs real in Athena

For Athena AI Risk Terminal, nominal and real returns can support better performance analysis.

At first, Athena can calculate nominal returns using market prices.

Later, Athena can calculate real returns by adding inflation data.

Possible inputs:

```text
Nominal asset return
Inflation rate
Country or currency region
Time period
Inflation index
```

Possible output:

```text
Nominal return
Inflation rate
Real return
Purchasing power change
```

Example output:

```text
Nominal return: 8.00%
Inflation: 3.00%
Exact real return: 4.85%
```

This helps users understand whether performance actually increased purchasing power.

---

### Data needed in Athena

To calculate real returns, Athena may need:

```text
Asset return
Portfolio return
Inflation rate
Inflation index
Country or region
Currency
Start date
End date
```

Example:

```text
asset: SPY
currency: USD
nominal_return: 8%
inflation_index: US CPI
inflation_rate: 3%
real_return: 4.85%
```

For Canadian portfolios, Athena may need Canadian inflation data.

For US portfolios, Athena may need US inflation data.

This matters because inflation is not the same in every country.

---

### Important limitation

Real return calculations depend on the inflation measure used.

Different inflation indices may produce different results.

Examples:

```text
Consumer Price Index
Core inflation
Personal consumption expenditure index
Country-specific inflation index
```

Also, an investor’s personal inflation rate may differ from official inflation.

Example:

```text
A student
A retiree
A homeowner
A renter
```

These people may experience different cost increases.

For Athena, the selected inflation source should be documented.

---

### CFA Level 1 takeaway

For CFA Level 1, nominal vs real return is a key concept.

Important ideas include:

```text
Nominal return
Real return
Inflation
Purchasing power
Approximate real return
Exact real return
Fisher relationship
```

The most important formulas are:

```text
Approximate real return ≈ nominal return - inflation
```

and:

```text
Real return = (1 + nominal return) / (1 + inflation) - 1
```

A simple memory rule:

```text
Nominal return tells how much money grew.
Real return tells how much purchasing power grew.
```

---

### Athena implementation takeaway

For Athena, nominal returns should be the default because they can be calculated directly from market prices.

Real returns require inflation data.

The performance module can later support:

```text
Nominal return calculation
Inflation data integration
Exact real return calculation
Purchasing power adjustment
Country-specific inflation selection
Real performance display
```

Example warning:

```text
Real return depends on the inflation index selected.
```

The goal is to help users distinguish between money growth and real wealth growth.

---

### Mini revision questions

1. What is a nominal return?

2. What is a real return?

3. Why can a positive nominal return still be bad?

4. What is the approximate real return formula?

5. What is the exact real return formula?

6. Why is purchasing power important?

7. If nominal return is 4% and inflation is 7%, is the real return positive or negative?

8. Why does Athena need inflation data to calculate real returns?

---

### Mini answers

1. A nominal return is the return before adjusting for inflation.

2. A real return is the return after adjusting for inflation.

3. A positive nominal return can still be bad if inflation is higher than the investment return.

4. The approximate formula is: real return ≈ nominal return - inflation.

5. The exact formula is: real return = (1 + nominal return) / (1 + inflation) - 1.

6. Purchasing power is important because it shows what money can actually buy.

7. The real return is negative because inflation is higher than the nominal return.

8. Athena needs inflation data because real return requires adjusting nominal performance for changes in price levels.

---

### Section summary

Nominal return measures investment performance before inflation.

Real return measures investment performance after inflation.

Inflation reduces purchasing power, so a positive nominal return does not always mean the investor became richer in real terms.

For CFA Level 1, this section is important because it introduces inflation adjustment, purchasing power and the Fisher relationship.

For Athena AI Risk Terminal, real returns can make performance analysis more meaningful, especially for long-term investing and high-inflation environments.

The key lesson is:

```text
Nominal return shows money growth.
Real return shows purchasing power growth.
```
---







## 14. Holding Period Return

Holding Period Return, or HPR, measures the total return earned over a specific investment period.

It answers a simple question:

```text
How much did the investor earn during the time the asset was held?
```

The holding period can be any length of time:

```text
One day
One month
One year
Three years
From purchase date to sale date
```

HPR includes both:

```text
Capital gain or loss
Income received during the holding period
```

This makes HPR more complete than a return based only on price change.

---

### Holding Period Return formula

The formula is:

```text
HPR = (Ending Value - Beginning Value + Income) / Beginning Value
```

Where:

```text
Beginning Value = value at the start of the holding period
Ending Value = value at the end of the holding period
Income = cash received during the holding period
```

Income can include:

```text
Dividends
Coupons
Distributions
Interest payments
```

Simple idea:

```text
HPR measures total gain relative to the initial investment.
```

---

### Basic example

Suppose an investor buys a stock.

```text
Beginning price = 100
Ending price    = 105
Dividend        = 2
```

Apply the formula:

```text
HPR = (105 - 100 + 2) / 100
HPR = 7 / 100
HPR = 7%
```

The investor earned:

```text
5 from price appreciation
2 from dividend income
```

Total gain:

```text
5 + 2 = 7
```

So the holding period return is:

```text
7%
```

---

### Capital gain component

The capital gain or loss is the change in the asset price.

Formula:

```text
Capital gain = Ending Value - Beginning Value
```

Example:

```text
Beginning price = 100
Ending price    = 105

Capital gain = 105 - 100
Capital gain = 5
```

The capital gain return is:

```text
5 / 100 = 5%
```

This only measures the price change.

It does not include income.

---

### Income component

The income component includes cash received while holding the asset.

Examples:

```text
Stock dividend
Bond coupon
ETF distribution
Interest income
```

Formula:

```text
Income return = Income / Beginning Value
```

Example:

```text
Income = 2
Beginning Value = 100

Income return = 2 / 100
Income return = 2%
```

In the full HPR example:

```text
Capital gain return = 5%
Income return       = 2%
HPR                 = 7%
```

---

### Positive HPR

A positive HPR means the investor made money during the holding period.

Example:

```text
Beginning value = 1,000
Ending value    = 1,100
Income          = 50
```

Calculation:

```text
HPR = (1,100 - 1,000 + 50) / 1,000
HPR = 150 / 1,000
HPR = 15%
```

The investor earned a positive total return.

---

### Negative HPR

A negative HPR means the investor lost money during the holding period.

Example:

```text
Beginning value = 1,000
Ending value    = 900
Income          = 20
```

Calculation:

```text
HPR = (900 - 1,000 + 20) / 1,000
HPR = -80 / 1,000
HPR = -8%
```

Even though the investor received income, the price loss was larger.

The total return is negative.

---

### Zero HPR

An HPR of zero means the investor broke even.

Example:

```text
Beginning value = 100
Ending value    = 95
Income          = 5
```

Calculation:

```text
HPR = (95 - 100 + 5) / 100
HPR = 0 / 100
HPR = 0%
```

The asset price fell, but the income exactly offset the loss.

---

### HPR for a stock

For a stock, HPR may include dividends.

Example:

```text
Purchase price = 50
Sale price     = 55
Dividend       = 1
```

Calculation:

```text
HPR = (55 - 50 + 1) / 50
HPR = 6 / 50
HPR = 12%
```

The investor earned:

```text
10% from price appreciation
2% from dividends
```

Total HPR:

```text
12%
```

---

### HPR for a bond

For a bond, HPR may include coupon payments.

Example:

```text
Beginning bond value = 1,000
Ending bond value    = 980
Coupon received      = 60
```

Calculation:

```text
HPR = (980 - 1,000 + 60) / 1,000
HPR = 40 / 1,000
HPR = 4%
```

Even though the bond price decreased, the coupon income created a positive total return.

This is why HPR is useful for fixed income.

---

### HPR for an ETF

For an ETF, HPR may include distributions.

Example:

```text
Beginning ETF price = 100
Ending ETF price    = 108
Distribution        = 2
```

Calculation:

```text
HPR = (108 - 100 + 2) / 100
HPR = 10 / 100
HPR = 10%
```

The ETF return includes both price appreciation and income distributed to the investor.

---

### HPR vs price return

Price return only looks at the price change.

HPR looks at price change plus income.

Simple comparison:

```text
Price return = price movement only
HPR = price movement + income
```

Example:

```text
Beginning price = 100
Ending price    = 105
Dividend        = 2
```

Price return:

```text
Price return = 105 / 100 - 1
Price return = 5%
```

Holding Period Return:

```text
HPR = (105 - 100 + 2) / 100
HPR = 7%
```

The HPR is higher because it includes the dividend.

---

### Why HPR matters

HPR matters because investment performance is not only about price changes.

Many investments generate income.

Examples:

```text
Stocks may pay dividends.
Bonds may pay coupons.
ETFs may pay distributions.
Cash may earn interest.
```

If income is ignored, the return may be understated.

This is especially important for:

```text
Dividend stocks
Bond portfolios
Income funds
Long-term investors
Total return analysis
```

Simple idea:

```text
HPR gives a more complete view of what the investor actually earned.
```

---

### Holding period length

The holding period is the time between the start and end of the investment.

Examples:

```text
Buy on January 1 and sell on January 31 = one-month holding period
Buy on January 1 and sell on December 31 = one-year holding period
Buy today and sell tomorrow = one-day holding period
```

The same HPR can mean different things depending on the length of the holding period.

Example:

```text
10% return in one month is very different from 10% return over five years.
```

This is why analysts often annualize returns when comparing investments over different horizons.

---

### HPR over multiple periods

If an investment has several holding period returns, the total return is compounded.

Example:

```text
Year 1 HPR = 10%
Year 2 HPR = -5%
```

The total two-year return is not:

```text
10% - 5% = 5%
```

Instead, it is:

```text
Total return = (1 + 0.10) × (1 - 0.05) - 1
Total return = 1.10 × 0.95 - 1
Total return = 1.045 - 1
Total return = 4.5%
```

The correct two-year return is:

```text
4.5%
```

This happens because returns compound over time.

---

### HPR and reinvested income

HPR includes income received during the period.

However, analysts must be clear about whether income is reinvested.

Example:

```text
Dividend received = 2
```

The investor could:

```text
Keep the dividend as cash
Reinvest the dividend into more shares
```

For short holding periods, the difference may be small.

For long horizons, reinvestment can significantly affect total performance.

This is why total return indices often assume dividends are reinvested.

---

### HPR before and after costs

Basic HPR usually ignores transaction costs and taxes unless they are explicitly included.

But in real life, investors may face:

```text
Commissions
Bid-ask spread costs
Management fees
Taxes
Foreign exchange costs
```

A gross HPR is calculated before these costs.

A net HPR is calculated after these costs.

Simple comparison:

```text
Gross HPR = return before costs
Net HPR = return after costs
```

Example:

```text
Gross HPR = 7%
Fees and costs = 1%

Net HPR = 6%
```

For Athena, the first version can focus on gross HPR, then later support fees and taxes.

---

### HPR and currency

For international investments, HPR depends on the currency used.

Example:

```text
A Canadian investor buys a US stock.
The stock return in USD is 8%.
```

The investor’s return in CAD may be different because of USD/CAD exchange rate movements.

Simple idea:

```text
Local-currency HPR = return in the asset’s currency
Base-currency HPR = return converted into the investor’s reporting currency
```

This distinction matters for multi-currency portfolios.

For Athena, the currency used in the HPR calculation should be explicit.

---

### HPR and inflation

HPR is usually calculated as a nominal return.

This means it does not automatically adjust for inflation.

Example:

```text
Nominal HPR = 8%
Inflation   = 3%
```

Approximate real HPR:

```text
Real HPR ≈ 8% - 3%
Real HPR ≈ 5%
```

For long-term performance analysis, Athena can later show both:

```text
Nominal HPR
Real HPR
```

This gives a better view of purchasing power.

---

### HPR data needed in Athena

To calculate HPR, Athena needs:

```text
Beginning value
Ending value
Income received
Holding period start date
Holding period end date
Currency
Asset identifier
```

For a stock, this may mean:

```text
purchase_price
sale_price
dividends_received
start_date
end_date
currency
```

For a bond, this may mean:

```text
beginning_bond_value
ending_bond_value
coupon_income
start_date
end_date
currency
```

For a portfolio, this may mean:

```text
beginning_portfolio_value
ending_portfolio_value
cash_flows
income_received
start_date
end_date
base_currency
```

---

### HPR in Athena

Athena can use HPR to show total performance over a selected period.

Possible use cases:

```text
Calculate the total return of a stock position
Calculate the return of an ETF including distributions
Calculate the return of a bond including coupons
Compare asset HPR against benchmark HPR
Display portfolio performance over a chosen time range
```

Example output:

```text
Asset: AAPL
Beginning value: 10,000
Ending value: 10,800
Income received: 120
Holding period return: 9.20%
Currency: USD
```

Calculation:

```text
HPR = (10,800 - 10,000 + 120) / 10,000
HPR = 920 / 10,000
HPR = 9.20%
```

---

### Common beginner mistakes

Common mistakes include:

```text
Ignoring dividends or coupons
Confusing price return with total return
Forgetting the holding period length
Adding multi-period returns instead of compounding them
Mixing currencies
Ignoring fees and transaction costs
Comparing returns over different horizons without annualization
```

Example mistake:

```text
Year 1 return = 20%
Year 2 return = -20%
```

A beginner may think the total return is:

```text
0%
```

But the compounded return is:

```text
1.20 × 0.80 - 1 = -4%
```

The investor ends below the starting value.

---

### CFA Level 1 takeaway

For CFA Level 1, Holding Period Return is a fundamental performance measure.

Important concepts include:

```text
Beginning value
Ending value
Income
Capital gain or loss
Total return
Holding period
Compounding
Gross return
Net return
```

The most important formula is:

```text
HPR = (Ending Value - Beginning Value + Income) / Beginning Value
```

A simple memory rule:

```text
HPR measures what the investor earned during the holding period,
including both price change and income.
```

---

### Athena implementation takeaway

For Athena, HPR should be used as a basic total return measure.

The performance module should support:

```text
HPR calculation for assets
HPR calculation for portfolios
Income inclusion
Currency identification
Start and end date selection
Benchmark comparison
Gross vs net return extension later
```

Athena should clearly show whether HPR includes:

```text
Dividends
Coupons
Distributions
Fees
Taxes
Currency conversion
```

The goal is to make performance transparent and not confuse price return with total return.

---

### Mini revision questions

1. What does Holding Period Return measure?

2. What are the three main inputs in the HPR formula?

3. Why is HPR more complete than price return?

4. What types of income can be included in HPR?

5. Why does the length of the holding period matter?

6. How are multiple holding period returns combined?

7. Why can HPR differ between local currency and base currency?

8. What is the difference between gross HPR and net HPR?

---

### Mini answers

1. HPR measures the total return earned over a specific holding period.

2. The main inputs are beginning value, ending value and income.

3. HPR is more complete because it includes both price change and income.

4. Income can include dividends, coupons, distributions and interest payments.

5. The length matters because the same return can be more or less impressive depending on the time horizon.

6. Multiple HPRs are combined by compounding them, not by simply adding them.

7. HPR can differ because exchange rate movements affect returns when converted into the investor’s base currency.

8. Gross HPR is before costs, while net HPR is after costs such as fees, taxes or transaction costs.

---

### Section summary

Holding Period Return measures the total return earned during a specific investment period.

It includes both capital gain or loss and income received.

For CFA Level 1, HPR is important because it is one of the most basic and practical return measures.

For Athena AI Risk Terminal, HPR is useful because it helps users understand the total performance of an asset or portfolio over a selected time range.

The key lesson is:

```text
HPR measures the full return earned during the holding period,
not just the price change.
```
---












## 15. Simple returns

A simple return measures the percentage change in the value of an asset between two points in time.

It answers the question:

```text
How much did the asset increase or decrease relative to its starting value?
```

Simple returns are one of the most common return measures in finance because they are easy to understand and easy to communicate.

Formula:

```text
Return_t = (Price_t - Price_{t-1}) / Price_{t-1}
```

Equivalent formula:

```text
Return_t = Price_t / Price_{t-1} - 1
```

Where:

```text
Price_t = price at the end of the period
Price_{t-1} = price at the beginning of the period
```

Simple idea:

```text
Simple return = percentage change in price
```

---

### Positive simple return

A positive simple return means the asset price increased.

Example:

```text
Initial price = 100
Final price   = 105
```

Calculation:

```text
Return = 105 / 100 - 1
Return = 1.05 - 1
Return = 0.05
Return = 5%
```

The asset gained 5% during the period.

---

### Negative simple return

A negative simple return means the asset price decreased.

Example:

```text
Initial price = 100
Final price   = 92
```

Calculation:

```text
Return = 92 / 100 - 1
Return = 0.92 - 1
Return = -0.08
Return = -8%
```

The asset lost 8% during the period.

---

### Zero simple return

A zero simple return means the asset price did not change.

Example:

```text
Initial price = 100
Final price   = 100
```

Calculation:

```text
Return = 100 / 100 - 1
Return = 1 - 1
Return = 0%
```

The asset produced no price return during the period.

---

### Why simple returns are useful

Simple returns are useful because they are intuitive.

Most investors naturally think in percentage terms.

Example:

```text
The stock gained 5%.
The ETF lost 2%.
The portfolio returned 8% this year.
```

Simple returns are commonly used for:

```text
Performance reporting
Portfolio dashboards
Benchmark comparison
Client communication
Basic return analysis
Historical performance charts
```

They are especially useful when explaining investment performance to users who are not quantitative specialists.

---

### Simple return vs price change

A price change is measured in currency units.

A simple return is measured in percentage terms.

Example:

```text
Stock A moves from 100 to 110.
Stock B moves from 20 to 22.
```

Price changes:

```text
Stock A price change = 10
Stock B price change = 2
```

Simple returns:

```text
Stock A return = 110 / 100 - 1 = 10%
Stock B return = 22 / 20 - 1 = 10%
```

Even though Stock A increased by more dollars, both stocks produced the same percentage return.

Simple returns make assets easier to compare.

---

### Simple return with income

The basic simple return formula uses only prices.

However, if the asset pays income, the return should include that income.

Example:

```text
Initial price = 100
Final price   = 104
Dividend      = 2
```

Total simple return:

```text
Return = (104 - 100 + 2) / 100
Return = 6 / 100
Return = 6%
```

If the dividend is ignored, the return would be:

```text
Price return = 104 / 100 - 1
Price return = 4%
```

This is why analysts must distinguish between:

```text
Price return
Total return
```

For stocks and ETFs, adjusted close is often used to reflect dividends and splits more accurately.

---

### One-period simple return

A one-period simple return measures the return over one specific period.

Examples:

```text
One-day return
One-month return
One-year return
Holding-period return
```

Example:

```text
Monday close = 100
Tuesday close = 103
```

One-day return:

```text
Return = 103 / 100 - 1
Return = 3%
```

This is the basic building block for many market finance calculations.

---

### Multi-period simple returns

Simple returns over multiple periods must be compounded.

They should not simply be added.

Example:

```text
Day 1 return = +10%
Day 2 return = -10%
```

A beginner may think:

```text
Total return = 10% - 10% = 0%
```

But this is wrong.

Correct calculation:

```text
Initial value = 100

After Day 1:
100 × 1.10 = 110

After Day 2:
110 × 0.90 = 99
```

Final value:

```text
99
```

Total return:

```text
99 / 100 - 1 = -1%
```

So:

```text
+10% followed by -10% = -1%, not 0%
```

This is one of the most important beginner lessons in return calculation.

---

### Compounding simple returns

To combine simple returns over time, use:

```text
Total return = (1 + R1)(1 + R2)...(1 + Rn) - 1
```

Example:

```text
Month 1 return = 5%
Month 2 return = 3%
Month 3 return = -2%
```

Calculation:

```text
Total return = (1.05)(1.03)(0.98) - 1
Total return = 1.05987 - 1
Total return = 5.987%
```

The total return is approximately:

```text
5.99%
```

Not:

```text
5% + 3% - 2% = 6%
```

The difference may be small for small returns, but it becomes important over longer periods or with high volatility.

---

### Simple returns and volatility

Simple returns are often used to calculate volatility.

The process is:

```text
Price series
    ↓
Simple return series
    ↓
Standard deviation of returns
    ↓
Volatility
```

Example:

```text
Prices:
100, 102, 101, 105
```

Returns:

```text
102 / 100 - 1 = 2.00%
101 / 102 - 1 = -0.98%
105 / 101 - 1 = 3.96%
```

These returns can then be used to estimate how unstable the asset is.

For Athena, this is one of the most important workflows.

---

### Simple returns and portfolio returns

Simple returns are also useful for portfolio analysis.

If a portfolio contains multiple assets, the portfolio return can be calculated as a weighted average of asset returns for the same period.

Formula:

```text
Portfolio return = w1R1 + w2R2 + ... + wnRn
```

Where:

```text
w = portfolio weight
R = asset return
```

Example:

```text
Asset A weight = 60%
Asset A return = 5%

Asset B weight = 40%
Asset B return = 2%
```

Portfolio return:

```text
Portfolio return = (0.60 × 5%) + (0.40 × 2%)
Portfolio return = 3.0% + 0.8%
Portfolio return = 3.8%
```

This is why simple returns are practical for portfolio dashboards.

---

### Advantages of simple returns

Simple returns have several advantages:

```text
Easy to understand
Easy to calculate
Easy to explain
Useful for dashboards
Useful for performance reporting
Useful for portfolio return calculation
Directly linked to percentage gain or loss
```

Example:

```text
A return of 10% means the investment increased by 10% of its starting value.
```

This interpretation is straightforward.

---

### Limitations of simple returns

Simple returns also have limitations.

Important limitations include:

```text
They do not add cleanly over time.
They can be less convenient for some mathematical models.
They require compounding across multiple periods.
They can be affected by corporate actions if raw prices are used.
They can be misleading if income is ignored.
```

The biggest limitation is:

```text
Simple returns are not additive over time.
```

Example:

```text
+20% followed by -20% does not equal 0%.
```

Calculation:

```text
Initial value = 100
After +20% = 120
After -20% = 96
```

Total return:

```text
96 / 100 - 1 = -4%
```

---

### Simple returns vs log returns

Simple returns and log returns are both used in finance.

Simple returns are easier to interpret.

Log returns are more convenient for some mathematical models because they are additive over time.

Simple comparison:

```text
Simple return = better for reporting and interpretation
Log return = useful for modeling and time aggregation
```

For Athena, simple returns should be the default for user-facing dashboards.

Log returns can be used later for modeling, risk analysis and quantitative research.

---

### Data quality issues

Simple returns are sensitive to data problems.

Possible issues include:

```text
Missing prices
Zero prices
Negative prices
Duplicate dates
Wrong currency
Unadjusted prices
Corporate actions
Stale prices
```

Example:

```text
Price yesterday = 100
Price today = 0
```

Simple return:

```text
0 / 100 - 1 = -100%
```

This may be a real event, but it is often a data error.

Another problem:

```text
Price yesterday = 0
Price today = 100
```

The return is undefined because division by zero is impossible.

Athena should validate price data before calculating simple returns.

---

### Simple returns in Athena

Athena can use simple returns as a core calculation.

Possible use cases:

```text
Daily asset returns
Monthly asset returns
Portfolio returns
Benchmark returns
Cumulative performance
Volatility calculation
Correlation calculation
Drawdown analysis
Risk metrics
```

Example output:

```text
symbol: AAPL
date: 2026-04-29
price_t_minus_1: 100
price_t: 105
simple_return: 5.00%
price_field_used: adjusted_close
```

The system should clearly document which price field was used.

Example:

```text
Return calculated using adjusted close.
```

This avoids confusion between raw price returns and adjusted returns.

---

### CFA Level 1 takeaway

For CFA Level 1, simple returns are fundamental.

Important concepts include:

```text
Beginning price
Ending price
Percentage change
Positive return
Negative return
Compounding
Price return
Total return
Portfolio return
```

The key formula is:

```text
Return_t = Price_t / Price_{t-1} - 1
```

A simple memory rule:

```text
Simple return measures how much value changed relative to the starting value.
```

---

### Athena implementation takeaway

For Athena, simple returns should be one of the first market analytics implemented.

The return module should support:

```text
Simple return calculation
Adjusted close selection
Daily return series
Monthly return series
Portfolio return calculation
Benchmark return calculation
Data validation before calculation
Warning when returns look abnormal
```

The goal is to create a reliable return series that can be reused by volatility, correlation and risk modules.

---

### Mini revision questions

1. What does a simple return measure?

2. What is the simple return formula?

3. If a price moves from 100 to 105, what is the simple return?

4. If a price moves from 100 to 92, what is the simple return?

5. Why are simple returns useful?

6. Why can simple returns not simply be added over time?

7. How should multiple simple returns be combined?

8. Why should Athena validate prices before calculating returns?

---

### Mini answers

1. A simple return measures the percentage change in value between two points in time.

2. The formula is: Return_t = Price_t / Price_{t-1} - 1.

3. The simple return is 5%.

4. The simple return is -8%.

5. Simple returns are useful because they are intuitive, easy to explain and practical for reporting.

6. They cannot simply be added because returns compound over time.

7. Multiple simple returns should be combined by multiplying the growth factors: (1 + R1)(1 + R2)...(1 + Rn) - 1.

8. Athena should validate prices because missing, zero, negative or unadjusted prices can create incorrect returns.

---

### Section summary

A simple return measures the percentage change in an asset’s value between two points in time.

It is easy to understand and widely used in performance reporting, dashboards and portfolio analysis.

For CFA Level 1, simple returns are essential because they are one of the first building blocks of investment performance measurement.

For Athena AI Risk Terminal, simple returns are essential because they feed volatility, correlation, drawdown and risk calculations.

The key lesson is:

```text
Simple returns are easy to interpret,
but they must be compounded over time and calculated from clean price data.
```
---
























## 16. Log returns

Log returns use the natural logarithm to measure the return between two prices.

They are also called continuously compounded returns.

Formula:

```text
LogReturn_t = ln(Price_t / Price_{t-1})
```

Where:

```text
ln = natural logarithm
Price_t = price at the end of the period
Price_{t-1} = price at the beginning of the period
```

Simple idea:

```text
Log return measures the continuously compounded rate of return between two prices.
```

Log returns are especially useful in quantitative finance, risk modeling and time-series analysis.

---

### Basic example

Suppose an asset moves from 100 to 105.

```text
Initial price = 100
Final price   = 105
```

Calculation:

```text
LogReturn = ln(105 / 100)
LogReturn = ln(1.05)
LogReturn ≈ 0.0488
LogReturn ≈ 4.88%
```

The simple return is:

```text
Simple return = 105 / 100 - 1
Simple return = 5%
```

So for this example:

```text
Simple return = 5.00%
Log return    = 4.88%
```

The values are close, but not exactly the same.

---

### Why log returns are different

Simple returns measure direct percentage change.

Log returns measure continuously compounded growth.

Simple comparison:

```text
Simple return:
How much did the price change in percentage terms?

Log return:
What continuous growth rate connects the starting price to the ending price?
```

For small returns, simple returns and log returns are very close.

Example:

```text
Simple return = 1.00%
Log return    ≈ 0.995%
```

For larger returns, the difference becomes more visible.

---

### Positive log return

A positive log return means the price increased.

Example:

```text
Initial price = 100
Final price   = 110
```

Calculation:

```text
LogReturn = ln(110 / 100)
LogReturn = ln(1.10)
LogReturn ≈ 0.0953
LogReturn ≈ 9.53%
```

The asset increased in value.

---

### Negative log return

A negative log return means the price decreased.

Example:

```text
Initial price = 100
Final price   = 90
```

Calculation:

```text
LogReturn = ln(90 / 100)
LogReturn = ln(0.90)
LogReturn ≈ -0.1053
LogReturn ≈ -10.53%
```

The asset decreased in value.

Notice that a -10% simple return corresponds to a log return of about -10.53%.

---

### Zero log return

A zero log return means the price did not change.

Example:

```text
Initial price = 100
Final price   = 100
```

Calculation:

```text
LogReturn = ln(100 / 100)
LogReturn = ln(1)
LogReturn = 0
```

So the log return is:

```text
0%
```

---

### Why log returns are useful

Log returns are useful because they are additive over time.

This is the main advantage.

Example:

```text
Day 1 log return = 1%
Day 2 log return = 2%
```

The two-day log return is:

```text
1% + 2% = 3%
```

This additive property makes log returns convenient for mathematical modeling.

---

### Additivity example

Suppose a price moves like this:

```text
Day 0 price = 100
Day 1 price = 105
Day 2 price = 110
```

Day 1 log return:

```text
ln(105 / 100) = ln(1.05)
```

Day 2 log return:

```text
ln(110 / 105)
```

Total two-day log return:

```text
ln(105 / 100) + ln(110 / 105)
```

Using logarithm rules:

```text
ln(105 / 100) + ln(110 / 105)
= ln((105 / 100) × (110 / 105))
= ln(110 / 100)
```

So:

```text
Sum of daily log returns = total log return
```

This is why log returns are mathematically convenient.

---

### Simple returns are not additive

Simple returns do not add cleanly over time.

Example:

```text
Day 1 simple return = +10%
Day 2 simple return = -10%
```

A beginner may think the total return is:

```text
0%
```

But the actual result is:

```text
Initial value = 100
After +10% = 110
After -10% = 99
```

Total simple return:

```text
99 / 100 - 1 = -1%
```

Simple returns must be compounded.

Log returns can be added.

This is the key difference.

---

### Converting simple return to log return

If you already know the simple return, you can convert it to a log return.

Formula:

```text
Log return = ln(1 + simple return)
```

Example:

```text
Simple return = 5%
Simple return = 0.05
```

Calculation:

```text
Log return = ln(1 + 0.05)
Log return = ln(1.05)
Log return ≈ 4.88%
```

---

### Converting log return to simple return

If you know the log return, you can convert it back to a simple return.

Formula:

```text
Simple return = e^(log return) - 1
```

Example:

```text
Log return = 0.0488
```

Calculation:

```text
Simple return = e^0.0488 - 1
Simple return ≈ 0.05
Simple return ≈ 5%
```

This is useful because log returns are often used in models, while simple returns are easier to explain to users.

---

### Log returns and continuous compounding

Log returns are linked to continuous compounding.

Continuous compounding means the investment grows continuously over time instead of at discrete intervals.

Simple idea:

```text
Simple return = discrete growth
Log return = continuous growth
```

Example:

```text
Simple return = 5%
Log return ≈ 4.88%
```

A continuously compounded return of about 4.88% produces the same final value as a simple return of 5%.

---

### Log returns and modeling

Log returns are often used in quantitative finance because they have useful mathematical properties.

They are common in:

```text
Risk modeling
Volatility modeling
Time-series analysis
Option pricing
Monte Carlo simulation
Portfolio analytics
Academic finance research
```

For example, many models assume that log returns are approximately normally distributed over short time periods.

This assumption is not perfect, but it is common in financial modeling.

---

### Log returns and volatility

Volatility can be calculated using either simple returns or log returns.

A common quantitative workflow is:

```text
Price series
    ↓
Log return series
    ↓
Standard deviation of log returns
    ↓
Volatility estimate
```

Example:

```text
Prices:
100, 102, 101, 105
```

Log returns:

```text
ln(102 / 100)
ln(101 / 102)
ln(105 / 101)
```

These log returns can then be used to estimate volatility.

For short daily returns, volatility calculated from simple returns and log returns is often similar.

---

### Log returns and large price moves

For small returns, simple and log returns are close.

For large returns, they differ more.

Example:

```text
Initial price = 100
Final price   = 200
```

Simple return:

```text
200 / 100 - 1 = 100%
```

Log return:

```text
ln(200 / 100) = ln(2)
Log return ≈ 69.31%
```

The difference is large.

This is why users should know which return type is being displayed.

---

### Symmetry advantage

Log returns have a useful symmetry property.

Example:

```text
Price rises from 100 to 200.
Log return = ln(200 / 100) = ln(2) ≈ 69.31%
```

Then the price falls from 200 back to 100.

```text
Log return = ln(100 / 200) = ln(0.5) ≈ -69.31%
```

The log returns are symmetric:

```text
+69.31%
-69.31%
```

The total log return is:

```text
0%
```

This makes log returns elegant for mathematical analysis.

Simple returns do not have this symmetry:

```text
100 to 200 = +100%
200 to 100 = -50%
```

---

### Practical interpretation

Log returns are powerful, but they are less intuitive than simple returns.

Most users understand:

```text
The stock returned 5%.
```

More easily than:

```text
The continuously compounded log return was 4.88%.
```

For this reason, simple returns are often better for dashboards and communication.

Log returns are often better for quantitative calculations.

Practical rule:

```text
Use simple returns for user-facing interpretation.
Use log returns for modeling when their mathematical properties are useful.
```

---

### Data quality issues

Log returns require valid positive prices.

The logarithm is not defined for zero or negative prices.

Problem example:

```text
Price_t = 0
```

Then:

```text
ln(0 / Price_{t-1})
```

is not valid.

Another problem:

```text
Price_t = -10
```

A negative price is not valid for a normal stock or ETF price.

Athena must validate prices before calculating log returns.

Required checks:

```text
Price must be positive
Previous price must be positive
Dates must be ordered correctly
Duplicate dates must be removed or handled
Missing prices must be handled
Corporate actions must be considered
```

---

### Log returns in Athena

Athena can support log returns as an analytical return type.

Possible use cases:

```text
Quantitative modeling
Volatility estimation
Risk analysis
Return distribution analysis
Monte Carlo simulation
Option pricing extensions
Research notebooks
```

Example output:

```text
symbol: AAPL
date: 2026-04-29
price_t_minus_1: 100
price_t: 105
simple_return: 5.00%
log_return: 4.88%
price_field_used: adjusted_close
```

Athena should always display the return type clearly.

Example:

```text
Return type: simple return
```

or:

```text
Return type: log return
```

This avoids confusion between dashboard returns and modeling returns.

---

### Simple returns vs log returns in Athena

A good practical approach is:

```text
Default dashboard return = simple return
Quantitative modeling return = log return
```

Example:

```text
Portfolio performance page:
Show simple returns.

Risk modeling engine:
May use log returns.
```

This keeps the platform understandable for users while still supporting more advanced quantitative analysis.

---

### CFA Level 1 takeaway

For CFA Level 1, log returns are less common than simple holding period returns, but the concept is useful for understanding compounding and return measurement.

Important ideas include:

```text
Natural logarithm
Continuously compounded return
Additivity over time
Conversion between simple and log returns
Difference between interpretation and modeling
```

Important formulas:

```text
Log return = ln(Price_t / Price_{t-1})
```

```text
Log return = ln(1 + simple return)
```

```text
Simple return = e^(log return) - 1
```

A simple memory rule:

```text
Simple returns are easier to explain.
Log returns are easier to add over time.
```

---

### Athena implementation takeaway

For Athena, log returns should be supported but not confused with simple returns.

The return module should support:

```text
Log return calculation
Simple return calculation
Conversion between return types
Positive price validation
Adjusted close selection
Return type labeling
Documentation of formulas
```

The goal is to make Athena useful for both:

```text
User-friendly financial dashboards
Quantitative risk modeling
```

---

### Mini revision questions

1. What is a log return?

2. What is the log return formula?

3. Why are log returns useful over multiple periods?

4. Are log returns easier to explain than simple returns?

5. How do you convert a simple return into a log return?

6. How do you convert a log return into a simple return?

7. Why must prices be positive before calculating log returns?

8. In Athena, where are log returns most useful?

---

### Mini answers

1. A log return is a return calculated using the natural logarithm of the price ratio.

2. The formula is: LogReturn_t = ln(Price_t / Price_{t-1}).

3. Log returns are useful because they are additive over time.

4. No. Simple returns are usually easier to explain to users.

5. Use: log return = ln(1 + simple return).

6. Use: simple return = e^(log return) - 1.

7. Prices must be positive because the logarithm of zero or a negative number is not valid.

8. Log returns are most useful in Athena for modeling, volatility estimation, risk analysis and quantitative research.

---

### Section summary

Log returns measure continuously compounded returns using the natural logarithm.

They are especially useful because they are additive over time.

For CFA Level 1, log returns help reinforce the difference between simple return, compounding and continuous growth.

For Athena AI Risk Terminal, log returns are useful for quantitative modeling, volatility analysis and risk calculations.

The key lesson is:

```text
Simple returns are easier to interpret.
Log returns are easier to model.
```

---












## 17. Arithmetic vs geometric returns

Returns can be averaged in different ways.

The two most important methods are:

```text
Arithmetic mean return
Geometric mean return
```

They are both averages, but they answer different questions.

Simple idea:

```text
Arithmetic mean = average periodic return
Geometric mean = average compounded return
```

This distinction is very important in finance because investment returns compound over time.

---

### Why this matters

When analyzing investment performance, it is not enough to calculate a simple average.

Example:

```text
Year 1 return = +50%
Year 2 return = -50%
```

A beginner may think the average return is:

```text
0%
```

But the investment did not break even.

Calculation:

```text
Initial value = 100

After Year 1:
100 × 1.50 = 150

After Year 2:
150 × 0.50 = 75
```

Final value:

```text
75
```

Total return:

```text
75 / 100 - 1 = -25%
```

Even though the arithmetic average is 0%, the investor lost 25% over the full period.

This is why the difference between arithmetic and geometric returns matters.

---

### Arithmetic mean return

The arithmetic mean return is the simple average of periodic returns.

Formula:

```text
Arithmetic mean = (R1 + R2 + ... + Rn) / n
```

Where:

```text
R1, R2, ..., Rn = periodic returns
n = number of periods
```

Example:

```text
Year 1 return = +10%
Year 2 return = -5%
```

Calculation:

```text
Arithmetic mean = (10% - 5%) / 2
Arithmetic mean = 5% / 2
Arithmetic mean = 2.5%
```

The arithmetic mean tells us the average return per period.

---

### Geometric mean return

The geometric mean return measures the average compounded return over multiple periods.

Formula:

```text
Geometric mean = [(1 + R1)(1 + R2)...(1 + Rn)]^(1/n) - 1
```

Where:

```text
R1, R2, ..., Rn = periodic returns
n = number of periods
```

Example:

```text
Year 1 return = +10%
Year 2 return = -5%
```

Calculation:

```text
Geometric mean = [(1.10)(0.95)]^(1/2) - 1
Geometric mean = [1.045]^(1/2) - 1
Geometric mean ≈ 0.0223
Geometric mean ≈ 2.23%
```

The geometric mean tells us the constant return that would produce the same ending value over the full period.

---

### Arithmetic mean vs geometric mean

The key difference is:

```text
Arithmetic mean = average of returns
Geometric mean = compounded average growth rate
```

Example:

```text
Year 1 return = +10%
Year 2 return = -5%
```

Arithmetic mean:

```text
2.50%
```

Geometric mean:

```text
2.23%
```

The geometric mean is lower because it accounts for compounding.

---

### Why geometric mean is usually lower

When returns are volatile, the geometric mean is usually lower than the arithmetic mean.

This happens because losses hurt compounding.

Example:

```text
Year 1 return = +50%
Year 2 return = -50%
```

Arithmetic mean:

```text
(+50% - 50%) / 2 = 0%
```

Geometric mean:

```text
[(1.50)(0.50)]^(1/2) - 1
= [0.75]^(1/2) - 1
≈ -13.40%
```

The investor loses money over time, even though the arithmetic average is zero.

This effect is often called volatility drag.

---

### Volatility drag

Volatility drag means that volatility reduces compounded growth.

The more returns fluctuate, the larger the gap between arithmetic and geometric returns tends to be.

Example:

```text
Asset A:
Year 1 = +5%
Year 2 = +5%

Asset B:
Year 1 = +20%
Year 2 = -10%
```

Arithmetic means:

```text
Asset A arithmetic mean = 5%
Asset B arithmetic mean = 5%
```

But the compounded results are different.

Asset A:

```text
100 × 1.05 × 1.05 = 110.25
```

Asset B:

```text
100 × 1.20 × 0.90 = 108.00
```

Both have the same arithmetic mean, but Asset A ends with more wealth because its returns are more stable.

Simple idea:

```text
Higher volatility can reduce long-term compound growth.
```

---

### When to use arithmetic mean

The arithmetic mean is useful when estimating the expected return for a single future period.

Example:

```text
What is the expected return next year?
```

If returns are independent and the goal is to estimate a one-period expected return, the arithmetic mean may be more appropriate.

Common uses:

```text
Expected one-period return
Forecasting next-period return
Portfolio theory inputs
Scenario analysis
Mean return assumption
```

Simple idea:

```text
Use arithmetic mean for average one-period return.
```

---

### When to use geometric mean

The geometric mean is useful when measuring historical compounded performance over multiple periods.

Example:

```text
What annual return did the investment actually earn over five years?
```

Common uses:

```text
Historical performance
Long-term realized return
Compound annual growth rate
Multi-period investment growth
Performance reporting over time
```

Simple idea:

```text
Use geometric mean for realized long-term compound return.
```

---

### Geometric mean and CAGR

The geometric mean is closely related to CAGR.

CAGR means:

```text
Compound Annual Growth Rate
```

CAGR measures the annualized growth rate of an investment over multiple years.

Formula:

```text
CAGR = (Ending Value / Beginning Value)^(1 / number of years) - 1
```

Example:

```text
Beginning value = 100
Ending value    = 121
Number of years = 2
```

Calculation:

```text
CAGR = (121 / 100)^(1/2) - 1
CAGR = 1.21^(1/2) - 1
CAGR = 10%
```

This means the investment grew as if it earned 10% per year compounded annually.

---

### Example with three years

Suppose an investment has the following annual returns:

```text
Year 1 = +20%
Year 2 = -10%
Year 3 = +15%
```

Arithmetic mean:

```text
Arithmetic mean = (20% - 10% + 15%) / 3
Arithmetic mean = 25% / 3
Arithmetic mean = 8.33%
```

Geometric mean:

```text
Geometric mean = [(1.20)(0.90)(1.15)]^(1/3) - 1
Geometric mean = [1.242]^(1/3) - 1
Geometric mean ≈ 7.49%
```

The geometric mean is lower because the returns compound over time.

---

### Ending value interpretation

The geometric mean can be checked by applying it to the beginning value.

Example:

```text
Beginning value = 100
Geometric mean = 7.49%
Number of years = 3
```

Calculation:

```text
100 × (1.0749)^3 ≈ 124.20
```

This matches the actual compounded value:

```text
100 × 1.20 × 0.90 × 1.15 = 124.20
```

This is why the geometric mean is the correct average for realized multi-period growth.

---

### Arithmetic mean can be misleading

The arithmetic mean can be misleading when used to describe long-term investment growth.

Example:

```text
Year 1 return = +100%
Year 2 return = -50%
```

Arithmetic mean:

```text
(100% - 50%) / 2 = 25%
```

This looks positive.

But the actual investment result is:

```text
Initial value = 100
After Year 1 = 200
After Year 2 = 100
```

Final value:

```text
100
```

Total return:

```text
0%
```

Geometric mean:

```text
[(2.00)(0.50)]^(1/2) - 1
= 1^(1/2) - 1
= 0%
```

The geometric mean correctly shows that the investor did not grow wealth over the full period.

---

### Important relationship

When returns are not volatile, arithmetic and geometric means are close.

When returns are volatile, the gap becomes larger.

Simple relationship:

```text
More volatility → larger gap between arithmetic and geometric mean
```

Approximate intuition:

```text
Geometric mean is reduced by volatility.
```

This is why two investments with the same arithmetic average can produce different long-term results.

The more stable investment may compound better.

---

### Arithmetic mean and expected return

In finance, the arithmetic mean is often used as an estimate of expected return.

Example:

```text
Historical annual returns:
6%, 8%, 10%
```

Arithmetic mean:

```text
(6% + 8% + 10%) / 3 = 8%
```

An analyst may use 8% as a simple estimate of next year’s expected return.

However, this is only an estimate. Future returns may be different from historical returns.

---

### Geometric mean and realized performance

The geometric mean is better for describing what actually happened to invested wealth.

Example:

```text
Beginning portfolio value = 10,000
Ending portfolio value = 14,000
Time = 5 years
```

Geometric annual return:

```text
(14,000 / 10,000)^(1/5) - 1
```

This shows the annual compounded return earned over the period.

For performance reporting, this is usually more meaningful than the arithmetic average.

---

### Arithmetic vs geometric in portfolio analysis

Portfolio managers should understand both measures.

Example:

```text
Arithmetic mean return = useful for expected one-year return.
Geometric mean return = useful for long-term realized performance.
```

A portfolio with high volatility may have a strong arithmetic average but a weaker geometric average.

This means the portfolio may look attractive in average-return terms, but less attractive in compounded wealth terms.

---

### Common beginner mistake

A common beginner mistake is to average returns and assume that average represents actual long-term growth.

Example:

```text
Return year 1 = +30%
Return year 2 = -20%
```

Arithmetic mean:

```text
5%
```

But actual compounded result:

```text
100 × 1.30 × 0.80 = 104
```

Total two-year return:

```text
4%
```

Annual compounded return:

```text
(1.04)^(1/2) - 1 ≈ 1.98%
```

The arithmetic mean is 5%, but the realized compound annual return is only about 1.98%.

---

### Data needed in Athena

To calculate arithmetic and geometric returns, Athena needs:

```text
Return series
Number of periods
Start date
End date
Return frequency
Price field used
Currency
```

Example return series:

```text
Year 1 = 10%
Year 2 = -5%
Year 3 = 8%
```

Athena can calculate:

```text
Arithmetic mean return
Geometric mean return
Gap between both measures
Compounded ending value
```

---

### Arithmetic vs geometric in Athena

Athena can use both measures for different purposes.

Possible use cases for arithmetic mean:

```text
Average daily return
Average monthly return
Expected one-period return estimate
Portfolio input assumption
```

Possible use cases for geometric mean:

```text
Historical annualized return
Compound annual growth rate
Long-term performance reporting
Backtest performance
Portfolio growth analysis
```

Example output:

```text
Asset: SPY
Period: 5 years
Arithmetic mean annual return: 9.20%
Geometric mean annual return: 8.40%
Difference: 0.80%
```

Athena can explain:

```text
The geometric mean is lower because it reflects compounding and volatility.
```

---

### CFA Level 1 takeaway

For CFA Level 1, the distinction between arithmetic and geometric mean returns is very important.

Important concepts include:

```text
Arithmetic mean
Geometric mean
Compounding
Volatility drag
Expected one-period return
Realized multi-period return
Compound annual growth rate
```

The most important formulas are:

```text
Arithmetic mean = (R1 + R2 + ... + Rn) / n
```

```text
Geometric mean = [(1 + R1)(1 + R2)...(1 + Rn)]^(1/n) - 1
```

A simple memory rule:

```text
Arithmetic mean is for average period return.
Geometric mean is for compounded wealth growth.
```

---

### Athena implementation takeaway

For Athena, both averages should be supported and clearly labeled.

The return analytics module should support:

```text
Arithmetic mean return
Geometric mean return
CAGR calculation
Return frequency selection
Compounded growth calculation
Comparison between arithmetic and geometric returns
Warning when volatility creates a large gap
```

The goal is to avoid misleading users by showing only a simple average return.

Athena should help users understand the difference between average performance and compounded performance.

---

### Mini revision questions

1. What is the arithmetic mean return?

2. What is the geometric mean return?

3. Which mean is usually better for long-term realized performance?

4. Which mean is often used for expected one-period return?

5. Why is the geometric mean usually lower than the arithmetic mean?

6. What is volatility drag?

7. Why is +50% followed by -50% not equal to 0% total return?

8. How can Athena use both arithmetic and geometric returns?

---

### Mini answers

1. The arithmetic mean return is the simple average of periodic returns.

2. The geometric mean return is the compounded average return over multiple periods.

3. The geometric mean is usually better for long-term realized performance.

4. The arithmetic mean is often used for expected one-period return.

5. The geometric mean is usually lower because it accounts for compounding and the effect of volatility.

6. Volatility drag is the reduction in compounded growth caused by fluctuating returns.

7. Because returns compound. Starting with 100, +50% gives 150, then -50% gives 75, so the total return is -25%.

8. Athena can use arithmetic mean for average periodic return and geometric mean for compounded performance or CAGR.

---

### Section summary

Arithmetic and geometric returns are two different ways to average investment returns.

The arithmetic mean is the simple average of periodic returns.

The geometric mean measures compounded growth over time.

For CFA Level 1, this distinction is essential because investment returns compound.

For Athena AI Risk Terminal, both measures are useful, but they must be clearly labeled to avoid confusion.

The key lesson is:

```text
Arithmetic mean tells the average period return.
Geometric mean tells the compounded growth rate.
```
---
















## 18. Total return

Total return measures the full return earned from an investment.

It includes both:

```text
Price change
Income received
```

Simple idea:

```text
Total return = everything the investor earned from the investment
```

Income can include:

```text
Dividends
Coupons
Distributions
Interest payments
```

Total return is more complete than price return because many investments generate income in addition to price movement.

---

### Total return formula

The basic formula is:

```text
Total return = price return + income return
```

More explicitly:

```text
Total return = (Ending price - Beginning price + Income) / Beginning price
```

Where:

```text
Beginning price = value at the start of the period
Ending price = value at the end of the period
Income = cash received during the period
```

---

### Price return

Price return only measures the change in price.

Formula:

```text
Price return = (Ending price - Beginning price) / Beginning price
```

Example:

```text
Beginning price = 100
Ending price    = 104
```

Calculation:

```text
Price return = (104 - 100) / 100
Price return = 4 / 100
Price return = 4%
```

The asset price increased by 4%.

However, this ignores any income received.

---

### Income return

Income return measures income received relative to the beginning value.

Formula:

```text
Income return = Income / Beginning price
```

Example:

```text
Beginning price = 100
Dividend        = 3
```

Calculation:

```text
Income return = 3 / 100
Income return = 3%
```

The investor received income equal to 3% of the initial investment.

---

### Total return example

Suppose an investor owns a stock.

```text
Beginning price = 100
Ending price    = 104
Dividend        = 3
```

Price return:

```text
Price return = (104 - 100) / 100
Price return = 4%
```

Income return:

```text
Income return = 3 / 100
Income return = 3%
```

Total return:

```text
Total return = 4% + 3%
Total return = 7%
```

Using the full formula:

```text
Total return = (104 - 100 + 3) / 100
Total return = 7 / 100
Total return = 7%
```

The investor earned 7% in total.

---

### Total return vs price return

The difference between total return and price return is income.

Simple comparison:

```text
Price return = price movement only
Total return = price movement + income
```

Example:

```text
Price return = 4%
Income return = 3%
Total return = 7%
```

If the investor only looks at price return, the investment appears to have earned 4%.

But the full economic return is 7%.

This is why total return is often better for performance analysis.

---

### Why total return matters

Total return matters because income can represent a large part of investment performance.

This is especially true for:

```text
Dividend stocks
Bond portfolios
Income ETFs
Real estate investment trusts
Money market instruments
Long-term portfolios
```

Example:

```text
A stock price may remain stable,
but the investor may still earn dividends.
```

Another example:

```text
A bond price may fall,
but coupon income may offset part of the loss.
```

Price movement alone does not always show the full investment result.

---

### Total return for stocks

For stocks, total return includes:

```text
Price appreciation or depreciation
Dividends
```

Example:

```text
Beginning stock price = 50
Ending stock price    = 55
Dividend              = 1
```

Calculation:

```text
Total return = (55 - 50 + 1) / 50
Total return = 6 / 50
Total return = 12%
```

The stock earned:

```text
10% from price appreciation
2% from dividends
```

Total return:

```text
12%
```

---

### Total return for bonds

For bonds, total return includes:

```text
Bond price change
Coupon payments
```

Example:

```text
Beginning bond price = 1,000
Ending bond price    = 970
Coupon received      = 50
```

Calculation:

```text
Total return = (970 - 1,000 + 50) / 1,000
Total return = 20 / 1,000
Total return = 2%
```

Even though the bond price fell, the coupon income created a positive total return.

This is why total return is essential in fixed income analysis.

---

### Total return for ETFs

For ETFs, total return includes:

```text
ETF price movement
Distributions
```

ETF distributions may come from:

```text
Dividends
Bond coupons
Interest income
Capital gains distributions
```

Example:

```text
Beginning ETF price = 100
Ending ETF price    = 106
Distribution        = 2
```

Calculation:

```text
Total return = (106 - 100 + 2) / 100
Total return = 8%
```

The investor earned 6% from price movement and 2% from distributions.

---

### Total return index

A total return index includes both price changes and reinvested income.

This is different from a price return index.

Simple comparison:

```text
Price return index = price movement only
Total return index = price movement + reinvested income
```

Example:

```text
Index price return = 8%
Dividend contribution = 2%
Total return index return = 10%
```

For long-term analysis, total return indices are usually more meaningful because they reflect reinvested income.

This is especially important when comparing portfolios to benchmarks.

---

### Reinvested income

Total return calculations often assume income is reinvested.

Reinvested income means that dividends, coupons or distributions are used to buy more of the investment.

Example:

```text
Investor receives a dividend.
Instead of keeping it as cash,
the investor reinvests it into the asset.
```

Over long periods, reinvested income can significantly increase final wealth.

This is one reason total return can be much higher than price return over long horizons.

---

### Total return and adjusted close

For stocks and ETFs, adjusted close is often used to approximate total return.

Adjusted close attempts to reflect corporate actions such as:

```text
Dividends
Stock splits
Special distributions
```

Example:

```text
A dividend may reduce the raw stock price,
but adjusted close helps reflect that the investor received income.
```

For Athena, adjusted close can be useful when calculating historical total returns from price series.

However, Athena should clearly document whether total return is calculated from:

```text
Adjusted close
Explicit income data
A total return index
```

This matters because different methods may produce slightly different results.

---

### Total return and income timing

Income timing can affect return calculations.

Example:

```text
Dividend paid early in the year
Dividend paid at the end of the year
```

If income is reinvested, the timing matters because earlier income can earn additional returns.

For simple analysis, total return may treat income as received during the period.

For more advanced analysis, Athena could track exact income dates.

Example fields:

```text
dividend_date
coupon_payment_date
distribution_date
reinvestment_date
```

This is not required for the first version, but it is useful for future precision.

---

### Gross total return vs net total return

Total return can be measured before or after costs.

### Gross total return

Gross total return is measured before costs.

Possible costs ignored:

```text
Trading fees
Management fees
Taxes
Bid-ask spread costs
Foreign exchange costs
```

### Net total return

Net total return is measured after costs.

Simple comparison:

```text
Gross total return = return before costs
Net total return = return after costs
```

Example:

```text
Gross total return = 8%
Costs and fees = 1%
Net total return = 7%
```

For Athena’s first version, gross total return is easier to implement.

A later version can support net returns.

---

### Total return and taxes

Taxes can reduce the return an investor actually keeps.

Taxable items may include:

```text
Dividends
Interest income
Capital gains
Foreign withholding taxes
```

Example:

```text
Dividend received = 100
Tax paid = 15
Net dividend = 85
```

The investor’s after-tax total return is lower than the pre-tax total return.

For CFA Level 1, the key idea is that investor returns can be measured before or after taxes.

For Athena, tax modeling can be a future extension, not a first MVP feature.

---

### Total return and currency

For international investments, total return depends on currency conversion.

Example:

```text
A Canadian investor owns a US ETF.
The ETF return in USD is 8%.
```

The investor’s CAD return also depends on:

```text
USD/CAD movement
```

If the US dollar appreciates against the Canadian dollar, the CAD return may be higher.

If the US dollar depreciates, the CAD return may be lower.

Simple distinction:

```text
Local-currency total return = return in the asset currency
Base-currency total return = return converted into the investor’s reporting currency
```

Athena should clearly state which currency is used.

---

### Total return and inflation

Total return is usually reported as a nominal return.

This means it is not automatically adjusted for inflation.

Example:

```text
Nominal total return = 7%
Inflation = 3%
```

Approximate real total return:

```text
Real total return ≈ 7% - 3%
Real total return ≈ 4%
```

For long-term analysis, real total return can be more meaningful because it shows purchasing power growth.

Athena can later support both:

```text
Nominal total return
Real total return
```

---

### Common beginner mistakes

Common mistakes include:

```text
Looking only at price return
Ignoring dividends
Ignoring coupons
Ignoring ETF distributions
Comparing price return to a total return benchmark
Forgetting fees and taxes
Mixing currencies
Ignoring inflation for long-term analysis
```

Example mistake:

```text
Portfolio price return = 6%
Benchmark total return = 8%
```

This comparison may be unfair if the portfolio return excludes income while the benchmark includes income.

The return type must be consistent.

---

### Total return data needed in Athena

To calculate total return, Athena may need:

```text
Beginning price
Ending price
Income received
Income date
Currency
Start date
End date
Price field used
Asset identifier
```

For stocks:

```text
beginning_price
ending_price
dividends
currency
```

For bonds:

```text
beginning_price
ending_price
coupon_payments
currency
```

For ETFs:

```text
beginning_price
ending_price
distributions
currency
```

For portfolios:

```text
beginning_portfolio_value
ending_portfolio_value
income_received
cash_flows
base_currency
```

---

### Total return in Athena

Athena can use total return to show complete investment performance.

Possible use cases:

```text
Asset total return
Portfolio total return
Benchmark total return
ETF total return
Bond total return
Income contribution analysis
Price return vs total return comparison
```

Example output:

```text
Asset: SPY
Beginning price: 100
Ending price: 108
Distributions: 2
Price return: 8.00%
Income return: 2.00%
Total return: 10.00%
Currency: USD
```

This helps the user understand where the return came from.

---

### Price return vs income return contribution

Athena can separate total return into components.

Example:

```text
Total return = 10%
Price return = 7%
Income return = 3%
```

This decomposition is useful because two assets can have the same total return but different sources.

Example:

```text
Asset A:
Price return = 10%
Income return = 0%
Total return = 10%

Asset B:
Price return = 4%
Income return = 6%
Total return = 10%
```

Both assets earned 10%, but their return profiles are different.

Asset A is more growth-driven.

Asset B is more income-driven.

---

### CFA Level 1 takeaway

For CFA Level 1, total return is a basic but essential performance measure.

Important concepts include:

```text
Price return
Income return
Dividends
Coupons
Distributions
Total return index
Gross return
Net return
Nominal return
Real return
```

The key formula is:

```text
Total return = (Ending price - Beginning price + Income) / Beginning price
```

A simple memory rule:

```text
Total return = price movement + income.
```

Price return alone can understate performance when income is important.

---

### Athena implementation takeaway

For Athena, total return should be clearly separated from price return.

The performance module should support:

```text
Price return calculation
Income return calculation
Total return calculation
Adjusted close usage
Return type labeling
Benchmark return consistency
Currency identification
Future net return extension
```

The goal is to make sure users understand whether a displayed return includes income or not.

A useful label would be:

```text
Return type: Total return
Income included: Yes
Price field: Adjusted close
Currency: USD
```

This makes the analysis transparent.

---

### Mini revision questions

1. What does total return include?

2. What is the difference between price return and total return?

3. What types of income can be included in total return?

4. Why is total return important for bonds?

5. Why is total return important for dividend stocks?

6. What is a total return index?

7. Why should Athena label return types clearly?

8. What is the difference between gross total return and net total return?

---

### Mini answers

1. Total return includes both price change and income received.

2. Price return includes only price movement, while total return includes price movement and income.

3. Income can include dividends, coupons, distributions and interest payments.

4. Total return is important for bonds because coupon income can be a major part of the return.

5. Total return is important for dividend stocks because price return alone ignores dividends.

6. A total return index includes price changes and reinvested income.

7. Athena should label return types clearly so users know whether income is included.

8. Gross total return is before costs, while net total return is after costs such as fees, taxes and transaction costs.

---

### Section summary

Total return measures the complete return of an investment.

It includes both price movement and income.

For CFA Level 1, total return is essential because many investments generate income, and price return alone can be incomplete.

For Athena AI Risk Terminal, total return helps users understand the full performance of an asset, ETF, bond or portfolio.

The key lesson is:

```text
Price return shows price movement.
Total return shows the full investment result.
```
---






## 19. Compounding and annualization

Compounding means that returns accumulate over time.

When an investment earns a return, the new value becomes the base for the next return.

Simple idea:

```text
Compounding = earning returns on previous returns
```

This is one of the most important concepts in finance because investment performance is not linear over time.

Returns multiply through time.  
They do not simply add.

---

### Why compounding matters

Suppose an investment starts at 100.

If it gains 10%, the new value is:

```text
100 × 1.10 = 110
```

If it then loses 10%, the loss is applied to 110, not to the original 100.

```text
110 × 0.90 = 99
```

Final value:

```text
99
```

Total return:

```text
99 / 100 - 1 = -1%
```

So:

```text
+10% followed by -10% = -1%
```

not:

```text
0%
```

This happens because the second return is applied to the new value created after the first return.

---

### Growth factor

A growth factor converts a return into a multiplier.

Formula:

```text
Growth factor = 1 + return
```

Examples:

```text
Return = 10%
Growth factor = 1.10
```

```text
Return = -10%
Growth factor = 0.90
```

```text
Return = 0%
Growth factor = 1.00
```

To compound returns, multiply the growth factors.

Example:

```text
Return 1 = 10%
Return 2 = -10%
```

Growth factors:

```text
1.10
0.90
```

Compounded return:

```text
(1.10 × 0.90) - 1 = -1%
```

---

### Multi-period compounded return

When there are multiple returns, the total return is:

```text
Total return = (1 + R1)(1 + R2)...(1 + Rn) - 1
```

Where:

```text
R1, R2, ..., Rn = periodic returns
```

Example:

```text
Year 1 return = 5%
Year 2 return = 8%
Year 3 return = -3%
```

Calculation:

```text
Total return = (1.05)(1.08)(0.97) - 1
Total return = 1.09998 - 1
Total return ≈ 10.00%
```

The investment earned approximately 10% over the full period.

---

### Compounding vs adding returns

A common beginner mistake is to add returns.

Example:

```text
Year 1 return = 20%
Year 2 return = -20%
```

Adding returns gives:

```text
20% - 20% = 0%
```

But this is wrong.

Correct calculation:

```text
Initial value = 100
After +20% = 120
After -20% = 96
```

Final value:

```text
96
```

Total return:

```text
96 / 100 - 1 = -4%
```

So:

```text
+20% followed by -20% = -4%
```

not:

```text
0%
```

The larger the returns are, the more important compounding becomes.

---

### Compounding positive returns

Compounding is powerful when returns are positive.

Example:

```text
Initial value = 100
Annual return = 10%
Time = 3 years
```

Calculation:

```text
Year 1: 100 × 1.10 = 110
Year 2: 110 × 1.10 = 121
Year 3: 121 × 1.10 = 133.10
```

Final value:

```text
133.10
```

Total return:

```text
33.10%
```

The investor earned more than 30% because gains were reinvested and compounded.

---

### Compounding negative returns

Losses also compound.

Example:

```text
Initial value = 100
Annual return = -10%
Time = 3 years
```

Calculation:

```text
Year 1: 100 × 0.90 = 90
Year 2: 90 × 0.90 = 81
Year 3: 81 × 0.90 = 72.90
```

Final value:

```text
72.90
```

Total return:

```text
72.90 / 100 - 1 = -27.10%
```

A 10% loss repeated for three years does not produce exactly a 30% loss.

It produces a compounded loss of 27.10%.

---

### Annualization

Annualization converts a return or risk measure into a yearly equivalent.

It answers the question:

```text
What would this return or risk look like on a yearly basis?
```

Annualization is useful because investments are often measured over different time periods.

Example:

```text
Investment A return = 5% over 6 months
Investment B return = 9% over 1 year
```

To compare them properly, the returns should be expressed over the same time horizon.

Annualization makes returns easier to compare.

---

### Annualized return

Annualized return expresses a multi-period return as an equivalent yearly return.

Formula:

```text
Annualized return = (Ending value / Beginning value)^(1 / years) - 1
```

This formula gives the constant annual return that would produce the same ending value.

Simple idea:

```text
Annualized return = average compounded yearly return
```

---

### Annualized return example

Suppose:

```text
Beginning value = 100
Ending value    = 121
Time            = 2 years
```

Calculation:

```text
Annualized return = (121 / 100)^(1/2) - 1
Annualized return = 1.21^(1/2) - 1
Annualized return = 1.10 - 1
Annualized return = 10%
```

This means the investment grew as if it earned:

```text
10% per year compounded annually
```

---

### Why annualized return is not always the simple average

Suppose an investment earns:

```text
Year 1 return = 20%
Year 2 return = -10%
```

Arithmetic average:

```text
(20% - 10%) / 2 = 5%
```

But the compounded result is:

```text
100 × 1.20 × 0.90 = 108
```

Ending value:

```text
108
```

Annualized return:

```text
(108 / 100)^(1/2) - 1
= 1.08^(1/2) - 1
≈ 3.92%
```

So:

```text
Arithmetic average return = 5.00%
Annualized compounded return = 3.92%
```

The annualized return is lower because it reflects compounding.

---

### Annualizing short-period returns

Short-period returns can be annualized, but the method must be used carefully.

Example:

```text
Monthly return = 1%
```

Annualized return using compounding:

```text
Annualized return = (1.01)^12 - 1
Annualized return ≈ 12.68%
```

This assumes the 1% monthly return continues for 12 months.

This may not actually happen.

Therefore, annualized short-period returns should be interpreted carefully.

---

### Simple annualization mistake

A common mistake is to multiply a short-period return by the number of periods.

Example:

```text
Monthly return = 1%
```

Simple multiplication gives:

```text
1% × 12 = 12%
```

But compounded annualization gives:

```text
(1.01)^12 - 1 = 12.68%
```

The difference comes from compounding.

For small returns, the difference may be small.

For larger returns, the difference becomes more important.

---

### Annualized return from daily returns

If Athena has daily returns, it can annualize average performance.

A simplified approach is:

```text
Annualized return = (1 + average daily return)^252 - 1
```

Why 252?

Because financial markets usually have approximately:

```text
252 trading days per year
```

Example:

```text
Average daily return = 0.04%
```

Calculation:

```text
Annualized return = (1.0004)^252 - 1
Annualized return ≈ 10.60%
```

This is an estimate, not a guarantee.

---

### Annualized volatility

Volatility is annualized differently from returns.

For daily volatility:

```text
Annualized volatility = Daily volatility × sqrt(252)
```

This is not the same as annualizing returns.

Returns compound.

Volatility scales with the square root of time under simplifying assumptions.

Simple comparison:

```text
Return annualization uses compounding.
Volatility annualization uses square root of time.
```

---

### Why volatility uses square root of time

Volatility is based on standard deviation.

Variance scales approximately linearly with time.

Standard deviation is the square root of variance.

That is why volatility scales with the square root of time.

Simple logic:

```text
Variance over 1 year ≈ daily variance × 252
Volatility = square root of variance
Annualized volatility ≈ daily volatility × sqrt(252)
```

This rule assumes that returns are independent and similarly distributed over time.

In real markets, this assumption is not always perfect.

---

### Annualized volatility example

Suppose:

```text
Daily volatility = 1%
```

Annualized volatility:

```text
Annualized volatility = 1% × sqrt(252)
Annualized volatility ≈ 1% × 15.87
Annualized volatility ≈ 15.87%
```

This means the annualized volatility estimate is approximately 15.87%.

---

### Monthly volatility annualization

If volatility is measured using monthly returns, the annualization factor is:

```text
sqrt(12)
```

Formula:

```text
Annualized volatility = Monthly volatility × sqrt(12)
```

Example:

```text
Monthly volatility = 4%
```

Calculation:

```text
Annualized volatility = 4% × sqrt(12)
Annualized volatility ≈ 13.86%
```

The annualization factor depends on the data frequency.

---

### Common annualization factors

Common annualization factors include:

```text
Daily returns: 252 trading days
Weekly returns: 52 weeks
Monthly returns: 12 months
Quarterly returns: 4 quarters
```

For returns, these are used in compounding formulas.

For volatility, their square roots are used.

Simple table:

```text
Frequency   Return annualization        Volatility annualization

Daily       (1 + R)^252 - 1              Vol × sqrt(252)
Weekly      (1 + R)^52 - 1               Vol × sqrt(52)
Monthly     (1 + R)^12 - 1               Vol × sqrt(12)
Quarterly   (1 + R)^4 - 1                Vol × sqrt(4)
```

---

### Return annualization vs volatility annualization

This distinction is essential.

Returns and volatility do not annualize the same way.

```text
Returns:
Annualized using compounding.

Volatility:
Annualized using square root of time.
```

Example:

```text
Daily return = 0.05%
Daily volatility = 1%
```

Annualized return estimate:

```text
(1.0005)^252 - 1 ≈ 13.42%
```

Annualized volatility estimate:

```text
1% × sqrt(252) ≈ 15.87%
```

The formulas are different because the concepts are different.

---

### Annualization and data frequency

Athena must know the data frequency before annualizing.

Example:

```text
Daily data
Monthly data
Weekly data
```

If Athena uses the wrong frequency, the annualized result will be wrong.

Example mistake:

```text
Using sqrt(252) for monthly volatility
```

This would overstate the annualized volatility.

Correct monthly formula:

```text
Monthly volatility × sqrt(12)
```

So Athena should always store or infer the return frequency.

---

### Annualization and investment horizon

Annualization can make returns comparable, but it can also be misleading if the period is too short.

Example:

```text
One-day return = 2%
```

Annualizing this mechanically gives a very large number:

```text
(1.02)^252 - 1
```

This assumes the asset earns 2% every trading day for a full year.

That is unrealistic.

Practical rule:

```text
Annualized numbers are more meaningful when based on enough observations.
```

Athena should avoid over-interpreting annualized returns from very short samples.

---

### CAGR and annualized return

CAGR means Compound Annual Growth Rate.

It is a type of annualized return.

Formula:

```text
CAGR = (Ending value / Beginning value)^(1 / years) - 1
```

This is the same formula used for annualized return over multiple years.

Example:

```text
Beginning value = 10,000
Ending value    = 15,000
Years           = 5
```

Calculation:

```text
CAGR = (15,000 / 10,000)^(1/5) - 1
CAGR = 1.5^(1/5) - 1
CAGR ≈ 8.45%
```

This means the investment grew at an equivalent annual compounded rate of 8.45%.

---

### Compounding frequency

Compounding frequency describes how often returns are applied.

Examples:

```text
Annual compounding
Semi-annual compounding
Quarterly compounding
Monthly compounding
Daily compounding
Continuous compounding
```

The more frequently returns compound, the slightly higher the ending value can become, all else equal.

Example:

```text
10% annual interest compounded annually
```

is slightly different from:

```text
10% annual interest compounded monthly
```

This topic is especially important in fixed income and quantitative methods.

---

### Continuous compounding

Continuous compounding is the theoretical case where compounding happens constantly.

It is linked to log returns.

Simple idea:

```text
Simple return = discrete compounding
Log return = continuous compounding
```

This is why log returns are often described as continuously compounded returns.

For Athena, continuous compounding is more relevant for advanced modeling than for basic dashboards.

---

### Compounding and risk

Compounding also explains why large losses are difficult to recover from.

Example:

```text
Loss = -50%
```

Starting from 100:

```text
100 × 0.50 = 50
```

To return from 50 to 100, the investment needs:

```text
100 / 50 - 1 = 100%
```

So:

```text
A 50% loss requires a 100% gain to recover.
```

This is important in risk management.

Avoiding large drawdowns can be very important for long-term compounded growth.

---

### Drawdowns and compounding

A drawdown is a decline from a previous peak.

Example:

```text
Portfolio peak = 100
Portfolio trough = 80
```

Drawdown:

```text
80 / 100 - 1 = -20%
```

To recover:

```text
100 / 80 - 1 = 25%
```

A 20% loss requires a 25% gain to recover.

This shows why volatility and large losses can damage long-term compounding.

---

### Compounding in Athena

Athena can use compounding to calculate:

```text
Cumulative returns
CAGR
Annualized returns
Portfolio growth
Backtest performance
Drawdown recovery
Scenario analysis
```

Example:

```text
Initial portfolio value = 100,000
Return year 1 = 8%
Return year 2 = -5%
Return year 3 = 12%
```

Compounded value:

```text
100,000 × 1.08 × 0.95 × 1.12
= 114,912
```

Total return:

```text
114,912 / 100,000 - 1 = 14.912%
```

This is more accurate than simply adding returns:

```text
8% - 5% + 12% = 15%
```

---

### Annualization in Athena

Athena should annualize returns and volatility carefully.

The system should know:

```text
Data frequency
Number of observations
Start date
End date
Annualization factor
Return type
Volatility method
```

Example output:

```text
Daily volatility: 1.00%
Annualization factor: sqrt(252)
Annualized volatility: 15.87%
```

Another example:

```text
Beginning value: 100
Ending value: 121
Period: 2 years
Annualized return: 10.00%
```

Athena should clearly show the method used.

---

### Common beginner mistakes

Common mistakes include:

```text
Adding returns instead of compounding them
Thinking +10% and -10% cancel perfectly
Using the same formula for annualizing return and volatility
Using sqrt(252) for returns
Using compounding for volatility
Annualizing very short periods without caution
Using the wrong annualization factor
Ignoring data frequency
Confusing arithmetic mean with CAGR
```

Example mistake:

```text
Daily volatility = 1%
Annualized volatility = 1% × 252
```

This is wrong.

Correct formula:

```text
Annualized volatility = 1% × sqrt(252)
```

---

### CFA Level 1 takeaway

For CFA Level 1, compounding and annualization are essential.

Important concepts include:

```text
Growth factor
Compounded return
Annualized return
CAGR
Compounding frequency
Annualized volatility
Square-root-of-time rule
Data frequency
Drawdown recovery
```

Important formulas:

```text
Total compounded return = (1 + R1)(1 + R2)...(1 + Rn) - 1
```

```text
Annualized return = (Ending value / Beginning value)^(1 / years) - 1
```

```text
Annualized volatility = periodic volatility × sqrt(number of periods per year)
```

A simple memory rule:

```text
Returns compound.
Volatility scales with the square root of time.
```

---

### Athena implementation takeaway

For Athena, compounding and annualization must be implemented carefully because they affect performance and risk metrics.

The analytics module should support:

```text
Compounded return calculation
Cumulative return curves
CAGR calculation
Annualized return calculation
Annualized volatility calculation
Frequency-aware annualization
Drawdown recovery calculation
Clear method labels
```

Athena should avoid showing annualized metrics without explaining:

```text
The period used
The data frequency
The annualization factor
The formula applied
```

This makes the platform more transparent and reliable.

---

### Mini revision questions

1. What does compounding mean?

2. Why does +10% followed by -10% not equal 0%?

3. What is a growth factor?

4. How do you combine multiple period returns?

5. What does annualized return measure?

6. What is the annualized return formula?

7. How do you annualize daily volatility?

8. Why do returns and volatility annualize differently?

9. What is CAGR?

10. Why can annualizing very short-period returns be misleading?

---

### Mini answers

1. Compounding means returns accumulate over time on the updated investment value.

2. Because the -10% loss is applied to the new value after the +10% gain, not to the original value.

3. A growth factor is 1 plus the return.

4. Multiple returns are combined by multiplying their growth factors: (1 + R1)(1 + R2)...(1 + Rn) - 1.

5. Annualized return expresses a multi-period return as an equivalent yearly rate.

6. The formula is: Annualized return = (Ending value / Beginning value)^(1 / years) - 1.

7. Daily volatility is annualized by multiplying it by sqrt(252).

8. Returns compound over time, while volatility is based on standard deviation and scales with the square root of time.

9. CAGR is the Compound Annual Growth Rate, the annualized compounded growth rate over multiple years.

10. It can be misleading because it assumes a short-period return continues for a full year.

---

### Section summary

Compounding means that returns accumulate over time on the updated investment value.

Annualization converts returns or risk measures into yearly equivalents.

For CFA Level 1, this section is essential because it explains how investment returns grow over time and why risk is annualized differently from return.

For Athena AI Risk Terminal, compounding and annualization are essential for portfolio performance, volatility analysis, backtesting and risk dashboards.

The key lesson is:

```text
Returns must be compounded over time.
Volatility must be annualized using the square-root-of-time rule.
```
---












## Part III — Volatility, distributions and statistical risk

## 20. Volatility

Volatility measures how much returns move around their average.

If returns move a lot, volatility is high.  
If returns are stable, volatility is low.

Volatility is one of the most important concepts in market finance because it measures uncertainty.

Simple idea:

```text
Volatility = instability of returns
```

A volatile asset has returns that fluctuate strongly.

A low-volatility asset has returns that are more stable.

---

### Volatility measures movement

Volatility does not only mean loss.

It measures movement in both directions:

```text
Upward movement
Downward movement
```

An asset can be volatile because it rises sharply, falls sharply, or both.

Example:

```text
Day 1: +5%
Day 2: -6%
Day 3: +4%
Day 4: -7%
```

This asset is volatile because returns are moving strongly from day to day.

Important distinction:

```text
Volatility measures uncertainty.
Loss measures negative performance.
```

They are related, but they are not the same thing.

---

### Low volatility example

A low-volatility asset has returns that stay close to the average.

Example:

```text
Day 1: +0.1%
Day 2: -0.2%
Day 3: +0.1%
Day 4: +0.0%
```

The returns are small and stable.

This means the asset is not moving much from day to day.

A low-volatility asset may feel more predictable.

---

### High volatility example

A high-volatility asset has returns that move strongly.

Example:

```text
Day 1: +5%
Day 2: -6%
Day 3: +4%
Day 4: -7%
```

The returns are far from stable.

The asset may generate large gains, but it can also generate large losses.

This is why volatility is often used as a risk indicator.

---

### Volatility and risk

In finance, volatility is commonly used as a measure of risk.

The reason is simple:

```text
The more returns fluctuate,
the less certain the investment outcome becomes.
```

Example:

```text
Asset A usually moves between -1% and +1% per day.
Asset B usually moves between -8% and +8% per day.
```

Asset B is more uncertain.

An investor in Asset B faces a wider range of possible outcomes.

This does not mean Asset B is always bad.

It means the investor must be comfortable with larger fluctuations.

---

### Volatility and investor experience

Two assets can have the same average return but very different volatility.

Example:

```text
Asset A:
Average return = 6%
Volatility = low

Asset B:
Average return = 6%
Volatility = high
```

Both assets have the same average return, but Asset B may be much harder to hold.

Why?

Because its value may rise and fall sharply along the way.

This matters because investors do not only care about final return.  
They also care about the path taken to get there.

Simple idea:

```text
The same return can feel very different depending on volatility.
```

---

### Volatility and uncertainty

Volatility is useful because the future is uncertain.

If an asset has high historical volatility, its future value may be harder to predict.

Example:

```text
Low-volatility asset:
Expected range of outcomes is narrower.

High-volatility asset:
Expected range of outcomes is wider.
```

This is why volatility is often used in:

```text
Risk management
Portfolio construction
Option pricing
Stress testing
Performance evaluation
```

---

### Volatility and standard deviation

Volatility is usually measured using the standard deviation of returns.

Simple idea:

```text
Volatility = standard deviation of returns
```

Standard deviation measures how far observations are from their average.

If returns are close to the average, standard deviation is low.

If returns are far from the average, standard deviation is high.

Example:

```text
Stable returns → low standard deviation → low volatility
Unstable returns → high standard deviation → high volatility
```

The detailed formula is covered in the variance and standard deviation section, but the key intuition is simple:

```text
Volatility measures dispersion.
```

---

### Volatility uses returns, not prices

Volatility is usually calculated from returns, not directly from prices.

Why?

Because prices are not directly comparable across assets.

Example:

```text
Stock A price = 20
Stock B price = 500
```

The price level alone does not tell us which asset is riskier.

Instead, analysts calculate percentage returns first.

Then they measure how much those returns fluctuate.

Basic workflow:

```text
Historical prices
      ↓
Returns
      ↓
Standard deviation of returns
      ↓
Volatility
```

This is the correct logic for Athena.

---

### Volatility and time horizon

Volatility depends on the time horizon.

Examples:

```text
Daily volatility
Monthly volatility
Annualized volatility
Rolling volatility
```

A daily volatility number and an annualized volatility number do not mean the same thing.

Example:

```text
Daily volatility = 1%
Annualized volatility ≈ 15.87%
```

The annualized number expresses the risk on a yearly scale.

Athena should always label the volatility horizon clearly.

A volatility value without a time horizon is incomplete.

---

### Volatility and market regimes

Volatility changes over time.

Markets can move through different regimes.

Examples:

```text
Calm market regime
Normal market regime
Stressed market regime
Crisis market regime
```

During calm periods, volatility may be low.

During crises, volatility can rise quickly.

Example:

```text
Before crisis:
Daily returns are small and stable.

During crisis:
Daily returns become large and unpredictable.
```

This is why rolling volatility is useful.

It helps detect when market conditions are changing.

---

### Volatility and diversification

Volatility can be reduced through diversification.

A portfolio with several assets may be less volatile than a single asset if the assets do not all move together.

Example:

```text
Asset A is volatile.
Asset B is volatile.
But they do not always move in the same direction.
```

The portfolio may have lower volatility than each individual asset.

This is because correlation matters.

Simple idea:

```text
Portfolio volatility depends on individual asset volatility and correlations.
```

This concept becomes important in portfolio management.

---

### Volatility and correlation

Volatility measures how much one asset moves.

Correlation measures how two assets move together.

They answer different questions.

```text
Volatility:
How unstable is this asset?

Correlation:
How does this asset move relative to another asset?
```

Both are needed for portfolio risk analysis.

Example:

```text
A portfolio of volatile assets can still reduce risk
if the assets are not highly correlated.
```

Athena should eventually combine volatility and correlation to estimate portfolio risk.

---

### Volatility and drawdowns

Volatility is related to risk, but it does not directly measure maximum loss.

An asset may have high volatility because it moves strongly up and down.

A drawdown measures decline from a previous peak.

Example:

```text
Peak value = 100
Trough value = 80

Drawdown = -20%
```

Volatility and drawdown are different.

```text
Volatility = dispersion of returns
Drawdown = loss from peak to trough
```

Both are useful risk measures.

Volatility tells us about instability.  
Drawdown tells us about experienced loss.

---

### Volatility and options

Volatility is very important for options.

Option prices depend heavily on expected volatility.

Simple idea:

```text
Higher expected volatility usually increases option value.
```

Why?

Because options benefit from large price movements.

Even if the underlying asset moves upward or downward, larger movements can make options more valuable.

This is why implied volatility is important in derivatives analysis.

For Athena’s first version, historical volatility is enough.  
Later, implied volatility can be added for options and derivatives modules.

---

### Volatility is not the same as probability of loss

A common beginner mistake is to think:

```text
High volatility = guaranteed loss
```

This is not correct.

High volatility means a wider range of possible outcomes.

Example:

```text
A high-volatility asset may gain 20%.
It may also lose 20%.
```

Volatility does not predict direction.

It measures the size of fluctuations.

Simple idea:

```text
Volatility tells us how much an asset moves,
not whether it will go up or down.
```

---

### Volatility and expected return

In finance, investors often expect higher returns for taking more risk.

This is called the risk-return tradeoff.

Simple idea:

```text
Higher risk should require higher expected return.
```

However, this is not guaranteed.

A volatile asset does not automatically produce a higher return.

Example:

```text
Asset A:
Expected return = 8%
Volatility = 15%

Asset B:
Expected return = 8%
Volatility = 35%
```

Both assets have the same expected return, but Asset B has more risk.

Asset B is less attractive if it does not compensate the investor for the extra volatility.

---

### Volatility and risk-adjusted performance

Volatility is often used to evaluate risk-adjusted performance.

A portfolio return is more meaningful when compared with the risk taken.

Example:

```text
Portfolio A:
Return = 10%
Volatility = 12%

Portfolio B:
Return = 10%
Volatility = 25%
```

Both portfolios earned 10%, but Portfolio A achieved the return with less volatility.

This may make Portfolio A more attractive.

Later, Athena can use volatility in risk-adjusted metrics such as:

```text
Sharpe ratio
Information ratio
Volatility-adjusted return
```

---

### Historical volatility

Historical volatility is calculated from past returns.

It answers:

```text
How volatile was the asset in the past?
```

Example:

```text
Use the last 252 daily returns
to estimate one-year historical volatility.
```

Historical volatility is useful because it is observable and easy to calculate.

However, it is backward-looking.

It does not guarantee future volatility.

---

### Expected volatility

Expected volatility is an estimate of future volatility.

It answers:

```text
How volatile do we expect the asset to be in the future?
```

Expected volatility may be based on:

```text
Historical volatility
Implied volatility
Risk models
Scenario analysis
Market conditions
```

This is harder to estimate because the future is uncertain.

For Athena’s first version, historical volatility is the simplest and most transparent approach.

---

### Volatility data needed in Athena

To calculate volatility, Athena needs:

```text
Asset identifier
Clean price series
Return series
Return type
Date range
Frequency
Volatility window
Annualization factor
Currency
```

Example:

```text
symbol: AAPL
return_type: simple return
frequency: daily
window: 252 trading days
annualization_factor: sqrt(252)
```

This information is necessary because volatility depends on methodology.

---

### Volatility in Athena

Athena can use volatility to support:

```text
Asset risk analysis
Portfolio risk analysis
Market regime detection
Risk dashboards
Benchmark comparison
Rolling risk analysis
Stress monitoring
```

Example output:

```text
Asset: AAPL
Daily volatility: 1.20%
Annualized volatility: 19.05%
Window: 252 trading days
Return type: simple return
Price field: adjusted close
```

This output is useful because it shows both the number and the methodology.

---

### Volatility labels in Athena

Athena should always label volatility clearly.

A volatility number should include:

```text
Frequency
Window
Annualization status
Return type
Price field used
```

Bad label:

```text
Volatility = 18%
```

Better label:

```text
Annualized volatility = 18%
Window = 252 daily returns
Return type = simple return
Price field = adjusted close
```

This avoids confusion and makes the result more professional.

---

### Common beginner mistakes

Common mistakes include:

```text
Thinking volatility only means loss
Calculating volatility from prices instead of returns
Forgetting to annualize volatility
Using the wrong annualization factor
Comparing daily volatility with annualized volatility
Ignoring the date range used
Assuming historical volatility predicts the future perfectly
Confusing volatility with drawdown
Confusing volatility with correlation
```

Example mistake:

```text
Asset A volatility = 1%
Asset B volatility = 20%
```

This comparison is incomplete unless we know the time horizon.

A daily volatility of 1% and an annualized volatility of 20% are not directly comparable.

---

### CFA Level 1 takeaway

For CFA Level 1, volatility is a core risk concept.

Important ideas include:

```text
Return dispersion
Standard deviation
Risk
Uncertainty
Historical volatility
Annualized volatility
Risk-return tradeoff
Diversification
Portfolio risk
```

A simple memory rule:

```text
Volatility measures how much returns fluctuate around their average.
```

Another important rule:

```text
Volatility measures movement, not direction.
```

---

### Athena implementation takeaway

For Athena, volatility should be one of the first risk metrics implemented.

The volatility module should support:

```text
Return series calculation
Daily volatility
Annualized volatility
Rolling volatility
Window selection
Frequency-aware annualization
Volatility comparison
Benchmark volatility
Portfolio volatility extension
Clear methodology labels
```

Athena should make volatility understandable, not just display a number.

The user should be able to answer:

```text
What asset is volatile?
Over what period?
Using which returns?
Annualized or not?
Compared with what benchmark?
```

---

### Mini revision questions

1. What does volatility measure?

2. Does volatility only measure losses?

3. Why is volatility usually calculated from returns instead of prices?

4. What is the relationship between volatility and standard deviation?

5. Why does the time horizon matter for volatility?

6. What is the difference between volatility and drawdown?

7. What is historical volatility?

8. Why should Athena label volatility methodology clearly?

---

### Mini answers

1. Volatility measures how much returns fluctuate around their average.

2. No. Volatility measures both upward and downward movement.

3. Returns are used because they make assets comparable in percentage terms.

4. Volatility is commonly measured as the standard deviation of returns.

5. The time horizon matters because daily, monthly and annualized volatility are different measures.

6. Volatility measures dispersion of returns, while drawdown measures decline from a previous peak.

7. Historical volatility is volatility calculated from past returns.

8. Athena should label methodology clearly because volatility depends on frequency, window, return type and annualization.

---

### Section summary

Volatility measures the instability of returns.

It is one of the most important measures of market risk because it shows how uncertain an asset’s returns are.

For CFA Level 1, volatility is essential because it connects return dispersion, risk, standard deviation, diversification and portfolio management.

For Athena AI Risk Terminal, volatility is a core risk metric that supports asset analysis, portfolio analysis, benchmark comparison and risk dashboards.

The key lesson is:

```text
Volatility measures how much returns move.
It does not predict direction,
but it helps measure uncertainty.
```

---

























## 21. Daily volatility

Daily volatility measures how much an asset’s daily returns fluctuate.

It is usually calculated as the standard deviation of daily returns.

Formula:

```text
Daily volatility = standard_deviation(daily_returns)
```

Simple idea:

```text
Daily volatility = typical daily movement of returns
```

If daily returns are close to their average, daily volatility is low.

If daily returns move far away from their average, daily volatility is high.

---

### Why daily volatility matters

Daily volatility is useful because it gives a short-term measure of market risk.

It helps answer questions such as:

```text
How much does this asset usually move in one day?
Is this asset stable or unstable on a daily basis?
Has daily risk increased recently?
Is this asset more volatile than another asset?
```

Daily volatility is often the first volatility measure calculated from market prices.

It is also the starting point for annualized volatility.

---

### Daily returns first

Daily volatility is not calculated directly from prices.

It is calculated from daily returns.

The basic workflow is:

```text
Daily prices
    ↓
Daily returns
    ↓
Standard deviation of daily returns
    ↓
Daily volatility
```

Example price series:

```text
Date        Price
Day 0       100
Day 1       101
Day 2       99
Day 3       102
```

Daily returns:

```text
Day 1 return = 101 / 100 - 1 = 1.00%
Day 2 return = 99 / 101 - 1 ≈ -1.98%
Day 3 return = 102 / 99 - 1 ≈ 3.03%
```

Daily volatility is calculated from these daily returns.

---

### Interpretation

If daily volatility is:

```text
Daily volatility = 1%
```

A simplified interpretation is:

```text
Daily returns typically move around their average by about 1%.
```

This does not mean the asset will move exactly 1% every day.

It means that, historically, daily returns have had a typical dispersion of about 1%.

Example:

```text
Average daily return = 0.05%
Daily volatility = 1.00%
```

This means daily returns are usually much more affected by daily fluctuations than by the average daily return.

---

### Low daily volatility

An asset with low daily volatility has relatively stable daily returns.

Example:

```text
Day 1: +0.10%
Day 2: -0.05%
Day 3: +0.08%
Day 4: -0.12%
Day 5: +0.03%
```

The returns stay close to zero.

This asset has low daily instability.

Low daily volatility is common for:

```text
Short-term government bond funds
Money market instruments
Stable large-cap assets during calm periods
```

---

### High daily volatility

An asset with high daily volatility has daily returns that move strongly.

Example:

```text
Day 1: +4.00%
Day 2: -5.50%
Day 3: +3.20%
Day 4: -6.00%
Day 5: +5.10%
```

The returns fluctuate widely.

This asset has high daily instability.

High daily volatility is common for:

```text
Small-cap stocks
Crypto assets
Leveraged ETFs
Commodity-related assets
Distressed stocks
High-growth technology stocks
```

---

### Daily volatility and risk

Daily volatility is often interpreted as a short-term risk measure.

A higher daily volatility means the asset has a wider range of possible daily outcomes.

Example:

```text
Asset A daily volatility = 0.8%
Asset B daily volatility = 3.0%
```

Asset B is more unstable on a daily basis.

This does not mean Asset B will always lose money.

It means Asset B’s daily returns are less predictable and more dispersed.

Simple idea:

```text
Higher daily volatility = higher short-term uncertainty
```

---

### Daily volatility and standard deviation

Daily volatility is usually the standard deviation of daily returns.

Standard deviation measures how far returns are from their average.

If daily returns are close to the average:

```text
Standard deviation is low.
```

If daily returns are far from the average:

```text
Standard deviation is high.
```

Therefore:

```text
Low standard deviation of daily returns = low daily volatility
High standard deviation of daily returns = high daily volatility
```

---

### Example with stable returns

Suppose daily returns are:

```text
Day 1: +0.10%
Day 2: +0.05%
Day 3: -0.05%
Day 4: +0.00%
Day 5: +0.08%
```

These returns are close to each other.

The daily volatility will be low.

Interpretation:

```text
The asset did not move much from day to day.
```

---

### Example with unstable returns

Suppose daily returns are:

```text
Day 1: +2.00%
Day 2: -3.00%
Day 3: +4.00%
Day 4: -2.50%
Day 5: +3.50%
```

These returns are far from each other.

The daily volatility will be high.

Interpretation:

```text
The asset moved significantly from day to day.
```

---

### Daily volatility vs annualized volatility

Daily volatility measures risk at the daily level.

Annualized volatility expresses that risk on a yearly scale.

Simple comparison:

```text
Daily volatility = one-day return instability
Annualized volatility = yearly equivalent risk estimate
```

Daily volatility is often converted into annualized volatility using:

```text
Annualized volatility = Daily volatility × sqrt(252)
```

Why 252?

Because there are approximately 252 trading days in a year.

Example:

```text
Daily volatility = 1%
Annualized volatility = 1% × sqrt(252)
Annualized volatility ≈ 15.87%
```

Daily volatility is the building block.

Annualized volatility is often used for comparison.

---

### Why daily volatility is not multiplied by 252

A common beginner mistake is to annualize volatility like this:

```text
Daily volatility × 252
```

This is wrong.

Volatility is based on standard deviation, not return.

The correct formula is:

```text
Daily volatility × sqrt(252)
```

Simple rule:

```text
Returns compound.
Volatility scales with the square root of time.
```

This rule assumes that daily returns are independent and have similar variance over time.

In real markets, this assumption is imperfect, but it is widely used.

---

### Daily volatility and time window

Daily volatility depends on the chosen time window.

Examples:

```text
20-day daily volatility
60-day daily volatility
252-day daily volatility
```

The window changes the interpretation.

```text
20-day volatility = recent short-term volatility
60-day volatility = medium-term volatility
252-day volatility = one-year historical volatility
```

Example:

```text
20-day daily volatility = 2.5%
252-day daily volatility = 1.2%
```

This may indicate that the asset has recently become more volatile.

Athena should always show the window used.

---

### Daily volatility and rolling volatility

Daily volatility can be calculated over a rolling window.

Example:

```text
Calculate daily volatility using the last 20 daily returns.
Move the window forward by one day.
Repeat the calculation.
```

This creates a rolling volatility series.

Rolling daily volatility is useful because volatility changes over time.

Example:

```text
A stock may have low volatility during normal periods
and high volatility during earnings announcements or crises.
```

For Athena, rolling volatility can help users detect market regime changes.

---

### Daily volatility and market stress

Daily volatility often increases during stressful market periods.

Examples of stress events:

```text
Earnings shocks
Interest rate surprises
Inflation surprises
Banking stress
Geopolitical events
Market crashes
Liquidity crises
```

During these periods, daily returns can become larger and less predictable.

Example:

```text
Normal period:
Daily volatility = 1%

Stress period:
Daily volatility = 4%
```

This means the asset has become much more unstable on a daily basis.

---

### Daily volatility and liquidity

Daily volatility can be affected by liquidity.

Illiquid assets may show unstable or unreliable price movements.

Example:

```text
Low volume
Wide bid-ask spread
Few trades
Large price jumps
```

These conditions can increase measured volatility.

However, the volatility may partly reflect poor trading conditions rather than true economic risk.

This is why Athena should analyze volatility together with volume and bid-ask spread when possible.

---

### Daily volatility and return type

Daily volatility can be calculated using different return types.

Common choices:

```text
Simple daily returns
Log daily returns
```

For many daily return series, the results are similar.

But the method should be documented.

Example:

```text
Daily volatility calculated from simple returns.
```

or:

```text
Daily volatility calculated from log returns.
```

Athena should always record the return type used.

---

### Daily volatility data needed in Athena

To calculate daily volatility, Athena needs:

```text
Asset identifier
Clean daily price series
Daily return series
Return type
Date range
Volatility window
Price field used
Currency
Data source
```

Example:

```text
symbol: AAPL
price_field_used: adjusted_close
return_type: simple_return
frequency: daily
window: 252 trading days
```

This makes the volatility result transparent and reproducible.

---

### Daily volatility in Athena

Athena can use daily volatility to support:

```text
Asset risk analysis
Short-term risk monitoring
Volatility comparison
Rolling volatility charts
Market stress detection
Portfolio risk inputs
Benchmark risk comparison
```

Example output:

```text
Asset: AAPL
Daily volatility: 1.20%
Window: 252 daily returns
Return type: simple return
Price field: adjusted close
Data frequency: daily
```

This output is much clearer than simply displaying:

```text
Volatility = 1.20%
```

because it explains exactly what the number means.

---

### Daily volatility label

A daily volatility number should always be labeled clearly.

Bad label:

```text
Volatility = 1.20%
```

Better label:

```text
Daily volatility = 1.20%
Window = 252 trading days
Return type = simple returns
Price field = adjusted close
```

This prevents confusion between daily volatility and annualized volatility.

---

### Common beginner mistakes

Common mistakes include:

```text
Calculating volatility from prices instead of returns
Confusing daily volatility with annualized volatility
Multiplying daily volatility by 252 instead of sqrt(252)
Using too few daily returns
Ignoring missing data
Ignoring outliers
Ignoring corporate actions
Forgetting to label the time window
Comparing volatility numbers with different frequencies
```

Example mistake:

```text
Asset A daily volatility = 1%
Asset B annualized volatility = 15%
```

These are not directly comparable because they use different time horizons.

---

### CFA Level 1 takeaway

For CFA Level 1, daily volatility is important because it introduces volatility as the standard deviation of daily returns.

Important concepts include:

```text
Daily returns
Standard deviation
Dispersion
Short-term risk
Annualization
Square-root-of-time rule
Volatility window
```

The core formula is:

```text
Daily volatility = standard_deviation(daily_returns)
```

A simple memory rule:

```text
Daily volatility tells how unstable returns are from day to day.
```

---

### Athena implementation takeaway

For Athena, daily volatility should be calculated from validated daily returns.

The volatility module should support:

```text
Daily return calculation
Daily volatility calculation
Window selection
Simple return or log return selection
Adjusted close usage
Annualized volatility conversion
Rolling daily volatility
Clear methodology labels
Data quality warnings
```

Athena should make sure users understand whether a volatility number is daily or annualized.

---

### Mini revision questions

1. What does daily volatility measure?

2. What is the usual formula for daily volatility?

3. Why is daily volatility calculated from returns instead of prices?

4. What does daily volatility of 1% mean?

5. How do you convert daily volatility into annualized volatility?

6. Why is daily volatility multiplied by sqrt(252), not 252?

7. Why does the volatility window matter?

8. Why should Athena label daily volatility clearly?

---

### Mini answers

1. Daily volatility measures how much daily returns fluctuate.

2. The usual formula is: daily volatility = standard deviation of daily returns.

3. It is calculated from returns because returns measure percentage movements and make assets comparable.

4. It means daily returns typically move around their average by about 1%, under a simplified interpretation.

5. Use: annualized volatility = daily volatility × sqrt(252).

6. Because volatility is based on standard deviation, and standard deviation scales with the square root of time.

7. The window matters because a 20-day volatility and a 252-day volatility can describe different market conditions.

8. Athena should label it clearly to avoid confusion with annualized volatility or volatility calculated using another method.

---

### Section summary

Daily volatility measures the instability of daily returns.

It is calculated as the standard deviation of daily returns and is often used as the building block for annualized volatility.

For CFA Level 1, daily volatility is important because it connects daily returns, standard deviation, risk and annualization.

For Athena AI Risk Terminal, daily volatility is useful for asset risk analysis, rolling volatility charts and short-term risk monitoring.

The key lesson is:

```text
Daily volatility measures how much an asset typically moves from day to day.
It must be calculated from clean daily returns and clearly labeled.
```
---










## 22. Annualized volatility

Annualized volatility converts periodic volatility into a yearly measure.

When volatility is calculated from daily returns, it is called daily volatility.  
When it is converted to a yearly scale, it is called annualized volatility.

Simple idea:

```text
Daily volatility = short-term return instability
Annualized volatility = yearly equivalent volatility
```

Annualized volatility is useful because it allows investors to compare assets using the same time horizon.

---

### Formula

For daily volatility, the standard formula is:

```text
Annualized volatility = Daily volatility × sqrt(252)
```

Where:

```text
252 = approximate number of trading days in one year
sqrt(252) ≈ 15.87
```

So the formula can also be written as:

```text
Annualized volatility = Daily volatility × 15.87
```

---

### Why 252?

Financial markets are not open every day.

A calendar year has about:

```text
365 calendar days
```

But stock markets are usually open around:

```text
252 trading days per year
```

Weekends and market holidays are excluded.

That is why daily market volatility is usually annualized using:

```text
sqrt(252)
```

---

### Example

Suppose an asset has:

```text
Daily volatility = 1%
```

Annualized volatility:

```text
Annualized volatility = 1% × sqrt(252)
Annualized volatility = 1% × 15.87
Annualized volatility ≈ 15.87%
```

This means the asset has an estimated yearly volatility of approximately:

```text
15.87%
```

---

### Interpretation

If an asset has:

```text
Annualized volatility = 20%
```

A simplified interpretation is:

```text
The asset’s yearly returns have historically fluctuated around their average by about 20%.
```

This does not mean the asset will lose 20%.

It also does not mean the asset will move exactly 20% every year.

It means the asset has a yearly risk estimate based on the dispersion of returns.

Simple idea:

```text
Annualized volatility measures yearly uncertainty, not guaranteed loss.
```

---

### Why annualized volatility matters

Annualized volatility matters because it makes risk comparisons easier.

Daily volatility numbers are useful, but they are not always intuitive for investors.

Example:

```text
Asset A daily volatility = 0.75%
Asset B daily volatility = 2.00%
```

These numbers can be compared, but annualized volatility is easier to understand in portfolio and risk reports.

Annualized:

```text
Asset A annualized volatility = 0.75% × sqrt(252) ≈ 11.91%
Asset B annualized volatility = 2.00% × sqrt(252) ≈ 31.75%
```

Now the risk difference is clearer.

Asset B is much more volatile on a yearly scale.

---

### Comparing assets

Annualized volatility allows analysts to compare different assets on the same basis.

Example:

```text
Asset A annualized volatility = 12%
Asset B annualized volatility = 35%
```

Asset B is more volatile.

This means Asset B has historically shown larger return fluctuations than Asset A.

However, higher volatility does not automatically mean a better or worse investment.

The investor must compare volatility with expected return.

Example:

```text
Asset A:
Expected return = 8%
Annualized volatility = 12%

Asset B:
Expected return = 8%
Annualized volatility = 35%
```

Both assets have the same expected return, but Asset B has much higher risk.

Asset B may be less attractive if it does not compensate the investor for the extra volatility.

---

### Annualized volatility vs annualized return

Annualized volatility and annualized return are not calculated the same way.

Annualized return uses compounding.

Example:

```text
Annualized return = (Ending value / Beginning value)^(1 / years) - 1
```

Annualized volatility uses the square-root-of-time rule.

Example:

```text
Annualized volatility = Daily volatility × sqrt(252)
```

Simple comparison:

```text
Returns compound over time.
Volatility scales with the square root of time.
```

This is one of the most important distinctions in market risk analysis.

---

### Why volatility uses the square root of time

Volatility is based on standard deviation.

Standard deviation is the square root of variance.

Under simplifying assumptions, variance increases proportionally with time.

Simple logic:

```text
Daily variance × 252 = annual variance
```

Because volatility is the square root of variance:

```text
Annualized volatility = sqrt(daily variance × 252)
```

This becomes:

```text
Annualized volatility = Daily volatility × sqrt(252)
```

This rule assumes that daily returns are independent and have stable variance.

In real markets, this assumption is not perfect, but it is widely used in finance.

---

### Annualization factors

The annualization factor depends on the data frequency.

Common examples:

```text
Daily volatility    → multiply by sqrt(252)
Weekly volatility   → multiply by sqrt(52)
Monthly volatility  → multiply by sqrt(12)
Quarterly volatility → multiply by sqrt(4)
```

Example:

```text
Monthly volatility = 4%
```

Annualized volatility:

```text
Annualized volatility = 4% × sqrt(12)
Annualized volatility ≈ 13.86%
```

Athena must know the data frequency before annualizing volatility.

---

### Common mistake

A common beginner mistake is to multiply daily volatility by 252.

Wrong:

```text
Annualized volatility = Daily volatility × 252
```

Correct:

```text
Annualized volatility = Daily volatility × sqrt(252)
```

Example:

```text
Daily volatility = 1%
```

Wrong calculation:

```text
1% × 252 = 252%
```

Correct calculation:

```text
1% × sqrt(252) ≈ 15.87%
```

The wrong result massively overstates volatility.

---

### Annualized volatility and risk comparison

Annualized volatility is commonly used in professional finance because it puts risk on a standard yearly scale.

It helps compare:

```text
Stocks
ETFs
Indices
Portfolios
Funds
Strategies
Benchmarks
```

Example:

```text
Portfolio annualized volatility = 14%
Benchmark annualized volatility = 18%
```

The portfolio has been less volatile than the benchmark.

This may be positive if the portfolio also achieved competitive returns.

---

### Annualized volatility and portfolio analysis

Annualized volatility is useful for portfolio risk analysis.

Example:

```text
Portfolio A:
Annualized return = 9%
Annualized volatility = 10%

Portfolio B:
Annualized return = 9%
Annualized volatility = 25%
```

Both portfolios have the same annualized return.

But Portfolio A achieved the return with less volatility.

This makes Portfolio A more attractive from a risk-adjusted perspective.

This logic prepares later metrics such as:

```text
Sharpe ratio
Information ratio
Risk-adjusted return
```

---

### Annualized volatility and investment style

Different investments usually have different volatility levels.

General examples:

```text
Money market instruments: low volatility
Government bonds: low to moderate volatility
Large-cap equity indices: moderate volatility
Single stocks: moderate to high volatility
Small-cap stocks: higher volatility
Commodities: often high volatility
Leveraged ETFs: very high volatility
Crypto assets: very high volatility
```

These are general tendencies, not fixed rules.

Volatility can change over time depending on market conditions.

---

### Annualized volatility and market regimes

Annualized volatility can change significantly across market regimes.

Example:

```text
Calm market:
Annualized volatility = 10%

Stress market:
Annualized volatility = 35%
```

This means the asset became much more unstable during the stress period.

For Athena, comparing volatility across time can help identify changes in market conditions.

---

### Annualized volatility and rolling windows

Annualized volatility is often calculated over rolling windows.

Common windows:

```text
20 trading days
60 trading days
252 trading days
```

Example:

```text
20-day annualized volatility = short-term risk estimate
60-day annualized volatility = medium-term risk estimate
252-day annualized volatility = one-year risk estimate
```

A rolling annualized volatility chart can show whether risk is rising or falling over time.

---

### Annualized volatility and sample size

Annualized volatility is more reliable when calculated from enough data.

Example:

```text
Volatility based on 5 daily returns = weak estimate
Volatility based on 252 daily returns = more stable estimate
```

A very short sample can be misleading.

Example:

```text
A stock had three calm days.
This does not prove that the stock is low-risk.
```

Athena should display the number of observations used in the calculation.

---

### Annualized volatility and assumptions

The square-root-of-time rule relies on simplifying assumptions.

Important assumptions include:

```text
Returns are independent
Return variance is stable
The return distribution does not change dramatically
There are no major structural breaks
```

In real markets, these assumptions can fail.

Examples:

```text
Volatility clustering
Market crises
Liquidity shocks
Earnings announcements
Regime changes
```

This does not make annualized volatility useless.

It means the result should be interpreted as an estimate, not as a certainty.

---

### Annualized volatility in Athena

Athena should calculate annualized volatility from a clean return series.

Basic workflow:

```text
Clean price series
      ↓
Daily returns
      ↓
Daily volatility
      ↓
Annualized volatility
```

Example output:

```text
Asset: AAPL
Return type: simple return
Price field: adjusted close
Window: 252 trading days
Daily volatility: 1.20%
Annualized volatility: 19.05%
Annualization factor: sqrt(252)
```

This is clear because the user can see:

```text
What data was used
What window was used
What formula was used
Whether the result is daily or annualized
```

---

### Data needed in Athena

To calculate annualized volatility, Athena needs:

```text
Asset identifier
Clean price series
Return series
Return type
Data frequency
Volatility window
Annualization factor
Start date
End date
Currency
Price field used
```

Example:

```text
symbol: SPY
return_type: simple_return
price_field_used: adjusted_close
frequency: daily
window: 252
annualization_factor: sqrt(252)
```

Without the frequency, Athena cannot annualize correctly.

---

### Common beginner mistakes

Common mistakes include:

```text
Multiplying daily volatility by 252
Comparing daily volatility with annualized volatility
Ignoring the data frequency
Using the wrong annualization factor
Using too few observations
Assuming annualized volatility is a guaranteed future outcome
Confusing volatility with loss
Forgetting to mention the calculation window
```

Example of unclear output:

```text
Volatility = 18%
```

Better output:

```text
Annualized volatility = 18%
Window = 252 daily returns
Annualization factor = sqrt(252)
Return type = simple return
Price field = adjusted close
```

---

### CFA Level 1 takeaway

For CFA Level 1, annualized volatility is important because it standardizes risk over a yearly horizon.

Important concepts include:

```text
Daily volatility
Annualized volatility
Standard deviation
Square-root-of-time rule
Trading days
Risk comparison
Data frequency
Volatility estimation
```

The key formula is:

```text
Annualized volatility = Daily volatility × sqrt(252)
```

A simple memory rule:

```text
Daily volatility becomes annualized volatility by multiplying by the square root of the number of trading periods in a year.
```

---

### Athena implementation takeaway

For Athena, annualized volatility should be one of the core risk metrics.

The volatility module should support:

```text
Daily volatility calculation
Annualized volatility calculation
Frequency-aware annualization
Window selection
Rolling annualized volatility
Benchmark volatility comparison
Portfolio volatility extension
Clear methodology labels
Warnings for short samples
```

Athena should always make the annualization method transparent.

The user should know whether the number is daily, weekly, monthly or annualized.

---

### Mini revision questions

1. What does annualized volatility measure?

2. How do you annualize daily volatility?

3. Why do we use 252 for daily market data?

4. Why do we multiply by sqrt(252) instead of 252?

5. What is the annualized volatility if daily volatility is 1%?

6. Why is annualized volatility useful for comparing assets?

7. Why does Athena need to know the data frequency?

8. Why should annualized volatility be interpreted as an estimate?

---

### Mini answers

1. Annualized volatility measures return instability expressed on a yearly scale.

2. Use: annualized volatility = daily volatility × sqrt(252).

3. Because there are approximately 252 trading days in a year.

4. Because volatility is based on standard deviation, and standard deviation scales with the square root of time.

5. Approximately 15.87%.

6. It puts assets on the same yearly risk scale.

7. Athena needs the data frequency to choose the correct annualization factor.

8. It is an estimate because it relies on assumptions that may not always hold in real markets.

---

### Section summary

Annualized volatility converts periodic volatility into a yearly risk measure.

For daily data, the standard formula is:

```text
Annualized volatility = Daily volatility × sqrt(252)
```

For CFA Level 1, this section is important because it explains how risk is standardized across time horizons.

For Athena AI Risk Terminal, annualized volatility is essential for comparing assets, portfolios and benchmarks on the same risk scale.

The key lesson is:

```text
Returns annualize through compounding.
Volatility annualizes through the square-root-of-time rule.
```

---



















## 23. Rolling volatility

Rolling volatility measures how volatility changes over time.

It is calculated over a moving window of returns.

Simple idea:

```text
Rolling volatility = volatility calculated repeatedly through time
```

Instead of calculating one volatility number for the whole period, rolling volatility calculates many volatility values.

Each value uses the most recent observations in the chosen window.

Common windows include:

```text
20 trading days
60 trading days
252 trading days
```

---

### Why rolling volatility matters

Volatility is not constant.

An asset can be calm during one period and unstable during another period.

Example:

```text
Normal market period:
Returns are small and stable.

Stress market period:
Returns become large and unpredictable.
```

Rolling volatility helps detect these changes.

It answers questions such as:

```text
Is the asset becoming more volatile?
Is the asset becoming calmer?
Did market risk increase recently?
Is current volatility higher than normal?
```

This makes rolling volatility useful for risk monitoring.

---

### How rolling volatility works

A rolling volatility calculation uses a fixed window.

Example:

```text
20-day rolling volatility
```

This means Athena uses the most recent 20 daily returns to calculate volatility.

Then the window moves forward by one day.

Example:

```text
First calculation:
Day 1 to Day 20

Second calculation:
Day 2 to Day 21

Third calculation:
Day 3 to Day 22
```

Each window produces one volatility value.

The result is a time series of volatility values.

---

### Simple example

Suppose Athena calculates 5-day rolling volatility.

```text
Day 1 return
Day 2 return
Day 3 return
Day 4 return
Day 5 return
```

These five returns produce the first volatility estimate.

Then the window moves forward:

```text
Day 2 return
Day 3 return
Day 4 return
Day 5 return
Day 6 return
```

This produces the second volatility estimate.

The calculation continues through the dataset.

Simple idea:

```text
Old observation leaves the window.
New observation enters the window.
Volatility is recalculated.
```

---

### Rolling window

A rolling window is the number of observations used in each calculation.

Examples:

```text
20-day window = uses 20 daily returns
60-day window = uses 60 daily returns
252-day window = uses 252 daily returns
```

The choice of window affects the result.

A short window reacts quickly.

A long window reacts more slowly.

---

### 20-day rolling volatility

A 20-day rolling volatility is a short-term volatility measure.

It uses approximately one month of trading days.

Simple interpretation:

```text
20-day rolling volatility = recent short-term risk
```

It is useful for detecting sudden changes in market conditions.

Example:

```text
20-day rolling volatility rises sharply after earnings news.
```

Because the window is short, it reacts quickly to recent shocks.

However, it can also be noisy.

---

### 60-day rolling volatility

A 60-day rolling volatility is a medium-term volatility measure.

It uses approximately three months of trading days.

Simple interpretation:

```text
60-day rolling volatility = medium-term risk
```

It is less noisy than a 20-day window but still reacts to changing conditions.

It can be useful for monitoring quarterly risk trends.

---

### 252-day rolling volatility

A 252-day rolling volatility is a longer-term volatility measure.

It uses approximately one year of trading days.

Simple interpretation:

```text
252-day rolling volatility = one-year historical risk
```

It is more stable than shorter windows.

However, it reacts more slowly to recent changes.

Example:

```text
A market shock may quickly affect 20-day volatility,
but 252-day volatility may rise more gradually.
```

---

### Short window vs long window

The window length creates a tradeoff.

Short windows are more responsive.

Long windows are more stable.

Simple comparison:

```text
Short window:
Reacts quickly but can be noisy.

Long window:
More stable but reacts slowly.
```

Example:

```text
20-day volatility = good for recent stress detection
252-day volatility = good for long-term risk context
```

Athena can show multiple windows to give a more complete view.

---

### Rolling volatility and annualization

Rolling volatility is often annualized.

For daily returns, the process is:

```text
1. Calculate standard deviation inside the rolling window.
2. Multiply by sqrt(252).
```

Formula:

```text
Rolling annualized volatility = rolling daily volatility × sqrt(252)
```

Example:

```text
20-day daily rolling volatility = 1.50%
```

Annualized:

```text
20-day annualized rolling volatility = 1.50% × sqrt(252)
20-day annualized rolling volatility ≈ 23.81%
```

The result should be labeled clearly.

Example:

```text
20-day annualized rolling volatility
```

This tells the user both the window and the annualization status.

---

### Rolling volatility chart

Rolling volatility is often displayed as a line chart.

The chart shows how risk changes through time.

Example interpretation:

```text
Rising rolling volatility = risk is increasing
Falling rolling volatility = risk is decreasing
Stable rolling volatility = risk is relatively steady
```

A rolling volatility chart can help identify:

```text
Market stress periods
Volatility spikes
Calm periods
Risk regime changes
Post-crisis normalization
```

This is very useful for Athena’s frontend.

---

### Volatility spike

A volatility spike happens when rolling volatility rises sharply.

Example:

```text
20-day annualized volatility moves from 12% to 35%
```

This may happen because of:

```text
Earnings shock
Interest rate surprise
Inflation surprise
Geopolitical event
Liquidity crisis
Market crash
Company-specific news
```

A volatility spike is not automatically bad, but it tells the user that the asset has become more unstable.

Athena can flag volatility spikes as risk warnings.

---

### Volatility regime

A volatility regime describes the general level of market volatility.

Common regimes:

```text
Low volatility regime
Normal volatility regime
High volatility regime
Crisis volatility regime
```

Rolling volatility helps identify these regimes.

Example:

```text
Annualized rolling volatility below 10% = low volatility
Annualized rolling volatility around 15% to 25% = normal or moderate
Annualized rolling volatility above 30% = high
```

The exact thresholds depend on the asset class.

A 30% volatility may be high for a broad equity index, but more normal for a single high-growth stock.

---

### Rolling volatility and asset comparison

Rolling volatility can compare risk across assets through time.

Example:

```text
Asset A 20-day volatility = 15%
Asset B 20-day volatility = 35%
```

Asset B is more volatile over the recent window.

But this comparison should use the same methodology:

```text
Same return type
Same window
Same frequency
Same annualization method
Same date range
```

Otherwise, the comparison may be misleading.

---

### Rolling volatility and benchmark comparison

Rolling volatility is useful for comparing an asset or portfolio against a benchmark.

Example:

```text
Portfolio 60-day volatility = 14%
Benchmark 60-day volatility = 18%
```

The portfolio was less volatile than its benchmark over the same rolling window.

Another example:

```text
Portfolio 60-day volatility = 25%
Benchmark 60-day volatility = 18%
```

The portfolio was more volatile than its benchmark.

This helps evaluate whether the portfolio is taking more or less risk than the reference market.

---

### Rolling volatility and risk monitoring

Rolling volatility is useful for monitoring risk limits.

Example:

```text
Risk limit:
Portfolio annualized volatility should stay below 20%.
```

Athena can calculate rolling volatility and warn the user if the limit is breached.

Example warning:

```text
Portfolio 60-day annualized volatility increased to 24%.
Risk limit exceeded.
```

This makes rolling volatility useful for middle-office and risk management workflows.

---

### Rolling volatility and market stress

Rolling volatility often rises during market stress.

Example:

```text
Before stress:
20-day annualized volatility = 12%

During stress:
20-day annualized volatility = 45%
```

This tells the user that daily returns have become much more unstable.

Rolling volatility can therefore act as an early warning signal.

However, it is still based on historical returns.

It shows what has happened recently, not what will happen with certainty.

---

### Rolling volatility and lag

Rolling volatility can lag behind sudden events.

Because it uses historical observations, it may take time to fully reflect a new risk regime.

Example:

```text
A major market shock happens today.
The rolling window still contains many calm days from before the shock.
```

The volatility estimate may rise gradually as more high-volatility days enter the window.

This is especially true for long windows such as 252 days.

Simple idea:

```text
Rolling volatility reacts with a delay,
especially when the window is long.
```

---

### Rolling volatility and window choice

The correct window depends on the analysis goal.

Example:

```text
Short-term trader:
May prefer 20-day volatility.

Portfolio manager:
May prefer 60-day or 252-day volatility.

Risk manager:
May monitor several windows at once.
```

A good Athena dashboard can show:

```text
20-day rolling volatility
60-day rolling volatility
252-day rolling volatility
```

This gives the user short-term, medium-term and long-term views of risk.

---

### Rolling volatility and data quality

Rolling volatility is sensitive to data quality problems.

Possible issues include:

```text
Missing prices
Wrong prices
Duplicate dates
Outliers
Unadjusted corporate actions
Incorrect return calculations
Wrong frequency
```

Example:

```text
A stock split is not adjusted correctly.
```

This can create a false extreme return.

That false return can produce a large artificial volatility spike.

Athena should validate price and return data before calculating rolling volatility.

---

### Rolling volatility data needed in Athena

To calculate rolling volatility, Athena needs:

```text
Asset identifier
Clean price series
Return series
Return type
Rolling window size
Data frequency
Annualization factor
Start date
End date
Price field used
Currency
```

Example:

```text
symbol: AAPL
return_type: simple_return
price_field_used: adjusted_close
frequency: daily
window: 20 trading days
annualization_factor: sqrt(252)
```

The output should make the methodology clear.

---

### Rolling volatility in Athena

Athena can use rolling volatility to support:

```text
Risk monitoring
Market regime detection
Volatility charts
Portfolio risk dashboards
Benchmark risk comparison
Volatility spike warnings
Risk limit monitoring
Stress period analysis
```

Example output:

```text
Asset: AAPL
Window: 20 trading days
Return type: simple return
Price field: adjusted close
Annualized rolling volatility today: 24.50%
Previous value: 18.20%
Change: +6.30 percentage points
```

This helps the user understand not only the current volatility level, but also how it changed.

---

### Frontend display idea

A useful Athena frontend component could be:

```text
RollingVolatilityChart
```

It could display:

```text
20-day annualized volatility
60-day annualized volatility
252-day annualized volatility
Benchmark rolling volatility
Volatility spike markers
```

Possible user insight:

```text
The asset’s short-term volatility is rising faster than its long-term volatility.
```

This can indicate a recent increase in market uncertainty.

---

### Common beginner mistakes

Common mistakes include:

```text
Forgetting to specify the rolling window
Comparing different window lengths directly
Mixing daily and monthly volatility
Forgetting to annualize when comparing yearly risk
Using too few observations
Ignoring data quality problems
Assuming rolling volatility predicts the future perfectly
Confusing rolling volatility with realized future volatility
```

Example of unclear output:

```text
Rolling volatility = 22%
```

Better output:

```text
20-day annualized rolling volatility = 22%
Return type = simple return
Price field = adjusted close
Frequency = daily
```

---

### CFA Level 1 takeaway

For CFA Level 1, rolling volatility is useful because it shows that risk is not constant over time.

Important concepts include:

```text
Moving window
Volatility window
Historical volatility
Annualized volatility
Short-term risk
Medium-term risk
Long-term risk
Market regimes
Risk monitoring
```

A simple memory rule:

```text
Rolling volatility shows how volatility evolves through time.
```

---

### Athena implementation takeaway

For Athena, rolling volatility should be a core chart-based risk metric.

The volatility module should support:

```text
Rolling window selection
20-day rolling volatility
60-day rolling volatility
252-day rolling volatility
Annualized rolling volatility
Benchmark comparison
Volatility spike detection
Risk warnings
Clear methodology labels
```

Athena should make volatility dynamic, not static.

The user should be able to see whether risk is rising, falling or stable.

---

### Mini revision questions

1. What is rolling volatility?

2. What does a 20-day rolling volatility use?

3. Why is rolling volatility useful?

4. What is the difference between a short window and a long window?

5. Why is rolling volatility often annualized?

6. Why can rolling volatility lag behind sudden market events?

7. Why should Athena show the window used?

8. What can a volatility spike indicate?

---

### Mini answers

1. Rolling volatility is volatility calculated repeatedly over a moving window of returns.

2. It uses the most recent 20 daily returns.

3. It is useful because volatility changes over time and rolling volatility helps detect changing risk conditions.

4. A short window reacts quickly but is noisy. A long window is more stable but reacts slowly.

5. It is annualized to express risk on a common yearly scale.

6. It can lag because the window still contains older observations from before the event.

7. Athena should show the window because 20-day, 60-day and 252-day volatility have different meanings.

8. A volatility spike can indicate a sudden increase in market uncertainty, stress or abnormal price movement.

---

### Section summary

Rolling volatility measures how volatility changes over time.

It is calculated over a moving window, such as 20, 60 or 252 trading days.

For CFA Level 1, rolling volatility helps reinforce that risk is dynamic and can change across market regimes.

For Athena AI Risk Terminal, rolling volatility is useful for risk monitoring, volatility charts, benchmark comparison and stress detection.

The key lesson is:

```text
Rolling volatility turns volatility from one static number into a time series of changing risk.
```

---
















## 24. Realized volatility

Realized volatility is volatility calculated from historical returns.

It answers the question:

```text
How volatile was the asset in the past?
```

Realized volatility is backward-looking because it uses returns that have already happened.

Simple idea:

```text
Realized volatility = observed historical volatility
```

It does not predict the future with certainty.  
It measures how much the asset actually moved over a past period.

---

### Why realized volatility matters

Realized volatility matters because it gives a concrete measure of past market risk.

It is based on observed price behavior, not forecasts.

It helps answer questions such as:

```text
How unstable was this asset recently?
Was the asset more volatile this month than last month?
Did volatility increase during a market stress period?
How risky was this asset compared with its benchmark?
```

For Athena AI Risk Terminal, realized volatility is useful because it is transparent, testable and easy to explain.

---

### Basic calculation logic

Realized volatility is usually calculated in three steps:

```text
1. Collect historical prices
2. Convert prices into returns
3. Calculate the standard deviation of returns
```

Basic workflow:

```text
Historical prices
      ↓
Historical returns
      ↓
Standard deviation
      ↓
Realized volatility
```

If the volatility is annualized, an additional step is added:

```text
Daily realized volatility × sqrt(252)
```

---

### Simple example

Suppose Athena has the following prices:

```text
Date        Price
Day 0       100
Day 1       102
Day 2       101
Day 3       105
```

First, calculate daily returns:

```text
Day 1 return = 102 / 100 - 1 = 2.00%
Day 2 return = 101 / 102 - 1 ≈ -0.98%
Day 3 return = 105 / 101 - 1 ≈ 3.96%
```

Then calculate the standard deviation of these returns.

That standard deviation is the realized volatility over the selected period.

---

### Realized volatility is backward-looking

Realized volatility only uses past data.

Example:

```text
20-day realized volatility
```

means:

```text
Volatility calculated using the last 20 daily returns.
```

It tells us what happened during those 20 days.

It does not guarantee that the next 20 days will have the same volatility.

Simple distinction:

```text
Realized volatility = what happened
Expected volatility = what may happen
```

---

### Common realized volatility windows

Realized volatility can be calculated over different windows.

Common examples:

```text
20-day realized volatility
60-day realized volatility
252-day realized volatility
```

Each window has a different interpretation.

```text
20-day realized volatility = recent short-term volatility
60-day realized volatility = medium-term volatility
252-day realized volatility = one-year historical volatility
```

The window should always be shown clearly.

---

### 20-day realized volatility

A 20-day realized volatility uses approximately one month of daily returns.

It is useful for short-term risk analysis.

Example:

```text
20-day realized volatility increased from 12% to 28%.
```

This may indicate that the asset has recently become much more unstable.

Because the window is short, the measure reacts quickly to recent market shocks.

However, it can also be noisy.

---

### 60-day realized volatility

A 60-day realized volatility uses approximately three months of daily returns.

It is useful for medium-term risk analysis.

It is less noisy than a 20-day measure, but it still reacts to changing market conditions.

Example:

```text
60-day realized volatility = 18%
```

This gives a broader view of recent risk than the 20-day measure.

---

### 252-day realized volatility

A 252-day realized volatility uses approximately one year of daily returns.

It is useful for long-term historical risk analysis.

Example:

```text
252-day realized volatility = 22%
```

This means the asset’s volatility over the last year was approximately 22% on an annualized basis, if the result is annualized.

A 252-day window is more stable, but it reacts slowly to recent shocks.

---

### Realized volatility vs rolling volatility

Realized volatility and rolling volatility are closely related.

Realized volatility is a volatility estimate calculated from historical returns.

Rolling volatility is realized volatility calculated repeatedly through time.

Simple comparison:

```text
Realized volatility = one historical volatility estimate
Rolling volatility = a time series of historical volatility estimates
```

Example:

```text
252-day realized volatility today = one number
252-day rolling volatility = one number for each date over time
```

In Athena, rolling volatility can be built from repeated realized volatility calculations.

---

### Realized volatility vs implied volatility

Realized volatility is calculated from historical returns.

Implied volatility is extracted from option prices.

Simple comparison:

```text
Realized volatility = based on past price movements
Implied volatility = based on option market expectations
```

Realized volatility answers:

```text
How volatile was the asset?
```

Implied volatility answers:

```text
How volatile does the options market expect the asset to be?
```

For Athena’s first version, realized volatility is easier to implement because it only requires historical prices.

Implied volatility can be added later in the derivatives module.

---

### Realized volatility and annualization

Realized volatility is often annualized.

If realized volatility is calculated from daily returns, the formula is:

```text
Annualized realized volatility = Daily realized volatility × sqrt(252)
```

Example:

```text
Daily realized volatility = 1.20%
```

Annualized:

```text
Annualized realized volatility = 1.20% × sqrt(252)
Annualized realized volatility ≈ 19.05%
```

The result should be labeled clearly:

```text
252-day annualized realized volatility = 19.05%
```

This tells the user the window and the annualization method.

---

### Realized volatility and asset comparison

Realized volatility can compare the historical risk of different assets.

Example:

```text
Asset A realized volatility = 15%
Asset B realized volatility = 35%
```

Asset B was more volatile over the selected period.

However, the comparison is only valid if both calculations use the same methodology:

```text
Same return type
Same window
Same frequency
Same annualization method
Same date range
```

Otherwise, the comparison can be misleading.

---

### Realized volatility and benchmark comparison

Realized volatility is useful for comparing an asset or portfolio with a benchmark.

Example:

```text
Portfolio realized volatility = 14%
Benchmark realized volatility = 20%
```

The portfolio was less volatile than the benchmark.

Another example:

```text
Portfolio realized volatility = 28%
Benchmark realized volatility = 18%
```

The portfolio was more volatile than the benchmark.

This helps evaluate whether the portfolio took more or less risk than the reference market.

---

### Realized volatility and market regimes

Realized volatility can help identify market regimes.

Examples:

```text
Low realized volatility = calm market
High realized volatility = stressed market
Rising realized volatility = risk increasing
Falling realized volatility = risk decreasing
```

Example:

```text
20-day realized volatility = 45%
252-day realized volatility = 18%
```

This may suggest that the asset has recently entered a much more volatile period.

Athena can use this comparison to detect short-term stress.

---

### Realized volatility is not a perfect forecast

Realized volatility is useful, but it has limitations.

It is based on the past.

The future may be different.

Example:

```text
An asset had low volatility for the last 252 days.
Tomorrow, unexpected news causes a large price move.
```

The historical realized volatility did not predict that shock.

Simple idea:

```text
Realized volatility is evidence from the past, not a guarantee about the future.
```

---

### Realized volatility and sample size

The reliability of realized volatility depends on the number of observations.

Example:

```text
5 daily returns = weak estimate
20 daily returns = short-term estimate
252 daily returns = more stable estimate
```

A very short window may react quickly, but it can be noisy.

A long window is more stable, but it may hide recent changes.

Athena should show the number of observations used.

---

### Realized volatility and data quality

Realized volatility is very sensitive to bad data.

Possible issues include:

```text
Missing prices
Duplicate dates
Wrong prices
Unadjusted stock splits
Outliers
Stale prices
Wrong currency
Incorrect return calculation
```

Example:

```text
A stock split is not adjusted correctly.
```

This may create a false extreme return.

That false return can artificially increase realized volatility.

Athena should validate price data before calculating realized volatility.

---

### Realized volatility data needed in Athena

To calculate realized volatility, Athena needs:

```text
Asset identifier
Clean historical price series
Return series
Return type
Start date
End date
Window size
Data frequency
Annualization factor
Price field used
Currency
Data source
```

Example:

```text
symbol: AAPL
price_field_used: adjusted_close
return_type: simple_return
frequency: daily
window: 252 trading days
annualization_factor: sqrt(252)
```

This makes the calculation reproducible and transparent.

---

### Realized volatility in Athena

Athena can use realized volatility to support:

```text
Asset risk analysis
Portfolio risk analysis
Benchmark comparison
Volatility regime detection
Risk dashboards
Historical risk reports
Stress period comparison
```

Example output:

```text
Asset: AAPL
Window: 252 trading days
Return type: simple return
Price field: adjusted close
Daily realized volatility: 1.20%
Annualized realized volatility: 19.05%
```

This is useful because it explains both the result and the methodology.

---

### Realized volatility labels in Athena

Athena should avoid unclear labels.

Bad label:

```text
Volatility = 19%
```

Better label:

```text
252-day annualized realized volatility = 19%
Return type = simple return
Price field = adjusted close
Frequency = daily
Annualization factor = sqrt(252)
```

This makes the result professional and easier to trust.

---

### Common beginner mistakes

Common mistakes include:

```text
Thinking realized volatility predicts the future perfectly
Using prices instead of returns
Forgetting to annualize
Using the wrong annualization factor
Comparing different windows
Ignoring data quality problems
Using too few observations
Confusing realized volatility with implied volatility
Confusing volatility with loss
```

Example mistake:

```text
Realized volatility was low last year,
so the asset cannot be risky this year.
```

This is wrong.

Past volatility can inform risk analysis, but it does not eliminate future uncertainty.

---

### CFA Level 1 takeaway

For CFA Level 1, realized volatility is important because it connects historical returns, standard deviation and risk measurement.

Important concepts include:

```text
Historical returns
Observed volatility
Backward-looking risk
Standard deviation
Volatility window
Annualization
Comparison with expected or implied volatility
```

A simple memory rule:

```text
Realized volatility measures how much the asset actually moved in the past.
```

---

### Athena implementation takeaway

For Athena, realized volatility should be one of the first volatility metrics implemented.

The volatility module should support:

```text
Historical return calculation
Daily realized volatility
Annualized realized volatility
Window selection
Benchmark comparison
Portfolio realized volatility
Data quality checks
Clear methodology labels
```

Realized volatility is valuable because it is simple, transparent and easy to test.

It can become the foundation for more advanced risk metrics later.

---

### Mini revision questions

1. What is realized volatility?

2. Is realized volatility backward-looking or forward-looking?

3. What data is needed to calculate realized volatility?

4. What does 20-day realized volatility mean?

5. What is the difference between realized volatility and implied volatility?

6. Why is realized volatility useful in Athena?

7. Why can bad price data distort realized volatility?

8. Why should Athena show the window used?

---

### Mini answers

1. Realized volatility is volatility calculated from historical returns.

2. It is backward-looking because it uses past data.

3. It needs a clean historical price series and a return series.

4. It means volatility calculated using the most recent 20 daily returns.

5. Realized volatility is based on past returns, while implied volatility is extracted from option prices and reflects market expectations.

6. It is useful because it provides a simple, transparent and testable measure of historical risk.

7. Bad price data can create false returns, which can artificially increase or decrease volatility.

8. Athena should show the window because 20-day, 60-day and 252-day volatility have different meanings.

---

### Section summary

Realized volatility measures how volatile an asset was in the past.

It is calculated from historical returns and can be measured over different windows such as 20, 60 or 252 trading days.

For CFA Level 1, realized volatility is important because it reinforces the idea of historical risk measurement using return dispersion.

For Athena AI Risk Terminal, realized volatility is a core risk metric because it is transparent, testable and based on observed market behavior.

The key lesson is:

```text
Realized volatility tells us how much an asset actually moved in the past.
It is useful for risk analysis,
but it is not a guarantee of future volatility.
```

---



















## 25. Implied volatility

Implied volatility is the volatility implied by the market price of an option.

It is not calculated directly from historical returns.

Instead, it is extracted from option prices using an option pricing model.

Simple idea:

```text
Implied volatility = volatility estimate embedded in option prices
```

It reflects how much volatility the options market appears to expect in the future.

---

### Why implied volatility exists

An option price depends on several inputs.

For a basic option model, important inputs include:

```text
Underlying asset price
Strike price
Time to maturity
Risk-free interest rate
Dividend yield
Volatility
Option type
```

Most of these inputs are directly observable or known.

Example:

```text
Underlying price = current stock price
Strike price = contract specification
Time to maturity = expiration date
Risk-free rate = market interest rate
Option type = call or put
```

Volatility is different.

Future volatility is unknown.

So the market price of the option can be used to infer the volatility assumption that investors are pricing in.

That inferred volatility is called implied volatility.

---

### Basic intuition

Suppose an option is expensive.

One possible reason is that the market expects the underlying asset to move a lot before expiration.

Large expected movements make options more valuable.

Therefore:

```text
Higher option price → higher implied volatility
Lower option price → lower implied volatility
```

This relationship is not the only factor in option pricing, but it is one of the most important.

---

### Implied volatility and option prices

Options become more valuable when expected volatility increases.

Why?

Because an option benefits from the possibility of large price movements.

For a call option:

```text
Large upward movement can create value.
```

For a put option:

```text
Large downward movement can create value.
```

The buyer of an option has limited downside but potential upside from large movements.

Because of this, higher expected volatility usually increases both call and put option prices.

Simple idea:

```text
More expected movement = more valuable optionality
```

---

### Realized volatility vs implied volatility

Realized volatility is calculated from historical returns.

Implied volatility is extracted from option prices.

Simple comparison:

```text
Realized volatility = based on past price movements
Implied volatility = based on current option prices
```

Realized volatility answers:

```text
How volatile was the asset in the past?
```

Implied volatility answers:

```text
How much volatility is the options market pricing for the future?
```

Important distinction:

```text
Realized volatility is backward-looking.
Implied volatility is forward-looking.
```

However, implied volatility is not a perfect forecast.

It is a market-implied estimate that can include risk premiums, supply and demand effects, and investor fear.

---

### Example

Suppose a stock has been calm recently.

```text
20-day realized volatility = 12%
```

But the company will announce earnings next week.

Options traders may expect a large price move.

As a result:

```text
Implied volatility = 35%
```

This means the options market is pricing much more future uncertainty than what was observed in recent historical returns.

This can happen before:

```text
Earnings announcements
Central bank decisions
Inflation reports
Product launches
Regulatory decisions
Geopolitical events
```

---

### Why implied volatility can rise

Implied volatility can rise even before the underlying asset moves.

This happens because option prices can change when investors expect future uncertainty.

Example:

```text
A stock is stable today.
But important news is expected tomorrow.
```

Even if the stock price does not move today, option prices may increase.

This increases implied volatility.

Simple idea:

```text
Implied volatility can move before realized volatility changes.
```

This is why implied volatility is useful as a forward-looking market signal.

---

### Implied volatility and uncertainty

Implied volatility is often interpreted as a market measure of uncertainty.

Higher implied volatility usually means the market expects larger future price movements.

Lower implied volatility usually means the market expects calmer future price movements.

Example:

```text
Low implied volatility:
Market expects relatively calm movement.

High implied volatility:
Market expects larger movement or greater uncertainty.
```

But implied volatility does not tell the direction of the expected move.

It only tells the expected magnitude of movement.

Important distinction:

```text
Implied volatility indicates expected movement size.
It does not indicate expected direction.
```

---

### Implied volatility does not predict direction

A common beginner mistake is to think:

```text
High implied volatility means the stock will go down.
```

This is not necessarily true.

High implied volatility means the market expects a larger move.

The move could be:

```text
Up
Down
Both directions over time
```

Example:

```text
Before earnings, implied volatility rises.
```

The market may expect a large move, but it may not know whether the earnings reaction will be positive or negative.

Simple rule:

```text
Volatility is about magnitude, not direction.
```

---

### Implied volatility and fear

Implied volatility often rises when investors become nervous.

During market stress, investors may buy put options for protection.

This can increase option prices and raise implied volatility.

Example:

```text
Market stress increases.
Investors buy downside protection.
Put option demand rises.
Option prices rise.
Implied volatility rises.
```

This is why implied volatility is sometimes associated with market fear.

However, the interpretation depends on the asset and option market.

---

### Implied volatility and VIX

The VIX is a well-known measure of implied volatility for the US equity market.

It is often called the market’s “fear gauge”.

The VIX is based on S&P 500 index options.

Simple idea:

```text
VIX = market-implied volatility estimate from S&P 500 options
```

A high VIX usually indicates higher expected market volatility.

A low VIX usually indicates calmer market expectations.

For Athena, VIX-like indicators can later be used as market stress indicators.

---

### Implied volatility and time to maturity

Options have expiration dates.

Implied volatility can differ across maturities.

Example:

```text
1-week implied volatility = 40%
3-month implied volatility = 25%
1-year implied volatility = 20%
```

This means the market expects near-term uncertainty to be higher than long-term uncertainty.

This often happens before major events.

The pattern of implied volatility across maturities is called the volatility term structure.

Simple idea:

```text
Volatility term structure = implied volatility across different expirations
```

This is an advanced topic, but it is useful for derivatives and risk analysis.

---

### Implied volatility smile and skew

Implied volatility can also differ across strike prices.

In theory, some simple models assume one volatility number for all strikes.

In practice, different option strikes often have different implied volatilities.

This creates shapes called:

```text
Volatility smile
Volatility skew
```

### Volatility smile

A volatility smile happens when options far from the current price have higher implied volatility than options near the current price.

### Volatility skew

A volatility skew happens when implied volatility is higher on one side of the strike range.

For equity markets, downside put options often have higher implied volatility because investors demand protection against crashes.

This topic is more advanced, but Athena can later use it in derivatives analytics.

---

### Implied volatility and option moneyness

Moneyness describes the relationship between the underlying price and the option strike price.

Common categories:

```text
In the money
At the money
Out of the money
```

Implied volatility is often compared using at-the-money options because they are usually liquid and informative.

Example:

```text
At-the-money implied volatility = commonly used reference volatility
```

For a first implementation, Athena could start with at-the-money implied volatility if options data is available.

---

### Implied volatility and annualization

Implied volatility is usually quoted as an annualized number.

Example:

```text
Implied volatility = 25%
```

This usually means:

```text
Annualized implied volatility = 25%
```

This makes implied volatility comparable with annualized realized volatility.

Example:

```text
252-day realized volatility = 18%
Implied volatility = 25%
```

The options market is pricing more future volatility than the asset realized historically over the selected period.

---

### Implied volatility vs expected return

Implied volatility does not directly tell expected return.

It tells expected uncertainty.

Example:

```text
Implied volatility = 40%
```

This does not mean:

```text
Expected return = 40%
```

It means the options market is pricing a high level of expected movement.

A high-volatility asset can still have poor returns.

A low-volatility asset can still produce positive returns.

Simple distinction:

```text
Expected return = expected direction and compensation
Implied volatility = expected movement size
```

---

### Implied volatility and risk premium

Implied volatility is often higher than future realized volatility.

One reason is the volatility risk premium.

Investors may be willing to pay for protection against large moves.

Option sellers may demand compensation for taking that risk.

Simple idea:

```text
Implied volatility can include a risk premium.
```

This means implied volatility is not a pure forecast.

It may reflect:

```text
Expected future volatility
Investor fear
Demand for protection
Option market liquidity
Risk premiums
Supply and demand imbalances
```

This is important for advanced interpretation.

---

### Implied volatility and realized volatility comparison

Comparing implied volatility with realized volatility can be useful.

Example:

```text
Realized volatility = 15%
Implied volatility = 25%
```

This may suggest that the market expects future volatility to be higher than recent historical volatility.

Another example:

```text
Realized volatility = 30%
Implied volatility = 20%
```

This may suggest that recent volatility was high, but the options market expects calmer conditions ahead.

However, this comparison must be interpreted carefully.

The realized volatility window and the implied volatility maturity should be consistent.

Example:

```text
Compare 30-day implied volatility with 30-day realized volatility.
```

---

### Implied volatility use cases

Implied volatility is useful for:

```text
Option pricing
Risk monitoring
Market stress analysis
Event risk analysis
Volatility trading
Hedging decisions
Comparing market expectations with historical behavior
```

Example use case:

```text
Before earnings, implied volatility rises sharply.
Athena flags that the market is pricing a large expected move.
```

Another use case:

```text
Implied volatility is much higher than realized volatility.
Athena highlights that options are pricing elevated future uncertainty.
```

---

### Implied volatility and options strategy

Option traders use implied volatility to evaluate whether options look expensive or cheap.

Example:

```text
High implied volatility:
Options may be expensive.

Low implied volatility:
Options may be cheaper.
```

This does not mean high implied volatility is always bad or low implied volatility is always good.

The key question is:

```text
Will future realized volatility be higher or lower than implied volatility?
```

If future realized volatility is higher than implied volatility, option buyers may benefit.

If future realized volatility is lower than implied volatility, option sellers may benefit.

This is an advanced idea, but it is central to volatility trading.

---

### Implied volatility data needed in Athena

To analyze implied volatility, Athena may need options market data.

Important fields include:

```text
underlying_symbol
option_symbol
option_type
strike_price
expiration_date
option_market_price
underlying_price
risk_free_rate
dividend_yield
implied_volatility
bid
ask
volume
open_interest
data_source
timestamp
```

Example:

```text
underlying_symbol: AAPL
option_type: Call
strike_price: 180
expiration_date: 2026-06-19
option_market_price: 8.50
implied_volatility: 28%
```

This data is more complex than simple stock price data.

That is why implied volatility can be added after the first market data and realized volatility modules are stable.

---

### Implied volatility in Athena

For Athena AI Risk Terminal, implied volatility can support advanced risk and derivatives features.

Possible use cases:

```text
Compare realized volatility and implied volatility
Display option-implied market expectations
Detect event risk
Monitor volatility regimes
Support option pricing
Support Greeks calculation
Support derivatives dashboards
Track VIX-like indicators
```

Example output:

```text
Underlying: AAPL
30-day realized volatility: 18%
30-day implied volatility: 32%
Difference: +14 percentage points
Interpretation: options market is pricing higher future uncertainty than recent historical volatility
```

This would help users understand market expectations.

---

### MVP approach

For Athena’s first version, implied volatility does not need to be implemented immediately.

The MVP can start with:

```text
Historical prices
Simple returns
Log returns
Realized volatility
Rolling volatility
Annualized volatility
```

Implied volatility can be added later when Athena supports:

```text
Options data
Option pricing models
Greeks
Volatility surfaces
Derivatives risk
```

This is a good implementation order because realized volatility is easier to compute and test.

---

### Common beginner mistakes

Common mistakes include:

```text
Thinking implied volatility is calculated from historical returns
Thinking implied volatility predicts direction
Thinking high implied volatility always means the asset will fall
Comparing implied volatility with realized volatility over inconsistent horizons
Ignoring option maturity
Ignoring option strike
Ignoring bid-ask spreads in options
Assuming implied volatility is a perfect forecast
Confusing implied volatility with expected return
```

Example mistake:

```text
Implied volatility is 30%, so the stock should return 30%.
```

This is wrong.

Implied volatility measures expected movement, not expected return.

---

### CFA Level 1 takeaway

For CFA Level 1, implied volatility is important mainly as a derivatives and risk concept.

Important ideas include:

```text
Option prices
Expected volatility
Forward-looking market expectations
Realized vs implied volatility
Volatility and option value
Maturity
Strike price
Market uncertainty
```

A simple memory rule:

```text
Realized volatility comes from past returns.
Implied volatility comes from option prices.
```

Another important rule:

```text
Implied volatility measures expected movement, not expected direction.
```

---

### Athena implementation takeaway

For Athena, implied volatility should be treated as an advanced feature.

The derivatives module can later support:

```text
Options data ingestion
Implied volatility display
Realized vs implied volatility comparison
Volatility term structure
Volatility smile and skew
Option pricing
Greeks calculation
Volatility risk monitoring
```

The first version should focus on realized volatility because it only requires historical price data.

Implied volatility becomes valuable once Athena starts analyzing options and derivatives.

---

### Mini revision questions

1. What is implied volatility?

2. Is implied volatility calculated from historical returns?

3. What type of market data is used to extract implied volatility?

4. What is the difference between realized volatility and implied volatility?

5. Does high implied volatility predict the direction of the asset price?

6. Why can implied volatility rise before a major event?

7. Why is implied volatility important for options?

8. Why should Athena implement realized volatility before implied volatility?

---

### Mini answers

1. Implied volatility is the volatility implied by option market prices.

2. No. It is extracted from option prices using an option pricing model.

3. Option market data is used, including option price, strike, maturity and underlying price.

4. Realized volatility is based on past returns, while implied volatility is based on option prices and market expectations.

5. No. Implied volatility measures expected movement size, not direction.

6. It can rise because investors expect greater uncertainty or larger future price movements.

7. It is important because volatility is one of the key inputs that affects option prices.

8. Athena should implement realized volatility first because it is simpler, transparent and only requires historical price data.

---

### Section summary

Implied volatility is the volatility level embedded in option prices.

It is forward-looking because it reflects the volatility that the options market appears to price for the future.

For CFA Level 1, implied volatility is important because it connects options, market expectations, uncertainty and risk.

For Athena AI Risk Terminal, implied volatility is an advanced feature that can later support options analytics, Greeks, volatility surfaces and derivatives risk monitoring.

The key lesson is:

```text
Realized volatility tells what happened.
Implied volatility tells what the options market is pricing.
```

---






















## 26. Variance and standard deviation

Variance and standard deviation are measures of dispersion.

They explain how far returns are from their average.

Simple idea:

```text
Dispersion = how spread out the returns are
```

If returns are close to their average, dispersion is low.

If returns are far from their average, dispersion is high.

In finance, dispersion matters because it helps measure risk and uncertainty.

---

### Why dispersion matters

Two assets can have the same average return but very different risk.

Example:

```text
Asset A returns:
4%, 5%, 6%

Asset B returns:
-10%, 5%, 20%
```

Both assets may have a similar average return.

But Asset B is much more unstable.

This instability is measured by variance and standard deviation.

Simple idea:

```text
Average return tells the center.
Variance and standard deviation tell the spread.
```

---

### Mean return

Before calculating variance or standard deviation, we need the mean return.

The mean return is the average return.

Formula:

```text
Mean return = (R1 + R2 + ... + Rn) / n
```

Example:

```text
Returns:
2%, 4%, 6%
```

Calculation:

```text
Mean return = (2% + 4% + 6%) / 3
Mean return = 12% / 3
Mean return = 4%
```

The mean return is:

```text
4%
```

Variance and standard deviation measure how far each return is from this mean.

---

### Variance

Variance measures the average squared deviation from the mean.

Conceptually:

```text
Variance = average squared distance from the mean return
```

The word “squared” is important.

Each deviation from the mean is squared so that negative and positive deviations do not cancel each other out.

Example:

```text
Return above the mean = positive deviation
Return below the mean = negative deviation
```

If deviations were simply added together, they could cancel out.

Squaring solves that problem.

---

### Variance intuition

Suppose the average return is:

```text
Mean return = 4%
```

And one return is:

```text
Return = 6%
```

Deviation from the mean:

```text
6% - 4% = 2%
```

Another return is:

```text
Return = 2%
```

Deviation from the mean:

```text
2% - 4% = -2%
```

Both returns are equally far from the mean.

The squared deviations are positive in both cases.

```text
(2%)²
(-2%)²
```

This is why variance captures distance from the average, not direction.

---

### Population variance

Population variance is used when the data represents the full population.

Formula:

```text
Population variance = [(R1 - mean)^2 + (R2 - mean)^2 + ... + (Rn - mean)^2] / n
```

Where:

```text
R = return
mean = average return
n = number of observations
```

Population variance divides by:

```text
n
```

This is used when all relevant observations are included.

---

### Sample variance

Sample variance is used when the data is a sample from a larger population.

Formula:

```text
Sample variance = [(R1 - mean)^2 + (R2 - mean)^2 + ... + (Rn - mean)^2] / (n - 1)
```

Sample variance divides by:

```text
n - 1
```

This adjustment is used because a sample may underestimate the true population variance.

For CFA Level 1, the distinction between population variance and sample variance is important.

Simple rule:

```text
Population variance divides by n.
Sample variance divides by n - 1.
```

---

### Variance example

Suppose we have three returns:

```text
Return 1 = 2%
Return 2 = 4%
Return 3 = 6%
```

First, calculate the mean:

```text
Mean = (2% + 4% + 6%) / 3
Mean = 4%
```

Now calculate deviations from the mean:

```text
2% - 4% = -2%
4% - 4% = 0%
6% - 4% = 2%
```

Square the deviations:

```text
(-2%)² = 0.0004
0%²    = 0.0000
2%²    = 0.0004
```

Population variance:

```text
Variance = (0.0004 + 0.0000 + 0.0004) / 3
Variance = 0.0008 / 3
Variance = 0.0002667
```

The variance is:

```text
0.0002667
```

---

### Why variance is hard to interpret

Variance is useful mathematically, but it is not always easy to interpret.

The reason is that variance is expressed in squared units.

Example:

```text
Returns are measured in %
Variance is measured in squared %
```

This makes variance less intuitive for most users.

Example:

```text
Variance = 0.0004
```

This number is mathematically useful, but it is not as easy to understand as:

```text
Standard deviation = 2%
```

This is why finance usually reports standard deviation instead of variance.

---

### Standard deviation

Standard deviation is the square root of variance.

Formula:

```text
Standard deviation = sqrt(variance)
```

Standard deviation is easier to interpret because it is expressed in the same unit as returns.

Example:

```text
Variance = 0.0004
```

Then:

```text
Standard deviation = sqrt(0.0004)
Standard deviation = 0.02
Standard deviation = 2%
```

This means returns typically move around their average by about 2%, under a simplified interpretation.

---

### Standard deviation example

Using the previous variance:

```text
Variance = 0.0002667
```

Standard deviation:

```text
Standard deviation = sqrt(0.0002667)
Standard deviation ≈ 0.0163
Standard deviation ≈ 1.63%
```

So the returns have a standard deviation of approximately:

```text
1.63%
```

This is easier to interpret than the variance.

---

### Standard deviation and volatility

In finance, the standard deviation of returns is commonly called volatility.

Simple relationship:

```text
Volatility = standard deviation of returns
```

Example:

```text
Daily standard deviation of returns = 1%
Daily volatility = 1%
```

If the standard deviation of daily returns is high, the asset is volatile.

If the standard deviation of daily returns is low, the asset is stable.

---

### Low standard deviation

A low standard deviation means returns are close to their average.

Example:

```text
Returns:
0.1%, 0.2%, 0.0%, -0.1%, 0.1%
```

These returns are stable.

The standard deviation will be low.

Interpretation:

```text
The asset has low return dispersion.
```

---

### High standard deviation

A high standard deviation means returns are far from their average.

Example:

```text
Returns:
5%, -6%, 4%, -7%, 6%
```

These returns move strongly.

The standard deviation will be high.

Interpretation:

```text
The asset has high return dispersion.
```

In finance, this usually means higher volatility.

---

### Variance vs standard deviation

Variance and standard deviation are closely related, but they are used differently.

Simple comparison:

```text
Variance:
Mathematically useful, but harder to interpret.

Standard deviation:
Easier to interpret because it uses the same unit as returns.
```

Example:

```text
Variance = 0.0004
Standard deviation = 2%
```

For dashboards, reports and user explanations, standard deviation is usually better.

For mathematical models, variance is often useful.

---

### Sample standard deviation

Sample standard deviation is the square root of sample variance.

Formula:

```text
Sample standard deviation = sqrt(sample variance)
```

This is commonly used when historical returns are treated as a sample.

Example:

```text
Historical daily returns over 252 days
```

These 252 returns are usually treated as a sample of possible return behavior.

In that case, sample standard deviation is often appropriate.

---

### Population vs sample in practice

The difference between population and sample matters most when the dataset is small.

Example:

```text
Only 5 returns available
```

The difference between dividing by `n` and `n - 1` can be meaningful.

With a large dataset, the difference becomes smaller.

Example:

```text
252 daily returns
```

The difference between dividing by 252 and 251 is small, but the methodology should still be documented.

Athena should clearly choose one method and apply it consistently.

---

### Variance and portfolio risk

Variance is very important in portfolio theory.

Portfolio risk depends on:

```text
Individual asset variances
Covariances between assets
Portfolio weights
```

This means portfolio variance is not just the weighted average of individual variances.

Correlation and covariance matter.

Simple idea:

```text
Portfolio risk depends on how assets move individually and together.
```

This concept becomes important in portfolio management and diversification.

---

### Standard deviation and risk comparison

Standard deviation helps compare the risk of assets.

Example:

```text
Asset A annualized standard deviation = 12%
Asset B annualized standard deviation = 30%
```

Asset B has more return dispersion.

This means Asset B is more volatile.

However, higher volatility is not automatically bad.

The investor must compare risk with expected return.

Example:

```text
Asset A return = 8%, volatility = 12%
Asset B return = 8%, volatility = 30%
```

Asset B has the same return but much more risk.

---

### Standard deviation and normal distribution

Standard deviation is often used with the normal distribution.

If returns were normally distributed, standard deviation would help estimate the probability of different outcomes.

For a normal distribution:

```text
About 68% of observations fall within 1 standard deviation of the mean.
About 95% fall within 2 standard deviations.
About 99.7% fall within 3 standard deviations.
```

However, financial returns are not always normal.

They often have:

```text
Fat tails
Skewness
Extreme events
Volatility clustering
```

So standard deviation is useful, but it does not capture all forms of risk.

---

### Limitation of standard deviation

Standard deviation treats upside and downside movements equally.

Example:

```text
Return = +5%
Return = -5%
```

Both can increase standard deviation.

But investors usually care more about downside risk than upside movement.

This is a limitation.

Simple idea:

```text
Standard deviation measures total dispersion, not only downside risk.
```

This is why other risk metrics may also be useful, such as:

```text
Downside deviation
Maximum drawdown
Value at Risk
Conditional Value at Risk
```

For Athena, standard deviation is a foundation, but not the only risk metric.

---

### Variance and standard deviation data needed in Athena

To calculate variance and standard deviation, Athena needs:

```text
Asset identifier
Clean return series
Return type
Date range
Frequency
Mean return
Number of observations
Population or sample method
Price field used
Currency
```

Example:

```text
symbol: AAPL
return_type: simple_return
frequency: daily
number_of_observations: 252
variance_method: sample
price_field_used: adjusted_close
```

This makes the calculation reproducible.

---

### Variance and standard deviation in Athena

Athena can use variance and standard deviation to support:

```text
Volatility calculation
Risk comparison
Portfolio risk analysis
Benchmark risk comparison
Rolling volatility
Return distribution analysis
Risk-adjusted performance
```

Example output:

```text
Asset: AAPL
Window: 252 daily returns
Mean daily return: 0.05%
Sample variance: 0.000144
Daily standard deviation: 1.20%
Annualized volatility: 19.05%
```

This output is useful because it shows the path from return data to volatility.

---

### Calculation transparency in Athena

Athena should label variance and standard deviation clearly.

Bad label:

```text
Risk = 0.000144
```

Better label:

```text
Sample variance of daily returns = 0.000144
Daily standard deviation = 1.20%
Annualized volatility = 19.05%
Window = 252 trading days
```

The second version is much easier to understand.

---

### Common beginner mistakes

Common mistakes include:

```text
Confusing variance and standard deviation
Forgetting that variance is in squared units
Calculating volatility from prices instead of returns
Using population variance when sample variance is intended
Ignoring the number of observations
Comparing daily standard deviation with annualized standard deviation
Assuming standard deviation captures all risk
Forgetting that upside moves also increase standard deviation
```

Example mistake:

```text
Variance = 0.0004, so volatility = 0.04%
```

Correct calculation:

```text
Standard deviation = sqrt(0.0004)
Standard deviation = 0.02
Standard deviation = 2%
```

---

### CFA Level 1 takeaway

For CFA Level 1, variance and standard deviation are essential quantitative concepts.

Important ideas include:

```text
Mean return
Deviation from the mean
Squared deviation
Variance
Standard deviation
Sample variance
Population variance
Volatility
Dispersion
Risk measurement
```

Important formulas:

```text
Variance = average squared deviation from the mean
```

```text
Standard deviation = sqrt(variance)
```

Simple memory rule:

```text
Variance measures squared dispersion.
Standard deviation converts dispersion back into return units.
```

Another important rule:

```text
In finance, standard deviation of returns is commonly used as volatility.
```

---

### Athena implementation takeaway

For Athena, variance and standard deviation should be implemented as core statistical functions.

The analytics module should support:

```text
Mean return calculation
Sample variance calculation
Population variance calculation
Standard deviation calculation
Daily volatility calculation
Annualized volatility calculation
Window selection
Method labeling
Data validation
```

Athena should use standard deviation as the main user-facing volatility measure.

Variance can be stored or displayed for technical users, but standard deviation is easier for most users to understand.

---

### Mini revision questions

1. What does variance measure?

2. What does standard deviation measure?

3. How are variance and standard deviation related?

4. Why is standard deviation easier to interpret than variance?

5. In finance, what is the standard deviation of returns commonly called?

6. What is the difference between population variance and sample variance?

7. Why should volatility be calculated from returns instead of prices?

8. What is one limitation of standard deviation as a risk measure?

---

### Mini answers

1. Variance measures the average squared deviation from the mean.

2. Standard deviation measures dispersion in the same unit as returns.

3. Standard deviation is the square root of variance.

4. It is easier to interpret because it is expressed in the same unit as returns.

5. It is commonly called volatility.

6. Population variance divides by n, while sample variance divides by n - 1.

7. Returns are used because they make assets comparable in percentage terms.

8. Standard deviation treats upside and downside movements equally, even though investors usually care more about downside risk.

---

### Section summary

Variance and standard deviation measure how spread out returns are around their average.

Variance is mathematically useful but harder to interpret because it is expressed in squared units.

Standard deviation is easier to interpret because it is expressed in the same unit as returns.

For CFA Level 1, these concepts are essential because they form the foundation of volatility and risk measurement.

For Athena AI Risk Terminal, standard deviation is a core input for volatility, rolling volatility, benchmark comparison and portfolio risk analysis.

The key lesson is:

```text
Variance measures squared dispersion.
Standard deviation translates that dispersion into a usable volatility measure.
```

---


























## 27. Return distributions

A return distribution shows how returns are spread across different possible outcomes.

It helps answer the question:

```text
What kinds of returns did the asset produce, and how often?
```

A return distribution can show:

```text
Average return
Volatility
Extreme losses
Extreme gains
Asymmetry
Tail behavior
Frequency of outcomes
```

Simple idea:

```text
Return distribution = the shape of historical returns
```

Looking only at one number, such as average return, is not enough.

The distribution shows the full pattern of returns.

---

### Why return distributions matter

Return distributions matter because two assets can have the same average return but very different risk profiles.

Example:

```text
Asset A:
Average return = 5%
Returns are stable.

Asset B:
Average return = 5%
Returns are very volatile.
```

The average return is the same.

But the investor experience is very different.

Asset A may feel stable and predictable.  
Asset B may have large gains and large losses.

Simple idea:

```text
The average tells the center.
The distribution tells the full story.
```

---

### Basic example

A return distribution may show that most daily returns are between:

```text
-1% and +1%
```

but occasionally returns may be:

```text
-5% or +6%
```

This tells us that normal daily movements are small, but extreme events sometimes happen.

A good risk system should care about both:

```text
Normal behavior
Extreme behavior
```

Extreme returns are especially important for risk management.

---

### What a return distribution can show

A return distribution can help analyze:

```text
Where returns are centered
How spread out returns are
How often losses occur
How often gains occur
How extreme the worst losses are
Whether the distribution is symmetric
Whether the distribution has fat tails
```

This makes distributions useful for understanding both performance and risk.

---

### Mean of the distribution

The mean is the average return.

Example:

```text
Returns:
2%, 4%, 6%
```

Mean:

```text
Mean = (2% + 4% + 6%) / 3
Mean = 4%
```

The mean tells us the center of the distribution.

But it does not tell us how risky the returns are.

Example:

```text
Asset A returns:
4%, 4%, 4%

Asset B returns:
-10%, 4%, 22%
```

Both can have the same mean, but Asset B is much more dispersed.

---

### Dispersion of the distribution

Dispersion means how spread out the returns are.

Low dispersion:

```text
Returns are close to the mean.
```

High dispersion:

```text
Returns are far from the mean.
```

Standard deviation is a common measure of dispersion.

Simple relationship:

```text
High dispersion = high volatility
Low dispersion = low volatility
```

For Athena, the distribution gives a visual explanation of volatility.

---

### Shape of the distribution

The shape of the distribution matters.

A distribution can be:

```text
Symmetric
Skewed
Fat-tailed
Narrow
Wide
```

Each shape gives different information about risk.

Example:

```text
Narrow distribution:
Returns are stable.

Wide distribution:
Returns are more uncertain.
```

A wide distribution usually means higher volatility.

---

### Symmetric distribution

A symmetric distribution has similar behavior on both sides of the mean.

Simple idea:

```text
Positive and negative deviations are balanced.
```

Example:

```text
Returns around the mean:
-2%, -1%, 0%, +1%, +2%
```

This distribution is roughly balanced.

In practice, financial returns are often not perfectly symmetric.

---

### Skewed distribution

A skewed distribution is not balanced.

It has more extreme outcomes on one side.

There are two main types:

```text
Positive skewness
Negative skewness
```

### Positive skewness

Positive skewness means the distribution has more extreme positive outcomes.

Example:

```text
Most returns are small,
but there are occasional large gains.
```

### Negative skewness

Negative skewness means the distribution has more extreme negative outcomes.

Example:

```text
Most returns are normal,
but there are occasional large losses.
```

Negative skewness is important in risk management because investors usually care strongly about large downside events.

---

### Tails of the distribution

The tails are the far left and far right parts of the distribution.

```text
Left tail = extreme negative returns
Right tail = extreme positive returns
```

Example:

```text
Left tail:
-8%, -10%, -15%

Right tail:
+8%, +10%, +15%
```

The tails matter because they show rare but important events.

In risk management, the left tail is especially important because it represents large losses.

---

### Fat tails

A distribution has fat tails when extreme events happen more often than expected under a normal distribution.

Simple idea:

```text
Fat tails = more extreme events than a normal model would suggest
```

Example:

```text
A normal model may suggest that -8% daily returns are extremely rare.
But in real financial markets, large losses may happen more often than the model predicts.
```

This matters because models that ignore fat tails may underestimate risk.

---

### Return distribution and normal distribution

The normal distribution is a common statistical model.

It is symmetric and described by:

```text
Mean
Standard deviation
```

However, financial returns are often not perfectly normal.

They may show:

```text
Skewness
Fat tails
Extreme events
Volatility clustering
```

Simple warning:

```text
Normal distribution assumptions are useful,
but they should not be accepted blindly.
```

This is important for CFA Level 1 and for Athena’s risk engine.

---

### Histogram

A histogram is a common way to display a return distribution.

It groups returns into ranges called bins.

Example bins:

```text
Less than -5%
-5% to -3%
-3% to -1%
-1% to +1%
+1% to +3%
+3% to +5%
More than +5%
```

The histogram shows how many returns fall into each range.

Example interpretation:

```text
Most returns are between -1% and +1%.
A few returns are below -5%.
A few returns are above +5%.
```

This gives a visual view of risk and return behavior.

---

### Return distribution example

Suppose an asset has the following daily returns:

```text
-1.0%
+0.5%
+0.8%
-0.3%
+0.2%
-4.5%
+1.1%
+0.4%
+5.2%
-0.6%
```

Most returns are small.

But there are two larger moves:

```text
-4.5%
+5.2%
```

The distribution would show a concentration near zero and some observations in the tails.

This tells us the asset is usually calm but can occasionally move strongly.

---

### Distribution vs single metric

A single metric can hide important details.

Example:

```text
Average return = 0.5%
```

This number does not show whether returns were:

```text
Stable
Highly volatile
Skewed
Affected by extreme losses
Affected by extreme gains
```

A return distribution gives more context.

Simple idea:

```text
One number summarizes.
A distribution explains.
```

---

### Distribution and risk

Return distributions are central to risk analysis.

They help identify:

```text
Probability of losses
Size of extreme losses
Downside asymmetry
Tail risk
Volatility patterns
```

Example:

```text
An asset with frequent small gains but rare huge losses
may look attractive on average,
but can be dangerous.
```

This type of risk may not be visible from average return alone.

---

### Downside risk

Downside risk focuses on negative outcomes.

In a return distribution, downside risk is mainly visible in the left side of the distribution.

Important questions:

```text
How often are returns negative?
How large are the worst losses?
How fat is the left tail?
Is the distribution negatively skewed?
```

For Athena, downside risk can later connect to:

```text
Value at Risk
Conditional Value at Risk
Maximum drawdown
Stress testing
```

---

### Return distribution and VaR

Value at Risk, or VaR, is linked to the return distribution.

VaR focuses on the left tail of the distribution.

Simple idea:

```text
VaR estimates a loss threshold at a chosen confidence level.
```

Example:

```text
5% daily VaR = -3%
```

This means that, based on the model or historical distribution, losses worse than 3% are expected only 5% of the time.

This is covered later in the risk management documentation, but the foundation starts with understanding return distributions.

---

### Return distribution and CVaR

Conditional Value at Risk, or CVaR, also depends on the left tail.

CVaR looks beyond the VaR threshold.

Simple idea:

```text
VaR asks: where does the bad tail start?
CVaR asks: how bad are losses once we are in the bad tail?
```

This is why understanding the full return distribution is important for advanced risk metrics.

---

### Distribution and time horizon

Return distributions depend on the time horizon.

Examples:

```text
Daily return distribution
Weekly return distribution
Monthly return distribution
Annual return distribution
```

A daily distribution may show many small returns.

A monthly distribution may show larger movements.

Athena should not mix different return frequencies in the same distribution unless the methodology is clear.

Practical rule:

```text
Compare distributions only when return frequency is consistent.
```

---

### Distribution and asset class

Different asset classes can have different return distributions.

Examples:

```text
Large equity index:
Usually moderate daily volatility.

Single growth stock:
Often wider distribution.

Commodity:
May have large price swings.

Bond fund:
Usually narrower distribution, depending on duration and credit risk.

Leveraged ETF:
Very wide distribution.
```

This is useful for comparing risk across assets.

---

### Distribution and outliers

Outliers are extreme observations.

In a return distribution, outliers appear in the tails.

Example:

```text
Normal daily returns:
-1% to +1%

Outlier:
-12%
```

An outlier can be:

```text
A real market event
A data error
```

Athena should flag outliers before using them blindly.

It should not automatically delete them because extreme returns may be real and important for risk analysis.

---

### Distribution and data quality

Return distributions are sensitive to data quality problems.

Possible issues include:

```text
Missing prices
Wrong prices
Unadjusted corporate actions
Duplicate dates
Incorrect currency conversion
Stale prices
Bad outlier handling
```

Example:

```text
A stock split is not adjusted.
```

This can create a false extreme negative return.

That false return would distort the distribution and make the asset look riskier than it really was.

Athena should validate data before building return distributions.

---

### Return distribution data needed in Athena

To build a return distribution, Athena needs:

```text
Asset identifier
Clean price series
Return series
Return type
Date range
Frequency
Price field used
Currency
Number of observations
```

Example:

```text
symbol: AAPL
return_type: simple_return
frequency: daily
date_range: 2021-01-01 to 2026-01-01
price_field_used: adjusted_close
number_of_observations: 1,260
```

This makes the distribution transparent and reproducible.

---

### Return distribution in Athena

Athena can use return distributions to support:

```text
Return histogram
Volatility analysis
Tail risk analysis
Outlier detection
Skewness calculation
Kurtosis calculation
VaR and CVaR foundations
Asset comparison
Benchmark comparison
```

Example output:

```text
Asset: AAPL
Return type: simple daily returns
Average daily return: 0.05%
Daily volatility: 1.20%
Worst daily return: -7.50%
Best daily return: +6.80%
Skewness: negative
Tail behavior: fat left tail warning
```

This gives a much richer view than average return alone.

---

### Frontend display idea

A useful Athena frontend component could be:

```text
ReturnDistributionChart
```

It could display:

```text
Histogram of returns
Mean return marker
Zero return line
Worst return marker
Best return marker
Normal distribution overlay
Tail risk warnings
```

This would help users visually understand risk.

Example insight:

```text
Most returns are small, but the left tail contains several large negative observations.
```

---

### Common beginner mistakes

Common mistakes include:

```text
Looking only at average return
Ignoring volatility
Ignoring extreme losses
Assuming returns are normally distributed
Ignoring skewness
Ignoring fat tails
Removing outliers automatically
Mixing daily and monthly returns
Using unclean price data
Ignoring the number of observations
```

Example mistake:

```text
Asset A and Asset B both have a 5% average return,
so they are equally risky.
```

This is wrong.

They may have very different return distributions.

---

### CFA Level 1 takeaway

For CFA Level 1, return distributions are important because they connect return, risk and probability.

Important concepts include:

```text
Mean
Variance
Standard deviation
Skewness
Kurtosis
Normal distribution
Fat tails
Tail risk
Downside risk
Outliers
```

A simple memory rule:

```text
The mean tells the center.
The standard deviation tells the spread.
Skewness tells the asymmetry.
Kurtosis tells the tail heaviness.
```

---

### Athena implementation takeaway

For Athena, return distributions should be used to move beyond simple average returns.

The analytics module should support:

```text
Return distribution chart
Histogram calculation
Mean return
Standard deviation
Worst and best returns
Skewness
Kurtosis
Tail risk indicators
Outlier warnings
Data quality checks
```

The goal is to help users understand the full behavior of returns, not only one summary number.

---

### Mini revision questions

1. What is a return distribution?

2. Why is average return alone not enough?

3. What does the left tail of a return distribution represent?

4. What does the right tail represent?

5. What are fat tails?

6. Why can two assets with the same average return have different risk?

7. Why should Athena validate data before building a return distribution?

8. How can a histogram help users understand returns?

---

### Mini answers

1. A return distribution shows how returns are spread across possible outcomes.

2. Average return alone does not show volatility, extreme losses, skewness or tail behavior.

3. The left tail represents extreme negative returns.

4. The right tail represents extreme positive returns.

5. Fat tails mean extreme events occur more often than expected under a normal distribution.

6. They can have different volatility, skewness and tail risk even if the average return is the same.

7. Bad data can create false extreme returns and distort the distribution.

8. A histogram visually shows how often returns fall into different ranges.

---

### Section summary

A return distribution shows the full pattern of returns.

It helps analyze average return, volatility, extreme outcomes, skewness and tail behavior.

For CFA Level 1, return distributions are important because they connect probability, risk, standard deviation, skewness, kurtosis and normality.

For Athena AI Risk Terminal, return distributions are useful for dashboards, tail risk analysis, outlier detection and future VaR/CVaR calculations.

The key lesson is:

```text
Average return is only the center.
The return distribution shows the full risk profile.
```

---


















## 28. Skewness and kurtosis

Skewness and kurtosis describe the shape of a return distribution.

They help answer questions that average return and volatility cannot fully answer.

Simple idea:

```text
Mean = center of the distribution
Volatility = spread of the distribution
Skewness = asymmetry of the distribution
Kurtosis = tail heaviness of the distribution
```

These measures are important because financial returns are often not perfectly normal.

They may show:

```text
Asymmetry
Fat tails
Extreme gains
Extreme losses
Crash risk
```

This means that average return and volatility do not tell the full story.

---

### Why shape matters

Two assets can have the same average return and the same volatility, but different distribution shapes.

Example:

```text
Asset A:
Average return = 5%
Volatility = 15%
Distribution is balanced.

Asset B:
Average return = 5%
Volatility = 15%
Distribution has rare but severe losses.
```

Both assets look similar if we only use average return and volatility.

But Asset B may be more dangerous because of its downside tail risk.

This is why skewness and kurtosis are useful.

---

### Skewness

Skewness measures asymmetry in a distribution.

A distribution is symmetric when the left side and right side are balanced.

A distribution is skewed when one side has more extreme outcomes than the other.

Simple idea:

```text
Skewness = direction of extreme outcomes
```

There are three basic cases:

```text
Zero skewness
Positive skewness
Negative skewness
```

---

### Zero skewness

Zero skewness means the distribution is approximately symmetric.

Simple idea:

```text
Positive and negative deviations are balanced.
```

Example:

```text
Returns:
-3%, -2%, -1%, 0%, +1%, +2%, +3%
```

The distribution is balanced around the center.

In this case, extreme positive and extreme negative outcomes are similar.

A normal distribution has zero skewness.

---

### Positive skewness

Positive skewness means the distribution has a longer or heavier right tail.

Simple idea:

```text
Positive skewness = more extreme positive outcomes
```

Example:

```text
Most returns are small or moderate,
but there are occasional very large gains.
```

Example return pattern:

```text
-2%, -1%, 0%, +1%, +2%, +15%
```

The large positive return creates a right tail.

This may be attractive to some investors because there is potential for large upside.

Simple interpretation:

```text
Positive skewness = upside tail
```

---

### Negative skewness

Negative skewness means the distribution has a longer or heavier left tail.

Simple idea:

```text
Negative skewness = more extreme negative outcomes
```

Example:

```text
Most returns are small or moderate,
but there are occasional very large losses.
```

Example return pattern:

```text
-15%, -2%, -1%, 0%, +1%, +2%
```

The large negative return creates a left tail.

Negative skewness is especially important in risk management because investors usually care strongly about large downside events.

Simple interpretation:

```text
Negative skewness = downside tail
```

---

### Why negative skewness matters

Negative skewness can indicate crash risk.

An investment may look stable most of the time, but occasionally experience large losses.

Example:

```text
Strategy return pattern:
+1%, +1%, +1%, +1%, -20%
```

The average return may still look acceptable before the large loss occurs.

But the distribution has important downside risk.

This type of pattern is dangerous because it can create a false sense of stability.

Simple idea:

```text
Small frequent gains can hide rare large losses.
```

---

### Skewness and investor preference

Many investors prefer positive skewness.

Why?

Because positive skewness offers the possibility of large upside outcomes.

Many investors dislike negative skewness.

Why?

Because negative skewness means rare but severe losses may occur.

Simple comparison:

```text
Positive skewness:
Occasional large gains.

Negative skewness:
Occasional large losses.
```

For portfolio risk analysis, negative skewness is usually more concerning.

---

### Skewness example

Suppose two assets have similar average returns.

```text
Asset A returns:
-2%, -1%, 0%, +1%, +2%, +3%

Asset B returns:
-10%, -1%, 0%, +1%, +2%, +3%
```

Asset B has a more negative tail because of the -10% return.

Its skewness is more negative.

This means Asset B has more downside asymmetry.

---

### Kurtosis

Kurtosis measures the heaviness of the tails of a distribution.

Simple idea:

```text
Kurtosis = how much extreme outcomes matter
```

High kurtosis means extreme events occur more often than they would under a normal distribution.

Low kurtosis means extreme events are less frequent.

In finance, kurtosis is important because markets often experience extreme events more frequently than simple normal models suggest.

---

### Tails of a distribution

The tails are the far ends of the distribution.

```text
Left tail = extreme negative returns
Right tail = extreme positive returns
```

Example:

```text
Left tail:
-8%, -12%, -20%

Right tail:
+8%, +12%, +20%
```

Kurtosis focuses on how heavy these tails are.

A distribution with heavy tails has more extreme outcomes.

---

### Normal kurtosis and excess kurtosis

A normal distribution has kurtosis equal to:

```text
3
```

Excess kurtosis compares a distribution’s kurtosis to the normal distribution.

Formula:

```text
Excess kurtosis = kurtosis - 3
```

For a normal distribution:

```text
Excess kurtosis = 3 - 3
Excess kurtosis = 0
```

Simple interpretation:

```text
Excess kurtosis = 0 means normal-like tail heaviness.
Positive excess kurtosis means heavier tails than normal.
Negative excess kurtosis means lighter tails than normal.
```

This distinction matters because some sources report kurtosis, while others report excess kurtosis.

Athena should label which measure is being used.

---

### High kurtosis

High kurtosis means the distribution has heavy tails.

Simple idea:

```text
High kurtosis = more extreme events
```

Example:

```text
Most returns are normal,
but occasionally returns are extremely large or extremely negative.
```

A high-kurtosis distribution may have many small normal observations and a few very large outliers.

In finance, high kurtosis is important because it can indicate tail risk.

---

### Low kurtosis

Low kurtosis means the distribution has lighter tails.

Simple idea:

```text
Low kurtosis = fewer extreme events
```

Returns are more concentrated and less likely to produce extreme outliers.

However, low kurtosis does not mean there is no risk.

It only means extreme tail events were less frequent in the observed sample.

---

### Fat tails

Fat tails are closely related to high kurtosis.

A distribution has fat tails when extreme outcomes occur more often than expected under a normal distribution.

Example:

```text
Normal model expectation:
Very large daily losses should be extremely rare.

Real market behavior:
Large daily losses happen more often than the normal model suggests.
```

This is a major issue in risk management.

Models that assume normal returns may underestimate large losses.

---

### Skewness vs kurtosis

Skewness and kurtosis measure different things.

Simple comparison:

```text
Skewness = asymmetry
Kurtosis = tail heaviness
```

Example:

```text
Negative skewness:
The left tail is heavier than the right tail.

High kurtosis:
Both tails may contain more extreme outcomes.
```

A distribution can have:

```text
High kurtosis with little skewness
Negative skewness with moderate kurtosis
Both negative skewness and high kurtosis
```

The most dangerous case for risk management is often:

```text
Negative skewness + high kurtosis
```

This means the distribution has large downside events and heavy tails.

---

### Example: normal-looking returns with hidden tail risk

Suppose a strategy has these returns:

```text
+0.5%, +0.4%, +0.6%, +0.5%, +0.4%, -8.0%
```

Most returns look stable.

But one large loss changes the risk profile.

This strategy may have:

```text
Negative skewness
High kurtosis
```

The average return and volatility may not fully capture the danger of the large left-tail event.

This is why distribution shape matters.

---

### Why financial returns are often not normal

Financial returns often differ from the normal distribution.

They may show:

```text
Fat tails
Skewness
Volatility clustering
Sudden jumps
Market crashes
Liquidity shocks
```

Reasons include:

```text
Investor behavior
Leverage
Liquidity constraints
News shocks
Earnings surprises
Central bank decisions
Geopolitical events
Forced selling
```

Because of this, normal distribution assumptions must be used carefully.

---

### Skewness and downside risk

Skewness is especially useful for downside risk analysis.

Negative skewness can show that large losses are more important than large gains.

Example:

```text
Asset A:
Skewness = +0.5

Asset B:
Skewness = -1.2
```

Asset B has more downside asymmetry.

This may be a warning sign for investors who care about large losses.

For Athena, skewness can help identify assets or strategies with hidden crash risk.

---

### Kurtosis and tail risk

Kurtosis helps identify tail risk.

A high-kurtosis asset may have more extreme outcomes than volatility alone suggests.

Example:

```text
Asset A:
Volatility = 15%
Kurtosis = normal-like

Asset B:
Volatility = 15%
Kurtosis = high
```

Both assets have the same volatility.

But Asset B may have more extreme returns.

This means Asset B may be riskier than it appears if we only look at standard deviation.

---

### Skewness, kurtosis and VaR

Skewness and kurtosis are important for Value at Risk.

If returns are assumed to be normal, VaR may underestimate risk when the distribution has:

```text
Negative skewness
High kurtosis
Fat tails
```

Example:

```text
A normal model may estimate a small probability of a large loss.
But if returns have fat tails, large losses may occur more often.
```

This is why distribution shape matters before building VaR and CVaR models.

---

### Skewness, kurtosis and CVaR

Conditional Value at Risk, or CVaR, focuses on losses beyond the VaR threshold.

If a return distribution has a heavy left tail, CVaR can become much worse.

Simple idea:

```text
VaR asks where the bad tail begins.
CVaR asks how bad the tail is after that point.
```

Negative skewness and high kurtosis can both make CVaR more severe.

This connects skewness and kurtosis directly to Athena’s future risk management modules.

---

### Interpreting skewness values

Skewness values are usually interpreted qualitatively.

Example:

```text
Skewness near 0:
Distribution is roughly symmetric.

Positive skewness:
Right tail is more important.

Negative skewness:
Left tail is more important.
```

A very negative skewness can be a warning sign.

Example:

```text
Skewness = -2.0
```

This may indicate significant downside asymmetry.

However, interpretation depends on the asset class, sample size and data quality.

---

### Interpreting kurtosis values

Kurtosis can be interpreted relative to the normal distribution.

If using regular kurtosis:

```text
Kurtosis = 3 means normal-like tails.
Kurtosis > 3 means heavier tails.
Kurtosis < 3 means lighter tails.
```

If using excess kurtosis:

```text
Excess kurtosis = 0 means normal-like tails.
Excess kurtosis > 0 means heavier tails.
Excess kurtosis < 0 means lighter tails.
```

Athena should clearly state whether it displays kurtosis or excess kurtosis.

---

### Data quality issues

Skewness and kurtosis are very sensitive to outliers and bad data.

Possible issues include:

```text
Incorrect prices
Unadjusted stock splits
Missing values
Duplicate dates
Wrong currency conversion
Stale prices
Extreme data errors
```

Example:

```text
A stock split is not adjusted correctly.
```

This can create a false extreme return.

That false return may produce:

```text
Artificial negative skewness
Artificial high kurtosis
```

Athena should validate returns before calculating distribution shape metrics.

---

### Sample size problem

Skewness and kurtosis require enough observations to be meaningful.

Example:

```text
10 daily returns = weak estimate
252 daily returns = better estimate
5 years of daily returns = stronger estimate
```

With small samples, one extreme observation can dominate the result.

Athena should show the number of observations used.

Example:

```text
Skewness calculated from 30 daily returns
```

This is less reliable than:

```text
Skewness calculated from 1,260 daily returns
```

---

### Skewness and kurtosis data needed in Athena

To calculate skewness and kurtosis, Athena needs:

```text
Asset identifier
Clean return series
Return type
Date range
Frequency
Number of observations
Price field used
Currency
Data source
```

Example:

```text
symbol: AAPL
return_type: simple_return
frequency: daily
date_range: 2021-01-01 to 2026-01-01
price_field_used: adjusted_close
number_of_observations: 1,260
```

This makes the result transparent and reproducible.

---

### Skewness and kurtosis in Athena

Athena can use skewness and kurtosis to support:

```text
Return distribution analysis
Tail risk detection
Downside risk warnings
VaR and CVaR preparation
Outlier detection
Risk dashboards
Asset comparison
Benchmark comparison
```

Example output:

```text
Asset: AAPL
Return type: simple daily returns
Skewness: -0.85
Excess kurtosis: 4.20
Interpretation: distribution shows downside asymmetry and fat tails
```

This gives the user more information than volatility alone.

---

### Frontend display idea

A useful Athena frontend component could be:

```text
DistributionShapeCard
```

It could display:

```text
Skewness value
Kurtosis value
Tail risk warning
Normal distribution comparison
Number of observations
Return frequency
```

Example user insight:

```text
This asset has negative skewness, meaning its extreme returns are more concentrated on the downside.
```

Another insight:

```text
This asset has high excess kurtosis, meaning extreme returns occurred more often than expected under a normal distribution.
```

---

### Common beginner mistakes

Common mistakes include:

```text
Thinking volatility tells the full risk story
Ignoring skewness
Ignoring kurtosis
Assuming all return distributions are normal
Confusing skewness with volatility
Confusing kurtosis with volatility
Forgetting that high kurtosis means more extreme events
Ignoring sample size
Using dirty return data
Not distinguishing kurtosis from excess kurtosis
```

Example mistake:

```text
Two assets have the same volatility, so they have the same risk.
```

This is incomplete.

One asset may have more negative skewness or heavier tails.

---

### CFA Level 1 takeaway

For CFA Level 1, skewness and kurtosis are important because they describe the shape of a distribution beyond mean and standard deviation.

Important concepts include:

```text
Symmetry
Asymmetry
Positive skewness
Negative skewness
Tail risk
Kurtosis
Excess kurtosis
Fat tails
Normal distribution
Extreme events
```

Simple memory rule:

```text
Skewness tells which side has the tail.
Kurtosis tells how heavy the tails are.
```

Another useful rule:

```text
Negative skewness is about downside asymmetry.
High kurtosis is about extreme outcomes.
```

---

### Athena implementation takeaway

For Athena, skewness and kurtosis should be part of the return distribution analytics module.

The analytics module should support:

```text
Skewness calculation
Kurtosis calculation
Excess kurtosis calculation
Distribution shape interpretation
Tail risk warning
Normal distribution comparison
Outlier flagging
Sample size display
Data quality checks
```

Athena should not rely only on volatility to describe risk.

The platform should help users understand whether returns are symmetric, skewed or fat-tailed.

---

### Mini revision questions

1. What does skewness measure?

2. What does positive skewness mean?

3. What does negative skewness mean?

4. Why is negative skewness important in risk management?

5. What does kurtosis measure?

6. What are fat tails?

7. What is excess kurtosis?

8. Why are skewness and kurtosis useful in Athena?

---

### Mini answers

1. Skewness measures the asymmetry of a distribution.

2. Positive skewness means the distribution has more extreme positive outcomes.

3. Negative skewness means the distribution has more extreme negative outcomes.

4. Negative skewness is important because it may indicate large downside events or crash risk.

5. Kurtosis measures the heaviness of the tails of a distribution.

6. Fat tails mean extreme events occur more often than expected under a normal distribution.

7. Excess kurtosis is kurtosis minus 3, so a normal distribution has excess kurtosis of 0.

8. They are useful because they help Athena detect asymmetry, tail risk and extreme-event behavior beyond volatility.

---

### Section summary

Skewness and kurtosis describe the shape of a return distribution.

Skewness measures asymmetry.

Kurtosis measures tail heaviness.

For CFA Level 1, these concepts are important because financial returns are often not perfectly normal.

For Athena AI Risk Terminal, skewness and kurtosis are useful for identifying downside asymmetry, fat tails and hidden tail risk.

The key lesson is:

```text
Volatility tells how spread out returns are.
Skewness tells whether extreme outcomes lean left or right.
Kurtosis tells whether extreme outcomes happen more often than expected.
```

---

































## 29. Normal distribution and fat tails

The normal distribution is one of the most common statistical models in finance.

It is often used to model returns, risk and uncertainty.

A normal distribution is described by two main parameters:

```text
Mean
Standard deviation
```

The mean tells where the distribution is centered.

The standard deviation tells how spread out the observations are.

Simple idea:

```text
Normal distribution = symmetric bell-shaped distribution
```

However, financial returns are often not perfectly normal.

They may show:

```text
Fat tails
Skewness
Extreme events
Volatility clustering
Market crashes
```

This matters because models based only on normal assumptions can underestimate risk.

---

### What is a normal distribution?

A normal distribution is a symmetric bell-shaped distribution.

It has most observations near the average and fewer observations far away from the average.

Simple visual idea:

```text
Most outcomes are near the center.
Extreme outcomes are rare.
```

In a normal distribution:

```text
Mean = center of the distribution
Standard deviation = spread around the mean
```

A normal distribution is useful because it is simple, mathematically convenient and widely understood.

---

### Symmetry

A normal distribution is symmetric.

This means the left side and the right side have the same shape.

Simple idea:

```text
Positive deviations and negative deviations are balanced.
```

Example:

```text
A return of +2% and a return of -2%
are equally far from the mean if the mean is 0%.
```

In a perfectly normal distribution, extreme gains and extreme losses are equally likely if they are the same distance from the mean.

In real financial markets, this symmetry often does not hold perfectly.

---

### The 68-95-99.7 rule

For a normal distribution, there is a useful rule:

```text
About 68% of observations fall within 1 standard deviation of the mean.
About 95% fall within 2 standard deviations.
About 99.7% fall within 3 standard deviations.
```

Example:

```text
Mean return = 0%
Standard deviation = 1%
```

Then, under a normal distribution:

```text
About 68% of returns are between -1% and +1%.
About 95% of returns are between -2% and +2%.
About 99.7% of returns are between -3% and +3%.
```

This rule is useful, but it depends on the normality assumption.

---

### Why the normal distribution is useful

The normal distribution is useful because it makes risk easier to model.

It helps analysts estimate:

```text
Expected ranges of returns
Probability of extreme outcomes
Standard deviation bands
Confidence intervals
Risk estimates
```

Example:

```text
If returns are normally distributed,
an analyst can estimate how unusual a -3% daily return is.
```

This is why the normal distribution appears frequently in finance, statistics and risk management.

---

### Normal distribution in finance

In finance, the normal distribution is sometimes used to approximate returns.

Example:

```text
Daily stock returns may be modeled as approximately normal.
```

This can be useful for simple models.

However, it is only an approximation.

Real market returns often behave differently from a perfect normal distribution.

The problem is not that the normal distribution is useless.

The problem is that it can be too simple for real markets.

---

### Normal distribution limitation

The main limitation is that the normal distribution can underestimate extreme events.

Under a normal distribution, very large losses should be extremely rare.

But in financial markets, large losses often happen more frequently than a normal model suggests.

Simple idea:

```text
Normal model says extreme events are very rare.
Markets show extreme events happen more often.
```

This difference is called fat tails.

---

### What are fat tails?

Fat tails mean that extreme outcomes occur more often than expected under a normal distribution.

The tails are the far left and far right parts of the return distribution.

```text
Left tail = extreme negative returns
Right tail = extreme positive returns
```

A fat-tailed distribution has more observations in the tails.

Simple idea:

```text
Fat tails = more extreme gains and losses than a normal model predicts
```

For risk management, the left tail is especially important because it represents large losses.

---

### Fat tail example

Suppose a normal model suggests that a daily loss worse than -5% should be extremely rare.

But historical market data shows several daily losses below -5%.

This means the actual return distribution may have a fat left tail.

Example:

```text
Normal model expectation:
Very large daily losses should almost never happen.

Market reality:
Large daily losses happen more often than expected.
```

This matters because risk models may underestimate losses if they assume normality blindly.

---

### Normal tails vs fat tails

A normal distribution has thin tails.

A fat-tailed distribution has heavier tails.

Simple comparison:

```text
Normal tails:
Extreme returns are very rare.

Fat tails:
Extreme returns are less rare than the normal model suggests.
```

Example:

```text
Normal distribution:
Most returns are near the mean.
Very few returns are extremely far away.

Fat-tailed distribution:
Most returns may still be near the mean,
but extreme returns happen more often.
```

This is one reason why financial risk can be larger than simple models suggest.

---

### Why financial returns have fat tails

Financial returns can have fat tails because markets are affected by sudden and extreme events.

Examples:

```text
Financial crises
Interest rate shocks
Inflation surprises
Earnings shocks
Liquidity crises
Geopolitical events
Bank failures
Forced selling
Leverage unwinding
Policy announcements
```

These events can create large price moves that are much bigger than normal daily fluctuations.

Markets are also influenced by human behavior.

Fear, panic and forced liquidation can amplify price movements.

---

### Fat tails and market crashes

Market crashes are one of the clearest examples of fat-tail risk.

In calm periods, daily returns may appear stable.

But during a crisis, returns can become extreme.

Example:

```text
Normal daily movement:
-1% to +1%

Crisis daily movement:
-8%, -10%, or worse
```

A model that assumes normality may treat these moves as almost impossible.

But real markets show that they can happen.

This is why fat tails are central to risk management.

---

### Normal distribution and VaR

Value at Risk, or VaR, is sometimes calculated using a normal distribution assumption.

This is called a parametric or variance-covariance VaR approach.

Simple idea:

```text
Normal VaR uses mean and standard deviation to estimate loss thresholds.
```

This can be simple and fast.

However, if returns have fat tails, normal VaR may underestimate extreme losses.

Example:

```text
Normal VaR may say large losses are very unlikely.
Historical data may show large losses happen more often.
```

This is why Athena should clearly show when a risk metric assumes normality.

---

### Normal distribution and CVaR

Conditional Value at Risk, or CVaR, focuses on losses beyond the VaR threshold.

If a distribution has fat tails, CVaR can be much worse than a normal model suggests.

Simple idea:

```text
Fat tails make the bad tail more dangerous.
```

Example:

```text
VaR tells where the loss threshold begins.
CVaR tells how severe losses are beyond that threshold.
```

If the left tail is fat, losses beyond VaR can be very large.

This is why fat tails matter for advanced Athena risk modules.

---

### Normal distribution and skewness

A normal distribution has zero skewness.

This means it is symmetric.

Financial returns may have positive or negative skewness.

Negative skewness is especially important because it means the left tail is more extreme.

Simple comparison:

```text
Normal distribution:
Balanced left and right tails.

Negatively skewed distribution:
More extreme negative outcomes.
```

A negatively skewed and fat-tailed distribution can be much riskier than a normal distribution with the same mean and standard deviation.

---

### Normal distribution and kurtosis

A normal distribution has kurtosis of 3.

If using excess kurtosis, a normal distribution has:

```text
Excess kurtosis = 0
```

High kurtosis means heavier tails.

Simple idea:

```text
High kurtosis = more extreme events
```

Financial returns often have positive excess kurtosis.

This means they can have more extreme outcomes than a normal distribution.

For Athena, kurtosis can help detect whether the normality assumption may be weak.

---

### Normal assumption vs historical data

There are two broad ways to analyze risk.

```text
Model-based approach
Historical-data approach
```

### Model-based approach

A model-based approach may assume returns follow a normal distribution.

Example:

```text
Use mean and standard deviation to estimate probabilities.
```

This is simple and efficient.

But it may underestimate fat-tail risk.

### Historical-data approach

A historical-data approach uses actual historical returns directly.

Example:

```text
Look at the worst 5% of historical returns.
```

This can capture past extreme events.

But it assumes the past sample is relevant for the future.

Both approaches have strengths and weaknesses.

---

### Why normality should be checked

Before relying on a normal model, analysts should check whether returns look approximately normal.

They can examine:

```text
Histogram of returns
Skewness
Kurtosis
Extreme observations
Normal distribution overlay
Q-Q plot
Tail behavior
```

If returns show strong skewness or fat tails, the normal assumption may be weak.

Athena can help by showing distribution diagnostics.

---

### Normal distribution overlay

A useful visual method is to compare the actual return distribution with a normal distribution.

Example:

```text
Actual return histogram
Normal distribution curve with same mean and standard deviation
```

If the actual histogram has more extreme observations than the normal curve, this suggests fat tails.

This is useful because users can visually see whether the normal model fits the data well.

---

### Practical example

Suppose an asset has:

```text
Mean daily return = 0.05%
Daily volatility = 1.00%
```

Under a normal distribution, most returns should be near:

```text
-2% to +2%
```

But suppose the actual data contains several returns such as:

```text
-6%
-8%
+7%
```

This suggests that the asset has more extreme returns than the normal distribution would imply.

The asset may have fat tails.

---

### Fat tails and risk underestimation

Fat tails can cause risk models to underestimate losses.

Example:

```text
Model assumes normal returns.
Model estimates low probability of -10% daily loss.
Market data shows -10% daily losses happened several times.
```

The model is too optimistic.

This can lead to:

```text
Underestimated VaR
Underestimated CVaR
Underestimated stress loss
Too much leverage
Poor risk limits
False sense of security
```

For Athena, this is a critical risk management lesson.

---

### Normal distribution is still useful

The normal distribution should not be rejected completely.

It is still useful for:

```text
Basic statistical intuition
Simple risk models
Teaching mean and standard deviation
Approximate calculations
Benchmarking against actual distributions
```

The key is to use it carefully.

Simple rule:

```text
Normal distribution is a useful starting point,
not a complete description of financial markets.
```

---

### Data quality and fat tails

Not every extreme return is a true market event.

Some extreme observations can come from data errors.

Examples:

```text
Wrong price
Missing price stored as zero
Unadjusted stock split
Incorrect currency conversion
Duplicate records
Bad timestamp alignment
```

Athena should flag extreme observations and investigate whether they are real or data errors.

Important rule:

```text
Do not automatically delete tail observations.
First determine whether they are real market events or data problems.
```

Extreme events are important for risk analysis when they are real.

---

### Normal distribution and Athena

Athena should support both normal-based analytics and historical analytics.

Possible normal-based analytics:

```text
Normal distribution overlay
Parametric VaR
Standard deviation bands
Probability estimates
```

Possible historical analytics:

```text
Historical return distribution
Historical VaR
Historical CVaR
Worst historical returns
Tail event detection
```

The platform should clearly label the method used.

Example:

```text
VaR method: normal assumption
```

or:

```text
VaR method: historical simulation
```

This transparency is important for professional risk analysis.

---

### Normality warnings in Athena

Athena can display warnings when returns appear far from normal.

Example warnings:

```text
Return distribution shows negative skewness.
Return distribution shows high excess kurtosis.
Extreme left-tail observations detected.
Normal model may underestimate tail risk.
```

These warnings help users avoid blindly trusting simple models.

---

### Data needed in Athena

To analyze normality and fat tails, Athena needs:

```text
Clean return series
Return frequency
Date range
Mean return
Standard deviation
Skewness
Kurtosis
Number of observations
Outlier flags
Price field used
Data source
```

Example:

```text
symbol: SPY
return_type: simple daily returns
date_range: 2021-01-01 to 2026-01-01
mean_daily_return: 0.04%
daily_volatility: 1.10%
skewness: -0.70
excess_kurtosis: 3.80
```

This allows Athena to describe whether returns look normal or fat-tailed.

---

### Frontend display idea

A useful Athena frontend component could be:

```text
ReturnDistributionNormalityPanel
```

It could display:

```text
Return histogram
Normal distribution overlay
Mean marker
Standard deviation bands
Skewness
Excess kurtosis
Tail risk warnings
Worst historical returns
```

Example user insight:

```text
This asset has heavier tails than a normal distribution, meaning extreme returns occurred more often than a normal model would predict.
```

---

### Common beginner mistakes

Common mistakes include:

```text
Assuming all returns are normally distributed
Ignoring fat tails
Ignoring skewness
Thinking standard deviation captures all risk
Deleting extreme returns automatically
Confusing data errors with real tail events
Using normal VaR without checking distribution shape
Believing normal models predict crises accurately
Ignoring sample size
```

Example mistake:

```text
The model says this loss should almost never happen,
so it cannot happen.
```

This is dangerous.

Markets can produce extreme events more often than simple models suggest.

---

### CFA Level 1 takeaway

For CFA Level 1, the normal distribution is important because it provides a foundation for probability, standard deviation and risk analysis.

However, financial returns often differ from the normal distribution.

Important concepts include:

```text
Normal distribution
Mean
Standard deviation
Symmetry
68-95-99.7 rule
Skewness
Kurtosis
Excess kurtosis
Fat tails
Tail risk
Extreme events
```

A simple memory rule:

```text
Normal distribution is symmetric and convenient.
Financial returns often have fat tails and extreme events.
```

Another important rule:

```text
Normal models can underestimate tail risk.
```

---

### Athena implementation takeaway

For Athena, normal distribution assumptions should be explicit.

The analytics module should support:

```text
Return histogram
Normal distribution overlay
Skewness calculation
Kurtosis calculation
Fat-tail detection
Tail risk warnings
Historical distribution analysis
Normal-based model labels
Historical method labels
```

Athena should help users understand when normal assumptions are being used and when historical data is being used directly.

The goal is to avoid a false sense of precision in risk analysis.

---

### Mini revision questions

1. What are the two main parameters of a normal distribution?

2. What does it mean for a distribution to be symmetric?

3. What are fat tails?

4. Why can the normal distribution underestimate market risk?

5. What does the left tail of a return distribution represent?

6. Why is high kurtosis important?

7. Why should Athena label normal-based models clearly?

8. Why should extreme returns not be deleted automatically?

---

### Mini answers

1. The two main parameters are mean and standard deviation.

2. Symmetry means the left and right sides of the distribution are balanced.

3. Fat tails mean extreme outcomes occur more often than expected under a normal distribution.

4. It can underestimate risk because real markets often have more extreme losses and gains than the normal model predicts.

5. The left tail represents extreme negative returns.

6. High kurtosis is important because it indicates heavier tails and more extreme events.

7. Athena should label normal-based models clearly so users know when a calculation depends on a normality assumption.

8. Extreme returns may be real market events, so they should be investigated before being removed.

---

### Section summary

The normal distribution is a symmetric bell-shaped model described by mean and standard deviation.

It is useful, but financial returns are often not perfectly normal.

They may have fat tails, skewness and extreme events.

For CFA Level 1, this section is important because it connects probability, standard deviation, skewness, kurtosis and risk.

For Athena AI Risk Terminal, normality assumptions must be transparent because models based only on normal distributions can underestimate extreme losses.

The key lesson is:

```text
Normal distribution is a useful model,
but financial returns often have fat tails.
Risk systems must not ignore extreme events.
```

---
























## 30. Correlation

Correlation measures how two assets move together.

It helps answer the question:

```text
Do these two assets tend to move in the same direction, in opposite directions, or independently?
```

Correlation ranges from:

```text
-1 to +1
```

The interpretation is:

```text
+1  = perfect positive correlation
 0  = no clear linear relationship
-1  = perfect negative correlation
```

Simple idea:

```text
Correlation = co-movement between two return series
```

In finance, correlation is usually calculated using returns, not prices.

---

### Why correlation matters

Correlation matters because it is central to diversification.

A portfolio can contain many assets and still be poorly diversified if all assets move together.

Example:

```text
A portfolio owns 20 technology stocks.
If all 20 stocks rise and fall together,
the portfolio may still be highly concentrated in one type of risk.
```

Diversification is stronger when assets do not move perfectly together.

Simple idea:

```text
Diversification depends on correlation, not only the number of assets.
```

---

### Positive correlation

Positive correlation means two assets tend to move in the same direction.

Example:

```text
Asset A rises.
Asset B also tends to rise.

Asset A falls.
Asset B also tends to fall.
```

If two assets have a correlation close to +1, they move very similarly.

Example:

```text
Correlation = +0.90
```

This means the two assets have a strong positive relationship.

They do not move perfectly together, but their returns are usually closely related.

---

### Negative correlation

Negative correlation means two assets tend to move in opposite directions.

Example:

```text
Asset A rises.
Asset B tends to fall.

Asset A falls.
Asset B tends to rise.
```

If two assets have a correlation close to -1, they move in strongly opposite directions.

Example:

```text
Correlation = -0.80
```

This means the two assets often move in opposite directions.

Negative correlation can be useful for hedging and risk reduction.

---

### Zero correlation

A correlation near zero means there is no clear linear relationship between the two assets.

Example:

```text
Correlation = 0.02
```

This does not mean the assets never move together.

It means there is no strong linear pattern in their returns.

Simple interpretation:

```text
Correlation near zero = weak linear co-movement
```

This can help diversification because one asset’s movement does not strongly explain the other asset’s movement.

---

### Correlation uses returns

Correlation should usually be calculated using returns, not raw prices.

Why?

Because prices can trend over time and may create misleading relationships.

Example:

```text
Stock A price rises over five years.
Stock B price also rises over five years.
```

This does not necessarily mean their short-term returns are strongly related.

For market risk, the important question is:

```text
Do their returns move together?
```

Athena should calculate correlation from return series.

---

### Correlation formula intuition

The exact formula uses covariance and standard deviations.

Conceptually:

```text
Correlation = standardized co-movement between two return series
```

More specifically:

```text
Correlation = covariance(asset A returns, asset B returns) / (standard deviation A × standard deviation B)
```

The result is standardized between:

```text
-1 and +1
```

This makes correlation easier to interpret than covariance.

---

### Correlation vs covariance

Correlation and covariance are related, but they are not the same.

Simple comparison:

```text
Covariance:
Measures joint movement, but depends on the scale of returns.

Correlation:
Measures joint movement on a standardized scale from -1 to +1.
```

Because correlation is standardized, it is easier to read.

Example:

```text
Correlation = +0.75
```

This is immediately understandable as a strong positive relationship.

Covariance values are harder to interpret directly.

---

### Correlation and diversification

Diversification works better when assets are not perfectly correlated.

Example:

```text
Asset A return = +5%
Asset B return = -2%
```

If Asset B does not always move with Asset A, it can help reduce portfolio volatility.

A portfolio with low or negative correlations may have lower risk than a portfolio where all assets move together.

Simple idea:

```text
Low correlation can reduce portfolio risk.
```

This is one of the most important lessons in portfolio management.

---

### Perfect positive correlation

Perfect positive correlation means:

```text
Correlation = +1
```

The two assets move perfectly together in a linear way.

Example:

```text
When Asset A increases by a certain amount,
Asset B increases proportionally.

When Asset A decreases,
Asset B decreases proportionally.
```

In this case, combining the two assets gives little diversification benefit.

Simple interpretation:

```text
Perfect positive correlation = no meaningful diversification benefit between the two assets.
```

---

### Perfect negative correlation

Perfect negative correlation means:

```text
Correlation = -1
```

The two assets move perfectly in opposite directions.

Example:

```text
When Asset A rises,
Asset B falls in a perfectly offsetting way.
```

This can create strong risk reduction.

In theory, if assets are combined with the right weights, perfect negative correlation can eliminate some risk.

In practice, perfect negative correlation is rare.

---

### Correlation near zero

Correlation near zero means the assets do not have a clear linear relationship.

Example:

```text
Correlation = 0.05
```

This can provide diversification benefits because the assets are not strongly linked.

However, zero correlation does not mean there is no relationship at all.

It only means there is no strong linear relationship.

There may still be non-linear relationships or crisis-period relationships.

---

### Correlation example

Suppose two stocks have daily returns.

```text
AAPL daily returns:
+1%, -2%, +1.5%, +0.5%

MSFT daily returns:
+0.8%, -1.7%, +1.2%, +0.4%
```

These returns move in similar directions.

The correlation is likely positive.

Another example:

```text
Asset A returns:
+2%, +1%, -1%, -2%

Asset B returns:
-1.5%, -0.8%, +0.9%, +1.7%
```

These returns often move in opposite directions.

The correlation is likely negative.

---

### Correlation matrix

A correlation matrix shows correlations between several assets.

Example:

```text
          AAPL   MSFT   Gold   Bonds
AAPL      1.00   0.75   0.10   -0.20
MSFT      0.75   1.00   0.05   -0.15
Gold      0.10   0.05   1.00    0.25
Bonds    -0.20  -0.15   0.25    1.00
```

The diagonal is always:

```text
1.00
```

because each asset is perfectly correlated with itself.

Correlation matrices are useful for portfolio analysis because they show how assets interact.

---

### Correlation and portfolio risk

Portfolio risk depends on:

```text
Asset weights
Individual asset volatility
Correlations between assets
```

This means that portfolio risk is not just the average of individual risks.

Example:

```text
Two risky assets may create a less risky portfolio
if their correlation is low.
```

This is one of the foundations of modern portfolio theory.

Simple idea:

```text
Portfolio risk depends on how assets move together.
```

---

### Correlation and crisis periods

Correlation can change during market stress.

Assets that appear weakly correlated in normal periods may become highly correlated during crises.

Example:

```text
Normal market:
Many assets move differently.

Crisis market:
Many risky assets fall together.
```

This is important because diversification may be weaker exactly when investors need it most.

Simple warning:

```text
Correlation is not constant.
```

Athena should eventually allow users to compare correlations across different periods.

---

### Rolling correlation

Rolling correlation measures how correlation changes over time.

Example:

```text
60-day rolling correlation between AAPL and MSFT
```

This means Athena calculates the correlation using the most recent 60 daily returns, then moves the window forward.

Rolling correlation can show whether two assets are becoming more or less related.

Example:

```text
Correlation rises from 0.40 to 0.85.
```

This means diversification between the two assets may have decreased.

---

### Correlation and asset classes

Different asset classes may have different correlations.

Examples:

```text
Stocks and stocks:
Often positively correlated, especially within the same sector.

Stocks and government bonds:
Sometimes lower or negative correlation, depending on the period.

Stocks and commodities:
Can vary depending on inflation, growth and supply shocks.

Currencies:
Depend on macroeconomic and interest rate relationships.
```

Correlations are not fixed.

They depend on market regimes, economic conditions and investor behavior.

---

### Correlation and sector exposure

Stocks in the same sector often have positive correlation.

Example:

```text
AAPL and MSFT are both large technology-related companies.
Their returns may often move together.
```

Banks may also move together because they are affected by similar drivers:

```text
Interest rates
Credit conditions
Economic growth
Regulation
```

For Athena, sector exposure can help explain why some assets are highly correlated.

---

### Correlation and benchmarks

Correlation with a benchmark can show how closely an asset or portfolio behaves like the market.

Example:

```text
Portfolio correlation with S&P 500 = 0.95
```

This means the portfolio behaves very similarly to the S&P 500.

Another example:

```text
Portfolio correlation with S&P 500 = 0.30
```

This means the portfolio is less closely linked to the S&P 500.

This is useful for understanding active risk and diversification.

---

### Correlation is not causation

A very important rule:

```text
Correlation does not prove causation.
```

If two assets move together, it does not automatically mean one asset causes the other to move.

Example:

```text
Two stocks may both rise because the whole market rises.
```

The relationship may be caused by a third factor.

Possible common drivers:

```text
Interest rates
Market sentiment
Sector news
Economic growth
Inflation expectations
Liquidity conditions
```

Athena should present correlation as a relationship, not as proof of cause.

---

### Correlation limitations

Correlation is useful, but it has limitations.

Important limitations include:

```text
Correlation measures linear relationships only.
Correlation can change over time.
Correlation can increase during crises.
Correlation can be distorted by outliers.
Correlation depends on the chosen time period.
Correlation does not prove causation.
```

This means correlation should be interpreted carefully.

It is a powerful tool, but it is not a complete risk model by itself.

---

### Data quality issues

Correlation is sensitive to data quality.

Possible issues include:

```text
Missing returns
Different trading calendars
Stale prices
Wrong currency conversion
Outliers
Unadjusted corporate actions
Mismatched dates
Different frequencies
```

Example:

```text
Asset A has daily data.
Asset B has weekly data.
```

These should not be directly correlated without proper alignment.

Athena should align dates and frequencies before calculating correlation.

---

### Correlation data needed in Athena

To calculate correlation, Athena needs:

```text
Two or more clean return series
Same date range
Same frequency
Aligned dates
Return type
Currency consistency
Price field used
Number of observations
```

Example:

```text
asset_1: AAPL
asset_2: MSFT
return_type: simple_return
frequency: daily
date_range: 2024-01-01 to 2026-01-01
observations: 502
```

This makes the correlation result reproducible.

---

### Correlation in Athena

Athena can use correlation to support:

```text
Portfolio diversification analysis
Correlation matrix
Benchmark relationship analysis
Sector co-movement analysis
Rolling correlation charts
Risk concentration detection
Portfolio construction
```

Example output:

```text
Asset 1: AAPL
Asset 2: MSFT
Correlation: 0.76
Date range: 2024-01-01 to 2026-01-01
Frequency: daily returns
Interpretation: strong positive co-movement
```

This helps the user understand whether two assets provide diversification.

---

### Frontend display idea

A useful Athena frontend component could be:

```text
CorrelationMatrix
```

It could display:

```text
Asset-by-asset correlations
Color-coded correlation levels
Benchmark correlation
Rolling correlation option
Date range selector
Return frequency selector
```

Another useful component:

```text
RollingCorrelationChart
```

This could show how the relationship between two assets changes over time.

---

### Correlation interpretation guide

A simple guide:

```text
+0.80 to +1.00:
Very strong positive correlation

+0.50 to +0.80:
Strong positive correlation

+0.20 to +0.50:
Moderate positive correlation

-0.20 to +0.20:
Weak or no linear correlation

-0.50 to -0.20:
Moderate negative correlation

-0.80 to -0.50:
Strong negative correlation

-1.00 to -0.80:
Very strong negative correlation
```

These thresholds are only practical guidelines.

They should not be treated as absolute rules.

Interpretation depends on the asset class, time period and market regime.

---

### Common beginner mistakes

Common mistakes include:

```text
Thinking many assets automatically means diversification
Calculating correlation from prices instead of returns
Ignoring the time period used
Ignoring crisis-period correlation changes
Confusing correlation with causation
Comparing correlations calculated with different frequencies
Ignoring currency effects
Ignoring outliers
Assuming correlation is stable forever
```

Example mistake:

```text
A portfolio has 30 stocks, so it must be diversified.
```

This is not necessarily true.

If all 30 stocks are highly correlated, diversification may be weak.

---

### CFA Level 1 takeaway

For CFA Level 1, correlation is essential for portfolio management.

Important concepts include:

```text
Co-movement
Positive correlation
Negative correlation
Zero correlation
Diversification
Portfolio risk
Correlation matrix
Covariance
Linear relationship
Correlation is not causation
```

The key range is:

```text
-1 ≤ correlation ≤ +1
```

A simple memory rule:

```text
Correlation measures how assets move together.
Diversification improves when correlations are lower.
```

---

### Athena implementation takeaway

For Athena, correlation should be part of the portfolio analytics module.

The analytics module should support:

```text
Pairwise correlation calculation
Correlation matrix generation
Rolling correlation
Benchmark correlation
Sector correlation
Date alignment
Frequency consistency
Return type labeling
Data quality checks
```

Athena should help users understand whether a portfolio is truly diversified.

The goal is not only to count assets, but to measure how their returns move together.

---

### Mini revision questions

1. What does correlation measure?

2. What is the range of correlation?

3. What does a correlation of +1 mean?

4. What does a correlation of -1 mean?

5. Why is correlation important for diversification?

6. Why should correlation be calculated from returns instead of prices?

7. What is a correlation matrix?

8. Why does correlation not prove causation?

---

### Mini answers

1. Correlation measures how two assets move together.

2. Correlation ranges from -1 to +1.

3. A correlation of +1 means the assets move perfectly together in a linear way.

4. A correlation of -1 means the assets move perfectly in opposite directions.

5. Correlation is important because diversification is stronger when assets do not move perfectly together.

6. Returns are used because they measure comparable percentage movements and avoid misleading price trends.

7. A correlation matrix shows pairwise correlations between several assets.

8. Correlation does not prove causation because two assets may move together due to another common factor.

---

### Section summary

Correlation measures how two assets move together.

It ranges from -1 to +1 and is central to diversification and portfolio risk analysis.

For CFA Level 1, correlation is essential because it explains why combining assets can reduce portfolio risk.

For Athena AI Risk Terminal, correlation is useful for portfolio construction, benchmark comparison, risk concentration detection and diversification analysis.

The key lesson is:

```text
Diversification is not about owning many assets.
It is about owning assets that do not all move together.
```

---

























## 31. Covariance

Covariance measures how two assets move together.

It shows whether the returns of two assets tend to move in the same direction or in opposite directions.

Simple idea:

```text
Covariance = joint movement between two return series
```

Covariance is important because portfolio risk does not depend only on the risk of each individual asset.

It also depends on how assets move together.

---

### Basic interpretation

Covariance can be positive, negative or close to zero.

```text
Positive covariance = assets tend to move in the same direction
Negative covariance = assets tend to move in opposite directions
Near zero covariance = weak joint movement
```

Example:

```text
If Asset A often rises when Asset B rises,
their covariance is likely positive.
```

Another example:

```text
If Asset A often rises when Asset B falls,
their covariance may be negative.
```

---

### Positive covariance

Positive covariance means two assets tend to move in the same direction.

Example:

```text
Asset A return is above its average.
Asset B return is also above its average.
```

or:

```text
Asset A return is below its average.
Asset B return is also below its average.
```

This creates positive joint movement.

Simple interpretation:

```text
Positive covariance = assets move together
```

Positive covariance can reduce diversification benefits because the assets may rise and fall at the same time.

---

### Negative covariance

Negative covariance means two assets tend to move in opposite directions.

Example:

```text
Asset A return is above its average.
Asset B return is below its average.
```

or:

```text
Asset A return is below its average.
Asset B return is above its average.
```

This creates negative joint movement.

Simple interpretation:

```text
Negative covariance = assets move opposite to each other
```

Negative covariance can improve diversification because one asset may help offset the movement of another.

---

### Near-zero covariance

Near-zero covariance means there is weak joint movement between the two assets.

Example:

```text
Asset A moves independently from Asset B.
```

This does not mean there is no relationship at all.

It means that, based on the observed data, there is little linear joint movement.

Simple interpretation:

```text
Near-zero covariance = weak linear co-movement
```

---

### Covariance uses returns

Covariance should usually be calculated from returns, not prices.

Why?

Because portfolio risk is based on how asset returns move together.

Example:

```text
AAPL price and MSFT price may both trend upward over time.
```

But the real risk question is:

```text
Do AAPL returns and MSFT returns move together day by day?
```

For Athena, covariance should be calculated using clean return series.

---

### Covariance formula intuition

Covariance compares deviations from average returns.

For each asset, we compare its return with its mean return.

Simple idea:

```text
Deviation = return - average return
```

Then covariance looks at whether deviations for two assets move together.

Conceptually:

```text
Covariance = average product of deviations from the mean
```

If both assets are above their average at the same time, the product is positive.

If both assets are below their average at the same time, the product is also positive.

If one asset is above its average while the other is below its average, the product is negative.

---

### Simple covariance logic

Suppose we compare Asset A and Asset B.

```text
Case 1:
Asset A above average
Asset B above average
Product of deviations = positive

Case 2:
Asset A below average
Asset B below average
Product of deviations = positive

Case 3:
Asset A above average
Asset B below average
Product of deviations = negative

Case 4:
Asset A below average
Asset B above average
Product of deviations = negative
```

If the positive products dominate, covariance is positive.

If the negative products dominate, covariance is negative.

---

### Covariance formula

A common sample covariance formula is:

```text
Covariance(A, B) = Σ[(RA_i - mean_A)(RB_i - mean_B)] / (n - 1)
```

Where:

```text
RA_i = return of Asset A at time i
RB_i = return of Asset B at time i
mean_A = average return of Asset A
mean_B = average return of Asset B
n = number of observations
```

The population version divides by:

```text
n
```

The sample version divides by:

```text
n - 1
```

For historical market data, sample covariance is commonly used.

---

### Small example

Suppose two assets have the following returns:

```text
Asset A returns:
+2%, 0%, -2%

Asset B returns:
+3%, 0%, -3%
```

Both assets move in the same direction.

When Asset A is above average, Asset B is also above average.

When Asset A is below average, Asset B is also below average.

The covariance will be positive.

Simple interpretation:

```text
The assets tend to move together.
```

---

### Negative covariance example

Suppose two assets have these returns:

```text
Asset A returns:
+2%, 0%, -2%

Asset B returns:
-3%, 0%, +3%
```

When Asset A is above average, Asset B is below average.

When Asset A is below average, Asset B is above average.

The covariance will be negative.

Simple interpretation:

```text
The assets tend to move in opposite directions.
```

---

### Covariance vs correlation

Covariance and correlation are related, but they are not the same.

```text
Covariance = raw joint movement
Correlation = standardized joint movement
```

Covariance depends on the scale of returns.

Correlation standardizes covariance so the result is always between:

```text
-1 and +1
```

This is why correlation is usually easier to interpret.

---

### Why covariance is harder to interpret

Covariance does not have a fixed range.

It can be:

```text
Positive
Negative
Small
Large
```

But the size depends on the scale of returns.

Example:

```text
Covariance = 0.00012
```

This number is mathematically useful, but not very intuitive.

By contrast:

```text
Correlation = 0.75
```

is easier to interpret because it means strong positive co-movement.

---

### Relationship between covariance and correlation

Correlation is calculated from covariance.

Formula:

```text
Correlation(A, B) = Covariance(A, B) / (Standard deviation of A × Standard deviation of B)
```

This means:

```text
Correlation standardizes covariance by the volatility of both assets.
```

Simple idea:

```text
Covariance tells joint movement.
Correlation makes joint movement easier to compare.
```

---

### Why covariance matters in portfolio risk

Covariance is essential in portfolio risk calculations.

A portfolio’s risk depends on:

```text
Asset weights
Individual asset variances
Covariances between assets
```

This means portfolio volatility is not just the weighted average of individual volatilities.

The way assets move together matters.

Simple idea:

```text
Portfolio risk depends on both individual risk and joint movement.
```

---

### Two-asset portfolio variance

For a portfolio with two assets, the variance formula is:

```text
Portfolio variance =
(wA^2 × variance_A)
+ (wB^2 × variance_B)
+ (2 × wA × wB × covariance_AB)
```

Where:

```text
wA = weight of Asset A
wB = weight of Asset B
variance_A = variance of Asset A returns
variance_B = variance of Asset B returns
covariance_AB = covariance between Asset A and Asset B returns
```

The covariance term is important because it captures how the two assets interact.

---

### Interpretation of the covariance term

The covariance term can increase or reduce portfolio risk.

If covariance is positive:

```text
The covariance term increases portfolio variance.
```

If covariance is negative:

```text
The covariance term reduces portfolio variance.
```

If covariance is near zero:

```text
The covariance term has limited effect.
```

This is why assets with low or negative covariance can improve diversification.

---

### Diversification effect

Covariance explains why diversification can reduce risk.

Example:

```text
Asset A is risky.
Asset B is risky.
But they do not move perfectly together.
```

The portfolio may be less risky than holding only one asset.

This happens because losses in one asset may be partly offset by gains or smaller losses in another asset.

Simple idea:

```text
Low covariance can reduce portfolio volatility.
```

---

### Covariance matrix

A covariance matrix shows the covariances between several assets.

Example:

```text
          AAPL      MSFT      Gold
AAPL      Var A     Cov AM    Cov AG
MSFT      Cov MA    Var M     Cov MG
Gold      Cov GA    Cov GM    Var G
```

The diagonal contains variances.

The off-diagonal values contain covariances.

Simple interpretation:

```text
Diagonal = individual asset variance
Off-diagonal = joint movement between assets
```

Covariance matrices are very important in portfolio optimization.

---

### Covariance matrix example

A simplified covariance matrix may look like this:

```text
          AAPL      MSFT      Gold
AAPL      0.0004    0.0003    0.0000
MSFT      0.0003    0.0005   -0.0001
Gold      0.0000   -0.0001    0.0002
```

Interpretation:

```text
AAPL and MSFT have positive covariance.
MSFT and Gold have slightly negative covariance.
AAPL and Gold have near-zero covariance.
```

This suggests that Gold may provide more diversification benefit than MSFT in this simplified example.

---

### Covariance and optimization

Portfolio optimization often uses covariance.

A common goal is to find asset weights that balance return and risk.

The optimizer needs:

```text
Expected returns
Variances
Covariances
Portfolio constraints
```

Covariance tells the optimizer how assets interact.

Without covariance, the optimizer cannot properly estimate portfolio risk.

This is why covariance is a core input in quantitative portfolio management.

---

### Covariance and risk concentration

Covariance can reveal hidden risk concentration.

Example:

```text
A portfolio has many different stocks.
But most stocks have high positive covariance with each other.
```

The portfolio may still be exposed to the same market risk.

Simple warning:

```text
Many assets do not guarantee diversification if their returns move together.
```

Athena can use covariance and correlation to detect this type of concentration.

---

### Covariance and changing markets

Covariance is not constant.

It can change over time.

Example:

```text
During calm markets:
Assets may have moderate covariance.

During crises:
Risky assets may move together more strongly.
```

This means historical covariance may not fully represent future covariance.

Athena can later support rolling covariance to show how joint movement changes over time.

---

### Rolling covariance

Rolling covariance calculates covariance over a moving window.

Example:

```text
60-day rolling covariance between AAPL and MSFT
```

This means Athena calculates covariance using the most recent 60 daily returns, then moves the window forward.

Rolling covariance can show whether assets are becoming more or less connected.

This can be useful for risk monitoring.

---

### Covariance and data quality

Covariance is sensitive to data quality problems.

Possible issues include:

```text
Missing returns
Different trading calendars
Unaligned dates
Different return frequencies
Outliers
Wrong currency conversion
Unadjusted corporate actions
Stale prices
```

Example:

```text
Asset A has a return on Monday.
Asset B has no return on Monday.
```

Athena must align dates correctly before calculating covariance.

Otherwise, the covariance may be wrong.

---

### Data needed in Athena

To calculate covariance, Athena needs:

```text
Two clean return series
Same date range
Same frequency
Aligned dates
Return type
Number of observations
Currency consistency
Price field used
Sample or population method
```

Example:

```text
asset_1: AAPL
asset_2: MSFT
return_type: simple_return
frequency: daily
date_range: 2024-01-01 to 2026-01-01
method: sample covariance
observations: 502
```

This makes the calculation transparent and reproducible.

---

### Covariance in Athena

Athena can use covariance to support:

```text
Portfolio variance calculation
Portfolio volatility calculation
Covariance matrix generation
Portfolio optimization
Risk contribution analysis
Diversification analysis
Benchmark risk comparison
```

Example output:

```text
Asset 1: AAPL
Asset 2: MSFT
Sample covariance: 0.0003
Date range: 2024-01-01 to 2026-01-01
Frequency: daily returns
Return type: simple return
```

For user-facing dashboards, Athena may show correlation more prominently because it is easier to interpret.

For portfolio calculations, Athena should still compute covariance internally.

---

### Frontend display idea

A useful Athena frontend component could be:

```text
CovarianceMatrix
```

It could show:

```text
Asset variances on the diagonal
Asset covariances off the diagonal
Date range
Return frequency
Method used
```

However, for most users, a correlation matrix may be easier to understand.

A practical approach:

```text
Show correlation matrix by default.
Make covariance matrix available in advanced analytics.
```

---

### Common beginner mistakes

Common mistakes include:

```text
Confusing covariance with correlation
Thinking covariance is always between -1 and +1
Calculating covariance from prices instead of returns
Ignoring date alignment
Ignoring different frequencies
Forgetting that covariance depends on scale
Assuming covariance is stable over time
Ignoring covariance in portfolio risk
```

Example mistake:

```text
Covariance = 0.0003, so the assets are weakly related.
```

This conclusion may be incomplete.

The covariance number must be interpreted relative to the volatilities of the two assets.

Correlation is usually better for direct interpretation.

---

### CFA Level 1 takeaway

For CFA Level 1, covariance is important because it is a foundation of portfolio risk.

Important concepts include:

```text
Joint movement
Positive covariance
Negative covariance
Near-zero covariance
Variance
Standard deviation
Correlation
Portfolio variance
Diversification
Covariance matrix
```

A simple memory rule:

```text
Covariance measures whether two assets move together.
Correlation standardizes that movement between -1 and +1.
```

Another important rule:

```text
Covariance is essential for calculating portfolio risk.
```

---

### Athena implementation takeaway

For Athena, covariance should be implemented as a core portfolio analytics function.

The analytics module should support:

```text
Pairwise covariance calculation
Covariance matrix generation
Sample covariance
Population covariance
Date alignment
Return frequency consistency
Portfolio variance calculation
Portfolio volatility calculation
Clear methodology labels
```

Covariance may be less intuitive than correlation, but it is essential for portfolio mathematics.

Athena should use covariance internally for risk calculations and show correlation when the goal is user-friendly interpretation.

---

### Mini revision questions

1. What does covariance measure?

2. What does positive covariance mean?

3. What does negative covariance mean?

4. Why is correlation easier to interpret than covariance?

5. How are covariance and correlation related?

6. Why is covariance important for portfolio risk?

7. What is a covariance matrix?

8. Why should Athena align dates before calculating covariance?

---

### Mini answers

1. Covariance measures the joint movement of two assets’ returns.

2. Positive covariance means the assets tend to move in the same direction.

3. Negative covariance means the assets tend to move in opposite directions.

4. Correlation is easier to interpret because it is standardized between -1 and +1.

5. Correlation equals covariance divided by the product of the two assets’ standard deviations.

6. Covariance is important because portfolio risk depends on how assets move together.

7. A covariance matrix shows variances and covariances for a group of assets.

8. Athena should align dates because covariance requires returns from the same time periods.

---

### Section summary

Covariance measures how two assets move together.

Positive covariance means assets tend to move in the same direction.

Negative covariance means they tend to move in opposite directions.

For CFA Level 1, covariance is important because it supports portfolio variance, diversification and correlation.

For Athena AI Risk Terminal, covariance is essential for portfolio risk calculations and optimization.

The key lesson is:

```text
Covariance is harder to interpret than correlation,
but it is essential for calculating portfolio risk.
```

---

























## Part IV — Liquidity, execution, benchmarks and market behavior

## 32. Liquidity

Liquidity measures how easy it is to buy or sell an asset without strongly affecting its price.

Simple idea:

```text
Liquidity = ease of trading
```

A liquid asset can be traded quickly, with low transaction costs and limited price impact.

An illiquid asset is harder to trade. Buying or selling it may take more time, cost more money, or move the market price significantly.

---

### Liquid asset

A liquid asset usually has:

```text
High trading volume
Many buyers and sellers
Narrow bid-ask spread
Fast execution
Deep order book
Low transaction costs
Small price impact
```

Example:

```text
A large ETF tracking the S&P 500 is usually liquid.
```

This means an investor can usually buy or sell it quickly without moving the price much.

---

### Illiquid asset

An illiquid asset may have:

```text
Low trading volume
Few market participants
Wide bid-ask spread
Slow execution
High transaction costs
Large price impact
Limited available quotes
```

Example:

```text
A small-cap stock with low trading volume may be illiquid.
```

If an investor tries to sell a large position, the price may fall significantly because there are not enough buyers at the current price.

---

### Why liquidity matters

Liquidity matters because market prices are not enough.

An asset may look attractive on a chart, but it may be difficult to trade in practice.

Example:

```text
Asset return looks strong.
Volatility looks acceptable.
But trading volume is very low.
```

This creates a practical problem:

```text
Can the investor actually enter or exit the position at a fair price?
```

In real markets, the ability to trade matters as much as the theoretical return.

---

### Liquidity and transaction costs

Illiquidity creates transaction costs.

Important transaction costs include:

```text
Bid-ask spread
Brokerage commissions
Market impact
Slippage
Taxes
Foreign exchange costs
```

Even if explicit commissions are low, the investor may still pay implicit costs through the bid-ask spread and price impact.

Simple idea:

```text
Illiquidity makes trading more expensive.
```

---

### Bid-ask spread and liquidity

The bid-ask spread is one of the most important liquidity indicators.

```text
Bid = price buyers are willing to pay
Ask = price sellers are willing to accept
Spread = Ask - Bid
```

A narrow spread usually means better liquidity.

A wide spread usually means weaker liquidity.

Example:

```text
Bid = 99.99
Ask = 100.01
Spread = 0.02
```

This is a narrow spread.

Another example:

```text
Bid = 98.00
Ask = 102.00
Spread = 4.00
```

This is a wide spread.

The wider spread makes trading more expensive.

---

### Volume and liquidity

Volume is another basic liquidity indicator.

High volume often means the asset is actively traded.

Example:

```text
Daily volume = 50,000,000 shares
```

This suggests strong trading activity.

Low volume can signal weak liquidity.

Example:

```text
Daily volume = 5,000 shares
```

This may make it harder to buy or sell a large position.

However, volume alone is not enough.

A complete liquidity analysis should also consider:

```text
Bid-ask spread
Order book depth
Trade size
Market impact
Trading frequency
```

---

### Market depth

Market depth measures how much buying and selling interest exists at different price levels.

A deep market has many orders close to the current price.

Example:

```text
Many buyers and sellers are available near the current market price.
```

A shallow market has few orders.

Example:

```text
Only a small number of shares are available near the current price.
```

In a shallow market, a large order can move the price significantly.

Simple idea:

```text
Market depth tells how much can be traded before the price moves.
```

---

### Price impact

Price impact is the effect of a trade on the market price.

Example:

```text
Current price = 100
Investor sells a large position
Price falls to 97
```

The trade had a negative price impact.

Large trades in illiquid assets can move prices more than large trades in liquid assets.

Simple comparison:

```text
Liquid asset:
Large trade has small price impact.

Illiquid asset:
Large trade has large price impact.
```

For risk management, price impact matters because the theoretical market price may not be the price the investor can actually get.

---

### Slippage

Slippage is the difference between the expected execution price and the actual execution price.

Example:

```text
Expected selling price = 100
Actual selling price = 99.50
```

Slippage:

```text
Slippage = 99.50 - 100
Slippage = -0.50
```

Slippage is more likely when:

```text
Liquidity is low
Markets move quickly
Order size is large
Bid-ask spreads are wide
Volatility is high
```

Simple idea:

```text
Slippage is the cost of not getting the expected price.
```

---

### Liquidity during normal markets

During normal market conditions, many assets may appear liquid.

Example:

```text
High volume
Narrow spreads
Fast execution
Stable market depth
```

Investors may assume they can always trade easily.

However, liquidity can change.

An asset that is liquid today may become less liquid during market stress.

---

### Liquidity during market stress

Liquidity is especially important during stressed market conditions.

During stress, many investors may want to sell at the same time.

This can create:

```text
Wider bid-ask spreads
Lower market depth
Higher slippage
Larger price impact
Forced selling
Temporary market dislocations
```

Example:

```text
A bond ETF may trade normally during calm periods.
During a crisis, selling pressure may rise and spreads may widen.
```

Liquidity risk often becomes most visible when investors need liquidity the most.

---

### Liquidity risk

Liquidity risk is the risk that an investor cannot buy or sell an asset quickly at a fair price.

There are two important forms:

```text
Market liquidity risk
Funding liquidity risk
```

### Market liquidity risk

Market liquidity risk is the risk that an asset cannot be traded easily without affecting its price.

Example:

```text
An investor wants to sell a small-cap stock,
but there are not enough buyers.
```

### Funding liquidity risk

Funding liquidity risk is the risk that an investor or institution cannot obtain cash or financing when needed.

Example:

```text
A fund needs cash to meet redemptions,
but its assets are hard to sell quickly.
```

For Athena’s market finance module, market liquidity risk is the main focus.

---

### Liquidity and asset classes

Liquidity differs across asset classes.

General examples:

```text
Major currencies:
Usually very liquid.

Large-cap stocks:
Usually liquid.

Major equity ETFs:
Usually liquid.

Government bonds:
Often liquid, especially for major issuers.

Small-cap stocks:
Can be less liquid.

Corporate bonds:
Can be less liquid than government bonds.

Private equity:
Very illiquid.

Real estate:
Illiquid compared with public securities.
```

These are general tendencies, not fixed rules.

Liquidity depends on the instrument, market conditions and trade size.

---

### Liquidity and trade size

Liquidity depends on the size of the trade.

Example:

```text
Buying 100 shares of a large-cap stock may be easy.
Buying 5,000,000 shares may move the market.
```

An asset can be liquid for small trades but less liquid for large institutional trades.

Simple idea:

```text
Liquidity is relative to order size.
```

This is important for portfolio managers because large portfolios cannot always trade at displayed market prices.

---

### Liquidity and valuation

Illiquidity can affect valuation.

An asset may have an estimated value, but if it cannot be sold quickly, its practical value may be lower.

Example:

```text
Estimated fair value = 100
Price available for immediate sale = 95
```

This difference reflects liquidity pressure.

In stressed markets, prices may fall because investors demand compensation for holding less liquid assets.

---

### Liquidity premium

A liquidity premium is extra expected return required by investors for holding less liquid assets.

Simple idea:

```text
Less liquid asset → investors may demand higher expected return
```

Example:

```text
A private investment may need to offer higher expected returns
because investors cannot sell it easily.
```

This concept is important in asset pricing and portfolio management.

---

### Liquidity and risk management

Liquidity is a key risk management concept.

A portfolio may look safe based on volatility, but liquidity can create hidden risk.

Example:

```text
Portfolio volatility = moderate
But many assets are illiquid
```

During a crisis, the portfolio may be difficult to rebalance or liquidate.

This can create larger losses than expected.

Simple warning:

```text
Low volatility does not always mean low liquidity risk.
```

---

### Liquidity indicators

Common liquidity indicators include:

```text
Trading volume
Average daily volume
Dollar volume
Bid-ask spread
Relative spread
Market depth
Turnover
Days to liquidate
Open interest for derivatives
```

For Athena’s first version, useful indicators include:

```text
Volume
Dollar volume
Average daily volume
Bid-ask spread
Relative volume
Liquidity warning flag
```

These are easier to implement with basic market data.

---

### Dollar volume

Dollar volume measures the monetary value traded.

Formula:

```text
Dollar volume = price × volume
```

Example:

```text
Price = 50
Volume = 2,000,000 shares
```

Calculation:

```text
Dollar volume = 50 × 2,000,000
Dollar volume = 100,000,000
```

Dollar volume is useful because share volume alone can be misleading.

Example:

```text
1,000,000 shares at 5 dollars = 5,000,000 dollars traded
1,000,000 shares at 500 dollars = 500,000,000 dollars traded
```

The share volume is the same, but the traded value is very different.

---

### Relative spread

Relative spread expresses the bid-ask spread as a percentage of the mid-price.

Formula:

```text
Relative spread = (Ask - Bid) / Mid-price
```

Where:

```text
Mid-price = (Bid + Ask) / 2
```

Example:

```text
Bid = 99
Ask = 101
Mid-price = 100
Spread = 2
```

Relative spread:

```text
Relative spread = 2 / 100
Relative spread = 2%
```

Relative spread makes it easier to compare assets with different price levels.

---

### Days to liquidate

Days to liquidate estimates how long it may take to sell a position based on trading volume.

Simple formula:

```text
Days to liquidate = position size / average daily volume
```

Example:

```text
Position size = 1,000,000 shares
Average daily volume = 250,000 shares
```

Calculation:

```text
Days to liquidate = 1,000,000 / 250,000
Days to liquidate = 4 days
```

This is a simplified estimate.

In practice, selling a large position may take longer if the investor wants to avoid moving the market price.

---

### Liquidity and ETFs

ETF liquidity has two layers:

```text
Liquidity of ETF shares
Liquidity of underlying holdings
```

An ETF may trade on an exchange, but the liquidity of its underlying assets still matters.

Example:

```text
An ETF holding large US stocks is usually liquid.
An ETF holding emerging market bonds may have more liquidity risk.
```

For Athena, ETF liquidity should consider both trading volume and the nature of the underlying exposure when available.

---

### Liquidity and derivatives

For derivatives, liquidity may be measured using:

```text
Trading volume
Open interest
Bid-ask spread
Market depth
```

Open interest measures the number of outstanding contracts.

Example:

```text
High open interest may indicate active participation in an options or futures market.
```

For Athena’s first version, derivatives liquidity can be added later.

---

### Data quality issues

Liquidity analysis depends on reliable data.

Possible data issues include:

```text
Missing volume
Missing bid or ask
Negative volume
Zero volume on active trading days
Stale quotes
Incorrect exchange data
Outlier spreads
Wrong currency
Mismatched timestamps
```

Example:

```text
Bid = 105
Ask = 100
```

This is suspicious because the bid should normally be lower than or equal to the ask.

Athena should flag this as a data quality issue.

---

### Liquidity data needed in Athena

To analyze liquidity, Athena may need:

```text
Asset identifier
Date or timestamp
Volume
Average daily volume
Price
Dollar volume
Bid
Ask
Bid-ask spread
Relative spread
Exchange
Currency
Data source
```

Example:

```text
symbol: AAPL
date: 2026-04-29
close: 180
volume: 50,000,000
dollar_volume: 9,000,000,000
bid: 179.99
ask: 180.01
spread: 0.02
currency: USD
exchange: NASDAQ
```

This allows Athena to build simple liquidity indicators.

---

### Liquidity in Athena

Athena can use liquidity analysis to support:

```text
Asset liquidity scoring
Trading cost estimation
Liquidity warnings
Portfolio liquidity analysis
Risk dashboards
Market stress monitoring
Position sizing support
```

Example output:

```text
Asset: AAPL
Average daily volume: 50,000,000 shares
Dollar volume: 9,000,000,000 USD
Bid-ask spread: 0.02
Liquidity signal: High
```

Another example:

```text
Asset: SmallCapXYZ
Average daily volume: 15,000 shares
Bid-ask spread: 3.50%
Liquidity signal: Weak
Warning: trading this asset may involve high transaction costs
```

---

### Liquidity score idea

Athena could create a simple liquidity score using indicators such as:

```text
Average daily volume
Dollar volume
Bid-ask spread
Relative spread
Days to liquidate
```

Example:

```text
Liquidity score:
High
Medium
Low
```

This would make liquidity easier to understand for users.

However, the score should be transparent.

Athena should explain why an asset is classified as liquid or illiquid.

---

### Liquidity and portfolio construction

Liquidity should influence portfolio construction.

A portfolio with many illiquid assets may be difficult to rebalance.

Example:

```text
The portfolio needs to reduce risk quickly.
But several positions cannot be sold without large price impact.
```

This can create operational and market risk.

Portfolio managers must consider:

```text
Position size
Asset liquidity
Redemption risk
Market stress scenarios
Rebalancing needs
```

For Athena, liquidity can later become part of portfolio risk monitoring.

---

### Common beginner mistakes

Common mistakes include:

```text
Thinking high return means good investment without checking liquidity
Using volume alone as the only liquidity measure
Ignoring bid-ask spread
Ignoring trade size
Forgetting liquidity can disappear during stress
Assuming ETF liquidity is always perfect
Ignoring market impact
Ignoring stale prices
Comparing assets without considering dollar volume
```

Example mistake:

```text
This asset gained 20%, so it is attractive.
```

Better question:

```text
Can the investor actually buy or sell it at a fair price?
```

---

### CFA Level 1 takeaway

For CFA Level 1, liquidity is important because it affects transaction costs, risk and investment suitability.

Important concepts include:

```text
Market liquidity
Trading volume
Bid-ask spread
Transaction costs
Market impact
Slippage
Liquidity risk
Liquidity premium
Ease of trading
```

A simple memory rule:

```text
Liquidity measures how easily an asset can be traded without large cost or price impact.
```

Another important rule:

```text
Liquidity often becomes most valuable during market stress.
```

---

### Athena implementation takeaway

For Athena, liquidity should be part of the market analytics module.

The liquidity module should support:

```text
Volume analysis
Average daily volume
Dollar volume
Bid-ask spread
Relative spread
Liquidity warnings
Data quality checks
Portfolio liquidity extension
```

Athena should not only show whether an asset has good historical returns.

It should also show whether the asset is realistically tradable.

---

### Mini revision questions

1. What does liquidity measure?

2. What are common signs of a liquid asset?

3. What are common signs of an illiquid asset?

4. Why does liquidity matter during market stress?

5. What is the bid-ask spread?

6. What is slippage?

7. Why can volume alone be an incomplete liquidity measure?

8. Why should Athena include liquidity indicators?

---

### Mini answers

1. Liquidity measures how easy it is to buy or sell an asset without strongly affecting its price.

2. A liquid asset usually has high volume, many buyers and sellers, narrow spreads and fast execution.

3. An illiquid asset may have low volume, few participants, wide spreads and large price impact.

4. Liquidity matters during stress because many investors may want to sell at the same time, causing spreads and price impact to increase.

5. The bid-ask spread is the difference between the ask price and the bid price.

6. Slippage is the difference between the expected execution price and the actual execution price.

7. Volume alone is incomplete because liquidity also depends on spreads, depth, trade size and market impact.

8. Athena should include liquidity indicators because an asset can look attractive but be difficult or expensive to trade.

---

### Section summary

Liquidity measures the ease of trading an asset.

A liquid asset can usually be bought or sold quickly with low transaction costs and limited price impact.

An illiquid asset may be difficult or expensive to trade.

For CFA Level 1, liquidity is important because it affects transaction costs, risk and investment suitability.

For Athena AI Risk Terminal, liquidity is important because risk analysis should consider not only returns and volatility, but also whether an asset can realistically be traded.

The key lesson is:

```text
An asset is not only risky because its price moves.
It can also be risky because it is hard to trade.
```

---



















## 33. Bid, ask and bid-ask spread

The bid, ask and bid-ask spread are basic concepts in market trading.

They help explain how buying and selling actually happen in a market.

Simple idea:

```text
Bid = price buyers are willing to pay
Ask = price sellers are willing to accept
Spread = difference between ask and bid
```

These concepts are important because the market price shown on a screen is not always the exact price at which an investor can trade.

---

### Bid price

The bid is the highest price that buyers are currently willing to pay for an asset.

Example:

```text
Bid = 99.95
```

This means buyers are willing to buy the asset at:

```text
99.95
```

If an investor wants to sell immediately, they may sell at the bid price.

Simple idea:

```text
The bid is the price available to a seller.
```

---

### Ask price

The ask is the lowest price that sellers are currently willing to accept for an asset.

Example:

```text
Ask = 100.05
```

This means sellers are willing to sell the asset at:

```text
100.05
```

If an investor wants to buy immediately, they may buy at the ask price.

Simple idea:

```text
The ask is the price available to a buyer.
```

---

### Bid-ask spread

The bid-ask spread is the difference between the ask price and the bid price.

Formula:

```text
Spread = Ask - Bid
```

Example:

```text
Bid = 99.95
Ask = 100.05

Spread = 100.05 - 99.95
Spread = 0.10
```

The spread is:

```text
0.10
```

This spread represents an implicit trading cost.

---

### Why bid and ask are different

The bid and ask are different because buyers and sellers do not always agree on the exact price.

Buyers want to buy at the lowest possible price.

Sellers want to sell at the highest possible price.

The market exists between these two forces.

Simple idea:

```text
Buyers prefer lower prices.
Sellers prefer higher prices.
The spread is the gap between them.
```

In liquid markets, this gap is usually small.

In illiquid markets, this gap can be large.

---

### Mid-price

The mid-price is the average of the bid and ask.

Formula:

```text
Mid-price = (Bid + Ask) / 2
```

Example:

```text
Bid = 99.95
Ask = 100.05
```

Calculation:

```text
Mid-price = (99.95 + 100.05) / 2
Mid-price = 100.00
```

The mid-price is often used as a reference price.

However, investors usually cannot buy or sell exactly at the mid-price unless an order is matched there.

---

### Spread as a trading cost

The bid-ask spread is an implicit cost of trading.

Example:

```text
Bid = 99.95
Ask = 100.05
```

If an investor buys immediately, they may pay:

```text
100.05
```

If the investor immediately sells, they may receive:

```text
99.95
```

The difference is:

```text
0.10
```

This means the investor loses money from crossing the spread.

Simple idea:

```text
Buying happens near the ask.
Selling happens near the bid.
The spread is a cost of immediacy.
```

---

### Round-trip cost

A round-trip trade means buying and then selling.

If an investor buys at the ask and sells at the bid, the spread reduces the return.

Example:

```text
Buy price = 100.05
Sell price = 99.95
```

Loss from spread:

```text
99.95 / 100.05 - 1 ≈ -0.10%
```

Even if the market does not move, the investor loses because of the spread.

This is why spread matters for trading costs.

---

### Narrow spread

A narrow spread usually indicates good liquidity.

Example:

```text
Bid = 100.00
Ask = 100.01

Spread = 0.01
```

This means buyers and sellers are very close in price.

Narrow spreads are common in:

```text
Large-cap stocks
Major ETFs
Major currency pairs
Highly traded futures
```

A narrow spread usually means trading is cheaper and easier.

---

### Wide spread

A wide spread usually indicates weaker liquidity or higher uncertainty.

Example:

```text
Bid = 98.00
Ask = 102.00

Spread = 4.00
```

This means buyers and sellers are far apart.

Wide spreads can happen when:

```text
Trading volume is low
Market uncertainty is high
The asset is illiquid
News is expected
Market makers demand more compensation
Volatility is high
```

A wide spread makes trading more expensive.

---

### Absolute spread

The absolute spread is the simple difference between ask and bid.

Formula:

```text
Absolute spread = Ask - Bid
```

Example:

```text
Bid = 99.95
Ask = 100.05

Absolute spread = 0.10
```

This is easy to calculate.

However, absolute spread can be hard to compare across assets with different price levels.

---

### Relative spread

The relative spread expresses the spread as a percentage of the mid-price.

Formula:

```text
Relative spread = (Ask - Bid) / Mid-price
```

Where:

```text
Mid-price = (Bid + Ask) / 2
```

Example:

```text
Bid = 99.95
Ask = 100.05
Mid-price = 100.00
Spread = 0.10
```

Calculation:

```text
Relative spread = 0.10 / 100.00
Relative spread = 0.10%
```

Relative spread is useful because it makes spreads comparable across assets.

---

### Why relative spread matters

Absolute spread can be misleading.

Example:

```text
Asset A:
Bid = 99.95
Ask = 100.05
Spread = 0.10

Asset B:
Bid = 9.95
Ask = 10.05
Spread = 0.10
```

Both assets have the same absolute spread.

But the relative spread is different.

Asset A:

```text
Relative spread = 0.10 / 100.00 = 0.10%
```

Asset B:

```text
Relative spread = 0.10 / 10.00 = 1.00%
```

Asset B is more expensive to trade in percentage terms.

---

### Bid-ask spread and liquidity

The bid-ask spread is one of the most important liquidity indicators.

Simple relationship:

```text
Small spread = better liquidity
Large spread = weaker liquidity
```

A small spread suggests that buyers and sellers agree closely on the asset’s value.

A large spread suggests more uncertainty, lower activity or higher trading cost.

For Athena, bid-ask spread can be used as a practical liquidity signal.

---

### Bid-ask spread and volatility

Spreads often widen when volatility increases.

Why?

Because market makers and liquidity providers face more risk when prices move quickly.

Example:

```text
Normal period:
Bid = 99.99
Ask = 100.01

Stress period:
Bid = 99.50
Ask = 100.50
```

The spread widens during stress.

Simple idea:

```text
Higher uncertainty can increase trading costs.
```

This is why liquidity and volatility are connected.

---

### Bid-ask spread and market stress

During market stress, spreads can become much wider.

This can happen because:

```text
Buyers disappear
Sellers become aggressive
Market makers reduce liquidity
Uncertainty increases
Volatility rises
Order books become thinner
```

Example:

```text
A bond ETF may trade with a narrow spread in normal conditions.
During a crisis, its spread may widen significantly.
```

This makes trading more expensive exactly when investors may need liquidity.

---

### Bid-ask spread and order type

The spread matters differently depending on the order type.

### Market order

A market order executes immediately at the best available price.

If buying, it usually executes at the ask.

If selling, it usually executes at the bid.

Simple idea:

```text
Market order = fast execution, but pays the spread
```

### Limit order

A limit order sets a maximum buying price or minimum selling price.

It may avoid crossing the spread.

But execution is not guaranteed.

Simple idea:

```text
Limit order = price control, but uncertain execution
```

---

### Example with market order

Suppose:

```text
Bid = 99.95
Ask = 100.05
```

If an investor places a market buy order:

```text
Execution price ≈ 100.05
```

If an investor places a market sell order:

```text
Execution price ≈ 99.95
```

The investor pays for immediate execution through the spread.

---

### Example with limit order

Suppose:

```text
Bid = 99.95
Ask = 100.05
```

An investor places a limit buy order at:

```text
100.00
```

This order may execute if a seller is willing to sell at 100.00.

But it may not execute immediately.

Simple tradeoff:

```text
Market order = execution certainty
Limit order = price certainty
```

---

### Bid-ask spread and slippage

The bid-ask spread is related to slippage.

Slippage is the difference between the expected execution price and the actual execution price.

Example:

```text
Expected buy price = 100.05
Actual buy price = 100.20
```

Slippage:

```text
100.20 - 100.05 = 0.15
```

Slippage can happen when:

```text
Markets move quickly
Order size is large
Liquidity is low
The bid-ask spread is wide
The order book is shallow
```

Spread is one trading cost.  
Slippage is another possible execution cost.

---

### Bid-ask spread and trade size

The displayed bid and ask may only be available for a limited quantity.

Example:

```text
Ask = 100.05 for 500 shares
```

If an investor wants to buy 10,000 shares, the full order may execute at higher prices.

This means the real execution cost can be larger than the quoted spread.

Simple idea:

```text
The displayed spread does not always show the full cost of a large trade.
```

For large portfolios, market depth also matters.

---

### Bid size and ask size

Bid size and ask size show how much quantity is available at the bid and ask.

Example:

```text
Bid = 99.95
Bid size = 1,000 shares

Ask = 100.05
Ask size = 800 shares
```

This means:

```text
Buyers are willing to buy 1,000 shares at 99.95.
Sellers are willing to sell 800 shares at 100.05.
```

Bid size and ask size help measure market depth.

---

### Bid-ask spread and ETFs

ETF spreads are important because ETFs trade on exchanges.

A liquid ETF usually has:

```text
High trading volume
Narrow bid-ask spread
Active market makers
Liquid underlying holdings
```

An ETF with a wide spread may be more expensive to trade.

Example:

```text
Large S&P 500 ETF:
Spread may be very narrow.

Niche ETF:
Spread may be wider.
```

For Athena, ETF liquidity analysis should include bid-ask spread when available.

---

### Bid-ask spread and bonds

Bonds often trade less transparently than stocks.

Some bonds may have wider spreads because they are less frequently traded.

Example:

```text
Government bonds:
Often more liquid.

Small corporate bonds:
May have wider spreads.
```

This matters because bond prices shown in a system may not always represent easy execution prices.

For a later Athena fixed-income module, bid-ask spread can be important for bond liquidity analysis.

---

### Bid-ask spread data needed in Athena

To analyze bid-ask spread, Athena needs:

```text
Asset identifier
Timestamp
Bid price
Ask price
Bid size
Ask size
Mid-price
Absolute spread
Relative spread
Currency
Exchange
Data source
```

Example:

```text
symbol: AAPL
timestamp: 2026-04-29 10:30:00
bid: 179.99
ask: 180.01
mid_price: 180.00
absolute_spread: 0.02
relative_spread: 0.0111%
currency: USD
exchange: NASDAQ
```

This allows Athena to calculate and display trading cost indicators.

---

### Bid-ask spread in Athena

Athena can use bid-ask spread to support:

```text
Liquidity analysis
Trading cost estimation
Execution risk analysis
Market stress monitoring
ETF liquidity comparison
Asset quality warnings
Portfolio liquidity dashboards
```

Example output:

```text
Asset: AAPL
Bid: 179.99
Ask: 180.01
Mid-price: 180.00
Absolute spread: 0.02
Relative spread: 0.0111%
Liquidity signal: Strong
```

Another example:

```text
Asset: SmallCapXYZ
Bid: 9.50
Ask: 10.50
Mid-price: 10.00
Absolute spread: 1.00
Relative spread: 10.00%
Liquidity signal: Weak
Warning: trading costs may be high
```

---

### Data quality checks

Bid and ask data must be validated.

Possible issues include:

```text
Missing bid
Missing ask
Bid greater than ask
Zero bid
Zero ask
Negative bid or ask
Stale quotes
Incorrect timestamps
Wrong currency
Outlier spreads
```

Example problem:

```text
Bid = 105
Ask = 100
```

This is suspicious because the bid is higher than the ask.

Athena should flag it as a data quality issue.

---

### Common beginner mistakes

Common mistakes include:

```text
Thinking the last price is always the price you can trade at
Ignoring the bid-ask spread
Thinking a small absolute spread is always cheap
Ignoring relative spread
Ignoring trade size
Ignoring bid size and ask size
Using market orders without considering spread
Forgetting spreads widen during stress
```

Example mistake:

```text
The asset price is 100, so I can buy and sell at exactly 100.
```

This is not always true.

The actual buy price may be closer to the ask, and the sell price may be closer to the bid.

---

### CFA Level 1 takeaway

For CFA Level 1, bid, ask and spread are important because they explain trading costs and market liquidity.

Important concepts include:

```text
Bid price
Ask price
Bid-ask spread
Mid-price
Liquidity
Transaction cost
Market order
Limit order
Slippage
Relative spread
```

A simple memory rule:

```text
Buyers pay the ask.
Sellers receive the bid.
The spread is the cost of immediacy.
```

---

### Athena implementation takeaway

For Athena, bid-ask spread should be part of liquidity analytics.

The liquidity module should support:

```text
Bid and ask storage
Mid-price calculation
Absolute spread calculation
Relative spread calculation
Bid and ask validation
Liquidity warning generation
Trading cost display
Market stress spread monitoring
```

Athena should help users understand that market price is not the same as execution price.

The goal is to make liquidity and transaction costs visible.

---

### Mini revision questions

1. What is the bid price?

2. What is the ask price?

3. What is the bid-ask spread?

4. Why is the spread an implicit trading cost?

5. What is the mid-price?

6. Why is relative spread useful?

7. Why can spreads widen during market stress?

8. Why should Athena validate bid and ask data?

---

### Mini answers

1. The bid is the price buyers are willing to pay.

2. The ask is the price sellers are willing to accept.

3. The bid-ask spread is the difference between the ask and the bid.

4. It is a cost because immediate buyers usually pay the ask, while immediate sellers receive the bid.

5. The mid-price is the average of the bid and ask.

6. Relative spread expresses the spread as a percentage of price, making assets easier to compare.

7. Spreads can widen because volatility, uncertainty and liquidity risk increase.

8. Athena should validate bid and ask data because missing, stale or impossible quotes can distort liquidity analysis.

---

### Section summary

The bid is the price buyers are willing to pay.

The ask is the price sellers are willing to accept.

The bid-ask spread is the difference between them and represents an implicit trading cost.

For CFA Level 1, this section is important because it connects market prices, liquidity, transaction costs and execution.

For Athena AI Risk Terminal, bid-ask spread is useful for liquidity analysis, trading cost estimation and market stress monitoring.

The key lesson is:

```text
The market price is not always the execution price.
The bid-ask spread shows the cost of trading immediately.
```
---



























## 34. Order types and market microstructure

Market microstructure studies how trading actually happens in financial markets.

It focuses on the real process behind buying and selling financial instruments.

In simple terms, market microstructure tries to answer questions such as:

```text
How are orders submitted?
How are buyers and sellers matched?
How is the execution price determined?
Why can the execution price differ from the expected price?
How do bid, ask, volume and liquidity affect trading?
```

A beginner may think that trading is simple:

```text
Click buy
Receive the asset
```

But in reality, every trade depends on market liquidity, order type, order book depth, bid-ask spread, execution speed and market conditions.

For Athena AI Risk Terminal, market microstructure matters because execution quality can affect real portfolio performance.

A theoretical portfolio return may look good, but if the asset is difficult or expensive to trade, the real return can be lower.

Simple idea:

```text
Market price is not always the same as execution price.
```

---

### Why market microstructure matters

Market microstructure matters because investors do not trade in a perfect world.

In practice, trading can involve:

```text
Bid-ask spreads
Slippage
Low liquidity
Partial execution
Delayed execution
Market impact
Transaction costs
```

Example:

```text
Expected purchase price = 100
Actual execution price  = 100.50
```

The investor paid more than expected.

This difference may look small, but it can become important for:

```text
Large trades
Illiquid assets
High-frequency strategies
Short-term trading
Risk management
Portfolio rebalancing
```

For a risk platform, ignoring execution conditions can create unrealistic analysis.

---

### Basic order types

The most common order types are:

```text
Market order
Limit order
Stop order
Stop-limit order
```

Each order type gives a different balance between:

```text
Speed
Price control
Execution certainty
Execution risk
```

Simple comparison:

```text
Market order = priority is execution speed
Limit order = priority is price control
Stop order = priority is activation after a trigger
Stop-limit order = priority is trigger + price control
```

---

### Market order

A market order executes immediately at the best available price.

It tells the broker or trading system:

```text
Buy or sell now at the best available market price.
```

Example:

```text
Investor wants to buy 100 shares of AAPL.
Investor submits a market order.
The order executes immediately at the best available ask price.
```

For a buy order, the execution usually happens at the ask price.

For a sell order, the execution usually happens at the bid price.

Simple rule:

```text
Buy market order → executed near the ask
Sell market order → executed near the bid
```

---

### Advantage of a market order

The main advantage of a market order is fast execution.

```text
Advantage = fast execution
```

This is useful when the investor wants to enter or exit a position quickly.

Example:

```text
A risk manager needs to reduce exposure quickly during a market shock.
A market order may be used because execution speed matters more than exact price.
```

---

### Disadvantage of a market order

The main disadvantage is that the execution price is uncertain.

```text
Disadvantage = execution price is uncertain
```

The investor does not control the exact price.

Example:

```text
Expected price = 50.00
Actual execution price = 50.20
```

The difference can happen because the market moved or because there was not enough liquidity at the expected price.

Market orders are riskier when:

```text
Liquidity is low
Bid-ask spread is wide
Market volatility is high
Order size is large
Markets are moving quickly
```

---

### Limit order

A limit order sets a maximum buying price or a minimum selling price.

It tells the trading system:

```text
Execute only at my limit price or better.
```

For a buy limit order, the investor sets the maximum price they are willing to pay.

For a sell limit order, the investor sets the minimum price they are willing to accept.

Example:

```text
Current stock price = 100

Investor places a buy limit order at 98.
The order will execute only if the stock can be bought at 98 or lower.
```

Another example:

```text
Current stock price = 100

Investor places a sell limit order at 105.
The order will execute only if the stock can be sold at 105 or higher.
```

---

### Advantage of a limit order

The main advantage of a limit order is price control.

```text
Advantage = price control
```

The investor avoids paying more than the chosen buy price or selling below the chosen sell price.

This is useful when:

```text
The investor wants a specific entry price
The asset is illiquid
The bid-ask spread is wide
The investor wants to avoid poor execution
```

---

### Disadvantage of a limit order

The main disadvantage is that execution is not guaranteed.

```text
Disadvantage = execution is not guaranteed
```

Example:

```text
Current price = 100
Buy limit price = 98

If the market never falls to 98,
the order will not execute.
```

This means the investor may miss the trade.

Simple idea:

```text
Limit order gives price control,
but sacrifices execution certainty.
```

---

### Stop order

A stop order becomes active when a specified stop price is reached.

It is often used for:

```text
Risk control
Trade automation
Loss limitation
Trend-following strategies
```

A stop order is not active immediately.

It waits until the market reaches a trigger price.

Example:

```text
Investor owns a stock at 100.
Investor places a stop sell order at 90.

If the price falls to 90,
the stop order becomes active.
```

A stop order is commonly used as a stop-loss order.

---

### Stop-loss order

A stop-loss order is designed to limit losses.

Example:

```text
Purchase price = 100
Stop-loss price = 90
```

If the stock falls to 90, the stop order is triggered.

The goal is to avoid a larger loss if the price continues falling.

Simple idea:

```text
Stop-loss = automatic exit when the price moves against the investor
```

However, a stop-loss does not guarantee the exact exit price.

If the market moves quickly, the execution price may be lower than the stop price.

Example:

```text
Stop price = 90
Actual execution price = 88
```

This can happen during fast markets or low liquidity periods.

---

### Stop-buy order

A stop-buy order can be used to enter a position after the price rises above a certain level.

Example:

```text
Current price = 100
Stop-buy price = 105
```

If the price reaches 105, the buy order becomes active.

This may be used by traders who want confirmation that the price is moving upward before entering the position.

Simple idea:

```text
Stop-buy order = buy only after the price breaks above a chosen level
```

---

### Stop-limit order

A stop-limit order combines a stop trigger with a limit price.

It has two prices:

```text
Stop price
Limit price
```

The stop price activates the order.

The limit price controls the worst acceptable execution price.

Example:

```text
Investor owns a stock.

Stop price = 90
Limit price = 89
```

If the stock reaches 90, the order becomes active.

But the sell order will execute only at 89 or better.

---

### Advantage of a stop-limit order

The main advantage is that it provides both automation and price control.

```text
Advantage = trigger + price control
```

The investor avoids selling far below the chosen limit price.

This can be useful in volatile markets.

---

### Disadvantage of a stop-limit order

The main disadvantage is that execution is not guaranteed.

```text
Disadvantage = the order may not execute
```

Example:

```text
Stop price = 90
Limit price = 89

The market falls quickly from 90 to 85.
```

The order is triggered, but it may not execute because the price moved below the limit price.

Simple idea:

```text
Stop-limit order controls price,
but may fail to exit the position.
```

---

### Market order vs limit order

The main difference between a market order and a limit order is the trade-off between execution speed and price control.

```text
Market order:
- High execution probability
- Low price control

Limit order:
- High price control
- Lower execution probability
```

Example:

```text
Market order:
I want to buy now.

Limit order:
I want to buy only at this price or better.
```

A market order is usually better when speed matters.

A limit order is usually better when price matters.

---

### Stop order vs stop-limit order

A stop order and a stop-limit order are both activated by a trigger price.

The difference is what happens after the trigger.

```text
Stop order:
After trigger, it becomes a market order.

Stop-limit order:
After trigger, it becomes a limit order.
```

Simple comparison:

```text
Stop order = better chance of execution, worse price control
Stop-limit order = better price control, worse execution certainty
```

---

### Order book

The order book is the list of buy and sell orders waiting in the market.

It usually contains:

```text
Bid prices
Ask prices
Quantities available at each price
```

Example:

```text
Buy orders:
99.90 for 500 shares
99.80 for 1,000 shares
99.70 for 700 shares

Sell orders:
100.10 for 400 shares
100.20 for 900 shares
100.30 for 1,200 shares
```

The highest bid and the lowest ask form the best available prices.

```text
Best bid = highest price buyers are willing to pay
Best ask = lowest price sellers are willing to accept
```

---

### Order book depth

Order book depth refers to the quantity available at different price levels.

A deep order book has many orders and large quantities available.

A shallow order book has few orders and small quantities available.

Simple comparison:

```text
Deep order book = easier to trade large size
Shallow order book = harder to trade large size
```

Depth matters because a large order may consume several price levels.

Example:

```text
Best ask = 100.00 for 100 shares
Next ask = 100.20 for 200 shares
Next ask = 100.50 for 500 shares
```

If an investor wants to buy 600 shares, the full order may not execute at 100.00.

The average execution price may be higher.

---

### Slippage

Slippage is the difference between the expected execution price and the actual execution price.

Formula:

```text
Slippage = actual execution price - expected execution price
```

For a buy order, positive slippage usually means the investor paid more than expected.

Example:

```text
Expected execution price = 100.00
Actual execution price   = 100.30

Slippage = 100.30 - 100.00
Slippage = 0.30
```

For a sell order, slippage can happen when the investor sells for less than expected.

Example:

```text
Expected selling price = 100.00
Actual selling price   = 99.70

Slippage = 99.70 - 100.00
Slippage = -0.30
```

Simple idea:

```text
Slippage measures execution surprise.
```

---

### Why slippage happens

Slippage is more likely when:

```text
Liquidity is low
Bid-ask spread is wide
Market volatility is high
The order is large
The market moves quickly
There is not enough depth in the order book
```

Example:

```text
A stock has low volume.
The investor submits a large market buy order.
The order consumes several ask levels.
The final average price is higher than expected.
```

Slippage is an important real-world trading cost.

It may not appear directly as a fee, but it reduces performance.

---

### Market impact

Market impact happens when the trade itself moves the price.

This is especially important for large orders.

Example:

```text
An investor wants to buy a large quantity of an illiquid stock.
The buying pressure pushes the price upward.
```

The investor may end up paying more because their own order affected the market.

Simple idea:

```text
Market impact = price movement caused by the trade itself
```

Market impact is usually higher when:

```text
The order is large relative to normal volume
The asset is illiquid
The order book is shallow
The market is stressed
```

---

### Transaction costs

Transaction costs are the costs associated with trading.

They can include:

```text
Brokerage commissions
Bid-ask spread
Slippage
Market impact
Exchange fees
Taxes
```

Some costs are explicit.

Example:

```text
Commission = visible fee
```

Some costs are implicit.

Example:

```text
Bid-ask spread and slippage = hidden trading costs
```

For portfolio analysis, transaction costs matter because they reduce net returns.

Simple idea:

```text
Gross return is before trading costs.
Net return is after trading costs.
```

---

### Liquidity and execution quality

Liquidity affects execution quality.

A liquid asset usually has:

```text
High trading volume
Tight bid-ask spread
Deep order book
Many buyers and sellers
Low market impact
```

An illiquid asset may have:

```text
Low trading volume
Wide bid-ask spread
Shallow order book
Few market participants
High market impact
```

This means that two assets with the same historical return may not be equally attractive.

Example:

```text
Asset A return = 10%, liquid
Asset B return = 10%, illiquid
```

Asset B may be harder and more expensive to trade.

---

### Simple execution example

Assume the order book shows:

```text
Ask price  Quantity
100.00     100 shares
100.10     200 shares
100.30     300 shares
```

An investor submits a market buy order for 500 shares.

The execution may be:

```text
100 shares at 100.00
200 shares at 100.10
200 shares at 100.30
```

Average execution price:

```text
Average price = (100 × 100.00 + 200 × 100.10 + 200 × 100.30) / 500
Average price = 100.16
```

Even if the best ask was 100.00, the investor paid an average price of 100.16.

This is why order book depth matters.

---

### Order type comparison

A simple comparison:

```text
Market order:
Fast execution, uncertain price.

Limit order:
Controlled price, uncertain execution.

Stop order:
Triggered by a price level, then executed like a market order.

Stop-limit order:
Triggered by a price level, then executed only at the limit price or better.
```

Another way to remember:

```text
Market order = execute now
Limit order = execute at my price
Stop order = activate after a trigger
Stop-limit order = activate after a trigger, but respect my price limit
```

---

### CFA Level 1 takeaway

For CFA Level 1, order types and market microstructure are important because they explain how trades are actually executed.

Important concepts include:

```text
Market order
Limit order
Stop order
Stop-limit order
Bid price
Ask price
Bid-ask spread
Order book
Market depth
Slippage
Market impact
Transaction costs
Liquidity
```

A simple memory rule:

```text
Trading is not only about what asset to buy.
It is also about how the trade is executed.
```

A good investment idea can lose value if execution is poor.

---

### Athena implementation takeaway

For Athena, order types and market microstructure can support better risk and portfolio analysis.

In the first version, Athena does not need to execute real trades.

However, it should understand the concepts because they affect realistic performance.

Possible Athena features:

```text
Display bid and ask prices
Calculate bid-ask spread
Flag low-liquidity assets
Estimate simple slippage
Track trading volume
Show liquidity warnings
Compare theoretical price and execution price
```

Possible market microstructure fields:

```text
symbol
bid_price
ask_price
last_price
bid_ask_spread
volume
average_volume
order_size
estimated_slippage
liquidity_score
timestamp
data_source
```

Example liquidity warning:

```text
Warning:
This asset has low volume and a wide bid-ask spread.
Execution costs may be high.
```

This would make Athena more realistic because it would not treat all assets as equally easy to trade.

---

### Mini revision questions

1. What does market microstructure study?

2. What is the main advantage of a market order?

3. What is the main disadvantage of a market order?

4. What is the main advantage of a limit order?

5. Why is execution not guaranteed with a limit order?

6. What is a stop order used for?

7. What is the difference between a stop order and a stop-limit order?

8. What is slippage?

9. Why does order book depth matter?

10. Why is liquidity important for execution quality?

---

### Mini answers

1. Market microstructure studies how trading actually happens in markets.

2. The main advantage of a market order is fast execution.

3. The main disadvantage is that the execution price is uncertain.

4. The main advantage of a limit order is price control.

5. Execution is not guaranteed because the market may never reach the limit price.

6. A stop order is used to activate a trade when a specific price level is reached.

7. A stop order becomes a market order after the trigger, while a stop-limit order becomes a limit order.

8. Slippage is the difference between the expected execution price and the actual execution price.

9. Order book depth matters because large orders may execute across several price levels.

10. Liquidity is important because liquid assets are usually cheaper and easier to trade.

---

### Section summary

Market microstructure explains how trades are executed in real markets.

The main order types are market orders, limit orders, stop orders and stop-limit orders.

Each order type has a different trade-off between speed, price control and execution certainty.

For CFA Level 1, this section is important because it connects liquidity, bid-ask spreads, slippage and transaction costs.

For Athena AI Risk Terminal, market microstructure matters because real portfolio performance depends not only on market prices, but also on execution quality.

The key lesson is:

```text
A trade is not only a decision to buy or sell.
It is also an execution process with costs, risks and uncertainty.
```


---


























## 35. Benchmark

A benchmark is a reference used to evaluate performance.

It gives context to an asset, a portfolio or an investment strategy.

In simple terms, a benchmark helps answer the question:

```text
Did the investment perform well compared with an appropriate reference?
```

Examples of common benchmarks include:

```text
S&P 500
Nasdaq-100
TSX Composite
CAC 40
FTSE 100
MSCI World
Bloomberg US Aggregate Bond Index
```

A benchmark is not just a random market index.

It should represent the investment universe, risk profile and strategy being evaluated.

Simple idea:

```text
Performance without a benchmark is incomplete.
```

---

### Why benchmarks matter

Benchmarks matter because performance needs context.

A return number alone does not say enough.

Example:

```text
Portfolio return = +8%
```

At first, this looks positive.

But the interpretation changes when compared with a benchmark.

Example:

```text
Portfolio return  = +8%
Benchmark return  = +12%
```

The portfolio made money, but it underperformed the benchmark.

This means the manager or strategy did worse than the relevant market reference.

Another example:

```text
Portfolio return  = -3%
Benchmark return  = -10%
```

The portfolio lost money, but it outperformed the benchmark.

This means the portfolio protected capital better than the reference market.

Simple idea:

```text
Absolute performance = performance by itself
Relative performance = performance compared with a benchmark
```

Professional investors usually care about both.

---

### Absolute performance vs relative performance

Absolute performance measures the return of an investment by itself.

Example:

```text
Portfolio return = +7%
```

This tells us the portfolio increased in value.

Relative performance compares the portfolio return with a benchmark return.

Formula:

```text
Relative performance = portfolio return - benchmark return
```

Example:

```text
Portfolio return = +7%
Benchmark return = +5%

Relative performance = +7% - +5%
Relative performance = +2%
```

The portfolio outperformed the benchmark by 2 percentage points.

Another example:

```text
Portfolio return = +7%
Benchmark return = +10%

Relative performance = +7% - +10%
Relative performance = -3%
```

The portfolio underperformed the benchmark by 3 percentage points.

---

### Outperformance and underperformance

Outperformance happens when an investment performs better than its benchmark.

```text
Portfolio return > Benchmark return
```

Example:

```text
Portfolio return = +11%
Benchmark return = +8%

Outperformance = +3%
```

Underperformance happens when an investment performs worse than its benchmark.

```text
Portfolio return < Benchmark return
```

Example:

```text
Portfolio return = +6%
Benchmark return = +9%

Underperformance = -3%
```

Outperformance does not always mean the portfolio made money.

Example:

```text
Portfolio return = -4%
Benchmark return = -9%
```

The portfolio lost money, but it still outperformed because it lost less than the benchmark.

Simple idea:

```text
Outperformance means better than the benchmark,
not necessarily positive return.
```

---

### Benchmark selection

Benchmark selection is important because the wrong benchmark can create misleading conclusions.

A good benchmark should be:

```text
Relevant
Investable or representative
Transparent
Consistent with the strategy
Appropriate for the asset universe
Measurable
Clearly defined
```

---

### Relevant benchmark

A benchmark should be relevant to the portfolio or strategy.

Example:

```text
A US large-cap equity portfolio
should be compared with a US large-cap equity benchmark.
```

A relevant benchmark should reflect the type of assets being analyzed.

Good example:

```text
US large-cap equity portfolio → S&P 500
Canadian equity portfolio → TSX Composite
French large-cap equity portfolio → CAC 40
Global equity portfolio → MSCI World
```

Bad example:

```text
Canadian bank stock portfolio → Nasdaq-100
```

This benchmark would not be appropriate because the Nasdaq-100 is heavily focused on large non-financial Nasdaq-listed companies, especially technology and growth stocks.

The comparison would be misleading.

---

### Investable or representative benchmark

A benchmark should be investable or at least representative.

Investable means that an investor can reasonably gain exposure to the benchmark.

Example:

```text
An ETF can track the S&P 500.
```

This makes the S&P 500 an investable benchmark for US large-cap equity exposure.

Representative means that the benchmark accurately reflects the market or strategy being evaluated.

Example:

```text
A broad Canadian equity index can represent the Canadian equity market.
```

A benchmark does not always need to be directly tradable, but it should represent the investment universe clearly.

---

### Transparent benchmark

A benchmark should be transparent.

This means the investor should understand:

```text
What assets are included
How the benchmark is calculated
How constituents are weighted
How often it is rebalanced
What region, sector or style it represents
```

If a benchmark is not transparent, it is difficult to know whether the comparison is fair.

Example:

```text
A black-box benchmark with unclear rules is not ideal.
```

For Athena AI Risk Terminal, transparency matters because the user should understand why a benchmark was selected.

---

### Consistent with the strategy

A benchmark should match the investment strategy.

Example:

```text
A value equity strategy should be compared with a value-oriented benchmark.
A growth equity strategy should be compared with a growth-oriented benchmark.
A bond portfolio should be compared with a fixed income benchmark.
```

If the strategy is conservative, the benchmark should not be extremely aggressive.

If the strategy focuses on technology stocks, the benchmark should reflect technology or growth exposure.

Simple idea:

```text
The benchmark must match what the strategy is trying to do.
```

---

### Appropriate for the asset universe

The asset universe is the set of assets that the portfolio or strategy is allowed to invest in.

Example:

```text
US stocks
Canadian stocks
Global bonds
Emerging market equities
European large-cap stocks
```

A benchmark should be appropriate for this universe.

Example:

```text
Portfolio universe = Canadian equities
Appropriate benchmark = TSX Composite or another Canadian equity index
```

Bad example:

```text
Portfolio universe = Canadian equities
Benchmark = S&P 500
```

The S&P 500 may be useful as global market context, but it is not the best primary benchmark for a Canadian equity strategy.

---

### Benchmark examples by asset class

Different asset classes require different benchmarks.

Examples:

```text
US large-cap equities:
S&P 500

US technology or growth equities:
Nasdaq-100

Canadian equities:
TSX Composite

French large-cap equities:
CAC 40

Global developed market equities:
MSCI World

Emerging market equities:
MSCI Emerging Markets

US investment-grade bonds:
Bloomberg US Aggregate Bond Index

Short-term cash or money market:
Treasury bill rate or money market index
```

The key point is that benchmark choice depends on what is being measured.

---

### Equity benchmarks

Equity benchmarks are used to evaluate stock portfolios or equity strategies.

Examples:

```text
S&P 500
Nasdaq-100
Dow Jones Industrial Average
Russell 1000
Russell 2000
TSX Composite
CAC 40
FTSE 100
MSCI World
MSCI Emerging Markets
```

Equity benchmarks can represent:

```text
A country
A region
A sector
A market capitalization segment
An investment style
A factor exposure
```

Example:

```text
Small-cap US equity portfolio → Russell 2000
Large-cap US equity portfolio → S&P 500
Global developed equity portfolio → MSCI World
```

---

### Fixed income benchmarks

Fixed income benchmarks are used to evaluate bond portfolios.

Examples:

```text
Bloomberg US Aggregate Bond Index
Bloomberg Global Aggregate Bond Index
Government bond indices
Corporate bond indices
High-yield bond indices
Treasury bill indices
```

Bond benchmarks are more complex than equity benchmarks because bonds have additional characteristics.

Important fixed income benchmark dimensions include:

```text
Maturity
Duration
Credit quality
Issuer type
Currency
Interest rate exposure
```

Example:

```text
A short-term government bond portfolio
should not be compared with a long-term corporate bond benchmark.
```

The interest rate risk and credit risk would not match.

---

### Cash benchmark

Cash or short-term portfolios may use a money market benchmark.

Examples:

```text
Treasury bill rate
Overnight rate
Money market index
Short-term government bill index
```

A cash benchmark is useful when the goal is capital preservation and liquidity.

Example:

```text
Portfolio return = 4.2%
Cash benchmark = 3.8%
```

The portfolio earned slightly more than cash.

This can help evaluate whether extra risk was rewarded.

---

### Custom benchmark

Sometimes a portfolio does not fit one simple index.

In that case, a custom benchmark can be created.

A custom benchmark combines several benchmarks with weights.

Example:

```text
60% S&P 500
40% Bloomberg US Aggregate Bond Index
```

This could be used for a balanced portfolio with 60% equities and 40% bonds.

Another example:

```text
40% S&P 500
30% MSCI World ex USA
20% Bloomberg Global Aggregate Bond Index
10% Treasury bills
```

Custom benchmarks are useful for multi-asset portfolios.

Simple idea:

```text
Custom benchmark = weighted reference portfolio
```

---

### Benchmark return

Benchmark return measures the percentage change in the benchmark over a period.

Formula:

```text
Benchmark return = Benchmark value_t / Benchmark value_{t-1} - 1
```

Example:

```text
Benchmark value at start = 4,000
Benchmark value at end   = 4,400

Benchmark return = 4,400 / 4,000 - 1
Benchmark return = 10%
```

Athena can calculate benchmark returns using historical index levels or ETF prices if the benchmark is represented by a tradable ETF.

---

### Excess return

Excess return is the return above the benchmark.

Formula:

```text
Excess return = portfolio return - benchmark return
```

Example:

```text
Portfolio return = 12%
Benchmark return = 9%

Excess return = 12% - 9%
Excess return = 3%
```

A positive excess return means the portfolio outperformed.

A negative excess return means the portfolio underperformed.

In portfolio management, excess return is very important because it measures value added relative to the reference.

---

### Active return

Active return is another term often used for return relative to the benchmark.

Formula:

```text
Active return = portfolio return - benchmark return
```

Example:

```text
Portfolio return = 6%
Benchmark return = 8%

Active return = -2%
```

The portfolio had a negative active return.

Simple idea:

```text
Active return measures how different the result is from the benchmark.
```

For active managers, active return is a key performance indicator.

---

### Tracking error

Tracking error measures how much the portfolio's returns deviate from the benchmark's returns over time.

Simple idea:

```text
Tracking error = volatility of active returns
```

Example:

```text
Day 1 active return = +0.2%
Day 2 active return = -0.1%
Day 3 active return = +0.4%
Day 4 active return = -0.3%
```

Tracking error measures the variability of these active returns.

A low tracking error means the portfolio behaves similarly to the benchmark.

A high tracking error means the portfolio behaves differently from the benchmark.

This matters because a portfolio can outperform the benchmark but with much higher risk.

---

### Information ratio

The information ratio measures excess return per unit of active risk.

Formula:

```text
Information ratio = active return / tracking error
```

Simple idea:

```text
Information ratio = reward for taking benchmark-relative risk
```

Example:

```text
Active return = 4%
Tracking error = 8%

Information ratio = 4% / 8%
Information ratio = 0.50
```

A higher information ratio generally means the manager generated more excess return for each unit of benchmark-relative risk.

For Athena, the information ratio can be useful later when the platform includes performance analytics.

---

### Benchmark risk

A benchmark also has risk.

It can have:

```text
Volatility
Drawdowns
Sector concentration
Currency exposure
Interest rate exposure
Credit exposure
Liquidity risk
```

Example:

```text
Nasdaq-100 may have high technology exposure.
TSX Composite may have significant financials and energy exposure.
MSCI World may have large US equity exposure.
```

This means that selecting a benchmark also means selecting a risk reference.

A benchmark is not neutral.

It represents a specific market exposure.

---

### Benchmark mismatch

Benchmark mismatch happens when the benchmark does not match the portfolio.

Example:

```text
Portfolio = Canadian dividend stocks
Benchmark = Nasdaq-100
```

This is a mismatch because the benchmark has a different region, sector exposure and investment style.

Another example:

```text
Portfolio = short-term bonds
Benchmark = long-term bond index
```

This is a mismatch because the interest rate risk is different.

Benchmark mismatch can make performance analysis unfair.

A portfolio may look good or bad only because the comparison is wrong.

---

### Benchmark and risk-adjusted performance

Benchmarks are also useful for risk-adjusted performance.

A portfolio should not be judged only by return.

Example:

```text
Portfolio A return = 10%
Portfolio B return = 10%
```

They look equal.

But if:

```text
Portfolio A volatility = 8%
Portfolio B volatility = 20%
```

Portfolio A produced the same return with less risk.

Benchmark comparison can be combined with risk measures such as:

```text
Volatility
Beta
Tracking error
Information ratio
Sharpe ratio
Maximum drawdown
```

This gives a more complete view of performance.

---

### Benchmark in portfolio reporting

In professional portfolio reports, benchmark comparison is common.

A report may show:

```text
Portfolio return
Benchmark return
Excess return
Portfolio volatility
Benchmark volatility
Tracking error
Information ratio
Maximum drawdown
Sector weights vs benchmark
Currency exposure vs benchmark
```

Example:

```text
Portfolio technology weight = 35%
Benchmark technology weight = 28%

Active technology weight = +7%
```

This means the portfolio is overweight technology compared with the benchmark.

Benchmark reporting helps explain where performance and risk came from.

---

### Benchmark and active management

Active management tries to outperform a benchmark.

An active manager may choose securities or weights different from the benchmark.

Example:

```text
Benchmark weight in technology = 25%
Portfolio weight in technology = 35%
```

The manager is overweight technology.

If technology performs well, this may help performance.

If technology performs poorly, this may hurt performance.

Simple idea:

```text
Active management = intentional difference from the benchmark
```

These differences create active risk.

---

### Benchmark and passive management

Passive management tries to track a benchmark.

Example:

```text
An S&P 500 ETF tries to replicate the S&P 500.
```

The goal is not to beat the benchmark.

The goal is to match it as closely as possible.

For passive strategies, important metrics include:

```text
Tracking difference
Tracking error
Expense ratio
Liquidity
Replication quality
```

Simple idea:

```text
Passive management = follow the benchmark
Active management = beat the benchmark
```

---

### Benchmark and ETFs

Many ETFs are built around benchmarks.

Example:

```text
SPY tracks the S&P 500
QQQ tracks the Nasdaq-100
XIU tracks Canadian large-cap equities
```

The benchmark defines the ETF's target exposure.

The ETF is the tradable product.

Simple distinction:

```text
Benchmark/index = reference calculation
ETF = tradable instrument tracking that reference
```

This is important for Athena because a benchmark can be represented in two ways:

```text
As an index level
As a benchmark ETF proxy
```

For example, if direct index data is not available, Athena may use an ETF as a practical proxy.

---

### Benchmark data needed in Athena

A clean benchmark record may include:

```text
benchmark_id
benchmark_name
benchmark_symbol
asset_class
region
country
currency
benchmark_type
weighting_method
return_type
data_source
is_tradable_proxy
proxy_symbol
```

Example:

```text
benchmark_id: SP500
benchmark_name: S&P 500
benchmark_symbol: SPX
asset_class: Equity
region: United States
currency: USD
benchmark_type: Large-cap equity index
weighting_method: Market-cap-weighted
return_type: Price return or total return
data_source: Market data provider
is_tradable_proxy: false
proxy_symbol: SPY
```

For Athena's first version, the most important fields are:

```text
benchmark_name
benchmark_symbol
asset_class
currency
region
historical_values
proxy_symbol
```

---

### Benchmark mapping in Athena

Benchmark mapping means assigning the right benchmark to each asset, ETF or portfolio.

Example:

```text
AAPL → S&P 500 or Nasdaq-100
RY.TO → TSX Composite
AIR.PA → CAC 40 or STOXX Europe 600
SPY → S&P 500
QQQ → Nasdaq-100
```

For portfolios, benchmark mapping may depend on the portfolio strategy.

Example:

```text
US equity portfolio → S&P 500
Global equity portfolio → MSCI World
Balanced portfolio → custom 60/40 benchmark
```

Athena should allow benchmark mapping because the same asset can be analyzed against different references depending on the use case.

---

### Possible Athena features

Athena AI Risk Terminal could use benchmarks to support:

```text
Portfolio vs benchmark return comparison
Asset vs benchmark comparison
Excess return calculation
Tracking error calculation
Information ratio calculation
Benchmark volatility comparison
Benchmark drawdown comparison
Sector exposure vs benchmark
Currency exposure vs benchmark
Benchmark selection warnings
```

Example warning:

```text
Warning:
The selected benchmark may not match the portfolio's asset universe.
Portfolio region: Canada
Benchmark region: United States
```

This would help prevent misleading analysis.

---

### Simple benchmark comparison example

Assume:

```text
Portfolio return = 8%
Benchmark return = 12%
```

Then:

```text
Excess return = 8% - 12%
Excess return = -4%
```

The portfolio underperformed by 4 percentage points.

Another example:

```text
Portfolio return = -3%
Benchmark return = -10%
```

Then:

```text
Excess return = -3% - (-10%)
Excess return = +7%
```

The portfolio outperformed by 7 percentage points, even though the return was negative.

---

### Good benchmark vs bad benchmark

Good benchmark example:

```text
Portfolio:
Canadian large-cap equity stocks

Benchmark:
TSX Composite
```

Why it is good:

```text
Same country
Same broad asset class
Representative of Canadian equities
Relevant for comparison
```

Bad benchmark example:

```text
Portfolio:
Canadian large-cap equity stocks

Benchmark:
Nasdaq-100
```

Why it is weak:

```text
Different country
Different sector exposure
Different currency
Different investment universe
```

The comparison may still be interesting as market context, but it should not be the primary benchmark.

---

### CFA Level 1 takeaway

For CFA Level 1, benchmarks are important because they provide context for performance evaluation.

Important concepts include:

```text
Benchmark
Absolute return
Relative return
Excess return
Active return
Outperformance
Underperformance
Tracking error
Information ratio
Benchmark selection
Benchmark mismatch
Active management
Passive management
```

A simple memory rule:

```text
Benchmark = reference used to judge performance
```

Another useful rule:

```text
Positive return does not always mean good performance.
Negative return does not always mean bad relative performance.
```

The benchmark determines the context.

---

### Athena implementation takeaway

For Athena, benchmarks are essential for meaningful performance and risk analysis.

A portfolio return alone is incomplete.

Athena should compare assets and portfolios with relevant benchmarks to show:

```text
Whether the investment outperformed or underperformed
How much excess return was generated
Whether the benchmark is appropriate
How much active risk was taken
How portfolio exposures differ from the benchmark
```

Possible backend calculations:

```text
benchmark_return
portfolio_return
excess_return
tracking_error
information_ratio
benchmark_volatility
relative_drawdown
```

Possible frontend components:

```text
Portfolio vs Benchmark chart
Excess Return card
Benchmark Selection panel
Tracking Error card
Information Ratio card
Sector vs Benchmark exposure chart
Currency vs Benchmark exposure chart
```

The goal is to make performance analysis more professional and realistic.

---

### Mini revision questions

1. What is a benchmark?

2. Why does performance need context?

3. What is the difference between absolute performance and relative performance?

4. What does it mean to outperform a benchmark?

5. What does it mean to underperform a benchmark?

6. What are the characteristics of a good benchmark?

7. Why is benchmark selection important?

8. What is excess return?

9. What is tracking error?

10. What is the difference between active and passive management?

11. Why can benchmark mismatch be dangerous?

12. Why are benchmarks useful for Athena?

---

### Mini answers

1. A benchmark is a reference used to evaluate performance.

2. Performance needs context because a return can look good or bad depending on the market reference.

3. Absolute performance is the return by itself. Relative performance compares the return with a benchmark.

4. Outperforming means earning a higher return than the benchmark.

5. Underperforming means earning a lower return than the benchmark.

6. A good benchmark should be relevant, representative or investable, transparent, consistent with the strategy and appropriate for the asset universe.

7. Benchmark selection is important because the wrong benchmark can make performance analysis misleading.

8. Excess return is the portfolio return minus the benchmark return.

9. Tracking error measures how much the portfolio's returns deviate from the benchmark's returns over time.

10. Active management tries to outperform a benchmark, while passive management tries to track a benchmark.

11. Benchmark mismatch is dangerous because it can create unfair or misleading conclusions.

12. Benchmarks are useful for Athena because they allow portfolio and asset performance to be evaluated in context.

---

### Section summary

A benchmark is a reference used to evaluate performance.

It gives meaning to returns by comparing them with an appropriate market or strategy reference.

For CFA Level 1, benchmarks are important because they connect performance evaluation, active management, passive management, excess return and tracking error.

For Athena AI Risk Terminal, benchmarks are essential because the platform should not only show whether a portfolio made money, but also whether it performed well compared with the right reference.

The key lesson is:

```text
Performance without a benchmark has no context.
A benchmark turns raw return into meaningful performance analysis.
```


---

























## 36. Index construction basics

Indices can be built in different ways.

The construction method affects how the index behaves, which securities have the most influence, and how investors should interpret the index return.

In simple terms, index construction answers the question:

```text
How is the index calculated?
```

This matters because two indices can contain similar securities but behave differently if they use different weighting methods.

Common index construction methods include:

```text
Price-weighted index
Market-cap-weighted index
Equal-weighted index
Factor-weighted index
Fundamental-weighted index
```

For CFA Level 1 and for Athena AI Risk Terminal, the most important methods to understand first are:

```text
Price-weighted
Market-cap-weighted
Equal-weighted
```

A simple idea:

```text
Index construction determines which companies drive the index.
```

---

### Why index construction matters

Index construction matters because the same market can be represented in different ways.

Example:

```text
Index A contains 100 stocks.
Index B contains the same 100 stocks.
```

At first, they may look similar.

But if Index A is market-cap-weighted and Index B is equal-weighted, they may produce different returns.

Why?

Because the weights are different.

In one index, large companies may dominate.

In the other index, every company has the same importance.

Simple idea:

```text
Same stocks does not always mean same index behavior.
```

Index construction affects:

```text
Return
Risk
Sector exposure
Concentration
Diversification
Turnover
Rebalancing
Benchmark interpretation
```

For Athena, understanding index construction is important because benchmark comparison can be misleading if the benchmark structure is not understood.

---

### Index constituents

The securities included in an index are called constituents.

Example:

```text
An equity index may include:
Apple
Microsoft
Nvidia
JPMorgan
Amazon
Tesla
```

Each constituent has a weight.

The weight determines how much that security influences the index.

Example:

```text
Stock A weight = 8%
Stock B weight = 0.5%
```

A price movement in Stock A will have a much larger effect on the index than the same percentage movement in Stock B.

Simple idea:

```text
Constituent = security inside the index
Weight = importance of that security in the index
```

---

### Index weight

An index weight is the percentage of the index represented by one constituent.

Example:

```text
Company A weight = 6%
Company B weight = 2%
Company C weight = 1%
```

The sum of all weights should equal:

```text
100%
```

Weights are important because they explain what drives index performance.

Example:

```text
If a stock has a 10% index weight,
its movement matters much more than a stock with a 0.2% weight.
```

This is why large index constituents can strongly influence benchmark returns.

---

### Price-weighted index

In a price-weighted index, higher-priced stocks have more influence.

The index gives more weight to stocks with higher share prices.

Example:

```text
Stock A price = 300
Stock B price = 50
```

Stock A has more impact on the index because its share price is higher.

Simple idea:

```text
Higher share price = higher index influence
```

This method does not directly consider company size.

A company with a high share price can have more influence than a much larger company with a lower share price.

---

### Price-weighted index example

Assume an index has three stocks:

```text
Stock A price = 100
Stock B price = 50
Stock C price = 25
```

A simple price-weighted index can be based on the average price:

```text
Index level = (100 + 50 + 25) / 3
Index level = 58.33
```

Now assume Stock A rises by 10:

```text
Stock A price = 110
Stock B price = 50
Stock C price = 25
```

New index level:

```text
Index level = (110 + 50 + 25) / 3
Index level = 61.67
```

Stock A has a strong effect because its price is high.

If Stock C rises by 10 instead:

```text
Stock A price = 100
Stock B price = 50
Stock C price = 35
```

New index level:

```text
Index level = (100 + 50 + 35) / 3
Index level = 61.67
```

In this simplified example, the same dollar change has the same effect.

That is the key point of price weighting:

```text
Dollar price changes matter more than percentage changes.
```

---

### Weakness of price-weighted indices

Price-weighted indices can be easy to understand, but they have weaknesses.

The main weakness is that share price does not necessarily reflect company size.

Example:

```text
Company A share price = 300
Company B share price = 50
```

Company A is not automatically bigger or more important than Company B.

Company size depends on market capitalization:

```text
Market capitalization = share price × shares outstanding
```

A company can have a high share price but fewer shares outstanding.

Another company can have a lower share price but many more shares outstanding.

This is why price-weighted indices can sometimes give unusual weights.

---

### Stock splits and price-weighted indices

A stock split can affect the weight of a stock in a price-weighted index.

Example:

```text
Before split:
Stock price = 300

After 3-for-1 split:
Stock price = 100
```

The economic value of the company did not change because of the split.

But in a price-weighted index, the stock's influence may decrease because the share price is now lower.

This is one reason price-weighted indices require adjustment mechanisms.

Simple idea:

```text
A stock split changes the share price,
but not the company value.
```

---

### Market-cap-weighted index

In a market-cap-weighted index, larger companies have more influence.

Market capitalization is:

```text
Market cap = share price × number of shares outstanding
```

Example:

```text
Company A market cap = 2 trillion
Company B market cap = 50 billion
```

Company A has more influence because its total market value is much larger.

This is the most common index construction method.

Simple idea:

```text
Bigger company = bigger index weight
```

Many major indices use market-cap weighting.

Examples:

```text
S&P 500
Nasdaq-100
MSCI World
TSX Composite
CAC 40
```

---

### Market-cap-weighted index example

Assume an index has three companies:

```text
Company A market cap = 500 billion
Company B market cap = 300 billion
Company C market cap = 200 billion
```

Total market cap:

```text
Total market cap = 500 + 300 + 200
Total market cap = 1,000 billion
```

Weights:

```text
Company A weight = 500 / 1,000 = 50%
Company B weight = 300 / 1,000 = 30%
Company C weight = 200 / 1,000 = 20%
```

If Company A moves strongly, the index will be affected more than if Company C moves.

This is because Company A has the highest weight.

---

### Free-float market-cap weighting

Many market-cap-weighted indices use free-float market capitalization.

Free float refers to shares that are available for public trading.

Some shares may not be freely traded because they are held by:

```text
Founders
Governments
Strategic investors
Company insiders
Long-term controlling shareholders
```

Simple idea:

```text
Free-float market cap = share price × publicly tradable shares
```

Free-float adjustment makes the index more realistic because it focuses on shares that investors can actually trade.

Example:

```text
Company total shares = 1,000 million
Publicly tradable shares = 600 million
```

The free float is 60%.

An index provider may use only the tradable portion to calculate the index weight.

---

### Strengths of market-cap weighting

Market-cap weighting has several advantages.

```text
It reflects company size.
It is widely used.
It is easy to replicate.
It usually has lower turnover.
It naturally adjusts as market values change.
It is practical for passive investing.
```

Example:

```text
If a company grows in market value,
its index weight increases naturally.
```

This makes market-cap-weighted indices useful for ETFs and passive strategies.

---

### Weaknesses of market-cap weighting

Market-cap weighting also has weaknesses.

The main weakness is concentration.

Large companies can dominate the index.

Example:

```text
Top 10 stocks = 35% of the index
Remaining stocks = 65% of the index
```

If the largest stocks are concentrated in one sector, the index may become heavily exposed to that sector.

Example:

```text
A broad equity index may still be strongly influenced by technology stocks.
```

Another weakness is that market-cap weighting gives more weight to companies whose prices have already increased.

Simple idea:

```text
Market-cap weighting can overweight expensive or popular companies.
```

This does not mean the method is bad, but users must understand its behavior.

---

### Equal-weighted index

In an equal-weighted index, every constituent has the same weight.

Example:

```text
100 stocks
Each stock weight = 1%
```

This means each company contributes equally to the index return at the rebalancing date.

Simple idea:

```text
Every company has equal importance.
```

This is different from market-cap weighting, where large companies dominate.

---

### Equal-weighted index example

Assume an index has five stocks.

In an equal-weighted index:

```text
Stock A weight = 20%
Stock B weight = 20%
Stock C weight = 20%
Stock D weight = 20%
Stock E weight = 20%
```

If one stock performs very well, its weight may rise above 20%.

Example:

```text
Stock A weight after price increase = 24%
```

At the next rebalancing, the index may sell part of Stock A and buy more of the other stocks to return to equal weights.

This creates a rebalancing effect.

---

### Strengths of equal-weighted indices

Equal-weighted indices have several advantages.

```text
They reduce concentration in the largest companies.
They give more importance to smaller constituents.
They may provide broader participation.
They can reduce dominance by a few mega-cap stocks.
```

Example:

```text
In a market-cap-weighted index,
one very large company may dominate.

In an equal-weighted index,
that company receives the same weight as every other company.
```

This can make the index more diversified by constituent weight.

---

### Weaknesses of equal-weighted indices

Equal-weighted indices also have disadvantages.

They usually require more rebalancing.

Rebalancing creates:

```text
Higher turnover
Higher transaction costs
More trading
Potential tax effects
```

Equal-weighted indices may also have more exposure to smaller companies.

This can increase:

```text
Volatility
Liquidity risk
Small-cap exposure
Trading costs
```

Simple idea:

```text
Equal weighting reduces large-company concentration,
but it may increase turnover and exposure to smaller companies.
```

---

### Rebalancing

Rebalancing is the process of adjusting index weights back to target weights.

Example for an equal-weighted index:

```text
Target weight for each stock = 1%
```

After market movements, some stocks may become larger or smaller in the index.

Rebalancing restores the target structure.

Example:

```text
Stock A weight before rebalancing = 1.5%
Target weight = 1.0%

The index reduces Stock A's weight.
```

Rebalancing matters because it affects index behavior and transaction costs.

---

### Reconstitution

Reconstitution is the process of changing the list of index constituents.

Example:

```text
One company is removed from the index.
Another company is added.
```

This can happen when a company no longer meets the index rules.

Possible reasons include:

```text
Market capitalization changes
Liquidity changes
Sector classification changes
Bankruptcy
Merger or acquisition
Listing changes
Eligibility rules
```

Simple distinction:

```text
Rebalancing = changing weights
Reconstitution = changing constituents
```

---

### Price return index

A price return index includes only price changes.

It does not include dividends or other income.

Simple idea:

```text
Price return index = capital appreciation only
```

Example:

```text
Index starts at 1,000
Index ends at 1,080
```

Price return:

```text
Price return = 1,080 / 1,000 - 1
Price return = 8%
```

If the companies also paid dividends, those dividends are not included in the price return index.

---

### Total return index

A total return index includes price changes and reinvested income.

Simple idea:

```text
Total return index = price movement + reinvested dividends
```

Example:

```text
Price return = 8%
Dividend contribution = 2%
```

Total return:

```text
Total return = 10%
```

A total return index gives a more complete view of investor performance because it includes income.

For long-term analysis, total return indices are usually more useful than price return indices.

---

### Price return vs total return index

The distinction between price return and total return is important.

Simple comparison:

```text
Price return index:
Includes only price changes.

Total return index:
Includes price changes and reinvested income.
```

Example:

```text
Index start value = 1,000
Index end price value = 1,080
Dividends = 20
```

Price return:

```text
Price return = 1,080 / 1,000 - 1
Price return = 8%
```

Total return:

```text
Total return = (1,080 + 20) / 1,000 - 1
Total return = 10%
```

The total return is higher because it includes dividends.

Simple idea:

```text
Price return can understate long-term investment performance.
```

---

### Gross total return vs net total return

Some indices also distinguish between gross total return and net total return.

Gross total return includes reinvested income before withholding taxes.

Net total return includes reinvested income after withholding taxes.

Simple comparison:

```text
Gross total return = dividends reinvested before tax
Net total return = dividends reinvested after withholding tax
```

This matters especially for international indices where dividend taxation can affect investor returns.

For a beginner version of Athena, it is enough to understand that total return includes income.

A more advanced version can distinguish between gross and net return.

---

### Index concentration

Index concentration means that a small number of constituents represent a large part of the index.

Example:

```text
Top 5 stocks = 25% of the index
Top 10 stocks = 35% of the index
```

Concentration matters because the index may depend heavily on a few companies.

Example:

```text
If the largest technology stocks fall,
a concentrated index may fall significantly.
```

Market-cap-weighted indices can become concentrated when a few companies become very large.

Equal-weighted indices usually reduce this type of concentration.

---

### Sector concentration

Sector concentration means that an index is heavily exposed to one or a few sectors.

Examples of sectors:

```text
Technology
Financials
Energy
Healthcare
Industrials
Consumer discretionary
Utilities
Materials
Real estate
Communication services
```

Example:

```text
Technology weight = 40%
Energy weight = 5%
```

This index is strongly exposed to technology.

Sector concentration is important for risk analysis because sectors can behave differently across market cycles.

---

### Index turnover

Index turnover measures how much the index changes over time.

Turnover can come from:

```text
Rebalancing
Reconstitution
Changes in weights
Changes in constituents
Corporate actions
```

High turnover can increase trading costs for funds that track the index.

Example:

```text
An ETF tracking a high-turnover index may need to trade frequently.
```

This can create higher transaction costs and possibly higher tracking error.

---

### Corporate actions and index construction

Corporate actions can affect index construction.

Examples:

```text
Stock splits
Dividends
Mergers
Acquisitions
Spin-offs
Share buybacks
New share issuance
Delistings
```

Index providers adjust index calculations to avoid artificial distortions.

Example:

```text
A stock split lowers the share price,
but it does not reduce the company's economic value.
```

The index methodology must handle this correctly.

For Athena, corporate actions are also important for clean historical analysis.

---

### Index divisor

Some indices use an index divisor to maintain continuity.

The divisor is an adjustment factor used to prevent artificial jumps in the index level when structural changes happen.

Example:

```text
A stock split occurs.
A company is added or removed.
A special dividend is paid.
```

The divisor may be adjusted so that the index does not move only because of a technical change.

Simple idea:

```text
Index divisor helps keep the index level consistent over time.
```

For CFA Level 1, the key point is not to calculate complex divisors manually, but to understand why adjustments are needed.

---

### Index construction comparison

A simple comparison:

```text
Price-weighted index:
Higher-priced stocks have more influence.

Market-cap-weighted index:
Larger companies have more influence.

Equal-weighted index:
Every constituent has the same weight.
```

Another comparison:

```text
Price-weighted:
Simple, but share price can be misleading.

Market-cap-weighted:
Common and practical, but can become concentrated.

Equal-weighted:
Reduces large-company dominance, but requires more rebalancing.
```

---

### Example with the same three stocks

Assume three stocks:

```text
Stock A price = 100
Stock B price = 50
Stock C price = 25
```

And market capitalizations:

```text
Stock A market cap = 100 billion
Stock B market cap = 300 billion
Stock C market cap = 600 billion
```

In a price-weighted index, Stock A has the most influence because it has the highest share price.

In a market-cap-weighted index, Stock C has the most influence because it has the highest market capitalization.

In an equal-weighted index, all three stocks have the same weight:

```text
Stock A weight = 33.33%
Stock B weight = 33.33%
Stock C weight = 33.33%
```

This shows why index construction matters.

The same stocks can produce different index behavior depending on the weighting method.

---

### Benchmark interpretation

Index construction is important for benchmark interpretation.

Example:

```text
Portfolio return = 8%
Benchmark return = 10%
```

Before saying the portfolio underperformed, an analyst should understand what the benchmark represents.

Questions to ask:

```text
Is the benchmark market-cap-weighted?
Is it equal-weighted?
Is it concentrated in a few stocks?
Does it include dividends?
Is it price return or total return?
Does it match the portfolio universe?
```

A benchmark is only useful if its construction is understood.

---

### Index construction and ETFs

Many ETFs track indices.

The ETF inherits the index methodology.

Example:

```text
An ETF tracking a market-cap-weighted index
will usually be more exposed to the largest companies.
```

Another example:

```text
An ETF tracking an equal-weighted index
will usually rebalance more often.
```

This matters because two ETFs may cover the same market but behave differently.

Example:

```text
S&P 500 market-cap-weighted ETF
S&P 500 equal-weighted ETF
```

Both may hold the same 500 companies, but their weights and returns can differ.

---

### Index construction in Athena

For Athena AI Risk Terminal, index construction should be stored and displayed when benchmarks are used.

Possible benchmark fields:

```text
benchmark_symbol
benchmark_name
asset_class
region
currency
constituents_count
weighting_method
return_type
rebalancing_frequency
data_source
```

Example:

```text
benchmark_symbol: SPX
benchmark_name: S&P 500 Index
asset_class: Equity
region: United States
currency: USD
weighting_method: Market-cap-weighted
return_type: Price return
rebalancing_frequency: Quarterly
```

For Athena's first version, the most important fields are:

```text
benchmark_name
benchmark_symbol
weighting_method
return_type
currency
historical_values
```

---

### Possible Athena features

Athena could use index construction data to improve benchmark analysis.

Possible features:

```text
Display benchmark weighting method
Show price return vs total return label
Compare portfolio weights with benchmark weights
Flag benchmark concentration risk
Show top benchmark constituents
Show sector exposure of benchmark
Explain benchmark mismatch
Calculate benchmark returns consistently
```

Example warning:

```text
Warning:
The selected benchmark is price return only.
It may understate long-term performance compared with a total return benchmark.
```

Another warning:

```text
Warning:
The benchmark is highly concentrated in its top constituents.
Portfolio comparison may be driven by a small number of large companies.
```

This would make Athena more useful for professional-style analysis.

---

### CFA Level 1 takeaway

For CFA Level 1, index construction is important because the weighting method affects index performance and interpretation.

Important concepts include:

```text
Index constituent
Index weight
Price-weighted index
Market-cap-weighted index
Equal-weighted index
Price return index
Total return index
Rebalancing
Reconstitution
Index concentration
Sector concentration
Index divisor
Corporate actions
```

A simple memory rule:

```text
Price-weighted = higher share price matters more
Market-cap-weighted = bigger company matters more
Equal-weighted = every company matters equally
```

Another useful rule:

```text
Price return excludes dividends.
Total return includes reinvested income.
```

---

### Athena implementation takeaway

For Athena, index construction is important because benchmarks should not be treated as black boxes.

A benchmark has a structure.

That structure affects performance, risk and interpretation.

Athena should store and display index construction information so users understand what they are comparing against.

Possible backend logic:

```text
benchmark_weighting_method
benchmark_return_type
benchmark_constituent_weights
benchmark_rebalancing_frequency
benchmark_concentration_metrics
```

Possible frontend components:

```text
Benchmark Methodology card
Index Weighting badge
Price Return vs Total Return label
Top Constituents table
Sector Exposure chart
Benchmark Concentration warning
```

The goal is to make benchmark analysis more transparent.

---

### Mini revision questions

1. What does index construction mean?

2. Why does the construction method affect index behavior?

3. What is a constituent?

4. What is an index weight?

5. How does a price-weighted index work?

6. What is the weakness of a price-weighted index?

7. How does a market-cap-weighted index work?

8. Why can market-cap-weighted indices become concentrated?

9. How does an equal-weighted index work?

10. What is the difference between rebalancing and reconstitution?

11. What is the difference between a price return index and a total return index?

12. Why should Athena store the weighting method of a benchmark?

---

### Mini answers

1. Index construction means the method used to build and calculate an index.

2. The construction method affects index behavior because it determines which securities have the most influence.

3. A constituent is a security included in an index.

4. An index weight is the percentage of the index represented by one constituent.

5. A price-weighted index gives more influence to stocks with higher share prices.

6. Its weakness is that share price does not necessarily reflect company size.

7. A market-cap-weighted index gives more influence to companies with larger market capitalization.

8. It can become concentrated because very large companies may represent a large part of the index.

9. An equal-weighted index gives every constituent the same weight.

10. Rebalancing changes weights, while reconstitution changes the list of constituents.

11. A price return index includes only price changes, while a total return index includes price changes and reinvested income.

12. Athena should store the weighting method because benchmark behavior depends on how the index is constructed.

---

### Section summary

Indices can be constructed in different ways.

The main methods are price-weighted, market-cap-weighted and equal-weighted.

Each method gives different importance to different constituents.

For CFA Level 1, index construction is important because it explains why benchmarks can behave differently even when they represent similar markets.

For Athena AI Risk Terminal, index construction is important because benchmark analysis should be transparent and realistic.

The key lesson is:

```text
An index is not just a list of securities.
Its construction method determines how it behaves.
```


---































## 37. Market efficiency basics

Market efficiency describes how quickly and accurately market prices reflect information.

In simple terms, market efficiency asks the question:

```text
Do market prices already include the information available to investors?
```

If markets are efficient, prices adjust quickly when new information becomes available.

This means that it can be difficult to consistently outperform the market without:

```text
Taking additional risk
Having better information
Using better analysis
Reacting faster than other investors
Accepting higher uncertainty
```

Market efficiency is an important idea in finance because it connects directly to:

```text
Active investing
Passive investing
Security analysis
Market prices
Information
Risk and return
Portfolio management
```

For Athena AI Risk Terminal, market efficiency matters because it helps explain why a price should not be treated as random or meaningless.

A market price is usually the result of many investors processing information and trading.

Simple idea:

```text
Market price = information + expectations + trading activity
```

---

### Basic idea

The basic idea of market efficiency is that prices reflect available information.

If many investors analyze the same information, trade on it, and compete with each other, prices may adjust quickly.

Example:

```text
A company announces better-than-expected earnings.
Investors react quickly.
The stock price rises shortly after the announcement.
```

In an efficient market, the price should adjust rapidly to the new information.

This makes it difficult for an investor to profit after the information is already public.

Simple idea:

```text
If everyone already knows the information,
the price may already reflect it.
```

---

### Why market efficiency matters

Market efficiency matters because it affects how investors think about performance.

If markets are highly efficient, it is harder to consistently find mispriced securities.

This supports the idea of passive investing.

If markets are less efficient, active investors may have more opportunity to find undervalued or overvalued assets.

Market efficiency affects decisions such as:

```text
Should I try to pick individual stocks?
Should I invest in an index fund?
Can technical analysis work?
Can public news create trading opportunities?
Is active management worth the cost?
```

For a risk platform like Athena, market efficiency helps explain why benchmark comparison and risk-adjusted performance are important.

A portfolio should not only be judged by return.

It should also be judged by:

```text
Risk taken
Benchmark used
Costs paid
Information used
Consistency of performance
```

---

### Efficient Market Hypothesis

The Efficient Market Hypothesis, or EMH, is the theory that market prices reflect information.

It does not mean prices are always perfect.

It means that prices reflect information quickly enough that consistent abnormal profits are difficult to achieve.

Simple idea:

```text
EMH = prices reflect information
```

Important clarification:

```text
Efficient market does not mean correct market.
Efficient market means information is rapidly incorporated into prices.
```

Prices can still move, markets can still crash, and investors can still disagree.

Efficiency is about information processing, not perfection.

---

### Market price and intrinsic value

Market efficiency is related to the difference between market price and intrinsic value.

```text
Market price = price observed in the market
Intrinsic value = estimated true economic value
```

In an efficient market, the market price should be close to intrinsic value most of the time.

However, price and value can still differ.

Example:

```text
Market price = 80
Analyst estimated value = 100
```

The analyst may believe the asset is undervalued.

But if the market is efficient, finding this type of opportunity consistently is difficult.

Simple idea:

```text
Active investors search for gaps between price and value.
Market efficiency says those gaps are hard to find and exploit consistently.
```

---

### Information and prices

Market prices can reflect many types of information.

Examples:

```text
Historical prices
Trading volume
Earnings reports
Interest rates
Inflation data
Economic growth
Company news
Analyst forecasts
Regulatory announcements
Geopolitical events
Investor expectations
```

The more information prices reflect, the stronger the form of market efficiency.

This is why market efficiency is usually divided into three forms:

```text
Weak form
Semi-strong form
Strong form
```

---

### Forms of market efficiency

The common forms of market efficiency are:

```text
Weak form
Semi-strong form
Strong form
```

Each form describes a different level of information included in prices.

Simple comparison:

```text
Weak form:
Prices reflect past market data.

Semi-strong form:
Prices reflect all publicly available information.

Strong form:
Prices reflect all public and private information.
```

The stronger the form, the more information is assumed to be included in prices.

---

### Weak form efficiency

Weak form efficiency means that prices reflect past market data.

Past market data includes:

```text
Historical prices
Historical returns
Trading volume
Past price patterns
```

If weak-form efficiency holds, historical prices alone should not reliably predict future returns.

Simple idea:

```text
Past prices are already reflected in current prices.
```

This challenges simple technical analysis strategies that rely only on past price patterns.

Example:

```text
A stock increased for five days in a row.
An investor buys only because the stock increased for five days.
```

If weak-form efficiency holds, this pattern alone should not provide a reliable advantage.

---

### Weak form example

Assume a stock has the following daily returns:

```text
Day 1: +1%
Day 2: +2%
Day 3: +1%
Day 4: +3%
```

A beginner may think:

```text
The stock has been going up.
It will probably continue going up tomorrow.
```

Weak-form efficiency suggests that this past price information is already known and reflected in the current price.

Therefore, the pattern alone should not reliably predict tomorrow's return.

This does not mean prices cannot trend.

It means that simple historical patterns should not create easy, consistent profits after costs and risk.

---

### Weak form and technical analysis

Technical analysis studies past prices, charts and volume to make trading decisions.

Weak-form efficiency does not say that every technical strategy is useless.

But it does suggest that simple price patterns should not be easy sources of consistent abnormal return.

Examples of technical signals:

```text
Moving averages
Support and resistance
Momentum indicators
Chart patterns
Volume signals
```

If a signal is obvious and widely used, market participants may trade on it quickly.

This can reduce its effectiveness.

Simple idea:

```text
The more obvious a pattern is,
the less likely it is to be a free opportunity.
```

---

### Semi-strong form efficiency

Semi-strong form efficiency means that prices reflect all publicly available information.

Public information includes:

```text
Financial statements
Earnings announcements
News releases
Economic data
Interest rate decisions
Analyst reports
Public company guidance
Industry news
Regulatory filings
```

If semi-strong efficiency holds, public news is quickly incorporated into prices.

Simple idea:

```text
Public information should already be reflected in market prices.
```

This means it is difficult to consistently outperform by trading on public information after it has been released.

---

### Semi-strong form example

Assume a company announces strong earnings at 8:00 AM.

The news is public.

Many investors, analysts and trading systems react quickly.

By the time a beginner reads the news later in the day, the stock price may already have adjusted.

Example:

```text
Before announcement: stock price = 100
After announcement: stock price = 108
```

The market may have already incorporated the good news.

Buying after the price adjustment does not guarantee an easy profit.

Simple idea:

```text
Good news does not automatically mean good trade
if the price already moved.
```

---

### Semi-strong form and fundamental analysis

Fundamental analysis estimates the value of an asset using economic and financial information.

Examples:

```text
Revenue
Earnings
Cash flows
Margins
Growth
Interest rates
Competitive position
Valuation ratios
```

Semi-strong efficiency suggests that public fundamental information is quickly reflected in prices.

This makes it harder for analysts to outperform using only public information.

However, active investors may still try to outperform by:

```text
Interpreting information better
Forecasting future results better
Understanding business quality better
Reacting faster
Focusing on less-covered securities
Using a longer time horizon
```

Market efficiency does not eliminate analysis.

It makes the competition harder.

---

### Strong form efficiency

Strong form efficiency means that prices reflect all public and private information.

Private information includes non-public information known only to insiders or selected individuals.

Examples:

```text
Confidential merger discussions
Non-public earnings information
Internal company forecasts
Private regulatory information
Secret strategic decisions
```

If strong-form efficiency held perfectly, even insiders could not earn abnormal returns from private information.

This is the strongest form of market efficiency.

It is also the most unrealistic form in practice.

Simple idea:

```text
Strong form = prices reflect everything, even private information.
```

---

### Why strong form is unrealistic

Strong form efficiency is unrealistic because private information can exist before it becomes public.

Example:

```text
Company insiders may know about a major acquisition before the market knows.
```

If they traded on that information, they might have an unfair advantage.

This is why securities laws often prohibit insider trading.

The existence of insider trading rules suggests that private information can be valuable and is not always reflected in prices immediately.

For CFA Level 1, the key point is:

```text
Strong-form efficiency is the strongest theoretical form,
but it does not perfectly describe real markets.
```

---

### Comparing the three forms

A simple comparison:

```text
Weak form:
Prices reflect past price and volume data.

Semi-strong form:
Prices reflect all public information.

Strong form:
Prices reflect all public and private information.
```

Another way to remember:

```text
Weak = past market data
Semi-strong = public information
Strong = public + private information
```

The forms are cumulative.

If a market is semi-strong efficient, it should also be weak-form efficient.

If a market is strong-form efficient, it should also be semi-strong and weak-form efficient.

---

### Market efficiency and active investing

Active investing tries to outperform a benchmark.

Active investors may use:

```text
Security selection
Market timing
Sector allocation
Factor exposure
Fundamental analysis
Quantitative models
Alternative data
Macroeconomic views
```

Market efficiency makes active investing difficult because many investors are competing to find opportunities.

Simple idea:

```text
If many smart investors search for mispricing,
obvious opportunities disappear quickly.
```

This does not mean active investing cannot work.

It means that consistent outperformance requires skill, discipline, information advantage, risk-taking, or a market segment where inefficiencies exist.

---

### Market efficiency and passive investing

Market efficiency is one reason passive investing exists.

If it is difficult to beat the market consistently, some investors choose to track the market instead.

Passive investing usually aims to match a benchmark.

Examples:

```text
S&P 500 index fund
Nasdaq-100 ETF
Global equity ETF
Bond index fund
```

Passive investors often focus on:

```text
Low fees
Broad diversification
Benchmark tracking
Long-term discipline
Tax efficiency
Simple implementation
```

Simple idea:

```text
If beating the market is difficult,
owning the market may be a rational choice.
```

---

### Active vs passive investing

Active and passive investing are different responses to market efficiency.

```text
Active investing:
Try to outperform the benchmark.

Passive investing:
Try to track the benchmark.
```

Active management may be more attractive when:

```text
Markets are less efficient
Information is harder to process
Securities are less covered
Costs are reasonable
Manager skill is strong
```

Passive management may be more attractive when:

```text
Markets are highly efficient
Fees matter a lot
Diversification is desired
The investor wants simplicity
The investor accepts market return
```

There is no universal answer.

The best choice depends on the investor's objective, skill, cost sensitivity, risk tolerance and market segment.

---

### Market anomalies

A market anomaly is a pattern that seems inconsistent with market efficiency.

Examples often discussed in finance include:

```text
Momentum
Value effect
Size effect
Low-volatility effect
Post-earnings announcement drift
Calendar effects
```

An anomaly may suggest that markets are not perfectly efficient.

However, anomalies can weaken or disappear after they become widely known.

They may also reflect hidden risk, data mining, trading costs or behavioral biases.

Simple idea:

```text
An anomaly is not automatically free money.
```

For Athena, anomalies could be studied later through factor analytics or quantitative research modules.

---

### Behavioral finance and market efficiency

Behavioral finance studies how psychology affects financial decisions.

It challenges the idea that investors are always perfectly rational.

Examples of behavioral biases:

```text
Overconfidence
Herding
Loss aversion
Anchoring
Confirmation bias
Recency bias
Fear and greed
```

These biases can cause prices to deviate from fundamental value.

Example:

```text
Investors may overreact to bad news during a panic.
```

Behavioral finance does not completely reject market efficiency.

It shows that real markets can be affected by human behavior, especially in the short term.

---

### Efficient does not mean predictable

A common beginner mistake is to think that efficient markets are easy to predict.

That is the opposite.

If markets are efficient, prices already reflect available information.

Future price changes depend mostly on new information.

New information is uncertain.

Therefore, future returns are difficult to predict.

Simple idea:

```text
Efficient markets are hard to beat because new information is hard to predict.
```

---

### Efficient does not mean risk-free

Another common mistake is to think that efficient markets are safe.

Market efficiency does not remove risk.

Even in an efficient market, prices can fall sharply.

Example:

```text
An efficient stock market can still crash
if new information changes investor expectations.
```

Efficiency means information is reflected in prices.

It does not mean investors cannot lose money.

Simple idea:

```text
Efficient market ≠ risk-free market
```

---

### Efficient does not mean prices are always correct

Market prices can be wrong in hindsight.

Example:

```text
A stock trades at 100 today.
One year later, it trades at 50.
```

This does not automatically prove the market was inefficient at 100.

At the time, investors used the information available.

Later, new information changed expectations.

Simple idea:

```text
A price can be efficient given current information,
even if it later turns out to be wrong.
```

---

### Market efficiency and risk-adjusted return

When evaluating performance, it is not enough to ask:

```text
Did the portfolio beat the market?
```

It is also important to ask:

```text
How much risk was taken?
Was the outperformance due to skill or risk exposure?
Were fees and transaction costs included?
Was the benchmark appropriate?
```

An investor may outperform by taking more risk.

Example:

```text
Portfolio return = 12%
Benchmark return = 8%
```

This looks good.

But if the portfolio had much higher volatility or leverage, the comparison is incomplete.

Market efficiency connects naturally with risk-adjusted performance.

---

### Market efficiency and transaction costs

Even if a trading strategy appears profitable before costs, it may not be profitable after costs.

Costs include:

```text
Bid-ask spread
Commissions
Slippage
Market impact
Taxes
Management fees
```

In efficient markets, small opportunities may disappear after transaction costs.

Simple idea:

```text
A strategy must beat the market after costs, not before costs.
```

For Athena, this is important because theoretical returns should be interpreted carefully.

---

### Market efficiency in Athena

Athena AI Risk Terminal does not need to prove whether markets are efficient.

However, it should help users analyze performance realistically.

Market efficiency can influence Athena features such as:

```text
Benchmark comparison
Risk-adjusted performance
Passive vs active comparison
Excess return calculation
Information ratio
Tracking error
Transaction cost awareness
Factor exposure analysis
```

Athena should avoid presenting raw return as enough evidence of skill.

Example:

```text
Portfolio return = 15%
```

This should be compared with:

```text
Benchmark return
Portfolio volatility
Maximum drawdown
Factor exposure
Transaction costs
Time period
```

This makes the analysis more professional.

---

### Possible Athena features

Possible features related to market efficiency:

```text
Portfolio vs benchmark comparison
Excess return analysis
Active return chart
Tracking error calculation
Information ratio calculation
Risk-adjusted return metrics
Passive ETF comparison
Market anomaly research module
Factor exposure dashboard
Transaction cost warning
```

Example insight:

```text
The portfolio outperformed the benchmark,
but most of the excess return came from higher technology exposure.
```

Another example:

```text
The strategy beat the benchmark before costs,
but underperformed after estimated transaction costs.
```

These features would make Athena more realistic and closer to professional investment analysis.

---

### CFA Level 1 takeaway

For CFA Level 1, market efficiency is important because it explains how information is reflected in prices and why outperforming the market can be difficult.

Important concepts include:

```text
Efficient Market Hypothesis
Weak form efficiency
Semi-strong form efficiency
Strong form efficiency
Public information
Private information
Active investing
Passive investing
Market anomalies
Behavioral finance
Risk-adjusted return
Transaction costs
```

A simple memory rule:

```text
Weak = past market data
Semi-strong = public information
Strong = public + private information
```

Another useful rule:

```text
Market efficiency does not mean prices are perfect.
It means prices reflect available information quickly.
```

---

### Athena implementation takeaway

For Athena, market efficiency provides the conceptual foundation for benchmark-based analysis.

The platform should not only show returns.

It should help users understand whether returns were meaningful compared with a benchmark and the risk taken.

Possible backend calculations:

```text
portfolio_return
benchmark_return
excess_return
tracking_error
information_ratio
portfolio_volatility
benchmark_volatility
maximum_drawdown
transaction_cost_adjusted_return
```

Possible frontend components:

```text
Market Efficiency explanation card
Active vs Passive comparison panel
Portfolio vs Benchmark chart
Excess Return card
Information Ratio card
Tracking Error card
Transaction Cost warning
Factor Exposure explanation
```

The goal is to avoid naive performance interpretation.

---

### Mini revision questions

1. What does market efficiency mean?

2. What is the Efficient Market Hypothesis?

3. What does weak-form efficiency say?

4. What does semi-strong form efficiency say?

5. What does strong-form efficiency say?

6. Why is strong-form efficiency unrealistic in practice?

7. Why does market efficiency make active investing difficult?

8. Why does market efficiency support passive investing?

9. What is a market anomaly?

10. Why does efficient market not mean risk-free market?

11. Why are transaction costs important when evaluating strategies?

12. Why is market efficiency useful for Athena?

---

### Mini answers

1. Market efficiency means that market prices reflect available information quickly and accurately.

2. The Efficient Market Hypothesis is the theory that prices reflect information, making consistent abnormal profits difficult to achieve.

3. Weak-form efficiency says prices reflect past market data such as historical prices and volume.

4. Semi-strong form efficiency says prices reflect all publicly available information.

5. Strong-form efficiency says prices reflect all public and private information.

6. Strong-form efficiency is unrealistic because private information can exist before it becomes public.

7. Market efficiency makes active investing difficult because many investors compete to find and exploit mispricing.

8. It supports passive investing because if beating the market is difficult, tracking the market at low cost can be rational.

9. A market anomaly is a pattern that seems inconsistent with market efficiency.

10. Efficient markets are not risk-free because prices can still fall when new information changes expectations.

11. Transaction costs are important because a strategy must outperform after costs, not only before costs.

12. Market efficiency is useful for Athena because it supports benchmark comparison, risk-adjusted analysis and realistic performance interpretation.

---

### Section summary

Market efficiency describes how quickly and accurately prices reflect information.

The three main forms are weak form, semi-strong form and strong form.

Weak form says prices reflect past market data.

Semi-strong form says prices reflect public information.

Strong form says prices reflect both public and private information.

For CFA Level 1, market efficiency is important because it explains why consistent outperformance is difficult and why passive investing is widely used.

For Athena AI Risk Terminal, market efficiency matters because performance should be evaluated relative to benchmarks, risk, costs and available information.

The key lesson is:

```text
Market efficiency does not mean prices are always perfect.
It means that available information is quickly reflected in prices,
making easy and consistent outperformance difficult.
```


---

























## Part V — Data quality, Athena implementation and review


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
