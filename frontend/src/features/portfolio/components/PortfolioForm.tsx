import { FormEvent, useState } from "react";

import { PortfolioCreate } from "../../../types/portfolio";
import { BenchmarkSelector } from "./BenchmarkSelector";

type PortfolioFormProps = {
  onCreate: (payload: PortfolioCreate) => void;
  labels: {
    title: string;
    name: string;
    currency: string;
    benchmark: string;
    cash: string;
    create: string;
  };
};

const currencies = ["USD", "CAD", "EUR", "GBP"];

export function PortfolioForm({ onCreate, labels }: PortfolioFormProps) {
  const [name, setName] = useState("");
  const [baseCurrency, setBaseCurrency] = useState("USD");
  const [benchmark, setBenchmark] = useState("SPY");
  const [cash, setCash] = useState(0);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onCreate({
      name,
      base_currency: baseCurrency,
      benchmark,
      cash,
    });
    setName("");
    setCash(0);
  }

  return (
    <form className="card portfolio-form" onSubmit={handleSubmit}>
      <h2>{labels.title}</h2>
      <div className="form-grid">
        <label className="form-field">
          <span>{labels.name}</span>
          <input
            required
            value={name}
            onChange={(event) => setName(event.target.value)}
          />
        </label>
        <label className="form-field">
          <span>{labels.currency}</span>
          <select
            value={baseCurrency}
            onChange={(event) => setBaseCurrency(event.target.value)}
          >
            {currencies.map((currency) => (
              <option key={currency} value={currency}>
                {currency}
              </option>
            ))}
          </select>
        </label>
        <BenchmarkSelector
          value={benchmark}
          onChange={setBenchmark}
          label={labels.benchmark}
        />
        <label className="form-field">
          <span>{labels.cash}</span>
          <input
            min="0"
            step="100"
            type="number"
            value={cash}
            onChange={(event) => setCash(Number(event.target.value))}
          />
        </label>
      </div>
      <button className="button button--primary" type="submit">
        {labels.create}
      </button>
    </form>
  );
}
