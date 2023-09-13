from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from src.app.users.services import create, get_all_user, get_user_by_id, update
from src.app.database.core import get_db
from src.app.schemas import Payload, SMSCreate
from src.app.config import settings
from time import time
from requests import request
from json import dumps


router = APIRouter(prefix="/sms", tags=["Users"])

@router.post("/")
async def send_sms(sms: SMSCreate):
    try:
        payload = Payload(
            message=sms.message,
            number=sms.number,
            api_key=settings.SMS_API_KEY
        )

        response = request('POST', settings.SMS_URL, data = payload)
    except Exception as e:
        return {"success": False, "msg": e, "timestamp": time()}
    
    return {"success": True, "result": dumps(response.text, indent=4), "timestamp": time()}