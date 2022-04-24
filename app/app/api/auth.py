from typing import Any

from fastapi.security import OAuth2PasswordRequestForm

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.crud.users import user as user_crud
from app.models import User
from app.schemas.token import Token
from app.schemas.users import GetUser
from app.utils import security

router = APIRouter()


@router.post("/auth/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = user_crud.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    payload = {
        "email": user.email
    }
    return {
        "access_token": security.create_access_token(payload),
        "token_type": "bearer",
    }


@router.post("/auth/test-token", response_model=GetUser)
def test_token(current_user: User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user
