from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse

from app.middleware.auth import get_current_user_id
from app.middleware.error_handler import NotFoundError
from app.schemas.report import DeleteReportResponse, HistoryResponse, ReportDetailResponse
from app.services.report_service import report_service

router = APIRouter(tags=["Reports"])


@router.get("/history", response_model=HistoryResponse, summary="Get analysis history")
async def get_history(
    user_id: Annotated[str, Depends(get_current_user_id)],
    search: str | None = Query(default=None, max_length=100),
) -> HistoryResponse:
    return await report_service.get_history(user_id, search=search)


@router.get("/report/{report_id}", response_model=ReportDetailResponse, summary="Get report details")
async def get_report(
    report_id: str,
    user_id: Annotated[str, Depends(get_current_user_id)],
) -> ReportDetailResponse:
    return await report_service.get_report_detail(report_id, user_id)


@router.delete("/report/{report_id}", response_model=DeleteReportResponse, summary="Delete a report")
async def delete_report(
    report_id: str,
    user_id: Annotated[str, Depends(get_current_user_id)],
) -> DeleteReportResponse:
    await report_service.delete_report(report_id, user_id)
    return DeleteReportResponse(message="Report deleted successfully.", report_id=report_id)


@router.get("/download/{report_id}", summary="Download report PDF")
async def download_report(
    report_id: str,
    user_id: Annotated[str, Depends(get_current_user_id)],
) -> FileResponse:
    report = await report_service.get_report_document(report_id, user_id)
    pdf_path = await report_service.ensure_pdf_path(report_id, user_id)

    if not pdf_path or not Path(pdf_path).exists():
        raise NotFoundError("PDF report is not available for this analysis.")

    filename = f"{report.get('title', 'resume-report').replace(' ', '_')}.pdf"
    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=filename,
        headers={"Cache-Control": "no-store"},
    )
