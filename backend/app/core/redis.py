"""
爆单来 BaoDanLai — Redis 异步连接
用于缓存行情数据、限流、会话存储
"""

import redis.asyncio as aioredis

from app.core.config import get_settings

settings = get_settings()

redis_client: aioredis.Redis | None = None


async def get_redis() -> aioredis.Redis:
    """获取 Redis 客户端（全局单例）"""
    global redis_client
    if redis_client is None:
        redis_client = aioredis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            max_connections=20,
        )
    return redis_client


async def close_redis() -> None:
    """应用关闭时断开 Redis 连接"""
    global redis_client
    if redis_client is not None:
        await redis_client.close()
        redis_client = None
