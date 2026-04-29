-- ============================================
-- 爆单来 BaoDanLai — PostgreSQL 建表脚本
-- 使用前先创建数据库: CREATE DATABASE baodanlai;
-- ============================================

-- 用户表（兼容微信小程序 openid/unionid）
CREATE TABLE IF NOT EXISTS users (
    id            SERIAL PRIMARY KEY,
    nickname      VARCHAR(50)  NOT NULL,
    avatar_url    VARCHAR(500),
    phone         VARCHAR(20)  UNIQUE,
    wx_openid     VARCHAR(100) UNIQUE,
    wx_unionid    VARCHAR(100) UNIQUE,
    is_active     BOOLEAN      DEFAULT TRUE,
    created_at    TIMESTAMP    DEFAULT NOW(),
    updated_at    TIMESTAMP    DEFAULT NOW()
);

-- A股股票基本信息
CREATE TABLE IF NOT EXISTS stocks (
    id            SERIAL PRIMARY KEY,
    ts_code       VARCHAR(10)  UNIQUE NOT NULL,  -- 000001.SZ
    symbol        VARCHAR(6)   NOT NULL,          -- 000001
    name          VARCHAR(20)  NOT NULL,          -- 平安银行
    area          VARCHAR(20),                     -- 深圳
    industry      VARCHAR(20),                     -- 银行
    market        VARCHAR(10),                     -- 主板/创业板/科创板
    list_date     DATE,                            -- 上市日期
    is_active     BOOLEAN      DEFAULT TRUE,       -- 是否在市
    updated_at    TIMESTAMP    DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_stocks_symbol ON stocks(symbol);
CREATE INDEX IF NOT EXISTS idx_stocks_industry ON stocks(industry);

-- 日K线行情数据
CREATE TABLE IF NOT EXISTS stock_daily_quotes (
    id            SERIAL PRIMARY KEY,
    ts_code       VARCHAR(10)  NOT NULL,
    trade_date    DATE         NOT NULL,
    open          FLOAT,                           -- 开盘价
    high          FLOAT,                           -- 最高价
    low           FLOAT,                           -- 最低价
    close         FLOAT,                           -- 收盘价
    pre_close     FLOAT,                           -- 昨收价
    change_pct    FLOAT,                           -- 涨跌幅%
    vol           FLOAT,                           -- 成交量(手)
    amount        FLOAT,                           -- 成交额(千)
    turnover_rate FLOAT,                           -- 换手率%
    UNIQUE(ts_code, trade_date)
);
CREATE INDEX IF NOT EXISTS idx_quotes_ts_code ON stock_daily_quotes(ts_code);
CREATE INDEX IF NOT EXISTS idx_quotes_trade_date ON stock_daily_quotes(trade_date);

-- 财经新闻
CREATE TABLE IF NOT EXISTS news (
    id             SERIAL PRIMARY KEY,
    title          VARCHAR(200) NOT NULL,
    source         VARCHAR(50),                     -- 来源
    url            VARCHAR(500),                    -- 原文链接
    content        TEXT,                            -- 正文摘要
    importance     INTEGER      DEFAULT 3,          -- 重要度 1-5
    tags           VARCHAR(200),                    -- 标签，逗号分隔
    related_stocks VARCHAR(200),                    -- 关联股票代码
    published_at   TIMESTAMP,
    created_at     TIMESTAMP    DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_news_published ON news(published_at DESC);
CREATE INDEX IF NOT EXISTS idx_news_importance ON news(importance);

-- AI每日复盘报告
CREATE TABLE IF NOT EXISTS ai_reviews (
    id              SERIAL PRIMARY KEY,
    review_date     DATE         NOT NULL UNIQUE,   -- 复盘日期
    market_summary  TEXT,                            -- 大盘综述
    hot_sectors     TEXT,                            -- 热门板块 JSON
    risk_warning    TEXT,                            -- 风险提示
    strategy_advice TEXT,                            -- 操作建议
    raw_response    TEXT,                            -- AI原始响应
    model_name      VARCHAR(50),                    -- AI模型名
    created_at      TIMESTAMP    DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_reviews_date ON ai_reviews(review_date DESC);

-- 复盘中的个股点评
CREATE TABLE IF NOT EXISTS review_stock_picks (
    id            SERIAL PRIMARY KEY,
    review_id     INTEGER      NOT NULL REFERENCES ai_reviews(id) ON DELETE CASCADE,
    ts_code       VARCHAR(10)  NOT NULL,
    stock_name    VARCHAR(20)  NOT NULL,
    analysis      TEXT         NOT NULL,
    rating        VARCHAR(10),                     -- 看多/中性/看空
    reason_tags   VARCHAR(200),                    -- 原因标签
    created_at    TIMESTAMP    DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_picks_review ON review_stock_picks(review_id);
CREATE INDEX IF NOT EXISTS idx_picks_ts_code ON review_stock_picks(ts_code);

-- 用户自选股
CREATE TABLE IF NOT EXISTS watchlist (
    id            SERIAL PRIMARY KEY,
    user_id       INTEGER      NOT NULL,
    ts_code       VARCHAR(10)  NOT NULL,
    stock_name    VARCHAR(20)  NOT NULL,
    note          VARCHAR(200),
    created_at    TIMESTAMP    DEFAULT NOW(),
    UNIQUE(user_id, ts_code)
);
CREATE INDEX IF NOT EXISTS idx_watchlist_user ON watchlist(user_id);

-- ============================================
-- 初始数据：插入一个默认用户（开发阶段）
-- ============================================
INSERT INTO users (nickname, phone) VALUES ('测试用户', '13800138000')
    ON CONFLICT (phone) DO NOTHING;
