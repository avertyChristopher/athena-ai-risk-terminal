type BenchmarkSelectorProps = {
  value: string;
  onChange: (value: string) => void;
  label: string;
};

const benchmarks = ["SPY", "QQQ", "BND", "AAPL", "MSFT"];

export function BenchmarkSelector({
  value,
  onChange,
  label,
}: BenchmarkSelectorProps) {
  return (
    <label className="form-field">
      <span>{label}</span>
      <select value={value} onChange={(event) => onChange(event.target.value)}>
        {benchmarks.map((benchmark) => (
          <option key={benchmark} value={benchmark}>
            {benchmark}
          </option>
        ))}
      </select>
    </label>
  );
}
