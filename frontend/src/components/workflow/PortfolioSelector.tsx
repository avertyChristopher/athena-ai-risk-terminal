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

  const selectedTotalValue =
    (selectedPortfolio?.cash ?? 0) +
    holdings.reduce((total, holding) => total + holding.market_value, 0);

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
              {portfolio.strategy_type ? ` - ${portfolio.strategy_type}` : ""}
              {portfolio.risk_profile ? ` - ${portfolio.risk_profile}` : ""}
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
          <div className="workflow-stat-list__wide">
            <dt>{t("workflow.strategyType")}</dt>
            <dd>{selectedPortfolio.strategy_type ?? t("common.unavailable")}</dd>
          </div>
          <div>
            <dt>{t("workflow.totalValue")}</dt>
            <dd>
              {selectedTotalValue.toLocaleString(undefined, {
                style: "currency",
                currency: selectedPortfolio.base_currency,
                maximumFractionDigits: 0,
              })}
            </dd>
          </div>
          <div>
            <dt>{t("workflow.riskProfile")}</dt>
            <dd>{selectedPortfolio.risk_profile ?? t("common.unavailable")}</dd>
          </div>
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
