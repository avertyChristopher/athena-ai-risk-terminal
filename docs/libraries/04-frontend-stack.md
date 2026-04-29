# 04 — Frontend Stack

**Project:** Athena AI Risk Terminal  
**Recommended file path:** `docs/libraries/04-frontend-stack.md`  
**Purpose:** understand the frontend technologies and design patterns needed to build Athena's user interface: dashboards, forms, tables, charts, bilingual content, API integration, state management and professional risk-terminal UX.  
**Scope:** this document focuses on the frontend stack: React, TypeScript, Vite, Tailwind CSS, shadcn/ui, TanStack Query, React Hook Form, Zod, Recharts, i18next, frontend architecture, testing and UI/UX best practices.

---

## Table of Contents

1. What is a frontend?
2. Why Athena needs a strong frontend
3. Frontend role in Athena
4. Frontend vs backend
5. Frontend vs notebooks
6. Recommended frontend stack
7. React overview
8. Why React for Athena
9. Vite overview
10. TypeScript overview
11. Why TypeScript matters
12. Components
13. Props
14. State
15. Events
16. Conditional rendering
17. Lists and keys
18. Component composition
19. Feature-based architecture
20. Routing
21. Layouts
22. Pages vs components
23. UI components
24. shadcn/ui overview
25. Tailwind CSS overview
26. Utility-first styling
27. Responsive design
28. Dark mode
29. Design system
30. Cards
31. Tables
32. Forms
33. Badges
34. Modals and drawers
35. Toasts and alerts
36. Loading states
37. Empty states
38. Error states
39. Skeletons
40. API integration
41. Fetching data
42. API client
43. TanStack Query overview
44. Queries
45. Mutations
46. Query keys
47. Loading and error handling with TanStack Query
48. Cache invalidation
49. React Hook Form overview
50. Zod overview
51. Form validation
52. Trade ticket form
53. Option pricing form
54. Portfolio form
55. Risk scenario form
56. Data tables
57. Sorting
58. Filtering
59. Pagination
60. Charts overview
61. Recharts overview
62. Line charts
63. Bar charts
64. Pie and allocation charts
65. Area charts
66. Scatter plots
67. Risk dashboard charts
68. P&L charts
69. Yield curve charts
70. Option payoff charts
71. Internationalization overview
72. react-i18next overview
73. English and French structure
74. Translation keys
75. Formatting numbers
76. Formatting currencies
77. Formatting dates
78. Frontend data types
79. Shared API types
80. Frontend folder structure
81. Feature modules
82. Dashboard feature
83. Portfolio feature
84. Market data feature
85. Trade simulator feature
86. Risk monitor feature
87. Options pricing feature
88. RiskDNA feature
89. P&L and reports feature
90. Accessibility basics
91. Performance basics
92. Frontend testing
93. Unit tests
94. Component tests
95. API mocking
96. End-to-end tests
97. Code quality tools
98. Common beginner mistakes
99. Athena frontend development workflow
100. Summary

---

## 1. What is a frontend?

The frontend is the part of an application that users see and interact with.

It includes:

```text
Pages
Buttons
Forms
Charts
Tables
Navigation
Dashboards
Modals
Alerts
User interactions
```

In Athena, the frontend is the visual layer of the risk terminal.

It lets the user:

```text
Create portfolios
View market data
Simulate trades
Calculate risk
View VaR and CVaR
Run stress scenarios
Price options
View Greeks
Read RiskDNA explanations
Generate reports
```

Simple idea:

```text
Frontend = user interface.
Backend = data and logic engine.
```

The frontend should make complex financial information clear and usable.

---

## 2. Why Athena needs a strong frontend

Athena is not only about calculations.

It is also about making finance and risk understandable.

A strong frontend helps users:

```text
Understand portfolio structure
Interpret risk metrics
Compare before and after trade impact
See risk warnings quickly
Read explanations clearly
Interact with charts
Generate reports
```

Bad frontend:

```text
Numbers everywhere
No hierarchy
No clear status
No explanations
No visual structure
```

Good frontend:

```text
Clear dashboard
Important metrics first
Risk badges
Good charts
Readable tables
Clean forms
Consistent design
Bilingual interface
```

### Athena goal

Athena should feel like:

```text
A professional risk terminal
A learning platform
A portfolio analytics dashboard
A middle-office control tool
```

---

## 3. Frontend role in Athena

The frontend should not calculate official financial metrics.

Its role is to:

```text
Collect user input
Send requests to backend
Display backend results
Show charts and tables
Guide user workflow
Display warnings
Support bilingual content
Improve understanding
```

### Example

For option pricing:

```text
Frontend displays form.
User enters spot, strike, volatility, rate and maturity.
Frontend sends request to backend.
Backend calculates Black-Scholes price and Greeks.
Frontend displays results in cards, table and charts.
```

### Key rule

```text
Frontend displays finance logic.
Backend owns finance logic.
```

This keeps calculations consistent and testable.

---

## 4. Frontend vs backend

Frontend and backend have different responsibilities.

### Frontend

```text
User interface
Forms
Charts
Tables
Routing
Client-side state
API calls
Translations
User experience
```

### Backend

```text
Validation
Business logic
Finance calculations
Database
Authentication later
Report generation
Risk workflows
```

### Example

Frontend:

```text
Shows a TradeTicketForm.
```

Backend:

```text
Validates trade and calculates before/after risk impact.
```

Frontend:

```text
Displays PreTradeCheckPanel and RiskImpactChart.
```

The frontend should not duplicate backend calculations unless it is only for temporary visual preview and clearly not official.

---

## 5. Frontend vs notebooks

Notebooks are for exploration and learning.

Frontend is for product experience.

### Notebooks

Good for:

```text
Testing formulas
Visualizing data quickly
Learning concepts
Prototyping charts
```

### Frontend

Good for:

```text
Reusable UI
Interactive workflows
Clean dashboards
User-facing forms
API-driven data
Professional presentation
```

### Athena workflow

```text
Notebook proves the chart concept.
Backend exposes the metric.
Frontend displays it beautifully.
```

Example:

```text
Notebook: plot VaR loss distribution with matplotlib.
Frontend: display LossDistributionChart with Recharts.
```

---

## 6. Recommended frontend stack

Recommended Athena frontend stack:

```text
React
TypeScript
Vite
Tailwind CSS
shadcn/ui
TanStack Query
React Hook Form
Zod
Recharts
react-i18next
Vitest
React Testing Library
Playwright or Cypress later
ESLint
Prettier
```

### Main roles

