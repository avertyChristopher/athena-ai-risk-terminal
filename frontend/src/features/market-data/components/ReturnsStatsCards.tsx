import { PercentValue } from "../../../components/finance/PercentValue";
import { MarketDataAnalyticsResponse } from "../../../types/market-data";
import { MetricTile } from "./MetricTile";

type ReturnsStatsCardsProps = {
  analytics?: MarketDataAnalyticsResponse;
  labels: {
    simple: string;
    log: string;
    holdingPeriod: string;
    cumulative: string;
    arithmetic: string;
    geometric: string;
    annualized: string;
  };
  latestLogReturn: number;
};

export function ReturnsStatsCards({
  analytics,
  labels,
  latestLogReturn,
}: ReturnsStatsCardsProps) {
  return (
    <div className="metric-grid metric-grid--seven">
      <MetricTile
        label={labels.simple}
        value={analytics ? <PercentValue value={analytics.latest_return} /> : "--"}
      />
      <MetricTile
        label={labels.log}
        value={analytics ? <PercentValue value={latestLogReturn} /> : "--"}
      />
      <MetricTile
        label={labels.holdingPeriod}
        value={
          analytics ? <PercentValue value={analytics.holding_period_return} /> : "--"
        }
      />
      <MetricTile
        label={labels.cumulative}
        value={analytics ? <PercentValue value={analytics.cumulative_return} /> : "--"}
      />
      <MetricTile
        label={labels.arithmetic}
        value={
          analytics ? <PercentValue value={analytics.arithmetic_mean_return} /> : "--"
        }
      />
      <MetricTile
        label={labels.geometric}
        value={
          analytics ? <PercentValue value={analytics.geometric_mean_return} /> : "--"
        }
      />
      <MetricTile
        label={labels.annualized}
        value={analytics ? <PercentValue value={analytics.annualized_return} /> : "--"}
      />
    </div>
  );
}
