import {
  MarketDataAnalyticsResponse,
  ReturnPoint,
  VolatilityResponse,
} from "../../../types/market-data";
import { AnalyticsSection } from "./AnalyticsSection";
import { DrawdownChart } from "./DrawdownChart";
import { RollingVolatilityChart } from "./RollingVolatilityChart";
import { VolatilityStatsCards } from "./VolatilityStatsCards";

type RiskVolatilitySectionProps = {
  analytics?: MarketDataAnalyticsResponse;
  returns: ReturnPoint[];
  volatility?: VolatilityResponse;
  labels: {
    title: string;
    description: string;
    rollingVolatility: string;
    drawdown: string;
    variance: string;
    standardDeviation: string;
    dailyVolatility: string;
    annualizedVolatility: string;
    maxDrawdown: string;
    daily: string;
    annualized: string;
  };
};

export function RiskVolatilitySection({
  analytics,
  returns,
  volatility,
  labels,
}: RiskVolatilitySectionProps) {
  return (
    <AnalyticsSection title={labels.title} description={labels.description}>
      <VolatilityStatsCards analytics={analytics} labels={labels} />
      <div className="section-grid section-grid--two">
        <RollingVolatilityChart
          title={labels.rollingVolatility}
          volatility={volatility}
          labels={{ daily: labels.daily, annualized: labels.annualized }}
        />
        <DrawdownChart title={labels.drawdown} returns={returns} />
      </div>
    </AnalyticsSection>
  );
}