```text
React              = UI library
TypeScript         = typed JavaScript
Vite               = fast build tool
Tailwind CSS       = styling
shadcn/ui          = reusable UI components
TanStack Query     = server state and API data
React Hook Form    = form management
Zod                = frontend validation
Recharts           = charts
react-i18next      = bilingual interface
Vitest             = unit/component tests
Playwright/Cypress = end-to-end tests
```

### Athena recommendation

Start with:

```text
React
TypeScript
Vite
Tailwind CSS
shadcn/ui
TanStack Query
Recharts
```

Then add:

```text
React Hook Form
Zod
react-i18next
testing tools
```

---

## 7. React overview

React is a JavaScript library for building user interfaces.

It is based on components.

A component is a reusable piece of UI.

Example:

```tsx
function RiskCard() {
  return (
    <div>
      <h2>Portfolio VaR</h2>
      <p>12,500 CAD</p>
    </div>
  );
}
```

React lets you build complex applications from small components.

### Athena use

Athena can have components like:

```text
RiskSummaryCard
PortfolioTable
TradeTicketForm
OptionPricingForm
GreeksTable
RiskDNACard
PnLChart
```

---

## 8. Why React for Athena

React is a good choice for Athena because Athena needs:

```text
Interactive dashboards
Reusable cards
Reusable forms
Charts
Tables
Stateful workflows
API-driven data
Modular features
```

React is also widely used and works well with TypeScript.

### Example Athena dashboard

```text
RiskSummaryCard
PortfolioValueCard
VaRChart
StressScenarioTable
RiskDNAExplanationPanel
```

Each piece can be a React component.

### Core advantage

React makes it easier to separate UI into manageable parts.

---

## 9. Vite overview

Vite is a modern frontend build tool.

It provides:

```text
Fast development server
Hot module replacement
Simple React setup
Fast builds
Good TypeScript support
```

Create a React + TypeScript project:

```bash
npm create vite@latest frontend -- --template react-ts
```

Run development server:

```bash
cd frontend
npm install
npm run dev
```

Typical local URL:

```text
http://localhost:5173
```

### Athena use

Use Vite for the Athena frontend.

---

## 10. TypeScript overview

TypeScript is JavaScript with static types.

Example:

```ts
type RiskMetric = {
  portfolioId: string;
  varAmount: number;
  cvarAmount: number;
  currency: string;
};
```

TypeScript helps catch errors before runtime.

### Without TypeScript

```js
risk.varAmunt
```

This typo may fail at runtime.

### With TypeScript

```ts
risk.varAmunt
```

TypeScript can warn that `varAmunt` does not exist.

### Athena use

Finance apps have many structured objects.

TypeScript helps keep them consistent.

---

## 11. Why TypeScript matters

TypeScript matters because Athena has complex data:

```text
Portfolios
Positions
Trades
Risk metrics
Stress scenarios
Options
Greeks
RiskDNA scores
P&L records
Reports
```

Types help define exactly what data looks like.

Example:

```ts
export type OptionGreeks = {
  delta: number;
  gamma: number;
  vega: number;
  theta: number;
  rho: number;
};
```

### Benefits

```text
Fewer runtime bugs
Better autocomplete
Clearer API contracts
Easier refactoring
More professional code
```

### Athena rule

Use TypeScript types for all API responses.

---

## 12. Components

Components are reusable UI pieces.

Example:

```tsx
type MetricCardProps = {
  title: string;
  value: string;
  description?: string;
};

export function MetricCard({ title, value, description }: MetricCardProps) {
  return (
    <div className="rounded-2xl border p-4 shadow-sm">
      <h3 className="text-sm text-muted-foreground">{title}</h3>
      <p className="text-2xl font-semibold">{value}</p>
      {description && <p className="text-sm">{description}</p>}
    </div>
  );
}
```

### Athena components

```text
MetricCard
RiskLevelBadge
PortfolioWeightTable
VaRChart
OptionPayoffChart
ReportPreview
```

### Rule

A component should have one clear responsibility.

---

## 13. Props

Props are inputs passed to components.

Example:

```tsx
<MetricCard
  title="1-Day VaR"
  value="12,500 CAD"
  description="95% confidence level"
/>
```

The component receives:

```tsx
type MetricCardProps = {
  title: string;
  value: string;
  description?: string;
};
```

### Athena use

Props let you reuse the same component for different metrics.

Example:

```tsx
<MetricCard title="VaR" value="12,500 CAD" />
<MetricCard title="CVaR" value="18,900 CAD" />
<MetricCard title="Volatility" value="21.4%" />
```

---

## 14. State

State represents data that changes in the UI.

Example:

```tsx
import { useState } from "react";

function Counter() {
  const [count, setCount] = useState(0);

  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

### Athena examples

State can store:

```text
Selected portfolio
Selected date range
Open modal
Form values
Active tab
Selected scenario
```

### Important

Do not store server data manually if TanStack Query manages it.

Use local state for UI state.

Use TanStack Query for API data.

---

## 15. Events

Events respond to user actions.

Examples:

```text
Click button
Submit form
Change input
Select dropdown
Open modal
Switch tab
```

React example:

```tsx
<button onClick={() => console.log("Clicked")}>
  Calculate Risk
</button>
```

Form submit example:

```tsx
<form onSubmit={handleSubmit}>
  ...
</form>
```

### Athena use

Events trigger workflows:

```text
Calculate VaR
Simulate trade
Generate report
Run stress test
Price option
Change language
```

---

## 16. Conditional rendering

Conditional rendering shows UI based on conditions.

Example:

```tsx
{isLoading && <p>Loading...</p>}
{error && <p>Something went wrong.</p>}
{data && <RiskDashboard data={data} />}
```

### Athena use

Common conditions:

```text
Loading state
Error state
Empty portfolio
No market data
Risk warning
Limit breach
Report not generated yet
```

Example:

```tsx
{riskLevel === "Critical" && (
  <Alert>
    Critical risk level detected.
  </Alert>
)}
```

---

## 17. Lists and keys

React renders lists with `.map()`.

Example:

```tsx
{positions.map((position) => (
  <PositionRow key={position.id} position={position} />
))}
```

The `key` helps React identify each item.

### Athena use

Lists are everywhere:

```text
Positions
Trades
Reports
Risk drivers
P&L contributors
Stress scenarios
Workflow events
```

### Rule

Use stable IDs as keys.

Avoid using array index as key when data can change.

---

## 18. Component composition

Composition means building large UI from smaller components.

Example:

```tsx
function RiskDashboard() {
  return (
    <PageLayout>
      <RiskSummaryCards />
      <RiskCharts />
      <RiskDriverTable />
      <RiskDNAExplanationPanel />
    </PageLayout>
  );
}
```

### Why composition matters

It makes the frontend:

```text
Readable
Reusable
Testable
Maintainable
```

### Athena rule

Avoid giant components with hundreds of lines.

Break dashboards into smaller components.

---

## 19. Feature-based architecture

A feature-based architecture groups code by business feature.

Example:

```text
features/
├── dashboard/
├── portfolio/
├── market-data/
├── trade-simulator/
├── risk-monitor/
├── options-pricing/
├── riskdna/
├── pnl/
└── reports/
```

Each feature can contain:

```text
components
api
hooks
types
utils
pages
```

### Why feature-based architecture works for Athena

Athena has clear modules.

A feature-based structure keeps related UI together.

Better than having one huge `components/` folder with everything mixed.

---

## 20. Routing

Routing maps URLs to pages.

Common library:

```text
react-router-dom
```

Example routes:

```text
/
/dashboard
/portfolios
/market-data
/trade-simulator
/risk-monitor
/options
/riskdna
/pnl
/reports
```

Example:

```tsx
import { createBrowserRouter } from "react-router-dom";

