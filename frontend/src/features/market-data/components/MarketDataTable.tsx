import { MoneyValue } from "../../../components/finance/MoneyValue";
import { PricePoint } from "../../../types/market-data";

type MarketDataTableProps = {
  title: string;
  prices: PricePoint[];
  currency: string;
  labels: {
    date: string;
    open: string;
    high: string;
    low: string;
    close: string;
    volume: string;
  };
};

export function MarketDataTable({
  title,
  prices,
  currency,
  labels,
}: MarketDataTableProps) {
  return (
    <section className="card table-section">
      <h2>{title}</h2>
      <div className="table-scroll">
        <table className="data-table">
          <thead>
            <tr>
              <th>{labels.date}</th>
              <th>{labels.open}</th>
              <th>{labels.high}</th>
              <th>{labels.low}</th>
              <th>{labels.close}</th>
              <th>{labels.volume}</th>
            </tr>
          </thead>
          <tbody>
            {prices.map((price) => (
              <tr key={price.date}>
                <td>{price.date}</td>
                <td>
                  <MoneyValue value={price.open} currency={currency} />
                </td>
                <td>
                  <MoneyValue value={price.high} currency={currency} />
                </td>
                <td>
                  <MoneyValue value={price.low} currency={currency} />
                </td>
                <td>
                  <MoneyValue value={price.close} currency={currency} />
                </td>
                <td>{price.volume.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
