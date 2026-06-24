import { useMemo, useState } from "react";
import type { ReactNode } from "react";
import { useQuery } from "@tanstack/react-query";

import { MoneyValue } from "../../../components/finance/MoneyValue";
import { PercentValue } from "../../../components/finance/PercentValue";
import { PageHeader } from "../../../components/layout/PageHeader";
import { EmptyState } from "../../../components/ui/EmptyState";
import { ErrorBanner } from "../../../components/ui/ErrorBanner";
import { LoadingState } from "../../../components/ui/LoadingState";
import { StatusBadge } from "../../../components/ui/StatusBadge";
import { PortfolioSelector } from "../../../components/workflow/PortfolioSelector";
import { usePortfolioContext } from "../../../context/PortfolioContext";
import { useTranslation } from "../../../hooks/useTranslation";
import { apiClient } from "../../../lib/api-client";
import { endpoints } from "../../../lib/endpoints";
import type {
  CustomStressScenario,
  GroupStressImpact,
  IntegrationStatus,
  PositionStressImpact,
  RiskMetricComparison,
  ScenarioLibraryResponse,
  StressLimitBreach,
  StressScenarioDefinition,
  StressTestingResponse,
  StressTestingRunRequest,
  StressTestingStatus,
  WorstContributor,
} from "../../../types/stress-testing";

type StressTab =
  | "overview"
  | "scenario"
  | "positions"
  | "groups"
  | "risk"
  | "rates"
  | "volOptions"
  | "limits"
  | "methodology"
  | "commentary";

const tabs: StressTab[] = [
  "overview",
  "scenario",
  "positions",
  "groups",
  "risk",
  "rates",
  "volOptions",
  "limits",
  "methodology",
  "commentary",
];

const DEFAULT_CUSTOM_SCENARIO: CustomStressScenario = {
  name: "Custom Scenario",
  description: "User-defined multi-asset stress scenario.",
  equity_shock: -0.1,
  asset_class_shocks: {},
  sector_shocks: { Technology: -0.15 },
  symbol_shocks: {},
  rate_shock_bps: 50,
  volatility_shock: 0.25,
  fx_shock: 0,
  credit_spread_shock_bps: 75,
  liquidity_multiplier: 1,
};

