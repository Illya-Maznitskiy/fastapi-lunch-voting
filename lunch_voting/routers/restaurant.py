from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.restaurant import (
    Restaurant,
)  # Import the Restaurant model from models
from schemas.restaurant import (
    RestaurantCreate,
    RestaurantResponse,
)  # Correct import for the schema

router = APIRouter()


# Create a new restaurant (POST)
@router.post("/", response_model=RestaurantResponse)
def create_restaurant(
    restaurant: RestaurantCreate, db: Session = Depends(get_db)
):
    """
    Create a new restaurant in the database
    """
    db_restaurant = Restaurant(
        name=restaurant.name, location=restaurant.location
    )
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant


# Get all restaurants (GET)
@router.get("/", response_model=List[RestaurantResponse])
def get_restaurants(db: Session = Depends(get_db)):
    """
    Get all restaurants from the database
    """
    return db.query(Restaurant).all()


# Get a specific restaurant by ID (GET)
@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    """
    Get a specific restaurant by its ID
    """
    db_restaurant = (
        db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    )
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return db_restaurant


# Update an existing restaurant (PUT)
@router.put("/{restaurant_id}", response_model=RestaurantResponse)
def update_restaurant(
    restaurant_id: int,
    restaurant: RestaurantCreate,
    db: Session = Depends(get_db),
):
    """
    Update an existing restaurant
    """
    db_restaurant = (
        db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    )
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    db_restaurant.name = restaurant.name
    db_restaurant.location = restaurant.location
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant


# Delete a restaurant by ID (DELETE)
@router.delete("/{restaurant_id}")
def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    """
    Delete a restaurant by its ID
    """
    db_restaurant = (
        db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    )
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    db.delete(db_restaurant)
    db.commit()
    return {"message": "Restaurant deleted successfully"}
