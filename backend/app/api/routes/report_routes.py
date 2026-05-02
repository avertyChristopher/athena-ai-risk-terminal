from fastapi import APIRouter, Depends

from app.api.dependencies import get_report_service
from app.schemas.report_schema import ReportModuleStatus
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/status", response_model=ReportModuleStatus)
def get_report_status(
    service: ReportService = Depends(get_report_service),
) -> ReportModuleStatus:
    return service.get_module_status()
