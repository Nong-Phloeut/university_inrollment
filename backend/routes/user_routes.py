from fastapi import APIRouter, Depends, Query ,HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from controllers.user_controller import get_all_users, add_user, get_users_by_role_controller
from schemas.user_schema import UserCreate, UserRead ,LoginRequest
from models import User
import bcrypt
import secrets

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[UserRead])
def list_users(role: str = Query(None), db: Session = Depends(get_db)):
    if role:
        return get_users_by_role_controller(db, role)
    return get_all_users(db)

# @router.post("/", response_model=UserRead)
# def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
#     return add_user(db, user)
@router.post("/", response_model=UserRead, status_code=201)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user_in.password)
    new_user = User(
        name=user_in.name,
        email=user_in.email,
        password=hashed_password,
        role=user_in.role,
        status=user_in.status
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/by-role", response_model=List[UserRead])
def get_users_by_role_endpoint(role: int, db: Session = Depends(get_db)):
    return get_users_by_role_controller(db, role)


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
   # Generate fake token
    fake_token = secrets.token_hex(16)  # 32-char random hex string

    # Generate your token here (JWT or other)
    return {"message": "Login successful", "user_id": user.id ,"token":fake_token}

def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


