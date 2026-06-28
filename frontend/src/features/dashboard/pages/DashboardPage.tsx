import { Link } from "react-router-dom";
import { useState } from "react";
import type { ReactNode } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";

import { MoneyValue } from "../../../components/finance/MoneyValue";
import { PercentValue } from "../../../components/finance/PercentValue";
import { PersistenceStatusPanel } from "../../../components/ui/PersistenceStatusPanel";
import { StatusBadge, type StatusBadgeVariant } from "../../../components/ui/StatusBadge";
import { usePortfolioContext } from "../../../context/PortfolioContext";
import { useHealth } from "../../../hooks/useHealth";
import { useTranslation } from "../../../hooks/useTranslation";
import { athenaIntelligenceApi } from "../../../services/athenaIntelligenceApi";
import { demoWorkflowApi } from "../../../services/demoWorkflowApi";
import type { DemoRunSummary } from "../../../types/demo-workflow";

type Kpi = {
  label: string;
  value: string;
  detail: string;
  tone: "neutral" | "positive" | "warning";
};

type Module = {
  name: string;
  description: string;
  status: "Functional";
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
    value: "16/16",
    detail: "Core analytics, persistence, AI commentary, anomaly monitoring, trade workflow, P&L, reconciliation and reporting online",
    tone: "neutral",
  },
];

