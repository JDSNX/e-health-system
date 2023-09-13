from pydantic import BaseModel
from time import time
    
class Response(BaseModel):
    success: bool
    msg: str
    timestamp: int


class UserBase(BaseModel):    
    full_name: str
    emergency_contact_person: str
    emergency_contact_number: str
    password: str

class UserUpdate(UserBase):
    pass

class UserCreate(UserBase):
    pass

class User(UserBase):
    pass
