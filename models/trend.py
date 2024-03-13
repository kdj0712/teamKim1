from typing import Optional, List

from beanie import Document, Link
from pydantic import BaseModel, EmailStr

class news_trends(Document):
    news_title: Optional[str] = None
    news_when: Optional[str] = None
    news_contents : Optional[str] = None
    news_url : Optional[str] = None

    class Settings:
        name = "trend_news"