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
