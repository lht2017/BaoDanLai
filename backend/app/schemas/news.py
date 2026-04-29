"""
新闻相关 Pydantic Schema
"""

from datetime import datetime
from pydantic import BaseModel


class NewsOut(BaseModel):
    id: int
    title: str
    source: str | None = None
    url: str | None = None
    content: str | None = None
    importance: int = 3
    tags: str | None = None
    related_stocks: str | None = None
    published_at: datetime | None = None

    model_config = {"from_attributes": True}
