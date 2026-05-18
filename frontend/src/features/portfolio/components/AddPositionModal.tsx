import { FormEvent, useState } from "react";

import { PositionCreate } from "../../../types/portfolio";

type AddPositionModalProps = {
  isOpen: boolean;
  onClose: () => void;
  onCreate: (payload: PositionCreate) => void;
  labels: {
    title: string;
    symbol: string;
    name: string;
    type: string;
    quantity: string;
    averagePrice: string;
    currentPrice: string;
    currency: string;
    sector: string;
    country: string;
    cancel: string;
    add: string;
  };
};

export function AddPositionModal({
  isOpen,
  onClose,
  onCreate,
  labels,
}: AddPositionModalProps) {
  const [form, setForm] = useState<PositionCreate>({
    symbol: "AAPL",
    asset_name: "Apple Inc.",
    asset_type: "equity",
    quantity: 10,
    average_price: 180,
    current_price: 200,
    currency: "USD",
    sector: "Technology",
    country: "United States",
  });

  if (!isOpen) {
    return null;
  }

  function setField<K extends keyof PositionCreate>(
    key: K,
    value: PositionCreate[K],
  ) {
    setForm((current) => ({ ...current, [key]: value }));
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onCreate(form);
    onClose();
  }

  return (
    <div className="modal-backdrop" role="presentation">
      <form className="modal" onSubmit={handleSubmit}>
        <div className="section-heading">
          <h2>{labels.title}</h2>
          <button className="button button--ghost" type="button" onClick={onClose}>
            {labels.cancel}
          </button>
        </div>
        <div className="form-grid">
          <label className="form-field">
            <span>{labels.symbol}</span>
            <input
              required
              value={form.symbol}
              onChange={(event) => setField("symbol", event.target.value)}
            />
          </label>
          <label className="form-field">
            <span>{labels.name}</span>
            <input
              required
              value={form.asset_name}
              onChange={(event) => setField("asset_name", event.target.value)}
            />
          </label>
          <label className="form-field">
            <span>{labels.type}</span>
            <input
              required
              value={form.asset_type}
              onChange={(event) => setField("asset_type", event.target.value)}
            />
          </label>
          <label className="form-field">
            <span>{labels.quantity}</span>
            <input
              min="0"
              required
              step="1"
              type="number"
              value={form.quantity}
              onChange={(event) => setField("quantity", Number(event.target.value))}
            />
          </label>
          <label className="form-field">
            <span>{labels.averagePrice}</span>
            <input
              min="0"
              required
              step="0.01"
              type="number"
              value={form.average_price}
              onChange={(event) =>
                setField("average_price", Number(event.target.value))
              }
            />
          </label>
          <label className="form-field">
            <span>{labels.currentPrice}</span>
            <input
              min="0"
              required
              step="0.01"
              type="number"
              value={form.current_price}
              onChange={(event) =>
                setField("current_price", Number(event.target.value))
              }
            />
          </label>
          <label className="form-field">
            <span>{labels.currency}</span>
            <input
              required
              value={form.currency}
              onChange={(event) => setField("currency", event.target.value)}
            />
          </label>
          <label className="form-field">
            <span>{labels.sector}</span>
            <input
              required
              value={form.sector}
              onChange={(event) => setField("sector", event.target.value)}
            />
          </label>
          <label className="form-field">
            <span>{labels.country}</span>
            <input
              required
              value={form.country}
              onChange={(event) => setField("country", event.target.value)}
            />
          </label>
        </div>
        <button className="button button--primary" type="submit">
          {labels.add}
        </button>
      </form>
    </div>
  );
}
