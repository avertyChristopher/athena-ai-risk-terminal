# 02 — Fixed Income, Yield Curves and Bonds

**Project:** Athena AI Risk Terminal  
**Recommended file path:** `docs/finance/02-fixed-income-yield-curves-bonds.md`  
**Purpose:** build a strong foundation in fixed income, bonds, yield curves, spot rates, discount factors, duration, convexity, rate shocks and bond market risk before implementing the Rates Lab in Athena.  
**Scope:** this document focuses only on fixed income, yield curves and bonds. Other finance areas are documented separately.

---

## Table of Contents

1. What is fixed income?
2. Why fixed income matters
3. Main fixed income instruments
4. Bonds vs loans vs money market instruments
5. Bond issuers
6. Bond investors
7. Bond legal structure
8. Face value, par value and principal
9. Coupon rate
10. Coupon frequency
11. Maturity
12. Fixed-rate bonds
13. Floating-rate notes
14. Zero-coupon bonds
15. Callable bonds
16. Putable bonds
17. Convertible bonds
18. Bond cash flows
19. Time value of money
20. Discounting cash flows
21. Present value
22. Bond pricing formula
23. Premium, discount and par bonds
24. Clean price vs dirty price
25. Accrued interest
26. Yield to maturity
27. Current yield
28. Yield to call
29. Yield to worst
30. Spot rates
31. Discount factors
32. Forward rates
33. Par rates
34. Yield curves
35. Normal yield curve
36. Inverted yield curve
37. Flat yield curve
38. Steep yield curve
39. Term structure of interest rates
40. Bootstrapping spot rates
41. Bond price and yield relationship
42. Why bond prices fall when yields rise
43. Interest rate risk
44. Reinvestment risk
45. Credit risk
46. Default risk
47. Credit spreads
48. Government bonds
49. Corporate bonds
50. Investment grade vs high yield
51. Duration
52. Macaulay duration
53. Modified duration
54. Effective duration
55. Key rate duration
56. Dollar duration / money duration
57. Convexity
58. Duration and convexity approximation
59. Factors affecting duration and convexity
60. Rate shocks
61. Parallel shifts
62. Non-parallel shifts
63. Yield curve steepening
64. Yield curve flattening
65. Bond portfolio risk
66. Total return of a bond
67. Sources of bond return
68. Inflation and real rates
69. Nominal rates vs real rates
70. Liquidity in bond markets
71. Bid-ask spreads in fixed income
72. Bond market data quality
73. Common beginner mistakes
74. Key formulas
75. Possible API endpoints
76. Possible frontend components
77. Suggested tests
78. How Athena uses fixed income
79. Summary

---

## 1. What is fixed income?

Fixed income is the area of finance focused on debt instruments.

The most common fixed income instrument is a bond.

A bond is a contract where an investor lends money to an issuer. In return, the issuer promises to pay:

- interest payments;
- principal repayment at maturity.

Simple intuition:

```text
Equity = ownership
Fixed income = lending
```

When an investor buys a stock, the investor owns part of a company.  
When an investor buys a bond, the investor is lending money to an issuer.

The issuer can be:

- a government;
- a corporation;
- a municipality;
- a bank;
- a supranational institution.

Fixed income is called "fixed income" because many bonds pay scheduled cash flows. However, not all fixed income cash flows are perfectly fixed. Some instruments have floating rates, embedded options or credit risk.

### Athena link

In Athena AI Risk Terminal, this topic supports the future **Rates Lab**, especially:

- bond pricing;
- yield curve visualization;
- spot rates;
- discount factors;
- duration;
- convexity;
- rate shock stress testing.

---

## 2. Why fixed income matters

Fixed income is one of the largest areas of global finance.

It matters because governments, companies and institutions constantly borrow money.

### Why issuers issue bonds

Issuers use bonds to:

- finance public spending;
- fund corporate investments;
- refinance existing debt;
- fund acquisitions;
- manage liquidity;
- finance infrastructure.

### Why investors buy bonds

Investors buy bonds for:

- income;
- capital preservation;
- diversification;
- liability matching;
- liquidity;
- interest rate exposure;
- credit exposure.

### Simple comparison

```text
Stocks often focus on growth and ownership.
Bonds often focus on cash flows, rates and credit quality.
```

Fixed income is less intuitive than stocks because the main risk is often not "will the price go up?" but:

```text
What happens to the bond price when interest rates move?
Will the issuer repay?
Are the cash flows correctly discounted?
```

---

## 3. Main fixed income instruments

Fixed income includes many instruments.

Main categories:

```text
Government bonds
Corporate bonds
Municipal bonds
Treasury bills
Commercial paper
Certificates of deposit
Floating-rate notes
Inflation-linked bonds
Mortgage-backed securities
Asset-backed securities
```

### Government bonds

Issued by governments.

Examples:

```text
US Treasuries
Government of Canada bonds
French OATs
German Bunds
UK Gilts
```

They are often used as benchmarks.

### Corporate bonds

Issued by companies.

They usually offer higher yields than government bonds because they include credit risk.

### Treasury bills

Short-term government debt instruments.

They usually mature in less than one year.

### Commercial paper

Short-term debt issued by corporations.

### Floating-rate notes

Debt instruments whose coupon resets based on a reference rate.

### Inflation-linked bonds

Bonds whose principal or coupon is linked to inflation.

### Athena first version

For Athena's first fixed income module, focus on:

```text
Plain fixed-rate coupon bonds
Zero-coupon bonds
Simple yield curves
Spot rates
Discount factors
Duration
Rate shocks
```

---

## 4. Bonds vs loans vs money market instruments

### Bonds

Bonds are usually standardized debt securities that can trade in financial markets.

They have:

- issuer;
- face value;
- coupon rate;
- maturity date;
- payment schedule;
- market price.

### Loans

Loans are often private agreements between a borrower and a lender.

They are usually less standardized and less liquid than bonds.

### Money market instruments

Money market instruments are short-term debt instruments.

They usually have:

- short maturity;
- high liquidity;
- lower price volatility;
- lower yield.

Simple comparison:

```text
Bond = tradable debt security
Loan = private lending agreement
Money market instrument = short-term debt instrument
```

