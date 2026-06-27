import { useMemo, useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";

import { ErrorBanner } from "../../../components/ui/ErrorBanner";
import { LoadingState } from "../../../components/ui/LoadingState";
import { StatusBadge } from "../../../components/ui/StatusBadge";
import { apiClient } from "../../../lib/api-client";
import { endpoints } from "../../../lib/endpoints";
import { reportsCenterApi } from "../../../services/reportsCenterApi";
import type { PortfolioListResponse } from "../../../types/portfolio";
import type {
  GeneratedReport,
  ReportLanguage,
  ReportListItem,
  ReportStyle,
  ReportTemplate,
  ReportType,
} from "../../../types/reports-center";
import { useTranslation } from "../../../hooks/useTranslation";

type Tab =
  | "overview"
  | "generate"
  | "library"
  | "preview"
  | "exports"
  | "sources"
  | "methodology";

const reportTypes: ReportType[] = [
  "portfolio_overview",
  "risk_monitor",
  "stress_testing",
  "limit_breach",
  "trade_suitability",
  "fixed_income_exposure",
  "options_risk",
  "pnl_attribution",
  "full_portfolio_risk_pack",
];

const tabs: Tab[] = [
  "overview",
  "generate",
  "library",
  "preview",
  "exports",
  "sources",
  "methodology",
];

export function ReportsCenterPage() {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState<Tab>("overview");
  const [reportType, setReportType] = useState<ReportType>("full_portfolio_risk_pack");
  const [portfolioId, setPortfolioId] = useState("pf_004");
  const [language, setLanguage] = useState<ReportLanguage>("en");
  const [style, setStyle] = useState<ReportStyle>("executive");
  const [includeAthena, setIncludeAthena] = useState(true);
  const [includeMethodology, setIncludeMethodology] = useState(true);
  const [includeLimitations, setIncludeLimitations] = useState(true);
  const [selectedReport, setSelectedReport] = useState<GeneratedReport | null>(null);
  const [exportContent, setExportContent] = useState("");
  const [exportTitle, setExportTitle] = useState("");

  const statusQuery = useQuery({
    queryKey: ["reports-center-status"],
    queryFn: reportsCenterApi.status,
  });
  const templatesQuery = useQuery({
    queryKey: ["reports-center-templates"],
    queryFn: reportsCenterApi.templates,
  });
  const reportsQuery = useQuery({
    queryKey: ["reports-center-library"],
    queryFn: reportsCenterApi.reports,
  });
  const portfolioQuery = useQuery({
    queryKey: ["reports-center-portfolios"],
    queryFn: () => apiClient.get<PortfolioListResponse>(endpoints.portfolios),
  });

  const generateMutation = useMutation({
    mutationFn: () =>
      reportsCenterApi.generate({
        report_type: reportType,
        portfolio_id: portfolioId || null,
        language,
        style,
        include_athena_commentary: includeAthena,
        include_methodology: includeMethodology,
        include_limitations: includeLimitations,
      }),
    onSuccess: (report) => {
      setSelectedReport(report);
      setActiveTab("preview");
      void reportsQuery.refetch();
    },
  });

  const reports = reportsQuery.data?.items ?? [];
  const templates = templatesQuery.data?.templates ?? [];
  const lastReport = reports[0] ?? null;
  const reportsWithWarnings = reports.filter((report) => report.warnings_count > 0).length;
  const sourceModules = statusQuery.data?.source_modules ?? [];
  const selectedTemplate = templates.find((template) => template.report_type === reportType);

  const kpis = useMemo(
    () => [
      [t("reportsCenter.kpis.reportsGenerated"), String(reportsQuery.data?.total_reports ?? 0)],
      [t("reportsCenter.kpis.availableTemplates"), String(statusQuery.data?.templates_available ?? templates.length)],
      [t("reportsCenter.kpis.lastReport"), lastReport ? reportTypeLabel(lastReport.report_type, t) : t("common.unavailable")],
      [t("reportsCenter.kpis.sourceModulesConnected"), String(sourceModules.length)],
      [t("reportsCenter.kpis.reportsWithWarnings"), String(reportsWithWarnings)],
      [t("reportsCenter.kpis.exportFormats"), (statusQuery.data?.export_formats ?? ["json", "markdown", "csv"]).join(" / ")],
    ],
    [lastReport, reportsQuery.data?.total_reports, reportsWithWarnings, sourceModules.length, statusQuery.data, t, templates.length],
  );

  async function selectReport(reportId: string) {
    const report = await reportsCenterApi.report(reportId);
    setSelectedReport(report);
    setActiveTab("preview");
  }

  async function deleteReport(reportId: string) {
    await reportsCenterApi.deleteReport(reportId);
    if (selectedReport?.report_id === reportId) setSelectedReport(null);
    await reportsQuery.refetch();
  }

  async function exportReport(format: "json" | "markdown" | "csv", reportId = selectedReport?.report_id) {
    if (!reportId) return;
    if (format === "json") {
      const payload = await reportsCenterApi.exportJson(reportId);
      setExportTitle(t("reportsCenter.exportJson"));
      setExportContent(JSON.stringify(payload, null, 2));
    } else if (format === "markdown") {
      const payload = await reportsCenterApi.exportMarkdown(reportId);
      setExportTitle(t("reportsCenter.exportMarkdown"));
      setExportContent(payload.markdown);
    } else {
      const payload = await reportsCenterApi.exportCsv(reportId);
      setExportTitle(t("reportsCenter.exportCsv"));
      setExportContent(payload.csv);
    }
    if (!selectedReport || selectedReport.report_id !== reportId) {
      const report = await reportsCenterApi.report(reportId);
      setSelectedReport(report);
    }
    setActiveTab("exports");
  }

  if (statusQuery.isError || templatesQuery.isError || reportsQuery.isError) {
    return (
      <div className="page reports-center-page">
        <ErrorBanner
          title={t("reportsCenter.title")}
          message={t("reportsCenter.apiError")}
        />
      </div>
    );
  }

  return (
    <div className="page reports-center-page">
      <section className="reports-center-hero">
        <div>
          <span className="equity-kicker">{t("reportsCenter.eyebrow")}</span>
          <h1>{t("reportsCenter.title")}</h1>
          <p>{t("reportsCenter.subtitle")}</p>
        </div>
        <div className="reports-center-command-panel">
          <label>
            {t("reportsCenter.reportType")}
            <select value={reportType} onChange={(event) => setReportType(event.target.value as ReportType)}>
              {reportTypes.map((type) => (
                <option key={type} value={type}>
                  {reportTypeLabel(type, t)}
                </option>
              ))}
            </select>
          </label>
          <label>
            {t("workflow.portfolio")}
            <select value={portfolioId} onChange={(event) => setPortfolioId(event.target.value)}>
              {(portfolioQuery.data?.items ?? []).map((portfolio) => (
                <option key={portfolio.id} value={portfolio.id}>
                  {portfolio.name}
                </option>
              ))}
            </select>
          </label>
          <label>
            {t("common.language")}
            <select value={language} onChange={(event) => setLanguage(event.target.value as ReportLanguage)}>
              <option value="en">{t("common.english")}</option>
              <option value="fr">{t("common.french")}</option>
            </select>
          </label>
          <label>
            {t("reportsCenter.style")}
            <select value={style} onChange={(event) => setStyle(event.target.value as ReportStyle)}>
              <option value="professional">{t("reportsCenter.styles.professional")}</option>
              <option value="executive">{t("reportsCenter.styles.executive")}</option>
              <option value="educational">{t("reportsCenter.styles.educational")}</option>
            </select>
          </label>
          <button
            className="button button-primary"
            disabled={generateMutation.isPending}
            type="button"
            onClick={() => generateMutation.mutate()}
          >
            {generateMutation.isPending ? t("common.loading") : t("reportsCenter.generateReport")}
          </button>
          <button className="button button-secondary" type="button" onClick={() => void reportsQuery.refetch()}>
            {t("reportsCenter.refreshReports")}
          </button>
        </div>
      </section>

      <section className="reports-center-kpi-grid">
        {kpis.map(([label, value]) => (
          <div className="card reports-center-kpi" key={label}>
            <span>{label}</span>
            <strong>{value}</strong>
          </div>
        ))}
      </section>

      <nav className="risk-monitor-tabs reports-center-tabs" aria-label={t("reportsCenter.tabsLabel")}>
        {tabs.map((tab) => (
          <button
            key={tab}
            className={`risk-monitor-tab ${activeTab === tab ? "risk-monitor-tab--active" : ""}`}
            type="button"
            onClick={() => setActiveTab(tab)}
          >
            <span>{t(`reportsCenter.tabs.${tab}`)}</span>
          </button>
        ))}
      </nav>

      {templatesQuery.isLoading || statusQuery.isLoading ? (
        <LoadingState label={t("common.loading")} />
      ) : null}

      {activeTab === "overview" ? (
        <OverviewTab
          sourceModules={sourceModules}
          templates={templates}
          lastReport={lastReport}
          t={t}
        />
      ) : null}

      {activeTab === "generate" ? (
        <GenerateTab
          includeAthena={includeAthena}
          includeLimitations={includeLimitations}
          includeMethodology={includeMethodology}
          selectedTemplate={selectedTemplate}
          setIncludeAthena={setIncludeAthena}
          setIncludeLimitations={setIncludeLimitations}
          setIncludeMethodology={setIncludeMethodology}
          onGenerate={() => generateMutation.mutate()}
          isGenerating={generateMutation.isPending}
          t={t}
        />
      ) : null}

      {activeTab === "library" ? (
        <LibraryTab
          reports={reports}
          onDelete={deleteReport}
          onExport={(reportId, format) => exportReport(format, reportId)}
          onSelect={selectReport}
          t={t}
        />
      ) : null}

      {activeTab === "preview" ? (
        <PreviewTab report={selectedReport} onExport={exportReport} t={t} />
      ) : null}

      {activeTab === "exports" ? (
        <ExportsTab
          exportContent={exportContent}
          exportTitle={exportTitle}
          pdfNote={statusQuery.data?.pdf_roadmap_note ?? ""}
          report={selectedReport}
          onExport={exportReport}
          t={t}
        />
      ) : null}

      {activeTab === "sources" ? (
        <SourcesTab sourceModules={sourceModules} report={selectedReport} t={t} />
      ) : null}

      {activeTab === "methodology" ? (
        <MethodologyTab pdfNote={statusQuery.data?.pdf_roadmap_note ?? ""} t={t} />
      ) : null}
    </div>
  );
}

function OverviewTab({
  sourceModules,
  templates,
  lastReport,
  t,
}: {
  sourceModules: string[];
  templates: ReportTemplate[];
  lastReport: ReportListItem | null;
  t: (key: string) => string;
}) {
  return (
    <section className="reports-center-layout">
      <div className="analytics-section reports-center-panel">
        <header className="analytics-section__header">
          <h2>{t("reportsCenter.availableTemplates")}</h2>
          <p>{t("reportsCenter.overviewDescription")}</p>
        </header>
        <div className="reports-center-template-grid">
          {templates.map((template) => (
            <TemplateCard key={template.report_type} template={template} />
          ))}
        </div>
      </div>
      <aside className="card reports-center-side-panel">
        <span className="equity-kicker">{t("reportsCenter.lastReport")}</span>
        <h3>{lastReport ? reportTypeLabel(lastReport.report_type, t) : t("common.unavailable")}</h3>
        <p>{lastReport?.portfolio_name ?? t("reportsCenter.noReportGenerated")}</p>
        <div className="reports-center-chip-list">
          {sourceModules.map((module) => (
            <span key={module}>{module}</span>
          ))}
        </div>
      </aside>
    </section>
  );
}

function GenerateTab({
  includeAthena,
  includeLimitations,
  includeMethodology,
  selectedTemplate,
  setIncludeAthena,
  setIncludeLimitations,
  setIncludeMethodology,
  onGenerate,
  isGenerating,
  t,
}: {
  includeAthena: boolean;
  includeLimitations: boolean;
  includeMethodology: boolean;
  selectedTemplate: ReportTemplate | undefined;
  setIncludeAthena: (value: boolean) => void;
  setIncludeLimitations: (value: boolean) => void;
  setIncludeMethodology: (value: boolean) => void;
  onGenerate: () => void;
  isGenerating: boolean;
  t: (key: string) => string;
}) {
  return (
    <section className="analytics-section reports-center-panel">
      <header className="analytics-section__header">
        <h2>{t("reportsCenter.generateReport")}</h2>
        <p>{selectedTemplate?.purpose ?? t("reportsCenter.generateDescription")}</p>
      </header>
      <div className="reports-center-option-grid">
        <label className="reports-center-toggle">
          <input checked={includeAthena} type="checkbox" onChange={(event) => setIncludeAthena(event.target.checked)} />
          {t("reportsCenter.includeAthena")}
        </label>
        <label className="reports-center-toggle">
          <input checked={includeMethodology} type="checkbox" onChange={(event) => setIncludeMethodology(event.target.checked)} />
          {t("reportsCenter.includeMethodology")}
        </label>
        <label className="reports-center-toggle">
          <input checked={includeLimitations} type="checkbox" onChange={(event) => setIncludeLimitations(event.target.checked)} />
          {t("reportsCenter.includeLimitations")}
        </label>
      </div>
      <div className="reports-center-template-sections">
        {(selectedTemplate?.sections ?? []).map((section) => (
          <span key={section}>{section}</span>
        ))}
      </div>
      <button className="button button-primary" disabled={isGenerating} type="button" onClick={onGenerate}>
        {isGenerating ? t("common.loading") : t("reportsCenter.generateReport")}
      </button>
    </section>
  );
}

function LibraryTab({
  reports,
  onDelete,
  onExport,
  onSelect,
  t,
}: {
  reports: ReportListItem[];
  onDelete: (reportId: string) => void;
  onExport: (reportId: string, format: "json" | "markdown" | "csv") => void;
  onSelect: (reportId: string) => void;
  t: (key: string) => string;
}) {
  return (
    <section className="analytics-section reports-center-panel">
      <header className="analytics-section__header">
        <h2>{t("reportsCenter.reportLibrary")}</h2>
        <p>{t("reportsCenter.libraryDescription")}</p>
      </header>
      <div className="reports-center-table">
        <div className="reports-center-table__head">
          <span>{t("reportsCenter.reportType")}</span>
          <span>{t("workflow.portfolio")}</span>
          <span>{t("reportsCenter.generatedAt")}</span>
          <span>{t("reportsCenter.status")}</span>
          <span>{t("reportsCenter.actions")}</span>
        </div>
        {reports.map((report) => (
          <div className="reports-center-table__row" key={report.report_id}>
            <strong>{reportTypeLabel(report.report_type, t)}</strong>
            <span>{report.portfolio_name ?? t("common.unavailable")}</span>
            <span>{formatDate(report.generated_at)}</span>
            <StatusBadge
              label={`${report.status} / ${report.warnings_count} ${t("reportsCenter.warnings")}`}
              variant={report.warnings_count ? "warning" : "success"}
            />
            <div className="reports-center-actions">
              <button type="button" onClick={() => void onSelect(report.report_id)}>{t("reportsCenter.view")}</button>
              <button type="button" onClick={() => void onExport(report.report_id, "json")}>{t("reportsCenter.exportJson")}</button>
              <button type="button" onClick={() => void onExport(report.report_id, "markdown")}>{t("reportsCenter.exportMarkdown")}</button>
              <button type="button" onClick={() => void onDelete(report.report_id)}>{t("reportsCenter.delete")}</button>
            </div>
          </div>
        ))}
        {!reports.length ? <p className="reports-center-empty">{t("reportsCenter.noReportGenerated")}</p> : null}
      </div>
    </section>
  );
}

function PreviewTab({
  report,
  onExport,
  t,
}: {
  report: GeneratedReport | null;
  onExport: (format: "json" | "markdown" | "csv") => void;
  t: (key: string) => string;
}) {
  if (!report) {
    return <EmptyPanel title={t("reportsCenter.reportPreview")} message={t("reportsCenter.noReportSelected")} />;
  }
  return (
    <section className="analytics-section reports-center-panel">
      <header className="analytics-section__header">
        <h2>{report.title}</h2>
        <p>{report.executive_summary}</p>
      </header>
      <div className="reports-center-preview-meta">
        <StatusBadge label={report.status} variant={report.status === "generated" ? "success" : "warning"} />
        <span>{report.portfolio_name}</span>
        <span>{formatDate(report.generated_at)}</span>
        <span>{report.snapshot.source_modules.join(" / ")}</span>
      </div>
      <div className="reports-center-export-row">
        <button type="button" onClick={() => void onExport("json")}>{t("reportsCenter.exportJson")}</button>
        <button type="button" onClick={() => void onExport("markdown")}>{t("reportsCenter.exportMarkdown")}</button>
        <button type="button" onClick={() => void onExport("csv")}>{t("reportsCenter.exportCsv")}</button>
      </div>
      <div className="reports-center-section-list">
        {report.sections.map((section) => (
          <section className="card reports-center-report-section" key={section.section_id}>
            <div className="section-heading">
              <h3>{section.title}</h3>
              <StatusBadge label={section.status} variant={section.status === "available" ? "success" : "warning"} />
            </div>
            <p>{section.summary}</p>
            {Object.keys(section.metrics).length ? <pre>{JSON.stringify(section.metrics, null, 2)}</pre> : null}
            {section.table.length ? <MiniTable rows={section.table} /> : null}
          </section>
        ))}
      </div>
      <div className="reports-center-limitations">
        <h3>{t("reportsCenter.limitations")}</h3>
        {report.limitations.map((item) => <p key={item}>{item}</p>)}
        <strong>{report.disclaimer}</strong>
      </div>
    </section>
  );
}

function ExportsTab({
  exportContent,
  exportTitle,
  pdfNote,
  report,
  onExport,
  t,
}: {
  exportContent: string;
  exportTitle: string;
  pdfNote: string;
  report: GeneratedReport | null;
  onExport: (format: "json" | "markdown" | "csv") => void;
  t: (key: string) => string;
}) {
  return (
    <section className="analytics-section reports-center-panel">
      <header className="analytics-section__header">
        <h2>{t("reportsCenter.exports")}</h2>
        <p>{pdfNote}</p>
      </header>
      <div className="reports-center-export-row">
        <button disabled={!report} type="button" onClick={() => void onExport("json")}>{t("reportsCenter.exportJson")}</button>
        <button disabled={!report} type="button" onClick={() => void onExport("markdown")}>{t("reportsCenter.exportMarkdown")}</button>
        <button disabled={!report} type="button" onClick={() => void onExport("csv")}>{t("reportsCenter.exportCsv")}</button>
      </div>
      <pre className="reports-center-export-preview">
        {exportContent ? `${exportTitle}\n\n${exportContent}` : t("reportsCenter.noExportSelected")}
      </pre>
    </section>
  );
}

function SourcesTab({
  sourceModules,
  report,
  t,
}: {
  sourceModules: string[];
  report: GeneratedReport | null;
  t: (key: string) => string;
}) {
  const used = new Set(report?.snapshot.source_modules ?? []);
  return (
    <section className="analytics-section reports-center-panel">
      <header className="analytics-section__header">
        <h2>{t("reportsCenter.sourceModules")}</h2>
        <p>{t("reportsCenter.sourceModulesDescription")}</p>
      </header>
      <div className="reports-center-source-grid">
        {sourceModules.map((module) => (
          <div className="card reports-center-source-card" key={module}>
            <StatusBadge label={used.has(module) ? t("common.payloadAvailable") : t("common.connectedInputs")} variant={used.has(module) ? "success" : "info"} />
            <h3>{module}</h3>
            <p>{used.has(module) ? t("reportsCenter.lastUsedInReport") : t("reportsCenter.availableForSnapshots")}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

function MethodologyTab({ pdfNote, t }: { pdfNote: string; t: (key: string) => string }) {
  return (
    <section className="analytics-section reports-center-panel">
      <header className="analytics-section__header">
        <h2>{t("reportsCenter.methodology")}</h2>
        <p>{t("reportsCenter.methodologyDescription")}</p>
      </header>
      <div className="reports-center-methodology-grid">
        {[
          t("reportsCenter.snapshotMethodology"),
          t("reportsCenter.demoLimitations"),
          t("reportsCenter.aiLimitations"),
          t("reportsCenter.notInvestmentAdvice"),
          pdfNote,
        ].map((item) => (
          <div className="card" key={item}>
            <p>{item}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

function TemplateCard({ template }: { template: ReportTemplate }) {
  return (
    <article className="reports-center-template-card">
      <div>
        <StatusBadge label={template.report_type.replace(/_/g, " ")} variant="info" />
        <h3>{template.name}</h3>
        <p>{template.purpose}</p>
      </div>
      <div className="reports-center-chip-list">
        {template.source_modules.map((module) => <span key={module}>{module}</span>)}
      </div>
    </article>
  );
}

function MiniTable({ rows }: { rows: Record<string, unknown>[] }) {
  const keys = Array.from(new Set(rows.flatMap((row) => Object.keys(row)))).slice(0, 5);
  return (
    <div className="reports-center-mini-table">
      <div>
        {keys.map((key) => <strong key={key}>{key}</strong>)}
      </div>
      {rows.slice(0, 6).map((row, index) => (
        <div key={`${index}-${keys.join("-")}`}>
          {keys.map((key) => <span key={key}>{formatValue(row[key])}</span>)}
        </div>
      ))}
    </div>
  );
}

function EmptyPanel({ title, message }: { title: string; message: string }) {
  return (
    <section className="analytics-section reports-center-panel">
      <header className="analytics-section__header">
        <h2>{title}</h2>
        <p>{message}</p>
      </header>
    </section>
  );
}

function reportTypeLabel(type: ReportType, t: (key: string) => string) {
  const labels: Record<ReportType, string> = {
    portfolio_overview: t("reportsCenter.types.portfolioOverview"),
    risk_monitor: t("reportsCenter.types.riskMonitor"),
    stress_testing: t("reportsCenter.types.stressTesting"),
    limit_breach: t("reportsCenter.types.limitBreach"),
    trade_suitability: t("reportsCenter.types.tradeSuitability"),
    fixed_income_exposure: t("reportsCenter.types.fixedIncomeExposure"),
    options_risk: t("reportsCenter.types.optionsRisk"),
    pnl_attribution: t("reportsCenter.types.pnlAttribution"),
    full_portfolio_risk_pack: t("reportsCenter.types.fullPortfolioRiskPack"),
  };
  return labels[type];
}

function formatDate(value: string) {
  return new Date(value).toLocaleString();
}

function formatValue(value: unknown) {
  if (value === null || value === undefined) return "";
  if (typeof value === "number") return Number.isFinite(value) ? value.toFixed(4) : "";
  if (typeof value === "object") return JSON.stringify(value);
  return String(value);
}
