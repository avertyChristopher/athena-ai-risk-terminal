import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useMutation, useQuery } from "@tanstack/react-query";

import { MoneyValue } from "../../../components/finance/MoneyValue";
import { PageHeader } from "../../../components/layout/PageHeader";
import { EmptyState } from "../../../components/ui/EmptyState";
import { ErrorBanner } from "../../../components/ui/ErrorBanner";
import { LoadingState } from "../../../components/ui/LoadingState";
import { StatusBadge, type StatusBadgeVariant } from "../../../components/ui/StatusBadge";
import { apiClient } from "../../../lib/api-client";
import { endpoints } from "../../../lib/endpoints";
import { useTranslation } from "../../../hooks/useTranslation";
import { tradeBlotterApi } from "../../../services/tradeBlotterApi";
import type { PortfolioListResponse } from "../../../types/portfolio";
import type {
  TradeBlotterAction,
  TradeBlotterEntry,
  TradeBlotterEntryCreate,
  TradeBlotterStatusValue,
  TradeReviewAction,
} from "../../../types/trade-blotter";

type TradeBlotterTab =
  | "overview"
  | "register"
  | "workflow"
  | "costs"
  | "links"
  | "methodology";

const tabs: TradeBlotterTab[] = [
  "overview",
  "register",
  "workflow",
  "costs",
  "links",
  "methodology",
];
const tradeStatuses: TradeBlotterStatusValue[] = [
  "draft",
  "pending_review",
  "approved",
  "rejected",
  "simulated",
  "cancelled",
];
const statusOptions: Array<TradeBlotterStatusValue | "all"> = ["all", ...tradeStatuses];
const tradeActions: TradeBlotterAction[] = [
  "BUY",
  "SELL",
  "SHORT",
  "COVER",
  "OPTION",
  "BOND",
];
const actionOptions: Array<TradeBlotterAction | "all"> = ["all", ...tradeActions];
const reviewActions: TradeReviewAction[] = [
  "submit_for_review",
  "approve",
  "reject",
  "simulate",
  "cancel",
  "reopen",
];

