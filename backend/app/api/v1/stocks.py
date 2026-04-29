"""
股票相关 API 路由
"""

from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.stock import StockOut, StockDailyOut, WatchlistAdd, WatchlistOut
from app.services import stock_service

router = APIRouter(prefix="/stocks", tags=["股票"])


@router.get("/search", response_model=list[StockOut])
async def search(keyword: str = Query(..., min_length=1), db: AsyncSession = Depends(get_db)):
    """搜索股票（按代码或名称）"""
    stocks = await stock_service.search_stocks(db, keyword)
    return stocks


@router.get("/{ts_code}/daily", response_model=list[StockDailyOut])
async def get_daily(
    ts_code: str,
    start_date: date | None = None,
    end_date: date | None = None,
    limit: int = Query(default=60, le=250),
    db: AsyncSession = Depends(get_db),
):
    """获取个股日K线数据"""
    return await stock_service.get_stock_daily(db, ts_code, start_date, end_date, limit)


@router.post("/watchlist", response_model=WatchlistOut)
async def add_watchlist(item: WatchlistAdd, db: AsyncSession = Depends(get_db)):
    """添加自选股（user_id 后期从 JWT 获取，暂用默认值 1）"""
    return await stock_service.add_to_watchlist(db, user_id=1, ts_code=item.ts_code, stock_name=item.stock_name, note=item.note)


@router.get("/watchlist", response_model=list[WatchlistOut])
async def get_watchlist(db: AsyncSession = Depends(get_db)):
    """获取自选股列表"""
    return await stock_service.get_watchlist(db, user_id=1)


@router.delete("/watchlist/{ts_code}")
async def remove_watchlist(ts_code: str, db: AsyncSession = Depends(get_db)):
    """移除自选股"""
    ok = await stock_service.remove_from_watchlist(db, user_id=1, ts_code=ts_code)
    return {"success": ok}
