-- ============================================
-- 涨停股 & 市场情绪 建表脚本
-- 在现有数据库上追加执行即可
-- ============================================

-- 每日涨停股明细
CREATE TABLE IF NOT EXISTS limit_up_stocks (
    id                  SERIAL PRIMARY KEY,
    trade_date          DATE         NOT NULL,
    ts_code             VARCHAR(10)  NOT NULL,
    stock_name          VARCHAR(20)  NOT NULL,
    limit_up_time       TIME,
    limit_up_price      FLOAT,
    consecutive_boards  INTEGER      DEFAULT 1,
    is_broken           BOOLEAN      DEFAULT FALSE,
    turnover_rate       FLOAT,
    float_market_cap    FLOAT,
    amount              FLOAT,
    concepts            TEXT,
    is_st               BOOLEAN      DEFAULT FALSE,
    first_limit_up_time TIME,
    limit_up_count      INTEGER,
    last_price          FLOAT,
    change_pct          FLOAT,
    created_at          TIMESTAMP    DEFAULT NOW(),
    UNIQUE(ts_code, trade_date)
);
CREATE INDEX IF NOT EXISTS idx_limitup_date ON limit_up_stocks(trade_date);
CREATE INDEX IF NOT EXISTS idx_limitup_code ON limit_up_stocks(ts_code);
CREATE INDEX IF NOT EXISTS idx_limitup_boards ON limit_up_stocks(consecutive_boards);

-- 每日市场情绪
CREATE TABLE IF NOT EXISTS market_sentiment (
    id                  SERIAL PRIMARY KEY,
    trade_date          DATE         NOT NULL UNIQUE,
    up_count            INTEGER      DEFAULT 0,
    down_count          INTEGER      DEFAULT 0,
    flat_count          INTEGER      DEFAULT 0,
    limit_up_count      INTEGER      DEFAULT 0,
    limit_down_count    INTEGER      DEFAULT 0,
    broken_board_rate   FLOAT        DEFAULT 0.0,
    max_consecutive     INTEGER      DEFAULT 0,
    hot_sectors         TEXT,
    created_at          TIMESTAMP    DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_sentiment_date ON market_sentiment(trade_date);
