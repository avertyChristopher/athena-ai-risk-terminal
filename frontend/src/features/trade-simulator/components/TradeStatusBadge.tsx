type TradeStatusBadgeVariant =
  | "neutral"
  | "info"
  | "success"
  | "warning"
  | "danger";

type TradeStatusBadgeProps = {
  label: string;
  variant?: TradeStatusBadgeVariant;
};

export function TradeStatusBadge({
  label,
  variant = "neutral",
}: TradeStatusBadgeProps) {
  return (
    <span className={`trade-status-badge trade-status-badge--${variant}`}>
      {label}
    </span>
  );
}

export type { TradeStatusBadgeVariant };
