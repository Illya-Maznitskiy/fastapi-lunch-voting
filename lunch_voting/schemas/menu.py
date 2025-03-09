from pydantic import BaseModel
from datetime import date


# Schema for reading data (response model)
class MenuBase(BaseModel):
    name: str
    date: date
    restaurant_id: int


# Schema for creating a new Menu (request model)
class MenuCreate(MenuBase):
    pass


# Schema for the response model (when retrieving a Menu from DB)
class Menu(MenuBase):
    id: int

    class Config:
        orm_mode = True  # to tell Pydantic to convert from SQLAlchemy models
