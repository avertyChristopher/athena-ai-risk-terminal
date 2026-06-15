import type { ReactNode } from "react";

import { PortfolioStatusBadge } from "./PortfolioStatusBadge";

type PortfolioMetricCardProps = {
  title: string;
  value: ReactNode;
  subtitle?: ReactNode;
  badge?: string;
  tone?: "neutral" | "positive" | "warning" | "negative";
};

export function PortfolioMetricCard({
  title,
  value,
  subtitle,
  badge,
  tone = "neutral",
}: PortfolioMetricCardProps) {
  return (
    <article className={`portfolio-metric-card portfolio-metric-card--${tone}`}>
      <div className="portfolio-metric-card__header">
        <span>{title}</span>
        {badge ? <PortfolioStatusBadge label={badge} variant="info" /> : null}
      </div>
      <strong>{value}</strong>
      {subtitle ? <p>{subtitle}</p> : null}
    </article>
  );
}