### Mini-test

Question:

```text
Which is usually more liquid: a publicly traded government bond or a private loan?
```

Answer:

```text
The publicly traded government bond.
```

---

## 5. Bond issuers

A bond issuer is the entity borrowing money.

Common issuers:

```text
Sovereign governments
Government agencies
Municipalities
Corporations
Banks
Supranational organizations
```

### Government issuers

Governments issue bonds to finance deficits, infrastructure and public programs.

### Corporate issuers

Corporations issue bonds to finance growth, acquisitions, operations or refinancing.

### Supranational issuers

Supranational institutions issue bonds to finance development or international programs.

### Credit quality

Issuer quality matters.

A strong issuer usually pays a lower yield.  
A weaker issuer usually pays a higher yield.

Why?

Because investors require compensation for taking more credit risk.

---

## 6. Bond investors

Bond investors include:

```text
Individuals
Pension funds
Insurance companies
Mutual funds
Banks
Central banks
Hedge funds
Sovereign wealth funds
```

### Pension funds

Pension funds often use bonds to match long-term liabilities.

### Insurance companies

Insurance companies like bonds because they need predictable cash flows.

### Banks

Banks hold bonds for liquidity management, income and balance sheet management.

### Individuals

Individuals may buy bonds for income and stability.

### Why investor type matters

Different investors have different needs. This affects demand for different maturities, credit qualities and currencies.

Example:

```text
A pension fund may prefer long-term bonds.
A money market fund may prefer short-term instruments.
```

---

## 7. Bond legal structure

A bond is a legal contract.

Important legal elements:

```text
Issuer
Bondholder
Indenture
Covenants
Seniority
Collateral
Payment schedule
Default provisions
Call or put provisions
```

### Indenture

The indenture is the legal document defining bond terms.

### Covenants

Covenants are rules that protect bondholders.

Examples:

- limit on additional debt;
- requirement to maintain financial ratios;
- restrictions on asset sales;
- restrictions on dividend payments.

### Seniority

Seniority determines repayment priority if the issuer defaults.

Simplified priority:

```text
Secured debt
Senior unsecured debt
Subordinated debt
Preferred equity
Common equity
```

### Athena note

For Athena's first version, legal structure can be simplified. Later, credit risk modules can include seniority and covenants.

---

## 8. Face value, par value and principal

Face value, par value and principal usually refer to the amount repaid at maturity.

Common value:

```text
1,000
```

Example:

```text
Face value = 1,000
Maturity = 5 years
```

If the issuer does not default, the investor receives 1,000 at maturity.

### Par

A bond trades at par when its price equals face value.

```text
Price = 1,000
Face value = 1,000
```

### Bullet bond

A standard bond that repays principal at maturity is called a bullet bond.

Cash flow structure:

```text
Coupons during the bond life
Principal at maturity
```

This is the easiest structure to implement first.

---

## 9. Coupon rate

The coupon rate determines the interest payment as a percentage of face value.

Formula:

```text
Annual coupon payment = Coupon rate × Face value
```

Example:

```text
Face value = 1,000
Coupon rate = 5%

Annual coupon = 1,000 × 5%
Annual coupon = 50
```

### Coupon rate vs yield

This is a critical distinction.

```text
Coupon rate = contractual rate
Yield = market return measure
```

The coupon rate is fixed by the bond contract.  
The yield changes as the bond price changes.

### Beginner trap

A bond with a 5% coupon does not necessarily offer a 5% market yield if it trades above or below par.

---

## 10. Coupon frequency

Coupon frequency is how often coupons are paid.

Common frequencies:

```text
Annual
Semiannual
Quarterly
Monthly
```

### Example

```text
Face value = 1,000
Coupon rate = 6%
Coupon frequency = semiannual
```

Annual coupon:

```text
1,000 × 6% = 60
```

Semiannual coupon:

```text
60 / 2 = 30
```

The investor receives 30 every six months.

### Athena implementation note

A bond pricing function should include:

```text
coupon_rate
face_value
maturity
yield_to_maturity
payments_per_year
```

---

## 11. Maturity

Maturity is the date when principal is repaid.

Example:

```text
Issue date: 2026-01-01
Maturity date: 2031-01-01
Maturity: 5 years
```

### Maturity categories

Simplified:

```text
Short-term: less than 3 years
Medium-term: 3 to 10 years
Long-term: more than 10 years
```

### Why maturity matters

Maturity affects:

- interest rate sensitivity;
- reinvestment risk;
- yield level;
- liquidity;
- investor demand.

Longer maturity usually means higher interest rate sensitivity.

---

## 12. Fixed-rate bonds

A fixed-rate bond pays a coupon that does not change.

Example:

```text
Face value = 1,000
Coupon rate = 5%
Maturity = 10 years
```

The bond pays the same coupon each period.

### Advantages

For investors:

- predictable cash flows;
- easier valuation;
- stable income.

For issuers:

- predictable financing cost.

### Main risk

Fixed-rate bond prices are sensitive to market yield changes.

If market yields rise, the fixed coupon becomes less attractive.

---

## 13. Floating-rate notes

A floating-rate note, or FRN, pays a coupon that resets periodically.

Formula:

```text
Coupon = Reference rate + Spread
```

Example:

```text
Reference rate = 4%
Spread = 1%

Coupon = 5%
```

### Why FRNs matter

Floating-rate notes usually have lower interest rate sensitivity because coupons adjust with market rates.

### Main risks

FRNs still have:

- credit risk;
- liquidity risk;
- reset risk;
- spread risk.

### Simple comparison

```text
Fixed-rate bond = coupon fixed
Floating-rate note = coupon adjusts
```

---

## 14. Zero-coupon bonds

A zero-coupon bond pays no periodic coupons.

It is issued at a discount and repays face value at maturity.

Example:

```text
Purchase price = 800
Face value at maturity = 1,000
```

The investor earns return from the difference between purchase price and maturity value.

### Pricing formula

```text
Price = Face value / (1 + yield)^t
```

### Example

```text
Face value = 1,000
Yield = 5%
Maturity = 3 years

Price = 1,000 / (1.05)^3
Price = 863.84
```

