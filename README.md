# Market Intelligence AI

> Enter a product idea. Watch the market analysis build itself in real time.

A hackathon-MVP web app that turns a keyword into a structured market intelligence
report — streamed live, section by section — in under 60 seconds.

```
Browser → EventSource('/api/sse') → SvelteKit BFF → FastAPI pipeline → LLM + scrapers
```

---

## What it does

1. User types a keyword (e.g. *"eco-friendly bamboo skincare"*)
2. The backend fires parallel requests to **Amazon**, **Google Trends**, and **Reddit**
3. Marketplace products appear within **5 seconds** as the first live result
4. An LLM streams the remaining sections token-by-token:
   - **Viability score** (0–100) with explanation
   - **Target persona**
   - **Differentiation angles**
   - **Competitive overview**
5. Full report done in **< 60 seconds**
6. Export as **Markdown** (agent-parsable schema) or **PDF**

---

## Stack

| Layer | Technology |
|-------|-----------|
| Frontend | SvelteKit 2 + Svelte 5 (runes) |
| UI components | shadcn-svelte |
| Frontend runtime | Bun |
| Backend | FastAPI + Python 3.12 |
| Backend runtime | uv |
| Streaming | Server-Sent Events (SSE) — BFF proxy pattern |
| LLM | OpenHosta → OpenAI `gpt-4o-mini` (configurable) |
| Marketplace | Amazon (httpx + BeautifulSoup4) |
| Trends | Google Trends (pytrends) |
| Social | Reddit public JSON API |
| PDF export | fpdf2 |

---

## Project structure

```
.
├── backend/                  # FastAPI backend (uv)
│   ├── src/
│   │   ├── main.py           # App factory, CORS, /health
│   │   ├── config.py         # pydantic-settings (APP_* env vars)
│   │   ├── models/           # Pydantic SSE + report models
│   │   ├── routes/           # /stream, /export/md, /export/pdf
│   │   └── pipeline/
│   │       ├── orchestrator.py     # Parallel fetch + LLM chain + SSE emission
│   │       ├── sources/            # amazon.py, trends.py, reddit.py
│   │       ├── analysis/           # scorer, persona, angles, competitive
│   │       ├── export_generator.py # Markdown schema
│   │       └── pdf_generator.py    # fpdf2 PDF
│   └── src/tests/            # pytest test suite (TDD)
├── frontend/                 # SvelteKit frontend (bun)
│   └── src/
│       ├── lib/
│       │   ├── types.ts      # Zod schemas for all SSE events
│       │   └── sse.ts        # EventSource wrapper
│       └── routes/
│           ├── api/sse/      # BFF SSE proxy → FastAPI
│           └── +page.svelte  # Main page (Svelte 5 runes)
├── specs/                    # Product spec, plan, tasks, contracts
│   └── 001-market-intelligence-mvp/
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       ├── contracts/        # Frozen SSE event + MD export schemas
│       └── research.md
├── run.sh                    # Start both services
└── prd.md                    # Product Requirements Document
```

---

## Getting started

### Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) — Python package manager
- [Bun](https://bun.sh) — JavaScript runtime
- An OpenAI API key

### 1. Configure environment

```bash
cp backend/.env.example backend/.env
# Edit backend/.env and set APP_OPENAI_API_KEY=sk-...

cp frontend/.env.example frontend/.env
```

### 2. Start both services

```bash
chmod +x run.sh
./run.sh
```

Opens:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000

### 3. Manual start (if needed)

```bash
# Backend
cd backend
uv sync
uv run uvicorn src.main:app --reload --port 8000

# Frontend (separate terminal)
cd frontend
bun install
bun run dev
```

---

## API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check → `{"status": "ok"}` |
| `/stream?keyword={kw}` | GET | SSE stream (via BFF: `/api/sse?keyword={kw}`) |
| `/export/md?keyword={kw}` | GET | Markdown report download |
| `/export/pdf?keyword={kw}` | GET | PDF report download |

### SSE event sequence (stable contract)

```
source_unavailable?      ← 0–3 times if a source times out
marketplace_products     ← first event, < 5s
viability_score          ← streaming tokens → complete
target_persona           ← streaming tokens → complete
differentiation_angles   ← streaming tokens → complete
competitive_overview     ← streaming tokens → complete
export_ready             ← signals report complete
```

Each LLM section follows the pattern:

```json
{"status": "streaming", "token": "The"}
{"status": "streaming", "token": " market"}
{"status": "complete",  "content": "The market shows...", "score": 74}
```

### Markdown export schema (machine-parsable)

The Markdown export follows a frozen schema designed for AI agent consumption:

```markdown
# Market Intelligence Report: {keyword}

## Marketplace Products
- **{title}** — {price} — [View on Amazon]({url})

## Viability Score
Score: 74/100        ← always this exact format

## Target Persona
...

## Differentiation Angles
...

## Competitive Overview
...
```

Score extraction regex: `^Score: (\d+)/100$`

---

## Development

### Running tests

```bash
cd backend
uv run pytest -v
```

Current TDD status:

| Test file | Status | Turns green when |
|-----------|--------|-----------------|
| `test_health.py` | ✅ GREEN | — |
| `test_stream_contract.py` | 🟡 6/8 | LLM sections wired in orchestrator |
| `test_sources.py` | 🔴 0/9 | Amazon / Trends / Reddit implemented |
| `test_export.py` | 🔴 0/7 | `generate_markdown()` implemented |

### Backend configuration

All settings use the `APP_` env prefix:

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_OPENAI_API_KEY` | *(required)* | OpenAI API key |
| `APP_LLM_MODEL` | `gpt-4o-mini` | LLM model name |
| `APP_CORS_ORIGINS` | `["http://localhost:5173"]` | Allowed CORS origins |
| `APP_SOURCE_TIMEOUT` | `10` | Seconds before a data source is skipped |

### Architecture notes

**BFF proxy pattern**: The browser connects to SvelteKit's `/api/sse`, which proxies
to FastAPI. FastAPI is never exposed directly to the browser. This avoids CORS
complexity and allows adding auth headers later without frontend changes.

**Pipeline resilience**: Each data source has a 10-second timeout. If a source
exceeds it, the pipeline emits a `source_unavailable` event and continues with
the remaining sources. Results are always partial rather than total failure.

**Svelte 5 rune workaround**: svelte-check 4.4.5 requires the `$state()` variable
name to contain the string `"state"`. Use `let pageState = $state({...})`, not
`let data = $state({...})`.

---

## Roadmap

**Phase 1 — Hackathon MVP** *(current)*
- [x] Project architecture + SSE pipeline scaffold
- [x] TDD test suite (RED phase)
- [ ] Amazon scraper
- [ ] Google Trends + Reddit sources
- [ ] LLM analysis chain (OpenHosta)
- [ ] Markdown + PDF export
- [ ] Full dashboard UI (shadcn-svelte)

**Phase 2 — Post-hackathon**
- [ ] X/Twitter and eBay data sources
- [ ] Analysis history and idea comparison
- [ ] External agent API

**Phase 3 — Vision**
- [ ] Real-time market monitoring with alerts
- [ ] Team collaboration
- [ ] White-label reports
