import { FormEvent, useEffect, useMemo, useState } from "react";

import { apiClient } from "../../../lib/api-client";
import { endpoints } from "../../../lib/endpoints";
import { formatCurrency, formatPercent } from "../../../lib/formatters";
import {
  EquityValuationResponse,
  GgmValuationResponse,
  SensitivityResponse,
} from "../../../types/equity";

type GGMCalculatorProps = {
  valuation?: EquityValuationResponse;
  labels: {
    title: string;
    dividend: string;
    requiredReturn: string;
    growth: string;
    calculate: string;
    intrinsicValue: string;
    spread: string;
    sensitivity: string;
    invalid: string;
  };
};

export function GGMCalculator({ valuation, labels }: GGMCalculatorProps) {
  const [dividend, setDividend] = useState(0);
  const [requiredReturn, setRequiredReturn] = useState(0);
  const [growth, setGrowth] = useState(0);
  const [result, setResult] = useState<GgmValuationResponse | null>(null);
  const [sensitivity, setSensitivity] = useState<SensitivityResponse | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!valuation) {
      return;
    }

    setDividend(Number(valuation.dividend_next_year.toFixed(4)));
    setRequiredReturn(Number(valuation.required_return.toFixed(4)));
    setGrowth(Number(valuation.growth_rate.toFixed(4)));
    setResult({
      intrinsic_value: valuation.gordon_growth_value,
      spread: valuation.required_return - valuation.growth_rate,
    });
    setSensitivity(null);
    setError("");
  }, [valuation]);

  const growthRates = useMemo(
    () => [growth - 0.01, growth, growth + 0.01].map((value) => Number(value.toFixed(4))),
    [growth],
  );
  const requiredReturns = useMemo(
    () =>
      [requiredReturn - 0.01, requiredReturn, requiredReturn + 0.01].map((value) =>
        Number(value.toFixed(4)),
      ),
    [requiredReturn],
  );

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");

    try {
      const nextResult = await apiClient.post<GgmValuationResponse>(
        endpoints.equityGgm,
        {
          dividend_next_year: dividend,
          required_return: requiredReturn,
          growth_rate: growth,
        },
      );
      const nextSensitivity = await apiClient.post<SensitivityResponse>(
        endpoints.equitySensitivity,
        {
          dividend_next_year: dividend,
          required_returns: requiredReturns,
          growth_rates: growthRates,
        },
      );

      setResult(nextResult);
      setSensitivity(nextSensitivity);
    } catch {
      setResult(null);
      setSensitivity(null);
      setError(labels.invalid);
    }
  }

  return (
    <section className="card equity-card ggm-calculator">
      <h3>{labels.title}</h3>
      <form className="equity-calculator-grid" onSubmit={handleSubmit}>
        <label className="form-field">
          <span>{labels.dividend}</span>
          <input
            min="0"
            step="0.01"
            type="number"
            value={dividend}
            onChange={(event) => setDividend(Number(event.target.value))}
          />
        </label>
        <label className="form-field">
          <span>{labels.requiredReturn}</span>
          <input
            step="0.001"
            type="number"
            value={requiredReturn}
            onChange={(event) => setRequiredReturn(Number(event.target.value))}
          />
        </label>
        <label className="form-field">
          <span>{labels.growth}</span>
          <input
            step="0.001"
            type="number"
            value={growth}
            onChange={(event) => setGrowth(Number(event.target.value))}
          />
        </label>
        <button className="button button--primary" type="submit">
          {labels.calculate}
        </button>
      </form>

      {error ? <p className="status-message status-message--error">{error}</p> : null}

      <div className="metric-grid">
        <div className="metric-tile">
          <span>{labels.intrinsicValue}</span>
          <strong>{result ? formatCurrency(result.intrinsic_value) : "--"}</strong>
        </div>
        <div className="metric-tile">
          <span>{labels.spread}</span>
          <strong>{result ? formatPercent(result.spread) : "--"}</strong>
        </div>
      </div>

      <div className="compact-table-card">
        <h4>{labels.sensitivity}</h4>
        <table className="compact-table">
          <thead>
            <tr>
              <th>{labels.requiredReturn}</th>
              {growthRates.map((growthRate) => (
                <th key={growthRate}>{formatPercent(growthRate)}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {requiredReturns.map((requiredReturnValue) => (
              <tr key={requiredReturnValue}>
                <td>{formatPercent(requiredReturnValue)}</td>
                {growthRates.map((growthRate) => {
                  const cell = sensitivity?.cells.find(
                    (item) =>
                      item.required_return === requiredReturnValue &&
                      item.growth_rate === growthRate,
                  );
                  return (
                    <td key={growthRate}>
                      {cell?.intrinsic_value
                        ? formatCurrency(cell.intrinsic_value)
                        : "--"}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