### Why zero-coupon bonds matter

They are useful for learning:

- discounting;
- spot rates;
- present value;
- duration.

A zero-coupon bond's Macaulay duration equals its maturity.

---

## 15. Callable bonds

A callable bond gives the issuer the right to redeem the bond before maturity.

### Why issuers call bonds

Issuers may call bonds when rates fall.

Example:

```text
Old bond coupon = 6%
New market yield = 4%
```

The issuer may refinance at a lower cost.

### Investor perspective

Callable bonds create reinvestment risk.

The investor may lose a high-coupon bond and have to reinvest at lower yields.

### Yield implication

Callable bonds usually offer higher yields than similar non-callable bonds because the call option benefits the issuer.

---

## 16. Putable bonds

A putable bond gives the investor the right to sell the bond back to the issuer before maturity.

This benefits the investor.

### Why investors like putable bonds

If interest rates rise or credit quality worsens, the investor can put the bond back.

### Yield implication

Putable bonds usually offer lower yields than similar non-putable bonds because the embedded option benefits the investor.

Simple comparison:

```text
Callable bond = issuer has the option
Putable bond = investor has the option
```

---

## 17. Convertible bonds

A convertible bond gives the investor the right to convert the bond into shares of the issuer.

It combines:

```text
Debt
Equity option
```

### Investor benefit

Convertible bonds can provide:

- coupon income;
- downside support from bond value;
- upside participation if the stock rises.

### Issuer benefit

Issuers may offer lower coupons because investors value the conversion option.

### Athena note

Convertibles are advanced. Athena's first fixed income module should focus on plain bonds.

---

## 18. Bond cash flows

A bond's value comes from its cash flows.

For a standard coupon bond:

```text
Coupon payments
Principal repayment
```

Example:

```text
Face value = 1,000
Coupon rate = 5%
Maturity = 3 years
Annual coupon = 50
```

Cash flows:

```text
Year 1: 50
Year 2: 50
Year 3: 1,050
```

The final cash flow includes:

```text
Last coupon + principal
```

### Athena link

The Rates Lab should be able to display a bond cash flow table.

Possible columns:

```text
Period
Date
Coupon
Principal
Total cash flow
Discount factor
Present value
```

---

## 19. Time value of money

The time value of money means money today is worth more than the same amount in the future.

Why?

Because money today can be:

- invested;
- used immediately;
- protected from uncertainty;
- compensated for inflation and risk.

### Core idea

```text
Future money must be discounted to compare it with money today.
```

Example:

```text
1,000 today is worth more than 1,000 in five years.
```

This is the foundation of bond pricing.

---

## 20. Discounting cash flows

Discounting converts a future cash flow into present value.

Formula:

```text
Present Value = Future Cash Flow / (1 + discount rate)^t
```

Example:

```text
Future cash flow = 1,000
Discount rate = 5%
Time = 2 years

PV = 1,000 / (1.05)^2
PV = 907.03
```

### Intuition

The higher the discount rate, the lower the present value.

```text
Higher discount rate → lower present value
Lower discount rate → higher present value
```

This is the key to understanding bond prices.

---

## 21. Present value

Present value is the value today of a future cash flow.

Example:

```text
Future cash flow = 1,000
Time = 5 years
```

At 3%:

```text
PV = 1,000 / (1.03)^5
PV = 862.61
```

At 6%:

```text
PV = 1,000 / (1.06)^5
PV = 747.26
```

Same future cash flow. Different discount rate. Different present value.

### Key lesson

```text
When discount rates rise, present values fall.
```

This explains the inverse relationship between bond prices and yields.

---

## 22. Bond pricing formula

A standard coupon bond price is the present value of coupons plus principal.

Formula:

```text
Bond Price = C/(1+y)^1 + C/(1+y)^2 + ... + (C + Face)/(1+y)^n
```

Where:

```text
C = coupon payment
y = yield per period
n = number of periods
Face = face value
```

### Example

```text
Face value = 1,000
Coupon rate = 5%
Annual coupon = 50
Maturity = 3 years
Yield = 4%
```

Cash flows:

```text
Year 1: 50
Year 2: 50
Year 3: 1,050
```

Price:

```text
Price = 50/(1.04)^1 + 50/(1.04)^2 + 1,050/(1.04)^3
Price ≈ 1,027.75
```

The bond trades above par because coupon rate is greater than yield.

---

## 23. Premium, discount and par bonds

A bond can trade at:

```text
Premium
Discount
Par
```

### Par bond

```text
Price = Face value
```

Usually when:

```text
Coupon rate = yield
```

### Premium bond

```text
Price > Face value
```

Usually when:

```text
Coupon rate > yield
```

### Discount bond

```text
Price < Face value
```

Usually when:

```text
Coupon rate < yield
```

### Summary

```text
Coupon > Yield → Premium bond
Coupon = Yield → Par bond
Coupon < Yield → Discount bond
```

### Mini-test

Question:

```text
A bond has a coupon rate of 3% and market yield of 5%. Premium or discount?
```

Answer:

```text
Discount bond.
```

---

## 24. Clean price vs dirty price

Bond prices can be quoted as clean or dirty.

### Clean price

The clean price excludes accrued interest.

This is often the quoted price.

### Dirty price

The dirty price includes accrued interest.

Formula:

```text
Dirty price = Clean price + Accrued interest
```

### Example

```text
Clean price = 980
Accrued interest = 15

Dirty price = 995
```

The actual amount paid by the buyer is usually based on the dirty price.

### Athena note

First version can use clean price only, but professional documentation should mention dirty price and accrued interest.

---

## 25. Accrued interest

Accrued interest is interest earned since the last coupon payment but not yet paid.

Formula idea:

```text
Accrued interest = Coupon payment × fraction of coupon period elapsed
```

Example:

```text
Semiannual coupon = 30
Half of coupon period elapsed

Accrued interest = 30 × 0.5
Accrued interest = 15
```

### Why it matters

If the seller held the bond for part of the coupon period, the seller earned part of the next coupon.

The buyer compensates the seller through accrued interest.

### Common beginner mistake

Confusing quoted clean price with full settlement price.

---

## 26. Yield to maturity

