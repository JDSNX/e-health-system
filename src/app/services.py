from uuid import uuid4
from requests import get
from time import time
from .config import settings, headers
from .schemas import Response

def generator():
    return uuid4().hex.upper()[0:5]

async def check_user(ref_id: int):
    try:
        resp = get(url=f"{settings.URL}/users/{ref_id}.json", headers=headers)

    except Exception as e:
        return Response(success=False, msg=e, timestamp=time())

    return Response(success=True, msg=resp.json(), timestamp=time())