export const router = createBrowserRouter([
  { path: "/", element: <DashboardPage /> },
  { path: "/portfolios", element: <PortfoliosPage /> },
  { path: "/risk-monitor", element: <RiskMonitorPage /> },
]);
```

### Athena use

Each major module should have a route.

---

## 21. Layouts

A layout defines shared page structure.

Common layout elements:

```text
Sidebar
Top navigation
Main content area
Footer
Breadcrumb
Theme toggle
Language switcher
```

Example:

```tsx
export function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 p-6">{children}</main>
    </div>
  );
}
```

### Athena layout

Athena should feel like a terminal/dashboard.

Recommended layout:

```text
Left sidebar navigation
Top header with portfolio selector
Main content dashboard
Right panel optional for explanations
```

---

## 22. Pages vs components

Pages are route-level views.

Components are reusable UI pieces.

Example pages:

```text
DashboardPage
PortfolioPage
RiskMonitorPage
OptionsPricingPage
ReportsPage
```

Example components:

```text
MetricCard
RiskLevelBadge
GreeksTable
PayoffChart
TradeTicketForm
```

### Rule

Pages compose components.

Components should not know too much about routing.

### Athena example

`RiskMonitorPage` may include:

```text
RiskSummaryCards
VaRChart
StressScenarioTable
RiskDNAPanel
LimitStatusPanel
```

---

## 23. UI components

UI components are generic building blocks.

Examples:

```text
Button
Card
Input
Select
Dialog
Table
Badge
Tabs
Tooltip
Dropdown
Alert
```

Athena should use a consistent UI component system.

This avoids inconsistent design.

### Recommended

Use:

```text
shadcn/ui
Tailwind CSS
```

This combination gives a professional look without building every component from scratch.

---

## 24. shadcn/ui overview

shadcn/ui is a collection of reusable components built with Radix UI and Tailwind CSS.

It provides components like:

```text
Button
Card
Input
Dialog
Dropdown Menu
Table
Tabs
Badge
Alert
Select
Textarea
Tooltip
```

### Why it is good for Athena

Athena needs many dashboard components.

shadcn/ui helps build a clean interface quickly.

Example Athena components using shadcn/ui:

```text
Risk card
Trade form
Options pricing form
Report dialog
Risk driver table
Alert panel
```

### Important

shadcn/ui components are copied into your project, so you can customize them.

---

## 25. Tailwind CSS overview

Tailwind CSS is a utility-first CSS framework.

Instead of writing custom CSS classes, you compose utility classes.

Example:

```tsx
<div className="rounded-2xl border p-4 shadow-sm">
  <h3 className="text-sm text-muted-foreground">VaR</h3>
  <p className="text-2xl font-semibold">12,500 CAD</p>
</div>
```

### Benefits

```text
Fast styling
Consistent spacing
Responsive design
Easy customization
Works well with components
```

### Athena use

Tailwind is excellent for dashboards, cards and layouts.

---

## 26. Utility-first styling

Utility-first styling uses small classes for each style.

Example:

```text
p-4          = padding
rounded-2xl  = rounded corners
shadow-sm    = small shadow
text-sm      = small text
font-semibold = semi-bold font
grid         = grid layout
gap-4        = spacing between grid items
```

Example:

```tsx
<div className="grid grid-cols-1 gap-4 md:grid-cols-3">
  <MetricCard title="VaR" value="12,500 CAD" />
  <MetricCard title="CVaR" value="18,900 CAD" />
  <MetricCard title="Volatility" value="21.4%" />
</div>
```

### Athena rule

Use consistent spacing and grid layouts.

---

## 27. Responsive design

Responsive design means the UI works on different screen sizes.

Tailwind example:

```tsx
<div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
  ...
</div>
```

Meaning:

```text
1 column on small screens
2 columns on medium screens
4 columns on extra-large screens
```

### Athena use

Athena is dashboard-heavy, so desktop is the main target.

But it should still be usable on laptops and tablets.

### Rule

Do not design only for one screen size.

---

## 28. Dark mode

Dark mode is common for finance terminals.

It can make dashboards feel professional.

Tailwind and shadcn/ui support dark mode.

Example:

```tsx
<div className="bg-background text-foreground">
  ...
</div>
```

### Athena recommendation

Support both:

```text
light mode
dark mode
```

But make dark mode especially polished.

### Finance terminal aesthetic

Dark mode can work well for:

```text
Risk dashboards
Charts
Alerts
Market data
Trading workflows
```

---

## 29. Design system

A design system defines reusable visual rules.

It includes:

```text
Colors
Typography
Spacing
Cards
Tables
Badges
Buttons
Charts
Status colors
Icons
Layouts
```

### Athena statuses

Risk statuses should be consistent:

```text
Low
Medium
High
Critical
OK
Warning
Breach
```

### Important

Do not randomly style every page.

Use reusable components:

```text
MetricCard
StatusBadge
SectionHeader
DataTable
ChartCard
```

This makes Athena feel coherent.

---

## 30. Cards

Cards group information.

Example:

```tsx
<Card>
  <CardHeader>
    <CardTitle>Portfolio VaR</CardTitle>
  </CardHeader>
  <CardContent>
    <p className="text-2xl font-semibold">12,500 CAD</p>
  </CardContent>
