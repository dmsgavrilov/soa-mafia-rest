from datetime import datetime
from typing import List

from pydantic import BaseModel, validator


class BaseGame(BaseModel):
    status: str
    start_date: datetime
    end_date: datetime


class CreateGame(BaseGame):
    pass

    @validator("status")
    def sex_validation(cls, v, values, **kwargs):
        if v not in ("mafia won", "citizens won"):
            raise ValueError("Invalid status value. Must be in ('mafia won', 'citizens won')")
        return v


class UpdateGame(BaseModel):
    pass


class GetGame(BaseGame):
    id: int

    class Config:
        orm_mode = True


class GetGames(BaseModel):
    data: List[GetGame]
    count: int
