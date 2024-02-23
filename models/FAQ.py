from typing import Optional, List

from beanie import Document, Link
from pydantic import BaseModel, EmailStr

class FAQ(Document):
    ques_title: Optional[str] = None
    ques_content: Optional[str] = None
    ques_time: Optional[int] = None
    ques_answer: Optional[str] = None
    
    
  
    class Settings:
        name = "FAQ"