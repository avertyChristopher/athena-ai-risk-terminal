import { ReturnPoint } from "../../../types/market-data";

type OutliersTableProps = {
  title: string;
  returns: ReturnPoint[];
  outlierIndexes: number[];
  emptyLabel: string;
};

export function OutliersTable({
  title,
  returns,
  outlierIndexes,
  emptyLabel,
}: OutliersTableProps) {
  const outliers = outlierIndexes
    .map((index) => returns[index])
    .filter((item): item is ReturnPoint => Boolean(item));

  return (
    <section className="card compact-table-card">
      <h3>{title}</h3>
      {outliers.length === 0 ? (
        <p className="muted-note">{emptyLabel}</p>
      ) : (
        <table className="compact-table">
          <tbody>
            {outliers.map((item) => (
              <tr key={item.date}>
                <th>{item.date}</th>
                <td>{(item.simple_return * 100).toFixed(2)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}
