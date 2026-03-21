"""SSE stream contract tests (TDD — RED phase).

These tests define the expected SSE event sequence and payload shapes
per contracts/sse-events.md. They are expected to FAIL until the
pipeline is implemented.

Run with: uv run pytest src/tests/test_stream_contract.py -v
"""

import json
import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app


async def collect_sse_events(keyword: str) -> list[dict]:
    """Stream /stream endpoint and collect all parsed SSE events."""
    events = []
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        async with client.stream("GET", f"/stream?keyword={keyword}") as response:
            assert response.status_code == 200
            current_event_name = "message"
            async for line in response.aiter_lines():
                if line.startswith("event:"):
                    current_event_name = line[len("event:"):].strip()
                elif line.startswith("data:"):
                    data_str = line[len("data:"):].strip()
                    events.append({
                        "event": current_event_name,
                        "data": json.loads(data_str),
                    })
                    current_event_name = "message"
    return events


# --- Contract: event sequence ---

async def test_stream_emits_marketplace_products_first():
    """First event MUST be marketplace_products (constitution Principle I + NFR1)."""
    events = await collect_sse_events("bamboo skincare")
    assert len(events) > 0, "No SSE events received"
    assert events[0]["event"] == "marketplace_products", (
        f"First event must be 'marketplace_products', got '{events[0]['event']}'"
    )


async def test_stream_emits_export_ready_last():
    """Last event MUST be export_ready."""
    events = await collect_sse_events("bamboo skincare")
    assert events[-1]["event"] == "export_ready", (
        f"Last event must be 'export_ready', got '{events[-1]['event']}'"
    )


async def test_stream_contains_all_required_sections():
    """All 5 content sections MUST appear in the stream."""
    events = await collect_sse_events("bamboo skincare")
    event_names = {e["event"] for e in events}
    required = {
        "marketplace_products",
        "viability_score",
        "target_persona",
        "differentiation_angles",
        "competitive_overview",
    }
    missing = required - event_names
    assert not missing, f"Missing sections in SSE stream: {missing}"


# --- Contract: marketplace_products payload shape ---

async def test_marketplace_products_payload_shape():
    """marketplace_products event MUST have status='complete' and a products list."""
    events = await collect_sse_events("bamboo skincare")
    mp_events = [e for e in events if e["event"] == "marketplace_products"]
    assert len(mp_events) == 1, "Expected exactly one marketplace_products event"
    payload = mp_events[0]["data"]
    assert payload.get("status") == "complete"
    assert isinstance(payload.get("products"), list)


async def test_marketplace_products_items_have_required_fields():
    """Each product MUST have title, price, and url fields."""
    events = await collect_sse_events("bamboo skincare")
    mp_events = [e for e in events if e["event"] == "marketplace_products"]
    products = mp_events[0]["data"].get("products", [])
    for product in products:
        assert "title" in product, f"Product missing 'title': {product}"
        assert "price" in product, f"Product missing 'price': {product}"
        assert "url" in product, f"Product missing 'url': {product}"


# --- Contract: viability_score complete payload ---

async def test_viability_score_complete_has_score_field():
    """viability_score complete event MUST have an integer score 0-100."""
    events = await collect_sse_events("bamboo skincare")
    complete_events = [
        e for e in events
        if e["event"] == "viability_score" and e["data"].get("status") == "complete"
    ]
    assert len(complete_events) == 1, "Expected exactly one viability_score complete event"
    score = complete_events[0]["data"].get("score")
    assert isinstance(score, int), f"Score must be int, got {type(score)}"
    assert 0 <= score <= 100, f"Score must be 0-100, got {score}"


# --- Contract: source_unavailable payload ---

async def test_source_unavailable_has_source_field():
    """source_unavailable events MUST have a 'source' field."""
    events = await collect_sse_events("bamboo skincare")
    unavailable_events = [e for e in events if e["event"] == "source_unavailable"]
    for event in unavailable_events:
        assert "source" in event["data"], f"source_unavailable missing 'source': {event}"
        assert event["data"]["source"] in ("amazon", "google_trends", "reddit")


# --- Contract: empty keyword rejected ---

async def test_empty_keyword_returns_422():
    """Empty keyword MUST be rejected with 422 (validation error)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/stream?keyword=")
    assert response.status_code == 422


async def test_missing_keyword_returns_422():
    """Missing keyword MUST be rejected with 422."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/stream")
    assert response.status_code == 422
