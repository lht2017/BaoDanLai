"""
爆单来 BaoDanLai — FastAPI 主入口
启动: uvicorn app.main:app --reload --port 8000
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.database import engine, Base
from app.core.redis import close_redis
from app.api.v1 import stocks, reviews, news
from app.models.limit_up import LimitUpStock, MarketSentiment

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：启动时建表，关闭时断开连接"""
    # 启动：自动创建所有表（开发阶段，生产用 Alembic）
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # 关闭
    await close_redis()


app = FastAPI(
    title=settings.APP_NAME,
    description="A股AI自动复盘工具 — 后端API",
    version="0.1.0",
    lifespan=lifespan,
)

# 跨域配置（开发阶段允许所有来源）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(stocks.router, prefix="/api/v1")
app.include_router(reviews.router, prefix="/api/v1")
app.include_router(news.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"name": settings.APP_NAME, "version": "0.1.0", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "ok"}
