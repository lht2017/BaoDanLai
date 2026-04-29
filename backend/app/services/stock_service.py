"""
股票服务层：行情查询、自选股管理
"""

from datetime import date

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.stock import Stock, StockDailyQuote
from app.models.review import Watchlist


async def search_stocks(db: AsyncSession, keyword: str, limit: int = 20) -> list[Stock]:
    """按代码或名称搜索股票"""
    stmt = (
        select(Stock)
        .where(Stock.is_active == True)
        .where(
            (Stock.symbol.contains(keyword)) | (Stock.name.contains(keyword))
        )
        .limit(limit)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_stock_daily(
    db: AsyncSession, ts_code: str, start_date: date | None = None, end_date: date | None = None, limit: int = 60
) -> list[StockDailyQuote]:
    """获取日K线数据"""
    stmt = (
        select(StockDailyQuote)
        .where(StockDailyQuote.ts_code == ts_code)
        .order_by(desc(StockDailyQuote.trade_date))
        .limit(limit)
    )
    if start_date:
        stmt = stmt.where(StockDailyQuote.trade_date >= start_date)
    if end_date:
        stmt = stmt.where(StockDailyQuote.trade_date <= end_date)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def add_to_watchlist(db: AsyncSession, user_id: int, ts_code: str, stock_name: str, note: str | None = None) -> Watchlist:
    """添加自选股"""
    item = Watchlist(user_id=user_id, ts_code=ts_code, stock_name=stock_name, note=note)
    db.add(item)
    await db.flush()
    return item


async def remove_from_watchlist(db: AsyncSession, user_id: int, ts_code: str) -> bool:
    """移除自选股"""
    stmt = select(Watchlist).where(Watchlist.user_id == user_id, Watchlist.ts_code == ts_code)
    result = await db.execute(stmt)
    item = result.scalar_one_or_none()
    if item:
        await db.delete(item)
        return True
    return False


async def get_watchlist(db: AsyncSession, user_id: int) -> list[Watchlist]:
    """获取用户自选股列表"""
    stmt = select(Watchlist).where(Watchlist.user_id == user_id).order_by(desc(Watchlist.created_at))
    result = await db.execute(stmt)
    return list(result.scalars().all())
