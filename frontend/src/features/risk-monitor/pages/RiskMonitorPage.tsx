import { useMemo, useState } from "react";
import type { ReactNode } from "react";
import { useQuery } from "@tanstack/react-query";

import { AthenaAICommentaryCard } from "../../../components/ai/AthenaAICommentaryCard";
import { MoneyValue } from "../../../components/finance/MoneyValue";
import { PercentValue } from "../../../components/finance/PercentValue";
import { PageHeader } from "../../../components/layout/PageHeader";
import { PortfolioSelector } from "../../../components/workflow/PortfolioSelector";
import { usePortfolioContext } from "../../../context/PortfolioContext";
import { EmptyState } from "../../../components/ui/EmptyState";
import { LoadingState } from "../../../components/ui/LoadingState";
import { StatusBadge as RiskStatusBadge } from "../../../components/ui/StatusBadge";
import type { StatusBadgeVariant as BadgeVariant } from "../../../components/ui/StatusBadge";
import { useTranslation } from "../../../hooks/useTranslation";
import { apiClient } from "../../../lib/api-client";
import { endpoints } from "../../../lib/endpoints";
import {
  BenchmarkRiskResponse,
  RiskContributionResponse,
  RiskLimitOverrides,
  RiskLimitBreach,
  RiskMetric,
  RiskMonitorAnalysisResponse,
  RiskModuleStatus,
  RiskSourceMetadata,
  StressShockOverrides,
  StressScenarioResult,
} from "../../../types/risk";
import type { ModuleIntegrationStatus } from "../../../types/risk-shared";
import type { RiskMonitorPayload } from "../../../types/volatility";

const VOLATILITY_PAYLOAD_STORAGE_KEY = "athena.volatilityLab.riskPayload";

type RiskMonitorTab =
  | "overview"
  | "limits"
  | "metrics"
  | "stress"
  | "contribution"
  | "benchmark"
  | "commentary";

const tabs: RiskMonitorTab[] = [
  "overview",
  "limits",
  "metrics",
  "stress",
  "contribution",
  "benchmark",
  "commentary",
];

type RiskControlState = Required<
  Pick<
    RiskLimitOverrides,
    | "max_single_position_weight"
    | "max_sector_exposure"
    | "minimum_cash_reserve"
    | "max_portfolio_volatility"
    | "max_tracking_error"
  >
> &
  Required<StressShockOverrides>;

type RiskControlKey = keyof RiskControlState;

const DEFAULT_RISK_CONTROLS: RiskControlState = {
  max_single_position_weight: 0.25,
  max_sector_exposure: 0.5,
  minimum_cash_reserve: 0.05,
  max_portfolio_volatility: 0.2,
  max_tracking_error: 0.08,
  equity_market_shock: -0.1,
  technology_sector_shock: -0.15,
  interest_rate_shock: -0.05,
  largest_holding_shock: -0.2,
};

