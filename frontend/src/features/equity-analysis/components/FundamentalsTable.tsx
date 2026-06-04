import { formatCurrency } from "../../../lib/formatters";
import { EquityFundamentalsResponse } from "../../../types/equity";

type FundamentalsTableProps = {
  fundamentals?: EquityFundamentalsResponse;
  labels: {
    title: string;
    metric: string;
    value: string;
    revenue: string;
    ebit: string;
    ebitda: string;
    netIncome: string;
    eps: string;
    dividends: string;
    assets: string;
    liabilities: string;
    equity: string;
    debt: string;
    cash: string;
    operatingCashFlow: string;
    freeCashFlow: string;
    bookValuePerShare: string;
    enterpriseValue: string;
  };
};

export function FundamentalsTable({
  fundamentals,
  labels,
}: FundamentalsTableProps) {
  const rows = fundamentals
    ? [
        [labels.revenue, formatBillions(fundamentals.revenue)],
        [labels.ebit, formatBillions(fundamentals.ebit)],
        [labels.ebitda, formatBillions(fundamentals.ebitda)],
        [labels.netIncome, formatBillions(fundamentals.net_income)],
        [labels.eps, formatNullableCurrency(fundamentals.eps)],
        [labels.dividends, formatNullableCurrency(fundamentals.dividends_per_share)],
        [labels.assets, formatBillions(fundamentals.assets)],
        [labels.liabilities, formatBillions(fundamentals.liabilities)],
        [labels.equity, formatBillions(fundamentals.equity)],
        [labels.debt, formatBillions(fundamentals.debt)],
        [labels.cash, formatBillions(fundamentals.cash)],
        [labels.operatingCashFlow, formatBillions(fundamentals.operating_cash_flow)],
        [labels.freeCashFlow, formatBillions(fundamentals.free_cash_flow)],
        [
          labels.bookValuePerShare,
          formatNullableCurrency(fundamentals.book_value_per_share),
        ],
        [labels.enterpriseValue, formatBillions(fundamentals.enterprise_value)],
      ]
    : [];

  return (
    <section className="card equity-card compact-table-card">
      <h3>{labels.title}</h3>
      <table className="compact-table">
        <thead>
          <tr>
            <th>{labels.metric}</th>
            <th>{labels.value}</th>
          </tr>
        </thead>
        <tbody>
          {rows.map(([label, value]) => (
            <tr key={label}>
              <td>{label}</td>
              <td>{value}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}

function formatBillions(value: number | null | undefined) {
  return value === null || value === undefined ? "--" : `${formatCurrency(value)}B`;
}

function formatNullableCurrency(value: number | null | undefined) {
  return value === null || value === undefined ? "--" : formatCurrency(value);
}