export function StressTestingPage() {
  const { t } = useTranslation();
  const {
    holdings,
    isLoading: portfolioContextLoading,
    selectedPortfolio,
    selectedPortfolioId,
  } = usePortfolioContext();
  const [activeTab, setActiveTab] = useState<StressTab>("overview");
  const [scenarioId, setScenarioId] = useState("risk_off_combined");
  const [benchmarkSymbol, setBenchmarkSymbol] = useState("SPY");
  const [confidenceLevel, setConfidenceLevel] = useState(0.95);
  const [customScenario, setCustomScenario] = useState<CustomStressScenario>(
    DEFAULT_CUSTOM_SCENARIO,
  );
  const isCustomScenario = scenarioId === "custom_scenario";

  const statusQuery = useQuery({
    queryKey: ["stress-testing-status"],
    queryFn: () => apiClient.get<StressTestingStatus>(endpoints.stressTestingStatus),
  });
  const scenariosQuery = useQuery({
    queryKey: ["stress-testing-scenarios"],
    queryFn: () =>
      apiClient.get<ScenarioLibraryResponse>(endpoints.stressTestingScenarios),
  });
  const scenarios = scenariosQuery.data?.scenarios ?? [];
  const selectedScenario = useMemo(
    () => scenarios.find((scenario) => scenario.id === scenarioId) ?? null,
    [scenarioId, scenarios],
  );
  const holdingsSignature = useMemo(
    () =>
      holdings
        .map((holding) =>
          [
            holding.id,
            holding.symbol,
            holding.quantity,
            holding.current_price,
            holding.asset_type,
            holding.sector,
            holding.currency,
          ].join(":"),
        )
        .join("|"),
    [holdings],
  );

  const requestPayload = useMemo<StressTestingRunRequest | null>(() => {
    if (!selectedPortfolioId) {
      return null;
    }
    return {
      portfolio_id: selectedPortfolioId,
      scenario_id: isCustomScenario ? null : scenarioId,
      custom_scenario: isCustomScenario ? customScenario : null,
      benchmark_symbol: benchmarkSymbol.trim().toUpperCase() || "SPY",
      confidence_level: confidenceLevel,
      include_position_impacts: true,
      include_risk_metrics: true,
      include_module_links: true,
    };
  }, [
    benchmarkSymbol,
    confidenceLevel,
    customScenario,
    isCustomScenario,
    scenarioId,
    selectedPortfolioId,
  ]);

  const stressQuery = useQuery({
    queryKey: [
      "stress-testing-run",
      requestPayload,
      holdingsSignature,
    ],
    enabled: Boolean(requestPayload),
    queryFn: () =>
      apiClient.post<StressTestingResponse>(
        endpoints.stressTestingRun,
        requestPayload,
      ),
  });
  const analysis = stressQuery.data;
  const currency = analysis?.selected_portfolio.base_currency ?? "USD";
  const isLoading =
    portfolioContextLoading ||
    statusQuery.isLoading ||
    scenariosQuery.isLoading ||
    stressQuery.isLoading;
  const hasError = statusQuery.isError || scenariosQuery.isError || stressQuery.isError;

  function runStressTest() {
    void stressQuery.refetch();
    setActiveTab("overview");
  }

  function resetControls() {
    setScenarioId("risk_off_combined");
    setBenchmarkSymbol(selectedPortfolio?.benchmark ?? "SPY");
    setConfidenceLevel(0.95);
    setCustomScenario(DEFAULT_CUSTOM_SCENARIO);
    setActiveTab("overview");
  }

  return (
    <div className="page stress-testing-page risk-monitor-page">
      <PageHeader
        title={t("stressTesting.title")}
        subtitle={t("stressTesting.subtitle")}
      />

      <section className="risk-monitor-command-panel stress-command-panel">
        <div>
          <span>{t("stressTesting.workbench.eyebrow")}</span>
          <h2>{t("stressTesting.workbench.title")}</h2>
          <p>{t("stressTesting.workbench.description")}</p>
        </div>
        <div className="risk-monitor-badge-cluster">
          <StatusBadge
            label={statusQuery.data?.status ?? t("common.loading")}
            variant={statusQuery.data?.status === "ready" ? "success" : "warning"}
          />
          <StatusBadge label={t("stressTesting.badges.riskManagement")} variant="info" />
          <StatusBadge label={t("stressTesting.badges.portfolioConnected")} variant="success" />
          <StatusBadge label={t("stressTesting.badges.riskMonitorReady")} variant="success" />
          <StatusBadge label={t("stressTesting.badges.beta")} variant="warning" />
        </div>
      </section>

      <section className="stress-controls-grid">
        <PortfolioSelector compact showDetails />
        <div className="stress-control-card">
          <div className="section-heading">
            <span>{t("stressTesting.controls.eyebrow")}</span>
            <h2>{t("stressTesting.controls.title")}</h2>
            <p>{t("stressTesting.controls.description")}</p>
          </div>
          <div className="stress-control-grid">
            <label className="form-field">
              <span>{t("stressTesting.controls.scenario")}</span>
              <select
                value={scenarioId}
                onChange={(event) => setScenarioId(event.target.value)}
              >
                {scenarios.map((scenario) => (
                  <option key={scenario.id} value={scenario.id}>
                    {scenarioLabel(scenario, t)}
                  </option>
                ))}
                <option value="custom_scenario">
                  {t("stressTesting.scenarios.customScenario")}
                </option>
              </select>
            </label>
            <label className="form-field">
              <span>{t("stressTesting.controls.benchmark")}</span>
              <input
                value={benchmarkSymbol}
                onChange={(event) => setBenchmarkSymbol(event.target.value)}
              />
            </label>
            <label className="form-field">
              <span>{t("stressTesting.controls.confidence")}</span>
              <select
                value={confidenceLevel}
                onChange={(event) => setConfidenceLevel(Number(event.target.value))}
              >
                <option value={0.95}>95%</option>
                <option value={0.975}>97.5%</option>
                <option value={0.99}>99%</option>
              </select>
            </label>
          </div>
          {isCustomScenario ? (
            <CustomScenarioControls
              scenario={customScenario}
              onChange={setCustomScenario}
            />
          ) : selectedScenario ? (
            <ScenarioMiniCard scenario={selectedScenario} />
          ) : null}
          <div className="stress-actions">
            <button
              className="button button--primary"
              type="button"
              disabled={!requestPayload || isLoading}
              onClick={runStressTest}
            >
              {t("stressTesting.controls.run")}
            </button>
            <button
              className="button button--ghost"
              type="button"
              onClick={resetControls}
            >
              {t("stressTesting.controls.reset")}
            </button>
          </div>
        </div>
      </section>

      {hasError ? (
        <ErrorBanner
          title={t("stressTesting.error.title")}
          message={t("stressTesting.error.message")}
          retryLabel={t("stressTesting.error.retry")}
          onRetry={runStressTest}
        />
      ) : null}

      {isLoading ? <LoadingState label={t("common.loading")} /> : null}

      {!selectedPortfolio && !isLoading ? (
        <EmptyState
          title={t("stressTesting.empty.title")}
          message={t("stressTesting.empty.message")}
        />
      ) : null}

      {analysis ? (
        <>
          <StressKpiGrid analysis={analysis} currency={currency} />

          <nav className="risk-monitor-tabs stress-tabs" aria-label="Stress testing sections">
            {tabs.map((tab) => (
              <button
                key={tab}
                className={`risk-monitor-tab ${
                  activeTab === tab ? "risk-monitor-tab--active" : ""
                }`}
                type="button"
                onClick={() => setActiveTab(tab)}
              >
                <span>{t(`stressTesting.tabs.${tab}`)}</span>
                <small>{t(`stressTesting.tabs.${tab}Short`)}</small>
              </button>
            ))}
          </nav>

          <div className="risk-monitor-panel stress-panel">
            {activeTab === "overview" ? (
              <OverviewTab analysis={analysis} currency={currency} />
            ) : null}
            {activeTab === "scenario" ? (
              <ScenarioTab analysis={analysis} />
            ) : null}
            {activeTab === "positions" ? (
              <PositionImpactTab positions={analysis.position_impacts} currency={currency} />
            ) : null}
            {activeTab === "groups" ? (
              <GroupImpactTab analysis={analysis} currency={currency} />
            ) : null}
            {activeTab === "risk" ? (
              <RiskMetricsTab metrics={analysis.risk_metrics} currency={currency} />
            ) : null}
            {activeTab === "rates" ? (
              <RatesTab analysis={analysis} currency={currency} />
            ) : null}
            {activeTab === "volOptions" ? (
              <VolOptionsTab analysis={analysis} currency={currency} />
            ) : null}
            {activeTab === "limits" ? (
              <LimitBreachesTab breaches={analysis.limit_breaches} />
            ) : null}
            {activeTab === "methodology" ? (
              <MethodologyTab analysis={analysis} />
            ) : null}
            {activeTab === "commentary" ? (
              <CommentaryTab analysis={analysis} />
            ) : null}
          </div>
        </>
      ) : null}
    </div>
  );
}

