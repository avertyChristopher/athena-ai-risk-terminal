import { useMemo, useState } from "react";
import type { ReactNode } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";

import { AthenaAICommentaryCard } from "../../../components/ai/AthenaAICommentaryCard";
import { MoneyValue } from "../../../components/finance/MoneyValue";
import { PercentValue } from "../../../components/finance/PercentValue";
import { PageHeader } from "../../../components/layout/PageHeader";
import { EmptyState } from "../../../components/ui/EmptyState";
import { ErrorBanner } from "../../../components/ui/ErrorBanner";
import { LoadingState } from "../../../components/ui/LoadingState";
import { StatusBadge } from "../../../components/ui/StatusBadge";
import { apiClient } from "../../../lib/api-client";
import { endpoints } from "../../../lib/endpoints";
import { pnlAttributionApi } from "../../../services/pnlAttributionApi";
import type { PortfolioListResponse } from "../../../types/portfolio";
import type {
  AttributionMethod,
  GroupPnlContribution,
  PnlAttributionResult,
  PositionPnlContribution,
} from "../../../types/pnl-attribution";
import { useTranslation } from "../../../hooks/useTranslation";

type PnlTab =
  | "overview"
  | "positions"
  | "groups"
  | "realized"
  | "benchmark"
  | "rates"
  | "options"
  | "trades"
  | "methodology"
  | "commentary";

const tabs: PnlTab[] = [
  "overview",
  "positions",
  "groups",
  "realized",
  "benchmark",
  "rates",
  "options",
  "trades",
  "methodology",
  "commentary",
];

