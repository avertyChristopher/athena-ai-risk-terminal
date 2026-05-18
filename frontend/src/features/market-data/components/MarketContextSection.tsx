import {
  MarketAsset,
  MarketDataAnalyticsResponse,
  PricePoint,
} from "../../../types/market-data";
import { AnalyticsSection } from "./AnalyticsSection";
import { MarketContextPanel } from "./MarketContextPanel";
import { MomentumCards } from "./MomentumCards";
import { MovingAverageChart } from "./MovingAverageChart";

type MarketContextSectionProps = {
  asset?: MarketAsset;
  analytics?: MarketDataAnalyticsResponse;
  prices: PricePoint[];
  labels: {
    title: string;
    description: string;
    movingAverages: string;
    marketData: string;
    ma5: string;
    ma20: string;
    latest: string;
    momentum5: string;
    riskFree: string;
    fxRate: string;
    currencyConsistency: string;
    yieldCurve2y: string;
    yieldCurve10y: string;
    commodityProxy: string;
  };
};

export function MarketContextSection({
  asset,
  analytics,
  prices,
  labels,
}: MarketContextSectionProps) {
  return (
    <AnalyticsSection title={labels.title} description={labels.description}>
      <MomentumCards asset={asset} analytics={analytics} labels={labels} />
      <div className="section-grid section-grid--two">
        <MovingAverageChart
          title={labels.movingAverages}
          asset={asset}
          prices={prices}
          analytics={analytics}
          labels={{
            latest: labels.latest,
            ma5: labels.ma5,
            ma20: labels.ma20,
          }}
        />
        <MarketContextPanel
          title={labels.marketData}
          analytics={analytics}
          labels={{
            fxRate: labels.fxRate,
            currencyConsistency: labels.currencyConsistency,
            yieldCurve2y: labels.yieldCurve2y,
            yieldCurve10y: labels.yieldCurve10y,
            commodityProxy: labels.commodityProxy,
          }}
        />
      </div>
    </AnalyticsSection>
  );
}
