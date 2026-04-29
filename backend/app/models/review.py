"""
AI复盘报告模型
"""

from datetime import datetime, date
from sqlalchemy import String, Integer, Text, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class AIReview(Base):
    """AI每日复盘报告"""
    __tablename__ = "ai_reviews"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    review_date: Mapped[date] = mapped_column(Date, nullable=False, unique=True, comment="复盘日期")
    market_summary: Mapped[str | None] = mapped_column(Text, comment="大盘综述")
    hot_sectors: Mapped[str | None] = mapped_column(Text, comment="热门板块 JSON")
    risk_warning: Mapped[str | None] = mapped_column(Text, comment="风险提示")
    strategy_advice: Mapped[str | None] = mapped_column(Text, comment="操作建议")
    raw_response: Mapped[str | None] = mapped_column(Text, comment="AI原始响应")
    model_name: Mapped[str | None] = mapped_column(String(50), comment="使用的AI模型")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class ReviewStockPick(Base):
    """复盘中的个股点评"""
    __tablename__ = "review_stock_picks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    review_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="复盘报告ID")
    ts_code: Mapped[str] = mapped_column(String(10), nullable=False, comment="股票代码")
    stock_name: Mapped[str] = mapped_column(String(20), nullable=False, comment="股票名称")
    analysis: Mapped[str] = mapped_column(Text, nullable=False, comment="AI分析内容")
    rating: Mapped[str | None] = mapped_column(String(10), comment="评级 看多/中性/看空")
    reason_tags: Mapped[str | None] = mapped_column(String(200), comment="原因标签，逗号分隔")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Watchlist(Base):
    """用户自选股"""
    __tablename__ = "watchlist"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="用户ID")
    ts_code: Mapped[str] = mapped_column(String(10), nullable=False, comment="股票代码")
    stock_name: Mapped[str] = mapped_column(String(20), nullable=False, comment="股票名称")
    note: Mapped[str | None] = mapped_column(String(200), comment="备注")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    __table_args__ = (
        {"unique_together": [("user_id", "ts_code")]},
    )
