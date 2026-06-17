import { MoneyValue } from "../../../components/finance/MoneyValue";
import { PercentValue } from "../../../components/finance/PercentValue";
import { EmptyState } from "../../../components/ui/EmptyState";
import { PositionRead } from "../../../types/portfolio";
import { PortfolioStatusBadge } from "./PortfolioStatusBadge";

type PositionTableProps = {
  positions: PositionRead[];
  onEdit: (position: PositionRead) => void;
  onDelete: (positionId: string) => void;
  labels: {
    title: string;
    add: string;
    symbol: string;
    name: string;
    displayName?: string;
    type: string;
    quantity: string;
    averagePrice: string;
    currentPrice: string;
    marketValue: string;
    weight: string;
    portfolioWeight?: string;
    investedWeight?: string;
    costBasis?: string;
    unrealizedPnl?: string;
    currency: string;
    sector: string;
    country: string;
    exchange?: string;
    industry?: string;
    region?: string;
    actions: string;
    edit?: string;
    delete: string;
    emptyTitle?: string;
    emptyMessage?: string;
  };
  onAddClick: () => void;
};

export function PositionTable({
  positions,
  onEdit,
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
      {positions.length === 0 ? (
        <EmptyState
          title={labels.emptyTitle ?? "No positions"}
          message={
            labels.emptyMessage ??
            "Add a position to start calculating allocation, concentration and portfolio diagnostics."
          }
        />
      ) : (
        <div className="table-scroll">
          <table className="data-table">
            <thead>
              <tr>
                <th>{labels.symbol}</th>
                <th>{labels.name}</th>
                <th>{labels.displayName ?? "Display name"}</th>
                <th>{labels.type}</th>
                <th>{labels.quantity}</th>
                <th>{labels.averagePrice}</th>
                <th>{labels.currentPrice}</th>
                <th>{labels.marketValue}</th>
                <th>{labels.portfolioWeight ?? labels.weight}</th>
                <th>{labels.investedWeight ?? labels.weight}</th>
                <th>{labels.costBasis ?? "Cost basis"}</th>
                <th>{labels.unrealizedPnl ?? "Unrealized P&L"}</th>
                <th>{labels.currency}</th>
                <th>{labels.sector}</th>
                <th>{labels.country}</th>
                <th>{labels.exchange ?? "Exchange"}</th>
                <th>{labels.industry ?? "Industry"}</th>
                <th>{labels.region ?? "Region"}</th>
                <th>{labels.actions}</th>
              </tr>
            </thead>
            <tbody>
              {positions.map((position) => (
                <tr key={position.id}>
                  <td className="data-table__symbol">{position.symbol}</td>
                  <td>{position.asset_name}</td>
                  <td>{position.name ?? "--"}</td>
                  <td>
                    <PortfolioStatusBadge label={position.asset_type} variant="info" />
                  </td>
                  <td className="data-table__numeric">{position.quantity}</td>
                  <td className="data-table__numeric">
                    <MoneyValue
                      value={position.average_price}
                      currency={position.currency}
                    />
                  </td>
                  <td className="data-table__numeric">
                    <MoneyValue
                      value={position.current_price}
                      currency={position.currency}
                    />
                  </td>
                  <td className="data-table__numeric">
                    <MoneyValue
                      value={position.market_value}
                      currency={position.currency}
                    />
                  </td>
                  <td className="data-table__numeric">
                    <PercentValue value={position.portfolio_weight ?? position.weight} />
                  </td>
                  <td className="data-table__numeric">
                    <PercentValue value={position.invested_weight ?? position.weight} />
                  </td>
                  <td className="data-table__numeric">
                    <MoneyValue
                      value={position.cost_basis}
                      currency={position.currency}
                    />
                  </td>
                  <td
                    className={`data-table__numeric ${
                      position.unrealized_pnl >= 0
                        ? "positive-value"
                        : "negative-value"
                    }`}
                  >
                    <MoneyValue
                      value={position.unrealized_pnl}
                      currency={position.currency}
                    />{" "}
                    (<PercentValue value={position.unrealized_pnl_percent} />)
                  </td>
                  <td>{position.currency}</td>
                  <td>{position.sector}</td>
                  <td>{position.country}</td>
                  <td>{position.exchange ?? "--"}</td>
                  <td>{position.industry ?? "--"}</td>
                  <td>{position.region ?? "--"}</td>
                  <td className="data-table__actions">
                    <button
                      className="button button--ghost"
                      type="button"
                      onClick={() => onEdit(position)}
                    >
                      {labels.edit ?? "Edit"}
                    </button>
                    <button
                      className="button button--danger"
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
      )}
    </section>
  );
}
