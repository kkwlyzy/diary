import bcrypt as _bcrypt
from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserRegister, UserUpdate
from ..utils.jwt import create_access_token


def _hash_password(password: str) -> str:
    return _bcrypt.hashpw(password.encode("utf-8"), _bcrypt.gensalt()).decode("utf-8")


def _verify_password(password: str, password_hash: str) -> bool:
    return _bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def register(db: Session, data: UserRegister) -> dict:
    from .captcha_service import validate_captcha
    if not validate_captcha(data.captcha_session, data.captcha):
        raise ValueError("验证码错误")
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise ValueError("用户名已存在")
    user = User(
        username=data.username,
        password_hash=_hash_password(data.password),
        nickname=data.nickname or data.username,
        email=data.email,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer", "user": user}


def login(db: Session, username: str, password: str) -> dict:
    user = db.query(User).filter(User.username == username).first()
    if not user or not _verify_password(password, user.password_hash):
        raise ValueError("用户名或密码错误")
    token = create_access_token({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer", "user": user}


def get_user(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("用户不存在")
    return user


def update_user(db: Session, user_id: int, data: UserUpdate) -> User:
    user = get_user(db, user_id)
    if data.nickname is not None:
        user.nickname = data.nickname
    if data.avatar is not None:
        user.avatar = data.avatar
    if data.email is not None:
        user.email = data.email
    db.commit()
    db.refresh(user)
    return user
