from beanie import Document
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class Event(Document):
    title: str
    image: str
    description: str
    tags: List[str]
    location: str
    creator: Optional[str] = None

    class Settings:
        name = "events"

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "title": "FastAPI Book Launch",
            "image": "https://linktomyimage.com/image.png",
            "description": "We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
            "tags": ["python", "fastapi", "book", "launch"],
            "location": "Google Meet"
        }
    })

class EventUpdate(BaseModel):
    title: Optional[str]
    image: Optional[str]
    description: Optional[str]
    tags: Optional[List[str]]
    location: Optional[str]

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "title": "FastAPI Book Launch",
            "image": "https://linktomyimage.com/image.png",
            "description": "We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
            "tags": ["python", "fastapi", "book", "launch"],
            "location": "Google Meet"
        }
    })