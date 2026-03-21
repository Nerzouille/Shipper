"""Reddit community sentiment source.

TODO: implement with Reddit public JSON API (no auth required).
"""

import asyncio
from src.models.report import SourceResult


async def fetch_reddit(keyword: str, timeout: int = 10) -> SourceResult:
    """Fetch community sentiment from Reddit search.

    Endpoint: https://www.reddit.com/search.json?q={keyword}&sort=relevance&limit=25
    No authentication required for public search.

    Returns SourceResult with status:
      - "success": posts in data["posts"] (title, score, subreddit, num_comments)
      - "timeout": source exceeded timeout
      - "error":   unexpected failure
    """
    raise NotImplementedError("Reddit source not implemented yet")