const modules: Module[] = [
  {
    name: "Market Data",
    description: "Clean prices, returns, volatility, benchmarks and data quality metrics.",
    status: "Functional",
    maturity: "Connected",
    path: "/market-data",
    connectedInputs: ["CSV imports", "Demo market feed"],
    connectedOutputs: ["Equity", "Portfolio", "Volatility", "Rates", "Stress Testing", "Reconciliation"],
    features: ["Price history", "Returns", "Data quality"],
    badges: ["Market Data", "Demo", "Connected"],
  },
  {
    name: "Equity Analysis",
    description: "Analyze valuation, profitability, growth, risk and CFA-style diagnostics.",
    status: "Functional",
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
    status: "Functional",
    maturity: "Connected",
    path: "/portfolio-builder",
    connectedInputs: ["Market Data", "Equity Analysis"],
    connectedOutputs: ["Trade Simulator", "Risk Monitor", "Rates Lab", "Stress Testing", "Reconciliation"],
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
    connectedOutputs: ["Trade Blotter", "Portfolio impact preview", "Reconciliation Center"],
    features: ["Order simulation", "Before/after impact", "Suitability"],
    badges: ["Portfolio Ready", "No Execution", "Blotter Ready"],
  },
  {
    name: "Trade Blotter",
    description: "Persistent simulated trade register with review workflow, costs, suitability status and downstream P&L/reconciliation integration.",
    status: "Functional",
    maturity: "Persistent",
    path: "/trade-blotter",
    connectedInputs: ["Trade Simulator", "Manual trade tickets"],
    connectedOutputs: ["P&L Attribution", "Reconciliation Center", "Reports Center", "Risk Monitor", "Limit Center"],
    features: ["Trade register", "Review workflow", "Costs", "Audit trail"],
    badges: ["Trade Workflow", "Persistent", "Review", "P&L Ready", "Reconciliation Ready", "Functional"],
  },
  {
    name: "Risk Monitor",
    description: "Track VaR, CVaR, drawdown, configurable limits and stress shocks.",
    status: "Functional",
    maturity: "Functional",
    path: "/risk-monitor",
    connectedInputs: ["Portfolio", "Volatility", "Options", "Rates"],
    connectedOutputs: ["Limit Center", "Stress Testing"],
    features: ["VaR/CVaR", "Drawdown", "Risk limits"],
    badges: ["Functional", "Portfolio Ready"],
  },
  {
    name: "Volatility Lab",
    description: "Institutional volatility workstation with realized, EWMA, VaR/CVaR, beta, correlation and Risk Monitor-ready outputs.",
    status: "Functional",
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
    status: "Functional",
    maturity: "Functional",
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
      "Functional",
      "Bilingual",
    ],
    connectedInputs: ["Market Data", "Volatility Lab"],
    connectedOutputs: ["Risk Monitor-ready Greeks", "Stress Testing", "Limit Center"],
  },
  {
    name: "Rates Lab",
    description: "Analyze bond pricing, yield, duration, convexity, DV01 and curve scenarios.",
    status: "Functional",
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
    status: "Functional",
    maturity: "Functional",
    path: "/stress-testing",
    connectedInputs: ["Portfolio Builder", "Market Data", "Volatility Lab", "Rates Lab", "Options Pricing Lab"],
    connectedOutputs: ["Risk Monitor payload", "Limit Center"],
    features: ["Scenario library", "Portfolio shocks", "Worst contributors", "Risk payload"],
    badges: ["Risk Management", "Scenario Analysis", "Portfolio Connected", "Risk Monitor Ready", "Functional"],
  },
  {
    name: "Limit Center",
    description: "Centralize portfolio, market, stress, rates, options and trade limits with breach review.",
    status: "Functional",
    maturity: "Governance Functional",
    path: "/limit-center",
    connectedInputs: ["Portfolio Builder", "Risk Monitor", "Stress Testing", "Volatility Lab", "Options Pricing Lab", "Rates Lab", "Trade Simulator"],
    connectedOutputs: ["Risk governance workflow", "Reports Center", "P&L Attribution"],
    features: ["Limit rules", "Breach register", "Exception workflow", "Severity engine"],
    badges: ["Risk Governance", "Breach Register", "Exceptions", "Athena Intelligence", "Functional"],
  },
  {
    name: "P&L Attribution",
    description: "Explain portfolio gains and losses by position, asset class, sector, income, trades, rates and options drivers.",
    status: "Functional",
    maturity: "Performance Functional",
    path: "/pnl-attribution",
    connectedInputs: ["Portfolio Builder", "Market Data", "Trade Blotter", "Rates Lab", "Options Pricing Lab"],
    connectedOutputs: ["Reconciliation Center", "Reports Center", "Athena Intelligence"],
    features: ["Position P&L", "Group attribution", "Benchmark active return", "Rates/options hooks"],
    badges: ["Performance Attribution", "Portfolio Connected", "Market Data", "Reports Ready", "Athena Intelligence", "Functional"],
  },
  {
    name: "Reconciliation Center",
    description: "Detect position, cash, price, trade and P&L breaks between Athena records and demo custodian reference data.",
    status: "Functional",
    maturity: "Middle Office Functional",
    path: "/reconciliation",
    connectedInputs: ["Portfolio Builder", "Market Data", "Trade Blotter", "P&L Attribution", "Athena Intelligence"],
    connectedOutputs: ["Break Register", "Review Workflow", "Reports Center"],
    features: ["Position breaks", "Cash & FX checks", "Price controls", "Review workflow"],
    badges: ["Middle Office", "Data Quality", "Break Register", "P&L Control", "Reports Ready", "Athena Intelligence", "Functional"],
  },
  {
    name: "AI Anomaly Center",
    description: "Detect unusual risk, P&L, trade, market data, limit and reconciliation patterns across Athena's persisted history.",
    status: "Functional",
    maturity: "Monitoring Functional",
    path: "/ai-anomaly-center",
    connectedInputs: ["Market Data", "Trade Blotter", "P&L Attribution", "Reconciliation Center", "Limit Center", "Stress Testing"],
    connectedOutputs: ["Review workflow", "Reports Center", "Athena Intelligence"],
    features: ["Rule-based scan", "Anomaly register", "Scoring", "Review workflow"],
    badges: ["Monitoring", "Rule-Based AI", "Persisted History", "Review Workflow", "Reports Ready", "Athena Intelligence", "Functional"],
  },
  {
    name: "Reports Center",
    description: "Generate structured portfolio, anomaly, reconciliation, P&L, risk, stress, limits, trade, rates and options reports from Athena analytics.",
    status: "Functional",
    maturity: "Snapshot Based",
    path: "/reports-center",
    connectedInputs: ["Portfolio Builder", "AI Anomaly Center", "Reconciliation Center", "P&L Attribution", "Risk Monitor", "Stress Testing", "Limit Center", "Athena Intelligence"],
    connectedOutputs: ["JSON export", "Markdown export", "CSV tables"],
    features: ["Report templates", "Snapshot builder", "Risk pack"],
    badges: ["Reporting", "Export", "Risk Pack", "Athena Intelligence", "Snapshot Based", "Functional"],
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
  ["09:55", "AI Anomaly Center scan, persistence and review workflow available"],
  ["09:50", "Trade Blotter persistence and review workflow available"],
  ["09:48", "Reconciliation Center break register available"],
  ["09:45", "Limit Center governance workflow available"],
  ["09:42", "Market data refreshed"],
  ["09:40", "Portfolio summary updated"],
  ["09:38", "Data quality check completed"],
  ["09:35", "Equity analysis module available"],
];

