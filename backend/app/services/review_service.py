"""
AI复盘服务层：生成/获取复盘报告
"""

from datetime import date

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.review import AIReview, ReviewStockPick
from app.schemas.review import AIReviewOut, StockPickOut, ReviewDetailOut


async def get_latest_review(db: AsyncSession) -> AIReview | None:
    """获取最新一期复盘报告"""
    stmt = select(AIReview).order_by(desc(AIReview.review_date)).limit(1)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_review_by_date(db: AsyncSession, review_date: date) -> AIReview | None:
    """按日期获取复盘报告"""
    stmt = select(AIReview).where(AIReview.review_date == review_date)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_review_picks(db: AsyncSession, review_id: int) -> list[ReviewStockPick]:
    """获取复盘报告中的个股点评"""
    stmt = select(ReviewStockPick).where(ReviewStockPick.review_id == review_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_review_detail(db: AsyncSession, review_date: date) -> ReviewDetailOut | None:
    """获取复盘详情（报告+个股点评）"""
    review = await get_review_by_date(db, review_date)
    if not review:
        return None
    picks = await get_review_picks(db, review.id)
    return ReviewDetailOut(
        review=AIReviewOut.model_validate(review),
        picks=[StockPickOut.model_validate(p) for p in picks],
    )


async def get_review_list(db: AsyncSession, limit: int = 30) -> list[AIReview]:
    """获取复盘报告列表"""
    stmt = select(AIReview).order_by(desc(AIReview.review_date)).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())
