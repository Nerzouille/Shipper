"""Viability score generation via OpenHosta LLM.

TODO: implement streaming LLM call.
"""

from typing import AsyncGenerator
from src.models.sse import LLMTokenEvent, LLMCompleteEvent, LLMErrorEvent
from src.models.report import AggregatedData


async def stream_viability_score(
    data: AggregatedData,
) -> AsyncGenerator[LLMTokenEvent | LLMCompleteEvent | LLMErrorEvent, None]:
    """Stream a viability score (0-100) + explanation from LLM.

    Yields LLMTokenEvent for each token, then a final LLMCompleteEvent with
    score (int) and full content. Yields LLMErrorEvent on failure.

    SSE event name: viability_score
    """
    raise NotImplementedError("Viability scorer not implemented yet")
    yield  # make this an async generator
