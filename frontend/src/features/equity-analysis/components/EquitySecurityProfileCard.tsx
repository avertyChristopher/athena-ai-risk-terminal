import { SecurityProfile } from "../../../types/equity";

type EquitySecurityProfileCardProps = {
  profile?: SecurityProfile;
  labels: {
    title: string;
    equityType: string;
    votingRights: string;
    dividendProfile: string;
    bookValueContext: string;
    riskReturnNotes: string;
  };
};

export function EquitySecurityProfileCard({
  profile,
  labels,
}: EquitySecurityProfileCardProps) {
  if (!profile) {
    return <section className="card equity-card">{labels.title}</section>;
  }

  return (
    <section className="card equity-card">
      <h3>{labels.title}</h3>
      <dl className="equity-definition-list">
        <div>
          <dt>{labels.equityType}</dt>
          <dd>{profile.equity_type}</dd>
        </div>
        <div>
          <dt>{labels.votingRights}</dt>
          <dd>{profile.voting_rights}</dd>
        </div>
        <div>
          <dt>{labels.dividendProfile}</dt>
          <dd>{profile.dividend_profile}</dd>
        </div>
        <div>
          <dt>{labels.bookValueContext}</dt>
          <dd>{profile.book_value_context}</dd>
        </div>
      </dl>
      <h4>{labels.riskReturnNotes}</h4>
      <ul className="equity-list">
        {profile.risk_return_notes.map((note) => (
          <li key={note}>{note}</li>
        ))}
      </ul>
    </section>
  );
}
