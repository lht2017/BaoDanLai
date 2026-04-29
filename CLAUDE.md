# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BaoDanLai (爆单来) — A-share AI automated market review tool. Full-stack Python/FastAPI backend + Vue 3/TypeScript frontend. Designed for eventual migration to a WeChat Mini Program.

## Development Commands

### Infrastructure
```bash
docker-compose up -d    # Start PostgreSQL 16 (5432) and Redis 7 (6379)
docker-compose down     # Stop services
```

### Backend (run from `backend/`)
```bash
pip install -r requirements.txt
cp .env.example .env       # Fill in AI_API_KEY, TUSHARE_TOKEN, etc.
uvicorn app.main:app --reload --port 8000
```
Tables auto-create on startup via `Base.metadata.create_all`. Alembic is installed but not yet initialized.

### Frontend (run from `frontend/`)
```bash
npm install
npm run dev       # Vite dev server on :5173, proxies /api → localhost:8000
npm run build     # vue-tsc type-check + vite build
```

## Architecture

### Backend — Layered (FastAPI + SQLAlchemy 2.0 async)
- `app/core/config.py` — Singleton settings via pydantic-settings (`@lru_cache`), computes DATABASE_URL/REDIS_URL
- `app/core/database.py` — Async engine + session factory
- `app/core/redis.py` — Async Redis singleton
- `app/models/` — SQLAlchemy declarative models using `Mapped` type annotations
- `app/schemas/` — Pydantic v2 models (`from_attributes = True`) for request/response
- `app/services/` — Async business logic, receive `AsyncSession` as parameter
- `app/api/v1/` — FastAPI routers, versioned under `/api/v1/`, inject DB via `Depends(get_db)`

### Frontend — Vue 3 Composition API
- `src/api/index.ts` — Centralized Axios client with all API functions + TypeScript interfaces. Co-located for easy `wx.request` migration to WeChat Mini Program.
- `src/stores/stock.ts` — Pinia composition store for search and watchlist state
- `src/views/` — Page components, all lazy-loaded via router
- `src/styles/notion.css` — Notion-inspired design system (no component library)
- `@/` path alias maps to `src/`

### Database Schema (6 tables)
`users` (with WeChat openid/unionid), `stocks`, `stock_daily_quotes` (unique on ts_code+trade_date), `news`, `ai_reviews`, `review_stock_picks`, `watchlist` (unique on user_id+ts_code). DDL + seed data in `backend/sql/init.sql`.

### Stock Data Sources
`tushare` and `akshare` packages for A-share market data.

## Key Notes
- No test framework, linter, or CI/CD configured yet
- Auth is hardcoded (`user_id=1` in watchlist endpoints); JWT planned but not implemented
- AI review generation: config exists (DeepSeek) but no calling service code yet; `httpx` is the intended client
- `app/utils/` is empty — utility code not yet written
- Frontend dependencies may not be installed (no lock file in repo)
