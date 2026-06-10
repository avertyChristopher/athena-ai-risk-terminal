from fastapi import HTTPException

from app.modules.portfolio_builder.domain import (
    calculate_allocation_by_asset,
    calculate_allocation_by_asset_type,
    calculate_allocation_by_country,
    calculate_allocation_by_currency,
    calculate_allocation_by_sector,
    calculate_cash_weight,
    calculate_concentration_metrics,
    calculate_portfolio_market_value,
    calculate_portfolio_weights,
    calculate_position_market_value,
)
from app.modules.portfolio_builder.repository import (
    PortfolioRepository,
    PositionRepository,
)
from app.modules.portfolio_builder.schemas import (
    AllocationResponse,
    ConcentrationResponse,
    DeleteResponse,
    PortfolioCreate,
    PortfolioListResponse,
    PortfolioRead,
    PortfolioSummary,
    PortfolioUpdate,
    PositionCreate,
    PositionListResponse,
    PositionRead,
    PositionUpdate,
)


class PortfolioService:
    def __init__(
        self,
        repository: PortfolioRepository,
        position_repository: PositionRepository,
    ) -> None:
        self.repository = repository
        self.position_repository = position_repository

    def list_portfolios(self) -> PortfolioListResponse:
        return PortfolioListResponse(
            detail="Demo portfolios are available for builder workflows.",
            items=[
                PortfolioRead.model_validate(portfolio)
                for portfolio in self.repository.list_portfolios()
            ],
        )

    def get_portfolio(self, portfolio_id: str) -> PortfolioRead:
        return PortfolioRead.model_validate(self._get_portfolio_or_404(portfolio_id))

    def create_portfolio(self, payload: PortfolioCreate) -> PortfolioRead:
        portfolio = self.repository.create_portfolio(payload.model_dump())
        return PortfolioRead.model_validate(portfolio)

    def update_portfolio(
        self,
        portfolio_id: str,
        payload: PortfolioUpdate,
    ) -> PortfolioRead:
        self._get_portfolio_or_404(portfolio_id)
        portfolio = self.repository.update_portfolio(
            portfolio_id,
            payload.model_dump(exclude_none=True),
        )
        if portfolio is None:
            raise HTTPException(status_code=404, detail="Portfolio not found.")

        return PortfolioRead.model_validate(portfolio)

    def delete_portfolio(self, portfolio_id: str) -> DeleteResponse:
        self._get_portfolio_or_404(portfolio_id)
        self.repository.delete_portfolio(portfolio_id)
        return DeleteResponse(status="deleted", id=portfolio_id)

    def get_summary(self, portfolio_id: str) -> PortfolioSummary:
        portfolio = self._get_portfolio_or_404(portfolio_id)
        positions = self._decorated_positions(portfolio_id)
        market_values = [float(position["market_value"]) for position in positions]
        cash = float(portfolio["cash"])
        concentration = calculate_concentration_metrics(positions)

        return PortfolioSummary(
            portfolio_id=portfolio_id,
            name=str(portfolio["name"]),
            base_currency=str(portfolio["base_currency"]),
            total_value=calculate_portfolio_market_value(market_values, cash),
            number_of_positions=len(positions),
            benchmark=str(portfolio["benchmark"]),
            cash=cash,
            cash_weight=calculate_cash_weight(market_values, cash),
            largest_position_weight=float(concentration["largest_position_weight"]),
            top_5_holdings_weight=float(concentration["top_5_holdings_weight"]),
        )

    def get_allocation(
        self,
        portfolio_id: str,
        allocation_type: str,
    ) -> AllocationResponse:
        self._get_portfolio_or_404(portfolio_id)
        positions = self._decorated_positions(portfolio_id)
        calculators = {
            "assets": calculate_allocation_by_asset,
            "sectors": calculate_allocation_by_sector,
            "currencies": calculate_allocation_by_currency,
            "countries": calculate_allocation_by_country,
            "asset-types": calculate_allocation_by_asset_type,
        }
        calculator = calculators[allocation_type]

        return AllocationResponse(
            portfolio_id=portfolio_id,
            allocation_type=allocation_type,
            items=calculator(positions),
        )

    def get_concentration(self, portfolio_id: str) -> ConcentrationResponse:
        self._get_portfolio_or_404(portfolio_id)
        metrics = calculate_concentration_metrics(
            self._decorated_positions(portfolio_id),
        )

        return ConcentrationResponse(portfolio_id=portfolio_id, **metrics)

    def _get_portfolio_or_404(self, portfolio_id: str) -> dict[str, object]:
        portfolio = self.repository.get_portfolio(portfolio_id)
        if portfolio is None:
            raise HTTPException(status_code=404, detail="Portfolio not found.")

        return portfolio

    def _decorated_positions(self, portfolio_id: str) -> list[dict[str, object]]:
        portfolio = self._get_portfolio_or_404(portfolio_id)
        positions = self.position_repository.list_positions(portfolio_id)
        market_values = [
            calculate_position_market_value(
                float(position["quantity"]),
                float(position["current_price"]),
            )
            for position in positions
        ]
        weights = calculate_portfolio_weights(market_values, float(portfolio["cash"]))

        return [
            {**position, "market_value": market_value, "weight": weight}
            for position, market_value, weight in zip(positions, market_values, weights)
        ]


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
