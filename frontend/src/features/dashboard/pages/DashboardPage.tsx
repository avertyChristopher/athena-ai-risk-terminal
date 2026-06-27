import { Link } from "react-router-dom";
import type { ReactNode } from "react";
import { useQuery } from "@tanstack/react-query";

import { MoneyValue } from "../../../components/finance/MoneyValue";
import { PercentValue } from "../../../components/finance/PercentValue";
import { StatusBadge, type StatusBadgeVariant } from "../../../components/ui/StatusBadge";
import { usePortfolioContext } from "../../../context/PortfolioContext";
import { useHealth } from "../../../hooks/useHealth";
import { useTranslation } from "../../../hooks/useTranslation";
import { athenaIntelligenceApi } from "../../../services/athenaIntelligenceApi";

type Kpi = {
  label: string;
  value: string;
  detail: string;
  tone: "neutral" | "positive" | "warning";
};

type Module = {
  name: string;
  description: string;
  status: "Solid" | "Functional" | "Beta" | "Beta+" | "Coming Soon";
  maturity: string;
  path: string;
  connectedInputs: string[];
  connectedOutputs: string[];
  features: string[];
  badges: string[];
};

type WorkflowModule = {
  name: string;
  description: string;
  path: string;
  meta: string;
};

type DemoPortfolio = {
  name: string;
  strategyType: string;
  riskProfile: string;
  riskVariant: StatusBadgeVariant;
  targetAllocation: string;
  holdings: string;
  baseCurrency: string;
  benchmark: string;
  description: string;
  bestShowcase: string[];
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
    value: "10/12",
    detail: "Core analytics and governance online",
    tone: "neutral",
  },
];

