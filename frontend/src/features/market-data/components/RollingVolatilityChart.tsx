import { PercentValue } from "../../../components/finance/PercentValue";
import { VolatilityResponse } from "../../../types/market-data";

type RollingVolatilityChartProps = {
  title: string;
  volatility?: VolatilityResponse;
  labels: {
    daily: string;
    annualized: string;
  };
};

export function RollingVolatilityChart({
  title,
  volatility,
  labels,
}: RollingVolatilityChartProps) {
  return (
    <section className="card chart-panel volatility-panel">
      <h2>{title}</h2>
      <div>
        <span>{labels.daily}</span>
        <strong>
          {volatility ? <PercentValue value={volatility.daily_volatility} /> : "--"}
        </strong>
      </div>
      <div>
        <span>{labels.annualized}</span>
        <strong>
          {volatility ? (
            <PercentValue value={volatility.annualized_volatility} />
          ) : (
            "--"
          )}
        </strong>
      </div>
    </section>
  );
}
