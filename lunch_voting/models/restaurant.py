from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from lunch_voting.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String, index=True)

    menus = relationship("Menu", back_populates="restaurant")