</Card>
```

### Athena card examples

```text
Portfolio Value Card
Daily P&L Card
VaR Card
CVaR Card
RiskDNA Card
Limit Usage Card
Option Price Card
```

### Good card design

A card should include:

```text
Title
Main value
Context
Status if relevant
Trend if useful
```

---

## 31. Tables

Tables are essential for finance.

Athena tables:

```text
Positions table
Trades table
Risk drivers table
P&L contributors table
Stress scenarios table
Greeks table
Reports table
```

Good table features:

```text
Sorting
Filtering
Pagination
Sticky header if needed
Numeric alignment
Status badges
Empty state
```

### Numeric alignment

Financial numbers should often be right-aligned.

Example:

```text
Symbol | Quantity | Price | Market Value
AAPL   |       10 | 200.0 |      2,000.0
```

This improves readability.

---

## 32. Forms

Forms collect user input.

Athena forms:

```text
Portfolio creation form
Trade ticket form
Option pricing form
Stress scenario form
Report generation form
Risk limit form
```

Good forms need:

```text
Clear labels
Validation
Helpful error messages
Default values
Submission state
Reset/cancel behavior
```

### Example

An option pricing form should validate:

```text
spot price > 0
strike price > 0
time to maturity > 0
volatility > 0
```

---

## 33. Badges

Badges show compact status.

Examples:

```text
Low
Medium
High
Critical
OK
Warning
Breach
Draft
Approved
Rejected
Generated
```

Example component:

```tsx
<RiskLevelBadge level="High" />
```

### Athena use

Badges should be used for:

```text
Risk level
Trade status
Report status
Limit status
Data quality
AI review status
```

### Rule

Status labels should be visually consistent across the app.

---

## 34. Modals and drawers

Modals and drawers show secondary information without leaving the page.

Examples:

```text
Trade details
Risk driver explanation
Report preview
Edit portfolio modal
AI explanation review
```

### Modal

Good for focused actions.

Example:

```text
Confirm report approval
```

### Drawer

Good for detailed side panels.

Example:

```text
Open Risk Driver Details
```

### Athena use

A right-side drawer is useful for explanations.

---

## 35. Toasts and alerts

Toasts are temporary notifications.

Examples:

```text
Portfolio created.
Report generated.
Trade simulation completed.
```

Alerts are persistent warnings.

Examples:

```text
Risk limit breached.
Market data missing.
Report validation failed.
```

### Athena rule

Use alerts for important financial warnings.

Do not hide critical issues in temporary toasts only.

---

## 36. Loading states

Loading states tell the user data is being fetched.

Examples:

```text
Loading portfolio...
Calculating risk...
Generating report...
```

Good loading states reduce confusion.

### Athena examples

```tsx
if (isLoading) {
  return <RiskDashboardSkeleton />;
}
```

Possible loading components:

```text
Skeleton cards
Spinner
Progress indicator
Job status panel
```

For long calculations, show job status.

---

## 37. Empty states

Empty states explain what to do when there is no data.

Bad:

```text
Blank page
```

Better:

```text
No portfolios yet. Create your first portfolio to start analyzing risk.
```

Athena empty states:

```text
No portfolio selected
No positions yet
No trades found
No reports generated
No market data available
No risk metrics calculated
```

### Good empty state includes

```text
Short explanation
Next action
Button if useful
```

---

## 38. Error states

Error states show what went wrong.

Example:

```text
Unable to load risk metrics.
```

Better:

```text
Unable to load risk metrics because market data is missing for this portfolio.
```

### Athena error types

```text
API error
Validation error
Missing data
Calculation error
Permission error later
Report generation error
```

### Rule

Errors should be understandable and actionable.

---

## 39. Skeletons

Skeletons are placeholder UI elements shown while data loads.

Example:

```tsx
<div className="h-24 animate-pulse rounded-2xl bg-muted" />
```

Skeletons are useful for dashboards.

Athena skeleton examples:

```text
Metric card skeleton
Table skeleton
Chart skeleton
Report preview skeleton
```

### Why skeletons help

They make loading feel smoother and show the page structure before data arrives.

---

## 40. API integration

API integration connects frontend to backend.

Basic flow:

```text
Frontend calls backend endpoint.
Backend returns JSON.
Frontend displays result.
```

Example:

```ts
const response = await fetch("/api/portfolios");
const portfolios = await response.json();
```

### Athena recommendation

Do not call `fetch` everywhere manually.

Create an API client.

Use TanStack Query for data fetching.

---

## 41. Fetching data

Basic fetch:

```ts
async function getPortfolios() {
  const response = await fetch("http://localhost:8000/api/portfolios");

  if (!response.ok) {
    throw new Error("Failed to fetch portfolios");
  }

  return response.json();
}
```

### Problems with raw fetch everywhere

```text
Repeated code
No caching
Manual loading states
Manual error states
Harder refactoring
```

### Better

Use:

```text
API client
TanStack Query hooks
```

---

## 42. API client

An API client centralizes backend calls.

Example:

```ts
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function apiGet<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`);

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json() as Promise<T>;
}
```

Use:

```ts
const portfolios = await apiGet<Portfolio[]>("/api/portfolios");
```

### Athena use

Create:

```text
frontend/src/lib/api-client.ts
```

This keeps API logic consistent.

---

## 43. TanStack Query overview

TanStack Query manages server state.

It handles:

```text
Fetching
Caching
Loading states
Error states
Refetching
Mutations
Cache invalidation
```

Install:

```bash
npm install @tanstack/react-query
```

Setup:

```tsx
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();

<QueryClientProvider client={queryClient}>
  <App />
</QueryClientProvider>
```

### Athena use

Use TanStack Query for API data.

---

## 44. Queries

Queries fetch data.

Example:

```tsx
import { useQuery } from "@tanstack/react-query";

function usePortfolios() {
  return useQuery({
    queryKey: ["portfolios"],
    queryFn: () => apiGet<Portfolio[]>("/api/portfolios"),
  });
}
```

Use:

```tsx
const { data, isLoading, error } = usePortfolios();
```

### Athena query examples

```text
usePortfolios
usePortfolioSummary
useRiskMetrics
useRiskDNA
useReports
useTrades
useMarketPrices
```

---

## 45. Mutations

Mutations change data or trigger actions.

Examples:

```text
Create portfolio
Simulate trade
Generate report
Approve report
Run stress test
```

Example:

```tsx
import { useMutation, useQueryClient } from "@tanstack/react-query";

function useCreatePortfolio() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (input: CreatePortfolioInput) =>
      apiPost<Portfolio>("/api/portfolios", input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["portfolios"] });
    },
  });
}
```

### Athena use

Use mutations for user actions.

---

## 46. Query keys

Query keys identify cached data.

Examples:

```ts
["portfolios"]
["portfolio", portfolioId]
["risk", portfolioId]
["riskdna", portfolioId]
["reports", portfolioId]
```

