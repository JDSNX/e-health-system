from typing import Any, Optional
from pydantic import BaseModel, field_validator
from time import time
from re import match, compile

STRONG_PASSWORD_PATTERN = compile(r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{6,128}$")


class ModuleResult(BaseModel):
    BLOOD_OXYGEN_LEVEL: Optional[str]
    BODY_TEMPERATURE: Optional[str]
    ECG_RESULT: Optional[str]


class Data(BaseModel):
    ref_id: Optional[str] = None
    first_name: str
    last_name: str
    middle_initial: Optional[str] = None
    emergency_contact_person: str
    emergency_contact_number: str
    result: Optional[ModuleResult] = None
    timestamp: Optional[str] = time()
    password: Optional[str] = None

    @field_validator("password", mode="after")
    @classmethod
    def valid_password(cls, password: str) -> str:
        if not match(STRONG_PASSWORD_PATTERN, password):
            raise ValueError(
                "Password must contain at least "
                "one lower character, "
                "one upper character, "
                "digit or "
                "special symbol"
            )

        return password
        
class Response(BaseModel):
    success: bool
    msg: Any[str, dict]
    timestamp: int