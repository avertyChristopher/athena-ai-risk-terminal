import { StatusBadge } from "../../../components/ui/StatusBadge";
import type { StatusBadgeVariant } from "../../../components/ui/StatusBadge";

type PortfolioStatusBadgeVariant = StatusBadgeVariant;

type PortfolioStatusBadgeProps = {
  label: string;
  variant?: PortfolioStatusBadgeVariant;
};

export function PortfolioStatusBadge({
  label,
  variant = "neutral",
}: PortfolioStatusBadgeProps) {
  return <StatusBadge label={label} variant={variant} />;
}

export type { PortfolioStatusBadgeVariant };