Yield to maturity, or YTM, is the discount rate that makes the present value of all future bond cash flows equal to the bond's market price.

Conceptual equation:

```text
Bond price = PV(all cash flows discounted at YTM)
```

### Assumptions

YTM assumes:

- bond is held to maturity;
- issuer makes all payments;
- coupons are reinvested at the same yield.

### Interpretation

```text
Higher price → lower yield
Lower price → higher yield
```

YTM is usually solved numerically for coupon bonds.

### Athena implementation note

A YTM solver can use numerical methods such as:

```text
bisection
Newton-Raphson
scipy optimization
```

---

## 27. Current yield

Current yield measures annual coupon income relative to current price.

Formula:

```text
Current yield = Annual coupon / Bond price
```

Example:

```text
Annual coupon = 50
Bond price = 950

Current yield = 50 / 950
Current yield = 5.26%
```

### Limitation

Current yield ignores:

- capital gain or loss at maturity;
- reinvestment;
- time value of money.

It is simple but incomplete.

---

## 28. Yield to call

Yield to call is the yield assuming the bond is called at a specified call date.

It matters for callable bonds.

Conceptual equation:

```text
Bond price = PV(cash flows until call date + call price)
```

### Example intuition

If a bond has a 10-year maturity but can be called in 5 years, the investor may not receive cash flows for the full 10 years.

### Athena note

Yield to call is advanced. It can be added after standard YTM.

---

## 29. Yield to worst

Yield to worst is the lowest yield among possible redemption scenarios, assuming no default.

It can compare:

```text
Yield to maturity
Yield to first call
Yield to later call dates
```

The lowest one is yield to worst.

### Why it matters

Yield to worst is conservative.

It prevents investors from focusing only on the most attractive yield scenario.

Simple intuition:

```text
Yield to worst = worst contractual yield outcome before default.
```

---

## 30. Spot rates

A spot rate is the zero-coupon rate for a specific maturity.

It is the rate used to discount a single cash flow at that maturity.

Examples:

```text
1-year spot rate
2-year spot rate
5-year spot rate
10-year spot rate
```

### Why spot rates matter

A coupon bond has multiple cash flows at different dates.

A more precise valuation discounts each cash flow using the spot rate for that cash flow's maturity.

Formula:

```text
Bond price = CF1/(1+s1)^1 + CF2/(1+s2)^2 + ... + CFn/(1+sn)^n
```

Where:

```text
s_t = spot rate for maturity t
```

---

## 31. Discount factors

A discount factor converts a future cash flow into present value.

Formula:

```text
Discount factor = 1 / (1 + spot rate)^t
```

Then:

```text
Present value = Future cash flow × Discount factor
```

Example:

```text
Spot rate = 4%
Maturity = 2 years

Discount factor = 1 / (1.04)^2
Discount factor = 0.9246
```

A future cash flow of 1,000 is worth:

```text
1,000 × 0.9246 = 924.60
```

### Athena link

The Rates Lab should include a discount factors table.

---

## 32. Forward rates

A forward rate is an interest rate implied today for a future period.

Example:

```text
1-year rate starting 1 year from now
2-year rate starting 3 years from now
```

Forward rates are derived from spot rates.

### Intuition

If the 1-year and 2-year spot rates are known, the market-implied rate for the second year can be derived.

### Why forward rates matter

Forward rates help analyze:

- market expectations;
- curve shape;
- future rate assumptions;
- relative value.

Forward rates can be optional in Athena's first version.

---

## 33. Par rates

A par rate is the coupon rate that makes a bond trade at par.

Simple intuition:

```text
Par rate = coupon rate that makes price = face value
```

### Par curve vs spot curve

```text
Spot curve = zero-coupon rates by maturity
Par curve = coupon rates that price bonds at par
```

### Why par rates matter

Market yield curves are often quoted using par yields.

Athena can start with simple user-provided yield curve points and later support par-to-spot conversion.

---

## 34. Yield curves

A yield curve shows interest rates across maturities.

Example:

```text
1Y  = 3.50%
2Y  = 3.70%
5Y  = 4.00%
10Y = 4.25%
30Y = 4.50%
```

The x-axis is maturity.  
The y-axis is yield.

### Why yield curves matter

Yield curves are used for:

- bond pricing;
- rate expectations;
- economic interpretation;
- discounting;
- risk measurement;
- stress testing.

### Athena link

A yield curve chart is one of the key visual components of the Rates Lab.

---

## 35. Normal yield curve

A normal yield curve slopes upward.

```text
Long-term yields > short-term yields
```

Example:

```text
1Y  = 3.0%
5Y  = 3.8%
10Y = 4.3%
```

### Interpretation

A normal curve can reflect:

- compensation for longer maturity;
- inflation uncertainty;
- growth expectations;
- term premium.

Normal curves are common in stable environments.

---

## 36. Inverted yield curve

An inverted yield curve slopes downward.

```text
Short-term yields > long-term yields
```

Example:

```text
1Y  = 5.0%
5Y  = 4.2%
10Y = 3.8%
```

### Interpretation

An inverted curve may reflect:

- tight monetary policy;
- expected rate cuts;
- economic slowdown concerns;
- demand for long-term safe assets.

An inverted curve is closely watched by markets.

---

## 37. Flat yield curve

A flat yield curve means yields are similar across maturities.

Example:

```text
1Y  = 4.0%
5Y  = 4.1%
10Y = 4.0%
```

### Interpretation

A flat curve may indicate uncertainty or a transition between market regimes.

It can occur when markets are unsure about future rate direction.

---

## 38. Steep yield curve

A steep yield curve rises strongly with maturity.

Example:

```text
1Y  = 2.0%
5Y  = 3.5%
10Y = 5.0%
```

### Interpretation

A steep curve may reflect:

- expected future rate increases;
- inflation expectations;
- strong growth expectations;
- high term premium.

A steep curve affects bonds differently depending on maturity exposure.

---

## 39. Term structure of interest rates

The term structure of interest rates describes how yields vary across maturities.

It is represented visually by the yield curve.

### Main theories

Common theories include:

```text
Expectations theory
Liquidity preference theory
Market segmentation theory
Preferred habitat theory
```

