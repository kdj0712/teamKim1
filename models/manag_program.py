from typing import Optional, List

from beanie import Document, Link
from pydantic import BaseModel, Field, File
from datetime import datetime

class program(Document):
    program_title: Optional[str] = None
    program_date: Optional[datetime] = None
    program_thumbnail: Optional[File] = Field(alias="program_thumbnail")
    program_content: Optional[File] = Field(alias="program_content")
  
    class Settings:
        name = "manag_program"