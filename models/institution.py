from typing import Optional, List

from beanie import Document, Link
from pydantic import BaseModel, EmailStr

class Institutions(Document):
    hospital_name: Optional[str] = None
    hospital_address: Optional[str] = None
    hospital_phone: Optional[int] = None
    hospital_info: Optional[str] = None
    hospital_page : Optional[str] = None
    
  
    class Settings:
        name = "Institutions"