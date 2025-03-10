from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import UserResponse, UserCreate
from app.models import User
from app.auth import verify_access_token, get_password_hash
from typing import List
from app.logger import logger

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get current authenticated user
def get_current_user(token: str, db: Session = Depends(get_db)):
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.query(User).filter(User.email == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return user

# Get all users (Admin Only)
@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = db.query(User).all()
    logger.info(f"User {current_user.email} retrieved all users.")
    return users

# Get single user by ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    logger.info(f"User {current_user.email} retrieved user {user.email}.")
    return user

# Update own user data
@router.put("/", response_model=UserResponse)
def update_user(user_update: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    current_user.hashed_password = get_password_hash(user_update.password)
    db.commit()
    db.refresh(current_user)
    logger.info(f"User {current_user.email} updated their profile.")
    return current_user

# Delete own user account
@router.delete("/", response_model=dict)
def delete_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db.delete(current_user)
    db.commit()
    logger.warning(f"User {current_user.email} deleted their account.")
    return {"message": "User deleted successfully"}
