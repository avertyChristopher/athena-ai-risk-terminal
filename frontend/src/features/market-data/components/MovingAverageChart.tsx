import { MoneyValue } from "../../../components/finance/MoneyValue";
import {
  MarketAsset,
  MarketDataAnalyticsResponse,
  PricePoint,
} from "../../../types/market-data";

type MovingAverageChartProps = {
  title: string;
  asset?: MarketAsset;
  prices: PricePoint[];
  analytics?: MarketDataAnalyticsResponse;
  labels: {
    latest: string;
    ma5: string;
    ma20: string;
  };
};

export function MovingAverageChart({
  title,
  asset,
  prices,
  analytics,
  labels,
}: MovingAverageChartProps) {
  const latestPrice = prices[prices.length - 1]?.close ?? 0;
  const currency = asset?.currency ?? "USD";

  return (
    <section className="card compact-table-card">
      <h3>{title}</h3>
      <table className="compact-table">
        <tbody>
          <tr>
            <th>{labels.latest}</th>
            <td>
              <MoneyValue value={latestPrice} currency={currency} />
            </td>
          </tr>
          <tr>
            <th>{labels.ma5}</th>
            <td>
              {analytics?.moving_average_5 === null ? (
                "--"
              ) : (
                <MoneyValue
                  value={analytics?.moving_average_5 ?? 0}
                  currency={currency}
                />
              )}
            </td>
          </tr>
          <tr>
            <th>{labels.ma20}</th>
            <td>
              {analytics?.moving_average_20 === null ? (
                "--"
              ) : (
                <MoneyValue
                  value={analytics?.moving_average_20 ?? 0}
                  currency={currency}
                />
              )}
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  );
}
