"""
新闻服务层
"""

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.news import News


async def get_news_list(
    db: AsyncSession,
    importance: int | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[News]:
    """获取新闻列表，可按重要度筛选"""
    stmt = select(News).order_by(desc(News.published_at)).offset(offset).limit(limit)
    if importance:
        stmt = stmt.where(News.importance >= importance)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_news_by_id(db: AsyncSession, news_id: int) -> News | None:
    """获取新闻详情"""
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
