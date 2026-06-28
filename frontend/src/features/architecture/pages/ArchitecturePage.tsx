import { useQuery } from "@tanstack/react-query";

import { PersistenceStatusPanel } from "../../../components/ui/PersistenceStatusPanel";
import { StatusBadge } from "../../../components/ui/StatusBadge";
import { useTranslation } from "../../../hooks/useTranslation";
import { demoWorkflowApi } from "../../../services/demoWorkflowApi";

type ArchitectureModule = {
  name: string;
  status: string;
  role: string;
  inputs: string[];
  outputs: string[];
  persistence: string;
  endpoints: string[];
  limitations: string[];
};

const modules: ArchitectureModule[] = [
  {
    name: "Market Data",
    status: "Solid",
    role: "Clean demo prices, returns, volatility and coverage checks.",
    inputs: ["Demo market feed", "CSV imports"],
    outputs: ["Portfolio coverage", "Returns", "Risk inputs"],
    persistence: "SQLite demo data and import path",
    endpoints: ["/api/market-data/assets", "/api/market-data/coverage"],
    limitations: ["No live vendor feed by default."],
  },
  {
    name: "Equity Analysis",
    status: "Solid",
    role: "Single-stock fundamentals, ratios, valuation, growth and analyst diagnostics.",
    inputs: ["Market Data", "Selected symbol", "Demo fundamentals"],
    outputs: ["Valuation view", "Quality diagnostics", "Portfolio research input"],
    persistence: "Generated on demand from demo datasets",
    endpoints: ["/api/equity/{symbol}/overview", "/api/equity/{symbol}/valuation"],
    limitations: ["Demo fundamentals only; no live filings feed."],
  },
  {
    name: "Portfolio Builder",
    status: "Solid",
    role: "Portfolio universe, holdings, allocation, concentration and policy context.",
    inputs: ["Market Data", "Demo portfolio store"],
    outputs: ["Positions", "Summary", "Allocation"],
    persistence: "SQLite demo portfolio store",
    endpoints: ["/api/portfolios", "/api/portfolios/{id}/summary"],
    limitations: ["No real custodian position feed."],
  },
  {
    name: "Trade Simulator",
    status: "Functional",
    role: "Portfolio-aware pre-trade impact and suitability simulation.",
    inputs: ["Portfolio Builder", "Market Data"],
    outputs: ["Trade payload", "Blotter-ready ticket"],
    persistence: "Simulation output, optional blotter persistence",
    endpoints: ["/api/trade-simulator/simulate"],
    limitations: ["No broker execution."],
  },
  {
    name: "Trade Blotter",
    status: "Beta",
    role: "Persistent simulated trade register and review workflow.",
    inputs: ["Trade Simulator", "Manual tickets"],
    outputs: ["Trades", "Costs", "P&L/Reconciliation inputs"],
    persistence: "Persistent history",
    endpoints: ["/api/trade-blotter/trades"],
    limitations: ["Demo workflow, no real order management system."],
  },
  {
    name: "Risk Monitor",
    status: "Beta",
    role: "Portfolio risk score, VaR/CVaR, drawdown, concentration and alerts.",
    inputs: ["Portfolio Builder", "Market Data", "Volatility/Rates/Options payloads"],
    outputs: ["Risk score", "Limit payload", "Athena commentary"],
    persistence: "Generated on demand",
    endpoints: ["/api/risk-monitor/analyze"],
    limitations: ["Deterministic demo assumptions may be used."],
  },
  {
    name: "Volatility Lab",
    status: "Beta+",
    role: "Realized/EWMA volatility, beta, correlation and VaR source workbench.",
    inputs: ["Market Data", "Portfolio Builder"],
    outputs: ["Volatility payload", "Risk Monitor payload"],
    persistence: "Generated on demand",
    endpoints: ["/api/volatility-lab/analyze-portfolio"],
    limitations: ["No external volatility surface vendor."],
  },
  {
    name: "Options Pricing Lab",
    status: "Beta+",
    role: "Black-Scholes, Greeks, put-call parity, payoff and option strategy analytics.",
    inputs: ["Market Data", "Volatility Lab"],
    outputs: ["Greeks payload", "Risk/Limit payload"],
    persistence: "Generated on demand",
    endpoints: ["/api/options-pricing-lab/price"],
    limitations: ["Educational pricing models, not execution quotes."],
  },
  {
    name: "Rates Lab",
    status: "Beta+",
    role: "Bond pricing, yield, duration, convexity, DV01 and curve scenarios.",
    inputs: ["Manual bond inputs", "Demo curve", "Portfolio Builder"],
    outputs: ["Rates risk payload", "Stress/Limit inputs"],
    persistence: "Generated on demand",
    endpoints: ["/api/rates-lab/portfolio-exposure"],
    limitations: ["Demo curve and deterministic assumptions."],
  },
  {
    name: "Stress Testing",
    status: "Beta",
    role: "Scenario losses, contributors, severity and limit-ready stress payloads.",
    inputs: ["Portfolio Builder", "Market Data", "Rates/Options/Volatility"],
    outputs: ["Stress run", "Limit Center payload"],
    persistence: "Persistent history",
    endpoints: ["/api/stress-testing/run"],
    limitations: ["Scenario shocks are deterministic demo assumptions."],
  },
  {
    name: "Limit Center",
    status: "Beta",
    role: "Governance rules, breach detection, exception workflow and review state.",
    inputs: ["Risk Monitor", "Stress Testing", "Rates", "Options", "Trades"],
    outputs: ["Breach register", "Reports payload"],
    persistence: "Persistent history with fallback",
    endpoints: ["/api/limit-center/evaluate", "/api/limit-center/breaches"],
    limitations: ["Governance demo, not compliance certification."],
  },
  {
    name: "P&L Attribution",
    status: "Beta",
    role: "Position, sector, asset class, benchmark, trade, rates and options attribution.",
    inputs: ["Portfolio Builder", "Market Data", "Trade Blotter"],
    outputs: ["P&L analysis", "Reports/Reconciliation payload"],
    persistence: "Persistent history",
    endpoints: ["/api/pnl-attribution/analyze", "/api/pnl-attribution/history"],
    limitations: ["Demo attribution assumptions, not official accounting."],
  },
  {
    name: "Reconciliation Center",
    status: "Beta",
    role: "Position, cash, price, trade, P&L and FX breaks vs demo custodian reference.",
    inputs: ["Portfolio", "Market Data", "P&L", "Trade Blotter"],
    outputs: ["Break register", "Review workflow", "Reports payload"],
    persistence: "Persistent history",
    endpoints: ["/api/reconciliation/run", "/api/reconciliation/breaks"],
    limitations: ["Demo custodian only."],
  },
  {
    name: "Reports Center",
    status: "Beta",
    role: "Snapshot-based reports with JSON, Markdown and CSV exports.",
    inputs: ["Risk", "P&L", "Reconciliation", "Limits", "Stress", "AI Anomaly"],
    outputs: ["Reports", "Exports"],
    persistence: "SQLite demo snapshots",
    endpoints: ["/api/reports-center/generate", "/api/reports-center/reports"],
    limitations: ["PDF export is roadmap."],
  },
  {
    name: "AI Anomaly Center",
    status: "Beta",
    role: "Rule-based anomaly monitoring across persisted history.",
    inputs: ["Trades", "P&L", "Reconciliation", "Limits", "Stress", "Market Data"],
    outputs: ["Anomaly register", "Review workflow", "AI Anomaly Report"],
    persistence: "Persistent history with fallback",
    endpoints: ["/api/ai-anomaly-center/scan"],
    limitations: ["Not production ML or fraud detection."],
  },
  {
    name: "Athena Intelligence Engine",
    status: "Beta",
    role: "Structured commentary and synthesis from Athena payloads.",
    inputs: ["Structured module payloads"],
    outputs: ["Commentary", "Report summaries", "Anomaly explanations"],
    persistence: "SQLite demo / deterministic fallback",
    endpoints: ["/api/athena-intelligence/commentary"],
    limitations: ["No investment advice; deterministic fallback if provider unavailable."],
  },
];

