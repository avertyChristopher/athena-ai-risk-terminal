from sqlalchemy.orm import Session


class TradeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def simulation_available(self) -> bool:
        return False
