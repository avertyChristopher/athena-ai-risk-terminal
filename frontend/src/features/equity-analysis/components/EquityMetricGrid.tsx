import { ReactNode } from "react";

type EquityMetricGridProps = {
  metrics: Array<{
    label: string;
    value: ReactNode;
    note?: string;
  }>;
};

export function EquityMetricGrid({ metrics }: EquityMetricGridProps) {
  return (
    <div className="metric-grid equity-metric-grid">
      {metrics.map((metric) => (
        <div className="metric-tile" key={metric.label}>
          <span>{metric.label}</span>
          <strong>{metric.value}</strong>
          {metric.note ? <small>{metric.note}</small> : null}
        </div>
      ))}
    </div>
  );
}
