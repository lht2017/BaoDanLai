"""
股票相关 Pydantic Schema（请求/响应模型）
"""

from datetime import date
from pydantic import BaseModel


# ── 股票基础 ──

class StockOut(BaseModel):
    id: int
    ts_code: str
    symbol: str
    name: str
    industry: str | None = None
    market: str | None = None
    list_date: date | None = None

    model_config = {"from_attributes": True}


class StockDailyOut(BaseModel):
    ts_code: str
    trade_date: date
    open: float
    high: float
    low: float
    close: float
    pre_close: float | None = None
    change_pct: float | None = None
    vol: float | None = None
    amount: float | None = None

    model_config = {"from_attributes": True}


# ── 自选股 ──

class WatchlistAdd(BaseModel):
    ts_code: str
    stock_name: str
    note: str | None = None


class WatchlistOut(BaseModel):
    id: int
    ts_code: str
    stock_name: str
    note: str | None = None
    created_at: str | None = None

    model_config = {"from_attributes": True}
