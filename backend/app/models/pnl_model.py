from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class PnlModel(Base):
    __tablename__ = "pnl_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolios.id"), index=True)
    total_pnl: Mapped[float] = mapped_column(Numeric(18, 6), default=0)
    as_of: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