export function RiskMonitorPage() {
  const { t } = useTranslation();
  const {
    holdings,
    isLoading: isPortfolioContextLoading,
    selectPortfolio,
    selectedPortfolio,
  } = usePortfolioContext();
  const [activeTab, setActiveTab] = useState<RiskMonitorTab>("overview");
  const [riskControls, setRiskControls] = useState<RiskControlState>(
    DEFAULT_RISK_CONTROLS,
  );
  const volatilityPayload = useMemo(readVolatilityPayload, []);

  const statusQuery = useQuery({
    queryKey: ["risk-monitor-status"],
    queryFn: () => apiClient.get<RiskModuleStatus>(endpoints.riskMonitorStatus),
  });
  const holdingsSignature = useMemo(
    () =>
      holdings
        .map(
          (holding) =>
            [
              holding.id,
              holding.symbol,
              holding.asset_type,
              holding.quantity,
              holding.average_price,
              holding.current_price,
              holding.currency,
              holding.sector,
              holding.country,
            ].join(":"),
        )
        .join("|"),
    [holdings],
  );

  const analysisQuery = useQuery({
    queryKey: [
      "risk-monitor-analysis",
      selectedPortfolio?.id,
      volatilityPayload?.generated_at,
      holdingsSignature,
      riskControls,
    ],
    enabled: Boolean(selectedPortfolio?.id || volatilityPayload),
    queryFn: () => {
      if (volatilityPayload) {
        return apiClient.post<RiskMonitorAnalysisResponse>(
          endpoints.riskMonitorAnalyzeFromVolatility,
          volatilityPayload,
        );
      }
      return apiClient.post<RiskMonitorAnalysisResponse>(endpoints.riskMonitorAnalyze, {
        portfolio_id: selectedPortfolio?.id,
        benchmark_symbol: selectedPortfolio?.benchmark ?? "SPY",
        limits: buildLimitOverrides(riskControls),
        stress_shocks: buildStressShockOverrides(riskControls),
      });
    },
  });

  const analysis = analysisQuery.data;
  const isLoading =
    isPortfolioContextLoading || statusQuery.isLoading || analysisQuery.isLoading;
  const baseCurrency = selectedPortfolio?.base_currency ?? "USD";

  return (
    <div className="page risk-monitor-page">
      <PageHeader
        title={t("riskMonitor.title")}
        subtitle={t("riskMonitor.subtitle")}
      />

      <section className="risk-monitor-command-panel">
        <div>
          <span>{t("riskMonitor.workbench.eyebrow")}</span>
          <h2>{t("riskMonitor.workbench.title")}</h2>
          <p>{t("riskMonitor.workbench.description")}</p>
        </div>
        <div className="risk-monitor-command-panel__controls">
          <PortfolioSelector
            compact
            showDetails={false}
            onPortfolioChange={(portfolioId) => {
              selectPortfolio(portfolioId);
              setActiveTab("overview");
            }}
          />
          <div className="risk-monitor-holding-strip">
            <span>{t("riskMonitor.controls.coverage")}</span>
            <strong>
              {holdings.length} {t("riskMonitor.controls.positionsAnalyzed")}
            </strong>
            <div>
              {holdings.map((holding) => (
                <span className="status-pill" key={holding.id}>
                  {holding.symbol}
                </span>
              ))}
            </div>
          </div>
          <div className="risk-monitor-badge-cluster">
            <RiskStatusBadge
              label={statusQuery.data?.status ?? t("common.loading")}
              variant={statusQuery.data?.status === "ready" ? "success" : "warning"}
            />
            {analysis?.risk_source.badges.map((badge) => (
              <RiskStatusBadge
                key={badge}
                label={translateSourceBadge(badge, t)}
                variant={sourceBadgeVariant(badge)}
              />
            ))}
          </div>
          {volatilityPayload ? (
            <div className="workflow-notice">
              <strong>{t("riskMonitor.volatilityPayload.using")}</strong>
              <span>
                {t("riskMonitor.volatilityPayload.source")}:{" "}
                {volatilityPayload.source_module} /{" "}
                {new Date(volatilityPayload.generated_at).toLocaleString()}
              </span>
            </div>
          ) : null}
        </div>
      </section>

      <RiskControlsPanel
        controls={riskControls}
        onChange={(key, value) =>
          setRiskControls((current) => ({ ...current, [key]: value }))
        }
        onReset={() => setRiskControls(DEFAULT_RISK_CONTROLS)}
        t={t}
      />

      {isLoading ? <LoadingState label={t("common.loading")} /> : null}

      {!selectedPortfolio && !isLoading ? (
        <EmptyState
          title={t("riskMonitor.empty.title")}
          message={t("riskMonitor.empty.message")}
        />
      ) : null}

      {analysis ? (
        <>
          <RiskMonitorKpis
            analysis={analysis}
            currency={baseCurrency}
            t={t}
          />

          <nav className="risk-monitor-tabs" aria-label="Risk monitor sections">
            {tabs.map((tab) => (
              <button
                key={tab}
                className={`risk-monitor-tab ${
                  activeTab === tab ? "risk-monitor-tab--active" : ""
                }`}
                type="button"
                onClick={() => setActiveTab(tab)}
              >
                <span>{t(`riskMonitor.tabs.${tab}`)}</span>
                <small>{t(`riskMonitor.tabs.${tab}Short`)}</small>
              </button>
            ))}
          </nav>

          <div className="risk-monitor-panel">
            {activeTab === "overview" ? (
              <OverviewTab analysis={analysis} currency={baseCurrency} t={t} />
            ) : null}
            {activeTab === "limits" ? (
              <LimitsTab breaches={analysis.limit_breaches} t={t} />
            ) : null}
            {activeTab === "metrics" ? (
              <MetricsTab metrics={analysis.risk_metrics} t={t} />
            ) : null}
            {activeTab === "stress" ? (
              <StressTab
                scenarios={analysis.stress_tests}
                currency={baseCurrency}
                t={t}
              />
            ) : null}
            {activeTab === "contribution" ? (
              <ContributionTab
                contribution={analysis.risk_contribution}
                t={t}
              />
            ) : null}
            {activeTab === "benchmark" ? (
              <BenchmarkTab benchmark={analysis.benchmark_risk} t={t} />
            ) : null}
            {activeTab === "commentary" ? (
              <CommentaryTab analysis={analysis} t={t} />
            ) : null}
          </div>
        </>
      ) : null}
    </div>
  );
}

