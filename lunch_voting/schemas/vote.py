from pydantic import BaseModel
from datetime import datetime


# Pydantic schema for vote creation (POST request)
class VoteCreate(BaseModel):
    user_id: int
    menu_id: int

    class Config:
        orm_mode = (
            True  # This tells Pydantic to treat SQLAlchemy models as dicts.
        )


# Pydantic schema for vote read (GET request)
class VoteBase(BaseModel):
    id: int
    user_id: int
    menu_id: int
    created_at: datetime

    class Config:
        orm_mode = (
            True  # This tells Pydantic to treat SQLAlchemy models as dicts.
        )
