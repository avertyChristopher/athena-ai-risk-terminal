import { apiClient } from "../lib/api-client";
import { endpoints } from "../lib/endpoints";
import type {
  AIAnomalyCenterStatus,
  AnomalyCsvExportResponse,
  AnomalyHistoryResponse,
  AnomalyListResponse,
  AnomalyRecord,
  AnomalyReviewRequest,
  AnomalyReviewResponse,
  AnomalyScanRequest,
  AnomalyScanResponse,
} from "../types/ai-anomaly-center";

type AnomalyListFilters = {
  portfolio_id?: string;
  severity?: string;
  module_name?: string;
  status?: string;
};

export const aiAnomalyCenterApi = {
  status() {
    return apiClient.get<AIAnomalyCenterStatus>(endpoints.aiAnomalyCenterStatus);
  },
  scan(payload: AnomalyScanRequest) {
    return apiClient.post<AnomalyScanResponse>(endpoints.aiAnomalyCenterScan, payload);
  },
  anomalies(filters: AnomalyListFilters = {}) {
    return apiClient.get<AnomalyListResponse>(
      `${endpoints.aiAnomalyCenterAnomalies}${queryString(filters)}`,
    );
  },
  anomaly(anomalyId: string) {
    return apiClient.get<AnomalyRecord>(endpoints.aiAnomalyCenterAnomaly(anomalyId));
  },
  review(anomalyId: string, payload: AnomalyReviewRequest) {
    return apiClient.post<AnomalyReviewResponse>(
      endpoints.aiAnomalyCenterReview(anomalyId),
      payload,
    );
  },
  deleteAnomaly(anomalyId: string) {
    return apiClient.delete<{ deleted: boolean; anomaly_id: string }>(
      endpoints.aiAnomalyCenterAnomaly(anomalyId),
    );
  },
  history() {
    return apiClient.get<AnomalyHistoryResponse>(endpoints.aiAnomalyCenterHistory);
  },
  demo() {
    return apiClient.get<AnomalyScanResponse>(endpoints.aiAnomalyCenterDemo);
  },
  exportCsv() {
    return apiClient.get<AnomalyCsvExportResponse>(endpoints.aiAnomalyCenterExportCsv);
  },
};

function queryString(filters: AnomalyListFilters) {
  const params = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => {
    if (value) params.set(key, value);
  });
  const query = params.toString();
  return query ? `?${query}` : "";
}
