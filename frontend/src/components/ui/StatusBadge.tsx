export type StatusBadgeVariant =
  | "neutral"
  | "info"
  | "success"
  | "warning"
  | "danger";

type StatusBadgeProps = {
  label: string;
  variant?: StatusBadgeVariant;
};

export function StatusBadge({ label, variant = "neutral" }: StatusBadgeProps) {
  return (
    <span className={`risk-monitor-status-badge risk-monitor-status-badge--${variant}`}>
      {label}
    </span>
  );
}
