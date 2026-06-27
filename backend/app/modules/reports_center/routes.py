from fastapi import APIRouter, Depends

from app.api.dependencies import get_reports_center_service
from app.modules.reports_center.schemas import (
    CsvExportResponse,
    GeneratedReport,
    MarkdownExportResponse,
    ReportDeleteResponse,
    ReportGenerateRequest,
    ReportLibraryResponse,
    ReportTemplateListResponse,
    ReportsCenterStatus,
)
from app.modules.reports_center.service import ReportsCenterService


router = APIRouter(prefix="/reports-center", tags=["reports-center"])


@router.get("/status", response_model=ReportsCenterStatus)
def get_reports_center_status(
    service: ReportsCenterService = Depends(get_reports_center_service),
) -> ReportsCenterStatus:
    return service.get_status()


@router.get("/templates", response_model=ReportTemplateListResponse)
def list_report_templates(
    service: ReportsCenterService = Depends(get_reports_center_service),
) -> ReportTemplateListResponse:
    return service.list_templates()


@router.post("/generate", response_model=GeneratedReport)
def generate_report(
    payload: ReportGenerateRequest,
    service: ReportsCenterService = Depends(get_reports_center_service),
) -> GeneratedReport:
    return service.generate_report(payload)


@router.get("/reports", response_model=ReportLibraryResponse)
def list_reports(
    service: ReportsCenterService = Depends(get_reports_center_service),
) -> ReportLibraryResponse:
    return service.list_reports()


@router.get("/reports/{report_id}", response_model=GeneratedReport)
def get_report(
    report_id: str,
    service: ReportsCenterService = Depends(get_reports_center_service),
) -> GeneratedReport:
    return service.get_report(report_id)


@router.delete("/reports/{report_id}", response_model=ReportDeleteResponse)
def delete_report(
    report_id: str,
    service: ReportsCenterService = Depends(get_reports_center_service),
) -> ReportDeleteResponse:
    return service.delete_report(report_id)


@router.get("/reports/{report_id}/export/json")
def export_report_json(
    report_id: str,
    service: ReportsCenterService = Depends(get_reports_center_service),
) -> dict:
    return service.export_json(report_id)


@router.get("/reports/{report_id}/export/markdown", response_model=MarkdownExportResponse)
def export_report_markdown(
    report_id: str,
    service: ReportsCenterService = Depends(get_reports_center_service),
) -> MarkdownExportResponse:
    return service.export_markdown(report_id)


@router.get("/reports/{report_id}/export/csv", response_model=CsvExportResponse)
def export_report_csv(
    report_id: str,
    service: ReportsCenterService = Depends(get_reports_center_service),
) -> CsvExportResponse:
    return service.export_csv(report_id)


@router.get("/demo", response_model=GeneratedReport)
def get_reports_center_demo(
    service: ReportsCenterService = Depends(get_reports_center_service),
) -> GeneratedReport:
    return service.demo()
