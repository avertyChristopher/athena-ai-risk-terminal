import {
  DataQualityResponse,
  MarketAsset,
  MarketDataAnalyticsResponse,
  PricePoint,
} from "../../../types/market-data";
import { MoneyValue } from "../../../components/finance/MoneyValue";
import { PercentValue } from "../../../components/finance/PercentValue";
import { AnalyticsSection } from "./AnalyticsSection";
import { DataQualityPanel } from "./DataQualityPanel";
import { MarketDataTable } from "./MarketDataTable";
import { PriceChart } from "./PriceChart";
import { ReferenceDataPanel } from "./ReferenceDataPanel";
import { VolumeChart } from "./VolumeChart";

type AssetOverviewSectionProps = {
  asset?: MarketAsset;
  analytics?: MarketDataAnalyticsResponse;
  prices: PricePoint[];
  quality?: DataQualityResponse;
  labels: {
    title: string;
    description: string;
    priceHistory: string;
    volume: string;
    table: string;
    quality: string;
    adjustedClose: string;
    corporateActions: string;
    averageVolume20: string;
    latestDollarVolume: string;
    liquidityScore: string;
    liquidity: string;
    highLiquidity: string;
    moderateLiquidity: string;
    referenceData: string;
    date: string;
    open: string;
    high: string;
    low: string;
    close: string;
    volumeColumn: string;
    rows: string;
    missing: string;
    duplicates: string;
    outliers: string;
  };
};

export function AssetOverviewSection({
  asset,
  analytics,
  prices,
  quality,
  labels,
}: AssetOverviewSectionProps) {
  return (
    <AnalyticsSection title={labels.title} description={labels.description}>
      <div className="section-grid section-grid--two">
        <PriceChart title={labels.priceHistory} prices={prices} />
        <VolumeChart title={labels.volume} prices={prices} />
      </div>
      <div className="section-grid section-grid--two">
        <DataQualityPanel
          title={labels.quality}
          quality={quality}
          labels={{
            rows: labels.rows,
            missing: labels.missing,
            duplicates: labels.duplicates,
            outliers: labels.outliers,
          }}
        />
        <ReferenceDataPanel
          title={labels.referenceData}
          items={[
            {
              label: labels.adjustedClose,
              value: analytics ? (
                <MoneyValue
                  value={analytics.adjusted_close_latest}
                  currency={asset?.currency ?? "USD"}
                />
              ) : (
                "--"
              ),
            },
            {
              label: labels.corporateActions,
              value: analytics?.corporate_action_status ?? "--",
            },
            {
              label: labels.averageVolume20,
              value: analytics
                ? analytics.average_volume_20.toLocaleString(undefined, {
                    maximumFractionDigits: 0,
                  })
                : "--",
            },
            {
              label: labels.latestDollarVolume,
              value: analytics ? (
                <MoneyValue
                  value={analytics.latest_dollar_volume}
                  currency={asset?.currency ?? "USD"}
                />
              ) : (
                "--"
              ),
            },
            {
              label: labels.liquidityScore,
              value: analytics ? (
                <PercentValue value={analytics.liquidity_score} />
              ) : (
                "--"
              ),
            },
            {
              label: labels.liquidity,
              value:
                analytics && analytics.liquidity_score > 0.6
                  ? labels.highLiquidity
                  : labels.moderateLiquidity,
            },
          ]}
        />
      </div>
      <MarketDataTable
        title={labels.table}
        prices={prices}
        currency={asset?.currency ?? "USD"}
        labels={{
          date: labels.date,
          open: labels.open,
          high: labels.high,
          low: labels.low,
          close: labels.close,
          volume: labels.volumeColumn,
        }}
      />
    </AnalyticsSection>
  );
}