export function TradeBlotterPage() {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState<TradeBlotterTab>("overview");
  const [portfolioFilter, setPortfolioFilter] = useState("all");
  const [statusFilter, setStatusFilter] = useState<TradeBlotterStatusValue | "all">("all");
  const [actionFilter, setActionFilter] = useState<TradeBlotterAction | "all">("all");
  const [selectedTradeId, setSelectedTradeId] = useState("");
  const [manualTrade, setManualTrade] = useState<TradeBlotterEntryCreate>({
    portfolio_id: "pf_001",
    symbol: "AAPL",
    action: "BUY",
    quantity: 5,
    price: 195,
    currency: "USD",
    status: "draft",
    source_module: "manual_trade_blotter",
    suitability_status: "Manual Review",
    constraint_status: "pending",
  });

  const statusQuery = useQuery({
    queryKey: ["trade-blotter-status"],
    queryFn: tradeBlotterApi.status,
  });
  const portfolioQuery = useQuery({
    queryKey: ["trade-blotter-portfolios"],
    queryFn: () => apiClient.get<PortfolioListResponse>(endpoints.portfolios),
  });
  const tradesQuery = useQuery({
    queryKey: ["trade-blotter-trades", portfolioFilter, statusFilter],
    queryFn: () =>
      tradeBlotterApi.list({
        portfolio_id: portfolioFilter === "all" ? undefined : portfolioFilter,
        status: statusFilter === "all" ? undefined : statusFilter,
      }),
  });

  const createMutation = useMutation({
    mutationFn: tradeBlotterApi.create,
    onSuccess: (entry) => {
      setSelectedTradeId(entry.trade_id);
      setActiveTab("workflow");
      void tradesQuery.refetch();
      void statusQuery.refetch();
    },
  });
  const reviewMutation = useMutation({
    mutationFn: ({ tradeId, action }: { tradeId: string; action: TradeReviewAction }) =>
      tradeBlotterApi.review(tradeId, {
        action,
        reviewer: "frontend_analyst",
        note: `Frontend workflow action: ${action}`,
      }),
    onSuccess: (response) => {
      setSelectedTradeId(response.entry.trade_id);
      void tradesQuery.refetch();
      void statusQuery.refetch();
    },
  });
  const demoMutation = useMutation({
    mutationFn: tradeBlotterApi.demo,
    onSuccess: (response) => {
      setSelectedTradeId(response.entries[0]?.trade_id ?? "");
      void tradesQuery.refetch();
      void statusQuery.refetch();
    },
  });
  const deleteMutation = useMutation({
    mutationFn: tradeBlotterApi.delete,
    onSuccess: () => {
      setSelectedTradeId("");
      void tradesQuery.refetch();
      void statusQuery.refetch();
    },
  });

  const allEntries = tradesQuery.data?.entries ?? [];
  const entries = useMemo(
    () =>
      actionFilter === "all"
        ? allEntries
        : allEntries.filter((entry) => entry.action === actionFilter),
    [actionFilter, allEntries],
  );
  const selectedTrade =
    entries.find((entry) => entry.trade_id === selectedTradeId) ??
    entries[0] ??
    null;
  const kpis = buildKpis(entries);
  const isLoading = statusQuery.isLoading || tradesQuery.isLoading;
  const hasError = statusQuery.isError || tradesQuery.isError;

  function updateManualTrade<Value extends keyof TradeBlotterEntryCreate>(
    key: Value,
    value: TradeBlotterEntryCreate[Value],
  ) {
    setManualTrade((current) => ({ ...current, [key]: value }));
  }

  function createManualTrade() {
    createMutation.mutate({
      ...manualTrade,
      symbol: manualTrade.symbol.toUpperCase(),
      trade_date: new Date().toISOString().slice(0, 10),
      cost_estimate: Math.abs(manualTrade.quantity * manualTrade.price) * 0.0005,
      slippage_estimate: Math.abs(manualTrade.quantity * manualTrade.price) * 0.0003,
      risk_summary: {
        source: "manual_frontend_entry",
        no_real_execution: true,
      },
    });
  }

  return (
    <div className="page trade-blotter-page risk-monitor-page">
      <PageHeader
        title={t("tradeBlotter.title")}
        subtitle={t("tradeBlotter.subtitle")}
      />

      <section className="risk-monitor-command-panel trade-blotter-command-panel">
        <div>
          <span>{t("tradeBlotter.eyebrow")}</span>
          <h2>{t("tradeBlotter.workbenchTitle")}</h2>
          <p>{statusQuery.data?.detail ?? t("tradeBlotter.workbenchDescription")}</p>
        </div>
        <div className="risk-monitor-badge-cluster">
          <StatusBadge
            label={statusQuery.data?.persistence_enabled ? t("tradeBlotter.databaseConnected") : t("tradeBlotter.inMemoryFallback")}
            variant={statusQuery.data?.persistence_enabled ? "success" : "warning"}
          />
          <StatusBadge label={t("tradeBlotter.tradeWorkflow")} variant="info" />
          <StatusBadge label={t("tradeBlotter.review")} variant="warning" />
          <StatusBadge label={t("tradeBlotter.pnlReady")} variant="success" />
          <StatusBadge label={t("tradeBlotter.reconciliationReady")} variant="success" />
        </div>
      </section>

      <section className="trade-blotter-controls">
        <label className="form-field">
          <span>{t("workflow.portfolio")}</span>
          <select
            value={portfolioFilter}
            onChange={(event) => setPortfolioFilter(event.target.value)}
          >
            <option value="all">{t("common.all")}</option>
            {(portfolioQuery.data?.items ?? []).map((portfolio) => (
              <option key={portfolio.id} value={portfolio.id}>
                {portfolio.name}
              </option>
            ))}
          </select>
        </label>
        <label className="form-field">
          <span>{t("tradeBlotter.status")}</span>
          <select
            value={statusFilter}
            onChange={(event) => setStatusFilter(event.target.value as TradeBlotterStatusValue | "all")}
          >
            {statusOptions.map((status) => (
              <option key={status} value={status}>
                {status === "all" ? t("common.all") : statusLabel(status, t)}
              </option>
            ))}
          </select>
        </label>
        <label className="form-field">
          <span>{t("tradeBlotter.action")}</span>
          <select
            value={actionFilter}
            onChange={(event) => setActionFilter(event.target.value as TradeBlotterAction | "all")}
          >
            {actionOptions.map((action) => (
              <option key={action} value={action}>
                {action}
              </option>
            ))}
          </select>
        </label>
        <button className="button button--secondary" type="button" onClick={() => tradesQuery.refetch()}>
          {t("workflow.refresh")}
        </button>
        <button
          className="button button--primary"
          type="button"
          onClick={() => demoMutation.mutate()}
        >
          {t("tradeBlotter.loadDemo")}
        </button>
      </section>

      {hasError ? (
        <ErrorBanner
          title={t("tradeBlotter.title")}
          message={t("tradeBlotter.error")}
        />
      ) : null}

      <section className="trade-blotter-kpi-grid">
        {kpis.map((kpi) => (
          <article className={`card trade-blotter-kpi trade-blotter-kpi--${kpi.tone}`} key={kpi.label}>
            <span>{kpi.label}</span>
            <strong>{kpi.value}</strong>
            <p>{kpi.detail}</p>
          </article>
        ))}
      </section>

      <nav className="trade-analysis-tabs" aria-label="Trade blotter sections">
        {tabs.map((tab) => (
          <button
            key={tab}
            className={`trade-analysis-tab ${activeTab === tab ? "trade-analysis-tab--active" : ""}`}
            type="button"
            onClick={() => setActiveTab(tab)}
          >
            <span>{t(`tradeBlotter.tabs.${tab}`)}</span>
            <small>{t(`tradeBlotter.tabDescriptions.${tab}`)}</small>
          </button>
        ))}
      </nav>

      {isLoading ? (
        <LoadingState label={t("common.loading")} />
      ) : (
        <section className="trade-blotter-panel">
          {activeTab === "overview" ? (
            <OverviewPanel entries={entries} selectedTrade={selectedTrade} t={t} />
          ) : null}
          {activeTab === "register" ? (
            <RegisterPanel
              entries={entries}
              selectedTradeId={selectedTradeId}
              onSelect={(tradeId) => {
                setSelectedTradeId(tradeId);
                setActiveTab("workflow");
              }}
              onDelete={(tradeId) => deleteMutation.mutate(tradeId)}
              t={t}
            />
          ) : null}
          {activeTab === "workflow" ? (
            <WorkflowPanel
              selectedTrade={selectedTrade}
              reviewPending={reviewMutation.isPending}
              onReview={(action) => selectedTrade && reviewMutation.mutate({ tradeId: selectedTrade.trade_id, action })}
              t={t}
            />
          ) : null}
          {activeTab === "costs" ? (
            <CostsPanel entries={entries} selectedTrade={selectedTrade} t={t} />
          ) : null}
          {activeTab === "links" ? <DownstreamLinksPanel t={t} /> : null}
          {activeTab === "methodology" ? (
            <MethodologyPanel
              manualTrade={manualTrade}
              updateManualTrade={updateManualTrade}
              createManualTrade={createManualTrade}
              createPending={createMutation.isPending}
              t={t}
            />
          ) : null}
        </section>
      )}
    </div>
  );
}

