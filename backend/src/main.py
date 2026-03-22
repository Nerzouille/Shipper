import uuid
import asyncio
import json
from typing import Dict, List, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from src.routes.workflow import router as workflow_router
from src.routes.export import router as export_router

from src.scraper import (
    fetch_html, 
    clean_html_for_llm, 
    parse_marketplace_data, 
    generate_search_queries
)

MEMORY_STORE: Dict[str, Dict[str, Any]] = {}
CONCURRENCY_LIMITER = asyncio.Semaphore(2)  # Limit to 2 concurrent API calls total

app = FastAPI(title="Guided Analysis Workflow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workflow_router)
app.include_router(export_router)

class InitSearchRequest(BaseModel):
    product_description: str

class InitSearchResponse(BaseModel):
    session_id: str
    search_queries: List[str]

class ScrapeStreamRequest(BaseModel):
    final_queries: List[str]

class GenerateStrategyResponse(BaseModel):
    market_bilan: str
    persona: Dict[str, Any]
    strategy: str

@app.post("/api/init-search", response_model=InitSearchResponse)
async def init_search(request: InitSearchRequest):
    session_id = str(uuid.uuid4())
    
    MEMORY_STORE[session_id] = {
        "product_description": request.product_description,
        "search_queries": [],
        "products_by_source": {}
    }
    
    queries = await generate_search_queries(request.product_description)
    
    MEMORY_STORE[session_id]["search_queries"] = queries
    
    return InitSearchResponse(
        session_id=session_id,
        search_queries=queries
    )

async def process_single_source(source: str, queries: List[str]) -> dict:
    """Processes multiple queries for a single source, keeping only unique products (by URL)."""
    all_products = []
    seen_urls = set()
    
    # Define base URLs for absolute link reconstruction
    BASE_URLS = {
        "Amazon": "https://www.amazon.fr",
        "Aliexpress": "https://www.aliexpress.com",
        "eBay": "https://www.ebay.fr"
    }
    base_url = BASE_URLS.get(source, "")
    
    async def fetch_and_parse(query: str):
        async with CONCURRENCY_LIMITER:
            raw_html = await fetch_html(source, query)
            if not raw_html:
                return []
            
            clean_text = clean_html_for_llm(raw_html, base_url=base_url)
            if not clean_text:
                return []
            
            await asyncio.sleep(0.5)
            return await parse_marketplace_data(clean_text)

    all_tasks = []
    for i, q in enumerate(queries):
        all_tasks.append(fetch_and_parse(q))
        if i < len(queries) - 1:
            await asyncio.sleep(1) # stagger task creation
            
    results = await asyncio.gather(*all_tasks, return_exceptions=True)
    
    for products_list in results:
        if isinstance(products_list, Exception):
            print(f"Error processing a query for {source}: {products_list}")
            continue
            
        for p in products_list:
            key = p.get('url') or p.get('title')
            if key and key not in seen_urls:
                seen_urls.add(key)
                all_products.append(p)
                
    return {"source": source, "products": all_products}

@app.post("/api/scrape-stream/{session_id}")
async def scrape_stream(session_id: str, request: ScrapeStreamRequest):
    if session_id not in MEMORY_STORE:
        raise HTTPException(status_code=404, detail="Invalid or expired session")
        
    MEMORY_STORE[session_id]["search_queries"] = request.final_queries
    final_queries = request.final_queries
    
    sources = ["Amazon", "Aliexpress", "eBay"]
    for source in sources:
        MEMORY_STORE[session_id]["products_by_source"][source] = []

    async def event_generator():
        tasks = {
            asyncio.create_task(process_single_source(source, final_queries)): source
            for source in sources
        }
        
        pending = set(tasks.keys())
        
        while pending:
            done, pending = await asyncio.wait(
                pending, 
                return_when=asyncio.FIRST_COMPLETED,
                timeout=15.0
            )
            
            if not done:
                yield ": keep-alive\n\n"
                continue

            for completed_task in done:
                try:
                    result = await completed_task
                    source_name = result["source"]
                    products = result["products"]
                    
                    MEMORY_STORE[session_id]["products_by_source"][source_name] = products
                    
                    yield f"event: source_ready\n"
                    yield f"data: {json.dumps(result)}\n\n"
                except Exception as e:
                    yield f"event: error\n"
                    yield f"data: {json.dumps({'error': str(e)})}\n\n"
            
        yield "event: stream_complete\n"
        yield "data: {}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.post("/api/generate-strategy/{session_id}", response_model=GenerateStrategyResponse)
async def generate_strategy(session_id: str):
    if session_id not in MEMORY_STORE:
        raise HTTPException(status_code=404, detail="Invalid or expired session")
        
    session_data = MEMORY_STORE[session_id]
    all_products = session_data["products_by_source"]
    
    # TODO: Implement final LLM strategy generation using OpenHosta
    
    mock_strategy = {
        "market_bilan": "High demand, but current products suffer from long delivery times.",
        "persona": {
            "name": "Julie, 28",
            "need": "Speed and guaranteed quality",
            "budget": "Comfortable"
        },
        "strategy": "Focus messaging on 24h delivery and source via short supply chains."
    }
    
    return GenerateStrategyResponse(**mock_strategy)

@app.get("/health")
async def health():
    return {"status": "ok"}
