"""
涨停股数据爬虫 — akshare + 东方财富接口
主数据源: akshare.stock_zt_pool_em（稳定、免登录）
辅助接口: 东方财富市场概况（涨跌家数）
功能：抓取涨停股明细 + 市场情绪指标，存入 PostgreSQL
"""

import re
import time
from datetime import date, time as dt_time

import akshare as ak
from loguru import logger
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.core.config import get_settings

settings = get_settings()

# 东方财富沪深指数接口（获取涨跌家数）
INDEX_URL = "https://push2.eastmoney.com/api/qt/ulist.np/get"
INDEX_PARAMS = {
    "ut": "bd1d9ddb04089700cf9c27f6f7426281",
    "fltt": "2",
    "secids": "1.000001,0.399001",  # 上证指数 + 深证成指
    "fields": "f104,f105,f106,f152",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}


def _parse_ts_code(raw_code: str) -> str:
    """将 akshare 6位代码转为 TS 标准格式: 000001.SZ / 600519.SH / 300750.SZ"""
    code = raw_code.strip()
    if len(code) != 6:
        return code
    if code.startswith(("6", "9")):
        return f"{code}.SH"
    elif code.startswith(("4", "8")):
        return f"{code}.BJ"
    return f"{code}.SZ"


def _parse_time_str(raw) -> dt_time | None:
    """解析涨停时间 -> time 对象
    支持 '092500' / '09:25:00' / 整数 92500 等格式
    """
    if raw is None or raw == "" or raw == "None":
        return None
    s = str(raw).strip().replace(":", "")
    if len(s) >= 6:
        try:
            return dt_time(int(s[0:2]), int(s[2:4]), int(s[4:6]))
        except (ValueError, OverflowError):
            return None
    return None


def _is_st(name: str) -> bool:
    return bool(re.search(r"ST|退", name, re.IGNORECASE))


def fetch_limit_up_pool(date_str: str | None = None) -> list[dict]:
    """通过 akshare 抓取涨停股池
    date_str: 日期字符串 YYYYMMDD，None 表示当天实时数据
    """
    logger.info("开始抓取涨停股池 (akshare)...")

    for attempt in range(1, 4):
        try:
            if date_str:
                df = ak.stock_zt_pool_em(date=date_str)
            else:
                df = ak.stock_zt_pool_em(date=date.today().strftime("%Y%m%d"))

            if df is None or df.empty:
                logger.warning(f"涨停股池为空 (attempt {attempt}/3)")
                time.sleep(settings.CRAWLER_REQUEST_DELAY * 3)
                continue

            logger.info(f"涨停股池返回 {len(df)} 条")
            results = []
            for _, row in df.iterrows():
                try:
                    raw_code = str(row.get("代码", "")).strip()
                    if not raw_code:
                        continue

                    # 换手率
                    turnover = row.get("换手率")
                    if turnover is not None:
                        turnover = round(float(turnover), 2)

                    # 流通市值 (元 -> 亿)
                    fmc = row.get("流通市值")
                    if fmc is not None:
                        fmc = round(float(fmc) / 1e8, 2)
                    else:
                        fmc = None

                    # 成交额 (元 -> 亿)
                    amt = row.get("成交额")
                    if amt is not None:
                        amt = round(float(amt) / 1e8, 2)
                    else:
                        amt = None

                    # 涨停价 = 最新价 (涨停股)
                    price = row.get("最新价")
                    if price is not None:
                        price = round(float(price), 2)
                    else:
                        price = None

                    # 涨跌幅
                    pct = row.get("涨跌幅")
                    if pct is not None:
                        pct = round(float(pct), 2)
                    else:
                        pct = None

                    # 封板资金 (元 -> 万)
                    fund = row.get("封板资金")
                    if fund is not None:
                        fund = round(float(fund) / 1e4, 0)
                    else:
                        fund = None

                    # 连板数
                    lb = row.get("连板数")
                    if lb is not None:
                        lb = int(float(lb))
                    else:
                        lb = 1

                    # 炸板次数
                    broken_times = row.get("炸板次数")
                    if broken_times is not None:
                        broken_times = int(float(broken_times))
                    else:
                        broken_times = 0

                    results.append({
                        "ts_code": _parse_ts_code(raw_code),
                        "stock_name": str(row.get("名称", "")).strip(),
                        "limit_up_price": price,
                        "last_price": price,
                        "change_pct": pct,
                        "consecutive_boards": lb,
                        "first_limit_up_time": _parse_time_str(row.get("首次封板时间")),
                        "limit_up_time": _parse_time_str(row.get("最后封板时间")),
                        "turnover_rate": turnover,
                        "float_market_cap": fmc,
                        "amount": amt,
                        "is_broken": broken_times > 0,
                        "limit_up_count": int(fund) if fund else None,
                        "is_st": _is_st(str(row.get("名称", ""))),
                        "industry": str(row.get("所属行业", "")) if row.get("所属行业") else "",
                    })
                except (ValueError, TypeError) as e:
                    logger.warning(f"解析涨停股失败: {raw_code} {e}")

            return results

        except Exception as e:
            logger.warning(f"akshare 涨停池请求失败 (attempt {attempt}/3): {e}")
            time.sleep(settings.CRAWLER_REQUEST_DELAY * 3)

    logger.error("涨停股池最终获取失败")
    return []


