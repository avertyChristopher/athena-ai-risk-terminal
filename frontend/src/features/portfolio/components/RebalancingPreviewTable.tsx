import { MoneyValue } from "../../../components/finance/MoneyValue";
import { PercentValue } from "../../../components/finance/PercentValue";
import { RebalancingPreviewResponse } from "../../../types/portfolio";
import { PortfolioStatusBadge } from "./PortfolioStatusBadge";

type RebalancingPreviewTableProps = {
  preview: RebalancingPreviewResponse;
  currency: string;
  labels: {
    name: string;
    action: string;
    currentValue: string;
    targetValue: string;
    valueDifference: string;
    quantity: string;
    turnover: string;
    notes: string;
  };
};

export function RebalancingPreviewTable({
  preview,
  currency,
  labels,
}: RebalancingPreviewTableProps) {
  return (
    <div className="portfolio-rebalancing-preview">
      <div className="portfolio-rebalancing-preview__summary">
        <span>{labels.turnover}</span>
        <strong>
          <PercentValue value={preview.turnover_estimate} />
        </strong>
      </div>
      <div className="table-scroll">
        <table className="data-table portfolio-rebalance-table">
          <thead>
            <tr>
              <th>{labels.name}</th>
              <th>{labels.action}</th>
              <th>{labels.currentValue}</th>
              <th>{labels.targetValue}</th>
              <th>{labels.valueDifference}</th>
              <th>{labels.quantity}</th>
            </tr>
          </thead>
          <tbody>
            {preview.items.map((item) => {
              const action = item.action.toUpperCase();
              const quantity = Math.abs(item.estimated_quantity_difference);
              const valueTone =
                item.value_difference > 0
                  ? "positive-value"
                  : item.value_difference < 0
                    ? "negative-value"
                    : "";

              return (
                <tr key={item.name}>
                  <td className="data-table__symbol">{item.name}</td>
                  <td>
                    <PortfolioStatusBadge
                      label={action}
                      variant={action === "SELL" ? "warning" : "success"}
                    />
                  </td>
                  <td className="data-table__numeric">
                    <MoneyValue
                      value={item.current_market_value}
                      currency={currency}
                    />
                  </td>
                  <td className="data-table__numeric">
                    <MoneyValue
                      value={item.target_market_value}
                      currency={currency}
                    />
                  </td>
                  <td className={`data-table__numeric ${valueTone}`}>
                    <MoneyValue value={item.value_difference} currency={currency} />
                  </td>
                  <td className="data-table__numeric">
                    {action} {quantity.toFixed(2)}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      {preview.notes.length ? (
        <div className="portfolio-note-list">
          <strong>{labels.notes}</strong>
          <ul>
            {preview.notes.map((note) => (
              <li key={note}>{note}</li>
            ))}
          </ul>
        </div>
      ) : null}
    </div>
  );
}
