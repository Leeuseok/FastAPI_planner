from pydantic import BaseModel, EmailStr
from typing import Optional, List
from models.events import Event

class User(BaseModel):
    email:EmailStr
    username: str
    password: str
    events: Optional[List[Event]] = None

    class Config:
        schema_extra = {
            "example": {
                "email" : "fastapi@packt.com",
                "username": "FastPackt",
                "password": "strong!!!",
                "events": [],
            }
        }

class UserSignIn(BaseModel):
    email: EmailStr
    password : str

    class Config:
        schema_extra = {
            "example" : {
                "email": "fastapi@packt.com",
                "password": "strong!!!"
            }
        }

