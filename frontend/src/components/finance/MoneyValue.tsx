import { useTranslation } from "../../hooks/useTranslation";
import { formatCurrency } from "../../lib/formatters";

type MoneyValueProps = {
  value: number;
  currency?: string;
};

export function MoneyValue({
  value,
  currency = "USD",
}: MoneyValueProps) {
  const { i18n } = useTranslation();

  return (
    <span>
      {formatCurrency(
        value,
        currency,
        i18n.language.startsWith("fr") ? "fr-CA" : "en-CA",
      )}
    </span>
  );
}
