import { PercentValue } from "../../../components/finance/PercentValue";
import { MarketDataAnalyticsResponse } from "../../../types/market-data";
import { MetricTile } from "./MetricTile";

type RelativePerformanceCardsProps = {
  analytics?: MarketDataAnalyticsResponse;
  labels: {
    activeReturn: string;
    correlation: string;
    beta: string;
    sharpe: string;
  };
};

export function RelativePerformanceCards({
  analytics,
  labels,
}: RelativePerformanceCardsProps) {
  return (
    <div className="metric-grid">
      <MetricTile
        label={labels.activeReturn}
        value={
          analytics ? (
            <PercentValue value={analytics.active_return_vs_benchmark} />
          ) : (
            "--"
          )
        }
      />
      <MetricTile
        label={labels.correlation}
        value={analytics ? analytics.correlation_with_benchmark.toFixed(3) : "--"}
      />
      <MetricTile
        label={labels.beta}
        value={analytics ? analytics.beta_vs_benchmark.toFixed(3) : "--"}
      />
      <MetricTile
        label={labels.sharpe}
        value={analytics ? analytics.sharpe_ratio.toFixed(3) : "--"}
      />
    </div>
  );
}
