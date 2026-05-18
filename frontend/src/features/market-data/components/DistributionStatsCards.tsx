import { MarketDataAnalyticsResponse } from "../../../types/market-data";
import { PercentValue } from "../../../components/finance/PercentValue";
import { MetricTile } from "./MetricTile";

type DistributionStatsCardsProps = {
  analytics?: MarketDataAnalyticsResponse;
  labels: {
    skewness: string;
    kurtosis: string;
    outliers: string;
    normalComparison: string;
  };
};

export function DistributionStatsCards({
  analytics,
  labels,
}: DistributionStatsCardsProps) {
  return (
    <div className="metric-grid">
      <MetricTile
        label={labels.skewness}
        value={analytics ? analytics.skewness.toFixed(3) : "--"}
      />
      <MetricTile
        label={labels.kurtosis}
        value={analytics ? analytics.kurtosis.toFixed(3) : "--"}
      />
      <MetricTile
        label={labels.outliers}
        value={analytics ? analytics.outlier_indexes.length : "--"}
      />
      <MetricTile
        label={labels.normalComparison}
        value={
          analytics ? (
            <PercentValue value={analytics.normal_distribution_coverage} />
          ) : (
            "--"
          )
        }
      />
    </div>
  );
}