function StressKpiGrid({
  analysis,
  currency,
}: {
  analysis: StressTestingResponse;
  currency: string;
}) {
  const { t } = useTranslation();
  const worst = analysis.worst_contributors[0]?.name ?? t("common.unavailable");
  const stressedVar = analysis.risk_monitor_payload.stressed_var;
  const stressedCvar = analysis.risk_monitor_payload.stressed_cvar;
  const stressedVol = analysis.risk_monitor_payload.stressed_volatility;
  return (
    <section className="portfolio-metric-grid stress-kpi-grid">
      <StressMetricCard label={t("stressTesting.kpis.baseValue")} value={<MoneyValue value={analysis.base_portfolio_value} currency={currency} />} />
      <StressMetricCard label={t("stressTesting.kpis.stressedValue")} value={<MoneyValue value={analysis.stressed_portfolio_value} currency={currency} />} tone="warning" />
      <StressMetricCard label={t("stressTesting.kpis.estimatedLoss")} value={<MoneyValue value={analysis.dollar_loss} currency={currency} />} tone={analysis.dollar_loss > 0 ? "negative" : "positive"} />
      <StressMetricCard label={t("stressTesting.kpis.lossPercent")} value={<PercentValue value={analysis.percent_loss} />} tone={analysis.percent_loss > 0.1 ? "negative" : "warning"} />
      <StressMetricCard label={t("stressTesting.kpis.severity")} value={analysis.severity.severity} tone={severityTone(analysis.severity.severity)} meta={`${analysis.severity.score}/100`} />
      <StressMetricCard label={t("stressTesting.kpis.worstContributor")} value={worst} meta={analysis.worst_contributors[0] ? `${Math.round(analysis.worst_contributors[0].contribution_to_loss * 100)}%` : ""} />
      <StressMetricCard label={t("stressTesting.kpis.stressedVar")} value={stressedVar === null ? t("common.unavailable") : <MoneyValue value={stressedVar} currency={currency} />} />
      <StressMetricCard label={t("stressTesting.kpis.stressedCvar")} value={stressedCvar === null ? t("common.unavailable") : <MoneyValue value={stressedCvar} currency={currency} />} />
      <StressMetricCard label={t("stressTesting.kpis.stressedVol")} value={stressedVol === null ? t("common.unavailable") : <PercentValue value={stressedVol} />} />
    </section>
  );
}

