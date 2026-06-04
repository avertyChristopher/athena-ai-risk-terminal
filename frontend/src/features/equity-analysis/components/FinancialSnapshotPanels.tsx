import { formatLargeCurrency } from "../../../lib/formatters";
import { EquityFundamentalsResponse } from "../../../types/equity";

type FinancialSnapshotPanelsProps = {
  fundamentals?: EquityFundamentalsResponse;
  labels: {
    incomeStatement: string;
    balanceSheet: string;
    cashFlow: string;
    revenue: string;
    grossProfit: string;
    operatingIncome: string;
    ebit: string;
    ebitda: string;
    netIncome: string;
    assets: string;
    liabilities: string;
    equity: string;
    debt: string;
    cash: string;
    workingCapital: string;
    operatingCashFlow: string;
    capex: string;
    freeCashFlow: string;
  };
};

export function FinancialSnapshotPanels({
  fundamentals,
  labels,
}: FinancialSnapshotPanelsProps) {
  if (!fundamentals) {
    return <section className="card equity-card">{labels.incomeStatement}</section>;
  }

  return (
    <div className="section-grid section-grid--three">
      <SnapshotCard
        title={labels.incomeStatement}
        rows={[
          [labels.revenue, fundamentals.revenue],
          [labels.grossProfit, fundamentals.gross_profit],
          [labels.operatingIncome, fundamentals.operating_income],
          [labels.ebit, fundamentals.ebit],
          [labels.ebitda, fundamentals.ebitda],
          [labels.netIncome, fundamentals.net_income],
        ]}
      />
      <SnapshotCard
        title={labels.balanceSheet}
        rows={[
          [labels.assets, fundamentals.assets],
          [labels.liabilities, fundamentals.liabilities],
          [labels.equity, fundamentals.equity],
          [labels.debt, fundamentals.debt],
          [labels.cash, fundamentals.cash],
          [labels.workingCapital, fundamentals.working_capital],
        ]}
      />
      <SnapshotCard
        title={labels.cashFlow}
        rows={[
          [labels.operatingCashFlow, fundamentals.operating_cash_flow],
          [labels.capex, fundamentals.capital_expenditures],
          [labels.freeCashFlow, fundamentals.free_cash_flow],
        ]}
      />
    </div>
  );
}

function SnapshotCard({
  title,
  rows,
}: {
  title: string;
  rows: Array<[string, number | null]>;
}) {
  return (
    <section className="card equity-card compact-table-card">
      <h3>{title}</h3>
      <table className="compact-table">
        <tbody>
          {rows.map(([label, value]) => (
            <tr key={label}>
              <td>{label}</td>
              <td>{formatLargeCurrency(value)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