function OverviewPanel({
  entries,
  selectedTrade,
  t,
}: {
  entries: TradeBlotterEntry[];
  selectedTrade: TradeBlotterEntry | null;
  t: (key: string) => string;
}) {
  const statusSummary = countBy(entries, "status");
  return (
    <div className="trade-blotter-two-column">
      <section className="card trade-blotter-section-card">
        <div className="section-heading">
          <h2>{t("tradeBlotter.overview.statusSummary")}</h2>
          <StatusBadge label={t("tradeBlotter.persistentHistory")} variant="success" />
        </div>
        <div className="trade-blotter-status-grid">
          {tradeStatuses.map((status) => (
            <div key={status}>
              <span>{statusLabel(status, t)}</span>
              <strong>{statusSummary[status] ?? 0}</strong>
            </div>
          ))}
        </div>
      </section>
      <section className="card trade-blotter-section-card">
        <div className="section-heading">
          <h2>{t("tradeBlotter.overview.athena")}</h2>
          <StatusBadge label={t("tradeBlotter.beta")} variant="warning" />
        </div>
        <p>
          {selectedTrade
            ? `${selectedTrade.action} ${selectedTrade.quantity} ${selectedTrade.symbol} is ${statusLabel(selectedTrade.status, t).toLowerCase()} with ${selectedTrade.constraint_status ?? "no"} constraint status.`
            : t("tradeBlotter.empty")}
        </p>
        <div className="trade-blotter-mini-list">
          <span>{t("tradeBlotter.noRealExecution")}</span>
          <span>{t("tradeBlotter.notInvestmentAdvice")}</span>
          <span>{t("tradeBlotter.persistenceStatus")}</span>
        </div>
      </section>
    </div>
  );
}

