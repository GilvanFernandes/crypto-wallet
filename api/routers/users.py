from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from models import User
from schemas import UserCreate, UserUpdate, UserResponse, Token
from crud import create_user, get_user_by_email, update_user
from passlib.context import CryptContext
from dependencies import get_db, verify_password, create_access_token, get_current_user

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    """Criar novo usuário"""
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    db_user = create_user(db, user)
    return db_user

@router.put("/me", response_model=UserResponse)
def update_user_route(user_update: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Atualizar dados do usuário logado"""
    existing_user = db.query(User).filter(User.email == user_update.email, User.id != current_user.id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    db_user = update_user(db, current_user, user_update)
    return db_user

@router.post("/login", response_model=Token)
def login_route(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Autenticar usuário e gerar token JWT"""
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}