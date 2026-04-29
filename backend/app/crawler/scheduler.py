"""
定时任务调度器 — 每天 15:30 自动执行涨停股爬虫

使用方式:
  1. 手动执行（立即爬一次）:
     cd backend && python -m app.crawler.scheduler

  2. 定时模式（每天 15:30）:
     cd backend && python -m app.crawler.scheduler --schedule

  3. 指定日期:
     cd backend && python -m app.crawler.scheduler --date 2026-04-28

  4. crontab 方式:
     30 15 * * 1-5 cd /path/to/backend && python -m app.crawler.scheduler
"""

import argparse
import sys
import time
from datetime import date, datetime

from loguru import logger

# 配置日志格式
logger.remove()
logger.add(sys.stderr, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{level:<7}</level> | {message}")


def run_daily(target_date: date | None = None) -> None:
    """执行每日爬取任务"""
    from app.crawler.limit_up import crawl_limit_up

    try:
        crawl_limit_up(target_date)
    except Exception as e:
        logger.exception(f"爬取任务异常: {e}")
        raise


def run_scheduled() -> None:
    """启动定时调度，每天 15:30 执行"""
    try:
        import schedule
    except ImportError:
        logger.error("需要安装 schedule: pip install schedule")
        sys.exit(1)

    schedule_time = "15:30"
    logger.info(f"定时调度已启动，每天 {schedule_time} 执行涨停股爬虫")

    # 首次立即执行一次
    run_daily()

    schedule.every().day.at(schedule_time).do(run_daily)

    while True:
        schedule.run_pending()
        time.sleep(30)


def main() -> None:
    parser = argparse.ArgumentParser(description="爆单来 — 涨停股爬虫调度器")
    parser.add_argument("--schedule", action="store_true", help="启动定时模式（每天 15:30）")
    parser.add_argument("--date", type=str, default=None, help="指定爬取日期 (YYYY-MM-DD)")
    args = parser.parse_args()

    target_date = None
    if args.date:
        try:
            target_date = date.fromisoformat(args.date)
        except ValueError:
            logger.error(f"日期格式错误: {args.date}，应为 YYYY-MM-DD")
            sys.exit(1)

    if args.schedule:
        run_scheduled()
    else:
        run_daily(target_date)


if __name__ == "__main__":
    main()
