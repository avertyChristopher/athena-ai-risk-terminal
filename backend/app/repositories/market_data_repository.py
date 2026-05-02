from sqlalchemy.orm import Session


class MarketDataRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_supported_symbols(self) -> list[str]:
        return []