### Expectations theory

Long-term rates reflect expected future short-term rates.

### Liquidity preference theory

Investors demand extra compensation for holding longer maturities.

### Market segmentation theory

Different investors prefer different maturity segments.

### Preferred habitat theory

Investors have preferred maturities but may shift if sufficiently compensated.

---

## 40. Bootstrapping spot rates

Bootstrapping is the process of deriving spot rates from market prices of bonds.

The logic is step-by-step:

1. Use the shortest maturity instrument to get the first spot rate.
2. Use that spot rate to solve the next maturity.
3. Continue along the curve.

### Simple example idea

If a 1-year zero-coupon bond price is known, the 1-year spot rate can be solved.

Then a 2-year coupon bond can be used to solve the 2-year spot rate, because the 1-year spot rate is already known.

### Athena note

First version:

```text
User provides spot rates manually.
```

Advanced version:

```text
Athena bootstraps spot rates from bond prices.
```

---

## 41. Bond price and yield relationship

Bond prices and yields move in opposite directions.

```text
Yield increases → Bond price decreases
Yield decreases → Bond price increases
```

This is one of the most important fixed income rules.

### Intuition

The bond's coupon is fixed.  
The market yield changes.  
The bond price adjusts.

If market yields rise, an old lower-yielding bond becomes less attractive, so its price falls.

---

## 42. Why bond prices fall when yields rise

A bond is the present value of future cash flows.

If the discount rate increases, present value decreases.

Example:

```text
Future cash flow = 1,000
Time = 5 years
```

At 3%:

```text
PV = 1,000 / (1.03)^5
PV = 862.61
```

At 6%:

```text
PV = 1,000 / (1.06)^5
PV = 747.26
```

Same future cash flow. Higher discount rate. Lower present value.

### Core lesson

```text
Higher yields reduce the present value of fixed cash flows.
```

---

## 43. Interest rate risk

Interest rate risk is the risk that bond prices change because market interest rates change.

Fixed-rate bonds are especially exposed to interest rate risk.

### Main rules

```text
Longer maturity → higher interest rate risk
Lower coupon → higher interest rate risk
Higher duration → higher interest rate risk
```

### Example

A 30-year zero-coupon bond is highly sensitive to rate changes.

A short-term floating-rate note is much less sensitive.

### Athena link

Interest rate risk should be measured with:

- duration;
- convexity;
- rate shocks;
- key rate duration later.

---

## 44. Reinvestment risk

Reinvestment risk is the risk that future cash flows will be reinvested at lower rates.

This affects coupon bonds.

### Example

An investor receives coupon payments.

If market rates fall, future coupons may be reinvested at lower yields.

### Callable bond link

Callable bonds increase reinvestment risk because the issuer may call the bond when rates fall.

### Simple contrast

```text
Price risk is more painful when rates rise.
Reinvestment risk is more painful when rates fall.
```

---

## 45. Credit risk

Credit risk is the risk that the issuer may not fully meet its payment obligations.

Credit risk includes:

- default risk;
- downgrade risk;
- spread widening risk;
- recovery risk.

### Strong issuers

Usually have:

- lower yields;
- tighter credit spreads;
- lower default probability.

### Weak issuers

Usually have:

- higher yields;
- wider credit spreads;
- higher default probability.

Investors require compensation for credit risk.

---

## 46. Default risk

Default risk is the risk that the issuer fails to pay interest or principal.

Default can occur because of:

- weak cash flows;
- excessive debt;
- economic recession;
- poor management;
- sector collapse;
- liquidity crisis.

### Recovery rate

If default happens, investors may recover part of their investment.

Example:

```text
Face value = 1,000
Recovery value = 400

Recovery rate = 40%
```

### Loss given default

```text
Loss given default = 1 - recovery rate
```

If recovery is 40%:

```text
Loss given default = 60%
```

---

## 47. Credit spreads

A credit spread is the extra yield above a benchmark government or risk-free yield.

Formula:

```text
Credit spread = Corporate bond yield - Government bond yield
```

Example:

```text
Corporate bond yield = 6%
Government bond yield = 4%

Credit spread = 2%
```

### What spreads compensate for

Credit spreads compensate investors for:

- default risk;
- downgrade risk;
- liquidity risk;
- uncertainty.

### Spread widening

If spreads widen, corporate bond prices usually fall.

### Spread tightening

If spreads tighten, corporate bond prices usually rise.

---

## 48. Government bonds

Government bonds are issued by national governments.

Examples:

```text
US Treasuries
Government of Canada bonds
German Bunds
French OATs
UK Gilts
Japanese Government Bonds
```

### Why government bonds matter

They are used as:

- benchmarks;
- safe-haven assets;
- monetary policy instruments;
- discounting references;
- liquidity instruments.

### Risks

Government bonds still have risks:

- interest rate risk;
- inflation risk;
- currency risk;
- political risk;
- default risk in some cases.

Government bonds issued in a government's own currency are often considered low credit risk, but they are not risk-free in every possible sense.

---

## 49. Corporate bonds

Corporate bonds are issued by companies.

They usually offer higher yields than government bonds because they include credit risk.

### Corporate bond yield decomposition

```text
Corporate yield = government yield + credit spread
```

### Risk drivers

Corporate bond risk depends on:

- issuer credit quality;
- leverage;
- profitability;
- cash flow stability;
- sector conditions;
- maturity;
- liquidity;
- covenant protection.

### Athena note

Corporate bonds can be modeled later with credit spread fields.

---

## 50. Investment grade vs high yield

Corporate bonds are often classified by credit quality.

### Investment grade

Investment grade bonds are considered higher quality.

They usually have:

- lower default risk;
- lower yields;
- tighter spreads;
- better liquidity.

### High yield

High yield bonds are lower-rated bonds.

They usually have:

- higher default risk;
- higher yields;
- wider spreads;
- more credit sensitivity.

High yield bonds are also called speculative grade bonds.

Simple comparison:

```text
Investment grade = safer, lower yield
High yield = riskier, higher yield
```

---

## 51. Duration

Duration measures a bond's sensitivity to interest rate changes.