### Good query keys

Good:

```ts
["risk", portfolioId, { date }]
```

Bad:

```ts
["data"]
```

### Athena rule

Use descriptive query keys so cache invalidation is precise.

---

## 47. Loading and error handling with TanStack Query

Example:

```tsx
const { data, isLoading, error } = useRiskMetrics(portfolioId);

if (isLoading) {
  return <RiskDashboardSkeleton />;
}

if (error) {
  return <ErrorState message="Unable to load risk metrics." />;
}

return <RiskDashboard data={data} />;
```

### Athena rule

Every API-driven page should handle:

```text
Loading
Error
Empty
Success
```

This makes the app feel stable.

---

## 48. Cache invalidation

Cache invalidation refreshes stale data after changes.

Example:

```tsx
queryClient.invalidateQueries({ queryKey: ["portfolio", portfolioId] });
queryClient.invalidateQueries({ queryKey: ["risk", portfolioId] });
```

### Athena example

After simulating or applying a trade, refresh:

```text
portfolio summary
positions
risk metrics
RiskDNA
P&L if affected
```

### Rule

When a mutation changes data, invalidate related queries.

---

## 49. React Hook Form overview

React Hook Form manages forms efficiently.

Install:

```bash
npm install react-hook-form
```

Example:

```tsx
import { useForm } from "react-hook-form";

type FormValues = {
  name: string;
  baseCurrency: string;
};

function PortfolioForm() {
  const form = useForm<FormValues>();

  function onSubmit(values: FormValues) {
    console.log(values);
  }

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      <input {...form.register("name")} />
      <button type="submit">Create</button>
    </form>
  );
}
```

### Athena use

Use for:

```text
Portfolio forms
Trade forms
Option pricing forms
Stress scenario forms
Report forms
```

---

## 50. Zod overview

Zod is a TypeScript validation library.

Install:

```bash
npm install zod
```

Example:

```ts
import { z } from "zod";

const optionPricingSchema = z.object({
  spotPrice: z.number().positive(),
  strikePrice: z.number().positive(),
  timeToMaturity: z.number().positive(),
  volatility: z.number().positive(),
});
```

### Why Zod matters

Zod validates frontend form inputs before sending them to backend.

### Athena rule

Frontend validation improves UX, but backend validation remains mandatory.

Never rely only on frontend validation.

---

## 51. Form validation

React Hook Form and Zod work well together.

Install resolver:

```bash
npm install @hookform/resolvers
```

Example:

```tsx
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

const schema = z.object({
  spotPrice: z.number().positive(),
  strikePrice: z.number().positive(),
});

type FormValues = z.infer<typeof schema>;

const form = useForm<FormValues>({
  resolver: zodResolver(schema),
});
```

### Athena validation examples

```text
price > 0
quantity > 0
volatility > 0
confidence level between 0 and 1
portfolio name required
```

---

## 52. Trade ticket form

A TradeTicketForm collects proposed trade information.

Fields:

```text
portfolio
symbol
side
quantity
order type
estimated price
currency
trade reason
```

Validation:

```text
symbol required
side must be buy or sell
quantity > 0
estimated price > 0
```

Example workflow:

```text
User enters trade
Frontend validates form
Frontend sends POST /api/trades/simulate
Backend returns before/after impact
Frontend displays results
```

### Athena components

```text
TradeTicketForm
PreTradeCheckPanel
BeforeAfterRiskImpact
```

---

## 53. Option pricing form

An OptionPricingForm collects Black-Scholes inputs.

Fields:

```text
spot price
strike price
time to maturity
risk-free rate
volatility
dividend yield
option type optional
```

Validation:

```text
spot price > 0
strike price > 0
time to maturity > 0
volatility > 0
```

Output components:

```text
CallPriceCard
PutPriceCard
GreeksTable
PayoffChart
PutCallParityCheck
```

### Athena workflow

```text
User enters inputs
Backend calculates price and Greeks
Frontend displays results and charts
```

---

## 54. Portfolio form

A PortfolioForm creates or edits portfolio metadata.

Fields:

```text
name
description
base currency
benchmark
risk profile optional
```

Validation:

```text
name required
base currency required
benchmark optional
```

Possible base currencies:

```text
CAD
USD
EUR
GBP
```

### Athena use

Portfolio forms are the starting point for the whole system.

A portfolio must exist before risk, P&L and reports make sense.

---

## 55. Risk scenario form

A RiskScenarioForm defines stress testing assumptions.

Fields:

```text
scenario name
equity shock
rate shock
FX shock
volatility shock
liquidity shock
description
```

Example:

```text
Equity shock = -20%
Rate shock = +100 bps
Volatility shock = +50%
```

Validation:

```text
scenario name required
shock values must be numeric
```

### Athena use

Frontend collects scenario inputs.  
Backend applies shocks and calculates stressed losses.

---

## 56. Data tables

Data tables are central to Athena.

Tables include:

```text
Positions
Trades
Risk drivers
P&L contributors
Stress scenarios
Reports
Market data
Options Greeks
```

Good data table features:

```text
Sorting
Filtering
Pagination
Column alignment
Status badges
Export
Row details
```

### Athena recommendation

Start with simple tables.  
Add advanced table library later if needed.

Possible library:

```text
TanStack Table
```

---

## 57. Sorting

Sorting helps users analyze tables.

Examples:

```text
Sort positions by market value
Sort P&L contributors by loss
Sort risk drivers by severity
Sort reports by date
```

Frontend sorting can be local for small datasets.

Backend sorting is better for large datasets.

Example query:

```text
GET /api/trades?sort_by=trade_date&sort_order=desc
```

### Athena rule

For large data, sort on backend.

---

## 58. Filtering

Filtering narrows data.

Examples:

```text
Trades by status
Positions by sector
Reports by type
Risk drivers by severity
P&L by asset
```

Example:

```text
GET /api/trades?status=approved
```

Frontend filters are fine for small tables.

Backend filters are better for large data.

### Athena use

Filtering makes dashboards usable.

---

## 59. Pagination

Pagination splits large tables into pages.

Example:

```text
Page 1, 50 rows per page
```

API:

```text
GET /api/trades?page=1&page_size=50
```

Response:

```json
{
  "items": [],
  "page": 1,
  "page_size": 50,
  "total": 240
}
```

### Athena use

Use pagination for:

```text
Trades
Reports
Workflow events
Audit trail
Market data
```

---

## 60. Charts overview

Charts are essential in Athena.

Chart types:

```text
Line chart
Bar chart
Area chart
Pie chart
Scatter plot
Histogram
Gauge
Heatmap later
```

