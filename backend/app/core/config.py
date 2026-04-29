"""
爆单来 BaoDanLai — 全局配置管理
使用 pydantic-settings 从 .env 加载配置，支持类型校验和环境变量覆盖
"""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 应用
    APP_NAME: str = "爆单来"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_PORT: int = 8000
    APP_SECRET_KEY: str = "change-me"

    # PostgreSQL
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "baodanlai"
    POSTGRES_PASSWORD: str = "baodanlai_dev_2026"
    POSTGRES_DB: str = "baodanlai"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    REDIS_DB: int = 0

    # AI 服务
    AI_API_KEY: str = ""
    AI_API_BASE: str = "https://api.deepseek.com/v1"
    AI_MODEL: str = "deepseek-chat"

    # 数据源
    TUSHARE_TOKEN: str = ""

    # 爬虫
    CRAWLER_REQUEST_DELAY: float = 0.5

    # 日志
    LOG_LEVEL: str = "INFO"

    @property
    def DATABASE_URL(self) -> str:
        """异步 PostgreSQL 连接串"""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def DATABASE_URL_SYNC(self) -> str:
        """同步连接串（Alembic 迁移用）"""
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def REDIS_URL(self) -> str:
        pwd = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
        return f"redis://{pwd}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


@lru_cache
def get_settings() -> Settings:
    """全局单例，整个应用共享同一份配置"""
    return Settings()
