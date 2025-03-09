from pydantic import BaseModel
from typing import Optional


# Pydantic schema for user creation (POST request)
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        orm_mode = (
            True  # This tells Pydantic to treat SQLAlchemy models as dicts.
        )


# Pydantic schema for user read (GET request)
class UserBase(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = (
            True  # This tells Pydantic to treat SQLAlchemy models as dicts.
        )


# Pydantic schema for user update (optional)
class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]

    class Config:
        orm_mode = True