function RiskControlsPanel({
  controls,
  onChange,
  onReset,
  t,
}: {
  controls: RiskControlState;
  onChange: (key: RiskControlKey, value: number) => void;
  onReset: () => void;
  t: (key: string) => string;
}) {
  const limitFields: { key: RiskControlKey; label: string }[] = [
    {
      key: "max_single_position_weight",
      label: t("riskMonitor.assumptions.singlePosition"),
    },
    {
      key: "max_sector_exposure",
      label: t("riskMonitor.assumptions.sector"),
    },
    {
      key: "minimum_cash_reserve",
      label: t("riskMonitor.assumptions.cash"),
    },
    {
      key: "max_portfolio_volatility",
      label: t("riskMonitor.assumptions.volatility"),
    },
    {
      key: "max_tracking_error",
      label: t("riskMonitor.assumptions.trackingError"),
    },
  ];
  const stressFields: { key: RiskControlKey; label: string }[] = [
    {
      key: "equity_market_shock",
      label: t("riskMonitor.assumptions.equityShock"),
    },
    {
      key: "technology_sector_shock",
      label: t("riskMonitor.assumptions.techShock"),
    },
    {
      key: "interest_rate_shock",
      label: t("riskMonitor.assumptions.ratesShock"),
    },
    {
      key: "largest_holding_shock",
      label: t("riskMonitor.assumptions.issuerShock"),
    },
  ];

  return (
    <section className="risk-monitor-controls-panel">
      <div className="risk-monitor-controls-panel__header">
        <div>
          <span>{t("riskMonitor.assumptions.eyebrow")}</span>
          <h2>{t("riskMonitor.assumptions.title")}</h2>
          <p>{t("riskMonitor.assumptions.description")}</p>
        </div>
        <button className="button button--ghost" type="button" onClick={onReset}>
          {t("riskMonitor.assumptions.reset")}
        </button>
      </div>
      <div className="risk-monitor-control-groups">
        <RiskControlGroup
          title={t("riskMonitor.assumptions.limits")}
          fields={limitFields}
          controls={controls}
          onChange={onChange}
        />
        <RiskControlGroup
          title={t("riskMonitor.assumptions.stress")}
          fields={stressFields}
          controls={controls}
          onChange={onChange}
        />
      </div>
    </section>
  );
}

function RiskControlGroup({
  title,
  fields,
  controls,
  onChange,
}: {
  title: string;
  fields: { key: RiskControlKey; label: string }[];
  controls: RiskControlState;
  onChange: (key: RiskControlKey, value: number) => void;
}) {
  return (
    <div className="risk-monitor-control-group">
      <h3>{title}</h3>
      <div className="risk-monitor-control-grid">
        {fields.map((field) => (
          <label className="form-field" key={field.key}>
            <span>{field.label}</span>
            <input
              max={100}
              min={field.key.includes("shock") ? -100 : 0}
              step={1}
              type="number"
              value={Math.round(controls[field.key] * 100)}
              onChange={(event) => {
                const value = Number(event.target.value);
                if (Number.isFinite(value)) {
                  onChange(field.key, value / 100);
                }
              }}
            />
          </label>
        ))}
      </div>
    </div>
  );
}

