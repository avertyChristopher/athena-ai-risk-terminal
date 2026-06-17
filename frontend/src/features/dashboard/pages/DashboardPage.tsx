import { Link } from "react-router-dom";
import type { ReactNode } from "react";

import { MoneyValue } from "../../../components/finance/MoneyValue";
import { PercentValue } from "../../../components/finance/PercentValue";
import { usePortfolioContext } from "../../../context/PortfolioContext";
import { useHealth } from "../../../hooks/useHealth";
import { useTranslation } from "../../../hooks/useTranslation";

type Kpi = {
  label: string;
  value: string;
  detail: string;
  tone: "neutral" | "positive" | "warning";
};

type Module = {
  name: string;
  description: string;
  status: "Live" | "Demo" | "Beta" | "Coming Soon";
  path: string;
};

type WorkflowModule = {
  name: string;
  description: string;
  path: string;
  meta: string;
};

const kpis: Kpi[] = [
  {
    label: "Portfolio Value",
    value: "$125,430",
    detail: "Demo multi-asset portfolio",
    tone: "neutral",
  },
  {
    label: "Daily Return",
    value: "+0.84%",
    detail: "Positive session drift",
    tone: "positive",
  },
  {
    label: "Volatility",
    value: "18.6%",
    detail: "Annualized estimate",
    tone: "warning",
  },
  {
    label: "Risk Score",
    value: "Moderate",
    detail: "Concentration monitored",
    tone: "warning",
  },
  {
    label: "Data Quality",
    value: "96%",
    detail: "Clean demo data feeds",
    tone: "positive",
  },
  {
    label: "Active Modules",
    value: "5/12",
    detail: "Connected workflow online",
    tone: "neutral",
  },
];

const modules: Module[] = [
  {
    name: "Market Data",
    description: "Clean prices, returns, volatility, benchmarks and data quality metrics.",
    status: "Live",
    path: "/market-data",
  },
  {
    name: "Equity Analysis",
    description: "Analyze valuation, profitability, growth, risk and CFA-style diagnostics.",
    status: "Live",
    path: "/equity-analysis",
  },
  {
    name: "Portfolio Builder",
    description: "Build portfolios, monitor allocation, drift, concentration and policy fit.",
    status: "Live",
    path: "/portfolio-builder",
  },
  {
    name: "Trade Simulator",
    description: "Simulate portfolio-aware buy and sell orders before execution.",
    status: "Live",
    path: "/trade-simulator",
  },
  {
    name: "Risk Monitor",
    description: "Track VaR, CVaR, drawdown, configurable limits and stress shocks.",
    status: "Beta",
    path: "/risk-monitor",
  },
  {
    name: "Volatility Lab",
    description: "Inspect realized volatility, rolling volatility and distribution behavior.",
    status: "Coming Soon",
    path: "/volatility-lab",
  },
  {
    name: "Options Pricing Lab",
    description: "Price options, inspect Greeks and evaluate payoff sensitivity.",
    status: "Coming Soon",
    path: "/options-pricing-lab",
  },
  {
    name: "Rates Lab",
    description: "Analyze yield curves, bond pricing, duration and rate shocks.",
    status: "Coming Soon",
    path: "/rates-lab",
  },
  {
    name: "Stress Testing",
    description: "Design scenario libraries and compare portfolio shock impacts.",
    status: "Coming Soon",
    path: "/stress-testing",
  },
  {
    name: "Limit Center",
    description: "Centralize risk limits, threshold monitoring and breach review.",
    status: "Coming Soon",
    path: "/limit-center",
  },
  {
    name: "P&L Attribution",
    description: "Explain daily P&L by position, factor, market move and trade activity.",
    status: "Coming Soon",
    path: "/pnl-attribution",
  },
  {
    name: "Reports Center",
    description: "Generate portfolio, risk and analytics reports for review workflows.",
    status: "Coming Soon",
    path: "/reports-center",
  },
];

