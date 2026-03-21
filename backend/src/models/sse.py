"""SSE event payload models.

Event names (frozen per constitution Principle III):
  marketplace_products → viability_score → target_persona
  → differentiation_angles → competitive_overview → export_ready
"""

from typing import Literal
from pydantic import BaseModel, Field


class MarketplaceProduct(BaseModel):
    title: str
    price: str  # formatted string, e.g. "$14.99" or "N/A"
    url: str


# --- marketplace_products event ---

class MarketplaceProductsEvent(BaseModel):
    status: Literal["complete"] = "complete"
    products: list[MarketplaceProduct] = Field(default_factory=list)


# --- LLM section events (streaming / complete / error) ---

class LLMTokenEvent(BaseModel):
    status: Literal["streaming"] = "streaming"
    token: str


class LLMCompleteEvent(BaseModel):
    status: Literal["complete"] = "complete"
    content: str
    score: int | None = Field(default=None, ge=0, le=100)


class LLMErrorEvent(BaseModel):
    status: Literal["error"] = "error"
    partial_content: str = ""
    message: str


# --- source_unavailable event ---

class SourceUnavailableEvent(BaseModel):
    source: Literal["amazon", "google_trends", "reddit"]
    message: str


# --- export_ready event ---

class ExportReadyEvent(BaseModel):
    status: Literal["complete"] = "complete"


def format_sse(event_name: str, payload: BaseModel) -> str:
    """Format a Pydantic model as an SSE wire frame."""
    return f"event: {event_name}\ndata: {payload.model_dump_json()}\n\n"
