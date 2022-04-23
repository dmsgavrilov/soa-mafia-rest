import datetime
import bcrypt

import jwt

from app.config import settings

ALGORITHM = "HS256"


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password.encode())


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt()).decode()


def create_access_token(payload: dict) -> str:
    expire = datetime.datetime.utcnow() + datetime.timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload["exp"] = expire
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_access_token(token) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)
