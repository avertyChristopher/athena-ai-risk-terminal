import { useTranslation } from "../../hooks/useTranslation";
import { formatPercent } from "../../lib/formatters";

type PercentValueProps = {
  value: number;
};

export function PercentValue({ value }: PercentValueProps) {
  const { i18n } = useTranslation();

  return (
    <span>
      {formatPercent(value, i18n.language.startsWith("fr") ? "fr-CA" : "en-CA")}
    </span>
  );
}
