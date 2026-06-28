from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


ReportType = Literal[
    "portfolio_overview",
    "risk_monitor",
    "stress_testing",
    "limit_breach",
    "trade_suitability",
    "fixed_income_exposure",
    "options_risk",
    "pnl_attribution",
    "reconciliation",
    "ai_anomaly",
    "full_portfolio_risk_pack",
]
ReportLanguage = Literal["en", "fr"]
ReportStyle = Literal["professional", "executive", "educational"]
ReportStatusValue = Literal["generated", "generated_with_warnings"]


class ReportsCenterStatus(BaseModel):
    status: str = "ready"
    module: str = "reports-center"
    detail: str
    templates_available: int
    export_formats: list[str]
    source_modules: list[str]
    snapshot_based: bool = True
    pdf_roadmap_note: str


class ReportTemplate(BaseModel):
    report_type: ReportType
    name: str
    purpose: str
    sections: list[str]
    source_modules: list[str]
    export_formats: list[str]
    pdf_roadmap_note: str


class ReportTemplateListResponse(BaseModel):
    status: str = "ready"
    module: str = "reports-center"
    templates: list[ReportTemplate]


class ReportGenerateRequest(BaseModel):
    report_type: ReportType
    portfolio_id: str | None = Field(default="pf_001", min_length=1)
    language: ReportLanguage = "en"
    include_athena_commentary: bool = True
    include_methodology: bool = True
    include_limitations: bool = True
    source_payloads: dict[str, Any] = Field(default_factory=dict)
    style: ReportStyle = "professional"


class ReportSection(BaseModel):
    section_id: str
    title: str
    status: str = "available"
    summary: str
    source_modules: list[str] = Field(default_factory=list)
    metrics: dict[str, Any] = Field(default_factory=dict)
    table: list[dict[str, Any]] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class ReportSnapshot(BaseModel):
    snapshot_id: str
    report_id: str
    portfolio_id: str | None
    portfolio_name: str | None
    report_type: ReportType
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    source_modules: list[str] = Field(default_factory=list)
    data_sources: list[str] = Field(default_factory=list)
    payloads_used: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    generated_by: str = "reports_center"
    language: ReportLanguage = "en"


class GeneratedReport(BaseModel):
    report_id: str
    report_type: ReportType
    title: str
    portfolio_id: str | None
    portfolio_name: str | None
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    language: ReportLanguage
    style: ReportStyle
    status: ReportStatusValue
    executive_summary: str
    sections: list[ReportSection]
    snapshot: ReportSnapshot
    athena_commentary: dict[str, Any] | None = None
    assumptions: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    export_formats: list[str] = Field(default_factory=lambda: ["json", "markdown", "csv"])
    pdf_roadmap_note: str = "PDF export prepared but not enabled in this lightweight demo build."
    disclaimer: str = (
        "This report is generated for educational and analytical purposes "
        "and is not investment advice."
    )


class ReportListItem(BaseModel):
    report_id: str
    report_type: ReportType
    title: str
    portfolio_id: str | None
    portfolio_name: str | None
    generated_at: datetime
    language: ReportLanguage
    status: ReportStatusValue
    warnings_count: int
    source_modules: list[str]


class ReportLibraryResponse(BaseModel):
    status: str = "ready"
    module: str = "reports-center"
    total_reports: int
    items: list[ReportListItem]


class ReportDeleteResponse(BaseModel):
    deleted: bool
    report_id: str


class MarkdownExportResponse(BaseModel):
    report_id: str
    content_type: str = "text/markdown"
    markdown: str


class CsvExportResponse(BaseModel):
    report_id: str
    content_type: str = "text/csv"
    csv: str
    included_tables: list[str]
