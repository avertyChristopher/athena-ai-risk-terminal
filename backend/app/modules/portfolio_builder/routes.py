from fastapi import APIRouter, Depends

from app.api.dependencies import get_portfolio_service, get_position_service
from app.modules.portfolio_builder.schemas import (
    AllocationResponse,
    CfaConceptsResponse,
    ConcentrationResponse,
    ConstraintsResponse,
    DeleteResponse,
    DiversificationResponse,
    BenchmarkResponse,
    PerformanceMeasurementResponse,
    PolicyResponse,
    PortfolioCreate,
    PortfolioConstraints,
    PortfolioDiagnosticsResponse,
    PortfolioListResponse,
    PortfolioPolicy,
    PortfolioRead,
    PortfolioSummary,
    PortfolioUpdate,
    PositionCreate,
    PositionListResponse,
    PositionRead,
    PositionUpdate,
    RebalancingPreviewResponse,
    RiskReturnResponse,
    TargetAllocation,
    TargetAllocationResponse,
)
from app.modules.portfolio_builder.service import PortfolioService, PositionService

router = APIRouter(prefix="/portfolios", tags=["portfolios"])


@router.get("", response_model=PortfolioListResponse)
def list_portfolios(
    service: PortfolioService = Depends(get_portfolio_service),
) -> PortfolioListResponse:
    return service.list_portfolios()


@router.post("", response_model=PortfolioRead, status_code=201)
def create_portfolio(
    payload: PortfolioCreate,
    service: PortfolioService = Depends(get_portfolio_service),
) -> PortfolioRead:
    return service.create_portfolio(payload)


