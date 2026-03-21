"""Google Trends data source.

TODO: implement with pytrends.
"""

import asyncio
from src.models.report import SourceResult


async def fetch_trends(keyword: str, timeout: int = 10) -> SourceResult:
    """Fetch demand-signal data from Google Trends.

    Returns SourceResult with status:
      - "success": trend data in data["interest"] and data["related_queries"]
      - "timeout": source exceeded timeout
      - "error":   unexpected failure
    """
    raise NotImplementedError("Google Trends source not implemented yet")
