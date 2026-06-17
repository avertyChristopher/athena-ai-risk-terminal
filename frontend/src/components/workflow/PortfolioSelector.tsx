import { usePortfolioContext } from "../../context/PortfolioContext";
import { useTranslation } from "../../hooks/useTranslation";

type PortfolioSelectorProps = {
  compact?: boolean;
  showDetails?: boolean;
  className?: string;
  onPortfolioChange?: (portfolioId: string) => void;
};

export function PortfolioSelector({
  compact = false,
  showDetails = true,
  className = "",
  onPortfolioChange,
}: PortfolioSelectorProps) {
  const { t } = useTranslation();
  const {
    clearSelection,
    error,
    holdings,
    isLoading,
    portfolios,
    refreshPortfolios,
    selectPortfolio,
    selectedPortfolio,
    selectedPortfolioId,
  } = usePortfolioContext();

  function handlePortfolioChange(portfolioId: string) {
    selectPortfolio(portfolioId);
    onPortfolioChange?.(portfolioId);
  }

  return (
    <section
      className={`workflow-panel ${compact ? "workflow-panel--compact" : ""} ${className}`.trim()}
    >
      <header className="workflow-panel__header">
        <div>
          <span className="equity-kicker">{t("workflow.portfolioSelector")}</span>
          <h2>{t("workflow.selectedPortfolio")}</h2>
          {showDetails ? <p>{t("workflow.portfolioSelectorDescription")}</p> : null}
        </div>
        <div className="workflow-actions">
          <button
            className="button button--ghost"
            type="button"
            onClick={() => void refreshPortfolios()}
          >
            {t("workflow.refresh")}
          </button>
          <button className="button button--ghost" type="button" onClick={clearSelection}>
            {t("workflow.clear")}
          </button>
        </div>
      </header>

      <label className="form-field">
        <span>{t("workflow.portfolio")}</span>
        <select
          disabled={isLoading || portfolios.length === 0}
          value={selectedPortfolioId}
          onChange={(event) => handlePortfolioChange(event.target.value)}
        >
          <option value="">
            {isLoading ? t("workflow.portfolioLoading") : t("workflow.noPortfolio")}
          </option>
          {portfolios.map((portfolio) => (
            <option key={portfolio.id} value={portfolio.id}>
              {portfolio.name}
            </option>
          ))}
        </select>
      </label>

      {error ? (
        <p className="status-message status-message--error">
          {t("workflow.portfolioError")}
        </p>
      ) : null}

      {showDetails && selectedPortfolio ? (
        <dl className="workflow-stat-list">
          <div>
            <dt>{t("workflow.baseCurrency")}</dt>
            <dd>{selectedPortfolio.base_currency}</dd>
          </div>
          <div>
            <dt>{t("workflow.benchmark")}</dt>
            <dd>{selectedPortfolio.benchmark}</dd>
          </div>
          <div>
            <dt>{t("workflow.positions")}</dt>
            <dd>{holdings.length}</dd>
          </div>
        </dl>
      ) : null}
    </section>
  );
}
