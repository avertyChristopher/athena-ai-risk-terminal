import { PortfolioStatusBadge } from "./PortfolioStatusBadge";

type PortfolioWarningCardProps = {
  title: string;
  message: string;
  badge?: string;
  severity?: "warning" | "danger" | "info";
};

export function PortfolioWarningCard({
  title,
  message,
  badge,
  severity = "warning",
}: PortfolioWarningCardProps) {
  return (
    <article className={`portfolio-warning-card portfolio-warning-card--${severity}`}>
      <div className="portfolio-warning-card__header">
        <strong>{title}</strong>
        {badge ? <PortfolioStatusBadge label={badge} variant={severity} /> : null}
      </div>
      <p>{message}</p>
    </article>
  );
}
