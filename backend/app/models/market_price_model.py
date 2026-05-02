from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class MarketPriceModel(Base):
    __tablename__ = "market_prices"

    id: Mapped[int] = mapped_column(primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), index=True)
    price: Mapped[float] = mapped_column(Numeric(18, 6))
    as_of: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