@router.get("/{portfolio_id}", response_model=PortfolioRead)
def get_portfolio(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> PortfolioRead:
    return service.get_portfolio(portfolio_id)


@router.put("/{portfolio_id}", response_model=PortfolioRead)
def update_portfolio(
    portfolio_id: str,
    payload: PortfolioUpdate,
    service: PortfolioService = Depends(get_portfolio_service),
) -> PortfolioRead:
    return service.update_portfolio(portfolio_id, payload)


@router.delete("/{portfolio_id}", response_model=DeleteResponse)
def delete_portfolio(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> DeleteResponse:
    return service.delete_portfolio(portfolio_id)


@router.get("/{portfolio_id}/summary", response_model=PortfolioSummary)
def get_portfolio_summary(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> PortfolioSummary:
    return service.get_summary(portfolio_id)


@router.get("/{portfolio_id}/positions", response_model=PositionListResponse)
def list_positions(
    portfolio_id: str,
    service: PositionService = Depends(get_position_service),
) -> PositionListResponse:
    return service.list_positions(portfolio_id)


@router.post("/{portfolio_id}/positions", response_model=PositionRead, status_code=201)
def create_position(
    portfolio_id: str,
    payload: PositionCreate,
    service: PositionService = Depends(get_position_service),
) -> PositionRead:
    return service.create_position(portfolio_id, payload)


@router.put("/{portfolio_id}/positions/{position_id}", response_model=PositionRead)
def update_position(
    portfolio_id: str,
    position_id: str,
    payload: PositionUpdate,
    service: PositionService = Depends(get_position_service),
) -> PositionRead:
    return service.update_position(portfolio_id, position_id, payload)


@router.delete("/{portfolio_id}/positions/{position_id}", response_model=DeleteResponse)
def delete_position(
    portfolio_id: str,
    position_id: str,
    service: PositionService = Depends(get_position_service),
) -> DeleteResponse:
    return service.delete_position(portfolio_id, position_id)


@router.get("/{portfolio_id}/allocation/assets", response_model=AllocationResponse)
def get_asset_allocation(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> AllocationResponse:
    return service.get_allocation(portfolio_id, "assets")


@router.get("/{portfolio_id}/allocation/sectors", response_model=AllocationResponse)
def get_sector_allocation(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> AllocationResponse:
    return service.get_allocation(portfolio_id, "sectors")


@router.get("/{portfolio_id}/allocation/currencies", response_model=AllocationResponse)
def get_currency_allocation(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> AllocationResponse:
    return service.get_allocation(portfolio_id, "currencies")


@router.get("/{portfolio_id}/allocation/countries", response_model=AllocationResponse)
def get_country_allocation(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> AllocationResponse:
    return service.get_allocation(portfolio_id, "countries")


@router.get("/{portfolio_id}/allocation/asset-types", response_model=AllocationResponse)
def get_asset_type_allocation(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> AllocationResponse:
    return service.get_allocation(portfolio_id, "asset-types")


@router.get("/{portfolio_id}/concentration", response_model=ConcentrationResponse)
def get_concentration(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> ConcentrationResponse:
    return service.get_concentration(portfolio_id)


@router.get("/{portfolio_id}/diversification", response_model=DiversificationResponse)
def get_diversification(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> DiversificationResponse:
    return service.get_diversification(portfolio_id)


@router.get("/{portfolio_id}/risk-return", response_model=RiskReturnResponse)
def get_risk_return(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> RiskReturnResponse:
    return service.get_risk_return(portfolio_id)


@router.get("/{portfolio_id}/benchmark", response_model=BenchmarkResponse)
def get_benchmark(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> BenchmarkResponse:
    return service.get_benchmark(portfolio_id)


@router.get("/{portfolio_id}/policy", response_model=PolicyResponse)
def get_policy(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> PolicyResponse:
    return service.get_policy(portfolio_id)


@router.put("/{portfolio_id}/policy", response_model=PolicyResponse)
def update_policy(
    portfolio_id: str,
    payload: PortfolioPolicy,
    service: PortfolioService = Depends(get_portfolio_service),
) -> PolicyResponse:
    return service.update_policy(portfolio_id, payload)


@router.get("/{portfolio_id}/target-allocation", response_model=TargetAllocationResponse)
def get_target_allocation(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> TargetAllocationResponse:
    return service.get_target_allocation(portfolio_id)


@router.put("/{portfolio_id}/target-allocation", response_model=TargetAllocationResponse)
def update_target_allocation(
    portfolio_id: str,
    payload: list[TargetAllocation],
    service: PortfolioService = Depends(get_portfolio_service),
) -> TargetAllocationResponse:
    return service.update_target_allocation(portfolio_id, payload)


@router.get(
    "/{portfolio_id}/rebalancing-preview",
    response_model=RebalancingPreviewResponse,
)
def get_rebalancing_preview(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> RebalancingPreviewResponse:
    return service.get_rebalancing_preview(portfolio_id)


@router.get(
    "/{portfolio_id}/performance-measurement",
    response_model=PerformanceMeasurementResponse,
)
def get_performance_measurement(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> PerformanceMeasurementResponse:
    return service.get_performance_measurement(portfolio_id)


@router.get("/{portfolio_id}/constraints", response_model=ConstraintsResponse)
def get_constraints(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> ConstraintsResponse:
    return service.get_constraints(portfolio_id)


@router.put("/{portfolio_id}/constraints", response_model=ConstraintsResponse)
def update_constraints(
    portfolio_id: str,
    payload: PortfolioConstraints,
    service: PortfolioService = Depends(get_portfolio_service),
) -> ConstraintsResponse:
    return service.update_constraints(portfolio_id, payload)


@router.get("/{portfolio_id}/diagnostics", response_model=PortfolioDiagnosticsResponse)
def get_diagnostics(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> PortfolioDiagnosticsResponse:
    return service.get_diagnostics(portfolio_id)


@router.get("/{portfolio_id}/cfa-concepts", response_model=CfaConceptsResponse)
def get_cfa_concepts(
    portfolio_id: str,
    service: PortfolioService = Depends(get_portfolio_service),
) -> CfaConceptsResponse:
    return service.get_cfa_concepts(portfolio_id)
