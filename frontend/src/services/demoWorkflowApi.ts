import { apiClient } from "../lib/api-client";
import { endpoints } from "../lib/endpoints";
import type {
  DemoRunHistoryResponse,
  DemoRunRequest,
  DemoRunSummary,
  DemoWorkflowStatus,
} from "../types/demo-workflow";

export const demoWorkflowApi = {
  status() {
    return apiClient.get<DemoWorkflowStatus>(endpoints.demoWorkflowStatus);
  },
  run(payload: DemoRunRequest) {
    return apiClient.post<DemoRunSummary>(endpoints.demoWorkflowRun, payload);
  },
  history() {
    return apiClient.get<DemoRunHistoryResponse>(endpoints.demoWorkflowHistory);
  },
};
