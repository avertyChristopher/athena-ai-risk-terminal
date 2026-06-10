import { MarketAsset } from "../../../types/market-data";
import { useTranslation } from "../../../hooks/useTranslation";

type AssetSearchProps = {
  assets: MarketAsset[];
  selectedSymbol: string;
  onSelect: (symbol: string) => void;
  label: string;
};

export function AssetSearch({
  assets,
  selectedSymbol,
  onSelect,
  label,
}: AssetSearchProps) {
  const { t } = useTranslation();

  return (
    <section className="card selector-panel">
      <div className="selector-panel__copy">
        <span className="equity-kicker">{t("marketData.selectorEyebrow")}</span>
        <h2>{label}</h2>
        <p>{t("marketData.selectorDescription")}</p>
      </div>
      <label className="form-field market-data-selector">
        <span>{label}</span>
        <select
          value={selectedSymbol}
          onChange={(event) => onSelect(event.target.value)}
        >
          {assets.map((asset) => (
            <option key={asset.symbol} value={asset.symbol}>
              {asset.symbol} - {asset.name}
            </option>
          ))}
        </select>
      </label>
    </section>
  );
}
