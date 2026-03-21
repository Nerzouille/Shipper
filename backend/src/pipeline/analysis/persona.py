"""Target persona generation via OpenHosta LLM.

TODO: implement streaming LLM call.
"""

from typing import AsyncGenerator
from src.models.sse import LLMTokenEvent, LLMCompleteEvent, LLMErrorEvent
from src.models.report import AggregatedData


async def stream_persona(
    data: AggregatedData,
) -> AsyncGenerator[LLMTokenEvent | LLMCompleteEvent | LLMErrorEvent, None]:
    """Stream a target persona description from LLM.

    SSE event name: target_persona
    """
    raise NotImplementedError("Persona generator not implemented yet")
    yield
