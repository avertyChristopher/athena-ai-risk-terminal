import { ReactNode } from "react";

import { MoneyValue } from "../../../components/finance/MoneyValue";
import { PercentValue } from "../../../components/finance/PercentValue";
import {
  DataQualityResponse,
  MarketAsset,
  MarketDataAnalyticsResponse,
} from "../../../types/market-data";

type AssetSummaryPanelProps = {
  asset?: MarketAsset;
  analytics?: MarketDataAnalyticsResponse;
  quality?: DataQualityResponse;
  labels: {
    asset: string;
    latestPrice: string;
    latestReturn: string;
    annualizedVolatility: string;
    maxDrawdown: string;
    quality: string;
    valid: string;
    review: string;
  };
};

export function AssetSummaryPanel({
  asset,
  analytics,
  quality,
  labels,
}: AssetSummaryPanelProps) {
  return (
    <section className="asset-summary">
      <div className="asset-summary__identity">
        <span>{labels.asset}</span>
        <strong>{asset?.symbol ?? "--"}</strong>
        <small>{asset?.name ?? ""}</small>
      </div>
      <SummaryMetric label={labels.latestPrice}>
        {analytics ? (
          <MoneyValue value={analytics.latest_price} currency={asset?.currency ?? "USD"} />
        ) : (
          "--"
        )}
      </SummaryMetric>
      <SummaryMetric label={labels.latestReturn}>
        {analytics ? <PercentValue value={analytics.latest_return} /> : "--"}
      </SummaryMetric>
      <SummaryMetric label={labels.annualizedVolatility}>
        {analytics ? <PercentValue value={analytics.annualized_volatility} /> : "--"}
      </SummaryMetric>
      <SummaryMetric label={labels.maxDrawdown}>
        {analytics ? <PercentValue value={analytics.max_drawdown} /> : "--"}
      </SummaryMetric>
      <SummaryMetric label={labels.quality}>
        <span
          className={quality?.is_valid ? "status-pill" : "status-pill status-pill--warn"}
        >
          {quality ? (quality.is_valid ? labels.valid : labels.review) : "--"}
        </span>
      </SummaryMetric>
    </section>
  );
}

function SummaryMetric({
  label,
  children,
}: {
  label: string;
  children: ReactNode;
}) {
  return (
    <div className="asset-summary__metric">
      <span>{label}</span>
      <strong>{children}</strong>
    </div>
  );
}
