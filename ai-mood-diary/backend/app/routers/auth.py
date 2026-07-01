from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.user import UserRegister, UserLogin, UserUpdate, UserResponse, TokenResponse
from ..services import auth_service
from ..utils.jwt import verify_token

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/register", response_model=TokenResponse)
def register(data: UserRegister, db: Session = Depends(get_db)):
    try:
        return auth_service.register(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    try:
        return auth_service.login(db, data.username, data.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me", response_model=UserResponse)
def get_me(payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    try:
        return auth_service.get_user(db, payload["user_id"])
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/me", response_model=UserResponse)
def update_me(data: UserUpdate, payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    try:
        return auth_service.update_user(db, payload["user_id"], data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
