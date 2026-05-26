type EquityOption = {
  symbol: string;
  name: string;
};

type EquitySelectorProps = {
  options: EquityOption[];
  selectedSymbol: string;
  onSelect: (symbol: string) => void;
  label: string;
};

export function EquitySelector({
  options,
  selectedSymbol,
  onSelect,
  label,
}: EquitySelectorProps) {
  return (
    <label className="form-field equity-selector">
      <span>{label}</span>
      <select
        value={selectedSymbol}
        onChange={(event) => onSelect(event.target.value)}
      >
        {options.map((option) => (
          <option key={option.symbol} value={option.symbol}>
            {option.symbol} - {option.name}
          </option>
        ))}
      </select>
    </label>
  );
}
