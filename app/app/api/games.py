from fastapi import (
    APIRouter,
    Depends,
    status,
    Response
)

from sqlalchemy.orm import Session

from app.api import deps
from app.crud import game
from app.models import User
from app.schemas.games import CreateGame, GetGame, GetGames

router = APIRouter()


@router.post("", response_model=GetGame)
def create_game(
        data: CreateGame, db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_superuser)
):
    return game.create(db, obj_in=data)


@router.get("", response_model=GetGames)
def get_games(
        db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 10,
        current_user: User = Depends(deps.get_current_user)
):
    games, count = game.get_many(db, skip=skip, limit=limit)
    return {"data": games, "count": count}


@router.get("/{game_id}", response_model=GetGame)
def get_game(
        game_id: int,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_user)
):
    return game.get_by_id(db, game_id)


@router.delete("/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_game(
        game_id: int, db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_superuser)
):
    game.delete_user(db, game_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
