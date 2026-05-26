import { formatPercent } from "../../../lib/formatters";
import { EquityValuationResponse } from "../../../types/equity";

type ValuationMultiplesTableProps = {
  valuation?: EquityValuationResponse;
  labels: {
    title: string;
    metric: string;
    value: string;
    pe: string;
    pb: string;
    ps: string;
    evEbitda: string;
    dividendYield: string;
    earningsYield: string;
    fcfYield: string;
    impliedCost: string;
    impliedGrowth: string;
  };
};

export function ValuationMultiplesTable({
  valuation,
  labels,
}: ValuationMultiplesTableProps) {
  const rows = valuation
    ? [
        [labels.pe, valuation.pe_ratio.toFixed(1)],
        [labels.pb, valuation.pb_ratio.toFixed(1)],
        [labels.ps, valuation.ps_ratio.toFixed(1)],
        [labels.evEbitda, valuation.ev_ebitda.toFixed(1)],
        [labels.dividendYield, formatPercent(valuation.dividend_yield)],
        [labels.earningsYield, formatPercent(valuation.earnings_yield)],
        [labels.fcfYield, formatPercent(valuation.free_cash_flow_yield)],
        [labels.impliedCost, formatPercent(valuation.implied_cost_of_equity)],
        [labels.impliedGrowth, formatPercent(valuation.implied_growth_rate)],
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
