"""Pipeline orchestrator.

Coordinates parallel source fetching and sequential LLM analysis,
emitting SSE events in the stable order defined by the constitution:

  marketplace_products → viability_score → target_persona
  → differentiation_angles → competitive_overview → export_ready

TODO: wire real source fetchers and LLM analysis chain.
"""

import asyncio
from typing import AsyncGenerator

from src.config import Settings
from src.models.sse import (
    MarketplaceProductsEvent,
    SourceUnavailableEvent,
    ExportReadyEvent,
    format_sse,
)
from src.models.report import AggregatedData, AnalysisReport

# In-process report store: session_id → AnalysisReport
# This is the only "persistence" — lives for the duration of the process.
_report_store: dict[str, AnalysisReport] = {}


async def run_pipeline(
    keyword: str,
    session_id: str,
    settings: Settings,
) -> AsyncGenerator[str, None]:
    """Run the full analysis pipeline for a keyword.

    Yields SSE-formatted strings (wire frames) ready to send to the client.
    Stores the completed AnalysisReport in _report_store keyed by session_id.

    Current state: stub — emits placeholder events to prove the SSE pipeline works.
    """
    # TODO: replace stub with real implementation
    # Step 1: parallel source fetch (amazon, trends, reddit)
    # Step 2: emit source_unavailable for timed-out sources
    # Step 3: emit marketplace_products
    # Step 4: build AggregatedData
    # Step 5: stream viability_score, target_persona, differentiation_angles, competitive_overview
    # Step 6: store report, emit export_ready

    # Stub: emit a placeholder marketplace_products event so the frontend renders
    products_event = MarketplaceProductsEvent(products=[])
    yield format_sse("marketplace_products", products_event)

    export_event = ExportReadyEvent()
    yield format_sse("export_ready", export_event)


def get_report(session_id: str) -> AnalysisReport | None:
    return _report_store.get(session_id)