export function DashboardPage() {
  const { i18n, t } = useTranslation();
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
  const demoStatusQuery = useQuery({
    queryKey: ["demo-workflow-status"],
    queryFn: demoWorkflowApi.status,
  });
  const demoHistoryQuery = useQuery({
    queryKey: ["demo-workflow-history"],
    queryFn: demoWorkflowApi.history,
  });
  const [lastDemoRun, setLastDemoRun] = useState<DemoRunSummary | null>(null);
  const demoMutation = useMutation({
    mutationFn: () =>
      demoWorkflowApi.run({
        portfolio_id: "pf_004",
        language: i18n.language?.startsWith("fr") ? "fr" : "en",
        include_report: true,
      }),
    onSuccess: async (summary) => {
      setLastDemoRun(summary);
      await demoHistoryQuery.refetch();
    },
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
  const demoRun = lastDemoRun ?? demoHistoryQuery.data?.items[0] ?? null;
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
      name: "Trade Blotter",
      description: "Persist simulated trades, review decisions, cost estimates and downstream trade records.",
      path: "/trade-blotter",
      meta: "Persistent workflow",
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
    {
      name: "P&L Attribution",
      description: "Explain portfolio gains and losses by position, sector, asset class, trades, rates and options drivers.",
      path: "/pnl-attribution",
      meta: workflowPortfolioName,
    },
    {
      name: "Reconciliation Center",
      description: "Compare Athena portfolio, price, trade and P&L records with demo custodian reference data and review breaks.",
      path: "/reconciliation",
      meta: "Break register",
    },
    {
      name: "AI Anomaly Center",
      description: "Scan persisted history for unusual market data, trade, P&L, risk, limit, stress and reconciliation patterns.",
      path: "/ai-anomaly-center",
      meta: "Monitoring workflow",
    },
    {
      name: "Reports Center",
      description: "Generate snapshot-based portfolio, anomaly, reconciliation, P&L, risk, stress, limits, rates, options and trade reports.",
      path: "/reports-center",
      meta: "Risk pack",
    },
  ];
  const workflowTracks: Array<{
    title: string;
    modules: string[];
    destination?: string;
  }> = [
    {
      title: "Research to portfolio",
      modules: ["Market Data", "Equity Analysis", "Portfolio Builder", "Trade Simulator", "Trade Blotter", "P&L Attribution", "Reconciliation Center", "AI Anomaly Center"],
    },
    {
      title: "Derivatives risk",
      modules: ["Market Data", "Volatility Lab", "Options Pricing Lab", "Stress Testing", "Risk Monitor", "Limit Center", "AI Anomaly Center"],
    },
    {
      title: "Fixed-income risk",
      modules: ["Market Data", "Rates Lab", "Stress Testing", "Risk Monitor", "Limit Center", "AI Anomaly Center"],
    },
    {
      title: "Institutional stress workflow",
      modules: ["Portfolio Builder", "Volatility Lab", "Rates Lab", "Stress Testing", "Risk Monitor", "Limit Center", "P&L Attribution", "Reconciliation Center", "AI Anomaly Center", "Reports Center"],
    },
    {
      title: "Governance workflow",
      modules: ["Portfolio Builder", "Trade Simulator", "Trade Blotter", "Risk Monitor", "Stress Testing", "Limit Center", "P&L Attribution", "Reconciliation Center", "AI Anomaly Center", "Reports Center"],
      destination: "Report pack",
    },
    {
      title: "Performance attribution",
      modules: ["Market Data", "Portfolio Builder", "Trade Simulator", "Trade Blotter", "Rates Lab", "Options Pricing Lab", "P&L Attribution", "Reconciliation Center", "AI Anomaly Center", "Reports Center"],
      destination: "P&L report",
    },
    {
      title: "Middle-office reconciliation",
      modules: ["Portfolio Builder", "Market Data", "Trade Blotter", "P&L Attribution", "Reconciliation Center", "AI Anomaly Center", "Reports Center"],
      destination: "Reconciliation report",
    },
    {
      title: "Anomaly monitoring workflow",
      modules: ["Market Data", "Trade Blotter", "P&L Attribution", "Reconciliation Center", "Limit Center", "Stress Testing", "AI Anomaly Center", "Reports Center"],
      destination: "Anomaly report",
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
            construction, options and fixed-income analytics, P&L attribution, reconciliation, risk monitoring and limit governance in one clean
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

      <div className="dashboard-split-grid dashboard-split-grid--wide">
        <DemoWorkflowCard
          isRunning={demoMutation.isPending}
          run={demoRun}
          statusReady={demoStatusQuery.data?.status === "ready"}
          onRun={() => demoMutation.mutate()}
        />
        <SystemHealthCard
          activeModules={demoStatusQuery.data?.active_modules ?? 16}
          apiConnected={isConnected}
          databaseConnected={demoStatusQuery.data?.database_connected ?? false}
          lastDemoRun={demoRun}
          openAnomalies={demoRun?.anomalies_detected ?? 0}
          openBreaks={demoRun?.open_breaks ?? 0}
          reportsGenerated={demoRun?.generated_report_id ? 1 : 0}
        />
      </div>

      {demoMutation.isError ? (
        <section className="analytics-section">
          <header className="analytics-section__header">
            <h2>Demo workflow unavailable</h2>
            <p>The demo run could not complete. Check that the backend process is still running.</p>
          </header>
        </section>
      ) : null}

      {demoRun ? <DemoRunSummaryPanel run={demoRun} /> : null}

      <RecruiterQuickTour />

      {demoStatusQuery.data?.persistence?.length ? (
        <PersistenceStatusPanel
          compact
          title="Persistence Status"
          description="Local SQLite demo persistence and fallback behavior are explicit across the institutional workflow."
          items={demoStatusQuery.data.persistence}
        />
      ) : null}

      <DashboardSection
        title={t("workflow.connectedWorkflow")}
        description="Market Data and Portfolio Builder feed volatility, options, fixed-income, P&L and reconciliation analytics into Risk Monitor, Limit Center and reporting workflows."
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
        description="Sixteen connected workstations are active today, including the Architecture map, AI Anomaly Center, persistent Trade Blotter, P&L Attribution, Reconciliation Center and Reports Center."
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
            Rates Lab, Trade Simulator, Trade Blotter, Limit Center, P&L Attribution, Reconciliation Center and AI Anomaly Center. It generates structured commentary from module
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

function DemoWorkflowCard({
  isRunning,
  run,
  statusReady,
  onRun,
}: {
  isRunning: boolean;
  run: DemoRunSummary | null;
  statusReady: boolean;
  onRun: () => void;
}) {
  return (
    <section className="card dashboard-demo-run-card">
      <span className="equity-kicker">Demo Workflow</span>
      <div className="section-heading">
        <h2>Run Athena Demo Portfolio</h2>
        <StatusBadge label={statusReady ? "Ready" : "Backend check"} variant={statusReady ? "success" : "warning"} />
      </div>
      <p>
        Launch a coherent recruiter tour across Market Data, Portfolio Builder, Risk Monitor,
        P&L Attribution, Reconciliation, Limit Center, AI Anomaly Center and Reports Center.
      </p>
      <div className="dashboard-demo-run-actions">
        <button className="button button--primary" disabled={isRunning} type="button" onClick={onRun}>
          {isRunning ? "Running demo" : "Run Athena Demo Portfolio"}
        </button>
        {run?.generated_report_id ? (
          <Link className="button" to="/reports-center">
            View Generated Report
          </Link>
        ) : null}
      </div>
      <div className="dashboard-demo-run-pipeline">
        {["Market Data", "Portfolio", "Risk", "P&L", "Reconciliation", "Limits", "Anomalies", "Reports"].map((step) => (
          <span key={step}>{step}</span>
        ))}
      </div>
    </section>
  );
}

function SystemHealthCard({
  activeModules,
  apiConnected,
  databaseConnected,
  lastDemoRun,
  openAnomalies,
  openBreaks,
  reportsGenerated,
}: {
  activeModules: number;
  apiConnected: boolean;
  databaseConnected: boolean;
  lastDemoRun: DemoRunSummary | null;
  openAnomalies: number;
  openBreaks: number;
  reportsGenerated: number;
}) {
  const rows = [
    ["Backend ready", apiConnected ? "Yes" : "Demo fallback"],
    ["Database connected", databaseConnected ? "SQLite demo" : "Unknown"],
    ["Active modules", String(activeModules)],
    ["Last demo run", lastDemoRun ? formatDate(lastDemoRun.generated_at) : "Not run"],
    ["Reports generated", String(reportsGenerated)],
    ["Open anomalies / breaks", `${openAnomalies} / ${openBreaks}`],
  ];
  return (
    <section className="card dashboard-system-health-card">
      <span className="equity-kicker">System Health</span>
      <h2>Institutional demo readiness</h2>
      <div className="dashboard-system-health-grid">
        {rows.map(([label, value]) => (
          <div key={label}>
            <span>{label}</span>
            <strong>{value}</strong>
          </div>
        ))}
      </div>
    </section>
  );
}

function DemoRunSummaryPanel({ run }: { run: DemoRunSummary }) {
  const quickLinks = [
    ["View Portfolio", run.quick_links.portfolio],
    ["View Risk Monitor", run.quick_links.risk_monitor],
    ["View P&L", run.quick_links.pnl_attribution],
    ["View Reconciliation", run.quick_links.reconciliation],
    ["View Limit Center", run.quick_links.limit_center],
    ["View AI Anomalies", run.quick_links.ai_anomaly_center],
    ["View Generated Report", run.quick_links.reports_center],
  ];
  return (
    <DashboardSection
      title="Demo Run Summary"
      description="Point-in-time summary produced by the recruiter-ready Athena demo workflow."
    >
      <div className="dashboard-demo-summary-grid">
        <article>
          <span>Demo run ID</span>
          <strong>{run.demo_run_id}</strong>
        </article>
        <article>
          <span>Portfolio</span>
          <strong>{run.portfolio_name ?? run.portfolio_id}</strong>
        </article>
        <article>
          <span>Risk score</span>
          <strong>{run.risk_score ?? "n/a"}</strong>
        </article>
        <article>
          <span>Risk status</span>
          <strong>{run.highest_risk_status ?? "n/a"}</strong>
        </article>
        <article>
          <span>Total P&L</span>
          <strong>{run.total_pnl !== null && run.total_pnl !== undefined ? <MoneyValue value={run.total_pnl} /> : "n/a"}</strong>
        </article>
        <article>
          <span>Breaks / breaches / anomalies</span>
          <strong>{run.open_breaks ?? 0} / {run.limit_breaches ?? 0} / {run.anomalies_detected ?? 0}</strong>
        </article>
      </div>
      <div className="dashboard-demo-module-strip">
        {run.module_results.map((module) => (
          <article key={module.module}>
            <StatusBadge label={module.status} variant={module.status === "completed" ? "success" : "warning"} />
            <strong>{module.module}</strong>
            <span>{module.records_created} records</span>
          </article>
        ))}
      </div>
      {run.warnings.length ? (
        <div className="model-warning-list">
          {run.warnings.map((warning) => (
            <p key={warning}>{warning}</p>
          ))}
        </div>
      ) : null}
      <div className="dashboard-demo-run-actions">
        {quickLinks.map(([label, path]) => (
          <Link className="button" key={label} to={path}>
            {label}
          </Link>
        ))}
      </div>
    </DashboardSection>
  );
}

function RecruiterQuickTour() {
  const steps = [
    ["01", "View Dashboard", "/"],
    ["02", "Open Portfolio Builder", "/portfolio-builder"],
    ["03", "Run Risk Monitor", "/risk-monitor"],
    ["04", "Review P&L Attribution", "/pnl-attribution"],
    ["05", "Check Reconciliation", "/reconciliation"],
    ["06", "Generate Report", "/reports-center"],
    ["07", "Read Athena AI Commentary", "/ai-anomaly-center"],
  ];
  return (
    <DashboardSection
      title="Recruiter Quick Tour"
      description="A short path that shows the project value without requiring a deep code walkthrough."
    >
      <div className="dashboard-recruiter-tour">
        {steps.map(([index, label, path]) => (
          <Link key={index} to={path}>
            <span>{index}</span>
            <strong>{label}</strong>
          </Link>
        ))}
      </div>
    </DashboardSection>
  );
}

function formatDate(value: string) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString();
}

function ModuleCard({ module }: { module: Module }) {
  return (
    <Link className="dashboard-module-card" to={module.path}>
      <div>
        <div className="dashboard-module-badges">
          <StatusBadge label={module.status} variant="success" />
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
