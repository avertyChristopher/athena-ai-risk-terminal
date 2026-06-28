import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { AthenaAICommentaryCard } from "../../../components/ai/AthenaAICommentaryCard";
import { EmptyState } from "../../../components/ui/EmptyState";
import { ErrorBanner } from "../../../components/ui/ErrorBanner";
import { LoadingState } from "../../../components/ui/LoadingState";
import { StatusBadge, type StatusBadgeVariant } from "../../../components/ui/StatusBadge";
import { usePortfolioContext } from "../../../context/PortfolioContext";
import { useTranslation } from "../../../hooks/useTranslation";
import { aiAnomalyCenterApi } from "../../../services/aiAnomalyCenterApi";
import { reportsCenterApi } from "../../../services/reportsCenterApi";
import type {
  AnomalyCategory,
  AnomalyRecord,
  AnomalyReviewAction,
  AnomalyScanResponse,
  AnomalyScanScope,
  AnomalySeverity,
  AnomalyStatus,
} from "../../../types/ai-anomaly-center";

type Tab =
  | "overview"
  | "register"
  | "marketPortfolio"
  | "tradesPnl"
  | "riskLimitsStress"
  | "reconciliationData"
  | "ratesOptions"
  | "review"
  | "reports"
  | "methodology"
  | "commentary";

const scanScopes: AnomalyScanScope[] = [
  "all",
  "market_data",
  "portfolio",
  "trades",
  "pnl",
  "risk",
  "reconciliation",
  "limits",
  "stress",
  "rates_options",
];

const severityOptions: AnomalySeverity[] = ["low", "medium", "high", "critical"];
const statusOptions: AnomalyStatus[] = ["open", "under_review", "explained", "resolved", "ignored"];
const categoryOptions: AnomalyCategory[] = [
  "market_data",
  "portfolio",
  "trades",
  "pnl",
  "risk",
  "reconciliation",
  "limits",
  "stress",
  "rates_options",
];

const tabs: Tab[] = [
  "overview",
  "register",
  "marketPortfolio",
  "tradesPnl",
  "riskLimitsStress",
  "reconciliationData",
  "ratesOptions",
  "review",
  "reports",
  "methodology",
  "commentary",
];

