import { PercentValue } from "../../../components/finance/PercentValue";
import { ReturnPoint } from "../../../types/market-data";

type CumulativeReturnsChartProps = {
  title: string;
  returns: ReturnPoint[];
};

export function CumulativeReturnsChart({
  title,
  returns,
}: CumulativeReturnsChartProps) {
  const values = returns.map((item) => item.cumulative_return);
  const points = buildLinePoints(values);

  return (
    <section className="card chart-panel">
      <h3>{title}</h3>
      <svg className="line-chart" viewBox="0 0 100 44" role="img">
        <polyline points={points} fill="none" stroke="currentColor" strokeWidth="2" />
      </svg>
      <p className="chart-caption">
        <PercentValue value={values[values.length - 1] ?? 0} />
      </p>
    </section>
  );
}

function buildLinePoints(values: number[]) {
  if (values.length === 0) {
    return "";
  }

  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = max - min || 1;

  return values
    .map((value, index) => {
      const x = values.length === 1 ? 0 : (index / (values.length - 1)) * 100;
      const y = 40 - ((value - min) / range) * 36;
      return `${x},${y + 2}`;
    })
    .join(" ");
}
