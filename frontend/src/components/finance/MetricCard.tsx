import { ReactNode } from "react";

import { Card } from "../ui/Card";

type MetricCardProps = {
  title: string;
  value: ReactNode;
  subtitle: string;
  meta?: ReactNode;
};

export function MetricCard({
  title,
  value,
  subtitle,
  meta,
}: MetricCardProps) {
  return (
    <Card className="metric-card">
      <div className="metric-card__header">
        <p className="metric-card__title">{title}</p>
      </div>
      <div className="metric-card__value">{value}</div>
      <div className="metric-card__meta">
        <p className="metric-card__subtitle">{subtitle}</p>
        {meta}
      </div>
    </Card>
  );
}
