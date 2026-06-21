import { StatusBadge } from "../../../components/ui/StatusBadge";
import type { StatusBadgeVariant } from "../../../components/ui/StatusBadge";

type TradeStatusBadgeVariant = StatusBadgeVariant;

type TradeStatusBadgeProps = {
  label: string;
  variant?: TradeStatusBadgeVariant;
};

export function TradeStatusBadge({
  label,
  variant = "neutral",
}: TradeStatusBadgeProps) {
  return <StatusBadge label={label} variant={variant} />;
}

export type { TradeStatusBadgeVariant };
