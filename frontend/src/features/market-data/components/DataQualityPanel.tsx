import { DataQualityResponse } from "../../../types/market-data";

type DataQualityPanelProps = {
  title: string;
  quality?: DataQualityResponse;
  labels: {
    rows: string;
    missing: string;
    duplicates: string;
    outliers: string;
  };
};

export function DataQualityPanel({
  title,
  quality,
  labels,
}: DataQualityPanelProps) {
  return (
    <section className="card data-quality-panel">
      <h2>{title}</h2>
      <dl>
        <div>
          <dt>{labels.rows}</dt>
          <dd>{quality?.rows ?? 0}</dd>
        </div>
        <div>
          <dt>{labels.missing}</dt>
          <dd>{quality?.missing_price_dates.length ?? 0}</dd>
        </div>
        <div>
          <dt>{labels.duplicates}</dt>
          <dd>{quality?.duplicate_dates.length ?? 0}</dd>
        </div>
        <div>
          <dt>{labels.outliers}</dt>
          <dd>{quality?.outlier_indexes.length ?? 0}</dd>
        </div>
      </dl>
    </section>
  );
}