Athena charts:

```text
Portfolio value over time
Cumulative returns
Rolling volatility
VaR trend
RiskDNA timeline
P&L chart
Yield curve
Option payoff
Stress scenario losses
```

### Rule

A chart should answer a specific question.

Bad:

```text
Random chart because it looks good.
```

Better:

```text
Rolling volatility chart shows whether risk is increasing.
```

---

## 61. Recharts overview

Recharts is a charting library for React.

Install:

```bash
npm install recharts
```

Example:

```tsx
import { LineChart, Line, XAxis, YAxis, Tooltip } from "recharts";

<LineChart width={600} height={300} data={data}>
  <XAxis dataKey="date" />
  <YAxis />
  <Tooltip />
  <Line type="monotone" dataKey="value" />
</LineChart>
```

### Athena use

Recharts is good for:

```text
Line charts
Bar charts
Area charts
Pie charts
Responsive dashboard charts
```

---

## 62. Line charts

Line charts show values over time.

Athena examples:

```text
Portfolio value over time
Cumulative P&L
RiskDNA score timeline
Rolling volatility
VaR trend
```

Example data:

```ts
const data = [
  { date: "2026-04-27", value: 100000 },
  { date: "2026-04-28", value: 101200 },
  { date: "2026-04-29", value: 99600 },
];
```

Use line charts for time series.

---

## 63. Bar charts

Bar charts compare categories.

Athena examples:

```text
P&L by asset
Stress loss by scenario
Risk contribution by asset
Sector exposure
Top contributors
Worst contributors
```

Example:

```text
AAPL: -800
NVDA: -1400
MSFT: +300
```

Bar charts are excellent for ranking.

---

## 64. Pie and allocation charts

Pie or donut charts show allocation.

Athena examples:

```text
Sector allocation
Asset class allocation
Currency allocation
Country allocation
```

### Caution

Pie charts can become hard to read with many categories.

For many categories, use bar charts.

### Athena rule

Use pie/donut charts for high-level allocation only.

Use tables for detail.

---

## 65. Area charts

Area charts show filled time series.

Athena examples:

```text
Portfolio value
Cumulative return
Drawdown area
Risk exposure over time
```

Area charts can emphasize magnitude.

### Caution

Do not use too many overlapping areas.

Keep chart interpretation clear.

---

## 66. Scatter plots

Scatter plots show relationships.

Athena examples:

```text
Asset return vs benchmark return
Risk vs return
Volatility vs return
Beta analysis
```

Scatter plots are useful for analysis pages, less for main dashboards.

### Example question

```text
Do higher-volatility assets have higher returns in this sample?
```

Scatter plot can help explore.

---

## 67. Risk dashboard charts

Risk dashboard charts may include:

```text
VaR trend
CVaR trend
RiskDNA timeline
Stress loss bars
Risk contribution bars
Rolling volatility line
Limit usage gauge
```

### Dashboard layout

Top:

```text
Metric cards
```

Middle:

```text
Charts
```

Bottom:

```text
Tables and explanations
```

### Athena rule

Put the most important risk status near the top.

---

## 68. P&L charts

P&L charts may include:

```text
Daily P&L bar chart
Cumulative P&L line chart
Top contributors bar chart
Worst contributors bar chart
Explained vs unexplained P&L card
```

Example questions:

```text
Did the portfolio gain or lose today?
Which position drove the loss?
Is unexplained P&L high?
```

### Athena use

P&L charts support reporting and middle office control.

---

## 69. Yield curve charts

Yield curve charts show rates by maturity.

Data:

```ts
const curve = [
  { maturity: "1Y", rate: 3.5 },
  { maturity: "2Y", rate: 3.7 },
  { maturity: "5Y", rate: 4.0 },
  { maturity: "10Y", rate: 4.2 },
];
```

Chart:

```text
X-axis = maturity
Y-axis = yield
```

### Athena use

Yield curve charts support:

```text
Fixed Income Lab
Rates dashboard
Bond pricing
Rate shock visualization
```

---

## 70. Option payoff charts

Option payoff charts show profit or payoff at expiration.

X-axis:

```text
Underlying price at expiration
```

Y-axis:

```text
Payoff or profit
```

Charts:

```text
Long call payoff
Long put payoff
Short call payoff
Short put payoff
```

### Athena use

Options Pricing Lab should include:

```text
PayoffChart
ProfitLossChart
SensitivityChart
```

This makes options easier to understand visually.

---

## 71. Internationalization overview

Internationalization means making the app support multiple languages.

Athena should support:

```text
English
French
```

Because the project is bilingual.

Internationalization is often shortened as:

```text
i18n
```

### Athena use

The app should allow users to switch language.

Example:

```text
Risk Dashboard
Tableau de risque
```

### Rule

Do not hardcode all UI text directly in components if the app is bilingual.

---

## 72. react-i18next overview

`react-i18next` is a React internationalization library.

Install:

```bash
npm install i18next react-i18next
```

Basic usage:

```tsx
import { useTranslation } from "react-i18next";

function DashboardTitle() {
  const { t } = useTranslation();

  return <h1>{t("dashboard.title")}</h1>;
}
```

Translation file:

```json
{
  "dashboard": {
    "title": "Risk Dashboard"
  }
}
```

### Athena use

Use translation files for English and French UI labels.

---

## 73. English and French structure

Recommended structure:

```text
frontend/src/i18n/
├── en.json
└── fr.json
```

Example `en.json`:

```json
{
  "navigation": {
    "dashboard": "Dashboard",
    "portfolio": "Portfolio",
    "risk": "Risk Monitor"
  }
}
```

Example `fr.json`:

```json
{
  "navigation": {
    "dashboard": "Tableau de bord",
    "portfolio": "Portefeuille",
    "risk": "Suivi du risque"
  }
}
```

### Athena rule

Keep translation keys stable.

---

## 74. Translation keys

Use clear translation keys.

Good:

```text
risk.var.title
risk.cvar.title
portfolio.totalValue
tradeSimulator.submit
```

Bad:

```text
text1
label2
button3
```

Example:

```json
{
  "risk": {
    "var": {
      "title": "Value at Risk",
      "description": "Estimated loss threshold."
    }
  }
}
```

### Athena use

Translation keys should follow feature names.

---

## 75. Formatting numbers

Financial numbers must be formatted clearly.

Example:

```ts
export function formatNumber(value: number): string {
  return new Intl.NumberFormat("en-CA", {
    maximumFractionDigits: 2,
  }).format(value);
}
```

### Percent formatting

