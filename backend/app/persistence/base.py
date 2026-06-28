"""Compatibility re-export for the shared SQLAlchemy declarative base."""

from app.database.base import Base

__all__ = ["Base"]
