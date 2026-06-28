import { apiClient } from "../lib/api-client";
import { endpoints } from "../lib/endpoints";
import type {
  BreakRegisterResponse,
  ReconciliationBreak,
  ReconciliationCsvExportResponse,
  ReconciliationHistoryResponse,
  ReconciliationRequest,
  ReconciliationRunResult,
  ReconciliationStatus,
  ReviewRequest,
} from "../types/reconciliation";

export const reconciliationApi = {
  status() {
    return apiClient.get<ReconciliationStatus>(endpoints.reconciliationStatus);
  },
  run(payload: ReconciliationRequest) {
    return apiClient.post<ReconciliationRunResult>(
      endpoints.reconciliationRun,
      payload,
    );
  },
  demo() {
    return apiClient.get<ReconciliationRunResult>(endpoints.reconciliationDemo);
  },
  breaks() {
    return apiClient.get<BreakRegisterResponse>(endpoints.reconciliationBreaks);
  },
  breakItem(breakId: string) {
    return apiClient.get<ReconciliationBreak>(endpoints.reconciliationBreak(breakId));
  },
  reviewBreak(breakId: string, payload: ReviewRequest) {
    return apiClient.post<ReconciliationBreak>(
      endpoints.reconciliationReviewBreak(breakId),
      payload,
    );
  },
  history() {
    return apiClient.get<ReconciliationHistoryResponse>(
      endpoints.reconciliationHistory,
    );
  },
  historyItem(runId: string) {
    return apiClient.get<ReconciliationRunResult>(
      endpoints.reconciliationHistoryItem(runId),
    );
  },
  deleteHistoryItem(runId: string) {
    return apiClient.delete<{ deleted: boolean; run_id: string }>(
      endpoints.reconciliationHistoryItem(runId),
    );
  },
  exportCsv(runId: string) {
    return apiClient.get<ReconciliationCsvExportResponse>(
      endpoints.reconciliationExportCsv(runId),
    );
  },
};
