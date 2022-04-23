from typing import List, Optional

from pydantic import BaseModel, EmailStr, AnyUrl, validator
from pydantic.types import constr

from app.config import settings


class BaseUser(BaseModel):
    email: EmailStr
    nickname: str
    img_url: Optional[AnyUrl]
    sex: str
    is_superuser: bool


class CreateUser(BaseUser):
    password: constr(max_length=32, min_length=8)

    @validator("sex")
    def sex_validation(cls, v, values, **kwargs):
        if v not in ("f", "m"):
            raise ValueError("Invalid scope(s)")
        return v


class UpdateUser(BaseModel):
    nickname: str
    img_url: Optional[AnyUrl]
    sex: str
    password: Optional[constr(max_length=32, min_length=8)]

    @validator("sex")
    def sex_validation(cls, v, values, **kwargs):
        if v not in ("f", "m"):
            raise ValueError("Invalid scope(s)")
        return v


class GetUser(BaseUser):
    id: int

    class Config:
        orm_mode = True


class GetUsers(BaseModel):
    data: List[GetUser]
    count: int
