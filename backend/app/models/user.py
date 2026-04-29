"""
用户模型
字段设计兼容后期微信小程序迁移（openid / unionid）
"""

from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nickname: Mapped[str] = mapped_column(String(50), nullable=False, comment="昵称")
    avatar_url: Mapped[str | None] = mapped_column(String(500), comment="头像URL")
    phone: Mapped[str | None] = mapped_column(String(20), unique=True, comment="手机号")

    # 微信小程序预留字段
    wx_openid: Mapped[str | None] = mapped_column(String(100), unique=True, comment="微信openid")
    wx_unionid: Mapped[str | None] = mapped_column(String(100), unique=True, comment="微信unionid")

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
