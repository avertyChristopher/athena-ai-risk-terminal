type PortfolioStatusBadgeVariant =
  | "neutral"
  | "info"
  | "success"
  | "warning"
  | "danger";

type PortfolioStatusBadgeProps = {
  label: string;
  variant?: PortfolioStatusBadgeVariant;
};

export function PortfolioStatusBadge({
  label,
  variant = "neutral",
}: PortfolioStatusBadgeProps) {
  return (
    <span className={`portfolio-status-badge portfolio-status-badge--${variant}`}>
      {label}
    </span>
  );
}

export type { PortfolioStatusBadgeVariant };