export function PnlAttributionPage() {
  const { i18n, t } = useTranslation();
  const [activeTab, setActiveTab] = useState<PnlTab>("overview");
  const [portfolioId, setPortfolioId] = useState("pf_001");
  const [startDate, setStartDate] = useState("2026-05-13");
  const [endDate, setEndDate] = useState("2026-06-03");
  const [benchmarkSymbol, setBenchmarkSymbol] = useState("SPY");
  const [method, setMethod] = useState<AttributionMethod>("contribution");
  const [includeIncome, setIncludeIncome] = useState(true);
  const [includeFx, setIncludeFx] = useState(true);
  const [includeTrades, setIncludeTrades] = useState(true);
  const [includeRates, setIncludeRates] = useState(true);
  const [includeOptions, setIncludeOptions] = useState(true);
  const [analysis, setAnalysis] = useState<PnlAttributionResult | null>(null);
  const [csvPreview, setCsvPreview] = useState("");

  const statusQuery = useQuery({
    queryKey: ["pnl-attribution-status"],
    queryFn: pnlAttributionApi.status,
  });
  const historyQuery = useQuery({
    queryKey: ["pnl-attribution-history"],
    queryFn: pnlAttributionApi.history,
  });
  const portfolioQuery = useQuery({
    queryKey: ["pnl-attribution-portfolios"],
    queryFn: () => apiClient.get<PortfolioListResponse>(endpoints.portfolios),
  });

  const analyzeMutation = useMutation({
    mutationFn: () =>
      pnlAttributionApi.analyze({
        portfolio_id: portfolioId,
        start_date: startDate,
        end_date: endDate,
        benchmark_symbol: benchmarkSymbol.trim().toUpperCase() || "SPY",
        attribution_method: method,
        include_income: includeIncome,
        include_fx: includeFx,
        include_trades: includeTrades,
        include_rates: includeRates,
        include_options: includeOptions,
        language: i18n.language.startsWith("fr") ? "fr" : "en",
      }),
    onSuccess: (result) => {
      setAnalysis(result);
      setActiveTab("overview");
      setCsvPreview("");
      void historyQuery.refetch();
    },
  });

  const isLoading = statusQuery.isLoading || portfolioQuery.isLoading;
  const hasError = statusQuery.isError || portfolioQuery.isError || analyzeMutation.isError;
  const currency = "USD";
  const kpis = useMemo(() => buildKpis(analysis, t), [analysis, t]);

  function resetControls() {
    setPortfolioId("pf_001");
    setStartDate("2026-05-13");
    setEndDate("2026-06-03");
    setBenchmarkSymbol("SPY");
    setMethod("contribution");
    setIncludeIncome(true);
    setIncludeFx(true);
    setIncludeTrades(true);
    setIncludeRates(true);
    setIncludeOptions(true);
    setCsvPreview("");
    setActiveTab("overview");
  }

  async function exportCsv() {
    if (!analysis) return;
    const payload = await pnlAttributionApi.exportCsv(analysis.analysis_id);
    setCsvPreview(payload.csv);
    setActiveTab("methodology");
  }

  return (
    <div className="page pnl-attribution-page risk-monitor-page">
      <PageHeader
        title={t("pnlAttribution.title")}
        subtitle={t("pnlAttribution.subtitle")}
      />

      <section className="risk-monitor-command-panel pnl-command-panel">
        <div>
          <span>{t("pnlAttribution.eyebrow")}</span>
          <h2>{t("pnlAttribution.workbenchTitle")}</h2>
          <p>{t("pnlAttribution.workbenchDescription")}</p>
        </div>
        <div className="risk-monitor-badge-cluster">
          <StatusBadge
            label={statusQuery.data?.status ?? t("common.loading")}
            variant={statusQuery.data?.status === "ready" ? "success" : "warning"}
          />
          <StatusBadge label={t("pnlAttribution.badges.performanceAttribution")} variant="info" />
          <StatusBadge label={t("pnlAttribution.badges.portfolioConnected")} variant="success" />
          <StatusBadge label={t("pnlAttribution.badges.reportsReady")} variant="success" />
          <StatusBadge label={t("pnlAttribution.badges.beta")} variant="warning" />
        </div>
      </section>

      <section className="pnl-control-card">
        <div className="pnl-control-grid">
          <label className="form-field">
            <span>{t("workflow.portfolio")}</span>
            <select value={portfolioId} onChange={(event) => setPortfolioId(event.target.value)}>
              {(portfolioQuery.data?.items ?? []).map((portfolio) => (
                <option key={portfolio.id} value={portfolio.id}>
                  {portfolio.name}
                </option>
              ))}
            </select>
          </label>
          <label className="form-field">
            <span>{t("pnlAttribution.startDate")}</span>
            <input value={startDate} type="date" onChange={(event) => setStartDate(event.target.value)} />
          </label>
          <label className="form-field">
            <span>{t("pnlAttribution.endDate")}</span>
            <input value={endDate} type="date" onChange={(event) => setEndDate(event.target.value)} />
          </label>
          <label className="form-field">
            <span>{t("workflow.benchmark")}</span>
            <input value={benchmarkSymbol} onChange={(event) => setBenchmarkSymbol(event.target.value)} />
          </label>
          <label className="form-field">
            <span>{t("pnlAttribution.attributionMethod")}</span>
            <select value={method} onChange={(event) => setMethod(event.target.value as AttributionMethod)}>
              <option value="contribution">{t("pnlAttribution.methods.contribution")}</option>
              <option value="simple">{t("pnlAttribution.methods.simple")}</option>
              <option value="Brinson-lite">{t("pnlAttribution.methods.brinsonLite")}</option>
            </select>
          </label>
          <div className="pnl-control-actions">
            <button
              className="button button-primary"
              disabled={analyzeMutation.isPending}
              type="button"
              onClick={() => analyzeMutation.mutate()}
            >
              {analyzeMutation.isPending ? t("common.loading") : t("pnlAttribution.analyze")}
            </button>
            <button className="button button-secondary" type="button" onClick={resetControls}>
              {t("pnlAttribution.reset")}
            </button>
            <button className="button button-secondary" disabled={!analysis} type="button" onClick={() => void exportCsv()}>
              {t("pnlAttribution.exportCsv")}
            </button>
          </div>
        </div>
        <div className="pnl-toggle-row">
          {[
            [includeIncome, setIncludeIncome, t("pnlAttribution.includeIncome")],
            [includeFx, setIncludeFx, t("pnlAttribution.includeFx")],
            [includeTrades, setIncludeTrades, t("pnlAttribution.includeTrades")],
            [includeRates, setIncludeRates, t("pnlAttribution.includeRates")],
            [includeOptions, setIncludeOptions, t("pnlAttribution.includeOptions")],
          ].map(([checked, setter, label]) => (
            <label className="pnl-toggle" key={String(label)}>
              <input
                checked={Boolean(checked)}
                type="checkbox"
                onChange={(event) => (setter as (value: boolean) => void)(event.target.checked)}
              />
              <span>{label as string}</span>
            </label>
          ))}
        </div>
      </section>

      {hasError ? (
        <ErrorBanner
          title={t("pnlAttribution.apiError")}
          message={t("pnlAttribution.apiErrorDetail")}
        />
      ) : null}

      {isLoading ? <LoadingState label={t("common.loading")} /> : null}

      <section className="risk-monitor-kpi-grid pnl-kpi-grid">
        {kpis.map(([label, value, tone]) => (
          <PnlMetricCard
            key={label}
            label={label}
            value={value}
            tone={tone}
          />
        ))}
      </section>

      <nav className="risk-monitor-tabs pnl-tabs" aria-label={t("pnlAttribution.tabsLabel")}>
        {tabs.map((tab) => (
          <button
            key={tab}
            className={`risk-monitor-tab ${activeTab === tab ? "risk-monitor-tab--active" : ""}`}
            type="button"
            onClick={() => setActiveTab(tab)}
          >
            <span>{t(`pnlAttribution.tabs.${tab}`)}</span>
          </button>
        ))}
      </nav>

      {!analysis ? (
        <EmptyState
          title={t("pnlAttribution.emptyTitle")}
          message={t("pnlAttribution.emptyMessage")}
        />
      ) : null}

      {analysis && activeTab === "overview" ? (
        <OverviewTab analysis={analysis} currency={currency} t={t} />
      ) : null}
      {analysis && activeTab === "positions" ? (
        <PositionTab rows={analysis.position_contributions} currency={currency} t={t} />
      ) : null}
      {analysis && activeTab === "groups" ? (
        <GroupsTab analysis={analysis} currency={currency} t={t} />
      ) : null}
      {analysis && activeTab === "realized" ? (
        <RealizedTab analysis={analysis} currency={currency} t={t} />
      ) : null}
      {analysis && activeTab === "benchmark" ? (
        <BenchmarkTab analysis={analysis} t={t} />
      ) : null}
      {analysis && activeTab === "rates" ? (
        <RatesTab analysis={analysis} currency={currency} t={t} />
      ) : null}
      {analysis && activeTab === "options" ? (
        <OptionsTab analysis={analysis} currency={currency} t={t} />
      ) : null}
      {analysis && activeTab === "trades" ? (
        <TradesTab analysis={analysis} currency={currency} t={t} />
      ) : null}
      {analysis && activeTab === "methodology" ? (
        <MethodologyTab analysis={analysis} csvPreview={csvPreview} t={t} />
      ) : null}
      {analysis && activeTab === "commentary" ? (
        <AthenaAICommentaryCard
          commentary={analysis.athena_ai_commentary}
          title={t("pnlAttribution.athenaCommentary")}
        />
      ) : null}
    </div>
  );
}

