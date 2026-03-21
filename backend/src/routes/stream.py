"""SSE streaming endpoint.

GET /stream?keyword={kw}
"""

import uuid
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse, JSONResponse

from src.config import settings
from src.pipeline.orchestrator import run_pipeline

router = APIRouter()


@router.get("/stream")
async def stream(keyword: str = Query(..., min_length=1)):
    session_id = str(uuid.uuid4())

    return StreamingResponse(
        run_pipeline(keyword, session_id, settings),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
