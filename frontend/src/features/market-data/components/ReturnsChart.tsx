import { PercentValue } from "../../../components/finance/PercentValue";
import { ReturnPoint } from "../../../types/market-data";

type ReturnsChartProps = {
  title: string;
  returns: ReturnPoint[];
};

export function ReturnsChart({ title, returns }: ReturnsChartProps) {
  return (
    <section className="card chart-panel">
      <h2>{title}</h2>
      <div className="return-bars">
        {returns.map((item) => (
          <div className="return-bar" key={item.date}>
            <span>{item.date.slice(5)}</span>
            <div className="return-bar__track">
              <div
                className={
                  item.simple_return >= 0
                    ? "return-bar__fill return-bar__fill--positive"
                    : "return-bar__fill return-bar__fill--negative"
                }
                style={{ width: `${Math.min(Math.abs(item.simple_return) * 1400, 100)}%` }}
              />
            </div>
            <strong>
              <PercentValue value={item.simple_return} />
            </strong>
          </div>
        ))}
      </div>
    </section>
  );
}
