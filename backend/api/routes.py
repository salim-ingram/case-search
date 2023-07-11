from io import StringIO
from typing import List, Optional

from api import utilities as utils
from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import Response
from schemas.case import Case, CaseQuery

router = APIRouter()


@router.post("/query_by_name", response_model=List[CaseQuery])
async def get_cases_by_name(
    case_name: str,
    citation: Optional[str] | None = None,
) -> List[CaseQuery]:
    return await utils.get_cases_by_name(
        case_name=case_name,
        citation=citation,
    )


@router.post("/case", response_model=Case)
async def get_case_by_id(id: int, include_summary: bool) -> Case:
    return await utils.get_case_by_id(id=id, include_summary=include_summary)


@router.post("/case/summary")
async def get_case_summary(id: int) -> str:
    case = await utils.get_case_by_id(id=id, include_summary=True)
    return case["summary"]


@router.post("/case/download", response_class=Response)
async def download_case(id: int, background_tasks: BackgroundTasks):
    case = await get_case_by_id(id=id, include_summary=False)
    content = [
        "TY  - CASE \n",
        f"TI  - {case['case_name']} \n",
        f"A2  - {case['reporter']} \n",
        f"AB  - {case['summary']} \n",
        f"DA  - {case['date_decided']} \n",
        f"PY  - {(case['date_decided']).split('-')[0]} \n",
        f"VL  - {case['reporter_volume']} \n",
        f"SP  - {case['first_page']} \n",
        f"PB  - {case['court']} \n",
        f"SV  - {case['docket_number']} \n",
        f"UR  - {case['frontend_pdf_url']} \n",
        f"M1  - citation: {case['citation']}  \n",
        "ER  - ",
    ]
    buffer = StringIO()
    buffer.writelines(content)
    background_tasks.add_task(buffer.close)
    headers = {"Content-Disposition": 'attachment; filename="export.ris"'}
    return Response(
        buffer.getvalue(),
        headers=headers,
        media_type="application/x-research-info-systems",
    )
