import { MoneyValue } from "../../../components/finance/MoneyValue";
import { PercentValue } from "../../../components/finance/PercentValue";
import { PositionRead } from "../../../types/portfolio";

type PositionTableProps = {
  positions: PositionRead[];
  onDelete: (positionId: string) => void;
  labels: {
    title: string;
    add: string;
    symbol: string;
    name: string;
    type: string;
    quantity: string;
    averagePrice: string;
    currentPrice: string;
    marketValue: string;
    weight: string;
    currency: string;
    sector: string;
    country: string;
    actions: string;
    delete: string;
  };
  onAddClick: () => void;
};

export function PositionTable({
  positions,
  onDelete,
  labels,
  onAddClick,
}: PositionTableProps) {
  return (
    <section className="card table-section">
      <div className="section-heading">
        <h2>{labels.title}</h2>
        <button className="button button--primary" type="button" onClick={onAddClick}>
          {labels.add}
        </button>
      </div>
      <div className="table-scroll">
        <table className="data-table">
          <thead>
            <tr>
              <th>{labels.symbol}</th>
              <th>{labels.name}</th>
              <th>{labels.type}</th>
              <th>{labels.quantity}</th>
              <th>{labels.averagePrice}</th>
              <th>{labels.currentPrice}</th>
              <th>{labels.marketValue}</th>
              <th>{labels.weight}</th>
              <th>{labels.currency}</th>
              <th>{labels.sector}</th>
              <th>{labels.country}</th>
              <th>{labels.actions}</th>
            </tr>
          </thead>
          <tbody>
            {positions.map((position) => (
              <tr key={position.id}>
                <td>{position.symbol}</td>
                <td>{position.asset_name}</td>
                <td>{position.asset_type}</td>
                <td>{position.quantity}</td>
                <td>
                  <MoneyValue
                    value={position.average_price}
                    currency={position.currency}
                  />
                </td>
                <td>
                  <MoneyValue
                    value={position.current_price}
                    currency={position.currency}
                  />
                </td>
                <td>
                  <MoneyValue
                    value={position.market_value}
                    currency={position.currency}
                  />
                </td>
                <td>
                  <PercentValue value={position.weight} />
                </td>
                <td>{position.currency}</td>
                <td>{position.sector}</td>
                <td>{position.country}</td>
                <td>
                  <button
                    className="button button--ghost"
                    type="button"
                    onClick={() => onDelete(position.id)}
                  >
                    {labels.delete}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