function OverviewTab({
  analysis,
  currency,
  t,
}: {
  analysis: PnlAttributionResult;
  currency: string;
  t: (key: string) => string;
}) {
  const topWinner = analysis.top_winners[0];
  const topLoser = analysis.top_losers[0];
  return (
    <section className="risk-monitor-panel pnl-overview-grid">
      <article className="risk-monitor-section-card">
        <header className="risk-monitor-section-card__header">
          <h2>{t("pnlAttribution.executiveSummary")}</h2>
          <p>{analysis.athena_ai_commentary?.summary ?? t("pnlAttribution.noCommentary")}</p>
        </header>
        <div className="pnl-definition-grid">
          <Definition label={t("workflow.portfolio")} value={analysis.portfolio_name} />
          <Definition label={t("pnlAttribution.period")} value={`${analysis.period.start_date} - ${analysis.period.end_date}`} />
          <Definition label={t("pnlAttribution.totalPnl")} value={<MoneyValue value={analysis.total_pnl} currency={currency} />} />
          <Definition label={t("pnlAttribution.totalReturn")} value={<PercentValue value={analysis.total_pnl_percent} />} />
          <Definition label={t("pnlAttribution.topContributor")} value={topWinner ? `${topWinner.symbol} (${formatMoney(topWinner.total_pnl)})` : t("common.unavailable")} />
          <Definition label={t("pnlAttribution.worstContributor")} value={topLoser ? `${topLoser.symbol} (${formatMoney(topLoser.total_pnl)})` : t("common.unavailable")} />
        </div>
      </article>
      <article className="risk-monitor-section-card">
        <header className="risk-monitor-section-card__header">
          <h2>{t("pnlAttribution.mainDrivers")}</h2>
          <p>{t("pnlAttribution.mainDriversDescription")}</p>
        </header>
        <div className="risk-monitor-contribution-list">
          {analysis.top_winners.slice(0, 5).map((row) => (
            <ContributionRow key={row.symbol} label={row.symbol} value={row.total_pnl} percent={row.contribution_to_portfolio_return} />
          ))}
        </div>
      </article>
    </section>
  );
}

