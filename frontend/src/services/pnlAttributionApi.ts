import { apiClient } from "../lib/api-client";
import { endpoints } from "../lib/endpoints";
import type {
  PnlAttributionRequest,
  PnlAttributionResult,
  PnlAttributionStatus,
  PnlCsvExportResponse,
  PnlHistoryResponse,
} from "../types/pnl-attribution";

export const pnlAttributionApi = {
  status() {
    return apiClient.get<PnlAttributionStatus>(endpoints.pnlAttributionStatus);
  },
  analyze(payload: PnlAttributionRequest) {
    return apiClient.post<PnlAttributionResult>(endpoints.pnlAttributionAnalyze, payload);
  },
  demo() {
    return apiClient.get<PnlAttributionResult>(endpoints.pnlAttributionDemo);
  },
  history() {
    return apiClient.get<PnlHistoryResponse>(endpoints.pnlAttributionHistory);
  },
  historyItem(analysisId: string) {
    return apiClient.get<PnlAttributionResult>(endpoints.pnlAttributionHistoryItem(analysisId));
  },
  deleteHistoryItem(analysisId: string) {
    return apiClient.delete<{ deleted: boolean; analysis_id: string }>(
      endpoints.pnlAttributionHistoryItem(analysisId),
    );
  },
  exportCsv(analysisId: string) {
    return apiClient.get<PnlCsvExportResponse>(endpoints.pnlAttributionExportCsv(analysisId));
  },
};
