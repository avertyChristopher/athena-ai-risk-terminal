import type { ReactNode } from "react";

import { usePortfolioContext } from "../../context/PortfolioContext";
import { useTranslation } from "../../hooks/useTranslation";
import type { PositionRead } from "../../types/portfolio";

export type SymbolSelectionMode = "standalone" | "portfolio";

export type StandaloneSymbolOption = {
  symbol: string;
  name?: string;
};

type SymbolSelectorProps = {
  mode: SymbolSelectionMode;
  selectedSymbol: string;
  onModeChange: (mode: SymbolSelectionMode) => void;
  onSymbolChange: (
    symbol: string,
    source?: StandaloneSymbolOption | PositionRead,
  ) => void;
  standaloneOptions?: StandaloneSymbolOption[];
  allowManualEntry?: boolean;
  title?: string;
  description?: string;
  warning?: ReactNode;
  className?: string;
};

export function SymbolSelector({
  mode,
  selectedSymbol,
  onModeChange,
  onSymbolChange,
  standaloneOptions = [],
  allowManualEntry = true,
  title,
  description,
  warning,
  className = "",
}: SymbolSelectorProps) {
  const { t } = useTranslation();
  const { holdings, selectSymbol, selectedPortfolioName } = usePortfolioContext();
  const normalizedSymbol = selectedSymbol.toUpperCase();
  const selectedStandaloneSymbol = standaloneOptions.some(
    (option) => option.symbol.toUpperCase() === normalizedSymbol,
  )
    ? normalizedSymbol
    : "";
  const selectedHolding =
    holdings.find(
      (holding) => holding.symbol.toUpperCase() === normalizedSymbol,
    ) ?? null;

  function commitSymbol(
    symbol: string,
    source?: StandaloneSymbolOption | PositionRead,
  ) {
    const nextSymbol = symbol.trim().toUpperCase();
    selectSymbol(nextSymbol);
    onSymbolChange(nextSymbol, source);
  }

  function handleModeChange(nextMode: SymbolSelectionMode) {
    onModeChange(nextMode);

    if (nextMode === "portfolio" && holdings.length > 0) {
      commitSymbol(holdings[0].symbol, holdings[0]);
    }
  }

  return (
    <section className={`workflow-panel ${className}`.trim()}>
      <header className="workflow-panel__header">
        <div>
          <span className="equity-kicker">{t("workflow.symbolMode")}</span>
          <h2>{title ?? t("workflow.symbol")}</h2>
          <p>
            {description ??
              (mode === "portfolio"
                ? t("workflow.portfolioModeDescription")
                : t("workflow.standaloneModeDescription"))}
          </p>
        </div>
      </header>

      <div className="workflow-segmented-control" role="group">
        <button
          className={mode === "standalone" ? "is-active" : ""}
          type="button"
          onClick={() => handleModeChange("standalone")}
        >
          {t("workflow.standaloneSymbol")}
        </button>
        <button
          className={mode === "portfolio" ? "is-active" : ""}
          type="button"
          onClick={() => handleModeChange("portfolio")}
        >
          {t("workflow.portfolioHolding")}
        </button>
      </div>

      {warning ? <div className="workflow-warning">{warning}</div> : null}

      {mode === "portfolio" ? (
        <div className="workflow-selector-grid">
          <label className="form-field">
            <span>{t("workflow.selectHolding")}</span>
            <select
              disabled={holdings.length === 0}
              value={selectedHolding?.symbol ?? ""}
              onChange={(event) => {
                const holding = holdings.find(
                  (item) => item.symbol === event.target.value,
                );
                if (holding) {
                  commitSymbol(holding.symbol, holding);
                }
              }}
            >
              <option value="">{t("workflow.noHoldings")}</option>
              {holdings.map((holding) => (
                <option key={holding.id} value={holding.symbol}>
                  {holding.symbol} - {holding.asset_name}
                </option>
              ))}
            </select>
          </label>

          <HoldingDetails
            holding={selectedHolding}
            portfolioName={selectedPortfolioName}
          />
        </div>
      ) : (
        <div className="workflow-selector-grid">
          {standaloneOptions.length > 0 ? (
            <label className="form-field">
              <span>{t("workflow.trackedUniverse")}</span>
              <select
                value={selectedStandaloneSymbol}
                onChange={(event) => {
                  const option = standaloneOptions.find(
                    (item) => item.symbol === event.target.value,
                  );
                  if (option) {
                    commitSymbol(option.symbol, option);
                  }
                }}
              >
                <option value="">{t("workflow.chooseTrackedSymbol")}</option>
                {standaloneOptions.map((option) => (
                  <option key={option.symbol} value={option.symbol}>
                    {option.symbol} - {option.name ?? option.symbol}
                  </option>
                ))}
              </select>
            </label>
          ) : null}

          {allowManualEntry ? (
            <label className="form-field">
              <span>{t("workflow.manualSymbol")}</span>
              <input
                value={selectedSymbol}
                onChange={(event) => commitSymbol(event.target.value)}
                placeholder="AAPL"
              />
            </label>
          ) : null}
        </div>
      )}
    </section>
  );
}

function HoldingDetails({
  holding,
  portfolioName,
}: {
  holding: PositionRead | null;
  portfolioName: string;
}) {
  const { t } = useTranslation();

  if (!holding) {
    return (
      <div className="workflow-symbol-details">
        <strong>{t("workflow.noHoldings")}</strong>
        <p>{portfolioName || t("workflow.noPortfolio")}</p>
      </div>
    );
  }

  return (
    <dl className="workflow-symbol-details">
      <div>
        <dt>{t("workflow.selectedHolding")}</dt>
        <dd>
          {holding.symbol} / {holding.asset_name}
        </dd>
      </div>
      <div>
        <dt>{t("workflow.assetType")}</dt>
        <dd>{holding.asset_type}</dd>
      </div>
      <div>
        <dt>{t("workflow.quantity")}</dt>
        <dd>{formatNumber(holding.quantity)}</dd>
      </div>
      <div>
        <dt>{t("workflow.currentPrice")}</dt>
        <dd>{formatCurrency(holding.current_price, holding.currency)}</dd>
      </div>
      <div>
        <dt>{t("workflow.weight")}</dt>
        <dd>{formatPercent(holding.portfolio_weight)}</dd>
      </div>
    </dl>
  );
}

function formatNumber(value: number) {
  return new Intl.NumberFormat(undefined, {
    maximumFractionDigits: 2,
  }).format(value);
}

function formatCurrency(value: number, currency: string) {
  return new Intl.NumberFormat(undefined, {
    style: "currency",
    currency,
    maximumFractionDigits: 2,
  }).format(value);
}

function formatPercent(value: number) {
  return new Intl.NumberFormat(undefined, {
    style: "percent",
    maximumFractionDigits: 2,
  }).format(value);
}
