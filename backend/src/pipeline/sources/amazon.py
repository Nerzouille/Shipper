"""Amazon marketplace scraper.

TODO: implement real scraping with httpx + BeautifulSoup4.
"""

import asyncio
from src.models.report import SourceResult


async def fetch_amazon(keyword: str, timeout: int = 10) -> SourceResult:
    """Fetch marketplace products from Amazon search results.

    Returns SourceResult with status:
      - "success": products list in data["products"]
      - "timeout": source exceeded timeout
      - "error":   unexpected failure
    """
    raise NotImplementedError("Amazon scraper not implemented yet")
