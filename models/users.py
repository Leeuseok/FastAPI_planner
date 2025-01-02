from pydantic import BaseModel, EmailStr, ConfigDict
from beanie import Document
from typing import Optional, List
from models.events import Event

class User(Document):
    email: EmailStr
    password: str
    username: str
    events: Optional[List[Event]] = None

    class Settings:
        name = "users"

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "email": "fastapi@packt.com",
            "username": "FastPackt",
            "password": "strong!!!",
            "events": [],
        }
    })

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "access_token": "example_token_value",
            "token_type": "bearer"
        }
    })