"""
财经新闻/资讯模型
"""

from datetime import datetime
from sqlalchemy import String, Integer, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class News(Base):
    """财经新闻"""
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="标题")
    source: Mapped[str | None] = mapped_column(String(50), comment="来源")
    url: Mapped[str | None] = mapped_column(String(500), comment="原文链接")
    content: Mapped[str | None] = mapped_column(Text, comment="正文摘要")
    importance: Mapped[int] = mapped_column(Integer, default=3, comment="重要度 1-5")
    tags: Mapped[str | None] = mapped_column(String(200), comment="标签，逗号分隔")
    related_stocks: Mapped[str | None] = mapped_column(String(200), comment="关联股票代码，逗号分隔")
    published_at: Mapped[datetime | None] = mapped_column(DateTime, comment="发布时间")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
