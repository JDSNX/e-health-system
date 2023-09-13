from pydantic import BaseModel
from time import time
    
class Payload(BaseModel):
    message: str
    number: str
    api_key: str


class SMSCreate(BaseModel):
    message: str
    number: str