function RegisterPanel({
  entries,
  selectedTradeId,
  onSelect,
  onDelete,
  t,
}: {
  entries: TradeBlotterEntry[];
  selectedTradeId: string;
  onSelect: (tradeId: string) => void;
  onDelete: (tradeId: string) => void;
  t: (key: string) => string;
}) {
  if (!entries.length) {
    return <EmptyState title={t("tradeBlotter.emptyTitle")} message={t("tradeBlotter.emptyMessage")} />;
  }

  return (
    <section className="card trade-blotter-table-card">
      <div className="trade-blotter-table">
        <div className="trade-blotter-table__head">
          <span>{t("tradeBlotter.tradeId")}</span>
          <span>{t("workflow.portfolio")}</span>
          <span>{t("workflow.symbol")}</span>
          <span>{t("tradeBlotter.action")}</span>
          <span>{t("tradeBlotter.quantity")}</span>
          <span>{t("tradeBlotter.price")}</span>
          <span>{t("tradeBlotter.totalNotional")}</span>
          <span>{t("tradeBlotter.status")}</span>
          <span>{t("tradeBlotter.tradeDate")}</span>
          <span>{t("tradeBlotter.actions")}</span>
        </div>
        {entries.map((entry) => (
          <div
            className={`trade-blotter-table__row ${selectedTradeId === entry.trade_id ? "trade-blotter-table__row--selected" : ""}`}
            key={entry.trade_id}
          >
            <strong>{entry.trade_id}</strong>
            <span>{entry.portfolio_id}</span>
            <span>{entry.symbol}</span>
            <span>{entry.action}</span>
            <span>{entry.quantity.toLocaleString()}</span>
            <MoneyValue value={entry.price} currency={entry.currency} />
            <MoneyValue value={entry.estimated_trade_value} currency={entry.currency} />
            <StatusBadge label={statusLabel(entry.status, t)} variant={statusVariant(entry.status)} />
            <span>{entry.trade_date}</span>
            <div>
              <button type="button" onClick={() => onSelect(entry.trade_id)}>
                {t("tradeBlotter.review")}
              </button>
              <button type="button" onClick={() => onDelete(entry.trade_id)}>
                {t("tradeBlotter.delete")}
              </button>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

function WorkflowPanel({
  selectedTrade,
  reviewPending,
  onReview,
  t,
}: {
  selectedTrade: TradeBlotterEntry | null;
  reviewPending: boolean;
  onReview: (action: TradeReviewAction) => void;
  t: (key: string) => string;
}) {
  if (!selectedTrade) {
    return <EmptyState title={t("tradeBlotter.emptyTitle")} message={t("tradeBlotter.emptyMessage")} />;
  }
  return (
    <div className="trade-blotter-two-column">
      <section className="card trade-blotter-section-card">
        <div className="section-heading">
          <h2>{selectedTrade.symbol}</h2>
          <StatusBadge label={statusLabel(selectedTrade.status, t)} variant={statusVariant(selectedTrade.status)} />
        </div>
        <dl className="trade-blotter-detail-list">
          <div><dt>{t("tradeBlotter.suitabilityStatus")}</dt><dd>{selectedTrade.suitability_status ?? t("common.unavailable")}</dd></div>
          <div><dt>{t("tradeBlotter.constraintStatus")}</dt><dd>{selectedTrade.constraint_status ?? t("common.unavailable")}</dd></div>
          <div><dt>{t("tradeBlotter.estimatedCosts")}</dt><dd><MoneyValue value={selectedTrade.cost_estimate + selectedTrade.slippage_estimate} currency={selectedTrade.currency} /></dd></div>
          <div><dt>{t("tradeBlotter.sourceModule")}</dt><dd>{selectedTrade.source_module}</dd></div>
        </dl>
        <div className="trade-blotter-review-actions">
          {reviewActions.map((action) => (
            <button
              className={action === "approve" ? "button button--primary" : "button button--secondary"}
              disabled={reviewPending}
              key={action}
              type="button"
              onClick={() => onReview(action)}
            >
              {reviewActionLabel(action, t)}
            </button>
          ))}
        </div>
      </section>
      <section className="card trade-blotter-section-card">
        <div className="section-heading">
          <h2>{t("tradeBlotter.reviewHistory")}</h2>
          <StatusBadge label={`${selectedTrade.review_history.length}`} variant="info" />
        </div>
        {selectedTrade.review_history.length ? (
          <div className="trade-blotter-history-list">
            {selectedTrade.review_history.map((event) => (
              <div key={`${event.action}-${event.timestamp}`}>
                <strong>{reviewActionLabel(event.action, t)}</strong>
                <span>{event.from_status} {"->"} {event.to_status}</span>
                <p>{event.note ?? event.reviewer}</p>
              </div>
            ))}
          </div>
        ) : (
          <EmptyState title={t("tradeBlotter.noReviewHistory")} message={t("tradeBlotter.noReviewHistoryMessage")} />
        )}
      </section>
    </div>
  );
}

function CostsPanel({
  entries,
  selectedTrade,
  t,
}: {
  entries: TradeBlotterEntry[];
  selectedTrade: TradeBlotterEntry | null;
  t: (key: string) => string;
}) {
  const notional = entries.reduce((sum, entry) => sum + entry.estimated_trade_value, 0);
  const costs = entries.reduce((sum, entry) => sum + entry.cost_estimate + entry.slippage_estimate, 0);
  return (
    <div className="trade-blotter-two-column">
      <section className="card trade-blotter-section-card">
        <h2>{t("tradeBlotter.costsImpact")}</h2>
        <div className="trade-blotter-status-grid">
          <div><span>{t("tradeBlotter.totalNotional")}</span><strong><MoneyValue value={notional} /></strong></div>
          <div><span>{t("tradeBlotter.estimatedCosts")}</span><strong><MoneyValue value={costs} /></strong></div>
          <div><span>{t("tradeBlotter.turnoverProxy")}</span><strong>{notional ? `${((costs / notional) * 100).toFixed(2)}%` : "0.00%"}</strong></div>
        </div>
      </section>
      <section className="card trade-blotter-section-card">
        <h2>{t("tradeBlotter.selectedTrade")}</h2>
        {selectedTrade ? (
          <dl className="trade-blotter-detail-list">
            <div><dt>{t("tradeBlotter.cashImpact")}</dt><dd><MoneyValue value={cashImpact(selectedTrade)} currency={selectedTrade.currency} /></dd></div>
            <div><dt>{t("tradeBlotter.slippage")}</dt><dd><MoneyValue value={selectedTrade.slippage_estimate} currency={selectedTrade.currency} /></dd></div>
            <div><dt>{t("tradeBlotter.riskSummary")}</dt><dd>{Object.keys(selectedTrade.risk_summary).length ? JSON.stringify(selectedTrade.risk_summary) : t("common.unavailable")}</dd></div>
          </dl>
        ) : (
          <EmptyState title={t("tradeBlotter.emptyTitle")} message={t("tradeBlotter.emptyMessage")} />
        )}
      </section>
    </div>
  );
}

function DownstreamLinksPanel({ t }: { t: (key: string) => string }) {
  const links = [
    [t("nav.pnlAttribution"), "/pnl-attribution", t("tradeBlotter.downstream.pnl")],
    [t("nav.reconciliation"), "/reconciliation", t("tradeBlotter.downstream.reconciliation")],
    [t("nav.reportsCenter"), "/reports-center", t("tradeBlotter.downstream.reports")],
    [t("nav.riskMonitor"), "/risk-monitor", t("tradeBlotter.downstream.risk")],
    [t("nav.limitCenter"), "/limit-center", t("tradeBlotter.downstream.limits")],
  ];
  return (
    <div className="trade-blotter-link-grid">
      {links.map(([label, path, description]) => (
        <Link className="dashboard-workflow-card" key={path} to={path}>
          <div>
            <h3>{label}</h3>
            <p>{description}</p>
          </div>
          <strong>{t("workflow.continueWorkflow")}</strong>
        </Link>
      ))}
    </div>
  );
}

function MethodologyPanel({
  manualTrade,
  updateManualTrade,
  createManualTrade,
  createPending,
  t,
}: {
  manualTrade: TradeBlotterEntryCreate;
  updateManualTrade: <Value extends keyof TradeBlotterEntryCreate>(
    key: Value,
    value: TradeBlotterEntryCreate[Value],
  ) => void;
  createManualTrade: () => void;
  createPending: boolean;
  t: (key: string) => string;
}) {
  return (
    <div className="trade-blotter-two-column">
      <section className="card trade-blotter-section-card">
        <h2>{t("tradeBlotter.manualTrade")}</h2>
        <div className="trade-blotter-form-grid">
          <label className="form-field"><span>{t("workflow.portfolio")}</span><input value={manualTrade.portfolio_id} onChange={(event) => updateManualTrade("portfolio_id", event.target.value)} /></label>
          <label className="form-field"><span>{t("workflow.symbol")}</span><input value={manualTrade.symbol} onChange={(event) => updateManualTrade("symbol", event.target.value)} /></label>
          <label className="form-field"><span>{t("tradeBlotter.action")}</span><select value={manualTrade.action} onChange={(event) => updateManualTrade("action", event.target.value as TradeBlotterAction)}>{tradeActions.map((action) => <option key={action} value={action}>{action}</option>)}</select></label>
          <label className="form-field"><span>{t("tradeBlotter.quantity")}</span><input min="0.01" step="0.01" type="number" value={manualTrade.quantity} onChange={(event) => updateManualTrade("quantity", Number(event.target.value))} /></label>
          <label className="form-field"><span>{t("tradeBlotter.price")}</span><input min="0.01" step="0.01" type="number" value={manualTrade.price} onChange={(event) => updateManualTrade("price", Number(event.target.value))} /></label>
          <label className="form-field"><span>{t("tradeBlotter.status")}</span><select value={manualTrade.status} onChange={(event) => updateManualTrade("status", event.target.value as TradeBlotterStatusValue)}>{tradeStatuses.map((status) => <option key={status} value={status}>{statusLabel(status, t)}</option>)}</select></label>
        </div>
        <button className="button button--primary" disabled={createPending} type="button" onClick={createManualTrade}>
          {t("tradeBlotter.createManualTrade")}
        </button>
      </section>
      <section className="card trade-blotter-section-card">
        <h2>{t("common.methodology")}</h2>
        <ul className="dashboard-module-features">
          <li>{t("tradeBlotter.methodology.simulated")}</li>
          <li>{t("tradeBlotter.methodology.noExecution")}</li>
          <li>{t("tradeBlotter.methodology.noBroker")}</li>
          <li>{t("tradeBlotter.methodology.demoPersistence")}</li>
          <li>{t("tradeBlotter.notInvestmentAdvice")}</li>
        </ul>
      </section>
    </div>
  );
}

function buildKpis(entries: TradeBlotterEntry[]) {
  const totalNotional = entries.reduce((sum, entry) => sum + entry.estimated_trade_value, 0);
  const costs = entries.reduce((sum, entry) => sum + entry.cost_estimate + entry.slippage_estimate, 0);
  const count = (status: TradeBlotterStatusValue) => entries.filter((entry) => entry.status === status).length;
  return [
    { label: "Total Trades", value: String(entries.length), detail: "Persistent trade register", tone: "neutral" },
    { label: "Pending Review", value: String(count("pending_review")), detail: "Workflow queue", tone: "warning" },
    { label: "Approved Trades", value: String(count("approved")), detail: "P&L ready", tone: "positive" },
    { label: "Rejected Trades", value: String(count("rejected")), detail: "Control exceptions", tone: "warning" },
    { label: "Simulated Trades", value: String(count("simulated")), detail: "Saved from simulator", tone: "neutral" },
    { label: "Total Notional", value: formatMoney(totalNotional), detail: "Gross trade value", tone: "neutral" },
    { label: "Estimated Costs", value: formatMoney(costs), detail: "Costs + slippage", tone: "warning" },
    { label: "Last Trade", value: entries[0]?.symbol ?? "-", detail: entries[0]?.trade_date ?? "No trades", tone: "neutral" },
  ] as const;
}

function countBy(entries: TradeBlotterEntry[], key: "status") {
  return entries.reduce<Record<string, number>>((counts, entry) => {
    counts[entry[key]] = (counts[entry[key]] ?? 0) + 1;
    return counts;
  }, {});
}

function formatMoney(value: number) {
  return new Intl.NumberFormat(undefined, {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(value);
}

function statusVariant(status: TradeBlotterStatusValue): StatusBadgeVariant {
  if (status === "approved") return "success";
  if (status === "rejected" || status === "cancelled") return "danger";
  if (status === "pending_review") return "warning";
  if (status === "simulated") return "info";
  return "neutral";
}

function statusLabel(status: TradeBlotterStatusValue, t: (key: string) => string) {
  const labels: Record<TradeBlotterStatusValue, string> = {
    draft: t("tradeBlotter.draft"),
    pending_review: t("tradeBlotter.pendingReview"),
    approved: t("tradeBlotter.approvedTrades"),
    rejected: t("tradeBlotter.rejectedTrades"),
    simulated: t("tradeBlotter.simulatedTrades"),
    cancelled: t("tradeBlotter.cancelled"),
  };
  return labels[status];
}

function reviewActionLabel(action: TradeReviewAction, t: (key: string) => string) {
  const labels: Record<TradeReviewAction, string> = {
    submit_for_review: t("tradeBlotter.submitForReview"),
    approve: t("tradeBlotter.approveTrade"),
    reject: t("tradeBlotter.rejectTrade"),
    simulate: t("tradeBlotter.simulateTrade"),
    cancel: t("tradeBlotter.cancelTrade"),
    reopen: t("tradeBlotter.reopenTrade"),
  };
  return labels[action];
}

function cashImpact(entry: TradeBlotterEntry) {
  return entry.action === "SELL" || entry.action === "SHORT"
    ? entry.estimated_trade_value
    : -entry.estimated_trade_value;
}