```ts
export function formatPercent(value: number): string {
  return new Intl.NumberFormat("en-CA", {
    style: "percent",
    maximumFractionDigits: 2,
  }).format(value);
}
```

### Athena rule

Do not display raw numbers like:

```text
0.123456789
```

Display:

```text
12.35%
```

---

## 76. Formatting currencies

Currency formatting:

```ts
export function formatCurrency(value: number, currency = "CAD"): string {
  return new Intl.NumberFormat("en-CA", {
    style: "currency",
    currency,
    maximumFractionDigits: 2,
  }).format(value);
}
```

Example:

```ts
formatCurrency(12500, "CAD")
```

Output:

```text
$12,500.00
```

### Athena use

Use for:

```text
Portfolio value
P&L
VaR amount
Trade notional
Report values
```

### Rule

Always show currency when values are monetary.

---

## 77. Formatting dates

Date formatting:

```ts
export function formatDate(value: string): string {
  return new Intl.DateTimeFormat("en-CA").format(new Date(value));
}
```

### Athena use

Dates appear in:

```text
Market data
Trades
Reports
Risk metrics
P&L records
Workflow events
```

### Rule

Be consistent.

Avoid mixing:

```text
04/05/2026
2026-04-05
April 5, 2026
```

Use clear formats depending on context.

---

## 78. Frontend data types

Frontend types define data structures.

Example:

```ts
export type Portfolio = {
  id: string;
  name: string;
  baseCurrency: string;
  totalValue: number;
};

export type RiskMetric = {
  portfolioId: string;
  varAmount: number;
  cvarAmount: number;
  confidenceLevel: number;
  currency: string;
};
```

### Athena type files

Recommended:

```text
frontend/src/types/
├── portfolio.ts
├── trade.ts
├── risk.ts
├── option.ts
├── riskdna.ts
├── pnl.ts
└── report.ts
```

### Rule

Keep frontend types aligned with backend schemas.

---

## 79. Shared API types

In an ideal setup, frontend types match backend response schemas.

Options:

```text
Manually define frontend types
Generate types from OpenAPI later
Use shared schema definitions later
```

### Early Athena approach

Manually define types.

### Later professional approach

Generate TypeScript API client from FastAPI OpenAPI schema.

Tools can generate types from:

```text
openapi.json
```

### Rule

When backend response changes, update frontend types.

---

## 80. Frontend folder structure

Recommended structure:

```text
frontend/src/
├── app/
│   ├── router.tsx
│   └── providers.tsx
├── components/
│   ├── layout/
│   ├── ui/
│   ├── charts/
│   ├── tables/
│   └── forms/
├── features/
│   ├── dashboard/
│   ├── portfolio/
│   ├── market-data/
│   ├── trade-simulator/
│   ├── risk-monitor/
│   ├── options-pricing/
│   ├── riskdna/
│   ├── pnl/
│   └── reports/
├── i18n/
│   ├── en.json
│   └── fr.json
├── lib/
│   ├── api-client.ts
│   ├── formatters.ts
│   └── validators.ts
└── types/
```

### Why this works

It separates:

```text
App setup
Reusable components
Feature modules
Translations
Utilities
Types
```

---

## 81. Feature modules

Each feature can have its own structure.

Example:

```text
features/risk-monitor/
├── api/
│   └── risk-api.ts
├── components/
│   ├── RiskSummaryCards.tsx
│   ├── VaRTrendChart.tsx
│   └── RiskDriverTable.tsx
├── hooks/
│   └── use-risk-metrics.ts
├── pages/
│   └── RiskMonitorPage.tsx
└── types.ts
```

### Benefits

```text
Easy to find code
Feature ownership
Less global clutter
Scales well
```

### Athena rule

Build feature by feature.

---

## 82. Dashboard feature

Dashboard feature shows high-level overview.

Possible components:

```text
DashboardPage
PortfolioValueCard
DailyPnLCard
RiskDNACard
VaRCard
CVaRCard
TopRiskDrivers
RecentReports
```

Main questions:

```text
What is the portfolio value?
What is today's P&L?
What is the current risk level?
Are there warnings?
What changed recently?
```

### Athena dashboard goal

The dashboard should give a fast executive summary.

---

## 83. Portfolio feature

Portfolio feature manages holdings.

Components:

```text
PortfolioList
PortfolioDetails
PositionTable
AllocationChart
PortfolioForm
PortfolioSummaryCards
```

Main questions:

```text
What does the portfolio hold?
What are the weights?
What are the exposures?
What is the benchmark?
```

API hooks:

```text
usePortfolios
usePortfolio
usePortfolioPositions
useCreatePortfolio
```

---

## 84. Market data feature

Market data feature shows prices and returns.

Components:

```text
MarketDataPage
PriceChart
ReturnsChart
RollingVolatilityChart
MarketDataTable
DataQualityPanel
```

Main questions:

```text
What did prices do?
Are returns calculated?
Is volatility rising?
Is market data clean?
```

### Athena use

This feature supports the finance and risk modules.

---

## 85. Trade simulator feature

Trade simulator feature connects front office decisions to risk controls.

Components:

```text
TradeTicketForm
TradeSimulationResult
BeforeAfterPortfolioImpact
PreTradeCheckPanel
LimitCheckCard
TradeImpactExplanation
```

Main workflow:

```text
Enter trade
Simulate
View before/after exposure
View risk impact
Check limits
Review explanation
```

### Athena rule

Simulation should be clearly separate from execution.

---

## 86. Risk monitor feature

Risk monitor feature displays risk metrics.

Components:

```text
RiskMonitorPage
RiskSummaryCards
VaRTrendChart
CVaRCard
StressLossChart
RiskContributionChart
LimitStatusPanel
RiskDriverTable
```

Main questions:

```text
How risky is the portfolio?
What are the main risks?
Are limits breached?
What is the downside exposure?
```

### Athena use

This is one of the core product features.

---

## 87. Options pricing feature

Options pricing feature supports Black-Scholes and Greeks.

Components:

```text
OptionPricingPage
OptionPricingForm
CallPriceCard
PutPriceCard
GreeksTable
PayoffChart
ProfitLossChart
PutCallParityCheck
SensitivityChart
```

Main questions:

```text
What is the theoretical option price?
What are the Greeks?
How does payoff behave?
How sensitive is the option?
```

### Athena use

This feature connects derivatives theory to practical visualization.

---

## 88. RiskDNA feature

RiskDNA feature summarizes and explains risk.

Components:

```text
RiskDNAPage
RiskDNACard
RiskDNAScoreGauge
RiskLevelBadge
RiskDriverTable
RiskDNAExplanationPanel
RiskDNATimeline
BeforeAfterRiskDNAPanel
```