function RiskMonitorKpis({
  analysis,
  currency,
  t,
}: {
  analysis: RiskMonitorAnalysisResponse;
  currency: string;
  t: (key: string) => string;
}) {
  const metric = metricLookup(analysis.risk_metrics);
  return (
    <div className="risk-monitor-kpi-grid">
      <RiskMetricCard
        title={t("riskMonitor.kpis.score")}
        value={`${analysis.global_risk_score}/100`}
        subtitle={analysis.global_risk_status}
        tone={statusTone(analysis.global_risk_status)}
      />
      <RiskMetricCard
        title={t("riskMonitor.kpis.var")}
        value={formatRiskMetric(metric["VaR 95%"])}
        subtitle={sourceLabel(metric["VaR 95%"]?.source, t)}
      />
      <RiskMetricCard
        title={t("riskMonitor.kpis.cvar")}
        value={formatRiskMetric(metric["CVaR 95%"])}
        subtitle={sourceLabel(metric["CVaR 95%"]?.source, t)}
      />
      <RiskMetricCard
        title={t("riskMonitor.kpis.volatility")}
        value={formatRiskMetric(metric["Portfolio volatility"])}
        subtitle={sourceLabel(metric["Portfolio volatility"]?.source, t)}
      />
      <RiskMetricCard
        title={t("riskMonitor.kpis.drawdown")}
        value={formatRiskMetric(metric["Max drawdown"])}
        subtitle={t("riskMonitor.kpis.maxDrawdown")}
      />
      <RiskMetricCard
        title={t("riskMonitor.kpis.trackingError")}
        value={formatRiskMetric(metric["Tracking error"])}
        subtitle={analysis.benchmark_risk.active_risk_status}
      />
      <RiskMetricCard
        title={t("riskMonitor.kpis.breaches")}
        value={analysis.limit_breaches.length}
        subtitle={t("riskMonitor.kpis.activeBreaches")}
        tone={analysis.limit_breaches.length ? "warning" : "positive"}
      />
      <RiskMetricCard
        title={t("riskMonitor.kpis.totalValue")}
        value={<MoneyValue value={analysis.total_value} currency={currency} />}
        subtitle={analysis.portfolio_name}
      />
    </div>
  );
}

function OverviewTab({
  analysis,
  currency,
  t,
}: {
  analysis: RiskMonitorAnalysisResponse;
  currency: string;
  t: (key: string) => string;
}) {
  return (
    <div className="risk-monitor-stack">
      <RiskSectionCard
        title={t("riskMonitor.sections.surveillance")}
        description={analysis.athena_commentary.summary}
        badges={[
          {
            label: analysis.global_risk_status,
            variant: statusBadgeVariant(analysis.global_risk_status),
          },
        ]}
      >
        <div className="risk-monitor-overview-grid">
          <RiskDataSourcePanel source={analysis.risk_source} t={t} />
          <div className="risk-monitor-driver-list">
            <h3>{t("riskMonitor.sections.mainDrivers")}</h3>
            {analysis.main_drivers.map((driver) => (
              <p key={driver}>{driver}</p>
            ))}
          </div>
        </div>
      </RiskSectionCard>

      <IntegrationStatusPanel statuses={analysis.integration_statuses} t={t} />

      <div className="risk-monitor-two-column">
        <RiskSectionCard
          title={t("riskMonitor.sections.concentration")}
          description={t("riskMonitor.sections.concentrationDescription")}
        >
          <div className="risk-monitor-mini-grid">
            <RiskMetricCard
              title={t("riskMonitor.concentration.largest")}
              value={analysis.concentration.largest_position?.name ?? "-"}
              subtitle={
                analysis.concentration.largest_position ? (
                  <PercentValue
                    value={analysis.concentration.largest_position.weight}
                  />
                ) : (
                  t("common.unavailable")
                )
              }
            />
            <RiskMetricCard
              title={t("riskMonitor.concentration.topThree")}
              value={<PercentValue value={analysis.concentration.top_3_weight} />}
              subtitle={t("riskMonitor.concentration.topThreeLimit")}
            />
            <RiskMetricCard
              title={t("riskMonitor.concentration.cash")}
              value={<PercentValue value={analysis.concentration.cash_weight} />}
              subtitle={t("riskMonitor.concentration.cashLimit")}
            />
          </div>
          <ExposureList exposures={analysis.concentration.sector_exposures} />
        </RiskSectionCard>

        <RiskSectionCard
          title={t("riskMonitor.sections.alerts")}
          description={t("riskMonitor.sections.alertsDescription")}
        >
          <div className="risk-monitor-alert-grid">
            {analysis.alerts.map((alert) => (
              <article
                className={`risk-monitor-alert risk-monitor-alert--${alert.severity}`}
                key={`${alert.title}-${alert.message}`}
              >
                <div>
                  <strong>{alert.title}</strong>
                  <RiskStatusBadge
                    label={severityLabel(alert.severity, t)}
                    variant={severityVariant(alert.severity)}
                  />
                </div>
                <p>{alert.message}</p>
                <small>{alert.suggested_action}</small>
              </article>
            ))}
          </div>
        </RiskSectionCard>
      </div>
    </div>
  );
}

