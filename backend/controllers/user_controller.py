from sqlalchemy.orm import Session
from services.user_service import fetch_all_users, create_user ,fetch_users_by_role
from schemas.user_schema import UserCreate

def get_all_users(db: Session):
    return fetch_all_users(db)

def add_user(db: Session, user_data: UserCreate):
    return create_user(db, user_data)

def get_users_by_role_controller(db: Session, role: str):
    """Get users filtered by role name"""
    return fetch_users_by_role(db, role)
