import { PercentValue } from "../../../components/finance/PercentValue";
import { MarketDataAnalyticsResponse } from "../../../types/market-data";

type PercentilesTableProps = {
  title: string;
  analytics?: MarketDataAnalyticsResponse;
};

export function PercentilesTable({ title, analytics }: PercentilesTableProps) {
  const percentiles = Object.entries(analytics?.percentiles ?? {});

  return (
    <section className="card compact-table-card">
      <h3>{title}</h3>
      <table className="compact-table">
        <tbody>
          {percentiles.map(([label, value]) => (
            <tr key={label}>
              <th>{label.toUpperCase()}</th>
              <td>
                <PercentValue value={value} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
