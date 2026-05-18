import { PercentValue } from "../../../components/finance/PercentValue";
import { MarketDataAnalyticsResponse } from "../../../types/market-data";
import { MetricTile } from "./MetricTile";

type VolatilityStatsCardsProps = {
  analytics?: MarketDataAnalyticsResponse;
  labels: {
    variance: string;
    standardDeviation: string;
    dailyVolatility: string;
    annualizedVolatility: string;
    maxDrawdown: string;
  };
};

export function VolatilityStatsCards({
  analytics,
  labels,
}: VolatilityStatsCardsProps) {
  return (
    <div className="metric-grid">
      <MetricTile
        label={labels.variance}
        value={analytics ? analytics.variance.toFixed(6) : "--"}
      />
      <MetricTile
        label={labels.standardDeviation}
        value={
          analytics ? <PercentValue value={analytics.standard_deviation} /> : "--"
        }
      />
      <MetricTile
        label={labels.dailyVolatility}
        value={analytics ? <PercentValue value={analytics.daily_volatility} /> : "--"}
      />
      <MetricTile
        label={labels.annualizedVolatility}
        value={
          analytics ? <PercentValue value={analytics.annualized_volatility} /> : "--"
        }
      />
      <MetricTile
        label={labels.maxDrawdown}
        value={analytics ? <PercentValue value={analytics.max_drawdown} /> : "--"}
      />
    </div>
  );
}