const riskRows = [
  ["Portfolio Risk Level", "Moderate"],
  ["VaR 95%", "-2.35%"],
  ["CVaR 95%", "-3.80%"],
  ["Max Drawdown", "-12.4%"],
  ["Concentration Risk", "Technology exposure high"],
  ["Sector Exposure", "Tech 64% / Fixed Income 14%"],
];

const marketRows = [
  ["AAPL", 198.34, 0.84],
  ["MSFT", 512.6, 0.52],
  ["NVDA", 138.52, -1.12],
  ["SPY", 619.4, 0.31],
  ["QQQ", 543.18, 0.46],
  ["BND", 72.44, -0.08],
] as const;

const activityRows = [
  ["09:42", "Market data refreshed"],
  ["09:40", "Portfolio summary updated"],
  ["09:38", "Data quality check completed"],
  ["09:35", "Equity analysis module available"],
];

export function DashboardPage() {
  const { t } = useTranslation();
  const {
    holdings,
    selectedHolding,
    selectedPortfolioName,
    selectedSymbol,
  } = usePortfolioContext();
  const healthQuery = useHealth();
  const isConnected = !healthQuery.isError;
  const statusLabel = healthQuery.isLoading
    ? t("common.loading")
    : isConnected
      ? "API Connected"
      : "Demo Data Online";
  const workflowPortfolioName =
    selectedPortfolioName || "Athena Demo Portfolio";
  const workflowSymbol = selectedSymbol || selectedHolding?.symbol || "--";
  const workflowModules: WorkflowModule[] = [
    {
      name: "Market Data",
      description: "Inspect prices, returns, volatility and data quality for the selected symbol.",
      path: "/market-data",
      meta: workflowSymbol,
    },
    {
      name: "Equity Analysis",
      description: "Run stock-level valuation, fundamentals, quality and peer diagnostics.",
      path: "/equity-analysis",
      meta: workflowSymbol,
    },
    {
      name: "Portfolio Builder",
      description: "Review holdings, allocation, concentration, policy and portfolio risk.",
      path: "/portfolio-builder",
      meta: `${holdings.length} holdings`,
    },
    {
      name: "Trade Simulator",
      description: "Simulate BUY or SELL tickets against the selected portfolio context.",
      path: "/trade-simulator",
      meta: workflowPortfolioName,
    },
  ];

  return (
    <div className="page dashboard-page">
      <section className="dashboard-hero">
        <div className="dashboard-hero__content">
          <div className="dashboard-hero__badges">
            <span className="dashboard-badge">Demo Environment</span>
            <span className={isConnected ? "dashboard-status" : "dashboard-status dashboard-status--warning"}>
              {statusLabel}
            </span>
          </div>
          <h1>Athena AI Risk Terminal</h1>
          <p className="dashboard-hero__subtitle">
            Quantitative Finance, Portfolio Analytics & Risk Intelligence
          </p>
          <p className="dashboard-hero__body">
            Athena brings together market data, single-stock analysis, portfolio
            construction and risk monitoring in one clean research terminal for
            finance and risk management workflows.
          </p>
        </div>
        <div className="dashboard-hero__panel" aria-label="System summary">
          <span>System snapshot</span>
          <strong>{healthQuery.data?.service ?? "Athena API"}</strong>
          <p>{healthQuery.data?.status ?? "Demo data layer ready"}</p>
        </div>
      </section>

      <section className="dashboard-kpi-grid" aria-label="Dashboard KPIs">
        {kpis.map((kpi) => (
          <KpiCard key={kpi.label} kpi={kpi} />
        ))}
      </section>

      <DashboardSection
        title={t("workflow.connectedWorkflow")}
        description="One selected portfolio and symbol can now move through market data, equity analysis, portfolio review and pre-trade simulation."
      >
        <div className="dashboard-workflow-summary">
          <div>
            <span>{t("workflow.selectedPortfolio")}</span>
            <strong>{workflowPortfolioName}</strong>
          </div>
          <div>
            <span>{t("workflow.symbol")}</span>
            <strong>{workflowSymbol}</strong>
          </div>
          <div>
            <span>{t("workflow.positions")}</span>
            <strong>{holdings.length}</strong>
          </div>
        </div>
        <div className="dashboard-workflow-grid">
          {workflowModules.map((module, index) => (
            <WorkflowCard
              key={module.name}
              module={module}
              step={index + 1}
              actionLabel={t("workflow.continueWorkflow")}
            />
          ))}
        </div>
      </DashboardSection>

      <DashboardSection
        title="Platform Overview"
        description="Five connected workstations are active today, with the remaining analytics modules staged for future increments."
      >
        <div className="dashboard-module-grid">
          {modules.map((module) => (
            <ModuleCard key={module.name} module={module} />
          ))}
        </div>
      </DashboardSection>

      <div className="dashboard-split-grid">
        <DashboardSection
          title="Risk Snapshot"
          description="Portfolio-level risk indicators using deterministic demo analytics."
        >
          <div className="dashboard-risk-grid">
            {riskRows.map(([label, value]) => (
              <div className="dashboard-risk-row" key={label}>
                <span>{label}</span>
                <strong>{value}</strong>
              </div>
            ))}
          </div>
        </DashboardSection>

        <DashboardSection
          title="Market Snapshot"
          description="Demo latest prices and daily moves for the tracked universe."
        >
          <div className="dashboard-market-table">
            {marketRows.map(([ticker, price, change]) => (
              <div className="dashboard-market-row" key={ticker}>
                <strong>{ticker}</strong>
                <MoneyValue value={price} />
                <span className={change >= 0 ? "positive-value" : "negative-value"}>
                  <PercentValue value={change / 100} />
                </span>
              </div>
            ))}
          </div>
        </DashboardSection>
      </div>

      <div className="dashboard-split-grid dashboard-split-grid--wide">
        <section className="card dashboard-ai-card">
          <span className="equity-kicker">Athena Intelligence</span>
          <h2>AI Insights</h2>
          <p>
            The demo portfolio shows strong exposure to large-cap technology
            stocks. Volatility remains moderate, but concentration risk is
            elevated due to NVDA, AAPL and MSFT weights. A broader allocation
            across fixed income or defensive sectors could reduce downside risk.
          </p>
        </section>

        <section className="card dashboard-activity-card">
          <div className="section-heading">
            <h2>Recent Activity</h2>
            <span className="status-pill">Live log</span>
          </div>
          <div className="dashboard-activity-list">
            {activityRows.map(([time, label]) => (
              <div className="dashboard-activity-row" key={`${time}-${label}`}>
                <span>{time}</span>
                <strong>{label}</strong>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}

function DashboardSection({
  title,
  description,
  children,
}: {
  title: string;
  description: string;
  children: ReactNode;
}) {
  return (
    <section className="analytics-section dashboard-section">
      <header className="analytics-section__header">
        <h2>{title}</h2>
        <p>{description}</p>
      </header>
      {children}
    </section>
  );
}

function KpiCard({ kpi }: { kpi: Kpi }) {
  return (
    <section className={`card dashboard-kpi-card dashboard-kpi-card--${kpi.tone}`}>
      <span>{kpi.label}</span>
      <strong>{kpi.value}</strong>
      <p>{kpi.detail}</p>
    </section>
  );
}

function ModuleCard({ module }: { module: Module }) {
  return (
    <Link className="dashboard-module-card" to={module.path}>
      <div>
        <span className={`dashboard-module-status dashboard-module-status--${module.status.toLowerCase().replace(" ", "-")}`}>
          {module.status}
        </span>
        <h3>{module.name}</h3>
        <p>{module.description}</p>
      </div>
      <strong>Open module</strong>
    </Link>
  );
}

function WorkflowCard({
  module,
  step,
  actionLabel,
}: {
  module: WorkflowModule;
  step: number;
  actionLabel: string;
}) {
  return (
    <Link className="dashboard-workflow-card" to={module.path}>
      <div>
        <span className="dashboard-workflow-step">0{step}</span>
        <h3>{module.name}</h3>
        <p>{module.description}</p>
      </div>
      <div className="dashboard-workflow-card__footer">
        <span>{module.meta}</span>
        <strong>{actionLabel}</strong>
      </div>
    </Link>
  );
}
