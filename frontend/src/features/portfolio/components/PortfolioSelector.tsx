import { PortfolioRead } from "../../../types/portfolio";

type PortfolioSelectorProps = {
  portfolios: PortfolioRead[];
  selectedPortfolioId: string;
  onSelect: (portfolioId: string) => void;
  label: string;
};

export function PortfolioSelector({
  portfolios,
  selectedPortfolioId,
  onSelect,
  label,
}: PortfolioSelectorProps) {
  return (
    <label className="form-field portfolio-selector">
      <span>{label}</span>
      <select
        value={selectedPortfolioId}
        onChange={(event) => onSelect(event.target.value)}
      >
        {portfolios.map((portfolio) => (
          <option key={portfolio.id} value={portfolio.id}>
            {portfolio.name}
          </option>
        ))}
      </select>
    </label>
  );
}
