import { MarketDataAnalyticsResponse } from "../../../types/market-data";
import { AnalyticsSection } from "./AnalyticsSection";
import { BenchmarkComparisonChart } from "./BenchmarkComparisonChart";
import { BenchmarkStatsTable } from "./BenchmarkStatsTable";
import { RelativePerformanceCards } from "./RelativePerformanceCards";

type BenchmarkAnalysisSectionProps = {
  analytics?: MarketDataAnalyticsResponse;
  labels: {
    title: string;
    description: string;
    comparison: string;
    stats: string;
    activeReturn: string;
    correlation: string;
    covariance: string;
    beta: string;
    sharpe: string;
    benchmark: string;
  };
};

export function BenchmarkAnalysisSection({
  analytics,
  labels,
}: BenchmarkAnalysisSectionProps) {
  return (
    <AnalyticsSection title={labels.title} description={labels.description}>
      <RelativePerformanceCards analytics={analytics} labels={labels} />
      <div className="section-grid section-grid--two">
        <BenchmarkComparisonChart title={labels.comparison} analytics={analytics} />
        <BenchmarkStatsTable
          title={labels.stats}
          analytics={analytics}
          labels={labels}
        />
      </div>
    </AnalyticsSection>
  );
}
