import { ImpactMetric } from "../../../types/trade";
import { TradeStatusBadge } from "./TradeStatusBadge";

type BeforeAfterTableProps = {
  metrics: ImpactMetric[];
  labels: {
    metric: string;
    before: string;
    after: string;
    change: string;
    limit: string;
    status: string;
  };
  formatValue: (metric: ImpactMetric, value: number | string | null) => string;
};

export function BeforeAfterTable({
  metrics,
  labels,
  formatValue,
}: BeforeAfterTableProps) {
  return (
    <div className="table-scroll">
      <table className="data-table trade-before-after-table">
        <thead>
          <tr>
            <th>{labels.metric}</th>
            <th>{labels.before}</th>
            <th>{labels.after}</th>
            <th>{labels.change}</th>
            <th>{labels.limit}</th>
            <th>{labels.status}</th>
          </tr>
        </thead>
        <tbody>
          {metrics.map((metric) => (
            <tr key={metric.name}>
              <td className="data-table__symbol">{metric.name}</td>
              <td className="data-table__numeric">
                {formatValue(metric, metric.before)}
              </td>
              <td className="data-table__numeric">
                {formatValue(metric, metric.after)}
              </td>
              <td
                className={`data-table__numeric ${
                  (metric.change ?? 0) >= 0 ? "positive-value" : "negative-value"
                }`}
              >
                {metric.change === null ? "-" : formatValue(metric, metric.change)}
              </td>
              <td className="data-table__numeric">
                {metric.limit === null ? "-" : formatValue(metric, metric.limit)}
              </td>
              <td>
                <TradeStatusBadge
                  label={metric.status}
                  variant={metric.status === "breach" ? "danger" : "success"}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
