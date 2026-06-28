from __future__ import annotations

import logging

from sqlalchemy.exc import SQLAlchemyError

from app.database.base import Base
from app.database.session import engine

# Import modules so every SQLAlchemy model is registered before create_all.
from app.models import asset_model as _asset_model  # noqa: F401
from app.models import market_price_model as _market_price_model  # noqa: F401
from app.models import pnl_model as _pnl_model  # noqa: F401
from app.models import portfolio_model as _portfolio_model  # noqa: F401
from app.models import position_model as _position_model  # noqa: F401
from app.models import report_model as _report_model  # noqa: F401
from app.models import risk_metric_model as _risk_metric_model  # noqa: F401
from app.models import trade_model as _trade_model  # noqa: F401
from app.persistence import models as _workflow_models  # noqa: F401

logger = logging.getLogger(__name__)


def init_db() -> bool:
    try:
        Base.metadata.create_all(bind=engine)
        return True
    except SQLAlchemyError as exc:
        logger.warning("Athena persistence initialization failed: %s", exc)
        return False

