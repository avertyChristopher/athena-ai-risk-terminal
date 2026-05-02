import { useTranslation } from "../../hooks/useTranslation";

export type RiskLevel = "low" | "medium" | "high" | "critical";

type RiskBadgeProps = {
  level: RiskLevel;
};

export function RiskBadge({ level }: RiskBadgeProps) {
  const { t } = useTranslation();

  return (
    <span className={`risk-badge risk-badge--${level}`}>
      {t(`common.riskLevels.${level}`)}
    </span>
  );
}
