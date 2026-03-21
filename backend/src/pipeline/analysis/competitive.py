"""Competitive overview generation via OpenHosta LLM.

TODO: implement streaming LLM call.
"""

from typing import AsyncGenerator
from src.models.sse import LLMTokenEvent, LLMCompleteEvent, LLMErrorEvent
from src.models.report import AggregatedData


async def stream_competitive(
    data: AggregatedData,
) -> AsyncGenerator[LLMTokenEvent | LLMCompleteEvent | LLMErrorEvent, None]:
    """Stream a competitive overview from LLM.

    SSE event name: competitive_overview
    """
    raise NotImplementedError("Competitive overview generator not implemented yet")
    yield
