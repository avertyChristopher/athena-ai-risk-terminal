from fastapi import HTTPException

from app.domain.portfolios import (
    calculate_portfolio_weights,
    calculate_position_market_value,
)
from app.repositories.portfolio_repository import PortfolioRepository
from app.repositories.position_repository import PositionRepository
from app.schemas.portfolio_schema import DeleteResponse
from app.schemas.position_schema import (
    PositionCreate,
    PositionListResponse,
    PositionRead,
    PositionUpdate,
)


class PositionService:
    def __init__(
        self,
        repository: PositionRepository,
        portfolio_repository: PortfolioRepository,
    ) -> None:
        self.repository = repository
        self.portfolio_repository = portfolio_repository

    def list_positions(self, portfolio_id: str) -> PositionListResponse:
        self._get_portfolio_or_404(portfolio_id)
        return PositionListResponse(
            portfolio_id=portfolio_id,
            items=self._decorated_positions(portfolio_id),
        )

    def create_position(
        self,
        portfolio_id: str,
        payload: PositionCreate,
    ) -> PositionRead:
        self._get_portfolio_or_404(portfolio_id)
        created_position = self.repository.create_position(
            portfolio_id,
            payload.model_dump(),
        )
        positions = self._decorated_positions(portfolio_id)
        return next(
            position
            for position in positions
            if position.id == created_position["id"]
        )

    def update_position(
        self,
        portfolio_id: str,
        position_id: str,
        payload: PositionUpdate,
    ) -> PositionRead:
        self._get_portfolio_or_404(portfolio_id)
        position = self.repository.update_position(
            portfolio_id,
            position_id,
            payload.model_dump(exclude_none=True),
        )
        if position is None:
            raise HTTPException(status_code=404, detail="Position not found.")

        positions = self._decorated_positions(portfolio_id)
        return next(position for position in positions if position.id == position_id)

    def delete_position(self, portfolio_id: str, position_id: str) -> DeleteResponse:
        self._get_portfolio_or_404(portfolio_id)
        deleted = self.repository.delete_position(portfolio_id, position_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Position not found.")

        return DeleteResponse(status="deleted", id=position_id)

    def _get_portfolio_or_404(self, portfolio_id: str) -> dict[str, object]:
        portfolio = self.portfolio_repository.get_portfolio(portfolio_id)
        if portfolio is None:
            raise HTTPException(status_code=404, detail="Portfolio not found.")

        return portfolio

    def _decorated_positions(self, portfolio_id: str) -> list[PositionRead]:
        portfolio = self._get_portfolio_or_404(portfolio_id)
        positions = self.repository.list_positions(portfolio_id)
        market_values = [
            calculate_position_market_value(
                float(position["quantity"]),
                float(position["current_price"]),
            )
            for position in positions
        ]
        weights = calculate_portfolio_weights(market_values, float(portfolio["cash"]))

        return [
            PositionRead.model_validate(
                {**position, "market_value": market_value, "weight": weight},
            )
            for position, market_value, weight in zip(positions, market_values, weights)
        ]
