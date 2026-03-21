"""Export generator tests (TDD — RED phase).

These tests validate the frozen Markdown export schema per contracts/export-schema.md.
They are expected to FAIL until the export generator is implemented.

Run with: uv run pytest src/tests/test_export.py -v
"""

import re
from datetime import datetime, timezone
import pytest

from src.models.report import (
    AnalysisReport,
    ViabilityScore,
    TargetPersona,
    DifferentiationAngles,
    CompetitiveOverview,
)
from src.pipeline.export_generator import generate_markdown


def _make_full_report(keyword: str = "bamboo skincare", score: int = 74) -> AnalysisReport:
    from src.models.sse import MarketplaceProduct
    return AnalysisReport(
        keyword=keyword,
        generated_at=datetime(2026, 3, 21, 12, 0, tzinfo=timezone.utc),
        products=[
            MarketplaceProduct(title="Bamboo Face Wash", price="$14.99", url="https://amazon.com/dp/B001"),
        ],
        viability=ViabilityScore(score=score, explanation="Moderate opportunity."),
        persona=TargetPersona(description="Urban women aged 25-35."),
        angles=DifferentiationAngles(content="1. Zero-waste packaging"),
        competitive=CompetitiveOverview(content="3 dominant players."),
        unavailable_sources=[],
        is_partial=False,
    )


# --- Schema: score line format (machine-parsable contract) ---

def test_markdown_score_line_format():
    """Score MUST appear as 'Score: {n}/100' on its own line (frozen contract)."""
    report = _make_full_report(score=74)
    md = generate_markdown(report)
    assert re.search(r"^Score: 74/100$", md, re.MULTILINE), (
        "Score line missing or malformed. Must be exactly 'Score: 74/100'"
    )


def test_markdown_score_line_low_score():
    """Low score MUST use same format: 'Score: 28/100'."""
    report = _make_full_report(score=28)
    md = generate_markdown(report)
    assert re.search(r"^Score: 28/100$", md, re.MULTILINE)


# --- Schema: section headings (stable contract) ---

def test_markdown_has_all_required_headings():
    """All 5 section headings MUST be present."""
    report = _make_full_report()
    md = generate_markdown(report)
    assert "## Marketplace Products" in md
    assert "## Viability Score" in md
    assert "## Target Persona" in md
    assert "## Differentiation Angles" in md
    assert "## Competitive Overview" in md


# --- Schema: partial report flag ---

def test_markdown_partial_report_flag():
    """Partial report MUST include '**Partial report**:' line."""
    report = _make_full_report()
    report.unavailable_sources = ["amazon"]
    report.is_partial = True
    md = generate_markdown(report)
    assert "**Partial report**:" in md
    assert "amazon" in md


def test_markdown_no_partial_flag_when_complete():
    """Complete report MUST NOT include partial report flag."""
    report = _make_full_report()
    md = generate_markdown(report)
    assert "**Partial report**:" not in md


# --- Schema: N/A handling ---

def test_markdown_score_na_when_viability_missing():
    """Missing viability section MUST produce 'Score: N/A'."""
    report = _make_full_report()
    report.viability = None
    md = generate_markdown(report)
    assert re.search(r"^Score: N/A$", md, re.MULTILINE)


# --- Schema: product listing ---

def test_markdown_product_has_title_price_url():
    """Each product MUST appear with title, price, and URL."""
    report = _make_full_report()
    md = generate_markdown(report)
    assert "Bamboo Face Wash" in md
    assert "$14.99" in md
    assert "https://amazon.com/dp/B001" in md
