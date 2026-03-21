"""Data source unit tests (TDD — RED phase).

These tests define the expected interface and return shape for each source.
They are expected to FAIL until each source is implemented.

Run with: uv run pytest src/tests/test_sources.py -v
"""

import pytest
from src.models.report import SourceResult
from src.pipeline.sources.amazon import fetch_amazon
from src.pipeline.sources.trends import fetch_trends
from src.pipeline.sources.reddit import fetch_reddit


# --- Interface contract: all sources return SourceResult ---

async def test_amazon_returns_source_result():
    """fetch_amazon MUST return a SourceResult."""
    result = await fetch_amazon("bamboo skincare", timeout=10)
    assert isinstance(result, SourceResult)


async def test_trends_returns_source_result():
    """fetch_trends MUST return a SourceResult."""
    result = await fetch_trends("bamboo skincare", timeout=10)
    assert isinstance(result, SourceResult)


async def test_reddit_returns_source_result():
    """fetch_reddit MUST return a SourceResult."""
    result = await fetch_reddit("bamboo skincare", timeout=10)
    assert isinstance(result, SourceResult)


# --- Success path: returned data shape ---

async def test_amazon_success_contains_products():
    """On success, amazon result MUST have data['products'] as a list."""
    result = await fetch_amazon("bamboo skincare", timeout=10)
    if result.status == "success":
        assert isinstance(result.data, dict)
        assert isinstance(result.data.get("products"), list)
        for p in result.data["products"]:
            assert "title" in p
            assert "price" in p
            assert "url" in p


async def test_trends_success_contains_interest():
    """On success, trends result MUST have data['interest']."""
    result = await fetch_trends("bamboo skincare", timeout=10)
    if result.status == "success":
        assert isinstance(result.data, dict)
        assert "interest" in result.data


async def test_reddit_success_contains_posts():
    """On success, reddit result MUST have data['posts'] as a list."""
    result = await fetch_reddit("bamboo skincare", timeout=10)
    if result.status == "success":
        assert isinstance(result.data, dict)
        assert isinstance(result.data.get("posts"), list)


# --- Timeout path: status must be "timeout" not an exception ---

async def test_amazon_timeout_returns_timeout_status():
    """Amazon fetch with timeout=0 MUST return status='timeout', not raise."""
    result = await fetch_amazon("bamboo skincare", timeout=0)
    assert result.status == "timeout"


async def test_trends_timeout_returns_timeout_status():
    """Trends fetch with timeout=0 MUST return status='timeout', not raise."""
    result = await fetch_trends("bamboo skincare", timeout=0)
    assert result.status == "timeout"


async def test_reddit_timeout_returns_timeout_status():
    """Reddit fetch with timeout=0 MUST return status='timeout', not raise."""
    result = await fetch_reddit("bamboo skincare", timeout=0)
    assert result.status == "timeout"
