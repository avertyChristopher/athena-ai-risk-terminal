import { MetricCard } from "../../../components/finance/MetricCard";
import { MoneyValue } from "../../../components/finance/MoneyValue";
import { PercentValue } from "../../../components/finance/PercentValue";
import { PortfolioSummary } from "../../../types/portfolio";

type PortfolioSummaryCardsProps = {
  summary: PortfolioSummary;
  labels: {
    totalValue: string;
    positions: string;
    cash: string;
    largestPosition: string;
    benchmark: string;
    baseCurrency: string;
    cashWeight: string;
    concentration: string;
  };
};

export function PortfolioSummaryCards({
  summary,
  labels,
}: PortfolioSummaryCardsProps) {
  return (
    <section className="grid">
      <MetricCard
        title={labels.totalValue}
        value={
          <MoneyValue
            value={summary.total_market_value ?? summary.total_value}
            currency={summary.base_currency}
          />
        }
        subtitle={`${labels.benchmark}: ${summary.benchmark} · ${summary.data_source}`}
      />
      <MetricCard
        title={labels.positions}
        value={summary.number_of_positions}
        subtitle={`${labels.baseCurrency}: ${summary.base_currency} · ${summary.number_of_asset_classes} asset classes`}
      />
      <MetricCard
        title={labels.cash}
        value={<MoneyValue value={summary.cash} currency={summary.base_currency} />}
        subtitle={`${labels.cashWeight}: `}
        meta={<PercentValue value={summary.cash_weight} />}
      />
      <MetricCard
        title={labels.largestPosition}
        value={<PercentValue value={summary.largest_position_weight} />}
        subtitle={`${labels.concentration}: `}
        meta={<PercentValue value={summary.top_5_holdings_weight} />}
      />
    </section>
  );
}
