import { MarketAsset } from "../../../types/market-data";

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
  return (
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
  );
}
