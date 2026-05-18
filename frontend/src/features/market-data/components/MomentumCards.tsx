import { MoneyValue } from "../../../components/finance/MoneyValue";
import { PercentValue } from "../../../components/finance/PercentValue";
import {
  MarketAsset,
  MarketDataAnalyticsResponse,
} from "../../../types/market-data";
import { MetricTile } from "./MetricTile";

type MomentumCardsProps = {
  asset?: MarketAsset;
  analytics?: MarketDataAnalyticsResponse;
  labels: {
    ma5: string;
    ma20: string;
    momentum5: string;
    riskFree: string;
  };
};

export function MomentumCards({ asset, analytics, labels }: MomentumCardsProps) {
  const currency = asset?.currency ?? "USD";

  return (
    <div className="metric-grid">
      <MetricTile
        label={labels.ma5}
        value={
          analytics?.moving_average_5 === null ? (
            "--"
          ) : (
            <MoneyValue value={analytics?.moving_average_5 ?? 0} currency={currency} />
          )
        }
      />
      <MetricTile
        label={labels.ma20}
        value={
          analytics?.moving_average_20 === null ? (
            "--"
          ) : (
            <MoneyValue value={analytics?.moving_average_20 ?? 0} currency={currency} />
          )
        }
      />
      <MetricTile
        label={labels.momentum5}
        value={
          analytics?.momentum_5_day === null || analytics?.momentum_5_day === undefined ? (
            "--"
          ) : (
            <PercentValue value={analytics.momentum_5_day} />
          )
        }
      />
      <MetricTile
        label={labels.riskFree}
        value={
          analytics ? <PercentValue value={analytics.risk_free_rate_proxy} /> : "--"
        }
      />
    </div>
  );
}