The higher the duration, the more sensitive the bond price is to yield changes.

Approximation:

```text
% Price Change ≈ -Duration × Change in Yield
```

Example:

```text
Modified duration = 6
Yield increases by 1%

Approximate price change = -6%
```

### Why duration matters

Duration is one of the most important fixed income risk measures.

It turns yield movements into approximate price movements.

### Athena link

Duration should appear as a key metric in the Rates Lab.

---

## 52. Macaulay duration

Macaulay duration is the weighted average time to receive a bond's cash flows.

The weights are based on the present value of each cash flow.

### Intuition

Macaulay duration answers:

```text
On average, when does the investor receive the bond's present value?
```

### Zero-coupon bond

For a zero-coupon bond:

```text
Macaulay duration = maturity
```

Why?

Because the only cash flow occurs at maturity.

### Coupon bond

For a coupon bond, Macaulay duration is usually less than maturity because coupons are received before maturity.

---

## 53. Modified duration

Modified duration measures price sensitivity to yield changes.

Formula:

```text
Modified duration = Macaulay duration / (1 + yield per period)
```

Approximation:

```text
% Price Change ≈ -Modified Duration × Change in Yield
```

Example:

```text
Modified duration = 5
Yield increase = 0.50%

Price change ≈ -5 × 0.50%
Price change ≈ -2.5%
```

Modified duration is usually more directly useful for risk estimation than Macaulay duration.

---

## 54. Effective duration

Effective duration is used when a bond has embedded options.

Examples:

```text
Callable bonds
Putable bonds
Mortgage-backed securities
```

Formula idea:

```text
Effective duration = (Price_down - Price_up) / (2 × Price_0 × Change in yield)
```

Where:

```text
Price_down = price when yields decrease
Price_up = price when yields increase
Price_0 = initial price
```

### Why effective duration matters

For bonds with embedded options, cash flows can change when rates move.

Standard duration may not capture this correctly.

---

## 55. Key rate duration

Key rate duration measures sensitivity to changes at specific maturities on the yield curve.

Example key rates:

```text
2-year
5-year
10-year
30-year
```

### Why key rate duration matters

Yield curves do not always move in parallel.

A bond portfolio may be more sensitive to the 10-year rate than the 2-year rate.

Example:

```text
2Y key rate duration = 0.5
10Y key rate duration = 6.0
```

This means the bond is much more sensitive to 10-year rate changes.

---

## 56. Dollar duration / money duration

Dollar duration measures interest rate sensitivity in money terms.

Formula idea:

```text
Dollar duration = Modified duration × Market value
```

For a 1% yield move:

```text
Approximate dollar change = -Modified duration × Market value × 1%
```

Example:

```text
Market value = 1,000,000
Modified duration = 5
Yield increase = 1%

Dollar loss ≈ -5 × 1,000,000 × 1%
Dollar loss ≈ -50,000
```

Dollar duration is useful for portfolio-level risk.

---

## 57. Convexity

Convexity measures the curvature of the bond price-yield relationship.

Duration gives a linear approximation.  
Convexity improves the approximation for larger yield changes.

Simple intuition:

```text
Duration = first-order sensitivity
Convexity = second-order sensitivity
```

### Why convexity matters

The bond price-yield relationship is curved.

For small yield changes, duration may be enough.  
For larger yield changes, convexity becomes important.

Higher convexity is generally valuable.

---

## 58. Duration and convexity approximation

A common approximation for bond price change is:

```text
% Price Change ≈ -Duration × ΔYield + 0.5 × Convexity × (ΔYield)^2
```

Example:

```text
Modified duration = 6
Convexity = 40
Yield increase = 1% = 0.01
```

Approximate price change:

```text
= -6 × 0.01 + 0.5 × 40 × (0.01)^2
= -0.06 + 0.002
= -0.058
= -5.8%
```

Duration alone estimates -6%.  
Convexity improves the estimate to -5.8%.

---

## 59. Factors affecting duration and convexity

Duration and convexity depend on bond characteristics.

### Maturity

Longer maturity usually increases duration and convexity.

### Coupon rate

Lower coupon bonds usually have higher duration.

Higher coupon bonds return more cash flow earlier, reducing duration.

### Yield level

Higher yields usually reduce duration.

### Embedded options

Callable and putable features affect effective duration and convexity.

### Summary

```text
Longer maturity → higher duration
Lower coupon → higher duration
Lower yield → higher duration
Embedded options → more complex behavior
```

---

## 60. Rate shocks

A rate shock is a change applied to interest rates to estimate price impact.

Common shocks:

```text
+100 bps
-100 bps
+50 bps
-50 bps
```

One basis point is:

```text
1 bp = 0.01%
100 bps = 1.00%
```

Example:

```text
Modified duration = 7
Rate shock = +100 bps

Estimated price change = -7%
```

### Athena link

A Rate Shock Panel should show:

- initial bond price;
- shocked yield;
- estimated price change;
- estimated dollar loss;
- duration-based approximation;
- convexity-adjusted approximation.

---

## 61. Parallel shifts

A parallel shift means all points on the yield curve move by the same amount.

Example:

```text
1Y rate  +100 bps
5Y rate  +100 bps
10Y rate +100 bps
30Y rate +100 bps
```

Parallel shifts are simple and useful for stress testing.

### Athena first version

Start with parallel rate shocks:

```text
+50 bps
+100 bps
-50 bps
-100 bps
```

### Limitation

Real yield curves do not always move in parallel.

---

## 62. Non-parallel shifts

A non-parallel shift means different maturities move by different amounts.

Example:

```text
2Y rate  +150 bps
10Y rate +50 bps
30Y rate +20 bps
```

This changes the shape of the curve.

### Why it matters

Bond portfolios may have different exposures across maturities.

Non-parallel shifts require more advanced analysis, such as key rate duration.

---

## 63. Yield curve steepening

Yield curve steepening means the difference between long-term and short-term yields increases.

Example:

```text
Before:
2Y = 3.0%
10Y = 4.0%
Spread = 1.0%

After:
2Y = 3.0%
10Y = 5.0%
Spread = 2.0%
```

The curve became steeper.

### Types

