"""
新闻相关 API 路由
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.news import NewsOut
from app.services import news_service

router = APIRouter(prefix="/news", tags=["新闻"])


@router.get("/", response_model=list[NewsOut])
async def get_list(
    importance: int | None = Query(default=None, ge=1, le=5),
    limit: int = Query(default=50, le=200),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """获取新闻列表"""
    return await news_service.get_news_list(db, importance, limit, offset)


@router.get("/{news_id}", response_model=NewsOut | None)
async def get_detail(news_id: int, db: AsyncSession = Depends(get_db)):
    """获取新闻详情"""
    return await news_service.get_news_by_id(db, news_id)
