import { ReturnPoint } from "../../../types/market-data";

type ReturnDistributionChartProps = {
  title: string;
  returns: ReturnPoint[];
};

export function ReturnDistributionChart({
  title,
  returns,
}: ReturnDistributionChartProps) {
  const values = returns.map((item) => item.simple_return);
  const buckets = buildBuckets(values);
  const maxCount = Math.max(...buckets.map((bucket) => bucket.count), 1);

  return (
    <section className="card chart-panel">
      <h3>{title}</h3>
      <div className="distribution-bars">
        {buckets.map((bucket) => (
          <div className="distribution-bar" key={bucket.label}>
            <div className="distribution-bar__track">
              <div
                className="distribution-bar__fill"
                style={{ height: `${(bucket.count / maxCount) * 100}%` }}
              />
            </div>
            <span>{bucket.label}</span>
          </div>
        ))}
      </div>
    </section>
  );
}

function buildBuckets(values: number[]) {
  if (values.length === 0) {
    return [];
  }

  const min = Math.min(...values);
  const max = Math.max(...values);
  const bucketCount = 5;
  const width = (max - min || 0.01) / bucketCount;

  return Array.from({ length: bucketCount }, (_, index) => {
    const lower = min + width * index;
    const upper = index === bucketCount - 1 ? max + 0.0000001 : lower + width;
    const count = values.filter((value) => value >= lower && value < upper).length;

    return {
      label: `${(lower * 100).toFixed(1)}%`,
      count,
    };
  });
}
