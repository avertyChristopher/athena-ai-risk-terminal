import { FormEvent, useEffect, useMemo, useState } from "react";

import {
  PositionCreate,
  PositionRead,
  PositionUpdate,
} from "../../../types/portfolio";

type AddPositionModalProps = {
  isOpen: boolean;
  onClose: () => void;
  onCreate: (payload: PositionCreate) => void;
  onUpdate?: (positionId: string, payload: PositionUpdate) => void;
  position?: PositionRead | null;
  labels: {
    title: string;
    editTitle?: string;
    symbol: string;
    name: string;
    displayName?: string;
    type: string;
    quantity: string;
    averagePrice: string;
    currentPrice: string;
    currency: string;
    sector: string;
    country: string;
    exchange?: string;
    industry?: string;
    region?: string;
    cancel: string;
    add: string;
    update?: string;
  };
};

type PositionForm = PositionCreate & {
  exchange: string;
  industry: string;
  region: string;
};

const defaultPositionForm: PositionForm = {
  symbol: "AAPL",
  asset_name: "Apple Inc.",
  name: "",
  asset_type: "equity",
  quantity: 10,
  average_price: 180,
  current_price: 200,
  currency: "USD",
  sector: "Technology",
  country: "United States",
  exchange: "NASDAQ",
  industry: "Consumer Electronics",
  region: "North America",
};

export function AddPositionModal({
  isOpen,
  onClose,
  onCreate,
  onUpdate,
  position,
  labels,
}: AddPositionModalProps) {
  const isEditing = Boolean(position);
  const initialForm = useMemo(
    () => (position ? toPositionForm(position) : defaultPositionForm),
    [position],
  );
  const [form, setForm] = useState<PositionForm>(initialForm);

  useEffect(() => {
    if (isOpen) {
      setForm(initialForm);
    }
  }, [initialForm, isOpen]);

  if (!isOpen) {
    return null;
  }

  function setField<K extends keyof PositionForm>(
    key: K,
    value: PositionForm[K],
  ) {
    setForm((current) => ({ ...current, [key]: value }));
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const payload = toPayload(form);

    if (position && onUpdate) {
      onUpdate(position.id, payload);
      onClose();
      return;
    }

    onCreate(payload as PositionCreate);
    onClose();
  }

  return (
    <div className="modal-backdrop" role="presentation">
      <form className="modal" onSubmit={handleSubmit}>
        <div className="section-heading">
          <h2>{isEditing ? labels.editTitle ?? labels.title : labels.title}</h2>
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
            <span>{labels.displayName ?? "Display name"}</span>
            <input
              value={form.name ?? ""}
              onChange={(event) => setField("name", event.target.value)}
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
              min="0.01"
              required
              step="0.01"
              type="number"
              value={form.quantity}
              onChange={(event) => setField("quantity", Number(event.target.value))}
            />
          </label>
          <label className="form-field">
            <span>{labels.averagePrice}</span>
            <input
              min="0.01"
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
              min="0.01"
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
          <label className="form-field">
            <span>{labels.exchange ?? "Exchange"}</span>
            <input
              value={form.exchange}
              onChange={(event) => setField("exchange", event.target.value)}
            />
          </label>
          <label className="form-field">
            <span>{labels.industry ?? "Industry"}</span>
            <input
              value={form.industry}
              onChange={(event) => setField("industry", event.target.value)}
            />
          </label>
          <label className="form-field">
            <span>{labels.region ?? "Region"}</span>
            <input
              value={form.region}
              onChange={(event) => setField("region", event.target.value)}
            />
          </label>
        </div>
        <button className="button button--primary" type="submit">
          {isEditing ? labels.update ?? labels.add : labels.add}
        </button>
      </form>
    </div>
  );
}

function toPositionForm(position: PositionRead): PositionForm {
  return {
    symbol: position.symbol,
    asset_name: position.asset_name,
    name: position.name ?? "",
    asset_type: position.asset_type,
    quantity: position.quantity,
    average_price: position.average_price,
    current_price: position.current_price,
    currency: position.currency,
    sector: position.sector,
    country: position.country,
    exchange: position.exchange ?? "",
    industry: position.industry ?? "",
    region: position.region ?? "",
  };
}

function toPayload(form: PositionForm): PositionUpdate {
  return {
    symbol: form.symbol.trim().toUpperCase(),
    asset_name: form.asset_name.trim(),
    name: optionalText(form.name),
    asset_type: form.asset_type.trim(),
    quantity: form.quantity,
    average_price: form.average_price,
    current_price: form.current_price,
    currency: form.currency.trim().toUpperCase(),
    sector: form.sector.trim(),
    country: form.country.trim(),
    exchange: optionalText(form.exchange),
    industry: optionalText(form.industry),
    region: optionalText(form.region),
  };
}

function optionalText(value: string | null | undefined) {
  const trimmedValue = value?.trim();
  return trimmedValue ? trimmedValue : undefined;
}
