"""Export endpoints.

GET /export/md?keyword={kw}   → Markdown file download
GET /export/pdf?keyword={kw}  → PDF file download

TODO: wire to report store and generators once pipeline is implemented.
"""

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import Response

router = APIRouter(prefix="/export")


@router.get("/md")
async def export_md(keyword: str = Query(..., min_length=1)):
    # TODO: retrieve report from orchestrator._report_store
    # TODO: call export_generator.generate_markdown(report)
    raise HTTPException(status_code=501, detail="Export not implemented yet")


@router.get("/pdf")
async def export_pdf(keyword: str = Query(..., min_length=1)):
    # TODO: retrieve report from orchestrator._report_store
    # TODO: call pdf_generator.generate_pdf(markdown_content)
    raise HTTPException(status_code=501, detail="Export not implemented yet")
