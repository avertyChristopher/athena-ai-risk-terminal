import type { ReactNode } from "react";

type TradeMetricCardProps = {
  title: string;
  value: ReactNode;
  subtitle?: ReactNode;
  tone?: "neutral" | "positive" | "warning" | "negative";
};

export function TradeMetricCard({
  title,
  value,
  subtitle,
  tone = "neutral",
}: TradeMetricCardProps) {
  return (
    <article className={`trade-metric-card trade-metric-card--${tone}`}>
      <span>{title}</span>
      <strong>{value}</strong>
      {subtitle ? <p>{subtitle}</p> : null}
    </article>
  );
}
