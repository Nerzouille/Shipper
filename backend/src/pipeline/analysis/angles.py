"""Differentiation angles generation via OpenHosta LLM.

TODO: implement streaming LLM call.
"""

from typing import AsyncGenerator
from src.models.sse import LLMTokenEvent, LLMCompleteEvent, LLMErrorEvent
from src.models.report import AggregatedData


async def stream_angles(
    data: AggregatedData,
) -> AsyncGenerator[LLMTokenEvent | LLMCompleteEvent | LLMErrorEvent, None]:
    """Stream actionable differentiation angles from LLM.

    SSE event name: differentiation_angles
    """
    raise NotImplementedError("Differentiation angles generator not implemented yet")
    yield
