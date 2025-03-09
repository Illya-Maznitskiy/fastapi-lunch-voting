from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.user import User  # Import the User model
from schemas.user import UserCreate, UserBase, UserUpdate  # Import the schemas
from utils.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)  # Import auth functions

router = APIRouter()


# Create a new user (POST)
@router.post("/users/", response_model=UserBase)
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
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Get all users (GET) - This should be a protected route
@router.get("/users/", response_model=List[UserBase])
def get_users(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Get all users from the database.
    """
    users = db.query(User).all()
    return users


# Get a specific user by ID (GET) - This should be a protected route
@router.get("/users/{user_id}", response_model=UserBase)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Get a specific user by their ID.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Update an existing user (PUT) - This should be a protected route
@router.put("/users/{user_id}", response_model=UserBase)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
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
        db_user.password = hash_password(
            user_update.password
        )  # Hash the new password

    db.commit()
    db.refresh(db_user)
    return db_user


# Delete a user by ID (DELETE) - This should be a protected route
@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Delete a user by their ID.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}


# Login endpoint to generate JWT token (POST)
@router.post("/users/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    """
    Login and return an access token.
    """
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user is None or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Create JWT token
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}