```text
Bear steepening = long-term yields rise more
Bull steepening = short-term yields fall more
```

### Athena idea

A curve shape badge can identify:

```text
Normal
Inverted
Flat
Steep
```

---

## 64. Yield curve flattening

Yield curve flattening means the difference between long-term and short-term yields decreases.

Example:

```text
Before:
2Y = 3.0%
10Y = 5.0%
Spread = 2.0%

After:
2Y = 4.0%
10Y = 5.0%
Spread = 1.0%
```

The curve became flatter.

### Types

```text
Bear flattening = short-term yields rise more
Bull flattening = long-term yields fall more
```

### Why it matters

Flattening affects bonds differently depending on maturity exposure.

---

## 65. Bond portfolio risk

A bond portfolio contains multiple fixed income instruments.

Risk depends on:

- interest rate exposure;
- duration;
- convexity;
- credit quality;
- maturity distribution;
- currency exposure;
- liquidity;
- issuer concentration;
- sector exposure;
- curve exposure.

### Portfolio metrics

Athena can calculate:

```text
Weighted average yield
Weighted average duration
Weighted average convexity
Maturity bucket exposure
Credit quality exposure
Currency exposure
Rate shock loss
```

### Example risk

```text
Portfolio market value = 1,000,000
Weighted duration = 6
Rate shock = +100 bps

Estimated loss = 60,000
```

---

## 66. Total return of a bond

Bond total return includes more than coupon income.

Sources:

```text
Coupon income
Price change
Reinvestment income
Currency effect
Credit spread changes
```

Formula idea:

```text
Total return = income return + price return + reinvestment return + currency effect
```

Example:

```text
Coupon income = 4%
Price change = -2%
Currency effect = +1%

Total return = 3%
```

A bond can have a positive total return even if its price falls, if coupon income offsets the loss.

---

## 67. Sources of bond return

Bond return can come from several sources.

### Coupon income

Regular interest payments.

### Price change

Bond price changes due to yield movement, credit spread movement or time passing.

### Roll-down return

If the yield curve is upward sloping, a bond can move toward a shorter maturity point with a lower yield over time.

### Reinvestment income

Coupons can be reinvested.

### Currency effect

Foreign currency bonds can gain or lose due to exchange rates.

### Credit spread changes

If credit spreads tighten, corporate bond prices may rise.  
If spreads widen, corporate bond prices may fall.

---

## 68. Inflation and real rates

Inflation reduces purchasing power.

A nominal yield does not directly show real purchasing power gain.

Approximate formula:

```text
Real rate ≈ Nominal rate - Inflation
```

Exact formula:

```text
Real rate = (1 + nominal rate) / (1 + inflation) - 1
```

Example:

```text
Nominal yield = 5%
Inflation = 3%

Approximate real yield = 2%
```

### Why it matters

Bond investors care about real returns.

High inflation can make a positive nominal yield unattractive.

---

## 69. Nominal rates vs real rates

A nominal rate is not adjusted for inflation.

A real rate is adjusted for inflation.

### Nominal bond

A nominal bond pays fixed nominal cash flows.

Inflation can reduce the real value of those cash flows.

### Inflation-linked bond

An inflation-linked bond adjusts principal or coupons based on inflation.

Examples:

```text
TIPS in the United States
Real Return Bonds in Canada
Index-linked gilts in the UK
```

### Simple comparison

```text
Nominal rate = before inflation adjustment
Real rate = after inflation adjustment
```

---

## 70. Liquidity in bond markets

Bond market liquidity measures how easily bonds can be bought or sold without large price impact.

Bond liquidity can vary widely.

Government bonds are often more liquid.  
Small corporate bond issues may be less liquid.

### Liquidity indicators

Possible indicators:

```text
Bid-ask spread
Trading volume
Issue size
Number of dealers
Time since issuance
Credit quality
Market stress level
```

### Why liquidity matters

In stressed markets, liquidity can disappear quickly.

A bond may look safe based on price history but become difficult to sell.

---

## 71. Bid-ask spreads in fixed income

The bid is the price dealers are willing to pay.  
The ask is the price dealers are willing to sell at.

Formula:

```text
Spread = Ask - Bid
```

### Example

```text
Bid = 98.50
Ask = 99.00

Spread = 0.50
```

A wider spread means higher trading cost.

### Fixed income specificity

Bond markets are often less transparent than equity markets.

Many bonds trade over-the-counter rather than on centralized exchanges.

This can make bond liquidity harder to measure.

---

## 72. Bond market data quality

Bond market data can be messy.

Common problems:

- stale prices;
- missing quotes;
- inconsistent yield conventions;
- wrong coupon frequency;
- incorrect maturity date;
- missing accrued interest;
- wrong currency;
- duplicated securities;
- incorrect credit rating;
- outdated call schedule.

### Athena data checks

Athena should validate:

```text
face_value > 0
coupon_rate >= 0
maturity_date > valuation_date
currency is defined
coupon_frequency is valid
yield is not missing
price is positive
```

### Professional rule

Never trust bond data blindly.

Fixed income analytics are very sensitive to incorrect inputs.

---

## 73. Common beginner mistakes

### Mistake 1 — Confusing coupon rate and yield

Coupon rate is contractual.  
Yield is market-based.

### Mistake 2 — Forgetting the inverse price-yield relationship

When yields rise, bond prices fall.

### Mistake 3 — Ignoring coupon frequency

Annual and semiannual coupons produce different cash flow timing.

### Mistake 4 — Ignoring accrued interest

Clean price and dirty price are different.

### Mistake 5 — Using one yield for all cash flows without understanding spot rates

Spot rates discount cash flows by maturity.

### Mistake 6 — Thinking all bonds are safe

Bonds have interest rate risk, credit risk, liquidity risk and inflation risk.

### Mistake 7 — Ignoring duration

Duration is central to fixed income risk.

### Mistake 8 — Ignoring convexity for large rate moves

Duration alone can be too approximate for large shocks.

### Mistake 9 — Ignoring liquidity

Some bonds are hard to trade.

### Mistake 10 — Forgetting currency

A bond's yield and cash flows must be interpreted in the correct currency.

---

## 74. Key formulas

### Annual coupon

