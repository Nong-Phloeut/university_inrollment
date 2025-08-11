from sqlalchemy.orm import Session
from services.user_service import fetch_all_users, create_user
from schemas.user_schema import UserCreate

def get_all_users(db: Session):
    return fetch_all_users(db)

def add_user(db: Session, user_data: UserCreate):
    return create_user(db, user_data)
