export function formatCurrency(
  value: number,
  currency = "USD",
  locale = "en-CA",
) {
  return new Intl.NumberFormat(locale, {
    style: "currency",
    currency,
    maximumFractionDigits: 2,
  }).format(value);
}

export function formatPercent(value: number, locale = "en-CA") {
  return new Intl.NumberFormat(locale, {
    style: "percent",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value);
}

export function formatLargeCurrency(
  value: number | null | undefined,
  currency = "USD",
  locale = "en-CA",
) {
  if (value === null || value === undefined) {
    return "--";
  }

  return `${formatCurrency(value, currency, locale)}B`;
}

export function formatMultiple(value: number | null | undefined) {
  if (value === null || value === undefined) {
    return "--";
  }

  return `${value.toFixed(1)}x`;
}
