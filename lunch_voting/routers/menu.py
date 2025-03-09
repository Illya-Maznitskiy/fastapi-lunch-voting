from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.menu import Menu
from schemas.menu import (
    MenuCreate,
    Menu as MenuResponse,
)  # Import schemas and models

router = APIRouter()


# Create a new menu
@router.post("/menus/", response_model=MenuResponse)
def create_menu(menu: MenuCreate, db: Session = Depends(get_db)):
    # Create a new Menu object from the input schema
    db_menu = Menu(
        name=menu.name, date=menu.date, restaurant_id=menu.restaurant_id
    )

    # Add it to the session and commit
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)

    return db_menu


# Get all menus
@router.get("/menus/", response_model=List[MenuResponse])
def get_menus(db: Session = Depends(get_db)):
    menus = db.query(Menu).all()
    return menus


# Get a single menu by ID
@router.get("/menus/{menu_id}", response_model=MenuResponse)
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    return db_menu


# Update an existing menu
@router.put("/menus/{menu_id}", response_model=MenuResponse)
def update_menu(menu_id: int, menu: MenuCreate, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")

    db_menu.name = menu.name
    db_menu.date = menu.date
    db_menu.restaurant_id = menu.restaurant_id

    db.commit()
    db.refresh(db_menu)

    return db_menu


# Delete a menu
@router.delete("/menus/{menu_id}", response_model=MenuResponse)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")

    db.delete(db_menu)
    db.commit()

    return db_menu
