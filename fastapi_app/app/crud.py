from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate
from app.auth import get_password_hash, verify_password
from app.logger import logger

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User {db_user.email} created successfully.")
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        logger.warning(f"Failed login attempt for {email}.")
        return None
    logger.info(f"User {email} logged in successfully.")
    return user
