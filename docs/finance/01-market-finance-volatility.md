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
12. Nominal vs real returns
13. Price vs return
14. Holding Period Return
15. Simple returns
16. Log returns
17. Arithmetic vs geometric returns
18. Total return
19. Compounding and annualization
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
32. Liquidity
33. Bid, ask and bid-ask spread
34. Order types and market microstructure
35. Benchmark
36. Index construction basics
37. Market efficiency basics
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

## 23. Rolling volatility

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

## 24. Realized volatility

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

## 25. Implied volatility

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

## 26. Variance and standard deviation

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

## 27. Return distributions

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

## 28. Skewness and kurtosis

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

## 29. Normal distribution and fat tails

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

## 30. Correlation

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

## 31. Covariance

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

## 32. Liquidity

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

## 33. Bid, ask and bid-ask spread

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

## 34. Order types and market microstructure

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

## 35. Benchmark

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

## 36. Index construction basics

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

## 37. Market efficiency basics

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