function StressMetricCard({
  label,
  value,
  meta,
  tone = "neutral",
}: {
  label: string;
  value: ReactNode;
  meta?: string;
  tone?: "neutral" | "positive" | "warning" | "negative";
}) {
  return (
    <article className={`portfolio-metric-card portfolio-metric-card--${tone}`}>
      <div className="portfolio-metric-card__header">
        <span>{label}</span>
      </div>
      <strong>{value}</strong>
      {meta ? <p>{meta}</p> : null}
    </article>
  );
}

function OverviewTab({
  analysis,
  currency,
}: {
  analysis: StressTestingResponse;
  currency: string;
}) {
  const { t } = useTranslation();
  return (
    <div className="stress-two-column">
      <section className="card stress-section-card">
        <div className="section-heading">
          <span>{t("stressTesting.overview.scenario")}</span>
          <h2>{analysis.selected_scenario.name}</h2>
          <p>{analysis.selected_scenario.description}</p>
        </div>
        <dl className="stress-definition-grid">
          <Definition label={t("stressTesting.overview.portfolio")} value={analysis.selected_portfolio.name} />
          <Definition label={t("stressTesting.overview.positions")} value={analysis.selected_portfolio.positions} />
          <Definition label={t("stressTesting.overview.base")} value={<MoneyValue value={analysis.base_portfolio_value} currency={currency} />} />
          <Definition label={t("stressTesting.overview.stressed")} value={<MoneyValue value={analysis.stressed_portfolio_value} currency={currency} />} />
          <Definition label={t("stressTesting.overview.loss")} value={<MoneyValue value={analysis.dollar_loss} currency={currency} />} />
          <Definition label={t("stressTesting.overview.lossPercent")} value={<PercentValue value={analysis.percent_loss} />} />
        </dl>
      </section>
      <section className="card stress-section-card">
        <div className="section-heading">
          <span>{t("stressTesting.overview.severity")}</span>
          <h2>{analysis.severity.severity}</h2>
          <p>{analysis.athena_commentary.summary}</p>
        </div>
        <div className="stress-score-bar">
          <span style={{ width: `${analysis.severity.score}%` }} />
        </div>
        <ul className="portfolio-note-list">
          {analysis.severity.main_drivers.map((driver) => (
            <li key={driver}>{driver}</li>
          ))}
        </ul>
      </section>
      <section className="card stress-section-card stress-span-2">
        <div className="section-heading">
          <span>{t("stressTesting.overview.integrations")}</span>
          <h2>{t("stressTesting.overview.integrationsTitle")}</h2>
        </div>
        <div className="stress-integration-grid">
          {analysis.integrations.map((integration) => (
            <IntegrationCard key={integration.module} integration={integration} />
          ))}
        </div>
      </section>
    </div>
  );
}

