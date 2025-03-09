from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.vote import Vote  # Import the Vote model
from schemas.vote import VoteCreate, VoteBase  # Import the schemas

router = APIRouter()


# Create a new vote (POST)
@router.post("/", response_model=VoteBase)
def create_vote(vote: VoteCreate, db: Session = Depends(get_db)):
    """
    Create a new vote in the database.
    """
    # Check if the user and menu exist
    db_user = db.query(Vote).filter(Vote.user_id == vote.user_id).first()
    db_menu = db.query(Vote).filter(Vote.menu_id == vote.menu_id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")

    db_vote = Vote(user_id=vote.user_id, menu_id=vote.menu_id)
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return db_vote


# Get all votes (GET)
@router.get("/", response_model=List[VoteBase])
def get_votes(db: Session = Depends(get_db)):
    """
    Get all votes from the database.
    """
    votes = db.query(Vote).all()
    return votes


# Get a specific vote by ID (GET)
@router.get("/{vote_id}", response_model=VoteBase)
def get_vote(vote_id: int, db: Session = Depends(get_db)):
    """
    Get a specific vote by its ID.
    """
    db_vote = db.query(Vote).filter(Vote.id == vote_id).first()
    if db_vote is None:
        raise HTTPException(status_code=404, detail="Vote not found")
    return db_vote


# Delete a vote by ID (DELETE)
@router.delete("/{vote_id}")
def delete_vote(vote_id: int, db: Session = Depends(get_db)):
    """
    Delete a vote by its ID.
    """
    db_vote = db.query(Vote).filter(Vote.id == vote_id).first()
    if db_vote is None:
        raise HTTPException(status_code=404, detail="Vote not found")

    db.delete(db_vote)
    db.commit()
    return {"message": "Vote deleted successfully"}
