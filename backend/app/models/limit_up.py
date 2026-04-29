"""
涨停股 & 市场情绪 ORM 模型
"""

from datetime import datetime, date, time
from sqlalchemy import String, Integer, Float, Date, Time, Boolean, Text, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class LimitUpStock(Base):
    """每日涨停股明细"""
    __tablename__ = "limit_up_stocks"
    __table_args__ = (
        UniqueConstraint("ts_code", "trade_date", name="uq_limitup_code_date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    trade_date: Mapped[date] = mapped_column(Date, nullable=False, index=True, comment="交易日期")
    ts_code: Mapped[str] = mapped_column(String(10), nullable=False, index=True, comment="TS代码")
    stock_name: Mapped[str] = mapped_column(String(20), nullable=False, comment="股票名称")
    limit_up_time: Mapped[time | None] = mapped_column(Time, comment="最后涨停时间")
    limit_up_price: Mapped[float | None] = mapped_column(Float, comment="涨停价")
    consecutive_boards: Mapped[int] = mapped_column(Integer, default=1, comment="连板数")
    is_broken: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否炸板")
    turnover_rate: Mapped[float | None] = mapped_column(Float, comment="换手率%")
    float_market_cap: Mapped[float | None] = mapped_column(Float, comment="流通市值(亿)")
    amount: Mapped[float | None] = mapped_column(Float, comment="成交额(亿)")
    concepts: Mapped[str | None] = mapped_column(Text, comment="所属概念，逗号分隔")
    is_st: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否ST")
    first_limit_up_time: Mapped[time | None] = mapped_column(Time, comment="首次涨停时间")
    limit_up_count: Mapped[int | None] = mapped_column(Integer, comment="涨停封单数(手)")
    last_price: Mapped[float | None] = mapped_column(Float, comment="最新价")
    change_pct: Mapped[float | None] = mapped_column(Float, comment="涨跌幅%")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class MarketSentiment(Base):
    """每日市场情绪指标"""
    __tablename__ = "market_sentiment"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    trade_date: Mapped[date] = mapped_column(Date, nullable=False, unique=True, comment="交易日期")
    up_count: Mapped[int] = mapped_column(Integer, default=0, comment="上涨家数")
    down_count: Mapped[int] = mapped_column(Integer, default=0, comment="下跌家数")
    flat_count: Mapped[int] = mapped_column(Integer, default=0, comment="平盘家数")
    limit_up_count: Mapped[int] = mapped_column(Integer, default=0, comment="涨停家数")
    limit_down_count: Mapped[int] = mapped_column(Integer, default=0, comment="跌停家数")
    broken_board_rate: Mapped[float] = mapped_column(Float, default=0.0, comment="炸板率%")
    max_consecutive: Mapped[int] = mapped_column(Integer, default=0, comment="最高连板")
    hot_sectors: Mapped[str | None] = mapped_column(Text, comment="热门板块，逗号分隔")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
