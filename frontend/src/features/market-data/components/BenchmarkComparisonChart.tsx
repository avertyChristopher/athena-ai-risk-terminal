import { PercentValue } from "../../../components/finance/PercentValue";
import { MarketDataAnalyticsResponse } from "../../../types/market-data";

type BenchmarkComparisonChartProps = {
  title: string;
  analytics?: MarketDataAnalyticsResponse;
};

export function BenchmarkComparisonChart({
  title,
  analytics,
}: BenchmarkComparisonChartProps) {
  return (
    <section className="card chart-panel benchmark-chart">
      <h3>{title}</h3>
      <BenchmarkBar
        label={analytics?.symbol ?? "Asset"}
        value={analytics?.latest_return ?? 0}
      />
      <BenchmarkBar
        label={analytics?.benchmark_symbol ?? "Benchmark"}
        value={analytics?.benchmark_latest_return ?? 0}
      />
    </section>
  );
}

function BenchmarkBar({ label, value }: { label: string; value: number }) {
  return (
    <div className="benchmark-bar">
      <span>{label}</span>
      <div className="benchmark-bar__track">
        <div
          className={value >= 0 ? "benchmark-bar__fill" : "benchmark-bar__fill is-negative"}
          style={{ width: `${Math.min(Math.abs(value) * 1400, 100)}%` }}
        />
      </div>
      <strong>
        <PercentValue value={value} />
      </strong>
    </div>
  );
}
