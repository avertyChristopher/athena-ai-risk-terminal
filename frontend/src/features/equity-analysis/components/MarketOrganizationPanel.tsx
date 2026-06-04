import { formatLargeCurrency, formatMultiple } from "../../../lib/formatters";
import { EquitySecurityProfileResponse } from "../../../types/equity";

type MarketOrganizationPanelProps = {
  profile?: EquitySecurityProfileResponse;
  labels: {
    instrumentsTitle: string;
    marketTitle: string;
    marketVsBookTitle: string;
    type: string;
    exchange: string;
    currency: string;
    voting: string;
    liquidity: string;
    marketCap: string;
    freeFloatMarketCap: string;
    bookValuePerShare: string;
    marketToBook: string;
    demoBadge: string;
  };
};

export function MarketOrganizationPanel({
  profile,
  labels,
}: MarketOrganizationPanelProps) {
  if (!profile) {
    return <section className="card equity-card">{labels.instrumentsTitle}</section>;
  }

  return (
    <div className="section-grid section-grid--three">
      <section className="card equity-card">
        <h3>{labels.instrumentsTitle}</h3>
        <dl className="equity-definition-list">
          <Definition label={labels.type} value={profile.security_type} />
          <Definition label={labels.voting} value={profile.voting_rights} />
          <Definition label={labels.currency} value={profile.currency} />
        </dl>
      </section>
      <section className="card equity-card">
        <h3>{labels.marketTitle}</h3>
        <dl className="equity-definition-list">
          <Definition label={labels.exchange} value={profile.exchange} />
          <Definition label={labels.liquidity} value={profile.liquidity_note} />
          <Definition label={labels.demoBadge} value={profile.placeholders[0]} />
        </dl>
      </section>
      <section className="card equity-card">
        <h3>{labels.marketVsBookTitle}</h3>
        <dl className="equity-definition-list">
          <Definition
            label={labels.marketCap}
            value={formatLargeCurrency(profile.market_cap)}
          />
          <Definition
            label={labels.freeFloatMarketCap}
            value={formatLargeCurrency(profile.free_float_market_cap)}
          />
          <Definition
            label={labels.bookValuePerShare}
            value={
              profile.book_value_per_share === null
                ? "--"
                : `$${profile.book_value_per_share.toFixed(2)}`
            }
          />
          <Definition
            label={labels.marketToBook}
            value={formatMultiple(profile.market_to_book_value)}
          />
        </dl>
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