```text
Annual coupon = Coupon rate × Face value
```

### Coupon per period

```text
Coupon per period = Annual coupon / Payments per year
```

### Present value

```text
PV = Future Cash Flow / (1 + discount rate)^t
```

### Coupon bond price

```text
Bond Price = C/(1+y)^1 + C/(1+y)^2 + ... + (C+Face)/(1+y)^n
```

### Zero-coupon bond price

```text
Price = Face value / (1 + yield)^t
```

### Dirty price

```text
Dirty price = Clean price + Accrued interest
```

### Current yield

```text
Current yield = Annual coupon / Bond price
```

### Discount factor

```text
DF(t) = 1 / (1 + spot rate)^t
```

### Bond price using spot rates

```text
Price = CF1×DF1 + CF2×DF2 + ... + CFn×DFn
```

### Modified duration approximation

```text
% Price Change ≈ -Modified Duration × ΔYield
```

### Duration and convexity approximation

```text
% Price Change ≈ -Duration × ΔYield + 0.5 × Convexity × (ΔYield)^2
```

### Credit spread

```text
Credit spread = Corporate bond yield - Government bond yield
```

### Real rate approximation

```text
Real rate ≈ Nominal rate - Inflation
```

---

## 75. Possible API endpoints

Possible Athena API endpoints for the Rates Lab:

```text
GET  /api/rates/yield-curves
GET  /api/rates/yield-curves/{curve_id}
GET  /api/rates/spot-rates
POST /api/rates/discount-factors
POST /api/rates/bond-price
POST /api/rates/bond-cash-flows
POST /api/rates/yield-to-maturity
POST /api/rates/duration
POST /api/rates/convexity
POST /api/rates/rate-shock
POST /api/rates/curve-shock
```

### Example bond price request

```json
{
  "face_value": 1000,
  "coupon_rate": 0.05,
  "yield_to_maturity": 0.04,
  "maturity_years": 3,
  "payments_per_year": 1
}
```

### Example response

```json
{
  "price": 1027.75,
  "premium_discount_status": "premium",
  "cash_flows": [
    {"period": 1, "cash_flow": 50, "present_value": 48.08},
    {"period": 2, "cash_flow": 50, "present_value": 46.23},
    {"period": 3, "cash_flow": 1050, "present_value": 933.44}
  ]
}
```

---

## 76. Possible frontend components

Possible components for Athena's Rates Lab:

```text
YieldCurveChart
CurveShapeBadge
SpotRatesTable
DiscountFactorsTable
BondPricingForm
BondCashFlowTable
BondPriceCard
YieldToMaturityCard
DurationCard
ModifiedDurationCard
ConvexityCard
RateShockPanel
CurveShockPanel
MaturityBucketChart
CreditSpreadCard
DataQualityWarnings
```

### Page goal

The Rates Lab should help the user understand:

- how rates are structured by maturity;
- how bonds are priced;
- why bond prices change when yields move;
- how duration estimates rate sensitivity;
- how rate shocks affect bond value.

---

## 77. Suggested tests

### Bond pricing tests

```text
Bond price equals par when coupon rate = yield.
Bond price is above par when coupon rate > yield.
Bond price is below par when coupon rate < yield.
Bond price decreases when yield increases.
```

### Discount factor tests

```text
Discount factor is less than 1 for positive rates.
Discount factor decreases as maturity increases.
Discount factor decreases as spot rate increases.
```

### Duration tests

```text
Duration is positive.
Zero-coupon bond duration equals maturity.
Longer maturity generally increases duration.
Higher coupon generally decreases duration.
```

### Convexity tests

```text
Convexity is positive for standard option-free bonds.
Convexity improves the price change approximation.
```

### Rate shock tests

```text
Positive rate shock decreases bond price.
Negative rate shock increases bond price.
Dollar loss matches duration approximation direction.
```

### Data validation tests

```text
Negative face value is rejected.
Negative maturity is rejected.
Invalid coupon frequency is rejected.
Missing currency is flagged.
Maturity before valuation date is rejected.
```

---

## 78. How Athena uses fixed income

Athena AI Risk Terminal should use fixed income knowledge in the **Rates Lab** and later in portfolio risk.

### Main features

Athena should support:

```text
Yield curve visualization
Spot rates table
Discount factors table
Bond cash flow schedule
Bond price calculator
Yield to maturity solver
Duration calculator
Convexity calculator
Rate shock stress test
Curve shape classification
Bond data quality checks
```

### Example workflow

```text
1. User enters bond characteristics.
2. Athena generates cash flows.
3. Athena discounts the cash flows.
4. Athena returns the bond price.
5. Athena calculates duration and convexity.
6. Athena applies a rate shock.
7. Athena estimates price impact.
8. Athena explains the result clearly.
```

### Example explanation

```text
The bond price decreases under a +100 bps rate shock because fixed cash flows are discounted at a higher yield. The modified duration of 6.2 implies an approximate price decrease of 6.2%, partially adjusted by convexity.
```

### Data model idea

```text
Bond
YieldCurve
CurvePoint
SpotRate
DiscountFactor
BondValuation
RateShockResult
```

---

## 79. Summary

Fixed income is the study of debt instruments.

The most important fixed income instrument is the bond.

A bond is a set of future cash flows.  
The bond price is the present value of those cash flows.

Core ideas:

```text
Bond price = present value of future cash flows
Yields rise → bond prices fall
Yields fall → bond prices rise
Duration measures interest rate sensitivity
Convexity improves duration for larger rate moves
Yield curves show rates by maturity
Spot rates discount cash flows at specific maturities
Credit spreads compensate for credit risk
Liquidity matters in bond markets
```

For Athena AI Risk Terminal, this document prepares the implementation of:

- Rates Lab;
- YieldCurveChart;
- SpotRatesTable;
- DiscountFactorsTable;
- BondPricingForm;
- BondCashFlowTable;
- DurationCard;
- ConvexityCard;
- RateShockPanel;
- bond market data validation.

The key lesson is:

```text
Fixed income is not just about receiving coupons.
It is about cash flows, discount rates, yield curves, credit risk, liquidity and sensitivity to interest rate changes.
```
