import { useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";
import { Link } from "react-router-dom";
import { useMutation, useQuery } from "@tanstack/react-query";

import { AthenaAICommentaryCard } from "../../../components/ai/AthenaAICommentaryCard";
import { PageHeader } from "../../../components/layout/PageHeader";
import { EmptyState } from "../../../components/ui/EmptyState";
import { ErrorBanner } from "../../../components/ui/ErrorBanner";
import { LoadingState } from "../../../components/ui/LoadingState";
import { StatusBadge } from "../../../components/ui/StatusBadge";
import { usePortfolioContext } from "../../../context/PortfolioContext";
import { useTranslation } from "../../../hooks/useTranslation";
import { apiClient } from "../../../lib/api-client";
import { endpoints } from "../../../lib/endpoints";
import { reconciliationApi } from "../../../services/reconciliationApi";
import { reportsCenterApi } from "../../../services/reportsCenterApi";
import type { PortfolioListResponse } from "../../../types/portfolio";
import type {
  BreakSeverity,
  BreakStatus,
  BreakType,
  ExternalSource,
  OverallStatus,
  ReconciliationBreak,
  ReconciliationCheck,
  ReconciliationRequest,
  ReconciliationRunResult,
  ReconciliationTolerance,
  ReviewAction,
} from "../../../types/reconciliation";

type ReconTab =
  | "overview"
  | "positions"
  | "cashFx"
  | "prices"
  | "tradesPnl"
  | "register"
  | "review"
  | "reports"
  | "methodology"
  | "commentary";

const tabs: ReconTab[] = [
  "overview",
  "positions",
  "cashFx",
  "prices",
  "tradesPnl",
  "register",
  "review",
  "reports",
  "methodology",
  "commentary",
];

const checkTypes: ReconciliationCheck[] = [
  "positions",
  "cash",
  "prices",
  "trades",
  "pnl",
  "fx",
];

const defaultTolerance: ReconciliationTolerance = {
  position_quantity_tolerance: 0.0001,
  market_value_tolerance: 50,
  cash_tolerance: 100,
  price_tolerance_bps: 10,
  pnl_tolerance: 250,
};

const reviewActions: ReviewAction[] = [
  "mark_under_review",
  "explain",
  "resolve",
  "ignore",
  "reopen",
];

export function ReconciliationPage() {
  const { i18n, t } = useTranslation();
  const { selectedPortfolioId, selectPortfolio } = usePortfolioContext();
  const [activeTab, setActiveTab] = useState<ReconTab>("overview");
  const [portfolioId, setPortfolioId] = useState(selectedPortfolioId || "pf_001");
  const [reconciliationDate, setReconciliationDate] = useState("2026-06-03");
  const [externalSource, setExternalSource] =
    useState<ExternalSource>("demo_custodian");
  const [selectedChecks, setSelectedChecks] =
    useState<ReconciliationCheck[]>(checkTypes);
  const [tolerance, setTolerance] =
    useState<ReconciliationTolerance>(defaultTolerance);
  const [showTolerances, setShowTolerances] = useState(false);
  const [result, setResult] = useState<ReconciliationRunResult | null>(null);
  const [selectedBreakId, setSelectedBreakId] = useState("");
  const [severityFilter, setSeverityFilter] = useState<BreakSeverity | "all">("all");
  const [typeFilter, setTypeFilter] = useState<BreakType | "all">("all");
  const [statusFilter, setStatusFilter] = useState<BreakStatus | "all">("all");
  const [reviewer, setReviewer] = useState("analyst");
  const [reviewNote, setReviewNote] = useState("");
  const [reviewDecision, setReviewDecision] = useState("");
  const [csvPreview, setCsvPreview] = useState("");
  const [reportMessage, setReportMessage] = useState("");

  useEffect(() => {
    if (selectedPortfolioId) {
      setPortfolioId(selectedPortfolioId);
    }
  }, [selectedPortfolioId]);

  const statusQuery = useQuery({
    queryKey: ["reconciliation-status"],
    queryFn: reconciliationApi.status,
  });
  const historyQuery = useQuery({
    queryKey: ["reconciliation-history"],
    queryFn: reconciliationApi.history,
  });
  const breaksQuery = useQuery({
    queryKey: ["reconciliation-breaks"],
    queryFn: reconciliationApi.breaks,
  });
  const portfolioQuery = useQuery({
    queryKey: ["reconciliation-portfolios"],
    queryFn: () => apiClient.get<PortfolioListResponse>(endpoints.portfolios),
  });

  const language = i18n.language.startsWith("fr") ? "fr" : "en";

  const runMutation = useMutation({
    mutationFn: () => reconciliationApi.run(buildRequest()),
    onSuccess: (payload) => {
      setResult(payload);
      setActiveTab("overview");
      setSelectedBreakId(payload.breaks[0]?.break_id ?? "");
      setCsvPreview("");
      setReportMessage("");
      void historyQuery.refetch();
      void breaksQuery.refetch();
    },
  });

  const demoMutation = useMutation({
    mutationFn: reconciliationApi.demo,
    onSuccess: (payload) => {
      setResult(payload);
      setPortfolioId(payload.portfolio_id);
      selectPortfolio(payload.portfolio_id);
      setActiveTab("overview");
      setSelectedBreakId(payload.breaks[0]?.break_id ?? "");
      setCsvPreview("");
      setReportMessage("");
      void historyQuery.refetch();
      void breaksQuery.refetch();
    },
  });

  const reviewMutation = useMutation({
    mutationFn: (action: ReviewAction) =>
      reconciliationApi.reviewBreak(selectedBreakId, {
        action,
        reviewer,
        note: reviewNote || null,
        decision: reviewDecision || null,
      }),
    onSuccess: (updatedBreak) => {
      setResult((current) =>
        current
          ? {
              ...current,
              breaks: current.breaks.map((item) =>
                item.break_id === updatedBreak.break_id ? updatedBreak : item,
              ),
            }
          : current,
      );
      setReviewNote("");
      setReviewDecision("");
      void breaksQuery.refetch();
      void historyQuery.refetch();
    },
  });

  const reportMutation = useMutation({
    mutationFn: () =>
      reportsCenterApi.generate({
        report_type: "reconciliation",
        portfolio_id: result?.portfolio_id ?? portfolioId,
        language,
        style: "professional",
        include_athena_commentary: true,
        include_methodology: true,
        include_limitations: true,
        source_payloads: result ? { reconciliation: result } : {},
      }),
    onSuccess: (report) => {
      setReportMessage(
        `${t("reconciliationCenter.reportGenerated")} ${report.report_id}`,
      );
    },
  });

  const breakRegister = useMemo(
    () => result?.breaks ?? breaksQuery.data?.items ?? [],
    [breaksQuery.data?.items, result?.breaks],
  );
  const filteredBreaks = useMemo(
    () =>
      breakRegister.filter((item) => {
        const severityMatch =
          severityFilter === "all" || item.severity === severityFilter;
        const typeMatch = typeFilter === "all" || item.break_type === typeFilter;
        const statusMatch = statusFilter === "all" || item.status === statusFilter;
        return severityMatch && typeMatch && statusMatch;
      }),
    [breakRegister, severityFilter, statusFilter, typeFilter],
  );
  const selectedBreak =
    breakRegister.find((item) => item.break_id === selectedBreakId) ??
    breakRegister[0] ??
    null;
  const kpis = useMemo(() => buildKpis(result, historyQuery.data?.items[0], t), [
    historyQuery.data?.items,
    result,
    t,
  ]);
  const sourceModules = statusQuery.data?.source_modules ?? [];
  const isLoading =
    statusQuery.isLoading || portfolioQuery.isLoading || historyQuery.isLoading;
  const hasError =
    statusQuery.isError ||
    portfolioQuery.isError ||
    runMutation.isError ||
    demoMutation.isError ||
    reviewMutation.isError ||
    reportMutation.isError;

  function buildRequest(): ReconciliationRequest {
    return {
      portfolio_id: portfolioId || "pf_001",
      reconciliation_date: reconciliationDate,
      external_source: externalSource,
      checks: selectedChecks.length ? selectedChecks : checkTypes,
      tolerance,
      language,
    };
  }

  function handlePortfolioChange(value: string) {
    setPortfolioId(value);
    selectPortfolio(value);
  }

  function toggleCheck(check: ReconciliationCheck) {
    setSelectedChecks((current) =>
      current.includes(check)
        ? current.filter((item) => item !== check)
        : [...current, check],
    );
  }

  async function loadHistoryItem(runId: string) {
    const payload = await reconciliationApi.historyItem(runId);
    setResult(payload);
    setSelectedBreakId(payload.breaks[0]?.break_id ?? "");
    setActiveTab("overview");
    setCsvPreview("");
  }

  async function exportCsv() {
    if (!result) return;
    const payload = await reconciliationApi.exportCsv(result.run_id);
    setCsvPreview(payload.csv);
    setActiveTab("reports");
  }

  return (
    <div className="page reconciliation-page risk-monitor-page">
      <PageHeader
        title={t("reconciliationCenter.title")}
        subtitle={t("reconciliationCenter.subtitle")}
      />

      <section className="risk-monitor-command-panel reconciliation-command-panel">
        <div>
          <span>{t("reconciliationCenter.eyebrow")}</span>
          <h2>{t("reconciliationCenter.workbenchTitle")}</h2>
          <p>{t("reconciliationCenter.workbenchDescription")}</p>
        </div>
        <div className="risk-monitor-badge-cluster">
          <StatusBadge
            label={statusQuery.data?.status ?? t("common.loading")}
            variant={statusQuery.data?.status === "ready" ? "success" : "warning"}
          />
          <StatusBadge label={t("reconciliationCenter.badges.middleOffice")} variant="info" />
          <StatusBadge label={t("reconciliationCenter.badges.breakRegister")} variant="warning" />
          <StatusBadge label={t("reconciliationCenter.badges.reportsReady")} variant="success" />
          <StatusBadge label={t("reconciliationCenter.badges.beta")} variant="warning" />
        </div>
      </section>

      <section className="reconciliation-control-card">
        <div className="reconciliation-control-grid">
          <label className="form-field">
            <span>{t("workflow.portfolio")}</span>
            <select
              value={portfolioId}
              onChange={(event) => handlePortfolioChange(event.target.value)}
            >
              {(portfolioQuery.data?.items ?? []).map((portfolio) => (
                <option key={portfolio.id} value={portfolio.id}>
                  {portfolio.name}
                </option>
              ))}
            </select>
          </label>
          <label className="form-field">
            <span>{t("reconciliationCenter.reconciliationDate")}</span>
            <input
              type="date"
              value={reconciliationDate}
              onChange={(event) => setReconciliationDate(event.target.value)}
            />
          </label>
          <label className="form-field">
            <span>{t("reconciliationCenter.externalSource")}</span>
            <select
              value={externalSource}
              onChange={(event) =>
                setExternalSource(event.target.value as ExternalSource)
              }
            >
              <option value="demo_custodian">{t("reconciliationCenter.demoCustodian")}</option>
              <option value="uploaded_file_placeholder">
                {t("reconciliationCenter.uploadedFilePlaceholder")}
              </option>
              <option value="manual_reference">
                {t("reconciliationCenter.manualReference")}
              </option>
            </select>
          </label>
          <div className="reconciliation-action-row">
            <button
              className="button button-primary"
              disabled={runMutation.isPending}
              type="button"
              onClick={() => runMutation.mutate()}
            >
              {runMutation.isPending
                ? t("common.loading")
                : t("reconciliationCenter.runReconciliation")}
            </button>
            <button
              className="button button-secondary"
              disabled={demoMutation.isPending}
              type="button"
              onClick={() => demoMutation.mutate()}
            >
              {t("reconciliationCenter.runDemo")}
            </button>
            <button
              className="button button-secondary"
              type="button"
              onClick={() => void historyQuery.refetch()}
            >
              {t("reconciliationCenter.refreshHistory")}
            </button>
          </div>
        </div>

        <div className="reconciliation-check-grid">
          {checkTypes.map((check) => (
            <label className="reconciliation-check" key={check}>
              <input
                checked={selectedChecks.includes(check)}
                type="checkbox"
                onChange={() => toggleCheck(check)}
              />
              <span>{t(`reconciliationCenter.checks.${check}`)}</span>
            </label>
          ))}
          <button
            className="button button--ghost"
            type="button"
            onClick={() => setShowTolerances((value) => !value)}
          >
            {showTolerances
              ? t("reconciliationCenter.hideTolerances")
              : t("reconciliationCenter.showTolerances")}
          </button>
        </div>

        {showTolerances ? (
          <div className="reconciliation-tolerance-grid">
            {Object.entries(tolerance).map(([key, value]) => (
              <label className="form-field" key={key}>
                <span>{t(`reconciliationCenter.tolerances.${key}`)}</span>
                <input
                  min="0"
                  step={key.includes("quantity") ? "0.0001" : "1"}
                  type="number"
                  value={value}
                  onChange={(event) =>
                    setTolerance((current) => ({
                      ...current,
                      [key]: Number(event.target.value),
                    }))
                  }
                />
              </label>
            ))}
          </div>
        ) : null}
      </section>

      {hasError ? (
        <ErrorBanner
          title={t("reconciliationCenter.apiError")}
          message={t("reconciliationCenter.apiErrorDetail")}
        />
      ) : null}

      {isLoading ? <LoadingState label={t("common.loading")} /> : null}

      <section className="risk-monitor-kpi-grid reconciliation-kpi-grid">
        {kpis.map((kpi) => (
          <ReconMetricCard key={kpi.label} {...kpi} />
        ))}
      </section>

      <nav
        className="risk-monitor-tabs reconciliation-tabs"
        aria-label={t("reconciliationCenter.tabsLabel")}
      >
        {tabs.map((tab) => (
          <button
            key={tab}
            className={`risk-monitor-tab ${activeTab === tab ? "risk-monitor-tab--active" : ""}`}
            type="button"
            onClick={() => setActiveTab(tab)}
          >
            <span>{t(`reconciliationCenter.tabs.${tab}`)}</span>
          </button>
        ))}
      </nav>

      {!result && activeTab !== "register" ? (
        <EmptyState
          title={t("reconciliationCenter.emptyTitle")}
          message={t("reconciliationCenter.emptyMessage")}
        />
      ) : null}

      {result && activeTab === "overview" ? (
        <OverviewTab
          result={result}
          breaks={breakRegister}
          sourceModules={sourceModules}
          t={t}
          onSelectBreak={(breakId) => {
            setSelectedBreakId(breakId);
            setActiveTab("review");
          }}
        />
      ) : null}
      {result && activeTab === "positions" ? (
        <PositionTab result={result} t={t} />
      ) : null}
      {result && activeTab === "cashFx" ? <CashFxTab result={result} t={t} /> : null}
      {result && activeTab === "prices" ? <PricesTab result={result} t={t} /> : null}
      {result && activeTab === "tradesPnl" ? (
        <TradesPnlTab result={result} t={t} />
      ) : null}
      {activeTab === "register" ? (
        <BreakRegisterTab
          breaks={filteredBreaks}
          severityFilter={severityFilter}
          statusFilter={statusFilter}
          typeFilter={typeFilter}
          setSeverityFilter={setSeverityFilter}
          setStatusFilter={setStatusFilter}
          setTypeFilter={setTypeFilter}
          t={t}
          onSelectBreak={(breakId) => {
            setSelectedBreakId(breakId);
            setActiveTab("review");
          }}
        />
      ) : null}
      {activeTab === "review" ? (
        <ReviewTab
          selectedBreak={selectedBreak}
          reviewer={reviewer}
          reviewDecision={reviewDecision}
          reviewNote={reviewNote}
          isSubmitting={reviewMutation.isPending}
          setReviewer={setReviewer}
          setReviewDecision={setReviewDecision}
          setReviewNote={setReviewNote}
          submitReview={(action) => reviewMutation.mutate(action)}
          t={t}
        />
      ) : null}
      {activeTab === "reports" ? (
        <ReportsExportsTab
          csvPreview={csvPreview}
          historyItems={historyQuery.data?.items ?? []}
          reportMessage={reportMessage}
          result={result}
          isGenerating={reportMutation.isPending}
          onExportCsv={() => void exportCsv()}
          onGenerateReport={() => reportMutation.mutate()}
          onLoadHistory={(runId) => void loadHistoryItem(runId)}
          t={t}
        />
      ) : null}
      {result && activeTab === "methodology" ? (
        <MethodologyTab result={result} statusDetail={statusQuery.data?.detail ?? ""} t={t} />
      ) : null}
      {result && activeTab === "commentary" ? (
        <AthenaAICommentaryCard
          commentary={result.athena_ai_commentary}
          title={t("reconciliationCenter.athenaCommentary")}
        />
      ) : null}
    </div>
  );
}

function OverviewTab({
  breaks,
  onSelectBreak,
  result,
  sourceModules,
  t,
}: {
  breaks: ReconciliationBreak[];
  onSelectBreak: (breakId: string) => void;
  result: ReconciliationRunResult;
  sourceModules: string[];
  t: (key: string) => string;
}) {
  const importantBreaks = breaks
    .filter((item) => item.severity === "critical" || item.severity === "high")
    .slice(0, 5);
  return (
    <section className="risk-monitor-panel reconciliation-overview-grid">
      <article className="risk-monitor-section-card">
        <header className="risk-monitor-section-card__header">
          <h2>{t("reconciliationCenter.overviewTitle")}</h2>
          <p>{result.athena_ai_commentary?.summary ?? t("reconciliationCenter.overviewDescription")}</p>
        </header>
        <div className="reconciliation-status-strip">
          <StatusBadge
            label={statusLabel(result.overall_status, t)}
            variant={overallStatusVariant(result.overall_status)}
          />
          <span>{result.portfolio_name}</span>
          <span>{formatDate(result.reconciliation_date)}</span>
          <span>{sourceLabel(result.external_source, t)}</span>
        </div>
        <SummaryGrid
          rows={[
            [t("reconciliationCenter.totalBreaks"), result.total_breaks],
            [t("reconciliationCenter.openBreaks"), result.open_breaks],
            [t("reconciliationCenter.criticalBreaks"), result.critical_breaks],
            [t("reconciliationCenter.positionBreaks"), result.breaks_by_type.position ?? 0],
            [t("reconciliationCenter.cashBreaks"), result.breaks_by_type.cash ?? 0],
            [t("reconciliationCenter.priceBreaks"), result.breaks_by_type.price ?? 0],
            [t("reconciliationCenter.tradeBreaks"), result.breaks_by_type.trade ?? 0],
            [t("reconciliationCenter.pnlBreaks"), result.breaks_by_type.pnl ?? 0],
          ]}
        />
      </article>

      <article className="risk-monitor-section-card">
        <header className="risk-monitor-section-card__header">
          <h2>{t("reconciliationCenter.priorityBreaks")}</h2>
          <p>{t("reconciliationCenter.priorityBreaksDescription")}</p>
        </header>
        <div className="reconciliation-break-list">
          {importantBreaks.map((item) => (
            <button
              className={`reconciliation-break-list__item reconciliation-break-list__item--${item.severity}`}
              key={item.break_id}
              type="button"
              onClick={() => onSelectBreak(item.break_id)}
            >
              <span>{item.break_type}</span>
              <strong>{item.symbol ?? item.metric}</strong>
              <small>{item.explanation}</small>
            </button>
          ))}
          {!importantBreaks.length ? (
            <EmptyState
              title={t("reconciliationCenter.noPriorityBreaks")}
              message={t("reconciliationCenter.noPriorityBreaksMessage")}
            />
          ) : null}
        </div>
      </article>

      <article className="risk-monitor-section-card">
        <header className="risk-monitor-section-card__header">
          <h2>{t("reconciliationCenter.sourceModules")}</h2>
          <p>{t("reconciliationCenter.sourceModulesDescription")}</p>
        </header>
        <div className="reconciliation-source-grid">
          {sourceModules.map((module) => (
            <div className="reconciliation-source-card" key={module}>
              <StatusBadge label={t("common.connectedInputs")} variant="info" />
              <strong>{module}</strong>
              <span>{moduleDescription(module, t)}</span>
            </div>
          ))}
        </div>
      </article>

      <article className="risk-monitor-section-card">
        <header className="risk-monitor-section-card__header">
          <h2>{t("reconciliationCenter.warnings")}</h2>
          <p>{t("reconciliationCenter.warningsDescription")}</p>
        </header>
        <ListBlock items={result.warnings} empty={t("reconciliationCenter.noWarnings")} />
      </article>
    </section>
  );
}

function PositionTab({
  result,
  t,
}: {
  result: ReconciliationRunResult;
  t: (key: string) => string;
}) {
  return (
    <section className="risk-monitor-section-card">
      <header className="risk-monitor-section-card__header">
        <h2>{t("reconciliationCenter.positionReconciliation")}</h2>
        <p>{t("reconciliationCenter.positionDescription")}</p>
      </header>
      <Table
        columns={[
          t("workflow.symbol"),
          t("reconciliationCenter.internalQuantity"),
          t("reconciliationCenter.externalQuantity"),
          t("reconciliationCenter.difference"),
          t("reconciliationCenter.internalValue"),
          t("reconciliationCenter.externalValue"),
          t("reconciliationCenter.status"),
          t("reconciliationCenter.severity"),
        ]}
        rows={result.position_breaks.map((row) => [
          <strong key="symbol">{row.symbol}</strong>,
          formatNumber(row.internal_quantity),
          formatNumber(row.external_quantity),
          formatNumber(row.quantity_difference),
          formatMoney(row.internal_market_value),
          formatMoney(row.external_market_value),
          statusText(row.status),
          <SeverityBadge key="severity" severity={row.severity} />,
        ])}
      />
    </section>
  );
}

function CashFxTab({
  result,
  t,
}: {
  result: ReconciliationRunResult;
  t: (key: string) => string;
}) {
  return (
    <section className="risk-monitor-panel reconciliation-two-column">
      <article className="risk-monitor-section-card">
        <header className="risk-monitor-section-card__header">
          <h2>{t("reconciliationCenter.cashReconciliation")}</h2>
          <p>{t("reconciliationCenter.cashDescription")}</p>
        </header>
        <Table
          columns={[
            t("reconciliationCenter.currency"),
            t("reconciliationCenter.internalCash"),
            t("reconciliationCenter.externalCash"),
            t("reconciliationCenter.difference"),
            t("reconciliationCenter.tolerance"),
            t("reconciliationCenter.status"),
            t("reconciliationCenter.severity"),
          ]}
          rows={result.cash_breaks.map((row) => [
            row.currency,
            formatMoney(row.internal_cash, row.currency),
            formatMoney(row.external_cash, row.currency),
            formatMoney(row.cash_difference, row.currency),
            formatMoney(row.tolerance, row.currency),
            statusText(row.status),
            <SeverityBadge key="severity" severity={row.severity} />,
          ])}
        />
      </article>
      <article className="risk-monitor-section-card">
        <header className="risk-monitor-section-card__header">
          <h2>{t("reconciliationCenter.fxReconciliation")}</h2>
          <p>{t("reconciliationCenter.fxDescription")}</p>
        </header>
        {result.fx_breaks.length ? (
          <Table
            columns={[
              t("reconciliationCenter.currency"),
              t("reconciliationCenter.internalFxRate"),
              t("reconciliationCenter.externalFxRate"),
              t("reconciliationCenter.difference"),
              t("reconciliationCenter.translationDifference"),
              t("reconciliationCenter.status"),
              t("reconciliationCenter.severity"),
            ]}
            rows={result.fx_breaks.map((row) => [
              row.currency,
              formatNumber(row.internal_fx_rate),
              formatNumber(row.external_fx_rate),
              formatNumber(row.fx_difference),
              formatMoney(row.translation_difference),
              statusText(row.status),
              <SeverityBadge key="severity" severity={row.severity} />,
            ])}
          />
        ) : (
          <EmptyState
            title={t("reconciliationCenter.noFxBreaks")}
            message={t("reconciliationCenter.noFxBreaksMessage")}
          />
        )}
      </article>
    </section>
  );
}

function PricesTab({
  result,
  t,
}: {
  result: ReconciliationRunResult;
  t: (key: string) => string;
}) {
  return (
    <section className="risk-monitor-section-card">
      <header className="risk-monitor-section-card__header">
        <h2>{t("reconciliationCenter.priceReconciliation")}</h2>
        <p>{t("reconciliationCenter.priceDescription")}</p>
      </header>
      <Table
        columns={[
          t("workflow.symbol"),
          t("reconciliationCenter.internalPrice"),
          t("reconciliationCenter.externalPrice"),
          t("reconciliationCenter.differenceBps"),
          t("reconciliationCenter.internalTimestamp"),
          t("reconciliationCenter.externalTimestamp"),
          t("reconciliationCenter.status"),
          t("reconciliationCenter.severity"),
        ]}
        rows={result.price_breaks.map((row) => [
          <strong key="symbol">{row.symbol}</strong>,
          formatMoney(row.internal_price),
          formatMoney(row.external_price),
          formatNumber(row.price_difference_bps),
          row.internal_price_timestamp ?? "--",
          row.external_price_timestamp ?? "--",
          statusText(row.status),
          <SeverityBadge key="severity" severity={row.severity} />,
        ])}
      />
    </section>
  );
}

function TradesPnlTab({
  result,
  t,
}: {
  result: ReconciliationRunResult;
  t: (key: string) => string;
}) {
  return (
    <section className="risk-monitor-panel reconciliation-two-column">
      <article className="risk-monitor-section-card">
        <header className="risk-monitor-section-card__header">
          <h2>{t("reconciliationCenter.tradeReconciliation")}</h2>
          <p>{t("reconciliationCenter.tradeDescription")}</p>
        </header>
        <Table
          columns={[
            t("reconciliationCenter.tradeId"),
            t("workflow.symbol"),
            t("reconciliationCenter.action"),
            t("reconciliationCenter.quantity"),
            t("reconciliationCenter.internalValue"),
            t("reconciliationCenter.externalValue"),
            t("reconciliationCenter.status"),
            t("reconciliationCenter.severity"),
          ]}
          rows={result.trade_breaks.map((row) => [
            row.trade_id,
            row.symbol,
            row.action,
            formatNumber(row.quantity),
            formatMoney(row.internal_trade_value),
            formatMoney(row.external_trade_value),
            statusText(row.status),
            <SeverityBadge key="severity" severity={row.severity} />,
          ])}
        />
      </article>
      <article className="risk-monitor-section-card">
        <header className="risk-monitor-section-card__header">
          <h2>{t("reconciliationCenter.pnlReconciliation")}</h2>
          <p>{t("reconciliationCenter.pnlDescription")}</p>
        </header>
        <Table
          columns={[
            t("reconciliationCenter.internalPnl"),
            t("reconciliationCenter.externalPnl"),
            t("reconciliationCenter.unexplainedPnl"),
            t("reconciliationCenter.tolerance"),
            t("reconciliationCenter.status"),
            t("reconciliationCenter.severity"),
          ]}
          rows={result.pnl_breaks.map((row) => [
            formatMoney(row.internal_total_pnl),
            formatMoney(row.external_total_pnl),
            formatMoney(row.unexplained_pnl),
            formatMoney(row.tolerance),
            statusText(row.status),
            <SeverityBadge key="severity" severity={row.severity} />,
          ])}
        />
      </article>
    </section>
  );
}

function BreakRegisterTab({
  breaks,
  onSelectBreak,
  setSeverityFilter,
  setStatusFilter,
  setTypeFilter,
  severityFilter,
  statusFilter,
  t,
  typeFilter,
}: {
  breaks: ReconciliationBreak[];
  onSelectBreak: (breakId: string) => void;
  setSeverityFilter: (value: BreakSeverity | "all") => void;
  setStatusFilter: (value: BreakStatus | "all") => void;
  setTypeFilter: (value: BreakType | "all") => void;
  severityFilter: BreakSeverity | "all";
  statusFilter: BreakStatus | "all";
  t: (key: string) => string;
  typeFilter: BreakType | "all";
}) {
  return (
    <section className="risk-monitor-section-card">
      <header className="risk-monitor-section-card__header">
        <h2>{t("reconciliationCenter.breakRegister")}</h2>
        <p>{t("reconciliationCenter.breakRegisterDescription")}</p>
      </header>
      <div className="reconciliation-filter-row">
        <FilterSelect
          label={t("reconciliationCenter.severity")}
          value={severityFilter}
          options={["all", "low", "medium", "high", "critical"]}
          onChange={(value) => setSeverityFilter(value as BreakSeverity | "all")}
          t={t}
        />
        <FilterSelect
          label={t("reconciliationCenter.type")}
          value={typeFilter}
          options={["all", "position", "cash", "price", "trade", "pnl", "fx", "data_quality"]}
          onChange={(value) => setTypeFilter(value as BreakType | "all")}
          t={t}
        />
        <FilterSelect
          label={t("reconciliationCenter.status")}
          value={statusFilter}
          options={["all", "open", "under_review", "explained", "resolved", "ignored"]}
          onChange={(value) => setStatusFilter(value as BreakStatus | "all")}
          t={t}
        />
      </div>
      <Table
        columns={[
          t("reconciliationCenter.type"),
          t("workflow.symbol"),
          t("reconciliationCenter.metric"),
          t("reconciliationCenter.difference"),
          t("reconciliationCenter.severity"),
          t("reconciliationCenter.status"),
          t("reconciliationCenter.sourceModule"),
          t("reconciliationCenter.actions"),
        ]}
        rows={breaks.map((item) => [
          item.break_type,
          item.symbol ?? "--",
          item.metric,
          formatValue(item.difference),
          <SeverityBadge key="severity" severity={item.severity} />,
          <StatusBadge key="status" label={statusText(item.status)} variant={statusVariant(item.status)} />,
          item.source_module,
          <button
            className="reconciliation-link-button"
            key="action"
            type="button"
            onClick={() => onSelectBreak(item.break_id)}
          >
            {t("reconciliationCenter.review")}
          </button>,
        ])}
      />
      {!breaks.length ? (
        <EmptyState
          title={t("reconciliationCenter.noBreaks")}
          message={t("reconciliationCenter.noBreaksMessage")}
        />
      ) : null}
    </section>
  );
}

function ReviewTab({
  isSubmitting,
  reviewer,
  reviewDecision,
  reviewNote,
  selectedBreak,
  setReviewer,
  setReviewDecision,
  setReviewNote,
  submitReview,
  t,
}: {
  isSubmitting: boolean;
  reviewer: string;
  reviewDecision: string;
  reviewNote: string;
  selectedBreak: ReconciliationBreak | null;
  setReviewer: (value: string) => void;
  setReviewDecision: (value: string) => void;
  setReviewNote: (value: string) => void;
  submitReview: (action: ReviewAction) => void;
  t: (key: string) => string;
}) {
  if (!selectedBreak) {
    return (
      <EmptyState
        title={t("reconciliationCenter.noSelectedBreak")}
        message={t("reconciliationCenter.noSelectedBreakMessage")}
      />
    );
  }
  return (
    <section className="risk-monitor-panel reconciliation-review-grid">
      <article className="risk-monitor-section-card">
        <header className="risk-monitor-section-card__header">
          <h2>{t("reconciliationCenter.reviewWorkflow")}</h2>
          <p>{t("reconciliationCenter.reviewWorkflowDescription")}</p>
        </header>
        <div className="reconciliation-break-detail">
          <StatusBadge
            label={selectedBreak.severity}
            variant={severityVariant(selectedBreak.severity)}
          />
          <StatusBadge
            label={statusText(selectedBreak.status)}
            variant={statusVariant(selectedBreak.status)}
          />
          <Definition label={t("reconciliationCenter.breakId")} value={selectedBreak.break_id} />
          <Definition label={t("reconciliationCenter.type")} value={selectedBreak.break_type} />
          <Definition label={t("workflow.symbol")} value={selectedBreak.symbol ?? "--"} />
          <Definition label={t("reconciliationCenter.metric")} value={selectedBreak.metric} />
          <Definition label={t("reconciliationCenter.internalValue")} value={formatValue(selectedBreak.internal_value)} />
          <Definition label={t("reconciliationCenter.externalValue")} value={formatValue(selectedBreak.external_value)} />
          <Definition label={t("reconciliationCenter.difference")} value={formatValue(selectedBreak.difference)} />
          <Definition label={t("reconciliationCenter.tolerance")} value={formatValue(selectedBreak.tolerance)} />
        </div>
        <div className="reconciliation-explanation-box">
          <h3>{t("reconciliationCenter.explanation")}</h3>
          <p>{selectedBreak.explanation}</p>
          <h3>{t("reconciliationCenter.suggestedAction")}</h3>
          <p>{selectedBreak.suggested_action}</p>
        </div>
      </article>

      <article className="risk-monitor-section-card">
        <header className="risk-monitor-section-card__header">
          <h2>{t("reconciliationCenter.reviewActions")}</h2>
          <p>{t("reconciliationCenter.reviewActionsDescription")}</p>
        </header>
        <div className="reconciliation-review-form">
          <label className="form-field">
            <span>{t("reconciliationCenter.reviewer")}</span>
            <input value={reviewer} onChange={(event) => setReviewer(event.target.value)} />
          </label>
          <label className="form-field">
            <span>{t("reconciliationCenter.decision")}</span>
            <input
              value={reviewDecision}
              onChange={(event) => setReviewDecision(event.target.value)}
            />
          </label>
          <label className="form-field reconciliation-review-note">
            <span>{t("reconciliationCenter.note")}</span>
            <textarea
              value={reviewNote}
              onChange={(event) => setReviewNote(event.target.value)}
            />
          </label>
          <div className="reconciliation-review-actions">
            {reviewActions.map((action) => (
              <button
                className="button button-secondary"
                disabled={isSubmitting}
                key={action}
                type="button"
                onClick={() => submitReview(action)}
              >
                {t(`reconciliationCenter.reviewActionLabels.${action}`)}
              </button>
            ))}
          </div>
        </div>
        <div className="reconciliation-history-list">
          <h3>{t("reconciliationCenter.reviewHistory")}</h3>
          {selectedBreak.review_history.map((event) => (
            <div key={`${event.action}-${event.timestamp}`}>
              <strong>{t(`reconciliationCenter.reviewActionLabels.${event.action}`)}</strong>
              <span>{event.reviewer} / {formatDate(event.timestamp)}</span>
              <p>{event.note ?? event.decision ?? "--"}</p>
            </div>
          ))}
          {!selectedBreak.review_history.length ? (
            <p>{t("reconciliationCenter.noReviewHistory")}</p>
          ) : null}
        </div>
      </article>
    </section>
  );
}

function ReportsExportsTab({
  csvPreview,
  historyItems,
  isGenerating,
  onExportCsv,
  onGenerateReport,
  onLoadHistory,
  reportMessage,
  result,
  t,
}: {
  csvPreview: string;
  historyItems: Array<{
    run_id: string;
    portfolio_name: string;
    overall_status: OverallStatus;
    total_breaks: number;
    generated_at: string;
  }>;
  isGenerating: boolean;
  onExportCsv: () => void;
  onGenerateReport: () => void;
  onLoadHistory: (runId: string) => void;
  reportMessage: string;
  result: ReconciliationRunResult | null;
  t: (key: string) => string;
}) {
  return (
    <section className="risk-monitor-panel reconciliation-two-column">
      <article className="risk-monitor-section-card">
        <header className="risk-monitor-section-card__header">
          <h2>{t("reconciliationCenter.reportsExports")}</h2>
          <p>{t("reconciliationCenter.reportsExportsDescription")}</p>
        </header>
        <div className="reconciliation-export-actions">
          <button
            className="button button-primary"
            disabled={!result || isGenerating}
            type="button"
            onClick={onGenerateReport}
          >
            {isGenerating
              ? t("common.loading")
              : t("reconciliationCenter.generateReconciliationReport")}
          </button>
          <button
            className="button button-secondary"
            disabled={!result}
            type="button"
            onClick={onExportCsv}
          >
            {t("reconciliationCenter.exportCsv")}
          </button>
          <Link className="button button-secondary" to="/reports-center">
            {t("reconciliationCenter.openReportsCenter")}
          </Link>
        </div>
        {reportMessage ? <p className="status-message">{reportMessage}</p> : null}
        <pre className="reconciliation-csv-preview">
          {csvPreview || t("reconciliationCenter.noCsvPreview")}
        </pre>
      </article>
      <article className="risk-monitor-section-card">
        <header className="risk-monitor-section-card__header">
          <h2>{t("reconciliationCenter.history")}</h2>
          <p>{t("reconciliationCenter.historyDescription")}</p>
        </header>
        <div className="reconciliation-history-list">
          {historyItems.map((item) => (
            <button
              key={item.run_id}
              type="button"
              onClick={() => onLoadHistory(item.run_id)}
            >
              <strong>{item.portfolio_name}</strong>
              <span>{formatDate(item.generated_at)} / {item.total_breaks} {t("reconciliationCenter.breaks")}</span>
              <StatusBadge
                label={statusLabel(item.overall_status, t)}
                variant={overallStatusVariant(item.overall_status)}
              />
            </button>
          ))}
          {!historyItems.length ? (
            <p>{t("reconciliationCenter.noHistory")}</p>
          ) : null}
        </div>
      </article>
    </section>
  );
}

function MethodologyTab({
  result,
  statusDetail,
  t,
}: {
  result: ReconciliationRunResult;
  statusDetail: string;
  t: (key: string) => string;
}) {
  return (
    <section className="risk-monitor-panel reconciliation-methodology-grid">
      <article className="risk-monitor-section-card">
        <header className="risk-monitor-section-card__header">
          <h2>{t("reconciliationCenter.methodology")}</h2>
          <p>{statusDetail}</p>
        </header>
        <SummaryGrid
          rows={[
            [t("reconciliationCenter.positionQuantityTolerance"), result.methodology.tolerances.position_quantity_tolerance],
            [t("reconciliationCenter.marketValueTolerance"), formatMoney(result.methodology.tolerances.market_value_tolerance)],
            [t("reconciliationCenter.cashTolerance"), formatMoney(result.methodology.tolerances.cash_tolerance)],
            [t("reconciliationCenter.priceToleranceBps"), result.methodology.tolerances.price_tolerance_bps],
            [t("reconciliationCenter.pnlTolerance"), formatMoney(result.methodology.tolerances.pnl_tolerance)],
          ]}
        />
        <ListBlock title={t("reconciliationCenter.checksPerformed")} items={result.checks_performed.map((item) => t(`reconciliationCenter.checks.${item}`))} />
      </article>
      <article className="risk-monitor-section-card">
        <header className="risk-monitor-section-card__header">
          <h2>{t("reconciliationCenter.dataQuality")}</h2>
          <p>{t("reconciliationCenter.dataQualityDescription")}</p>
        </header>
        <ListBlock title={t("common.dataSource")} items={result.methodology.data_sources} />
        <ListBlock title={t("common.assumptions")} items={result.methodology.assumptions} />
        <ListBlock title={t("common.limitations")} items={result.limitations} />
        <p className="reconciliation-disclaimer">
          {t("reconciliationCenter.notInvestmentAdvice")}
        </p>
      </article>
    </section>
  );
}

function ReconMetricCard({
  label,
  tone,
  value,
}: {
  label: string;
  tone: "neutral" | "positive" | "negative" | "warning";
  value: ReactNode;
}) {
  return (
    <div className={`risk-monitor-metric-card reconciliation-metric-card reconciliation-metric-card--${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function Table({
  columns,
  rows,
}: {
  columns: string[];
  rows: ReactNode[][];
}) {
  return (
    <div className="reconciliation-table">
      <table>
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column}>{column}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, rowIndex) => (
            <tr key={`row-${rowIndex}`}>
              {row.map((cell, cellIndex) => (
                <td key={`cell-${rowIndex}-${cellIndex}`}>{cell}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {!rows.length ? (
        <div className="reconciliation-table-empty">No rows</div>
      ) : null}
    </div>
  );
}

function SeverityBadge({ severity }: { severity?: BreakSeverity | null }) {
  if (!severity) return <span>--</span>;
  return (
    <StatusBadge
      label={severity}
      variant={severityVariant(severity)}
    />
  );
}

function FilterSelect({
  label,
  onChange,
  options,
  t,
  value,
}: {
  label: string;
  onChange: (value: string) => void;
  options: string[];
  t: (key: string) => string;
  value: string;
}) {
  return (
    <label className="form-field">
      <span>{label}</span>
      <select value={value} onChange={(event) => onChange(event.target.value)}>
        {options.map((option) => (
          <option key={option} value={option}>
            {option === "all" ? t("common.all") : statusText(option)}
          </option>
        ))}
      </select>
    </label>
  );
}

function SummaryGrid({ rows }: { rows: Array<[string, ReactNode]> }) {
  return (
    <div className="reconciliation-summary-grid">
      {rows.map(([label, value]) => (
        <Definition key={label} label={label} value={value} />
      ))}
    </div>
  );
}

function Definition({ label, value }: { label: string; value: ReactNode }) {
  return (
    <div className="reconciliation-definition">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function ListBlock({
  empty,
  items,
  title,
}: {
  empty?: string;
  items: string[];
  title?: string;
}) {
  return (
    <div className="reconciliation-list-block">
      {title ? <h3>{title}</h3> : null}
      {items.length ? (
        <ul>
          {items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      ) : (
        <p>{empty ?? "--"}</p>
      )}
    </div>
  );
}

function buildKpis(
  result: ReconciliationRunResult | null,
  lastRun: { generated_at: string } | undefined,
  t: (key: string) => string,
) {
  const largestDifference = result
    ? Math.max(
        0,
        ...result.breaks
          .map((item) =>
            typeof item.difference === "number" ? Math.abs(item.difference) : 0,
          ),
      )
    : 0;
  return [
    {
      label: t("reconciliationCenter.overallStatus"),
      value: result ? statusLabel(result.overall_status, t) : "--",
      tone: result ? kpiTone(result.overall_status) : "neutral",
    },
    {
      label: t("reconciliationCenter.totalBreaks"),
      value: result?.total_breaks ?? "--",
      tone: result?.total_breaks ? "warning" : "positive",
    },
    {
      label: t("reconciliationCenter.openBreaks"),
      value: result?.open_breaks ?? "--",
      tone: result?.open_breaks ? "warning" : "positive",
    },
    {
      label: t("reconciliationCenter.criticalBreaks"),
      value: result?.critical_breaks ?? "--",
      tone: result?.critical_breaks ? "negative" : "positive",
    },
    {
      label: t("reconciliationCenter.positionBreaks"),
      value: result?.breaks_by_type.position ?? "--",
      tone: result?.breaks_by_type.position ? "warning" : "neutral",
    },
    {
      label: t("reconciliationCenter.cashBreaks"),
      value: result?.breaks_by_type.cash ?? "--",
      tone: result?.breaks_by_type.cash ? "warning" : "neutral",
    },
    {
      label: t("reconciliationCenter.priceBreaks"),
      value: result?.breaks_by_type.price ?? "--",
      tone: result?.breaks_by_type.price ? "warning" : "neutral",
    },
    {
      label: t("reconciliationCenter.pnlBreaks"),
      value: result?.breaks_by_type.pnl ?? "--",
      tone: result?.breaks_by_type.pnl ? "negative" : "neutral",
    },
    {
      label: t("reconciliationCenter.largestDifference"),
      value: result ? formatNumber(largestDifference) : "--",
      tone: largestDifference ? "warning" : "neutral",
    },
    {
      label: t("reconciliationCenter.lastRun"),
      value: result ? formatDate(result.generated_at) : lastRun ? formatDate(lastRun.generated_at) : "--",
      tone: "neutral",
    },
  ] as Array<{
    label: string;
    value: ReactNode;
    tone: "neutral" | "positive" | "negative" | "warning";
  }>;
}

function kpiTone(status: OverallStatus) {
  if (status === "reconciled") return "positive";
  if (status === "critical_breaks") return "negative";
  return "warning";
}

function overallStatusVariant(status: OverallStatus) {
  if (status === "reconciled") return "success";
  if (status === "critical_breaks") return "danger";
  if (status === "material_breaks") return "warning";
  return "info";
}

function severityVariant(severity: BreakSeverity) {
  if (severity === "critical" || severity === "high") return "danger";
  if (severity === "medium") return "warning";
  return "info";
}

function statusVariant(status: BreakStatus | string) {
  if (status === "resolved" || status === "explained") return "success";
  if (status === "under_review") return "warning";
  if (status === "ignored") return "neutral";
  return "info";
}

function statusLabel(status: OverallStatus, t: (key: string) => string) {
  return t(`reconciliationCenter.overallStatusLabels.${status}`);
}

function sourceLabel(source: ExternalSource, t: (key: string) => string) {
  if (source === "demo_custodian") return t("reconciliationCenter.demoCustodian");
  if (source === "uploaded_file_placeholder") return t("reconciliationCenter.uploadedFilePlaceholder");
  return t("reconciliationCenter.manualReference");
}

function statusText(value: string) {
  return value.replace(/_/g, " ");
}

function moduleDescription(moduleName: string, t: (key: string) => string) {
  const key = moduleName
    .toLowerCase()
    .replace(/&/g, "and")
    .replace(/[^a-z0-9]+/g, "_")
    .replace(/^_|_$/g, "");
  return t(`reconciliationCenter.moduleDescriptions.${key}`);
}

function formatMoney(value: number | null | undefined, currency = "USD") {
  if (value === null || value === undefined || Number.isNaN(value)) return "--";
  return new Intl.NumberFormat("en-CA", {
    currency,
    maximumFractionDigits: 2,
    style: "currency",
  }).format(value);
}

function formatNumber(value: number | null | undefined) {
  if (value === null || value === undefined || Number.isNaN(value)) return "--";
  return new Intl.NumberFormat("en-CA", {
    maximumFractionDigits: 4,
  }).format(value);
}

function formatValue(value: number | string | null | undefined) {
  if (value === null || value === undefined) return "--";
  if (typeof value === "number") return formatNumber(value);
  return value;
}

function formatDate(value: string) {
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toLocaleString();
}
