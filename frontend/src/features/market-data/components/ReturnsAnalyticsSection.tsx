import {
  MarketDataAnalyticsResponse,
  ReturnPoint,
} from "../../../types/market-data";
import { AnalyticsSection } from "./AnalyticsSection";
import { CumulativeReturnsChart } from "./CumulativeReturnsChart";
import { ReturnsChart } from "./ReturnsChart";
import { ReturnsStatsCards } from "./ReturnsStatsCards";

type ReturnsAnalyticsSectionProps = {
  analytics?: MarketDataAnalyticsResponse;
  returns: ReturnPoint[];
  labels: {
    title: string;
    description: string;
    returnsChart: string;
    cumulativeChart: string;
    simple: string;
    log: string;
    holdingPeriod: string;
    cumulative: string;
    arithmetic: string;
    geometric: string;
    annualized: string;
  };
};

export function ReturnsAnalyticsSection({
  analytics,
  returns,
  labels,
}: ReturnsAnalyticsSectionProps) {
  return (
    <AnalyticsSection title={labels.title} description={labels.description}>
      <ReturnsStatsCards
        analytics={analytics}
        latestLogReturn={returns[returns.length - 1]?.log_return ?? 0}
        labels={labels}
      />
      <div className="section-grid section-grid--two">
        <ReturnsChart title={labels.returnsChart} returns={returns} />
        <CumulativeReturnsChart title={labels.cumulativeChart} returns={returns} />
      </div>
    </AnalyticsSection>
  );
}