def fetch_market_overview() -> dict:
    """抓取市场概况：通过东方财富指数接口获取涨跌家数
    如果远程连接被拒，返回空 dict（主流程会用涨停池数据推算）
    """
    logger.info("开始抓取市场概况...")

    import requests
    for attempt in range(1, 4):
        try:
            resp = requests.get(
                INDEX_URL, params=INDEX_PARAMS,
                headers={**HEADERS, "Referer": "https://quote.eastmoney.com/"},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            diff = data.get("data", {}).get("diff", [])
            if not diff:
                logger.warning(f"市场概况返回空数据 (attempt {attempt}/3)")
                time.sleep(settings.CRAWLER_REQUEST_DELAY * 2)
                continue

            up = down = flat = 0
            for item in diff:
                up += int(item.get("f105", 0) or 0)
                down += int(item.get("f106", 0) or 0)
                flat += int(item.get("f152", 0) or 0)

            result = {
                "up_count": up,
                "down_count": down,
                "flat_count": flat,
            }
            logger.info(f"市场概况: 上涨 {up} / 下跌 {down} / 平盘 {flat}")
            return result

        except Exception as e:
            logger.warning(f"市场概况请求失败 (attempt {attempt}/3): {e}")
            time.sleep(settings.CRAWLER_REQUEST_DELAY * 3)

    logger.warning("市场概况获取失败，将从涨停池数据推算")
    return {}


def fetch_broken_pool(date_str: str | None = None) -> int:
    """抓取炸板池（含炸板次数的涨停股），返回炸板股数量"""
    logger.info("开始抓取炸板池...")

    for attempt in range(1, 4):
        try:
            if date_str:
                df = ak.stock_zt_pool_dtgc_em(date=date_str)
            else:
                df = ak.stock_zt_pool_dtgc_em(date=date.today().strftime("%Y%m%d"))

            if df is None or df.empty:
                return 0

            count = len(df)
            logger.info(f"炸板池: {count} 只")
            return count

        except Exception as e:
            logger.warning(f"炸板池请求失败 (attempt {attempt}/3): {e}")
            time.sleep(settings.CRAWLER_REQUEST_DELAY * 3)

    return 0


def save_to_db(trade_date: date, limit_up_stocks: list[dict], market_data: dict) -> None:
    """将数据写入 PostgreSQL（同步方式，适合爬虫场景）"""
    from app.models.limit_up import LimitUpStock, MarketSentiment

    engine = create_engine(settings.DATABASE_URL_SYNC, echo=False)
    with Session(engine) as session:
        # 1) 写入涨停股明细（upsert: 已存在则更新）
        saved_count = 0
        for stock in limit_up_stocks:
            stmt = select(LimitUpStock).where(
                LimitUpStock.ts_code == stock["ts_code"],
                LimitUpStock.trade_date == trade_date,
            )
            existing = session.scalar(stmt)
            if existing:
                # 更新关键字段
                existing.stock_name = stock.get("stock_name", existing.stock_name)
                existing.limit_up_price = stock.get("limit_up_price")
                existing.last_price = stock.get("last_price")
                existing.change_pct = stock.get("change_pct")
                existing.consecutive_boards = stock.get("consecutive_boards", 1)
                existing.is_broken = stock.get("is_broken", False)
                existing.turnover_rate = stock.get("turnover_rate")
                existing.float_market_cap = stock.get("float_market_cap")
                existing.amount = stock.get("amount")
                existing.concepts = stock.get("concepts", "")
                existing.limit_up_time = stock.get("limit_up_time")
                existing.first_limit_up_time = stock.get("first_limit_up_time")
                existing.limit_up_count = stock.get("limit_up_count")
                logger.debug(f"更新已存在: {stock['ts_code']} {trade_date}")
            else:
                row = LimitUpStock(
                    trade_date=trade_date,
                    ts_code=stock["ts_code"],
                    stock_name=stock["stock_name"],
                    limit_up_time=stock.get("limit_up_time"),
                    limit_up_price=stock.get("limit_up_price"),
                    consecutive_boards=stock.get("consecutive_boards", 1),
                    is_broken=stock.get("is_broken", False),
                    turnover_rate=stock.get("turnover_rate"),
                    float_market_cap=stock.get("float_market_cap"),
                    amount=stock.get("amount"),
                    concepts=stock.get("concepts", ""),
                    is_st=stock.get("is_st", False),
                    first_limit_up_time=stock.get("first_limit_up_time"),
                    limit_up_count=stock.get("limit_up_count"),
                    last_price=stock.get("last_price"),
                    change_pct=stock.get("change_pct"),
                )
                session.add(row)
                saved_count += 1

        logger.info(f"涨停股明细: 新增 {saved_count} 条")

        # 2) 写入/更新市场情绪
        if market_data:
            stmt = select(MarketSentiment).where(MarketSentiment.trade_date == trade_date)
            existing_sent = session.scalar(stmt)
            if existing_sent:
                for k, v in market_data.items():
                    setattr(existing_sent, k, v)
                logger.info(f"市场情绪: 更新 {trade_date}")
            else:
                sent = MarketSentiment(trade_date=trade_date, **market_data)
                session.add(sent)
                logger.info(f"市场情绪: 新增 {trade_date}")

        session.commit()
    engine.dispose()
    logger.info("数据库写入完成")


def crawl_limit_up(trade_date: date | None = None) -> None:
    """涨停股爬虫主流程

    流程: 市场概况 → 涨停股池 → 炸板池 → 计算指标 → 入库
    """
    if trade_date is None:
        trade_date = date.today()
    date_str = trade_date.strftime("%Y%m%d")

    logger.info(f"===== 开始爬取涨停数据: {trade_date} ({date_str}) =====")

    # 1. 抓取市场概况（涨跌家数）
    market_data = fetch_market_overview()

    # 2. 抓取涨停股池
    limit_up_stocks = fetch_limit_up_pool(date_str)

    if not limit_up_stocks:
        logger.warning("涨停股池为空，跳过后续步骤")
        # 仍然写入市场概况数据
        if market_data:
            market_data["limit_up_count"] = 0
            market_data["limit_down_count"] = 0
            market_data["broken_board_rate"] = 0.0
            market_data["max_consecutive"] = 0
            save_to_db(trade_date, [], market_data)
        return

    # 3. 抓取炸板池
    broken_count = fetch_broken_pool(date_str)
    total = len(limit_up_stocks) + broken_count

    # 4. 计算市场指标
    max_board = max((s["consecutive_boards"] for s in limit_up_stocks), default=0)
    industry_freq: dict[str, int] = {}
    for s in limit_up_stocks:
        ind = s.get("industry", "")
        if ind:
            industry_freq[ind] = industry_freq.get(ind, 0) + 1
    hot_sectors = ",".join(
        k for k, _ in sorted(industry_freq.items(), key=lambda x: x[1], reverse=True)[:5]
    )

    market_data["limit_up_count"] = len(limit_up_stocks)
    market_data["limit_down_count"] = 0  # akshare 不直接提供，后续可补充
    market_data["broken_board_rate"] = round(broken_count / total * 100, 2) if total > 0 else 0.0
    market_data["max_consecutive"] = max_board
    market_data["hot_sectors"] = hot_sectors

    logger.info(f"指标计算: 涨停 {len(limit_up_stocks)}, 炸板 {broken_count}, "
                f"炸板率 {market_data['broken_board_rate']}%, 最高连板 {max_board}")

    # 5. 写入数据库
    save_to_db(trade_date, limit_up_stocks, market_data)

    logger.info(f"===== 爬取完成 =====")
