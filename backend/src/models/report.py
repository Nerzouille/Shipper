"""Report / export domain models."""

from datetime import datetime
from pydantic import BaseModel
from .sse import MarketplaceProduct


class ViabilityScore(BaseModel):
    score: int  # 0-100
    explanation: str


class TargetPersona(BaseModel):
    description: str


class DifferentiationAngles(BaseModel):
    content: str


class CompetitiveOverview(BaseModel):
    content: str


class SourceResult(BaseModel):
    source: str
    status: str  # "success" | "timeout" | "error"
    data: dict | None = None
    error_message: str | None = None


class AggregatedData(BaseModel):
    keyword: str
    products: list[MarketplaceProduct] = []
    trend_data: dict | None = None
    reddit_data: dict | None = None
    available_sources: list[str] = []
    unavailable_sources: list[str] = []


class AnalysisReport(BaseModel):
    keyword: str
    generated_at: datetime
    products: list[MarketplaceProduct] = []
    viability: ViabilityScore | None = None
    persona: TargetPersona | None = None
    angles: DifferentiationAngles | None = None
    competitive: CompetitiveOverview | None = None
    unavailable_sources: list[str] = []
    is_partial: bool = False
