from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.user import User  # Import the User model
from schemas.user import UserCreate, UserBase, UserUpdate  # Import the schemas

router = APIRouter()


# Create a new user (POST)
@router.post("/", response_model=UserBase)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user in the database.
    """
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered"
        )

    db_user = User(
        username=user.username, email=user.email, password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Get all users (GET)
@router.get("/", response_model=List[UserBase])
def get_users(db: Session = Depends(get_db)):
    """
    Get all users from the database.
    """
    users = db.query(User).all()
    return users


# Get a specific user by ID (GET)
@router.get("/{user_id}", response_model=UserBase)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a specific user by their ID.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Update an existing user (PUT)
@router.put("/{user_id}", response_model=UserBase)
def update_user(
    user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)
):
    """
    Update an existing user.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.username:
        db_user.username = user_update.username
    if user_update.email:
        db_user.email = user_update.email
    if user_update.password:
        db_user.password = (
            user_update.password
        )  # Note: Don't store plain passwords in real applications

    db.commit()
    db.refresh(db_user)
    return db_user


# Delete a user by ID (DELETE)
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user by their ID.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}
