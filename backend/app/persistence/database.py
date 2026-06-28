"""Shared persistence database handles.

The project already owns the real engine/session in app.database; this module
keeps the persistence package discoverable without creating a second engine.
"""

from app.database.session import SessionLocal, engine, get_db

__all__ = ["SessionLocal", "engine", "get_db"]
