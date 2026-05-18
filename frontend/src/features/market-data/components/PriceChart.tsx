import { PricePoint } from "../../../types/market-data";

type PriceChartProps = {
  title: string;
  prices: PricePoint[];
};

export function PriceChart({ title, prices }: PriceChartProps) {
  const closes = prices.map((price) => price.close);
  const points = buildLinePoints(closes);

  return (
    <section className="card chart-panel">
      <h2>{title}</h2>
      <svg className="line-chart" viewBox="0 0 100 44" role="img">
        <polyline points={points} fill="none" stroke="currentColor" strokeWidth="2" />
      </svg>
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
