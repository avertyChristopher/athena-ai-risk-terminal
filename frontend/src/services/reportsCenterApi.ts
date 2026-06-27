import { apiClient } from "../lib/api-client";
import { endpoints } from "../lib/endpoints";
import type {
  CsvExportResponse,
  GeneratedReport,
  MarkdownExportResponse,
  ReportGenerateRequest,
  ReportLibraryResponse,
  ReportTemplateListResponse,
  ReportsCenterStatus,
} from "../types/reports-center";

export const reportsCenterApi = {
  status() {
    return apiClient.get<ReportsCenterStatus>(endpoints.reportsCenterStatus);
  },
  templates() {
    return apiClient.get<ReportTemplateListResponse>(endpoints.reportsCenterTemplates);
  },
  generate(payload: ReportGenerateRequest) {
    return apiClient.post<GeneratedReport>(endpoints.reportsCenterGenerate, payload);
  },
  reports() {
    return apiClient.get<ReportLibraryResponse>(endpoints.reportsCenterReports);
  },
  report(reportId: string) {
    return apiClient.get<GeneratedReport>(endpoints.reportsCenterReport(reportId));
  },
  deleteReport(reportId: string) {
    return apiClient.delete<{ deleted: boolean; report_id: string }>(
      endpoints.reportsCenterReport(reportId),
    );
  },
  exportJson(reportId: string) {
    return apiClient.get<GeneratedReport>(endpoints.reportsCenterExportJson(reportId));
  },
  exportMarkdown(reportId: string) {
    return apiClient.get<MarkdownExportResponse>(
      endpoints.reportsCenterExportMarkdown(reportId),
    );
  },
  exportCsv(reportId: string) {
    return apiClient.get<CsvExportResponse>(endpoints.reportsCenterExportCsv(reportId));
  },
  demo() {
    return apiClient.get<GeneratedReport>(endpoints.reportsCenterDemo);
  },
};