function PositionTab({
  rows,
  currency,
  t,
}: {
  rows: PositionPnlContribution[];
  currency: string;
  t: (key: string) => string;
}) {
  return (
    <section className="risk-monitor-section-card">
      <header className="risk-monitor-section-card__header">
        <h2>{t("pnlAttribution.positionPnl")}</h2>
        <p>{t("pnlAttribution.positionDescription")}</p>
      </header>
      <div className="pnl-table">
        <table>
          <thead>
            <tr>
              <th>{t("workflow.symbol")}</th>
              <th>{t("workflow.assetType")}</th>
              <th>{t("pnlAttribution.startingValue")}</th>
              <th>{t("pnlAttribution.endingValue")}</th>
              <th>{t("pnlAttribution.pricePnl")}</th>
              <th>{t("pnlAttribution.incomePnl")}</th>
              <th>{t("pnlAttribution.totalPnl")}</th>
              <th>{t("pnlAttribution.contributionToReturn")}</th>
              <th>{t("common.dataSource")}</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.symbol}>
                <td><strong>{row.symbol}</strong><span>{row.name}</span></td>
                <td>{row.asset_class}</td>
                <td><MoneyValue value={row.starting_value} currency={currency} /></td>
                <td><MoneyValue value={row.ending_value} currency={currency} /></td>
                <td className={toneClass(row.price_pnl)}><MoneyValue value={row.price_pnl} currency={currency} /></td>
                <td><MoneyValue value={row.income_pnl} currency={currency} /></td>
                <td className={toneClass(row.total_pnl)}><MoneyValue value={row.total_pnl} currency={currency} /></td>
                <td><PercentValue value={row.contribution_to_portfolio_return} /></td>
                <td>{row.data_source}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function GroupsTab({
  analysis,
  currency,
  t,
}: {
  analysis: PnlAttributionResult;
  currency: string;
  t: (key: string) => string;
}) {
  return (
    <section className="pnl-three-grid">
      <GroupPanel title={t("pnlAttribution.assetClassAttribution")} rows={analysis.asset_class_contributions} currency={currency} />
      <GroupPanel title={t("pnlAttribution.sectorAttribution")} rows={analysis.sector_contributions} currency={currency} />
      <GroupPanel title={t("pnlAttribution.currencyAttribution")} rows={analysis.currency_contributions} currency={currency} />
    </section>
  );
}

function RealizedTab({ analysis, currency, t }: { analysis: PnlAttributionResult; currency: string; t: (key: string) => string }) {
  return (
    <section className="risk-monitor-section-card">
      <header className="risk-monitor-section-card__header">
        <h2>{t("pnlAttribution.realizedVsUnrealized")}</h2>
        <p>{t("pnlAttribution.realizedDescription")}</p>
      </header>
      <div className="pnl-definition-grid">
        <Definition label={t("pnlAttribution.realizedPnl")} value={<MoneyValue value={analysis.realized_pnl} currency={currency} />} />
        <Definition label={t("pnlAttribution.unrealizedPnl")} value={<MoneyValue value={analysis.unrealized_pnl} currency={currency} />} />
        <Definition label={t("pnlAttribution.income")} value={<MoneyValue value={analysis.income_pnl} currency={currency} />} />
        <Definition label={t("pnlAttribution.feesCosts")} value={<MoneyValue value={analysis.fees_and_costs} currency={currency} />} />
        <Definition label={t("pnlAttribution.fxPnl")} value={<MoneyValue value={analysis.fx_pnl} currency={currency} />} />
      </div>
    </section>
  );
}

function BenchmarkTab({ analysis, t }: { analysis: PnlAttributionResult; t: (key: string) => string }) {
  const benchmark = analysis.benchmark_comparison;
  return (
    <section className="risk-monitor-section-card">
      <header className="risk-monitor-section-card__header">
        <h2>{t("pnlAttribution.benchmarkComparison")}</h2>
        <p>{benchmark.tracking_note}</p>
      </header>
      <div className="pnl-definition-grid">
        <Definition label={t("pnlAttribution.portfolioReturn")} value={<PercentValue value={benchmark.portfolio_return} />} />
        <Definition label={benchmark.benchmark_symbol} value={benchmark.benchmark_return === null ? t("common.unavailable") : <PercentValue value={benchmark.benchmark_return} />} />
        <Definition label={t("pnlAttribution.activeReturn")} value={benchmark.active_return === null ? t("common.unavailable") : <PercentValue value={benchmark.active_return} />} />
        <Definition label={t("pnlAttribution.relativePerformance")} value={benchmark.relative_performance} />
        <Definition label={t("pnlAttribution.allocationEffect")} value={benchmark.allocation_effect === null ? t("common.unavailable") : <PercentValue value={benchmark.allocation_effect} />} />
        <Definition label={t("pnlAttribution.selectionEffect")} value={benchmark.selection_effect === null ? t("common.unavailable") : <PercentValue value={benchmark.selection_effect} />} />
      </div>
    </section>
  );
}

function RatesTab({ analysis, currency, t }: { analysis: PnlAttributionResult; currency: string; t: (key: string) => string }) {
  return (
    <section className="risk-monitor-section-card">
      <header className="risk-monitor-section-card__header">
        <h2>{t("pnlAttribution.fixedIncomePnl")}</h2>
        <p>{t("pnlAttribution.ratesDescription")}</p>
      </header>
      {analysis.fixed_income_effects.length ? (
        <div className="pnl-table">
          <table>
            <thead>
              <tr>
                <th>{t("workflow.symbol")}</th>
                <th>{t("pnlAttribution.durationEffect")}</th>
                <th>{t("pnlAttribution.convexityEffect")}</th>
                <th>{t("pnlAttribution.couponIncome")}</th>
                <th>{t("pnlAttribution.rateShock")}</th>
                <th>{t("pnlAttribution.residualPnl")}</th>
              </tr>
            </thead>
            <tbody>
              {analysis.fixed_income_effects.map((row) => (
                <tr key={row.symbol}>
                  <td><strong>{row.symbol}</strong><span>{row.duration_source}</span></td>
                  <td><MoneyValue value={row.duration_effect} currency={currency} /></td>
                  <td><MoneyValue value={row.convexity_effect} currency={currency} /></td>
                  <td><MoneyValue value={row.income_effect} currency={currency} /></td>
                  <td>{row.rate_shock_bps} bps</td>
                  <td><MoneyValue value={row.residual_pnl} currency={currency} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <EmptyState title={t("pnlAttribution.noFixedIncome")} message={t("pnlAttribution.noFixedIncomeMessage")} />
      )}
    </section>
  );
}

function OptionsTab({ analysis, currency, t }: { analysis: PnlAttributionResult; currency: string; t: (key: string) => string }) {
  const options = analysis.options_effects;
  return (
    <section className="risk-monitor-section-card">
      <header className="risk-monitor-section-card__header">
        <h2>{t("pnlAttribution.optionsPnl")}</h2>
        <p>{options.notes.join(" ")}</p>
      </header>
      <div className="pnl-definition-grid">
        <Definition label="Delta" value={<MoneyValue value={options.delta_contribution} currency={currency} />} />
        <Definition label="Gamma" value={<MoneyValue value={options.gamma_contribution} currency={currency} />} />
        <Definition label="Vega" value={<MoneyValue value={options.vega_contribution} currency={currency} />} />
        <Definition label="Theta" value={<MoneyValue value={options.theta_contribution} currency={currency} />} />
        <Definition label="Rho" value={<MoneyValue value={options.rho_contribution} currency={currency} />} />
        <Definition label={t("pnlAttribution.residualPnl")} value={<MoneyValue value={options.residual_pnl} currency={currency} />} />
      </div>
    </section>
  );
}

function TradesTab({ analysis, currency, t }: { analysis: PnlAttributionResult; currency: string; t: (key: string) => string }) {
  const trade = analysis.trade_effects;
  return (
    <section className="risk-monitor-section-card">
      <header className="risk-monitor-section-card__header">
        <h2>{t("pnlAttribution.tradeImpact")}</h2>
        <p>{trade.warnings.join(" ") || t("pnlAttribution.tradeDescription")}</p>
      </header>
      <div className="pnl-definition-grid">
        <Definition label={t("pnlAttribution.tradeStatus")} value={trade.status} />
        <Definition label={t("pnlAttribution.transactionCosts")} value={<MoneyValue value={trade.total_trade_costs} currency={currency} />} />
        <Definition label={t("pnlAttribution.slippage")} value={<MoneyValue value={trade.estimated_slippage} currency={currency} />} />
        <Definition label={t("pnlAttribution.turnover")} value={<PercentValue value={trade.turnover} />} />
        <Definition label={t("pnlAttribution.tradeImpactCash")} value={<MoneyValue value={trade.trade_impact_on_cash} currency={currency} />} />
      </div>
    </section>
  );
}

function MethodologyTab({ analysis, csvPreview, t }: { analysis: PnlAttributionResult; csvPreview: string; t: (key: string) => string }) {
  return (
    <section className="risk-monitor-panel pnl-overview-grid">
      <article className="risk-monitor-section-card">
        <header className="risk-monitor-section-card__header">
          <h2>{t("pnlAttribution.methodology")}</h2>
          <p>{t("pnlAttribution.methodologyDescription")}</p>
        </header>
        <ListBlock title={t("common.assumptions")} items={analysis.methodology.assumptions} />
        <ListBlock title={t("common.dataSource")} items={analysis.methodology.data_sources} />
        <ListBlock title={t("common.limitations")} items={analysis.limitations} />
        <ListBlock title={t("pnlAttribution.warnings")} items={analysis.warnings} />
      </article>
      <article className="risk-monitor-section-card">
        <header className="risk-monitor-section-card__header">
          <h2>{t("pnlAttribution.dataQuality")}</h2>
          <p>{t("pnlAttribution.notInvestmentAdvice")}</p>
        </header>
        <pre className="pnl-csv-preview">{csvPreview || t("pnlAttribution.noCsvPreview")}</pre>
      </article>
    </section>
  );
}

function GroupPanel({ title, rows, currency }: { title: string; rows: GroupPnlContribution[]; currency: string }) {
  return (
    <article className="risk-monitor-section-card">
      <header className="risk-monitor-section-card__header">
        <h2>{title}</h2>
      </header>
      <div className="risk-monitor-contribution-list">
        {rows.map((row) => (
          <ContributionRow
            key={row.name}
            label={row.name}
            value={row.total_pnl}
            percent={row.contribution_to_portfolio_return}
            currency={currency}
          />
        ))}
      </div>
    </article>
  );
}

function PnlMetricCard({ label, value, tone }: { label: string; value: ReactNode; tone: "neutral" | "positive" | "negative" | "warning" }) {
  return (
    <div className={`risk-monitor-metric-card pnl-metric-card pnl-metric-card--${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function Definition({ label, value }: { label: string; value: ReactNode }) {
  return (
    <div className="pnl-definition">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function ContributionRow({ label, value, percent, currency = "USD" }: { label: string; value: number; percent: number; currency?: string }) {
  return (
    <div>
      <div>
        <strong>{label}</strong>
        <small><PercentValue value={percent} /></small>
      </div>
      <strong className={toneClass(value)}><MoneyValue value={value} currency={currency} /></strong>
    </div>
  );
}

function ListBlock({ title, items }: { title: string; items: string[] }) {
  if (!items.length) return null;
  return (
    <div className="pnl-list-block">
      <h3>{title}</h3>
      <ul>
        {items.map((item) => <li key={item}>{item}</li>)}
      </ul>
    </div>
  );
}

function buildKpis(analysis: PnlAttributionResult | null, t: (key: string) => string) {
  if (!analysis) {
    return [
      [t("pnlAttribution.startingValue"), "--", "neutral"],
      [t("pnlAttribution.endingValue"), "--", "neutral"],
      [t("pnlAttribution.totalPnl"), "--", "neutral"],
      [t("pnlAttribution.totalReturn"), "--", "neutral"],
      [t("pnlAttribution.realizedPnl"), "--", "neutral"],
      [t("pnlAttribution.unrealizedPnl"), "--", "neutral"],
      [t("pnlAttribution.income"), "--", "neutral"],
      [t("pnlAttribution.feesCosts"), "--", "neutral"],
      [t("pnlAttribution.activeReturn"), "--", "neutral"],
      [t("pnlAttribution.topContributor"), "--", "neutral"],
      [t("pnlAttribution.worstContributor"), "--", "neutral"],
    ] as Array<[string, ReactNode, "neutral" | "positive" | "negative" | "warning"]>;
  }
  return [
    [t("pnlAttribution.startingValue"), <MoneyValue value={analysis.starting_value} />, "neutral"],
    [t("pnlAttribution.endingValue"), <MoneyValue value={analysis.ending_value} />, analysis.total_pnl >= 0 ? "positive" : "negative"],
    [t("pnlAttribution.totalPnl"), <MoneyValue value={analysis.total_pnl} />, analysis.total_pnl >= 0 ? "positive" : "negative"],
    [t("pnlAttribution.totalReturn"), <PercentValue value={analysis.total_pnl_percent} />, analysis.total_pnl_percent >= 0 ? "positive" : "negative"],
    [t("pnlAttribution.realizedPnl"), <MoneyValue value={analysis.realized_pnl} />, "neutral"],
    [t("pnlAttribution.unrealizedPnl"), <MoneyValue value={analysis.unrealized_pnl} />, analysis.unrealized_pnl >= 0 ? "positive" : "negative"],
    [t("pnlAttribution.income"), <MoneyValue value={analysis.income_pnl} />, "positive"],
    [t("pnlAttribution.feesCosts"), <MoneyValue value={analysis.fees_and_costs} />, analysis.fees_and_costs > 0 ? "warning" : "neutral"],
    [
      t("pnlAttribution.activeReturn"),
      analysis.benchmark_comparison.active_return === null ? "--" : <PercentValue value={analysis.benchmark_comparison.active_return} />,
      (analysis.benchmark_comparison.active_return ?? 0) >= 0 ? "positive" : "negative",
    ],
    [t("pnlAttribution.topContributor"), analysis.top_winners[0]?.symbol ?? "--", "positive"],
    [t("pnlAttribution.worstContributor"), analysis.top_losers[0]?.symbol ?? "--", "warning"],
  ] as Array<[string, ReactNode, "neutral" | "positive" | "negative" | "warning"]>;
}

function toneClass(value: number) {
  if (value > 0) return "positive-value";
  if (value < 0) return "negative-value";
  return "";
}

function formatMoney(value: number) {
  return new Intl.NumberFormat("en-CA", {
    currency: "USD",
    style: "currency",
    maximumFractionDigits: 0,
  }).format(value);
}
