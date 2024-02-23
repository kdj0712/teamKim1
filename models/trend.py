from typing import Optional, List

from beanie import Document, Link
from pydantic import BaseModel, EmailStr

class trends(Document):
    trend_title: Optional[str] = None
    trend_content: Optional[str] = None
  
    class Settings:
        name = "trends"