function LimitsTab({
  breaches,
  t,
}: {
  breaches: RiskLimitBreach[];
  t: (key: string) => string;
}) {
  return (
    <RiskSectionCard
      title={t("riskMonitor.sections.limits")}
      description={t("riskMonitor.sections.limitsDescription")}
    >
      {breaches.length ? (
        <div className="risk-monitor-breach-grid">
          {breaches.map((breach) => (
            <article
              className={`risk-monitor-breach risk-monitor-breach--${breach.severity}`}
              key={`${breach.rule_name}-${breach.current_value}`}
            >
              <div>
                <strong>{breach.rule_name}</strong>
                <RiskStatusBadge
                  label={severityLabel(breach.severity, t)}
                  variant={severityVariant(breach.severity)}
                />
              </div>
              <p>{breach.explanation}</p>
              <dl>
                <div>
                  <dt>{t("riskMonitor.limits.current")}</dt>
                  <dd><PercentValue value={breach.current_value} /></dd>
                </div>
                <div>
                  <dt>{t("riskMonitor.limits.limit")}</dt>
                  <dd><PercentValue value={breach.limit_value} /></dd>
                </div>
              </dl>
              <small>{breach.suggested_action}</small>
            </article>
          ))}
        </div>
      ) : (
        <EmptyState
          title={t("riskMonitor.limits.noBreaches")}
          message={t("riskMonitor.limits.noBreachesMessage")}
        />
      )}
    </RiskSectionCard>
  );
}