const modules: Module[] = [
  {
    name: "Market Data",
    description: "Clean prices, returns, volatility, benchmarks and data quality metrics.",
    status: "Solid",
    maturity: "Connected",
    path: "/market-data",
    connectedInputs: ["CSV imports", "Demo market feed"],
    connectedOutputs: ["Equity", "Portfolio", "Volatility", "Rates", "Stress Testing"],
    features: ["Price history", "Returns", "Data quality"],
    badges: ["Market Data", "Demo", "Connected"],
  },
  {
    name: "Equity Analysis",
    description: "Analyze valuation, profitability, growth, risk and CFA-style diagnostics.",
    status: "Solid",
    maturity: "Connected",
    path: "/equity-analysis",
    connectedInputs: ["Market Data", "Selected symbol"],
    connectedOutputs: ["Portfolio Builder"],
    features: ["Fundamentals", "Ratios", "Valuation"],
    badges: ["CFA Level 1", "Market Data"],
  },
  {
    name: "Portfolio Builder",
    description: "Build portfolios, monitor allocation, drift, concentration and policy fit.",
    status: "Solid",
    maturity: "Connected",
    path: "/portfolio-builder",
    connectedInputs: ["Market Data", "Equity Analysis"],
    connectedOutputs: ["Trade Simulator", "Risk Monitor", "Rates Lab", "Stress Testing"],
    features: ["Allocation", "Constraints", "Performance"],
    badges: ["Portfolio Ready", "In-Memory Store"],
  },
  {
    name: "Trade Simulator",
    description: "Simulate portfolio-aware buy and sell orders before execution.",
    status: "Functional",
    maturity: "Connected",
    path: "/trade-simulator",
    connectedInputs: ["Portfolio Builder", "Market Data"],
    connectedOutputs: ["Portfolio impact preview"],
    features: ["Order simulation", "Before/after impact", "Suitability"],
    badges: ["Portfolio Ready", "No Execution"],
  },
  {
    name: "Risk Monitor",
    description: "Track VaR, CVaR, drawdown, configurable limits and stress shocks.",
    status: "Beta",
    maturity: "Beta",
    path: "/risk-monitor",
    connectedInputs: ["Portfolio", "Volatility", "Options", "Rates"],
    connectedOutputs: ["Limit Center", "Stress Testing"],
    features: ["VaR/CVaR", "Drawdown", "Risk limits"],
    badges: ["Beta", "Portfolio Ready"],
  },
  {
    name: "Volatility Lab",
    description: "Institutional volatility workstation with realized, EWMA, VaR/CVaR, beta, correlation and Risk Monitor-ready outputs.",
    status: "Beta+",
    maturity: "Payload Ready",
    path: "/volatility-lab",
    features: [
      "Realized volatility",
      "EWMA volatility",
      "VaR/CVaR",
      "Beta & correlation",
      "Risk Monitor-ready",
    ],
    badges: ["CFA Level 1", "Market Data Connected", "Risk Monitor Ready"],
    connectedInputs: ["Market Data", "Portfolio Builder"],
    connectedOutputs: ["Options Pricing", "Risk Monitor", "Stress Testing", "Limit Center"],
  },
  {
    name: "Options Pricing Lab",
    description: "Financially corrected beta for option pricing, observed parity, implied volatility and typed multi-leg strategies.",
    status: "Beta+",
    maturity: "Beta+",
    path: "/options-pricing-lab",
    features: [
      "Black-Scholes",
      "Binomial CRR",
      "Greeks",
      "Put-call parity",
      "Strategy lab",
      "Implied volatility",
    ],
    badges: [
      "CFA Level 1",
      "Greeks",
      "Strategy Lab",
      "Implied Volatility",
      "Beta+",
      "Bilingual",
    ],
    connectedInputs: ["Market Data", "Volatility Lab"],
    connectedOutputs: ["Risk Monitor-ready Greeks", "Stress Testing", "Limit Center"],
  },
  {
    name: "Rates Lab",
    description: "Analyze bond pricing, yield, duration, convexity, DV01 and curve scenarios.",
    status: "Beta+",
    maturity: "Payload Ready",
    path: "/rates-lab",
    features: [
      "Bond pricing",
      "Yield analysis",
      "Duration & convexity",
      "Yield curve",
      "Rate scenarios",
    ],
    badges: ["CFA Level 1", "Fixed Income", "Duration", "Yield Curve", "Risk Monitor Ready"],
    connectedInputs: ["Manual bond inputs", "Portfolio Builder", "Demo curve"],
    connectedOutputs: ["Risk Monitor", "Stress Testing", "Limit Center"],
  },
  {
    name: "Stress Testing",
    description: "Run portfolio stress scenarios across equities, rates, volatility, FX and credit shocks.",
    status: "Beta",
    maturity: "Beta",
    path: "/stress-testing",
    connectedInputs: ["Portfolio Builder", "Market Data", "Volatility Lab", "Rates Lab", "Options Pricing Lab"],
    connectedOutputs: ["Risk Monitor payload", "Limit Center"],
    features: ["Scenario library", "Portfolio shocks", "Worst contributors", "Risk payload"],
    badges: ["Risk Management", "Scenario Analysis", "Portfolio Connected", "Risk Monitor Ready", "Beta"],
  },
  {
    name: "Limit Center",
    description: "Centralize portfolio, market, stress, rates, options and trade limits with breach review.",
    status: "Beta",
    maturity: "Governance Beta",
    path: "/limit-center",
    connectedInputs: ["Portfolio Builder", "Risk Monitor", "Stress Testing", "Volatility Lab", "Options Pricing Lab", "Rates Lab", "Trade Simulator"],
    connectedOutputs: ["Risk governance workflow", "Reports Center future", "P&L Attribution future"],
    features: ["Limit rules", "Breach register", "Exception workflow", "Severity engine"],
    badges: ["Risk Governance", "Breach Register", "Exceptions", "Athena Intelligence", "Beta"],
  },
  {
    name: "P&L Attribution",
    description: "Explain daily P&L by position, factor, market move and trade activity.",
    status: "Coming Soon",
    maturity: "Roadmap",
    path: "/pnl-attribution",
    connectedInputs: [],
    connectedOutputs: [],
    features: ["Factor attribution", "Trade attribution"],
    badges: ["Coming Soon"],
  },
  {
    name: "Reports Center",
    description: "Generate portfolio, risk and analytics reports for review workflows.",
    status: "Coming Soon",
    maturity: "Roadmap",
    path: "/reports-center",
    connectedInputs: [],
    connectedOutputs: [],
    features: ["Portfolio reports", "Risk reports"],
    badges: ["Coming Soon"],
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
  ["09:45", "Limit Center governance workflow available"],
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
  const athenaStatusQuery = useQuery({
    queryKey: ["athena-intelligence-status"],
    queryFn: athenaIntelligenceApi.status,
  });
  const isConnected = !healthQuery.isError;
  const athenaStatus = athenaStatusQuery.data;
  const athenaProviderMode = athenaStatus?.provider_mode ?? "fallback";
  const statusLabel = healthQuery.isLoading
    ? t("common.loading")
    : isConnected
      ? "API Connected"
      : "Demo Data Online";
  const workflowPortfolioName =
    selectedPortfolioName || "Athena Balanced Growth Portfolio";
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
      name: "Volatility Lab",
      description: "Bridge Market Data and Portfolio Builder into VaR, EWMA, covariance and Risk Monitor-ready risk payloads.",
      path: "/volatility-lab",
      meta: selectedPortfolioName ? "Portfolio + asset" : workflowSymbol,
    },
    {
      name: "Options Pricing Lab",
      description: "Use Market Data prices and Volatility Lab inputs to price options, inspect Greeks and test payoff strategies.",
      path: "/options-pricing-lab",
      meta: workflowSymbol,
    },
    {
      name: "Rates Lab",
      description: "Transform bond inputs and demo curves into duration, DV01 and reusable rate-shock payloads.",
      path: "/rates-lab",
      meta: selectedPortfolioName ? "Portfolio + rates" : "Demo curve",
    },
    {
      name: "Stress Testing",
      description: "Run multi-asset portfolio shocks and convert stressed losses into Risk Monitor-ready payloads.",
      path: "/stress-testing",
      meta: selectedPortfolioName ? "Portfolio scenario" : "Scenario library",
    },
    {
      name: "Trade Simulator",
      description: "Simulate BUY or SELL tickets against the selected portfolio context.",
      path: "/trade-simulator",
      meta: workflowPortfolioName,
    },
    {
      name: "Risk Monitor",
      description: "Review limits, stress shocks, risk contribution and benchmark active risk.",
      path: "/risk-monitor",
      meta: "Risk controls",
    },
    {
      name: "Limit Center",
      description: "Evaluate centralized governance limits, inspect breaches and document exception decisions.",
      path: "/limit-center",
      meta: "Breach workflow",
    },
  ];
  const workflowTracks: Array<{
    title: string;
    modules: string[];
    destination?: string;
  }> = [
    {
      title: "Research to portfolio",
      modules: ["Market Data", "Equity Analysis", "Portfolio Builder", "Trade Simulator"],
    },
    {
      title: "Derivatives risk",
      modules: ["Market Data", "Volatility Lab", "Options Pricing Lab", "Stress Testing", "Risk Monitor", "Limit Center"],
    },
    {
      title: "Fixed-income risk",
      modules: ["Market Data", "Rates Lab", "Stress Testing", "Risk Monitor", "Limit Center"],
    },
    {
      title: "Institutional stress workflow",
      modules: ["Portfolio Builder", "Volatility Lab", "Rates Lab", "Stress Testing", "Risk Monitor", "Limit Center"],
    },
    {
      title: "Governance workflow",
      modules: ["Portfolio Builder", "Trade Simulator", "Risk Monitor", "Stress Testing", "Limit Center"],
      destination: "Limit review",
    },
  ];
  const demoPortfolioUniverse: DemoPortfolio[] = [
    {
      name: t("dashboard.demoUniverse.balanced.name"),
      strategyType: t("dashboard.demoUniverse.balanced.strategy"),
      riskProfile: t("dashboard.demoUniverse.balanced.risk"),
      riskVariant: "warning",
      targetAllocation: "60 / 30 / 5 / 5",
      holdings: "9",
      baseCurrency: "USD",
      benchmark: "SPY",
      description: t("dashboard.demoUniverse.balanced.description"),
      bestShowcase: ["Portfolio Builder", "Risk Monitor"],
    },
    {
      name: t("dashboard.demoUniverse.conservative.name"),
      strategyType: t("dashboard.demoUniverse.conservative.strategy"),
      riskProfile: t("dashboard.demoUniverse.conservative.risk"),
      riskVariant: "success",
      targetAllocation: "35 / 55 / 5 / 5",
      holdings: "7",
      baseCurrency: "USD",
      benchmark: "BND",
      description: t("dashboard.demoUniverse.conservative.description"),
      bestShowcase: ["Rates Lab", "Risk Monitor"],
    },
    {
      name: t("dashboard.demoUniverse.tech.name"),
      strategyType: t("dashboard.demoUniverse.tech.strategy"),
      riskProfile: t("dashboard.demoUniverse.tech.risk"),
      riskVariant: "danger",
      targetAllocation: "96 / 2 / 0 / 2",
      holdings: "6",
      baseCurrency: "USD",
      benchmark: "QQQ",
      description: t("dashboard.demoUniverse.tech.description"),
      bestShowcase: ["Limit Center", "Stress Testing"],
    },
    {
      name: t("dashboard.demoUniverse.multiAsset.name"),
      strategyType: t("dashboard.demoUniverse.multiAsset.strategy"),
      riskProfile: t("dashboard.demoUniverse.multiAsset.risk"),
      riskVariant: "info",
      targetAllocation: "60 / 30 / 5 / 5",
      holdings: "10",
      baseCurrency: "USD",
      benchmark: "SPY",
      description: t("dashboard.demoUniverse.multiAsset.description"),
      bestShowcase: [t("dashboard.demoUniverse.fullWorkflow")],
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
            construction, options and fixed-income analytics, risk monitoring and limit governance in one clean
            research terminal for finance and risk management workflows.
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
        description="Market Data and Portfolio Builder feed volatility, options, fixed-income and stress analytics into Risk Monitor and Limit Center governance workflows."
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
        <div className="dashboard-workflow-tracks">
          {workflowTracks.map((track) => (
            <div className="dashboard-workflow-track" key={track.title}>
              <div className="section-heading">
                <h3>{track.title}</h3>
                {track.destination ? <StatusBadge label={track.destination} variant="neutral" /> : null}
              </div>
              <div className="dashboard-workflow-grid">
                {track.modules.map((moduleName, index) => {
                  const module = workflowModules.find((item) => item.name === moduleName);
                  return module ? (
                    <WorkflowCard
                      key={`${track.title}-${module.name}`}
                      module={module}
                      step={index + 1}
                      actionLabel={t("workflow.continueWorkflow")}
                    />
                  ) : null;
                })}
              </div>
            </div>
          ))}
        </div>
      </DashboardSection>

      <DashboardSection
        title={t("dashboard.demoUniverse.title")}
        description={t("dashboard.demoUniverse.description")}
      >
        <div className="dashboard-demo-universe-grid">
          {demoPortfolioUniverse.map((portfolio) => (
            <DemoPortfolioCard
              key={portfolio.name}
              portfolio={portfolio}
              labels={{
                demoBadge: t("dashboard.demoUniverse.demoBadge"),
                strategyType: t("workflow.strategyType"),
                targetAllocation: t("portfolio.profile.targetAllocation"),
                holdings: t("workflow.positions"),
                baseCurrency: t("workflow.baseCurrency"),
                benchmark: t("workflow.benchmark"),
                bestShowcase: t("dashboard.demoUniverse.bestShowcase"),
                openPortfolioBuilder: t("dashboard.demoUniverse.openPortfolioBuilder"),
              }}
            />
          ))}
        </div>
      </DashboardSection>

      <DashboardSection
        title="Platform Overview"
        description="Ten connected workstations are active today, with P&L Attribution and Reports Center staged for future increments."
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
          <div className="section-heading">
            <h2>Athena Intelligence Engine</h2>
            <StatusBadge
              label={
                athenaStatusQuery.isLoading
                  ? t("common.loading")
                  : athenaProviderMode === "openai"
                    ? t("athenaIntelligence.openaiMode")
                    : t("athenaIntelligence.fallbackMode")
              }
              variant={athenaProviderMode === "openai" ? "success" : "warning"}
            />
          </div>
          <p>
            Central synthesis layer for Risk Monitor, Volatility Lab, Options Pricing Lab,
            Rates Lab, Trade Simulator and Limit Center. It generates structured commentary from module
            payloads only, with deterministic fallback and no investment-advice wording.
          </p>
          <div className="dashboard-intelligence-list">
            <span>{t("athenaIntelligence.structuredPayloads")}</span>
            <span>{t("athenaIntelligence.noSecrets")}</span>
            <span>{t("athenaIntelligence.riskSynthesis")}</span>
          </div>
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
  const statusVariant = module.status === "Solid" || module.status === "Functional"
    ? "success"
    : module.status === "Beta" || module.status === "Beta+"
      ? "warning"
      : "neutral";
  return (
    <Link className="dashboard-module-card" to={module.path}>
      <div>
        <div className="dashboard-module-badges">
          <StatusBadge label={module.status} variant={statusVariant} />
          <StatusBadge label={module.maturity} variant="info" />
        </div>
        <h3>{module.name}</h3>
        <p>{module.description}</p>
        <div className="dashboard-module-connections">
          <span>Inputs</span>
          <p>{module.connectedInputs.length ? module.connectedInputs.join(" / ") : "Not connected"}</p>
          <span>Outputs</span>
          <p>{module.connectedOutputs.length ? module.connectedOutputs.join(" / ") : "Not connected"}</p>
        </div>
        {module.features.length ? (
          <ul className="dashboard-module-features">
            {module.features.map((feature) => (
              <li key={feature}>{feature}</li>
            ))}
          </ul>
        ) : null}
        {module.badges.length ? (
          <div className="dashboard-module-badges">
            {module.badges.map((badge) => (
              <span key={badge}>{badge}</span>
            ))}
          </div>
        ) : null}
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

function DemoPortfolioCard({
  portfolio,
  labels,
}: {
  portfolio: DemoPortfolio;
  labels: {
    demoBadge: string;
    strategyType: string;
    targetAllocation: string;
    holdings: string;
    baseCurrency: string;
    benchmark: string;
    bestShowcase: string;
    openPortfolioBuilder: string;
  };
}) {
  return (
    <Link className="dashboard-demo-card" to="/portfolio-builder">
      <div className="dashboard-demo-card__header">
        <span className="equity-kicker">{labels.demoBadge}</span>
        <StatusBadge label={portfolio.riskProfile} variant={portfolio.riskVariant} />
      </div>
      <div>
        <p className="dashboard-demo-card__strategy">
          {labels.strategyType}: <strong>{portfolio.strategyType}</strong>
        </p>
        <h3>{portfolio.name}</h3>
        <p>{portfolio.description}</p>
      </div>
      <dl className="dashboard-demo-card__facts">
        <div>
          <dt>{labels.targetAllocation}</dt>
          <dd>{portfolio.targetAllocation}</dd>
        </div>
        <div>
          <dt>{labels.holdings}</dt>
          <dd>{portfolio.holdings}</dd>
        </div>
        <div>
          <dt>{labels.baseCurrency}</dt>
          <dd>{portfolio.baseCurrency}</dd>
        </div>
        <div>
          <dt>{labels.benchmark}</dt>
          <dd>{portfolio.benchmark}</dd>
        </div>
      </dl>
      <div className="dashboard-demo-card__showcase">
        <span>{labels.bestShowcase}</span>
        <div>
          {portfolio.bestShowcase.map((module) => (
            <strong key={module}>{module}</strong>
          ))}
        </div>
      </div>
      <span className="dashboard-demo-card__action">{labels.openPortfolioBuilder}</span>
    </Link>
  );
}