const flows: Array<[string, string[]]> = [
  ["Core portfolio workflow", ["Market Data", "Equity Analysis", "Portfolio Builder", "Risk Monitor"]],
  ["Trade workflow", ["Trade Simulator", "Trade Blotter", "P&L Attribution", "Reconciliation"]],
  ["Risk workflow", ["Volatility Lab", "Rates Lab", "Options Pricing Lab", "Risk Monitor", "Stress Testing", "Limit Center"]],
  ["Reporting workflow", ["Risk Monitor", "P&L", "Reconciliation", "Limits", "Stress", "Reports Center"]],
  ["AI workflow", ["Analytics payloads", "Athena Intelligence", "Commentary / Reports / Anomaly explanations"]],
  ["Monitoring workflow", ["Persisted history", "AI Anomaly Center", "Reports Center"]],
];

export function ArchitecturePage() {
  const { t } = useTranslation();
  const statusQuery = useQuery({
    queryKey: ["architecture-demo-status"],
    queryFn: demoWorkflowApi.status,
  });
  const persistence = statusQuery.data?.persistence ?? [];

  return (
    <div className="page architecture-page">
      <section className="architecture-hero">
        <span className="equity-kicker">{t("architecture.eyebrow")}</span>
        <h1>{t("architecture.title")}</h1>
        <p>{t("architecture.subtitle")}</p>
        <div className="architecture-hero__badges">
          <StatusBadge label="FastAPI" variant="info" />
          <StatusBadge label="React / TypeScript / Vite" variant="info" />
          <StatusBadge label="SQLite Demo Persistence" variant="success" />
          <StatusBadge label="Deterministic fallback" variant="warning" />
        </div>
      </section>

      <section className="architecture-overview-grid">
        <article>
          <span>{t("architecture.platformOverview")}</span>
          <strong>Athena AI Risk Terminal</strong>
          <p>Portfolio analytics, risk management, P&L attribution, reconciliation, reporting and AI-assisted monitoring in one modular demo platform.</p>
        </article>
        <article>
          <span>{t("architecture.activeModules")}</span>
          <strong>{statusQuery.data?.active_modules ?? modules.length}</strong>
          <p>Connected workstations and utility services ready for a recruiter walkthrough.</p>
        </article>
        <article>
          <span>{t("architecture.persistenceStatus")}</span>
          <strong>{statusQuery.data?.database_connected ? t("architecture.databaseConnected") : t("common.unavailable")}</strong>
          <p>Local SQLite demo foundation with explicit fallback labeling.</p>
        </article>
      </section>

      <section className="analytics-section">
        <header className="analytics-section__header">
          <h2>{t("architecture.moduleMap")}</h2>
          <p>{t("architecture.moduleMapDescription")}</p>
        </header>
        <div className="architecture-module-grid">
          {modules.map((module) => (
            <article key={module.name}>
              <div>
                <h3>{module.name}</h3>
                <StatusBadge label={module.status} variant={module.status === "Solid" ? "success" : "warning"} />
              </div>
              <p>{module.role}</p>
              <dl>
                <dt>{t("common.connectedInputs")}</dt>
                <dd>{module.inputs.join(" / ")}</dd>
                <dt>{t("common.connectedOutputs")}</dt>
                <dd>{module.outputs.join(" / ")}</dd>
                <dt>{t("architecture.persistenceStatus")}</dt>
                <dd>{module.persistence}</dd>
                <dt>{t("architecture.mainEndpoints")}</dt>
                <dd>{module.endpoints.join(" / ")}</dd>
              </dl>
              <ul>
                {module.limitations.map((limitation) => <li key={limitation}>{limitation}</li>)}
              </ul>
            </article>
          ))}
        </div>
      </section>

      <section className="analytics-section">
        <header className="analytics-section__header">
          <h2>{t("architecture.dataFlow")}</h2>
          <p>{t("architecture.dataFlowDescription")}</p>
        </header>
        <div className="architecture-flow-grid">
          {flows.map(([title, steps]) => (
            <article key={title}>
              <h3>{title}</h3>
              <div>
                {steps.map((step) => <span key={step}>{step}</span>)}
              </div>
            </article>
          ))}
        </div>
      </section>

      {persistence.length ? (
        <PersistenceStatusPanel
          title={t("architecture.persistenceMap")}
          description={t("architecture.persistenceMapDescription")}
          items={persistence}
        />
      ) : null}

      <section className="analytics-section">
        <header className="analytics-section__header">
          <h2>{t("architecture.projectLimitations")}</h2>
          <p>{t("architecture.projectLimitationsDescription")}</p>
        </header>
        <div className="architecture-limitations-grid">
          {[
            "Demo market data and deterministic assumptions are used where external feeds are unavailable.",
            "SQLite is the local demo persistence foundation; PostgreSQL is a future hardening path.",
            "No real broker execution, custodian integration or live market data vendor is active by default.",
            "Athena Intelligence uses deterministic fallback when no AI provider is configured.",
            "AI Anomaly Center is rule-based monitoring, not production fraud detection.",
            "Outputs are educational and analytical, not investment advice.",
          ].map((item) => <span key={item}>{item}</span>)}
        </div>
      </section>
    </div>
  );
}