function MetricsTab({
  metrics,
  t,
}: {
  metrics: RiskMetric[];
  t: (key: string) => string;
}) {
  return (
    <RiskSectionCard
      title={t("riskMonitor.sections.metrics")}
      description={t("riskMonitor.sections.metricsDescription")}
    >
      <div className="table-scroll">
        <table className="data-table risk-monitor-table">
          <thead>
            <tr>
              <th>{t("riskMonitor.table.metric")}</th>
              <th>{t("riskMonitor.table.value")}</th>
              <th>{t("riskMonitor.table.source")}</th>
              <th>{t("riskMonitor.table.description")}</th>
            </tr>
          </thead>
          <tbody>
            {metrics.map((metric) => (
              <tr key={metric.name}>
                <td className="data-table__symbol">{metric.name}</td>
                <td className="data-table__numeric">{formatRiskMetric(metric)}</td>
                <td>{sourceLabel(metric.source, t)}</td>
                <td>{metric.description}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </RiskSectionCard>
  );
}

function StressTab({
  scenarios,
  currency,
  t,
}: {
  scenarios: StressScenarioResult[];
  currency: string;
  t: (key: string) => string;
}) {
  return (
    <RiskSectionCard
      title={t("riskMonitor.sections.stress")}
      description={t("riskMonitor.sections.stressDescription")}
    >
      <div className="table-scroll">
        <table className="data-table risk-monitor-table">
          <thead>
            <tr>
              <th>{t("riskMonitor.table.scenario")}</th>
              <th>{t("riskMonitor.table.impact")}</th>
              <th>{t("riskMonitor.table.loss")}</th>
              <th>{t("riskMonitor.table.affected")}</th>
              <th>{t("riskMonitor.table.severity")}</th>
            </tr>
          </thead>
          <tbody>
            {scenarios.map((scenario) => (
              <tr key={scenario.name}>
                <td>
                  <strong>{scenario.name}</strong>
                  <p className="risk-monitor-table-note">{scenario.explanation}</p>
                </td>
                <td className="data-table__numeric negative-value">
                  <PercentValue value={scenario.estimated_impact_percent} />
                </td>
                <td className="data-table__numeric">
                  <MoneyValue value={scenario.estimated_loss} currency={currency} />
                </td>
                <td>{scenario.most_affected_holdings.join(", ") || "-"}</td>
                <td>
                  <RiskStatusBadge
                    label={severityLabel(scenario.severity, t)}
                    variant={severityVariant(scenario.severity)}
                  />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </RiskSectionCard>
  );
}

function ContributionTab({
  contribution,
  t,
}: {
  contribution: RiskContributionResponse;
  t: (key: string) => string;
}) {
  return (
    <div className="risk-monitor-two-column">
      <RiskSectionCard
        title={t("riskMonitor.sections.contribution")}
        description={contribution.method}
        badges={[
          {
            label: sourceLabel(contribution.contribution_source, t),
            variant:
              contribution.contribution_source === "realized_market_data"
                ? "success"
                : "warning",
          },
        ]}
      >
        <ContributionList items={contribution.by_asset} />
        {contribution.diversification_warning ? (
          <p className="risk-monitor-callout">
            {contribution.diversification_warning}
          </p>
        ) : null}
      </RiskSectionCard>

      <RiskSectionCard
        title={t("riskMonitor.sections.sectorContribution")}
        description={t("riskMonitor.sections.sectorContributionDescription")}
      >
        <ContributionList items={contribution.by_sector} />
      </RiskSectionCard>
    </div>
  );
}

function BenchmarkTab({
  benchmark,
  t,
}: {
  benchmark: BenchmarkRiskResponse;
  t: (key: string) => string;
}) {
  return (
    <RiskSectionCard
      title={t("riskMonitor.sections.benchmark")}
      description={benchmark.active_risk_status}
      badges={benchmark.badges.map((badge) => ({
        label: translateSourceBadge(badge, t),
        variant: sourceBadgeVariant(badge),
      }))}
    >
      <div className="risk-monitor-mini-grid">
        <RiskMetricCard
          title={t("riskMonitor.benchmark.symbol")}
          value={benchmark.benchmark_symbol}
        />
        <RiskMetricCard
          title={t("riskMonitor.benchmark.beta")}
          value={benchmark.beta === null ? "-" : benchmark.beta.toFixed(2)}
        />
        <RiskMetricCard
          title={t("riskMonitor.benchmark.activeExposure")}
          value={<PercentValue value={benchmark.active_exposure} />}
        />
        <RiskMetricCard
          title={t("riskMonitor.benchmark.trackingError")}
          value={
            benchmark.tracking_error === null ? (
              t("common.unavailable")
            ) : (
              <PercentValue value={benchmark.tracking_error} />
            )
          }
        />
        <RiskMetricCard
          title={t("riskMonitor.benchmark.informationRatio")}
          value={
            benchmark.information_ratio === null
              ? t("common.unavailable")
              : benchmark.information_ratio.toFixed(3)
          }
        />
      </div>
      <div className="risk-monitor-note-list">
        {benchmark.warnings.map((warning) => (
          <p key={warning}>{warning}</p>
        ))}
      </div>
    </RiskSectionCard>
  );
}

function CommentaryTab({
  analysis,
  t,
}: {
  analysis: RiskMonitorAnalysisResponse;
  t: (key: string) => string;
}) {
  return (
    <div className="risk-monitor-stack">
      <AthenaAICommentaryCard commentary={analysis.athena_ai_commentary} />
      <RiskSectionCard
        title={t("riskMonitor.sections.commentary")}
        description={analysis.athena_commentary.summary}
        badges={[{ label: t("riskMonitor.badges.deterministic"), variant: "info" }]}
      >
        <div className="risk-monitor-commentary-grid">
          <div>
            <h3>{t("riskMonitor.sections.mainDrivers")}</h3>
            <ul>
              {analysis.athena_commentary.main_drivers.map((driver) => (
                <li key={driver}>{driver}</li>
              ))}
            </ul>
          </div>
          <div>
            <h3>{t("riskMonitor.sections.nextActions")}</h3>
            <ul>
              {analysis.athena_commentary.suggested_actions.map((action) => (
                <li key={action}>{action}</li>
              ))}
            </ul>
          </div>
        </div>
      </RiskSectionCard>
    </div>
  );
}

function RiskDataSourcePanel({
  source,
  t,
}: {
  source: RiskSourceMetadata;
  t: (key: string) => string;
}) {
  return (
    <div className="risk-monitor-data-source">
      <div>
        <span>{t("riskMonitor.dataSource.source")}</span>
        <strong>{sourceLabel(source.metric_source, t)}</strong>
      </div>
      <div>
        <span>{t("riskMonitor.dataSource.observations")}</span>
        <strong>{source.observations.toLocaleString()}</strong>
      </div>
      <div>
        <span>{t("riskMonitor.dataSource.missingSymbols")}</span>
        <strong>
          {source.symbols_missing.length
            ? source.symbols_missing.join(", ")
            : t("riskMonitor.dataSource.none")}
        </strong>
      </div>
      <div>
        <span>{t("riskMonitor.dataSource.fallback")}</span>
        <strong>
          {source.fallback_used
            ? t("riskMonitor.dataSource.yes")
            : t("riskMonitor.dataSource.no")}
        </strong>
      </div>
      <p>{t("riskMonitor.dataSource.explanation")}</p>
    </div>
  );
}

function IntegrationStatusPanel({
  statuses,
  t,
}: {
  statuses: ModuleIntegrationStatus[];
  t: (key: string) => string;
}) {
  if (!statuses.length) {
    return null;
  }

  return (
    <RiskSectionCard
      title={t("riskMonitor.sections.integrationStatus")}
      description={t("riskMonitor.sections.integrationStatusDescription")}
    >
      <div className="risk-monitor-mini-grid">
        {statuses.map((status) => (
          <article className="risk-monitor-driver-list" key={status.module}>
            <div className="risk-monitor-badge-cluster">
              <RiskStatusBadge
                label={status.status}
                variant={integrationStatusVariant(status)}
              />
              <RiskStatusBadge
                label={
                  status.payload_available
                    ? t("common.payloadAvailable")
                    : t("common.requiresData")
                }
                variant={status.payload_available ? "success" : "warning"}
              />
            </div>
            <h3>{status.module}</h3>
            <p>
              {t("common.dataSource")}: {sourceLabel(status.data_source, t)}
            </p>
            {status.generated_at ? (
              <p>
                {t("common.generatedAt")}:{" "}
                {new Date(status.generated_at).toLocaleString()}
              </p>
            ) : null}
            {status.required_data.length ? (
              <p>
                {t("common.missingData")}: {status.required_data.join(", ")}
              </p>
            ) : null}
            {status.warnings.slice(0, 2).map((warning) => (
              <p key={warning}>{warning}</p>
            ))}
          </article>
        ))}
      </div>
    </RiskSectionCard>
  );
}

function RiskSectionCard({
  title,
  description,
  badges,
  children,
}: {
  title: string;
  description?: string;
  badges?: { label: string; variant?: BadgeVariant }[];
  children: ReactNode;
}) {
  return (
    <section className="risk-monitor-section-card">
      <div className="risk-monitor-section-card__header">
        <div>
          <h2>{title}</h2>
          {description ? <p>{description}</p> : null}
        </div>
        {badges?.length ? (
          <div className="risk-monitor-badge-cluster">
            {badges.map((badge) => (
              <RiskStatusBadge
                key={badge.label}
                label={badge.label}
                variant={badge.variant}
              />
            ))}
          </div>
        ) : null}
      </div>
      {children}
    </section>
  );
}

function RiskMetricCard({
  title,
  value,
  subtitle,
  tone = "neutral",
}: {
  title: string;
  value: ReactNode;
  subtitle?: ReactNode;
  tone?: "neutral" | "positive" | "warning" | "negative";
}) {
  return (
    <article className={`risk-monitor-metric-card risk-monitor-metric-card--${tone}`}>
      <span>{title}</span>
      <strong>{value}</strong>
      {subtitle ? <p>{subtitle}</p> : null}
    </article>
  );
}

function ExposureList({ exposures }: { exposures: { name: string; weight: number; status: string }[] }) {
  return (
    <div className="risk-monitor-exposure-list">
      {exposures.slice(0, 5).map((exposure) => (
        <div key={exposure.name}>
          <span>{exposure.name}</span>
          <strong><PercentValue value={exposure.weight} /></strong>
        </div>
      ))}
    </div>
  );
}

function ContributionList({
  items,
}: {
  items: { name: string; weight: number; contribution_percent: number }[];
}) {
  return (
    <div className="risk-monitor-contribution-list">
      {items.map((item) => (
        <div key={item.name}>
          <span>{item.name}</span>
          <div>
            <strong><PercentValue value={item.contribution_percent} /></strong>
            <small><PercentValue value={item.weight} /></small>
          </div>
        </div>
      ))}
    </div>
  );
}

function metricLookup(metrics: RiskMetric[]) {
  return metrics.reduce<Record<string, RiskMetric>>((lookup, metric) => {
    lookup[metric.name] = metric;
    return lookup;
  }, {});
}

function buildLimitOverrides(controls: RiskControlState): RiskLimitOverrides {
  return {
    max_single_position_weight: controls.max_single_position_weight,
    max_sector_exposure: controls.max_sector_exposure,
    minimum_cash_reserve: controls.minimum_cash_reserve,
    max_portfolio_volatility: controls.max_portfolio_volatility,
    max_tracking_error: controls.max_tracking_error,
  };
}

function buildStressShockOverrides(
  controls: RiskControlState,
): StressShockOverrides {
  return {
    equity_market_shock: controls.equity_market_shock,
    technology_sector_shock: controls.technology_sector_shock,
    interest_rate_shock: controls.interest_rate_shock,
    largest_holding_shock: controls.largest_holding_shock,
  };
}

function formatRiskMetric(metric?: RiskMetric) {
  if (!metric || metric.value === null) {
    return "--";
  }
  if (
    metric.name.includes("ratio") ||
    metric.name === "Beta" ||
    metric.name === "Information ratio"
  ) {
    return metric.value.toFixed(3);
  }
  return <PercentValue value={metric.value} />;
}

function sourceLabel(source: string | undefined, t: (key: string) => string) {
  if (source === "realized_market_data") {
    return t("riskMonitor.badges.realized");
  }
  if (source === "deterministic_demo") {
    return t("riskMonitor.badges.demo");
  }
  if (source === "partial_data") {
    return t("riskMonitor.badges.partialData");
  }
  if (source === "rates_lab" || source === "rates_lab_payload") {
    return t("common.ratesLabConnected");
  }
  if (
    source === "options_pricing_lab" ||
    source === "options_pricing_payload"
  ) {
    return t("common.optionsPricingConnected");
  }
  if (source === "volatility_lab" || source === "volatility_lab_payload") {
    return t("common.volatilityLabConnected");
  }
  if (source === "trade_simulator") {
    return t("common.tradeSimulatorReady");
  }
  if (source === "portfolio_builder") {
    return t("common.portfolioBuilderConnected");
  }
  if (source === "market_data") {
    return t("common.marketDataConnected");
  }
  return t("riskMonitor.badges.placeholder");
}

function translateSourceBadge(label: string, t: (key: string) => string) {
  const normalized = label.toLowerCase();
  if (normalized.includes("realized")) return t("riskMonitor.badges.realized");
  if (normalized.includes("demo")) return t("riskMonitor.badges.demo");
  if (normalized.includes("partial")) return t("riskMonitor.badges.partialData");
  if (normalized.includes("history")) return t("riskMonitor.badges.benchmarkHistory");
  if (normalized.includes("constituent")) return t("riskMonitor.badges.benchmarkFeed");
  if (normalized.includes("market data")) return t("riskMonitor.badges.requiresMarketData");
  return label;
}

function sourceBadgeVariant(label: string): BadgeVariant {
  const normalized = label.toLowerCase();
  if (normalized.includes("realized")) return "success";
  if (
    normalized.includes("demo") ||
    normalized.includes("partial") ||
    normalized.includes("requires")
  ) {
    return "warning";
  }
  return "info";
}

function severityLabel(severity: string, t: (key: string) => string) {
  return t(`riskMonitor.severity.${severity}`);
}

function severityVariant(severity: string): BadgeVariant {
  if (severity === "critical" || severity === "high") return "danger";
  if (severity === "medium") return "warning";
  return "info";
}

function integrationStatusVariant(status: ModuleIntegrationStatus): BadgeVariant {
  const normalized = status.status.toLowerCase();
  if (status.payload_available || normalized.includes("connected")) return "success";
  if (status.required_data.length || normalized.includes("fallback")) return "warning";
  return "info";
}

function readVolatilityPayload(): RiskMonitorPayload | null {
  if (typeof window === "undefined") {
    return null;
  }
  try {
    const stored = window.sessionStorage.getItem(VOLATILITY_PAYLOAD_STORAGE_KEY);
    return stored ? (JSON.parse(stored) as RiskMonitorPayload) : null;
  } catch {
    return null;
  }
}

function statusBadgeVariant(status: string): BadgeVariant {
  if (status.includes("Critical") || status.includes("High")) return "danger";
  if (status.includes("Elevated")) return "warning";
  if (status.includes("Moderate")) return "info";
  return "success";
}

function statusTone(status: string): "neutral" | "positive" | "warning" | "negative" {
  if (status.includes("Critical") || status.includes("High")) return "negative";
  if (status.includes("Elevated")) return "warning";
  if (status.includes("Low")) return "positive";
  return "neutral";
}
