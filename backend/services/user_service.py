from sqlalchemy.orm import Session
from models import User
from schemas.user_schema import UserCreate

def fetch_all_users(db: Session):
    return db.query(User).all()

def create_user(db: Session, user_data: UserCreate):
    user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        password=user_data.password,  # ? Hash in real apps
        role_id=user_data.role_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def fetch_users_by_role(db: Session, role_id: int):
    return db.query(User).filter(User.role_id == role_id).all()


