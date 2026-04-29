"""
复盘相关 Pydantic Schema
"""

from datetime import date
from pydantic import BaseModel


class AIReviewOut(BaseModel):
    id: int
    review_date: date
    market_summary: str | None = None
    hot_sectors: str | None = None
    risk_warning: str | None = None
    strategy_advice: str | None = None
    model_name: str | None = None
    created_at: str | None = None

    model_config = {"from_attributes": True}


class StockPickOut(BaseModel):
    ts_code: str
    stock_name: str
    analysis: str
    rating: str | None = None
    reason_tags: str | None = None

    model_config = {"from_attributes": True}


class ReviewDetailOut(BaseModel):
    """复盘报告详情（含个股点评）"""
    review: AIReviewOut
    picks: list[StockPickOut] = []
