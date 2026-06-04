import {
  formatLargeCurrency,
  formatMultiple,
  formatPercent,
} from "../../../lib/formatters";
import {
  EquityPeerComparisonResponse,
  EquityRelativeValuationResponse,
} from "../../../types/equity";

type RelativeValuationCardsProps = {
  relative?: EquityRelativeValuationResponse;
  labels: {
    relativeTitle: string;
    multiple: string;
    company: string;
    peerMedian: string;
    status: string;
    premiumDiscount: string;
  };
};

type PeerComparisonTableProps = {
  peers?: EquityPeerComparisonResponse;
  labels: {
    peerTitle: string;
    symbol: string;
    pe: string;
    pb: string;
    roe: string;
    growth: string;
    valuation: string;
    benchmark: string;
    relativePerformance: string;
    summary: string;
  };
};

export function RelativeValuationCards({
  relative,
  labels,
}: RelativeValuationCardsProps) {
  if (!relative) {
    return <section className="card equity-card">{labels.relativeTitle}</section>;
  }

  const keys = ["pe_ratio", "pb_ratio", "ps_ratio", "ev_ebitda"];
  return (
    <section className="card equity-card compact-table-card">
      <h3>{labels.relativeTitle}</h3>
      <table className="compact-table">
        <thead>
          <tr>
            <th>{labels.multiple}</th>
            <th>{labels.company}</th>
            <th>{labels.peerMedian}</th>
            <th>{labels.status}</th>
            <th>{labels.premiumDiscount}</th>
          </tr>
        </thead>
        <tbody>
          {keys.map((key) => (
            <tr key={key}>
              <td>{key.toUpperCase().replace("_", " ")}</td>
              <td>{formatMultiple(relative.multiples[key])}</td>
              <td>{formatMultiple(relative.peer_medians[key])}</td>
              <td>{relative.multiple_status[key]}</td>
              <td>
                {relative.premium_discount_to_peers[key] === null
                  ? "--"
                  : formatPercent(relative.premium_discount_to_peers[key] ?? 0)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}

export function PeerComparisonTable({
  peers,
  labels,
}: PeerComparisonTableProps) {
  if (!peers) {
    return <section className="card equity-card">{labels.peerTitle}</section>;
  }

  return (
    <div className="section-grid section-grid--two">
      <section className="card equity-card compact-table-card">
        <h3>{labels.peerTitle}</h3>
        <table className="compact-table">
          <thead>
            <tr>
              <th>{labels.symbol}</th>
              <th>{labels.pe}</th>
              <th>{labels.pb}</th>
              <th>{labels.roe}</th>
              <th>{labels.growth}</th>
            </tr>
          </thead>
          <tbody>
            {peers.peer_rows.map((row) => (
              <tr key={String(row.symbol)}>
                <td>{String(row.symbol)}</td>
                <td>{formatMultiple(Number(row.pe_ratio))}</td>
                <td>{formatMultiple(Number(row.pb_ratio))}</td>
                <td>{formatPercent(Number(row.roe ?? 0))}</td>
                <td>{formatPercent(Number(row.revenue_growth ?? 0))}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
      <section className="card equity-card">
        <h3>{labels.benchmark}: {peers.benchmark_symbol}</h3>
        <dl className="equity-definition-list">
          <Definition
            label={labels.relativePerformance}
            value={
              peers.relative_performance_vs_benchmark === null
                ? "--"
                : formatPercent(peers.relative_performance_vs_benchmark)
            }
          />
          <Definition label={labels.roe} value={peers.profitability_vs_peers} />
          <Definition label={labels.growth} value={peers.growth_vs_peers} />
          <Definition label={labels.valuation} value={peers.valuation_vs_peers} />
        </dl>
        <p className="equity-note">
          <strong>{labels.summary}: </strong>
          {peers.sector_relative_summary}
        </p>
      </section>
    </div>
  );
}

function Definition({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt>{label}</dt>
      <dd>{value}</dd>
    </div>
  );
}

export function formatPeerValue(value: number | null | undefined) {
  return value === null || value === undefined ? "--" : formatLargeCurrency(value);
}
