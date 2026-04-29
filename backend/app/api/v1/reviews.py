"""
AI复盘相关 API 路由
"""

from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.review import AIReviewOut, ReviewDetailOut
from app.services import review_service

router = APIRouter(prefix="/reviews", tags=["AI复盘"])


@router.get("/latest", response_model=AIReviewOut | None)
async def get_latest(db: AsyncSession = Depends(get_db)):
    """获取最新一期复盘报告"""
    return await review_service.get_latest_review(db)


@router.get("/list", response_model=list[AIReviewOut])
async def get_list(limit: int = Query(default=30, le=100), db: AsyncSession = Depends(get_db)):
    """获取复盘报告列表"""
    return await review_service.get_review_list(db, limit)


@router.get("/{review_date}", response_model=ReviewDetailOut | None)
async def get_detail(review_date: date, db: AsyncSession = Depends(get_db)):
    """获取指定日期的复盘详情（含个股点评）"""
    return await review_service.get_review_detail(db, review_date)
