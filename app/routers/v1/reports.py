from fastapi import APIRouter

from ...crud.report import get_report

router = APIRouter()


@router.get("/{report_code}", tags=["reports"])
async def read_reports(report_code: str):
    results = await get_report(report_code)

    return {
        "report_code": report_code,
        "report": results,
    }
