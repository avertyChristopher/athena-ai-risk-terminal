export type ReportType =
  | "portfolio_overview"
  | "risk_monitor"
  | "stress_testing"
  | "limit_breach"
  | "trade_suitability"
  | "fixed_income_exposure"
  | "options_risk"
  | "pnl_attribution"
  | "reconciliation"
  | "ai_anomaly"
  | "full_portfolio_risk_pack";

export type ReportLanguage = "en" | "fr";
export type ReportStyle = "professional" | "executive" | "educational";

export type ReportsCenterStatus = {
  status: string;
  module: string;
  detail: string;
  templates_available: number;
  export_formats: string[];
  source_modules: string[];
  snapshot_based: boolean;
  pdf_roadmap_note: string;
};

export type ReportTemplate = {
  report_type: ReportType;
  name: string;
  purpose: string;
  sections: string[];
  source_modules: string[];
  export_formats: string[];
  pdf_roadmap_note: string;
};

export type ReportTemplateListResponse = {
  status: string;
  module: string;
  templates: ReportTemplate[];
};

export type ReportGenerateRequest = {
  report_type: ReportType;
  portfolio_id?: string | null;
  language: ReportLanguage;
  include_athena_commentary: boolean;
  include_methodology: boolean;
  include_limitations: boolean;
  source_payloads?: Record<string, unknown>;
  style: ReportStyle;
};

export type ReportSection = {
  section_id: string;
  title: string;
  status: string;
  summary: string;
  source_modules: string[];
  metrics: Record<string, unknown>;
  table: Record<string, unknown>[];
  warnings: string[];
};

export type ReportSnapshot = {
  snapshot_id: string;
  report_id: string;
  portfolio_id: string | null;
  portfolio_name: string | null;
  report_type: ReportType;
  generated_at: string;
  source_modules: string[];
  data_sources: string[];
  payloads_used: Record<string, unknown>;
  warnings: string[];
  limitations: string[];
  generated_by: string;
  language: ReportLanguage;
};

export type GeneratedReport = {
  report_id: string;
  report_type: ReportType;
  title: string;
  portfolio_id: string | null;
  portfolio_name: string | null;
  generated_at: string;
  language: ReportLanguage;
  style: ReportStyle;
  status: "generated" | "generated_with_warnings";
  executive_summary: string;
  sections: ReportSection[];
  snapshot: ReportSnapshot;
  athena_commentary: Record<string, unknown> | null;
  assumptions: string[];
  limitations: string[];
  warnings: string[];
  export_formats: string[];
  pdf_roadmap_note: string;
  disclaimer: string;
};

export type ReportListItem = {
  report_id: string;
  report_type: ReportType;
  title: string;
  portfolio_id: string | null;
  portfolio_name: string | null;
  generated_at: string;
  language: ReportLanguage;
  status: "generated" | "generated_with_warnings";
  warnings_count: number;
  source_modules: string[];
};

export type ReportLibraryResponse = {
  status: string;
  module: string;
  total_reports: number;
  items: ReportListItem[];
};

export type MarkdownExportResponse = {
  report_id: string;
  content_type: string;
  markdown: string;
};

export type CsvExportResponse = {
  report_id: string;
  content_type: string;
  csv: string;
  included_tables: string[];
};