Main questions:

```text
What is the overall risk level?
Why is the score high or low?
What are the top drivers?
Did risk increase after a trade?
```

### Athena rule

RiskDNA should be explainable, not a black box.

---

## 89. P&L and reports feature

P&L and reports feature explains what happened and communicates it.

Components:

```text
PnLDashboardPage
PnLSummaryCard
DailyPnLChart
CumulativePnLChart
PositionPnLTable
TopContributorsTable
WorstContributorsTable
ReportBuilder
ReportPreview
ReportStatusBadge
```

Main questions:

```text
Did the portfolio gain or lose money?
Why?
Which positions contributed?
Is there unexplained P&L?
Is the report validated?
```

### Athena use

This is the final reporting layer of the platform.

---

## 90. Accessibility basics

Accessibility means the app can be used by more people.

Basic rules:

```text
Use semantic HTML
Label form fields
Ensure keyboard navigation
Use sufficient contrast
Do not rely only on color
Add aria labels when needed
```

Example:

```tsx
<label htmlFor="spot-price">Spot price</label>
<input id="spot-price" type="number" />
```

### Athena importance

Risk warnings should not rely only on color.

Use text labels like:

```text
Warning
Breach
Critical
```

---

## 91. Performance basics

Frontend performance matters.

Basic practices:

```text
Avoid unnecessary re-renders
Paginate large tables
Do not render thousands of rows at once
Use TanStack Query caching
Lazy load heavy pages if needed
Memoize expensive derived data when useful
```

### Athena examples

Large data:

```text
Market data table
Trade history
Audit trail
Workflow events
```

Use pagination or virtualization later.

### Rule

Do not load all historical market data into the UI if not needed.

---

## 92. Frontend testing

Frontend testing checks UI behavior.

Tools:

```text
Vitest
React Testing Library
Playwright or Cypress
Mock Service Worker optional
```

Types of tests:

```text
Unit tests
Component tests
Integration tests
End-to-end tests
```

### Athena testing targets

```text
Forms validate inputs
Risk cards render values
Tables render rows
Charts receive correct data
API errors show error states
Language switch works
```

---

## 93. Unit tests

Unit tests test small functions.

Examples:

```text
formatCurrency
formatPercent
formatDate
risk level mapping
status label helper
```

Example:

```ts
import { describe, expect, it } from "vitest";
import { formatPercent } from "@/lib/formatters";

describe("formatPercent", () => {
  it("formats decimal as percent", () => {
    expect(formatPercent(0.1234)).toBe("12.34%");
  });
});
```

### Athena use

Test utilities and pure functions first.

---

## 94. Component tests

Component tests check UI components.

Example:

```tsx
import { render, screen } from "@testing-library/react";
import { MetricCard } from "./MetricCard";

it("renders metric title and value", () => {
  render(<MetricCard title="VaR" value="12,500 CAD" />);

  expect(screen.getByText("VaR")).toBeInTheDocument();
  expect(screen.getByText("12,500 CAD")).toBeInTheDocument();
});
```

### Athena component tests

```text
RiskLevelBadge displays correct label
MetricCard displays title and value
GreeksTable displays Greeks
ErrorState displays message
```

---

## 95. API mocking

API mocking lets frontend tests run without real backend.

Tools:

```text
Mock Service Worker
Vitest mocks
Manual mock functions
```

Example use:

```text
Mock /api/portfolios response
Render PortfolioPage
Check portfolios appear
```

### Athena use

Mocking is useful because frontend tests should not require live backend.

### Rule

Use realistic mock data.

---

## 96. End-to-end tests

End-to-end tests simulate user workflows.

Tools:

```text
Playwright
Cypress
```

Example workflows:

```text
Create portfolio
Add position
Run risk calculation
Simulate trade
Price option
Generate report
Switch language
```

### Athena recommendation

Add E2E tests after core UI and backend are stable.

Do not start with too many E2E tests too early.

---

## 97. Code quality tools

Recommended frontend tools:

```text
ESLint
Prettier
TypeScript
Vitest
React Testing Library
Playwright later
```

Scripts:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint .",
    "test": "vitest"
  }
}
```

### Athena rule

Run build and lint before pushing important changes.

---

## 98. Common beginner mistakes

### Mistake 1 — Putting all UI in one component

Break pages into smaller components.

### Mistake 2 — Calculating official finance logic in frontend

Backend should own calculations.

### Mistake 3 — No loading states

Users need feedback.

### Mistake 4 — No error states

APIs can fail.

### Mistake 5 — No empty states

Blank pages confuse users.

### Mistake 6 — Inconsistent formatting

Use shared formatters for currency, percent and dates.

### Mistake 7 — Hardcoding text despite bilingual goal

Use i18n keys.

### Mistake 8 — Poor chart labels

Charts need titles and units.

### Mistake 9 — No TypeScript types

Finance data needs clear types.

### Mistake 10 — Building everything at once

Build feature by feature.

---

## 99. Athena frontend development workflow

Recommended workflow:

```text
1. Define the feature.
2. Define backend endpoint and response type.
3. Create TypeScript types.
4. Create API function.
5. Create TanStack Query hook.
6. Build UI components.
7. Add loading, error and empty states.
8. Add formatting.
9. Add translations.
10. Add tests.
```

Example for Options Pricing:

```text
1. Define OptionPricingRequest and OptionPricingResponse.
2. Backend exposes POST /api/options/black-scholes/price.
3. Frontend creates option types.
4. Frontend creates priceOption API function.
5. Frontend creates usePriceOption mutation.
6. Build OptionPricingForm and GreeksTable.
7. Add validation with Zod.
8. Display result cards and charts.
9. Add English/French labels.
10. Add component tests.
```

---

## 100. Summary

The frontend is the user-facing layer of Athena AI Risk Terminal.

Recommended stack:

```text
React
TypeScript
Vite
Tailwind CSS
shadcn/ui
TanStack Query
React Hook Form
Zod
Recharts
react-i18next
Vitest
React Testing Library
Playwright or Cypress later
```

Main frontend responsibilities:

```text
Display dashboards
Collect user inputs
Call backend APIs
Show charts and tables
Handle loading/error/empty states
Support bilingual UI
Create professional user experience
```

Most important principle:

```text
The frontend should make complex financial analytics understandable, but the backend should own official calculations.
```

Athena frontend should be:

```text
Clear
Professional
Bilingual
Modular
Typed
Dashboard-oriented
Risk-aware
User-friendly
```

The key lesson:

```text
A strong frontend turns Athena's quantitative engine into a product people can actually understand and use.
```