function ScenarioTab({ analysis }: { analysis: StressTestingResponse }) {
  const { t } = useTranslation();
  const shocks = analysis.selected_scenario.shocks;
  return (
    <div className="stress-two-column">
      <ShockMapCard title={t("stressTesting.scenario.assetClassShocks")} values={shocks.asset_class_shocks} />
      <ShockMapCard title={t("stressTesting.scenario.sectorShocks")} values={shocks.sector_shocks} />
      <ShockMapCard title={t("stressTesting.scenario.symbolShocks")} values={shocks.symbol_shocks} />
      <section className="card stress-section-card">
        <div className="section-heading">
          <span>{t("stressTesting.scenario.crossAsset")}</span>
          <h2>{t("stressTesting.scenario.assumptions")}</h2>
        </div>
        <dl className="stress-definition-grid">
          <Definition label={t("stressTesting.scenario.rateShock")} value={`${shocks.rate_shock_bps} bps`} />
          <Definition label={t("stressTesting.scenario.volShock")} value={<PercentValue value={shocks.volatility_shock} />} />
          <Definition label={t("stressTesting.scenario.fxShock")} value={<PercentValue value={shocks.fx_shock} />} />
          <Definition label={t("stressTesting.scenario.creditShock")} value={`${shocks.credit_spread_shock_bps} bps`} />
          <Definition label={t("stressTesting.scenario.liquidity")} value={`${shocks.liquidity_multiplier}x`} />
        </dl>
      </section>
    </div>
  );
}