export function AIAnomalyCenterPage() {
  const { t, i18n } = useTranslation();
  const queryClient = useQueryClient();
  const { portfolios, selectedPortfolioId, selectedPortfolioName } = usePortfolioContext();
  const [portfolioId, setPortfolioId] = useState(selectedPortfolioId || "pf_004");
  const [scanScope, setScanScope] = useState<AnomalyScanScope>("all");
  const [lookbackDays, setLookbackDays] = useState(60);
  const [severityThreshold, setSeverityThreshold] = useState<AnomalySeverity>("low");
  const [activeTab, setActiveTab] = useState<Tab>("overview");
  const [scanResult, setScanResult] = useState<AnomalyScanResponse | null>(null);
  const [selectedAnomaly, setSelectedAnomaly] = useState<AnomalyRecord | null>(null);
  const [categoryFilter, setCategoryFilter] = useState<"" | AnomalyCategory>("");
  const [severityFilter, setSeverityFilter] = useState<"" | AnomalySeverity>("");
  const [statusFilter, setStatusFilter] = useState<"" | AnomalyStatus>("");
  const [sourceFilter, setSourceFilter] = useState("");
  const [reviewer, setReviewer] = useState("analyst");
  const [reviewNote, setReviewNote] = useState("");
  const [reviewDecision, setReviewDecision] = useState("");
  const [exportPreview, setExportPreview] = useState("");
  const [generatedReportId, setGeneratedReportId] = useState("");

  useEffect(() => {
    if (selectedPortfolioId && portfolioId !== selectedPortfolioId) {
      setPortfolioId(selectedPortfolioId);
    }
  }, [portfolioId, selectedPortfolioId]);

  const language = i18n.language?.startsWith("fr") ? "fr" : "en";

  const statusQuery = useQuery({
    queryKey: ["ai-anomaly-center-status"],
    queryFn: aiAnomalyCenterApi.status,
  });

  const anomaliesQuery = useQuery({
    queryKey: ["ai-anomaly-center-anomalies", portfolioId, severityFilter, statusFilter],
    queryFn: () =>
      aiAnomalyCenterApi.anomalies({
        portfolio_id: portfolioId || undefined,
        severity: severityFilter || undefined,
        status: statusFilter || undefined,
      }),
  });

  const scanMutation = useMutation({
    mutationFn: () =>
      aiAnomalyCenterApi.scan({
        portfolio_id: portfolioId || null,
        scan_scope: scanScope,
        lookback_days: lookbackDays,
        severity_threshold: severityThreshold,
        persist_results: true,
        language,
      }),
    onSuccess: async (payload) => {
      setScanResult(payload);
      setSelectedAnomaly(payload.anomaly_records[0] ?? null);
      setActiveTab("overview");
      await queryClient.invalidateQueries({ queryKey: ["ai-anomaly-center-anomalies"] });
    },
  });

  const reviewMutation = useMutation({
    mutationFn: (action: AnomalyReviewAction) => {
      if (!selectedAnomaly) throw new Error("No anomaly selected");
      return aiAnomalyCenterApi.review(selectedAnomaly.anomaly_id, {
        action,
        reviewer,
        note: reviewNote || null,
        decision: reviewDecision || null,
      });
    },
    onSuccess: async ({ anomaly }) => {
      setSelectedAnomaly(anomaly);
      setReviewNote("");
      setReviewDecision("");
      await queryClient.invalidateQueries({ queryKey: ["ai-anomaly-center-anomalies"] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (anomalyId: string) => aiAnomalyCenterApi.deleteAnomaly(anomalyId),
    onSuccess: async () => {
      setSelectedAnomaly(null);
      await queryClient.invalidateQueries({ queryKey: ["ai-anomaly-center-anomalies"] });
    },
  });

  const exportMutation = useMutation({
    mutationFn: aiAnomalyCenterApi.exportCsv,
    onSuccess: (payload) => {
      setExportPreview(payload.csv);
      setActiveTab("reports");
    },
  });

  const reportMutation = useMutation({
    mutationFn: () =>
      reportsCenterApi.generate({
        report_type: "ai_anomaly",
        portfolio_id: portfolioId || null,
        language,
        style: "executive",
        include_athena_commentary: true,
        include_methodology: true,
        include_limitations: true,
      }),
    onSuccess: (report) => {
      setGeneratedReportId(report.report_id);
      setActiveTab("reports");
    },
  });

  const sourceModules = statusQuery.data?.source_modules ?? scanResult?.methodology.data_sources ?? [];
  const registerRecords = useMemo(
    () => anomaliesQuery.data?.items ?? scanResult?.anomaly_records ?? [],
    [anomaliesQuery.data?.items, scanResult?.anomaly_records],
  );
  const filteredRecords = useMemo(
    () =>
      registerRecords.filter((record) => {
        const matchesCategory = !categoryFilter || record.category === categoryFilter;
        const matchesSource = !sourceFilter || record.source_module === sourceFilter;
        return matchesCategory && matchesSource;
      }),
    [categoryFilter, registerRecords, sourceFilter],
  );
  const topAnomalies = useMemo(
    () => [...registerRecords].sort((a, b) => b.anomaly_score - a.anomaly_score).slice(0, 6),
    [registerRecords],
  );
  const severityCounts = scanResult?.anomalies_by_severity ?? countBy(registerRecords, "severity");
  const categoryCounts = scanResult?.anomalies_by_category ?? countBy(registerRecords, "category");
  const recurringIssues = useMemo(() => {
    const counts = new Map<string, number>();
    registerRecords.forEach((record) => {
      const key = `${record.source_module}:${record.anomaly_type}:${record.metric_name}`;
      counts.set(key, (counts.get(key) ?? 0) + 1);
    });
    return [...counts.values()].filter((count) => count > 1).length;
  }, [registerRecords]);

  useEffect(() => {
    if (!selectedAnomaly && registerRecords.length) {
      setSelectedAnomaly(registerRecords[0]);
    }
  }, [registerRecords, selectedAnomaly]);

  const kpis = [
    {
      label: t("aiAnomalyCenter.kpis.totalAnomalies"),
      value: String(registerRecords.length),
      detail: t("aiAnomalyCenter.kpis.totalAnomaliesDetail"),
    },
    {
      label: t("aiAnomalyCenter.kpis.criticalAnomalies"),
      value: String(severityCounts.critical ?? 0),
      detail: t("aiAnomalyCenter.severities.critical"),
      tone: "danger" as const,
    },
    {
      label: t("aiAnomalyCenter.kpis.highAnomalies"),
      value: String(severityCounts.high ?? 0),
      detail: t("aiAnomalyCenter.severities.high"),
      tone: "warning" as const,
    },
    {
      label: t("aiAnomalyCenter.kpis.openAnomalies"),
      value: String(registerRecords.filter((record) => record.status === "open").length),
      detail: t("aiAnomalyCenter.statuses.open"),
    },
    {
      label: t("aiAnomalyCenter.kpis.sourceModulesScanned"),
      value: String(sourceModules.length),
      detail: t("aiAnomalyCenter.sourceCoverage"),
    },
    {
      label: t("aiAnomalyCenter.kpis.highestSeverity"),
      value: scanResult?.highest_severity
        ? t(`aiAnomalyCenter.severities.${scanResult.highest_severity}`)
        : t("common.unavailable"),
      detail: scanResult?.scan_id ?? t("aiAnomalyCenter.noScan"),
      tone: scanResult?.highest_severity === "critical" ? ("danger" as const) : undefined,
    },
    {
      label: t("aiAnomalyCenter.kpis.lastScan"),
      value: scanResult ? formatDate(scanResult.generated_at) : t("common.unavailable"),
      detail: scanResult ? `${scanResult.total_records_scanned} ${t("aiAnomalyCenter.recordsScanned")}` : t("aiAnomalyCenter.notRunYet"),
    },
    {
      label: t("aiAnomalyCenter.kpis.recurringIssues"),
      value: String(recurringIssues),
      detail: t("aiAnomalyCenter.recurrenceDetail"),
    },
  ];

  if (statusQuery.isError || anomaliesQuery.isError) {
    return (
      <div className="page ai-anomaly-page">
        <ErrorBanner
          title={t("aiAnomalyCenter.apiError")}
          message={t("aiAnomalyCenter.apiErrorDetail")}
          retryLabel={t("workflow.refresh")}
          onRetry={() => {
            void statusQuery.refetch();
            void anomaliesQuery.refetch();
          }}
        />
      </div>
    );
  }

  return (
    <div className="page ai-anomaly-page">
      <section className="ai-anomaly-hero">
        <div>
          <span className="equity-kicker">{t("aiAnomalyCenter.eyebrow")}</span>
          <h1>{t("aiAnomalyCenter.title")}</h1>
          <p>{t("aiAnomalyCenter.subtitle")}</p>
          <div className="ai-anomaly-hero__badges">
            <StatusBadge label={t("aiAnomalyCenter.ruleBasedDetection")} variant="info" />
            <StatusBadge label={t("aiAnomalyCenter.reviewWorkflow")} variant="warning" />
            <StatusBadge label={t("aiAnomalyCenter.persistedHistory")} variant="success" />
            <StatusBadge label={t("common.beta")} variant="warning" />
          </div>
        </div>

        <div className="ai-anomaly-command-panel">
          <label>
            {t("workflow.portfolio")}
            <select value={portfolioId} onChange={(event) => setPortfolioId(event.target.value)}>
              {portfolios.map((portfolio) => (
                <option key={portfolio.id} value={portfolio.id}>
                  {portfolio.name}
                </option>
              ))}
              {!portfolios.length ? <option value="pf_004">{selectedPortfolioName || "pf_004"}</option> : null}
            </select>
          </label>
          <label>
            {t("aiAnomalyCenter.scanScope")}
            <select value={scanScope} onChange={(event) => setScanScope(event.target.value as AnomalyScanScope)}>
              {scanScopes.map((scope) => (
                <option key={scope} value={scope}>
                  {scope === "all" ? t("common.all") : categoryLabel(scope, t)}
                </option>
              ))}
            </select>
          </label>
          <label>
            {t("aiAnomalyCenter.lookbackDays")}
            <input
              min={1}
              max={365}
              type="number"
              value={lookbackDays}
              onChange={(event) => setLookbackDays(Number(event.target.value))}
            />
          </label>
          <label>
            {t("aiAnomalyCenter.severityThreshold")}
            <select value={severityThreshold} onChange={(event) => setSeverityThreshold(event.target.value as AnomalySeverity)}>
              {severityOptions.map((severity) => (
                <option key={severity} value={severity}>
                  {t(`aiAnomalyCenter.severities.${severity}`)}
                </option>
              ))}
            </select>
          </label>
          <button
            className="button button--primary"
            disabled={scanMutation.isPending}
            type="button"
            onClick={() => scanMutation.mutate()}
          >
            {scanMutation.isPending ? t("common.loading") : t("aiAnomalyCenter.runScan")}
          </button>
          <button className="button" type="button" onClick={() => void anomaliesQuery.refetch()}>
            {t("aiAnomalyCenter.refreshAnomalies")}
          </button>
        </div>
      </section>

      <section className="ai-anomaly-kpi-grid" aria-label={t("aiAnomalyCenter.kpiLabel")}>
        {kpis.map((kpi) => (
          <article className={`ai-anomaly-kpi ai-anomaly-kpi--${kpi.tone ?? "neutral"}`} key={kpi.label}>
            <span>{kpi.label}</span>
            <strong>{kpi.value}</strong>
            <p>{kpi.detail}</p>
          </article>
        ))}
      </section>

      {scanMutation.isError ? (
        <ErrorBanner
          title={t("aiAnomalyCenter.scanFailed")}
          message={t("aiAnomalyCenter.scanFailedDetail")}
        />
      ) : null}

      <nav className="ai-anomaly-tabs" aria-label={t("aiAnomalyCenter.tabsLabel")}>
        {tabs.map((tab) => (
          <button
            className={activeTab === tab ? "ai-anomaly-tab ai-anomaly-tab--active" : "ai-anomaly-tab"}
            key={tab}
            type="button"
            onClick={() => setActiveTab(tab)}
          >
            {t(`aiAnomalyCenter.tabs.${tab}`)}
          </button>
        ))}
      </nav>

      {activeTab === "overview" ? (
        <OverviewPanel
          categoryCounts={categoryCounts}
          commentary={scanResult?.athena_ai_commentary ?? null}
          records={registerRecords}
          severityCounts={severityCounts}
          t={t}
          topAnomalies={topAnomalies}
          onSelect={(record) => {
            setSelectedAnomaly(record);
            setActiveTab("review");
          }}
        />
      ) : null}

      {activeTab === "register" ? (
        <RegisterPanel
          categoryFilter={categoryFilter}
          records={filteredRecords}
          selectedId={selectedAnomaly?.anomaly_id}
          severityFilter={severityFilter}
          sourceFilter={sourceFilter}
          sourceModules={[...new Set(registerRecords.map((record) => record.source_module))]}
          statusFilter={statusFilter}
          t={t}
          onCategoryFilter={setCategoryFilter}
          onDelete={(record) => deleteMutation.mutate(record.anomaly_id)}
          onSelect={setSelectedAnomaly}
          onSeverityFilter={setSeverityFilter}
          onSourceFilter={setSourceFilter}
          onStatusFilter={setStatusFilter}
        />
      ) : null}

      {activeTab === "marketPortfolio" ? (
        <CategoryGroupPanel
          description={t("aiAnomalyCenter.panels.marketPortfolioDescription")}
          records={recordsFor(registerRecords, ["market_data", "portfolio"])}
          t={t}
          title={t("aiAnomalyCenter.panels.marketPortfolio")}
          onSelect={(record) => {
            setSelectedAnomaly(record);
            setActiveTab("review");
          }}
        />
      ) : null}

      {activeTab === "tradesPnl" ? (
        <CategoryGroupPanel
          description={t("aiAnomalyCenter.panels.tradesPnlDescription")}
          records={recordsFor(registerRecords, ["trades", "pnl"])}
          t={t}
          title={t("aiAnomalyCenter.panels.tradesPnl")}
          onSelect={(record) => {
            setSelectedAnomaly(record);
            setActiveTab("review");
          }}
        />
      ) : null}

      {activeTab === "riskLimitsStress" ? (
        <CategoryGroupPanel
          description={t("aiAnomalyCenter.panels.riskLimitsStressDescription")}
          records={recordsFor(registerRecords, ["risk", "limits", "stress"])}
          t={t}
          title={t("aiAnomalyCenter.panels.riskLimitsStress")}
          onSelect={(record) => {
            setSelectedAnomaly(record);
            setActiveTab("review");
          }}
        />
      ) : null}

      {activeTab === "reconciliationData" ? (
        <CategoryGroupPanel
          description={t("aiAnomalyCenter.panels.reconciliationDataDescription")}
          records={recordsFor(registerRecords, ["reconciliation", "market_data"])}
          t={t}
          title={t("aiAnomalyCenter.panels.reconciliationData")}
          onSelect={(record) => {
            setSelectedAnomaly(record);
            setActiveTab("review");
          }}
        />
      ) : null}

      {activeTab === "ratesOptions" ? (
        <CategoryGroupPanel
          description={t("aiAnomalyCenter.panels.ratesOptionsDescription")}
          records={recordsFor(registerRecords, ["rates_options"])}
          t={t}
          title={t("aiAnomalyCenter.panels.ratesOptions")}
          onSelect={(record) => {
            setSelectedAnomaly(record);
            setActiveTab("review");
          }}
        />
      ) : null}

      {activeTab === "review" ? (
        <ReviewPanel
          anomaly={selectedAnomaly}
          decision={reviewDecision}
          isPending={reviewMutation.isPending}
          note={reviewNote}
          reviewer={reviewer}
          t={t}
          onAction={(action) => reviewMutation.mutate(action)}
          onDecision={setReviewDecision}
          onNote={setReviewNote}
          onReviewer={setReviewer}
        />
      ) : null}

      {activeTab === "reports" ? (
        <ReportsExportsPanel
          csv={exportPreview}
          generatedReportId={generatedReportId}
          isExporting={exportMutation.isPending}
          isGenerating={reportMutation.isPending}
          t={t}
          onExport={() => exportMutation.mutate()}
          onGenerate={() => reportMutation.mutate()}
        />
      ) : null}

      {activeTab === "methodology" ? (
        <MethodologyPanel
          limitations={statusQuery.data?.limitations ?? scanResult?.limitations ?? []}
          methodology={scanResult?.methodology ?? null}
          sourceModules={sourceModules}
          t={t}
        />
      ) : null}

      {activeTab === "commentary" ? (
        <AthenaAICommentaryCard
          commentary={scanResult?.athena_ai_commentary ?? null}
          title={t("aiAnomalyCenter.athenaCommentary")}
        />
      ) : null}

      {statusQuery.isLoading || anomaliesQuery.isLoading ? (
        <LoadingState label={t("common.loading")} />
      ) : null}
    </div>
  );
}

function OverviewPanel({
  categoryCounts,
  commentary,
  records,
  severityCounts,
  t,
  topAnomalies,
  onSelect,
}: {
  categoryCounts: Record<string, number>;
  commentary: AnomalyScanResponse["athena_ai_commentary"] | null;
  records: AnomalyRecord[];
  severityCounts: Record<string, number>;
  t: (key: string) => string;
  topAnomalies: AnomalyRecord[];
  onSelect: (record: AnomalyRecord) => void;
}) {
  return (
    <div className="ai-anomaly-overview-grid">
      <section className="analytics-section">
        <header className="analytics-section__header">
          <h2>{t("aiAnomalyCenter.anomalySummary")}</h2>
          <p>{t("aiAnomalyCenter.anomalySummaryDescription")}</p>
        </header>
        <div className="ai-anomaly-summary-grid">
          <CountCard title={t("aiAnomalyCenter.bySeverity")} counts={severityCounts} t={t} type="severity" />
          <CountCard title={t("aiAnomalyCenter.byCategory")} counts={categoryCounts} t={t} type="category" />
        </div>
      </section>

      <section className="analytics-section">
        <header className="analytics-section__header">
          <h2>{t("aiAnomalyCenter.topAnomalies")}</h2>
          <p>{t("aiAnomalyCenter.topAnomaliesDescription")}</p>
        </header>
        <AnomalyCardList records={topAnomalies} t={t} onSelect={onSelect} />
      </section>

      <AthenaAICommentaryCard
        commentary={commentary}
        className="ai-anomaly-commentary-panel"
        title={t("aiAnomalyCenter.athenaCommentary")}
      />

      <section className="analytics-section">
        <header className="analytics-section__header">
          <h2>{t("aiAnomalyCenter.controlPosture")}</h2>
          <p>{t("aiAnomalyCenter.controlPostureDescription")}</p>
        </header>
        <div className="ai-anomaly-control-grid">
          {["open", "under_review", "explained", "resolved", "ignored"].map((status) => (
            <article key={status}>
              <span>{t(`aiAnomalyCenter.statuses.${status}`)}</span>
              <strong>{records.filter((record) => record.status === status).length}</strong>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}

function RegisterPanel({
  categoryFilter,
  records,
  selectedId,
  severityFilter,
  sourceFilter,
  sourceModules,
  statusFilter,
  t,
  onCategoryFilter,
  onDelete,
  onSelect,
  onSeverityFilter,
  onSourceFilter,
  onStatusFilter,
}: {
  categoryFilter: "" | AnomalyCategory;
  records: AnomalyRecord[];
  selectedId?: string;
  severityFilter: "" | AnomalySeverity;
  sourceFilter: string;
  sourceModules: string[];
  statusFilter: "" | AnomalyStatus;
  t: (key: string) => string;
  onCategoryFilter: (value: "" | AnomalyCategory) => void;
  onDelete: (record: AnomalyRecord) => void;
  onSelect: (record: AnomalyRecord) => void;
  onSeverityFilter: (value: "" | AnomalySeverity) => void;
  onSourceFilter: (value: string) => void;
  onStatusFilter: (value: "" | AnomalyStatus) => void;
}) {
  return (
    <section className="analytics-section">
      <header className="analytics-section__header">
        <h2>{t("aiAnomalyCenter.anomalyRegister")}</h2>
        <p>{t("aiAnomalyCenter.registerDescription")}</p>
      </header>
      <div className="ai-anomaly-filter-grid">
        <label>
          {t("aiAnomalyCenter.category")}
          <select value={categoryFilter} onChange={(event) => onCategoryFilter(event.target.value as "" | AnomalyCategory)}>
            <option value="">{t("common.all")}</option>
            {categoryOptions.map((category) => (
              <option key={category} value={category}>
                {categoryLabel(category, t)}
              </option>
            ))}
          </select>
        </label>
        <label>
          {t("aiAnomalyCenter.severity")}
          <select value={severityFilter} onChange={(event) => onSeverityFilter(event.target.value as "" | AnomalySeverity)}>
            <option value="">{t("common.all")}</option>
            {severityOptions.map((severity) => (
              <option key={severity} value={severity}>
                {t(`aiAnomalyCenter.severities.${severity}`)}
              </option>
            ))}
          </select>
        </label>
        <label>
          {t("aiAnomalyCenter.status")}
          <select value={statusFilter} onChange={(event) => onStatusFilter(event.target.value as "" | AnomalyStatus)}>
            <option value="">{t("common.all")}</option>
            {statusOptions.map((status) => (
              <option key={status} value={status}>
                {t(`aiAnomalyCenter.statuses.${status}`)}
              </option>
            ))}
          </select>
        </label>
        <label>
          {t("aiAnomalyCenter.sourceModule")}
          <select value={sourceFilter} onChange={(event) => onSourceFilter(event.target.value)}>
            <option value="">{t("common.all")}</option>
            {sourceModules.map((source) => (
              <option key={source} value={source}>
                {source}
              </option>
            ))}
          </select>
        </label>
      </div>
      <AnomalyTable
        records={records}
        selectedId={selectedId}
        t={t}
        onDelete={onDelete}
        onSelect={onSelect}
      />
    </section>
  );
}

function CategoryGroupPanel({
  description,
  records,
  t,
  title,
  onSelect,
}: {
  description: string;
  records: AnomalyRecord[];
  t: (key: string) => string;
  title: string;
  onSelect: (record: AnomalyRecord) => void;
}) {
  return (
    <section className="analytics-section">
      <header className="analytics-section__header">
        <h2>{title}</h2>
        <p>{description}</p>
      </header>
      <AnomalyCardList records={records} t={t} onSelect={onSelect} />
    </section>
  );
}

function ReviewPanel({
  anomaly,
  decision,
  isPending,
  note,
  reviewer,
  t,
  onAction,
  onDecision,
  onNote,
  onReviewer,
}: {
  anomaly: AnomalyRecord | null;
  decision: string;
  isPending: boolean;
  note: string;
  reviewer: string;
  t: (key: string) => string;
  onAction: (action: AnomalyReviewAction) => void;
  onDecision: (value: string) => void;
  onNote: (value: string) => void;
  onReviewer: (value: string) => void;
}) {
  if (!anomaly) {
    return (
      <section className="analytics-section">
        <EmptyState
          title={t("aiAnomalyCenter.emptyReviewTitle")}
          message={t("aiAnomalyCenter.emptyReviewMessage")}
        />
      </section>
    );
  }

  return (
    <section className="analytics-section">
      <header className="analytics-section__header">
        <h2>{t("aiAnomalyCenter.reviewWorkflow")}</h2>
        <p>{t("aiAnomalyCenter.reviewWorkflowDescription")}</p>
      </header>
      <div className="ai-anomaly-review-grid">
        <article className="ai-anomaly-detail-card">
          <div className="ai-anomaly-card__header">
            <StatusBadge label={t(`aiAnomalyCenter.severities.${anomaly.severity}`)} variant={severityVariant(anomaly.severity)} />
            <StatusBadge label={t(`aiAnomalyCenter.statuses.${anomaly.status}`)} variant={statusVariant(anomaly.status)} />
          </div>
          <h3>{anomaly.title}</h3>
          <p>{anomaly.description}</p>
          <dl>
            <div>
              <dt>{t("aiAnomalyCenter.anomalyId")}</dt>
              <dd>{anomaly.anomaly_id}</dd>
            </div>
            <div>
              <dt>{t("aiAnomalyCenter.sourceModule")}</dt>
              <dd>{anomaly.source_module}</dd>
            </div>
            <div>
              <dt>{t("aiAnomalyCenter.metric")}</dt>
              <dd>{anomaly.metric_name}</dd>
            </div>
            <div>
              <dt>{t("aiAnomalyCenter.observed")}</dt>
              <dd>{formatValue(anomaly.observed_value)}</dd>
            </div>
            <div>
              <dt>{t("aiAnomalyCenter.threshold")}</dt>
              <dd>{formatValue(anomaly.threshold)}</dd>
            </div>
            <div>
              <dt>{t("aiAnomalyCenter.confidence")}</dt>
              <dd>{t(`aiAnomalyCenter.confidences.${anomaly.confidence}`)}</dd>
            </div>
          </dl>
          <div className="ai-anomaly-explanation">
            <strong>{t("aiAnomalyCenter.explanation")}</strong>
            <p>{anomaly.explanation}</p>
            <strong>{t("aiAnomalyCenter.suggestedAction")}</strong>
            <p>{anomaly.suggested_action}</p>
          </div>
        </article>

        <article className="ai-anomaly-review-card">
          <label>
            {t("aiAnomalyCenter.reviewer")}
            <input value={reviewer} onChange={(event) => onReviewer(event.target.value)} />
          </label>
          <label>
            {t("aiAnomalyCenter.reviewNote")}
            <textarea rows={4} value={note} onChange={(event) => onNote(event.target.value)} />
          </label>
          <label>
            {t("aiAnomalyCenter.decision")}
            <input value={decision} onChange={(event) => onDecision(event.target.value)} />
          </label>
          <div className="ai-anomaly-review-actions">
            {(["mark_under_review", "explain", "resolve", "ignore", "reopen"] as AnomalyReviewAction[]).map((action) => (
              <button
                className={action === "resolve" ? "button button--primary" : "button"}
                disabled={isPending}
                key={action}
                type="button"
                onClick={() => onAction(action)}
              >
                {t(`aiAnomalyCenter.actions.${action}`)}
              </button>
            ))}
          </div>
        </article>
      </div>

      <section className="ai-anomaly-review-history">
        <h3>{t("aiAnomalyCenter.reviewHistory")}</h3>
        {anomaly.review_history.length ? (
          anomaly.review_history.map((event) => (
            <article key={`${event.timestamp}-${event.action}`}>
              <strong>{t(`aiAnomalyCenter.actions.${event.action}`)}</strong>
              <span>
                {t(`aiAnomalyCenter.statuses.${event.from_status}`)} {"->"} {t(`aiAnomalyCenter.statuses.${event.to_status}`)}
              </span>
              <p>{event.note || event.decision || t("common.unavailable")}</p>
              <time dateTime={event.timestamp}>{formatDate(event.timestamp)}</time>
            </article>
          ))
        ) : (
          <EmptyState
            title={t("aiAnomalyCenter.noReviewHistory")}
            message={t("aiAnomalyCenter.noReviewHistoryMessage")}
          />
        )}
      </section>
    </section>
  );
}

function ReportsExportsPanel({
  csv,
  generatedReportId,
  isExporting,
  isGenerating,
  t,
  onExport,
  onGenerate,
}: {
  csv: string;
  generatedReportId: string;
  isExporting: boolean;
  isGenerating: boolean;
  t: (key: string) => string;
  onExport: () => void;
  onGenerate: () => void;
}) {
  return (
    <section className="analytics-section">
      <header className="analytics-section__header">
        <h2>{t("aiAnomalyCenter.reportsExports")}</h2>
        <p>{t("aiAnomalyCenter.reportsExportsDescription")}</p>
      </header>
      <div className="ai-anomaly-export-actions">
        <button className="button button--primary" disabled={isGenerating} type="button" onClick={onGenerate}>
          {isGenerating ? t("common.loading") : t("aiAnomalyCenter.generateReport")}
        </button>
        <button className="button" disabled={isExporting} type="button" onClick={onExport}>
          {isExporting ? t("common.loading") : t("reportsCenter.exportCsv")}
        </button>
        <Link className="button" to="/reports-center">
          {t("aiAnomalyCenter.openReportsCenter")}
        </Link>
      </div>
      {generatedReportId ? (
        <p className="ai-anomaly-export-note">
          {t("aiAnomalyCenter.generatedReport")}: <strong>{generatedReportId}</strong>
        </p>
      ) : null}
      {csv ? (
        <pre className="ai-anomaly-export-preview">{csv}</pre>
      ) : (
        <EmptyState
          title={t("aiAnomalyCenter.noExportTitle")}
          message={t("aiAnomalyCenter.noExportMessage")}
        />
      )}
    </section>
  );
}

function MethodologyPanel({
  limitations,
  methodology,
  sourceModules,
  t,
}: {
  limitations: string[];
  methodology: AnomalyScanResponse["methodology"] | null;
  sourceModules: string[];
  t: (key: string) => string;
}) {
  return (
    <section className="analytics-section">
      <header className="analytics-section__header">
        <h2>{t("aiAnomalyCenter.methodology")}</h2>
        <p>{t("aiAnomalyCenter.methodologyDescription")}</p>
      </header>
      <div className="ai-anomaly-methodology-grid">
        <article>
          <h3>{t("aiAnomalyCenter.ruleBasedDetection")}</h3>
          <p>{methodology?.detection_mode ?? t("aiAnomalyCenter.deterministicMode")}</p>
          <div className="ai-anomaly-pill-list">
            {Object.entries(methodology?.score_mapping ?? {
              "0-25": "low",
              "26-50": "medium",
              "51-75": "high",
              "76-100": "critical",
            }).map(([range, severity]) => (
              <span key={range}>{range}: {severity}</span>
            ))}
          </div>
        </article>
        <article>
          <h3>{t("aiAnomalyCenter.scoringFactors")}</h3>
          <ul>
            {(methodology?.factors ?? [
              "magnitude of deviation",
              "portfolio impact",
              "recurrence",
              "source module confidence",
              "data quality",
              "unresolved status",
              "critical rule flag",
            ]).map((factor) => (
              <li key={factor}>{factor}</li>
            ))}
          </ul>
        </article>
        <article>
          <h3>{t("reportsCenter.sourceModules")}</h3>
          <div className="ai-anomaly-pill-list">
            {sourceModules.map((source) => <span key={source}>{source}</span>)}
          </div>
        </article>
        <article>
          <h3>{t("common.limitations")}</h3>
          <ul>
            {limitations.map((limitation) => <li key={limitation}>{limitation}</li>)}
            <li>{t("aiAnomalyCenter.notProductionFraudDetection")}</li>
            <li>{t("aiAnomalyCenter.notInvestmentAdvice")}</li>
          </ul>
        </article>
      </div>
    </section>
  );
}

function AnomalyCardList({
  records,
  t,
  onSelect,
}: {
  records: AnomalyRecord[];
  t: (key: string) => string;
  onSelect: (record: AnomalyRecord) => void;
}) {
  if (!records.length) {
    return (
      <EmptyState
        title={t("aiAnomalyCenter.emptyTitle")}
        message={t("aiAnomalyCenter.emptyMessage")}
      />
    );
  }

  return (
    <div className="ai-anomaly-card-list">
      {records.map((record) => (
        <button className="ai-anomaly-card" key={record.anomaly_id} type="button" onClick={() => onSelect(record)}>
          <div className="ai-anomaly-card__header">
            <StatusBadge label={t(`aiAnomalyCenter.severities.${record.severity}`)} variant={severityVariant(record.severity)} />
            <span className="ai-anomaly-score">{Math.round(record.anomaly_score)}</span>
          </div>
          <span className="ai-anomaly-card__source">{record.source_module}</span>
          <h3>{record.title}</h3>
          <p>{record.description}</p>
          <div className="ai-anomaly-card__footer">
            <span>{categoryLabel(record.category, t)}</span>
            <strong>{t(`aiAnomalyCenter.statuses.${record.status}`)}</strong>
          </div>
        </button>
      ))}
    </div>
  );
}

function AnomalyTable({
  records,
  selectedId,
  t,
  onDelete,
  onSelect,
}: {
  records: AnomalyRecord[];
  selectedId?: string;
  t: (key: string) => string;
  onDelete: (record: AnomalyRecord) => void;
  onSelect: (record: AnomalyRecord) => void;
}) {
  if (!records.length) {
    return (
      <EmptyState
        title={t("aiAnomalyCenter.emptyTitle")}
        message={t("aiAnomalyCenter.emptyMessage")}
      />
    );
  }

  return (
    <div className="table-scroll">
      <table className="data-table ai-anomaly-register-table">
        <thead>
          <tr>
            <th>{t("aiAnomalyCenter.anomalyId")}</th>
            <th>{t("aiAnomalyCenter.category")}</th>
            <th>{t("aiAnomalyCenter.sourceModule")}</th>
            <th>{t("aiAnomalyCenter.titleColumn")}</th>
            <th>{t("aiAnomalyCenter.severity")}</th>
            <th>{t("aiAnomalyCenter.anomalyScore")}</th>
            <th>{t("aiAnomalyCenter.status")}</th>
            <th>{t("aiAnomalyCenter.detectedAt")}</th>
            <th>{t("reportsCenter.actions")}</th>
          </tr>
        </thead>
        <tbody>
          {records.map((record) => (
            <tr className={selectedId === record.anomaly_id ? "ai-anomaly-selected-row" : undefined} key={record.anomaly_id}>
              <td className="data-table__symbol">{record.anomaly_id}</td>
              <td>{categoryLabel(record.category, t)}</td>
              <td>{record.source_module}</td>
              <td>{record.title}</td>
              <td><StatusBadge label={t(`aiAnomalyCenter.severities.${record.severity}`)} variant={severityVariant(record.severity)} /></td>
              <td className="data-table__numeric">{record.anomaly_score.toFixed(0)}</td>
              <td><StatusBadge label={t(`aiAnomalyCenter.statuses.${record.status}`)} variant={statusVariant(record.status)} /></td>
              <td>{formatDate(record.detected_at)}</td>
              <td className="data-table__actions">
                <button className="button button--compact" type="button" onClick={() => onSelect(record)}>
                  {t("reportsCenter.view")}
                </button>
                <button className="button button--compact button--danger" type="button" onClick={() => onDelete(record)}>
                  {t("reportsCenter.delete")}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function CountCard({
  counts,
  title,
  t,
  type,
}: {
  counts: Record<string, number>;
  title: string;
  t: (key: string) => string;
  type: "category" | "severity";
}) {
  const entries = Object.entries(counts);
  return (
    <article className="ai-anomaly-count-card">
      <h3>{title}</h3>
      {entries.length ? (
        entries.map(([key, count]) => (
          <div key={key}>
            <span>{type === "category" ? categoryLabel(key as AnomalyCategory, t) : t(`aiAnomalyCenter.severities.${key}`)}</span>
            <strong>{count}</strong>
          </div>
        ))
      ) : (
        <p>{t("aiAnomalyCenter.noAnomalies")}</p>
      )}
    </article>
  );
}

function recordsFor(records: AnomalyRecord[], categories: AnomalyCategory[]) {
  return records.filter((record) => categories.includes(record.category));
}

function countBy(records: AnomalyRecord[], field: "severity" | "category") {
  return records.reduce<Record<string, number>>((acc, record) => {
    const value = record[field];
    acc[value] = (acc[value] ?? 0) + 1;
    return acc;
  }, {});
}

function categoryLabel(category: AnomalyCategory | AnomalyScanScope, t: (key: string) => string) {
  if (category === "all") return t("common.all");
  return t(`aiAnomalyCenter.categories.${category}`);
}

function severityVariant(severity: AnomalySeverity): StatusBadgeVariant {
  if (severity === "critical") return "danger";
  if (severity === "high") return "warning";
  if (severity === "medium") return "info";
  return "success";
}

function statusVariant(status: AnomalyStatus): StatusBadgeVariant {
  if (status === "open") return "warning";
  if (status === "resolved" || status === "ignored") return "success";
  if (status === "under_review") return "info";
  return "neutral";
}

function formatDate(value: string) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString();
}

function formatValue(value: unknown) {
  if (value === null || value === undefined || value === "") return "n/a";
  if (typeof value === "number") return Number.isFinite(value) ? value.toLocaleString(undefined, { maximumFractionDigits: 4 }) : "n/a";
  if (typeof value === "object") return JSON.stringify(value);
  return String(value);
}
