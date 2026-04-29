"""
股票基础信息模型
"""

from datetime import datetime, date
from sqlalchemy import String, Integer, BigInteger, Float, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Stock(Base):
    """A股股票基本信息"""
    __tablename__ = "stocks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ts_code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, comment="TS代码 000001.SZ")
    symbol: Mapped[str] = mapped_column(String(6), nullable=False, comment="股票代码 000001")
    name: Mapped[str] = mapped_column(String(20), nullable=False, comment="股票名称")
    area: Mapped[str | None] = mapped_column(String(20), comment="地域")
    industry: Mapped[str | None] = mapped_column(String(20), comment="所属行业")
    market: Mapped[str | None] = mapped_column(String(10), comment="市场类型 主板/创业板/科创板")
    list_date: Mapped[date | None] = mapped_column(Date, comment="上市日期")
    is_active: Mapped[bool] = mapped_column(default=True, comment="是否在市")
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class StockDailyQuote(Base):
    """日K线行情数据"""
    __tablename__ = "stock_daily_quotes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ts_code: Mapped[str] = mapped_column(String(10), nullable=False, index=True, comment="TS代码")
    trade_date: Mapped[date] = mapped_column(nullable=False, index=True, comment="交易日期")
    open: Mapped[float] = mapped_column(Float, comment="开盘价")
    high: Mapped[float] = mapped_column(Float, comment="最高价")
    low: Mapped[float] = mapped_column(Float, comment="最低价")
    close: Mapped[float] = mapped_column(Float, comment="收盘价")
    pre_close: Mapped[float | None] = mapped_column(Float, comment="昨收价")
    change_pct: Mapped[float | None] = mapped_column(Float, comment="涨跌幅%")
    vol: Mapped[float | None] = mapped_column(Float, comment="成交量(手)")
    amount: Mapped[float | None] = mapped_column(Float, comment="成交额(千)")
    turnover_rate: Mapped[float | None] = mapped_column(Float, comment="换手率%")

    __table_args__ = (
        # 同一股票同一日期只有一条记录
        {"unique_together": [("ts_code", "trade_date")]},
    )
