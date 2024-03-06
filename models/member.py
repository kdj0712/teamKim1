from typing import Optional, List, Union

from beanie import Document, Link
from pydantic import BaseModel, EmailStr

class members(Document):
    user_ID: Optional[Union[str, int, float, bool]] = None
    user_pswd: Optional[Union[str, int, float, bool]] = None
    user_email: Optional[EmailStr] = None    
    user_name: Optional[Union[str, int, float, bool]] = None
    user_phone : Optional[Union[str, int, float, bool]] = None
    user_info : Optional[Union[str, int, float, bool]] = None
    user_birth : Optional[Union[str, int, float, bool]] = None
    user_postcode : Optional[Union[str, int, float, bool]] = None
    user_address : Optional[Union[str, int, float, bool]] = None
    user_detailed_address : Optional[Union[str, int, float, bool]] = None
    
  
    class Settings:
        name = "members"