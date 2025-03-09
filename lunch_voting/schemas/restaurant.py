from pydantic import BaseModel
from typing import List


# Define the Menu schema first
class Menu(BaseModel):
    name: str
    date: str

    class Config:
        orm_mode = True


# Restaurant schema
class RestaurantBase(BaseModel):
    name: str
    location: str


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantResponse(RestaurantBase):
    id: int
    menus: List[Menu]  # Directly use the Menu class here

    class Config:
        orm_mode = True


# Now, we don't need to call `update_forward_refs()` in this case because the Menu class is already defined above.
