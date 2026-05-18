import { MarketDataAnalyticsResponse } from "../../../types/market-data";

type BenchmarkStatsTableProps = {
  title: string;
  analytics?: MarketDataAnalyticsResponse;
  labels: {
    benchmark: string;
    covariance: string;
    correlation: string;
    beta: string;
  };
};

export function BenchmarkStatsTable({
  title,
  analytics,
  labels,
}: BenchmarkStatsTableProps) {
  return (
    <section className="card compact-table-card">
      <h3>{title}</h3>
      <table className="compact-table">
        <tbody>
          <tr>
            <th>{labels.benchmark}</th>
            <td>{analytics?.benchmark_symbol ?? "--"}</td>
          </tr>
          <tr>
            <th>{labels.covariance}</th>
            <td>{(analytics?.covariance_with_benchmark ?? 0).toFixed(6)}</td>
          </tr>
          <tr>
            <th>{labels.correlation}</th>
            <td>{(analytics?.correlation_with_benchmark ?? 0).toFixed(3)}</td>
          </tr>
          <tr>
            <th>{labels.beta}</th>
            <td>{(analytics?.beta_vs_benchmark ?? 0).toFixed(3)}</td>
          </tr>
        </tbody>
      </table>
    </section>
  );
}