function PositionImpactTab({
  positions,
  currency,
}: {
  positions: PositionStressImpact[];
  currency: string;
}) {
  const { t } = useTranslation();
  return (
    <section className="card stress-section-card">
      <div className="section-heading">
        <span>{t("stressTesting.positions.eyebrow")}</span>
        <h2>{t("stressTesting.positions.title")}</h2>
      </div>
      <div className="table-scroll">
        <table className="data-table stress-table">
          <thead>
            <tr>
              <th>{t("stressTesting.positions.symbol")}</th>
              <th>{t("stressTesting.positions.assetClass")}</th>
              <th>{t("stressTesting.positions.sector")}</th>
              <th>{t("stressTesting.positions.base")}</th>
              <th>{t("stressTesting.positions.shock")}</th>
              <th>{t("stressTesting.positions.stressed")}</th>
              <th>{t("stressTesting.positions.impact")}</th>
              <th>{t("stressTesting.positions.contribution")}</th>
            </tr>
          </thead>
          <tbody>
            {positions.map((position) => (
              <tr key={position.position_id}>
                <td className="data-table__symbol">{position.symbol}</td>
                <td>{position.asset_class}</td>
                <td>{position.sector}</td>
                <td><MoneyValue value={position.base_value} currency={currency} /></td>
                <td><PercentValue value={position.shock_applied} /></td>
                <td><MoneyValue value={position.stressed_value} currency={currency} /></td>
                <td className={position.dollar_impact < 0 ? "negative-value" : "positive-value"}>
                  <MoneyValue value={position.dollar_impact} currency={currency} />
                </td>
                <td><PercentValue value={position.contribution_to_loss} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function GroupImpactTab({
  analysis,
  currency,
}: {
  analysis: StressTestingResponse;
  currency: string;
}) {
  const { t } = useTranslation();
  return (
    <div className="stress-three-column">
      <GroupImpactCard title={t("stressTesting.groups.assetClass")} rows={analysis.asset_class_impacts} currency={currency} />
      <GroupImpactCard title={t("stressTesting.groups.sector")} rows={analysis.sector_impacts} currency={currency} />
      <GroupImpactCard title={t("stressTesting.groups.currency")} rows={analysis.currency_impacts} currency={currency} />
    </div>
  );
}

function RiskMetricsTab({
  metrics,
  currency,
}: {
  metrics: RiskMetricComparison[];
  currency: string;
}) {
  const { t } = useTranslation();
  return (
    <section className="card stress-section-card">
      <div className="section-heading">
        <span>{t("stressTesting.risk.eyebrow")}</span>
        <h2>{t("stressTesting.risk.title")}</h2>
      </div>
      <div className="stress-before-after-grid">
        {metrics.map((metric) => (
          <article className="stress-before-after-card" key={metric.metric}>
            <span>{metric.metric}</span>
            <div>
              <strong>{formatMetric(metric.before, metric.unit, currency)}</strong>
              <strong>{formatMetric(metric.after, metric.unit, currency)}</strong>
            </div>
            <p>{metric.source}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

function RatesTab({
  analysis,
  currency,
}: {
  analysis: StressTestingResponse;
  currency: string;
}) {
  const { t } = useTranslation();
  const rates = analysis.fixed_income_stress;
  return (
    <section className="card stress-section-card">
      <div className="section-heading">
        <span>{t("stressTesting.rates.eyebrow")}</span>
        <h2>{t("stressTesting.rates.title")}</h2>
        <p>{rates.data_source}</p>
      </div>
      <dl className="stress-definition-grid">
        <Definition label={t("stressTesting.rates.exposure")} value={<MoneyValue value={rates.fixed_income_exposure} currency={currency} />} />
        <Definition label={t("stressTesting.rates.weight")} value={<PercentValue value={rates.fixed_income_weight} />} />
        <Definition label={t("stressTesting.rates.duration")} value={formatNullable(rates.weighted_average_duration)} />
        <Definition label={t("stressTesting.rates.dv01")} value={rates.estimated_dv01 === null ? t("common.unavailable") : <MoneyValue value={rates.estimated_dv01} currency={currency} />} />
        <Definition label={t("stressTesting.rates.rateShock")} value={`${rates.rate_shock_bps} bps`} />
        <Definition label={t("stressTesting.rates.creditShock")} value={`${rates.credit_spread_shock_bps} bps`} />
        <Definition label={t("stressTesting.rates.impact")} value={<MoneyValue value={rates.rate_risk_impact} currency={currency} />} />
      </dl>
      <WarningList warnings={rates.warnings} />
    </section>
  );
}

function VolOptionsTab({
  analysis,
  currency,
}: {
  analysis: StressTestingResponse;
  currency: string;
}) {
  const { t } = useTranslation();
  const options = analysis.options_risk;
  return (
    <div className="stress-two-column">
      <section className="card stress-section-card">
        <div className="section-heading">
          <span>{t("stressTesting.volOptions.volEyebrow")}</span>
          <h2>{t("stressTesting.volOptions.volTitle")}</h2>
        </div>
        <dl className="stress-definition-grid">
          {analysis.risk_metrics
            .filter((metric) => metric.metric.includes("volatility"))
            .map((metric) => (
              <Definition
                key={metric.metric}
                label={metric.metric}
                value={formatMetric(metric.after, metric.unit, currency)}
              />
            ))}
          <Definition
            label={t("stressTesting.scenario.volShock")}
            value={<PercentValue value={analysis.selected_scenario.shocks.volatility_shock} />}
          />
        </dl>
      </section>
      <section className="card stress-section-card">
        <div className="section-heading">
          <span>{t("stressTesting.volOptions.optionsEyebrow")}</span>
          <h2>{t("stressTesting.volOptions.optionsTitle")}</h2>
          <p>{options.status}</p>
        </div>
        <dl className="stress-definition-grid">
          <Definition label={t("stressTesting.volOptions.ready")} value={options.options_pricing_lab_ready ? t("common.yes") : t("common.no")} />
          <Definition label={t("stressTesting.volOptions.detected")} value={options.option_positions_detected ? t("common.yes") : t("common.no")} />
          <Definition label={t("stressTesting.volOptions.delta")} value={options.delta_adjusted_exposure === null ? t("common.unavailable") : <MoneyValue value={options.delta_adjusted_exposure} currency={currency} />} />
        </dl>
        <WarningList warnings={options.warnings} />
      </section>
    </div>
  );
}

function LimitBreachesTab({ breaches }: { breaches: StressLimitBreach[] }) {
  const { t } = useTranslation();
  if (!breaches.length) {
    return (
      <EmptyState
        title={t("stressTesting.limits.emptyTitle")}
        message={t("stressTesting.limits.emptyMessage")}
      />
    );
  }
  return (
    <section className="card stress-section-card">
      <div className="section-heading">
        <span>{t("stressTesting.limits.eyebrow")}</span>
        <h2>{t("stressTesting.limits.title")}</h2>
      </div>
      <div className="stress-warning-grid">
        {breaches.map((breach) => (
          <article className="portfolio-warning-card portfolio-warning-card--high" key={breach.rule_name}>
            <div className="portfolio-warning-card__header">
              <strong>{breach.rule_name}</strong>
              <StatusBadge label={breach.severity} variant="warning" />
            </div>
            <p>{breach.explanation}</p>
            <small>{breach.suggested_action}</small>
          </article>
        ))}
      </div>
    </section>
  );
}

function MethodologyTab({ analysis }: { analysis: StressTestingResponse }) {
  const { t } = useTranslation();
  return (
    <div className="stress-two-column">
      <TextListCard title={t("stressTesting.methodology.assumptions")} items={analysis.methodology.assumptions} />
      <TextListCard title={t("stressTesting.methodology.sources")} items={analysis.methodology.data_sources} />
      <TextListCard title={t("stressTesting.methodology.limitations")} items={analysis.methodology.limitations} />
      <TextListCard title={t("stressTesting.methodology.warnings")} items={analysis.warnings.length ? analysis.warnings : [t("stressTesting.methodology.noWarnings")]} />
    </div>
  );
}

function CommentaryTab({ analysis }: { analysis: StressTestingResponse }) {
  const { t } = useTranslation();
  return (
    <div className="stress-two-column">
      <section className="card stress-section-card stress-commentary-card">
        <div className="section-heading">
          <span>{t("stressTesting.commentary.eyebrow")}</span>
          <h2>{t("stressTesting.commentary.title")}</h2>
          <p>{analysis.athena_commentary.summary}</p>
        </div>
      </section>
      <TextListCard title={t("stressTesting.commentary.keyPoints")} items={analysis.athena_commentary.key_points} />
      <TextListCard title={t("stressTesting.commentary.actions")} items={analysis.athena_commentary.suggested_actions} />
    </div>
  );
}

function CustomScenarioControls({
  scenario,
  onChange,
}: {
  scenario: CustomStressScenario;
  onChange: (scenario: CustomStressScenario) => void;
}) {
  const { t } = useTranslation();
  function update(key: keyof CustomStressScenario, value: number | string) {
    onChange({ ...scenario, [key]: value });
  }
  return (
    <div className="stress-custom-grid">
      <label className="form-field">
        <span>{t("stressTesting.custom.equity")}</span>
        <input
          type="number"
          value={scenario.equity_shock * 100}
          onChange={(event) => update("equity_shock", Number(event.target.value) / 100)}
        />
      </label>
      <label className="form-field">
        <span>{t("stressTesting.custom.technology")}</span>
        <input
          type="number"
          value={(scenario.sector_shocks.Technology ?? 0) * 100}
          onChange={(event) =>
            onChange({
              ...scenario,
              sector_shocks: {
                ...scenario.sector_shocks,
                Technology: Number(event.target.value) / 100,
              },
            })
          }
        />
      </label>
      <label className="form-field">
        <span>{t("stressTesting.custom.rate")}</span>
        <input
          type="number"
          value={scenario.rate_shock_bps}
          onChange={(event) => update("rate_shock_bps", Number(event.target.value))}
        />
      </label>
      <label className="form-field">
        <span>{t("stressTesting.custom.vol")}</span>
        <input
          type="number"
          value={scenario.volatility_shock * 100}
          onChange={(event) => update("volatility_shock", Number(event.target.value) / 100)}
        />
      </label>
      <label className="form-field">
        <span>{t("stressTesting.custom.fx")}</span>
        <input
          type="number"
          value={scenario.fx_shock * 100}
          onChange={(event) => update("fx_shock", Number(event.target.value) / 100)}
        />
      </label>
      <label className="form-field">
        <span>{t("stressTesting.custom.credit")}</span>
        <input
          type="number"
          value={scenario.credit_spread_shock_bps}
          onChange={(event) => update("credit_spread_shock_bps", Number(event.target.value))}
        />
      </label>
    </div>
  );
}

function ScenarioMiniCard({ scenario }: { scenario: StressScenarioDefinition }) {
  const { t } = useTranslation();
  return (
    <div className="stress-scenario-mini">
      <strong>{scenarioLabel(scenario, t)}</strong>
      <p>{scenario.description}</p>
    </div>
  );
}

function ShockMapCard({
  title,
  values,
}: {
  title: string;
  values: Record<string, number>;
}) {
  const { t } = useTranslation();
  const entries = Object.entries(values);
  return (
    <section className="card stress-section-card">
      <div className="section-heading">
        <span>{t("stressTesting.scenario.shocks")}</span>
        <h2>{title}</h2>
      </div>
      {entries.length ? (
        <dl className="stress-definition-grid">
          {entries.map(([name, value]) => (
            <Definition key={name} label={name} value={<PercentValue value={value} />} />
          ))}
        </dl>
      ) : (
        <p className="status-message">{t("stressTesting.scenario.noSpecificShock")}</p>
      )}
    </section>
  );
}

function GroupImpactCard({
  title,
  rows,
  currency,
}: {
  title: string;
  rows: GroupStressImpact[];
  currency: string;
}) {
  return (
    <section className="card stress-section-card">
      <div className="section-heading">
        <span>Impact</span>
        <h2>{title}</h2>
      </div>
      <div className="stress-impact-list">
        {rows.map((row) => (
          <div key={row.name}>
            <span>{row.name}</span>
            <strong className={row.dollar_impact < 0 ? "negative-value" : "positive-value"}>
              <MoneyValue value={row.dollar_impact} currency={currency} />
            </strong>
            <small><PercentValue value={row.loss_contribution} /></small>
          </div>
        ))}
      </div>
    </section>
  );
}

function IntegrationCard({ integration }: { integration: IntegrationStatus }) {
  return (
    <article className="stress-integration-card">
      <div>
        <strong>{integration.module}</strong>
        <StatusBadge label={integration.status} variant={integration.status.includes("Partial") ? "warning" : "success"} />
      </div>
      <p>{integration.data_source}</p>
      <WarningList warnings={integration.warnings} />
    </article>
  );
}

function TextListCard({ title, items }: { title: string; items: string[] }) {
  return (
    <section className="card stress-section-card">
      <div className="section-heading">
        <span>Athena</span>
        <h2>{title}</h2>
      </div>
      <ul className="portfolio-note-list">
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </section>
  );
}

function WarningList({ warnings }: { warnings: string[] }) {
  if (!warnings.length) {
    return null;
  }
  return (
    <ul className="portfolio-note-list stress-warning-list">
      {warnings.map((warning) => (
        <li key={warning}>{warning}</li>
      ))}
    </ul>
  );
}

function Definition({
  label,
  value,
}: {
  label: string;
  value: ReactNode;
}) {
  return (
    <div>
      <dt>{label}</dt>
      <dd>{value}</dd>
    </div>
  );
}

function formatNullable(value: number | null) {
  return value === null ? "Unavailable" : value.toFixed(2);
}

function formatMetric(value: number | null, unit: string, currency: string) {
  if (value === null) {
    return "Unavailable";
  }
  if (unit === "currency") {
    return new Intl.NumberFormat("en-CA", {
      style: "currency",
      currency,
      maximumFractionDigits: 0,
    }).format(value);
  }
  if (unit === "ratio") {
    return new Intl.NumberFormat("en-CA", {
      style: "percent",
      maximumFractionDigits: 2,
    }).format(value);
  }
  return value.toFixed(2);
}

function severityTone(severity: string) {
  if (["Severe", "Critical", "High"].includes(severity)) {
    return "negative";
  }
  if (["Elevated", "Moderate"].includes(severity)) {
    return "warning";
  }
  return "positive";
}

function scenarioLabel(
  scenario: StressScenarioDefinition,
  t: (key: string, options?: { defaultValue?: string }) => string,
) {
  const key = `stressTesting.scenarios.${scenario.id}`;
  const translated = t(key, { defaultValue: scenario.name });
  return translated === key ? scenario.name : translated;
}
