import {
  MarketDataAnalyticsResponse,
  ReturnPoint,
} from "../../../types/market-data";
import { AnalyticsSection } from "./AnalyticsSection";
import { DistributionStatsCards } from "./DistributionStatsCards";
import { OutliersTable } from "./OutliersTable";
import { PercentilesTable } from "./PercentilesTable";
import { ReturnDistributionChart } from "./ReturnDistributionChart";

type DistributionStatsSectionProps = {
  analytics?: MarketDataAnalyticsResponse;
  returns: ReturnPoint[];
  labels: {
    title: string;
    description: string;
    distribution: string;
    percentiles: string;
    outliers: string;
    emptyOutliers: string;
    skewness: string;
    kurtosis: string;
    normalComparison: string;
  };
};

export function DistributionStatsSection({
  analytics,
  returns,
  labels,
}: DistributionStatsSectionProps) {
  return (
    <AnalyticsSection title={labels.title} description={labels.description}>
      <DistributionStatsCards analytics={analytics} labels={labels} />
      <div className="section-grid section-grid--three">
        <ReturnDistributionChart title={labels.distribution} returns={returns} />
        <PercentilesTable title={labels.percentiles} analytics={analytics} />
        <OutliersTable
          title={labels.outliers}
          returns={returns}
          outlierIndexes={analytics?.outlier_indexes ?? []}
          emptyLabel={labels.emptyOutliers}
        />
      </div>
    </AnalyticsSection>
  );
}
